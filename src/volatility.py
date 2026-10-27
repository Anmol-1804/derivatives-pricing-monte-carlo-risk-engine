from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"


def calculate_log_returns(prices):
    close = prices["Close"].dropna()
    if (close <= 0).any():
        raise ValueError("Prices must be positive.")
    return np.log(close / close.shift(1)).dropna()


def calculate_annualised_volatility(returns, trading_days=252):
    returns = returns.dropna()
    if len(returns) < 2:
        raise ValueError("At least two valid returns are required.")
    return float(returns.std() * np.sqrt(trading_days))


def calculate_rolling_volatility(returns, window=30, trading_days=252):
    return returns.rolling(window).std() * np.sqrt(trading_days)


def main():
    price_file = DATA_DIR / "spy_prices.csv"
    if not price_file.exists():
        raise FileNotFoundError(f"Price file not found: {price_file}")

    prices = pd.read_csv(price_file, index_col="Date", parse_dates=True)
    returns = calculate_log_returns(prices)
    annual_volatility = calculate_annualised_volatility(returns)
    rolling_volatility = calculate_rolling_volatility(returns)

    print(f"Daily returns: {len(returns)}")
    print(f"Annualised historical volatility: {annual_volatility:.2%}")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    results = pd.DataFrame({
        "Log_Return": returns,
        "Rolling_30D_Annualised_Volatility": rolling_volatility,
    })
    results.to_csv(DATA_DIR / "spy_returns_volatility.csv")

    plt.figure(figsize=(12, 6))
    plt.plot(rolling_volatility.index, rolling_volatility * 100)
    plt.title("SPY: 30-Day Rolling Annualised Volatility")
    plt.xlabel("Date")
    plt.ylabel("Volatility (%)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    chart_file = FIGURES_DIR / "spy_rolling_volatility.png"
    plt.savefig(chart_file, dpi=300)
    plt.close()

    print(f"CSV saved: {DATA_DIR / 'spy_returns_volatility.csv'}")
    print(f"Chart saved: {chart_file}")


if __name__ == "__main__":
    main()
