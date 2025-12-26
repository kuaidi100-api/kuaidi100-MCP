def objects_to_markdown_table(
        obj_list,
        headers,
        attr_names=None,
        empty_message="> 无数据\n"
):
    """
    将任意对象列表转换为 Markdown 表格。

    参数:
        obj_list (list): 对象列表，如 [obj1, obj2, ...]
        headers (list[str]): 表头文字，如 ["时间", "状态", "详情"]
        attr_names (list[str], optional): 对应每个表头的对象属性名。
                                         如果未提供，则默认与 headers 相同。
        empty_message (str): 当列表为空时返回的提示信息。

    返回:
        str: Markdown 表格字符串
    """
    if not obj_list:
        return empty_message

    if attr_names is None:
        attr_names = headers  # 假设属性名和表头一致（需是合法标识符）

    col_widths = []
    for i in headers:
        col_widths.append(1)

    # 提取每行数据
    rows = []
    for obj in obj_list:
        row = []
        for attr in attr_names:
            value = getattr(obj, attr, "")
            # 转为字符串，并处理 None 或特殊值
            cell = str(value) if value is not None else ""
            row.append(cell)
        rows.append(row)

    # 辅助函数：格式化一行
    def format_row(r):
        return "|" + "|".join(cell.ljust(col_widths[i]) for i, cell in enumerate(r)) + "|"

    # 构建表格
    lines = [format_row(headers)]
    separator = "|-" + "-|-".join("-" * w for w in col_widths) + "-|"
    lines.append(separator)
    lines.extend(format_row(row) for row in rows)

    return "\n".join(lines)