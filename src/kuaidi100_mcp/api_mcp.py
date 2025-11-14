import os

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import Field

# 创建MCP服务器实例
mcp = FastMCP(
    name="kuaidi100_mcp",
    instructions="This is a MCP server for kuaidi100 API."
)

"""
获取环境变量中的API密钥, 用于调用快递100API
环境变量名为: KUAIDI100_API_KEY, 在客户端侧通过配置文件进行设置传入
获取方式请参考：https://poll.kuaidi100.com/manager/page/myinfo/enterprise
"""

kuaidi100_api_key = os.getenv('KUAIDI100_API_KEY')
kuaidi100_api_url = "https://api.kuaidi100.com/stdio/"

@mcp.tool(name="query_trace", description="查询物流轨迹服务，传入快递单号和手机号，获取对应快递的物流轨迹")
async def query_trace(kuaidi_num: str = Field(description="快递单号"),
                      phone: str = Field(description="手机号，当快递单号为SF开头时必填；如果用户没告知手机号，则不调用服务，继续追问用户手机号是什么"), default="") -> str:
    """
    查询物流轨迹服务, 根据快递单号查询物流轨迹
    """
    if not kuaidi100_api_key:
        return 'error: KUAIDI100_API_KEY not set'

    method = "queryTrace"
    # 调用查询物流轨迹API
    params = {
        "key": kuaidi100_api_key,
        "kuaidiNum": kuaidi_num,
        "phone": phone,
    }
    response = await http_get(kuaidi100_api_url + method, params)
    return response


@mcp.tool(name="estimate_time", description="通过快递公司编码、收寄件地址、下单时间、业务/产品类型来预估快递可送达的时间，以及过程需要花费的时间；用于寄件前快递送达时间预估")
async def estimate_time(kuaidi_com: str = Field(description="快递公司编码，一律用小写字母；目前仅支持：京东：jd，跨越：kuayue，顺丰：shunfeng，顺丰快运：shunfengkuaiyun，中通：zhongtong，德邦快递：debangkuaidi，EMS：ems，EMS-国际件：emsguoji，邮政国内:youzhengguonei，国际包裹：youzhengguoji，申通：shentong，圆通：yuantong，韵达：yunda，宅急送：zhaijisong，芝麻开门：zhimakaimen，联邦快递：lianbangkuaidi，天地华宇：tiandihuayu，安能快运：annengwuliu，京广速递：jinguangsudikuaijian，加运美：jiayunmeiwuliu，极兔速递：jtexpress"),
                        from_loc: str = Field(description="出发地（地址需包含3级及以上），例如：广东深圳南山区；如果没有省市区信息的话请补全，如广东深圳改为广东省深圳市南山区"),
                        to_loc: str = Field(description="目的地（地址需包含3级及以上），例如：北京海淀区；如果没有省市区信息的话请补全，如广东深圳改为广东省深圳市南山区。如果用户没告知目的地，则不调用服务，继续追问用户目的地是哪里"),
                        order_time: str = Field(description="下单时间，格式要求yyyy-MM-dd HH:mm:ss，例如：2023-08-08 08:08:08；如果用户没告知下单时间，则不传", default=""),
                        exp_type: str = Field(description="业务或产品类型，如：标准快递")) -> str:
    """
    通过快递公司编码、收寄件地址、下单时间和业务/产品类型来预估快递可送达的时间，以及过程需要花费的时间；用于寄件前快递送达时间预估",
    """
    if not kuaidi100_api_key:
        return 'error: KUAIDI100_API_KEY not set'

    method = "estimateTime"

    # 调用查询物流轨迹API
    params = {
        "key": kuaidi100_api_key,
        "kuaidicom": kuaidi_com,
        "from": from_loc,
        "to": to_loc,
        "orderTime": order_time,
        "expType": exp_type,
    }
    response = await http_get(kuaidi100_api_url + method, params)

    return response


