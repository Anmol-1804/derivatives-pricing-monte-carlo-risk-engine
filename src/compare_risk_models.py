from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.risk_metrics import calculate_var, calculate_expected_shortfall
from src.monte_carlo_risk import monte_carlo_var_es

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "spy_returns_volatility.csv"
OUTPUT_PATH = PROJECT_ROOT / "reports" / "figures" / "risk_model_comparison.png"

PORTFOLIO_VALUE = 100_000

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Missing data file: {DATA_PATH}")

data = pd.read_csv(DATA_PATH)

if "Log_Return" not in data.columns:
    raise ValueError("Expected a Log_Return column in the data.")

returns = data["Log_Return"].dropna()

historical = {}
for confidence in (0.95, 0.99):
    historical[confidence] = {
        "VaR": calculate_var(returns, confidence, PORTFOLIO_VALUE),
        "ES": calculate_expected_shortfall(
            returns, confidence, PORTFOLIO_VALUE
        ),
    }

monte_carlo = monte_carlo_var_es(
    portfolio_value=PORTFOLIO_VALUE,
    daily_returns=returns,
    confidence_levels=(0.95, 0.99),
    simulations=100_000,
    seed=42,
)

print("HISTORICAL VS MONTE CARLO RISK")
print(f"Portfolio value: ${PORTFOLIO_VALUE:,.2f}")

for confidence in (0.95, 0.99):
    print(f"\nConfidence level: {confidence:.0%}")
    for metric in ("VaR", "ES"):
        print(
            f"{metric}: Historical ${historical[confidence][metric]:,.2f}"
            f" | Monte Carlo ${monte_carlo[confidence][metric]:,.2f}"
        )

labels = ["95% VaR", "99% VaR", "95% ES", "99% ES"]
historical_values = [
    historical[0.95]["VaR"],
    historical[0.99]["VaR"],
    historical[0.95]["ES"],
    historical[0.99]["ES"],
]
monte_carlo_values = [
    monte_carlo[0.95]["VaR"],
    monte_carlo[0.99]["VaR"],
    monte_carlo[0.95]["ES"],
    monte_carlo[0.99]["ES"],
]

positions = range(len(labels))
width = 0.36

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(
    [p - width / 2 for p in positions],
    historical_values,
    width,
    label="Historical",
)
ax.bar(
    [p + width / 2 for p in positions],
    monte_carlo_values,
    width,
    label="Monte Carlo",
)

ax.set_title("Historical vs Monte Carlo Portfolio Risk")
ax.set_ylabel("Estimated one-day loss ($)")
ax.set_xticks(list(positions))
ax.set_xticklabels(labels)
ax.legend()
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
plt.close(fig)

print(f"\nChart saved to: {OUTPUT_PATH}")
