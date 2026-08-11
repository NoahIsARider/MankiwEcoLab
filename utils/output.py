"""
控制台输出工具
Console Output Utilities

提供对齐的表格与分隔线打印, 使 CLI 输出更易读。
"""


def print_table(columns: list, rows: list, title: str = None,
                float_precision: int = 2) -> None:
    """
    打印对齐的 ASCII 表格

    Args:
        columns: 列标题列表
        rows: 行数据列表 (每行为与列等长的列表)
        title: 可选表格标题
        float_precision: 浮点数保留位数
    """
    if not columns:
        return

    def fmt(value):
        if isinstance(value, float):
            return f"{value:.{float_precision}f}"
        return str(value)

    formatted_rows = [[fmt(cell) for cell in row] for row in rows]

    widths = [len(str(col)) for col in columns]
    for row in formatted_rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(cell))

    header = " | ".join(str(col).ljust(widths[i])
                        for i, col in enumerate(columns))
    border = "-+-".join("-" * w for w in widths)
    top = "+" + "-".join("-" * w for w in widths) + "+"
    bottom = "+" + "-".join("-" * w for w in widths) + "+"

    if title:
        print(title)
    print(top)
    print("| " + header + " |")
    print("|" + border + "|")
    for row in formatted_rows:
        line = " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(row))
        print("| " + line + " |")
    print(bottom)


def print_section(title: str, width: int = 70, char: str = "=") -> None:
    """打印分隔标题"""
    print("\n" + char * width)
    print(title)
    print(char * width)


def format_pct(value: float, precision: int = 2) -> str:
    """格式化百分比"""
    return f"{value:.{precision}f}%"