@mcp.tool(name="estimate_time_with_logistic", description="通过快递公司编码、收寄件地址、下单时间、历史物流轨迹信息来预估快递送达的时间；用于在途快递的到达时间预估")
async def estimate_time_with_logistic(kuaidi_com: str = Field(description="快递公司编码，一律用小写字母；目前仅支持：京东：jd，跨越：kuayue，顺丰：shunfeng，顺丰快运：shunfengkuaiyun，中通：zhongtong，德邦快递：debangkuaidi，EMS：ems，EMS-国际件：emsguoji，邮政国内:youzhengguonei，国际包裹：youzhengguoji，申通：shentong，圆通：yuantong，韵达：yunda，宅急送：zhaijisong，芝麻开门：zhimakaimen，联邦快递：lianbangkuaidi，天地华宇：tiandihuayu，安能快运：annengwuliu，京广速递：jinguangsudikuaijian，加运美：jiayunmeiwuliu，极兔速递：jtexpress"),
                                      from_loc: str = Field(description="出发地（地址需包含3级及以上），例如：广东深圳南山区；如果没有省市区信息的话请补全，如广东深圳改为广东省深圳市南山区"),
                                      to_loc: str = Field(description="目的地（地址需包含3级及以上），例如：北京海淀区；如果没有省市区信息的话请补全，如广东深圳改为广东省深圳市南山区。如果用户没告知目的地，则不调用服务，继续追问用户目的地是哪里"),
                                      order_time: str = Field(description="下单时间，格式要求yyyy-MM-dd HH:mm:ss，例如：2023-08-08 08:08:08；如果用户没告知下单时间，则不传",default=""),
                                      exp_type: str = Field(description="业务或产品类型，如：标准快递"),
                                      logistic: str = Field(description="历史物流轨迹信息，用于预测在途时还需多长时间到达；一般情况下取query_trace服务返回数据的历史物流轨迹信息转为json数组即可，数据格式为：[{\"time\":\"2025-05-09 13:15:26\",\"context\":\"您的快件离开【吉林省吉林市桦甸市】，已发往【长春转运中心】\"},{\"time\":\"2025-05-09 12:09:38\",\"context\":\"您的快件在【吉林省吉林市桦甸市】已揽收\"}]；time为物流轨迹节点的时间，context为在该物流轨迹节点的描述")) -> str:
    """
    通过快递公司编码、收寄件地址、下单时间和业务/产品类型、历史物流轨迹信息来预估快递送达的时间；用于在途快递的到达时间预估。接口返回的now属性为当前时间，使用arrivalTime-now计算预计还需运输时间
    """
    if not kuaidi100_api_key:
        return 'error: KUAIDI100_API_KEY not set'

    method = "estimateTimeWithLogistic"
    # 调用查询物流轨迹API
    params = {
        "key": kuaidi100_api_key,
        "kuaidicom": kuaidi_com,
        "from": from_loc,
        "to": to_loc,
        "orderTime": order_time,
        "expType": exp_type,
        "logistic": logistic,
    }
    response = await http_get(kuaidi100_api_url + method, params)
    return response


@mcp.tool(name="estimate_price", description="通过快递公司、收寄件地址和重量，预估快递公司运费")
async def estimate_price(kuaidi_com: str = Field(description="快递公司的编码，一律用小写字母；目前仅支持：顺丰：shunfeng，京东：jd，德邦快递：debangkuaidi，圆通：yuantong，中通：zhongtong，申通：shentong，韵达：yunda，EMS：ems"),
                         rec_addr: str = Field(description="收件地址，如”广东深圳南山区”；如果没有省市信息的话请补全，如广东深圳改为广东省深圳市。如果用户没告知收件地址，则不调用服务，继续追问用户收件地址是哪里"),
                         send_addr: str = Field(description="寄件地址，如”北京海淀区”；如果没有省市信息的话请补全，如广东深圳改为广东省深圳市。如果用户没告知寄件地址，则不调用服务，继续追问用户寄件地址是哪里"),
                         weight: str = Field(description="重量，默认单位为kg，参数无需带单位，如1.0；默认重量为1kg")) -> str :
    """
    通过快递公司、收寄件地址和重量，预估快递公司运费
    """
    if not kuaidi100_api_key:
        return 'error: KUAIDI100_API_KEY not set'

    method = "estimatePrice"

    # 调用查询物流轨迹API
    params = {
        "key": kuaidi100_api_key,
        "kuaidicom": kuaidi_com,
        "recAddr": rec_addr,
        "sendAddr": send_addr,
        "weight": weight,
    }
    response = await http_get(kuaidi100_api_url + method, params)
    return response


async def http_get(url: str = Field(description="请求的URL"),
                   params: dict = Field(description="请求的参数")) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.text
    except httpx.HTTPError as e:
        raise Exception(f"HTTP request failed: {str(e)}") from e
    except KeyError as e:
        raise Exception(f"Failed to parse response: {str(e)}") from e


if __name__ == "__main__":
    mcp.run(transport="streamable-http")

