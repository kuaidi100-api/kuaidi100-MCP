import httpx
from mcp.server.fastmcp import FastMCP, Context
from pydantic import Field

# 创建MCP服务器实例
mcp = FastMCP(
    name="kuaidi100_mcp",
    instructions="This is a MCP server for kuaidi100 API.",
    stateless_http=True
)

"""
获取环境变量中的API密钥, 用于调用快递100API
环境变量名为: KUAIDI100_API_KEY, 在客户端侧通过配置文件进行设置传入
获取方式请参考：https://poll.kuaidi100.com/manager/page/myinfo/enterprise
"""
kuaidi100_api_url = "https://api.kuaidi100.com/stdio/"

@mcp.tool(name="query_trace", description="根据快递单号，返回对应的实时物流轨迹信息")
async def query_trace(ctx: Context,
                      kuaidi_num: str = Field(description="快递单号"),
                      phone: str = Field(description="手机号，仅顺丰速运、顺丰快运、中通快递必填", default="")) -> str:
    """
    查询物流轨迹服务, 根据快递单号查询物流轨迹
    """
    kuaidi100_api_key = get_api_key(ctx)
    response_format = get_response_format(ctx)
    method = "queryTrace"

    # 调用查询物流轨迹API
    params = {
        "key": kuaidi100_api_key,
        "responseFormat": response_format,
        "kuaidiNum": kuaidi_num,
        "phone": phone,
    }
    response = await http_get(kuaidi100_api_url + method, params)
    return response


@mcp.tool(name="estimate_time", description="通过快递公司编码、收寄件地址、下单时间、业务/产品类型来预估快递可送达的时间，以及过程需要花费的时间；用于寄件前快递送达时间预估")
async def estimate_time(ctx: Context,
                        kuaidi_com: str = Field(description="快递公司编码，一律用小写字母；目前仅支持：圆通：yuantong，中通：zhongtong，顺丰：shunfeng，顺丰快运：shunfengkuaiyun，京东：jd，极兔速递：jtexpress，申通：shentong，韵达：yunda，EMS：ems，跨越：kuayue，德邦快递：debangkuaidi，EMS-国际件：emsguoji，邮政国内:youzhengguonei，国际包裹：youzhengguoji，宅急送：zhaijisong，芝麻开门：zhimakaimen，联邦快递：lianbangkuaidi，天地华宇：tiandihuayu，安能快运：annengwuliu，京广速递：jinguangsudikuaijian，加运美：jiayunmeiwuliu"),
                        from_loc: str = Field(description="出发地，例如：广东省深圳市南山区"),
                        to_loc: str = Field(description="目的地，例如：北京海淀区"),
                        order_time: str = Field(description="下单时间，格式要求yyyy-MM-dd HH:mm:ss，例如：2023-08-08 08:08:08", default=""),
                        exp_type: str = Field(description="业务/产品类型，如：标准快递")) -> str:
    """
    通过快递公司编码、收寄件地址、下单时间和业务/产品类型来预估快递可送达的时间，以及过程需要花费的时间；用于寄件前快递送达时间预估",
    """
    kuaidi100_api_key = get_api_key(ctx)
    response_format = get_response_format(ctx)
    method = "estimateTime"

    # 调用查询物流轨迹API
    params = {
        "key": kuaidi100_api_key,
        "responseFormat": response_format,
        "kuaidicom": kuaidi_com,
        "from": from_loc,
        "to": to_loc,
        "orderTime": order_time,
        "expType": exp_type,
    }
    response = await http_get(kuaidi100_api_url + method, params)

    return response


