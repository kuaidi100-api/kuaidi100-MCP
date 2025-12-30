from typing import Optional

from pydantic import BaseModel, Field

from markdown_utils import objects_to_markdown_table


class QueryTraceVO(BaseModel):
    """物流查询结果的结构化模型"""
    kuaidiCom: str  # 快递公司编码，如 "yuantong"
    kuaidiName: str  # 快递公司名称，如 "圆通速递"
    kuaidiNum: str  # 快递单号
    state: str  # 当前物流状态，如 "揽收"、"在途"、"已签收"
    fromTo: str  # 起点 -> 目的地，格式如 "黑龙江,哈尔滨市,松北区,太阳岛 -> "

    class QueryTraceData(BaseModel):
        """物流轨迹中的单条记录"""
        time: str
        status: str
        context: str

    data: list[QueryTraceData]  # 物流轨迹详情列表

    def markdown(self):
        return (f"- 📦️**快递公司**： {self.kuaidiName}\n"
                f"- ℹ️**快递单号**： {self.kuaidiNum}\n"
                f"- 📧️**物流状态**： {self.state}\n"
                f"- 🚚**起点->目的地**： {self.fromTo}\n"
                "**物流轨迹**"
                f"{objects_to_markdown_table(self.data, ['时间', '状态', '详情'], attr_names=['time', 'status', 'context'])}")


class AutoNumberVO(BaseModel):
    """
    自动单号识别-响应数据类型
    """
    class AutoNumberDataVO(BaseModel):
        lengthPre: str  # 单号长度
        comCode: str  # 快递公司编码
        name: str  # 快递公司名称

    data: list[AutoNumberDataVO]

    def markdown(self):
        return ("**智能单号识别结果**"
                f"{objects_to_markdown_table(self.data, ['快递公司编码', '快递公司名称'], attr_names=['comCode', 'name'])}")


class EstimateTimeVO(BaseModel):
    """
    时效预估-响应数据类型
    """
    fromName: str = Field(..., description="出发地名称")
    toName: str = Field(..., description="目的地名称")
    orderTime: str = Field(..., description="下单时间")
    arrivalTime: str = Field(..., description="预计到达时间")
    remainTime: int = Field(..., description="剩余时间")
    deliveryExpendTime: str = Field(..., description="预计耗时")
    expType: Optional[str] = Field(None, description="业务或产品类型")

    def markdown(self):
        return (f"- 📦️️**出发地**： {self.fromName}\n"
                f"- 📍️**目的地**： {self.toName}\n"
                f"- 📱**下单时间**： {self.orderTime}\n"
                f"- 🚚**预计到达时间**： {self.arrivalTime}\n"
                f"- 📨**预计耗时**： {self.deliveryExpendTime}\n"
                f"- 🕐**剩余时间**： {self.remainTime}\n"
        )


class EstimatePriceVO(BaseModel):
    """
    预估价格工具-响应数据类型
    """
    kuaidicom: str = Field(..., description="快递公司编码")
    kuaidiName: str = Field(..., description="快递公司名称")
    from_: str = Field(..., alias="from", description="出发地名称")
    to: str = Field(..., description="目的地名称")
    weight: str = Field(..., description="重量")

    class Combos(BaseModel):
        """价格详情中的单条记录"""
        price: str = Field(..., description="预估运费价格，单位：元")
        expType: str = Field(..., description="业务或产品类型")
        productName: Optional[str] = Field(None, description="产品名称")

    combos: list[Combos] = Field(..., description="价格详情")

    def markdown(self):
        return (f"- 🚚**快递公司**： {self.kuaidiName}\n"
                f"- 📦️️**出发地**： {self.from_}\n"
                f"- 📍️**目的地**： {self.to}\n"
                f"- ⚖️️**重量**： {self.weight}kg\n"
                "**价格详情**"
                f"{objects_to_markdown_table(self.combos, ['业务/产品类型', '价格（元）'], attr_names=['expType', 'price'])}")


class ResultVO(BaseModel):
    """
    异常信息处理-响应数据类型
    """
    message: str = Field(..., description="异常信息")

    def markdown(self):
        return f"- ⚠️**异常信息**： {self.message}"