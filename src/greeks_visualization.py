import numpy as np
import matplotlib.pyplot as plt
from src.greeks import calculate_greeks
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

K = 500
T = 0.5
r = 0.04
sigma = 0.25

spot_prices = np.linspace(350, 650, 200)

for option_type in ("call", "put"):
    results = [
        calculate_greeks(S, K, T, r, sigma, option_type)
        for S in spot_prices
    ]

    deltas = [item["Delta"] for item in results]
    gammas = [item["Gamma"] for item in results]

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    axes[0].plot(spot_prices, deltas, label="Delta")
    axes[0].axvline(K, linestyle="--", label="Strike Price")
    axes[0].set_title(f"{option_type.title()} Option - Delta")
    axes[0].set_ylabel("Delta")
    axes[0].grid(True)
    axes[0].legend()

    axes[1].plot(spot_prices, gammas, label="Gamma")
    axes[1].axvline(K, linestyle="--", label="Strike Price")
    axes[1].set_title(f"{option_type.title()} Option - Gamma")
    axes[1].set_xlabel("Underlying Spot Price ($)")
    axes[1].set_ylabel("Gamma")
    axes[1].grid(True)
    axes[1].legend()

    fig.suptitle("Black-Scholes Option Greeks")
    fig.tight_layout()

    output_path = FIGURES_DIR / f"{option_type}_delta_gamma.png"
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved: {output_path}")

print("\nGreek visualisations generated successfully.")
