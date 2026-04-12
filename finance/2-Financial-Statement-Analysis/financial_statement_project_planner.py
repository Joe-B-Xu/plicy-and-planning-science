from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


KNOWLEDGE_POINTS = [
    "资产负债表：理解资产、负债、所有者权益之间的关系。",
    "利润表：理解营业收入、成本、费用、利润的形成过程。",
    "现金流分析：判断利润和现金流是否一致。",
    "流动性分析：常见指标包括流动比率、速动比率。",
    "偿债能力分析：常见指标包括资产负债率、利息保障倍数。",
    "盈利能力分析：常见指标包括净利率、ROA、ROE。",
    "营运能力分析：常见指标包括总资产周转率、应收账款周转率。",
    "成长性分析：关注营业收入增长率、净利润增长率。",
    "杜邦分析：把 ROE 分解为利润率、周转率和权益乘数。",
    "趋势分析与横向比较：比较多个年份或多个企业的指标表现。",
]


@dataclass
class ProjectIdea:
    name: str
    goal: str
    inputs: List[str]
    outputs: List[str]
    steps: List[str]


PROJECTS = [
    ProjectIdea(
        name="财务比率自动计算器",
        goal="输入企业基础财务数据，自动生成常见财务比率。",
        inputs=["营业收入", "净利润", "总资产", "股东权益", "流动资产", "流动负债", "总负债"],
        outputs=["流动比率", "资产负债率", "净利率", "ROA", "ROE"],
        steps=[
            "建立基础输入模块，读取用户输入的财务数据。",
            "编写各项财务比率计算函数。",
            "将结果格式化输出，保留四位小数。",
            "后续可扩展为读取 Excel 或 CSV 文件。",
        ],
    ),
    ProjectIdea(
        name="企业趋势分析器",
        goal="根据多个年份的营业收入和净利润，分析企业成长趋势。",
        inputs=["多个年份的营业收入序列", "多个年份的净利润序列"],
        outputs=["各年份增长率", "增长趋势判断"],
        steps=[
            "输入连续年份的数据列表。",
            "逐年计算增长率。",
            "根据增长率是否持续为正、持续下降或波动，给出趋势判断。",
            "后续可扩展为折线图展示。",
        ],
    ),
    ProjectIdea(
        name="杜邦分析小工具",
        goal="拆解 ROE，帮助理解企业盈利能力的来源。",
        inputs=["净利润", "营业收入", "总资产", "股东权益"],
        outputs=["净利率", "总资产周转率", "权益乘数", "ROE"],
        steps=[
            "输入杜邦分析所需四个关键数字。",
            "计算净利率、总资产周转率、权益乘数。",
            "将三项指标相乘得到 ROE。",
            "解释哪一部分对 ROE 影响更大。",
        ],
    ),
    ProjectIdea(
        name="财务健康度评分器",
        goal="通过规则判断企业财务状况是否稳健。",
        inputs=["流动比率", "资产负债率", "净利率", "ROE"],
        outputs=["总评分", "风险等级", "简短建议"],
        steps=[
            "为每项指标设置简单阈值规则。",
            "根据指标区间累计分数。",
            "按总分给出稳健、一般、风险偏高等结论。",
            "后续可加入行业基准作更真实的比较。",
        ],
    ),
]


def safe_divide(numerator: float, denominator: float, name: str) -> float:
    if denominator == 0:
        raise ValueError(f"{name} 的分母不能为 0。")
    return numerator / denominator


def current_ratio(current_assets: float, current_liabilities: float) -> float:
    return safe_divide(current_assets, current_liabilities, "流动比率")


def debt_ratio(total_liabilities: float, total_assets: float) -> float:
    return safe_divide(total_liabilities, total_assets, "资产负债率")


def net_profit_margin(net_income: float, revenue: float) -> float:
    return safe_divide(net_income, revenue, "净利率")


def roa(net_income: float, total_assets: float) -> float:
    return safe_divide(net_income, total_assets, "ROA")


def roe(net_income: float, equity: float) -> float:
    return safe_divide(net_income, equity, "ROE")


def asset_turnover(revenue: float, total_assets: float) -> float:
    return safe_divide(revenue, total_assets, "总资产周转率")


def equity_multiplier(total_assets: float, equity: float) -> float:
    return safe_divide(total_assets, equity, "权益乘数")


def growth_rates(values: List[float]) -> List[float]:
    if len(values) < 2:
        raise ValueError("至少需要两个时期的数据。")
    rates = []
    for previous, current in zip(values, values[1:]):
        rates.append(safe_divide(current - previous, previous, "增长率"))
    return rates


def classify_trend(rates: List[float]) -> str:
    if all(rate > 0 for rate in rates):
        return "整体呈上升趋势"
    if all(rate < 0 for rate in rates):
        return "整体呈下降趋势"
    return "数据存在波动，需要进一步分析"


def dupont_analysis(net_income: float, revenue: float, total_assets: float, equity: float) -> Dict[str, float]:
    margin = net_profit_margin(net_income, revenue)
    turnover = asset_turnover(revenue, total_assets)
    multiplier = equity_multiplier(total_assets, equity)
    return {
        "净利率": margin,
        "总资产周转率": turnover,
        "权益乘数": multiplier,
        "ROE": margin * turnover * multiplier,
    }


