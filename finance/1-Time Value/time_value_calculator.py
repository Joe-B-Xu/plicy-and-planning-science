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
        raise ValueError("Please enter at least one cash flow.")
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
        "1": "Timeline and cash flow",
        "2": "Future value (FV)",
        "3": "Present value (PV)",
        "4": "Net present value (NPV)",
        "5": "Perpetuity",
        "6": "Growing perpetuity",
        "7": "Annuity present value",
        "8": "Annuity future value",
        "9": "Growing annuity present value",
        "10": "Loan payment per period",
        "11": "Remaining loan balance",
        "12": "Internal rate of return (IRR)",
        "0": "Exit",
    }

    while True:
        print("\nTime Value of Money Calculator")
        for key, name in menu.items():
            print(f"{key}. {name}")
        choice = input("Choose a module: ").strip()
        try:
            if choice == "1":
                cashflows = parse_cashflows(
                    input("Enter cash flows separated by commas, for example -1000,300,400,500: ")
                )
                print(timeline_as_table(cashflows))
            elif choice == "2":
                pv = read_float("Enter present value (PV): ")
                rate = read_float("Enter rate per period, for example 0.05: ")
                periods = read_int("Enter number of periods: ")
                show_result("Future value", future_value(pv, rate, periods))
            elif choice == "3":
                fv = read_float("Enter future value (FV): ")
                rate = read_float("Enter rate per period, for example 0.05: ")
                periods = read_int("Enter number of periods: ")
                show_result("Present value", present_value(fv, rate, periods))
            elif choice == "4":
                rate = read_float("Enter discount rate, for example 0.08: ")
                cashflows = parse_cashflows(input("Enter cash flows from t0, separated by commas: "))
                show_result("Net present value", npv(rate, cashflows))
            elif choice == "5":
                cashflow = read_float("Enter fixed cash flow per period: ")
                rate = read_float("Enter discount rate: ")
                show_result("Perpetuity present value", perpetuity_present_value(cashflow, rate))
            elif choice == "6":
                cashflow = read_float("Enter next period cash flow C1: ")
                rate = read_float("Enter discount rate r: ")
                growth = read_float("Enter growth rate g: ")
                show_result(
                    "Growing perpetuity present value",
                    growing_perpetuity_present_value(cashflow, rate, growth),
                )
            elif choice == "7":
                payment = read_float("Enter payment each period: ")
                rate = read_float("Enter rate: ")
                periods = read_int("Enter number of periods: ")
                show_result("Annuity present value", annuity_present_value(payment, rate, periods))
            elif choice == "8":
                payment = read_float("Enter payment each period: ")
                rate = read_float("Enter rate: ")
                periods = read_int("Enter number of periods: ")
                show_result("Annuity future value", annuity_future_value(payment, rate, periods))
            elif choice == "9":
                payment = read_float("Enter next period payment C1: ")
                rate = read_float("Enter discount rate r: ")
                growth = read_float("Enter growth rate g: ")
                periods = read_int("Enter number of periods n: ")
                show_result(
                    "Growing annuity present value",
                    growing_annuity_present_value(payment, rate, growth, periods),
                )
            elif choice == "10":
                principal = read_float("Enter loan principal: ")
                rate = read_float("Enter rate per period: ")
                periods = read_int("Enter total number of repayment periods: ")
                show_result("Payment per period", loan_payment(principal, rate, periods))
            elif choice == "11":
                principal = read_float("Enter loan principal: ")
                rate = read_float("Enter rate per period: ")
                periods = read_int("Enter total number of repayment periods: ")
                paid = read_int("Enter number of periods already paid: ")
                show_result("Remaining loan balance", remaining_loan_balance(principal, rate, periods, paid))
            elif choice == "12":
                cashflows = parse_cashflows(input("Enter cash flows from t0, separated by commas: "))
                show_result("Internal rate of return", irr(cashflows), percentage=True)
            elif choice == "0":
                print("Exited.")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError as error:
            print(f"Input or calculation error: {error}")


def demo() -> None:
    sample_cashflows = [-1000, 300, 420, 680]
    print("Sample cash flow timeline")
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
    print("1. Run interactive calculator")
    print("2. Run demo")
    mode = input("Choose mode (default 1): ").strip() or "1"
    if mode == "2":
        demo()
    else:
        run_interactive_calculator()
