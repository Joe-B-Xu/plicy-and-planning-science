from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


def future_value(present_value: float, rate: float, periods: int) -> float:
    return present_value * (1 + rate) ** periods


def present_value(future_value_amount: float, rate: float, periods: int) -> float:
    return future_value_amount / (1 + rate) ** periods


def npv(rate: float, cashflows: Iterable[float]) -> float:
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))


def irr(
    cashflows: Iterable[float],
    low: float = -0.9999,
    high: float = 10.0,
    tolerance: float = 1e-7,
    max_iterations: int = 10_000,
) -> float:
    cashflows = list(cashflows)
    low_value = npv(low, cashflows)
    high_value = npv(high, cashflows)
    if low_value == 0:
        return low
    if high_value == 0:
        return high
    while low_value * high_value > 0 and high < 1_000:
        high *= 2
        high_value = npv(high, cashflows)
    if low_value * high_value > 0:
        raise ValueError("IRR could not be bracketed. Check the cash flows.")
    for _ in range(max_iterations):
        mid = (low + high) / 2
        mid_value = npv(mid, cashflows)
        if abs(mid_value) < tolerance:
            return mid
        if low_value * mid_value < 0:
            high = mid
            high_value = mid_value
        else:
            low = mid
            low_value = mid_value
    raise ValueError("IRR did not converge.")


def perpetuity_present_value(cashflow_per_period: float, discount_rate: float) -> float:
    if discount_rate <= 0:
        raise ValueError("Discount rate must be positive.")
    return cashflow_per_period / discount_rate


def growing_perpetuity_present_value(
    next_period_cashflow: float, discount_rate: float, growth_rate: float
) -> float:
    if discount_rate <= growth_rate:
        raise ValueError("Discount rate must be greater than growth rate.")
    return next_period_cashflow / (discount_rate - growth_rate)


def annuity_present_value(payment: float, rate: float, periods: int) -> float:
    if periods <= 0:
        raise ValueError("Periods must be positive.")
    if rate == 0:
        return payment * periods
    return payment * (1 - (1 + rate) ** (-periods)) / rate


def annuity_future_value(payment: float, rate: float, periods: int) -> float:
    if periods <= 0:
        raise ValueError("Periods must be positive.")
    if rate == 0:
        return payment * periods
    return payment * ((1 + rate) ** periods - 1) / rate


def growing_annuity_present_value(
    first_payment: float, discount_rate: float, growth_rate: float, periods: int
) -> float:
    if periods <= 0:
        raise ValueError("Periods must be positive.")
    if discount_rate == growth_rate:
        return first_payment * periods / (1 + discount_rate)
    if discount_rate <= -1 or growth_rate <= -1:
        raise ValueError("Rates must be greater than -100%.")
    return (
        first_payment
        / (discount_rate - growth_rate)
        * (1 - ((1 + growth_rate) / (1 + discount_rate)) ** periods)
    )


def loan_payment(principal: float, rate: float, periods: int) -> float:
    if periods <= 0:
        raise ValueError("Periods must be positive.")
    if rate == 0:
        return principal / periods
    return principal * rate / (1 - (1 + rate) ** (-periods))


def remaining_loan_balance(
    principal: float, rate: float, total_periods: int, periods_paid: int
) -> float:
    if periods_paid < 0 or periods_paid > total_periods:
        raise ValueError("Periods paid must be between 0 and total periods.")
    payment = loan_payment(principal, rate, total_periods)
    if rate == 0:
        return principal - payment * periods_paid
    return payment * (1 - (1 + rate) ** (-(total_periods - periods_paid))) / rate


@dataclass
class TimelineEntry:
    period: int
    cashflow: float


def parse_cashflows(raw_text: str) -> List[float]:
    parts = [part.strip() for part in raw_text.replace(";", ",").split(",") if part.strip()]
    if not parts:
        raise ValueError("少なくとも 1 つのキャッシュフローを入力してください。")
    return [float(part) for part in parts]


def build_timeline(cashflows: Iterable[float]) -> List[TimelineEntry]:
    return [TimelineEntry(period=index, cashflow=value) for index, value in enumerate(cashflows)]


def timeline_as_table(cashflows: Iterable[float]) -> str:
    rows = ["Period | Cash Flow", "------ | ---------"]
    for entry in build_timeline(cashflows):
        rows.append(f"{entry.period:>6} | {entry.cashflow:>9.2f}")
    return "\n".join(rows)


def read_float(prompt: str) -> float:
    return float(input(prompt).strip())


def read_int(prompt: str) -> int:
    return int(input(prompt).strip())


def show_result(label: str, value: float, percentage: bool = False) -> None:
    if percentage:
        print(f"{label}: {value * 100:.4f}%")
    else:
        print(f"{label}: {value:.4f}")


