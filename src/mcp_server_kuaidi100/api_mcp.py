import os

import httpx
from httpx import Response
from mcp.server.fastmcp import FastMCP
import mcp.types as types
from mcp.types import TextContent, ImageContent, EmbeddedResource

# 创建MCP服务器实例
mcp = FastMCP(
    name="mcp-server-kuaidi100",
    version="1.0.0",
    instructions="This is a MCP server for kuaidi100 API."
)

"""
获取环境变量中的API密钥, 用于调用快递100API
环境变量名为: KUAIDI100_API_KEY, 在客户端侧通过配置文件进行设置传入
获取方式请参考：https://poll.kuaidi100.com/manager/page/myinfo/enterprise
"""

kuaidi100_api_key = os.getenv('KUAIDI100_API_KEY')
kuaidi100_api_url = "https://api.kuaidi100.com/stdio/"


async def query_trace(arguments: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    查询物流轨迹服务, 根据快递单号查询物流轨迹
    """
    kuaidi_num = arguments.get("kuaidi_num", "")
    phone = arguments.get("phone", "")
    method = "queryTrace"

    # 调用查询物流轨迹API
    params = {
        "key": f"{kuaidi100_api_key}",
        "kuaidiNum": f"{kuaidi_num}",
        "phone": f"{phone}",
    }

    response = await http_get(kuaidi100_api_url + method, params)
    return [types.TextContent(type="text", text=response.text)]


async def estimate_time(arguments: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    通过快递公司编码、收寄件地址、下单时间和业务/产品类型来预估快递可送达的时间，以及过程需要花费的时间；用于寄件前快递送达时间预估",
    """
    method = "estimateTime"
    kuaidi_com = arguments.get("kuaidi_com", "")
    from_param = arguments.get("from", "")
    to_param = arguments.get("to", "")
    order_time = arguments.get("order_time", "")
    exp_type = arguments.get("exp_type", "")

    # 调用查询物流轨迹API
    params = {
        "key": f"{kuaidi100_api_key}",
        "kuaidicom": f"{kuaidi_com}",
        "from": f"{from_param}",
        "to": f"{to_param}",
        "orderTime": f"{order_time}",
        "expType": f"{exp_type}",
    }
    response = await http_get(kuaidi100_api_url + method, params)

    return [types.TextContent(type="text", text=response.text)]


async def estimate_time_with_logistic(arguments: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    通过快递公司编码、收寄件地址、下单时间和业务/产品类型、历史物流轨迹信息来预估快递送达的时间；用于在途快递的到达时间预估。接口返回的now属性为当前时间，使用arrivalTime-now计算预计还需运输时间
    """
    method = "estimateTimeWithLogistic"
    kuaidi_com = arguments.get("kuaidi_com", "")
    from_param = arguments.get("from", "")
    to_param = arguments.get("to", "")
    order_time = arguments.get("order_time", "")
    exp_type = arguments.get("exp_type", "")
    logistic = arguments.get("logistic", "")

    # 调用查询物流轨迹API
    params = {
        "key": f"{kuaidi100_api_key}",
        "kuaidicom": f"{kuaidi_com}",
        "from": f"{from_param}",
        "to": f"{to_param}",
        "orderTime": f"{order_time}",
        "expType": f"{exp_type}",
        "logistic": f"{logistic}",
    }
    response = await http_get(kuaidi100_api_url + method, params)
    return [types.TextContent(type="text", text=response.text)]


async def estimate_price(arguments: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    通过快递公司、收寄件地址和重量，预估快递公司运费
    """
    method = "estimatePrice"
    kuaidi_com = arguments.get("kuaidi_com", "")
    rec_addr = arguments.get("rec_addr", "")
    send_addr = arguments.get("send_addr", "")
    weight = arguments.get("weight", "")

    # 调用查询物流轨迹API
    params = {
        "key": f"{kuaidi100_api_key}",
        "kuaidicom": f"{kuaidi_com}",
        "recAddr": f"{rec_addr}",
        "sendAddr": f"{send_addr}",
        "weight": f"{weight}",
    }
    response = await http_get(kuaidi100_api_url + method, params)
    return [types.TextContent(type="text", text=response.text)]


async def list_tools() -> list[types.Tool]:
    """
    列出所有可用的工具。

    Args:
        None.

    Returns:
        list (types.Tool): 包含了所有可用的工具, 每个工具都包含了名称、描述、输入schema三个属性.
    """
    return [
        types.Tool(
            name="query_trace",
            description="查询物流轨迹服务，传入快递单号和手机号，获取对应快递的物流轨迹",
            inputSchema={
                "type": "object",
                "required": ["kuaidi_num"],
                "properties": {
                    "kuaidi_num": {
                        "type": "string",
                        "description": "待查询的快递单号",
                    },
                    "phone": {
                        "type": "string",
                        "description": "手机号，非必填，当快递公司为顺丰时需要填入",

                    }
                }
            }
        ),
        types.Tool(
            name="estimate_time",
            description="通过快递公司编码、收寄件地址、下单时间和业务/产品类型来预估快递可送达的时间，以及过程需要花费的时间；用于寄件前快递送达时间预估",
            inputSchema={
                "type": "object",
                "required": ["kuaidi_com", "from", "to"],
                "properties": {
                    "kuaidi_com": {
                        "type": "string",
                        "description": "快递公司编码，一律用小写字母；目前仅支持：京东:jd, 跨越:kuayue, 顺丰:shunfeng, 顺丰快运:shunfengkuaiyun, 中通:zhongtong, 德邦快递:debangkuaidi,EMS:ems,EMS - 国际件:emsguoji, 邮政国内:youzhengguonei, 国际包裹:youzhengguoji, 申通:shentong, 圆通:yuantong, 韵达:yunda, 宅急送:zhaijisong, 芝麻开门:zhimakaimen, 联邦快递:lianbangkuaidi, 天地华宇:tiandihuayu, 安能快运:annengwuliu, 京广速递:jinguangsudikuaijian, 加运美:jiayunmeiwuliu, 极兔速递:jtexpress",
                    },
                    "from": {
                        "type": "string",
                        "description": "出发地（地址需包含3级及以上），例如：广东深圳南山区；如果没有省市区信息的话请补全，如广东深圳改为广东省深圳市南山区",
                    },
                    "to": {
                        "type": "string",
                        "description": "目的地（地址需包含3级及以上），例如：北京海淀区；如果没有省市区信息的话请补全，如广东深圳改为广东省深圳市南山区。如果用户没告知目的地，则不调用服务，继续追问用户目的地是哪里",
                    },
                    "order_time": {
                        "type": "string",
                        "description": "下单时间，格式要求yyyy-MM-dd HH:mm:ss, 例如：2023-08-08 08:08:08；如果没有传入则取当前时间；需要注意的是：填写明天或者后天等情况，则以今天为基准日，再取明天或者后天",
                    },
                    "exp_type": {
                        "type": "string",
                        "description": "业务或产品类型，如：标准快递",
                    }
                }
            }
        ),
        types.Tool(
            name="estimate_time_with_logistic",
            description="通过快递公司编码、收寄件地址、下单时间和业务/产品类型、历史物流轨迹信息来预估快递送达的时间。用于在途快递的到达时间预估；接口返回的now属性为当前时间，使用arrivalTime-now计算预计还需运输时间",
            inputSchema={
                "type": "object",
                "required": ["kuaidi_com", "from", "to", "order_time", "logistic"],
                "properties": {
                    "kuaidi_com": {
                        "type": "string",
                        "description": "快递公司编码，一律用小写字母；目前仅支持：京东:jd, 跨越:kuayue, 顺丰:shunfeng, 顺丰快运:shunfengkuaiyun, 中通:zhongtong, 德邦快递:debangkuaidi,EMS:ems,EMS - 国际件:emsguoji, 邮政国内:youzhengguonei, 国际包裹:youzhengguoji, 申通:shentong, 圆通:yuantong, 韵达:yunda, 宅急送:zhaijisong, 芝麻开门:zhimakaimen, 联邦快递:lianbangkuaidi, 天地华宇:tiandihuayu, 安能快运:annengwuliu, 京广速递:jinguangsudikuaijian, 加运美:jiayunmeiwuliu, 极兔速递:jtexpress",
                    },
                    "from": {
                        "type": "string",
                        "description": "出发地（地址需包含3级及以上），例如：广东深圳南山区；如果没有省市区信息的话请补全，如广东深圳改为广东省深圳市南山区",
                    },
                    "to": {
                        "type": "string",
                        "description": "目的地（地址需包含3级及以上），例如：北京海淀区；如果没有省市区信息的话请补全，如广东深圳改为广东省深圳市南山区。如果用户没告知目的地，则不调用服务，继续追问用户目的地是哪里",
                    },
                    "order_time": {
                        "type": "string",
                        "description": "下单时间，格式要求yyyy-MM-dd HH:mm:ss, 例如：2023-08-08 08:08:08；如果没有传入则取当前时间；需要注意的是：填写明天或者后天等情况，则以今天为基准日，再取明天或者后天",
                    },
                    "exp_type": {
                        "type": "string",
                        "description": "业务或产品类型，如：标准快递",
                    },
                    "logistic": {
                        "type": "string",
                        "description": "历史物流轨迹信息，用于预测在途时还需多长时间到达；一般情况下取query_trace服务返回数据的data数组转为string即可，数据为JSON数组格式，如：[{\"time\":\"2025-05-09 13:15:26\",\"context\":\"您的快件离开【吉林省吉林市桦甸市】，已发往【长春转运中心】\"},{\"time\":\"2025-05-09 12:09:38\",\"context\":\"您的快件在【吉林省吉林市桦甸市】已揽收\"}]；time为物流轨迹节点的时间，context为在该物流轨迹节点的描述",
                    }
                }
            }
        ),
        types.Tool(
            name="estimate_price",
            description="通过快递公司、收寄件地址和重量，预估快递公司运费",
            inputSchema={
                "type": "object",
                "required": ["kuaidi_com", "rec_addr", "send_addr", "weight"],
                "properties": {
                    "kuaidi_com": {
                        "type": "string",
                        "description": "快递公司的编码，一律用小写字母；目前仅支持：顺丰:shunfeng,京东:jd,德邦快递:debangkuaidi,圆通:yuantong,中通:zhongtong,申通:shentong,韵达:yunda,EMS:ems",
                    },
                    "rec_addr": {
                        "type": "string",
                        "description": "收件地址，如”广东深圳南山区”；如果没有省市信息的话请补全，如广东深圳改为广东省深圳市。如果用户没告知收件地址，则不调用服务，继续追问用户收件地址是哪里",

                    },
                    "send_addr": {
                        "type": "string",
                        "description": "寄件地址，如”北京海淀区”；如果没有省市信息的话请补全，如广东深圳改为广东省深圳市。如果用户没告知寄件地址，则不调用服务，继续追问用户寄件地址是哪里",
                    },
                    "weight": {
                        "type": "string",
                        "description": "重量，默认单位为kg，参数无需带单位，如1.0；默认重量为1kg",

                    }
                }
            }
        )

    ]


async def dispatch(name: str, arguments: dict) -> list[TextContent | ImageContent | EmbeddedResource] | None:
    """
    根据名称调度对应的工具函数, 并返回处理结果.

    Args:
        name (str): 工具函数的名称, 可选值为: "map_geocode", "map_reverse_geocode",
            "map_search_places", "map_place_details", "map_distance_matrix",
            "map_directions", "map_weather", "map_ip_location", "map_road_traffic",
            "map_mark".
        arguments (dict): 传递给工具函数的参数字典, 包括必要和可选参数.

    Returns:
        list[types.TextContent | types.ImageContent | types.EmbeddedResource]: 返回一个列表, 包含文本内容、图片内容或嵌入资源类型的元素.

    Raises:
        ValueError: 如果提供了未知的工具名称.
    """
    match name:
        case "query_trace":
            return await query_trace(arguments)
        case "estimate_time":
            return await estimate_time(arguments)
        case "estimate_time_with_logistic":
            return await estimate_time_with_logistic(arguments)
        case "estimate_price":
            return await estimate_price(arguments)
        case _:
            raise ValueError(f"Unknown tool: {name}")


async def http_get(url: str, params: dict) -> Response:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

    except httpx.HTTPError as e:
        raise Exception(f"HTTP request failed: {str(e)}") from e
    except KeyError as e:
        raise Exception(f"Failed to parse response: {str(e)}") from e
    return response


# 注册list_tools方法
mcp._mcp_server.list_tools()(list_tools)
# 注册dispatch方法
mcp._mcp_server.call_tool()(dispatch)

if __name__ == "__main__":
    mcp.run()
