# 1-Time Value

This project is a small Python calculator for the lecture topics around the time value of money.

Included modules:

- Timeline and cash flow table
- Future value (`FV`)
- Present value (`PV`)
- Net present value (`NPV`)
- Perpetuity
- Growing perpetuity
- Annuity present value
- Annuity future value
- Growing annuity present value
- Loan payment per period
- Remaining loan balance
- Internal rate of return (`IRR`)

## Run

```bash
python time_value_calculator.py
```

You can choose:

- Interactive mode: enter your own variables from the terminal
- Demo mode: see built-in sample calculations

## Notes

- Rates should be entered in decimal form. For example, `5%` should be entered as `0.05`.
- Cash flows should be entered from `t0`, separated by commas. Example: `-1000,300,400,500`
