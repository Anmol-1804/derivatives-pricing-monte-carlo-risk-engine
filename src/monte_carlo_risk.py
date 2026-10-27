import numpy as np


def monte_carlo_var_es(
    portfolio_value,
    daily_returns,
    confidence_levels=(0.95, 0.99),
    simulations=100_000,
    seed=42,
):
    """Estimate one-day portfolio VaR and ES using Monte Carlo simulation.

    Uses normally distributed daily returns calibrated to historical
    sample mean and standard deviation.
    """
    returns = np.asarray(daily_returns, dtype=float)
    returns = returns[np.isfinite(returns)]

    if portfolio_value <= 0:
        raise ValueError("portfolio_value must be positive.")
    if len(returns) < 2:
        raise ValueError("At least two valid daily returns are required.")
    if simulations < 1:
        raise ValueError("simulations must be positive.")

    for confidence in confidence_levels:
        if not 0 < confidence < 1:
            raise ValueError("Confidence levels must be between 0 and 1.")

    mean_return = np.mean(returns)
    daily_volatility = np.std(returns, ddof=1)

    rng = np.random.default_rng(seed)
    simulated_returns = rng.normal(
        loc=mean_return,
        scale=daily_volatility,
        size=simulations,
    )

    simulated_pnl = portfolio_value * simulated_returns
    simulated_losses = -simulated_pnl

    results = {}

    for confidence in confidence_levels:
        var = np.quantile(simulated_losses, confidence)
        tail_losses = simulated_losses[simulated_losses >= var]
        expected_shortfall = (
            float(np.mean(tail_losses)) if len(tail_losses) else float(var)
        )

        results[confidence] = {
            "VaR": float(var),
            "ES": expected_shortfall,
        }

    return results


if __name__ == "__main__":
    from pathlib import Path
    import pandas as pd

    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "spy_prices.csv"

    if not data_path.exists():
        raise FileNotFoundError(
            f"Could not find {data_path}. Run the data loader first."
        )

    prices = pd.read_csv(data_path, parse_dates=["Date"])
    prices = prices.sort_values("Date")

    if "Close" not in prices.columns:
        raise ValueError("The SPY price file must contain a Close column.")

    returns = prices["Close"].pct_change().dropna().to_numpy()

    results = monte_carlo_var_es(
        portfolio_value=100_000,
        daily_returns=returns,
    )

    print("MONTE CARLO PORTFOLIO RISK")
    print("Portfolio value: $100,000.00")
    print("Return model: Normal distribution calibrated to SPY daily returns")

    for confidence, metrics in results.items():
        print(f"\nConfidence level: {confidence:.0%}")
        print(f"Daily VaR: ${metrics['VaR']:,.2f}")
        print(f"Daily Expected Shortfall: ${metrics['ES']:,.2f}")