@mcp.tool(name="estimate_time_with_logistic", description="通过快递公司编码、收寄件地址、下单时间、历史物流轨迹信息来预估快递送达的时间；用于在途快递的到达时间预估")
async def estimate_time_with_logistic(ctx: Context,
                                      kuaidi_com: str = Field(description="快递公司编码，一律用小写字母；目前仅支持：圆通：yuantong，中通：zhongtong，顺丰：shunfeng，顺丰快运：shunfengkuaiyun，京东：jd，极兔速递：jtexpress，申通：shentong，韵达：yunda，EMS：ems，跨越：kuayue，德邦快递：debangkuaidi，EMS-国际件：emsguoji，邮政国内:youzhengguonei，国际包裹：youzhengguoji，宅急送：zhaijisong，芝麻开门：zhimakaimen，联邦快递：lianbangkuaidi，天地华宇：tiandihuayu，安能快运：annengwuliu，京广速递：jinguangsudikuaijian，加运美：jiayunmeiwuliu"),
                                      from_loc: str = Field(description="出发地，例如：广东省深圳市南山区"),
                                      to_loc: str = Field(description="目的地，例如：北京市海淀区"),
                                      order_time: str = Field(description="下单时间，格式要求yyyy-MM-dd HH:mm:ss, 例如：2023-08-08 08:08:08；取query_trace服务返回数据中最早物流轨迹的时间即可",default=""),
                                      exp_type: str = Field(description="业务或产品类型，如：标准快递"),
                                      logistic: str = Field(description="历史物流轨迹信息，用于预测在途时还需多长时间到达；一般情况下取query_trace服务返回数据的历史物流轨迹信息转为json数组即可，数据格式为：[{\"time\":\"2025-05-09 13:15:26\",\"context\":\"您的快件离开【吉林省吉林市桦甸市】，已发往【长春转运中心】\"},{\"time\":\"2025-05-09 12:09:38\",\"context\":\"您的快件在【吉林省吉林市桦甸市】已揽收\"}]；time为物流轨迹节点的时间，context为在该物流轨迹节点的描述"),
                                      ) -> str:
    """
    通过快递公司编码、收寄件地址、下单时间和业务/产品类型、历史物流轨迹信息来预估快递送达的时间；用于在途快递的到达时间预估。接口返回的now属性为当前时间，使用arrivalTime-now计算预计还需运输时间
    """
    kuaidi100_api_key = get_api_key(ctx)
    response_format = get_response_format(ctx)
    method = "estimateTimeWithLogistic"
    # 调用查询物流轨迹API
    params = {
        "key": kuaidi100_api_key,
        "responseFormat": response_format,
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
async def estimate_price(ctx: Context,
                         kuaidi_com: str = Field(description="快递公司的编码，一律用小写字母；目前仅支持：顺丰：shunfeng，京东：jd，德邦快递：debangkuaidi，圆通：yuantong，中通：zhongtong，申通：shentong，韵达：yunda，EMS：ems"),
                         rec_addr: str = Field(description="收件地址，如广东深圳南山区"),
                         send_addr: str = Field(description="寄件地址，如北京海淀区"),
                         weight: str = Field(description="重量，默认单位为kg，参数无需带单位，如1.0；默认重量为1kg"),) -> str :
    """
    通过快递公司、收寄件地址和重量，预估快递公司运费
    """
    kuaidi100_api_key = get_api_key(ctx)
    response_format = get_response_format(ctx)
    method = "estimatePrice"

    # 调用查询物流轨迹API
    params = {
        "key": kuaidi100_api_key,
        "responseFormat": response_format,
        "kuaidicom": kuaidi_com,
        "recAddr": rec_addr,
        "sendAddr": send_addr,
        "weight": weight,
    }
    response = await http_get(kuaidi100_api_url + method, params)
    return response


def get_api_key(ctx: Context) -> str:
    """
    从header中获取快递100的API Key
    """
    headers = ctx.request_context.request.headers
    kuaidi100_api_key = (headers.get("KUAIDI100_API_KEY")
                         or headers.get("kuaidi100-api-key")
                         or headers.get("kuaidi100_api_key"))
    if not kuaidi100_api_key:
        raise Exception('error: KUAIDI100_API_KEY not set')
    return kuaidi100_api_key


def get_response_format(ctx: Context) -> str:
    """
    从header中获取数据返回格式类型
    """
    headers = ctx.request_context.request.headers
    response_format = (headers.get("responseFormat")
                         or headers.get("ResponseFormat")
                         or headers.get("response_format"))
    if not response_format:
        return 'markdown'
    return response_format


async def http_get(url: str,
                   params: dict) -> str:
    """
    发送HTTP GET请求
    """
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

