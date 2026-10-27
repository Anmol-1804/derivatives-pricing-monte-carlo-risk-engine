import numpy as np
import pandas as pd


def calculate_var(returns, confidence_level=0.95, portfolio_value=100000):
    """Calculate historical Value at Risk as a positive loss amount."""
    returns = pd.Series(returns).dropna()

    if returns.empty:
        raise ValueError("Returns cannot be empty.")
    if not 0 < confidence_level < 1:
        raise ValueError("Confidence level must be between 0 and 1.")
    if portfolio_value <= 0:
        raise ValueError("Portfolio value must be positive.")

    return float(
        max(0.0, -returns.quantile(1 - confidence_level) * portfolio_value)
    )


def calculate_expected_shortfall(
    returns, confidence_level=0.95, portfolio_value=100000
):
    """Calculate historical Expected Shortfall as a positive loss amount."""
    returns = pd.Series(returns).dropna()

    if returns.empty:
        raise ValueError("Returns cannot be empty.")
    if not 0 < confidence_level < 1:
        raise ValueError("Confidence level must be between 0 and 1.")
    if portfolio_value <= 0:
        raise ValueError("Portfolio value must be positive.")

    var_threshold = returns.quantile(1 - confidence_level)
    tail_returns = returns[returns <= var_threshold]

    if tail_returns.empty:
        raise ValueError("No observations in the loss tail.")

    return float(max(0.0, -tail_returns.mean() * portfolio_value))


if __name__ == "__main__":
    data_path = "data/spy_returns_volatility.csv"
    data = pd.read_csv(data_path)

    returns = data["Log_Return"].dropna()
    portfolio_value = 100000

    print("HISTORICAL PORTFOLIO RISK")
    print(f"Portfolio value: ${portfolio_value:,.2f}")

    for confidence in (0.95, 0.99):
        var = calculate_var(returns, confidence, portfolio_value)
        es = calculate_expected_shortfall(returns, confidence, portfolio_value)

        print(f"\nConfidence level: {confidence:.0%}")
        print(f"Daily VaR: ${var:,.2f}")
        print(f"Daily Expected Shortfall: ${es:,.2f}")
