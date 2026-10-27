from pathlib import Path
import yfinance as yf
from pandas_datareader import data as pdr
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def download_spy_prices(start_date="2021-01-01", end_date="2026-01-01"):
    """Download daily SPY prices and save them locally."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    prices = yf.Ticker("SPY").history(
        start=start_date,
        end=end_date,
        auto_adjust=True,
    )

    if prices.empty:
        raise ValueError("No SPY data returned. Check your internet connection.")

    prices.index = prices.index.tz_localize(None)
    prices.index.name = "Date"

    output_path = DATA_DIR / "spy_prices.csv"
    prices.to_csv(output_path)

    print(f"Saved {len(prices)} SPY observations to {output_path}")
    print(prices.head())
    return prices


def download_treasury_rates(
    start_date="2021-01-01",
    end_date="2026-01-01",
):
    """Download monthly US 3-month Treasury bill rates from FRED."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    rates = pdr.DataReader(
        "TB3MS",
        "fred",
        start=start_date,
        end=end_date,
    )

    if rates.empty:
        raise ValueError("No Treasury rate data returned.")

    rates.index.name = "Date"
    rates = rates.rename(
        columns={"TB3MS": "Treasury_3M_Rate_Percent"}
    )

    output_path = DATA_DIR / "treasury_rates.csv"
    rates.to_csv(output_path)

    print(f"Saved {len(rates)} Treasury rate observations to {output_path}")
    print(rates.head())

    return rates


if __name__ == "__main__":
    print("Downloading SPY prices...")
    download_spy_prices()

    print("\nDownloading US Treasury rates...")
    download_treasury_rates()
    print("Downloading SPY prices...")
    download_spy_prices()