def run_interactive_calculator() -> None:
    menu = {
        "1": "時間軸とキャッシュフロー",
        "2": "将来価値 (FV)",
        "3": "現在価値 (PV)",
        "4": "正味現在価値 (NPV)",
        "5": "永久債",
        "6": "成長型永久債",
        "7": "年金現価",
        "8": "年金終価",
        "9": "成長型年金現価",
        "10": "借入金の毎期返済額",
        "11": "借入残高",
        "12": "内部収益率 (IRR)",
        "0": "終了",
    }

    while True:
        print("\nお金の時間価値計算プログラム")
        for key, name in menu.items():
            print(f"{key}. {name}")
        choice = input("計算したい項目を選んでください: ").strip()
        try:
            if choice == "1":
                cashflows = parse_cashflows(
                    input("キャッシュフローをカンマ区切りで入力してください。例: -1000,300,400,500: ")
                )
                print(timeline_as_table(cashflows))
            elif choice == "2":
                pv = read_float("現在価値 (PV) を入力してください: ")
                rate = read_float("1 期間あたりの利率を入力してください。例: 0.05: ")
                periods = read_int("期間数を入力してください: ")
                show_result("将来価値", future_value(pv, rate, periods))
            elif choice == "3":
                fv = read_float("将来価値 (FV) を入力してください: ")
                rate = read_float("1 期間あたりの利率を入力してください。例: 0.05: ")
                periods = read_int("期間数を入力してください: ")
                show_result("現在価値", present_value(fv, rate, periods))
            elif choice == "4":
                rate = read_float("割引率を入力してください。例: 0.08: ")
                cashflows = parse_cashflows(input("t0 からのキャッシュフローをカンマ区切りで入力してください: "))
                show_result("正味現在価値", npv(rate, cashflows))
            elif choice == "5":
                cashflow = read_float("毎期の一定キャッシュフローを入力してください: ")
                rate = read_float("割引率を入力してください: ")
                show_result("永久債の現在価値", perpetuity_present_value(cashflow, rate))
            elif choice == "6":
                cashflow = read_float("次期のキャッシュフロー C1 を入力してください: ")
                rate = read_float("割引率 r を入力してください: ")
                growth = read_float("成長率 g を入力してください: ")
                show_result(
                    "成長型永久債の現在価値",
                    growing_perpetuity_present_value(cashflow, rate, growth),
                )
            elif choice == "7":
                payment = read_float("毎期の支払額を入力してください: ")
                rate = read_float("利率を入力してください: ")
                periods = read_int("期間数を入力してください: ")
                show_result("年金現価", annuity_present_value(payment, rate, periods))
            elif choice == "8":
                payment = read_float("毎期の支払額を入力してください: ")
                rate = read_float("利率を入力してください: ")
                periods = read_int("期間数を入力してください: ")
                show_result("年金終価", annuity_future_value(payment, rate, periods))
            elif choice == "9":
                payment = read_float("次期の支払額 C1 を入力してください: ")
                rate = read_float("割引率 r を入力してください: ")
                growth = read_float("成長率 g を入力してください: ")
                periods = read_int("期間数 n を入力してください: ")
                show_result(
                    "成長型年金現価",
                    growing_annuity_present_value(payment, rate, growth, periods),
                )
            elif choice == "10":
                principal = read_float("借入元本を入力してください: ")
                rate = read_float("1 期間あたりの利率を入力してください: ")
                periods = read_int("総返済回数を入力してください: ")
                show_result("毎期返済額", loan_payment(principal, rate, periods))
            elif choice == "11":
                principal = read_float("借入元本を入力してください: ")
                rate = read_float("1 期間あたりの利率を入力してください: ")
                periods = read_int("総返済回数を入力してください: ")
                paid = read_int("すでに返済した回数を入力してください: ")
                show_result("借入残高", remaining_loan_balance(principal, rate, periods, paid))
            elif choice == "12":
                cashflows = parse_cashflows(input("t0 からのキャッシュフローをカンマ区切りで入力してください: "))
                show_result("内部収益率", irr(cashflows), percentage=True)
            elif choice == "0":
                print("終了しました。")
                break
            else:
                print("無効な選択です。もう一度入力してください。")
        except ValueError as error:
            print(f"入力または計算エラー: {error}")


def demo() -> None:
    sample_cashflows = [-1000, 300, 420, 680]
    print("サンプルのキャッシュフロー時間軸")
    print(timeline_as_table(sample_cashflows))
    print()
    show_result("FV of 1000 at 5% for 3 periods", future_value(1000, 0.05, 3))
    show_result("PV of 1157.625 at 5% for 3 periods", present_value(1157.625, 0.05, 3))
    show_result("NPV at 10%", npv(0.10, sample_cashflows))
    show_result("IRR", irr(sample_cashflows), percentage=True)
    show_result("Perpetuity PV", perpetuity_present_value(80, 0.08))
    show_result("Growing perpetuity PV", growing_perpetuity_present_value(80, 0.08, 0.03))
    show_result("Annuity PV", annuity_present_value(200, 0.06, 5))
    show_result("Growing annuity PV", growing_annuity_present_value(200, 0.08, 0.03, 5))
    show_result("Loan payment", loan_payment(10000, 0.01, 12))


if __name__ == "__main__":
    print("1. 対話モードを実行")
    print("2. デモを実行")
    mode = input("モードを選んでください（デフォルトは 1）: ").strip() or "1"
    if mode == "2":
        demo()
    else:
        run_interactive_calculator()