def financial_health_score(current_ratio_value: float, debt_ratio_value: float, margin_value: float, roe_value: float) -> Dict[str, str]:
    score = 0
    notes = []

    if current_ratio_value >= 2:
        score += 25
        notes.append("流动性较强")
    elif current_ratio_value >= 1:
        score += 15
        notes.append("流动性基本正常")
    else:
        notes.append("流动性偏弱")

    if debt_ratio_value <= 0.5:
        score += 25
        notes.append("负债水平较稳健")
    elif debt_ratio_value <= 0.7:
        score += 15
        notes.append("负债水平可接受")
    else:
        notes.append("负债压力偏高")

    if margin_value >= 0.1:
        score += 25
        notes.append("盈利能力较好")
    elif margin_value >= 0.03:
        score += 15
        notes.append("盈利能力一般")
    else:
        notes.append("盈利能力偏弱")

    if roe_value >= 0.15:
        score += 25
        notes.append("股东回报较好")
    elif roe_value >= 0.08:
        score += 15
        notes.append("股东回报一般")
    else:
        notes.append("股东回报偏弱")

    if score >= 80:
        level = "稳健"
    elif score >= 50:
        level = "一般"
    else:
        level = "风险偏高"

    return {
        "score": str(score),
        "level": level,
        "advice": "；".join(notes),
    }


def print_knowledge_points() -> None:
    print("\n讲义知识点拆解")
    for index, point in enumerate(KNOWLEDGE_POINTS, start=1):
        print(f"{index}. {point}")


def print_projects() -> None:
    print("\n可做项目与实行方案")
    for index, project in enumerate(PROJECTS, start=1):
        print(f"\n{index}. {project.name}")
        print(f"目标: {project.goal}")
        print("输入: " + "、".join(project.inputs))
        print("输出: " + "、".join(project.outputs))
        print("实行方案:")
        for step_index, step in enumerate(project.steps, start=1):
            print(f"  {step_index}. {step}")


def read_float(prompt: str) -> float:
    return float(input(prompt).strip())


def read_series(prompt: str) -> List[float]:
    raw = input(prompt).strip()
    values = [item.strip() for item in raw.replace("，", ",").split(",") if item.strip()]
    if not values:
        raise ValueError("请输入至少一个数字。")
    return [float(item) for item in values]


def run_ratio_calculator() -> None:
    revenue = read_float("请输入营业收入: ")
    net_income = read_float("请输入净利润: ")
    total_assets = read_float("请输入总资产: ")
    equity = read_float("请输入股东权益: ")
    current_assets = read_float("请输入流动资产: ")
    current_liabilities = read_float("请输入流动负债: ")
    total_liabilities = read_float("请输入总负债: ")

    print("\n财务比率结果")
    print(f"流动比率: {current_ratio(current_assets, current_liabilities):.4f}")
    print(f"资产负债率: {debt_ratio(total_liabilities, total_assets):.4f}")
    print(f"净利率: {net_profit_margin(net_income, revenue):.4f}")
    print(f"ROA: {roa(net_income, total_assets):.4f}")
    print(f"ROE: {roe(net_income, equity):.4f}")


def run_trend_analyzer() -> None:
    revenue_series = read_series("请输入多个年份的营业收入，用逗号分隔: ")
    profit_series = read_series("请输入多个年份的净利润，用逗号分隔: ")

    revenue_rates = growth_rates(revenue_series)
    profit_rates = growth_rates(profit_series)

    print("\n趋势分析结果")
    print("营业收入增长率: " + ", ".join(f"{rate:.2%}" for rate in revenue_rates))
    print("净利润增长率: " + ", ".join(f"{rate:.2%}" for rate in profit_rates))
    print(f"营业收入趋势判断: {classify_trend(revenue_rates)}")
    print(f"净利润趋势判断: {classify_trend(profit_rates)}")


def run_dupont_tool() -> None:
    net_income = read_float("请输入净利润: ")
    revenue = read_float("请输入营业收入: ")
    total_assets = read_float("请输入总资产: ")
    equity = read_float("请输入股东权益: ")

    result = dupont_analysis(net_income, revenue, total_assets, equity)

    print("\n杜邦分析结果")
    for name, value in result.items():
        print(f"{name}: {value:.4f}")


def run_health_scorer() -> None:
    current_ratio_value = read_float("请输入流动比率: ")
    debt_ratio_value = read_float("请输入资产负债率: ")
    margin_value = read_float("请输入净利率: ")
    roe_value = read_float("请输入 ROE: ")

    result = financial_health_score(current_ratio_value, debt_ratio_value, margin_value, roe_value)
    print("\n财务健康度结果")
    print(f"总评分: {result['score']}")
    print(f"风险等级: {result['level']}")
    print(f"建议: {result['advice']}")


def main() -> None:
    while True:
        print("\n财务诸表分析项目规划器")
        print("1. 查看知识点拆解")
        print("2. 查看可做项目与实行方案")
        print("3. 财务比率自动计算")
        print("4. 企业趋势分析")
        print("5. 杜邦分析")
        print("6. 财务健康度评分")
        print("0. 退出")

        choice = input("请选择功能: ").strip()

        try:
            if choice == "1":
                print_knowledge_points()
            elif choice == "2":
                print_projects()
            elif choice == "3":
                run_ratio_calculator()
            elif choice == "4":
                run_trend_analyzer()
            elif choice == "5":
                run_dupont_tool()
            elif choice == "6":
                run_health_scorer()
            elif choice == "0":
                print("已退出。")
                break
            else:
                print("无效输入，请重新选择。")
        except ValueError as error:
            print(f"输入错误: {error}")


if __name__ == "__main__":
    main()
