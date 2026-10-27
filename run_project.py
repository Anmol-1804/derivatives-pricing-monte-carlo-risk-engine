import subprocess
import sys

SCRIPTS = [
    ("Volatility Analysis", "src.volatility"),
    ("Option Greeks", "src.greeks"),
    ("Monte Carlo Risk", "src.monte_carlo_risk"),
    ("Risk Model Comparison", "src.compare_risk_models"),
    ("Greeks Visualisations", "src.greeks_visualization"),
]

def main():
    print("=" * 60)
    print("DERIVATIVES PRICING & MONTE CARLO RISK ENGINE")
    print("=" * 60)

    failed = []

    for title, module in SCRIPTS:
        print(f"\n{'-' * 60}")
        print(f"Running: {title}")
        print("-" * 60)

        result = subprocess.run(
            [sys.executable, "-m", module],
            check=False,
        )

        if result.returncode != 0:
            failed.append((title, result.returncode))
            print(f"FAILED: {title}")
        else:
            print(f"COMPLETED: {title}")

    print("\n" + "=" * 60)
    print("PROJECT RUN SUMMARY")
    print("=" * 60)

    if failed:
        for title, code in failed:
            print(f"FAILED: {title} (exit code {code})")
        sys.exit(1)

    print("All analyses completed successfully.")

if __name__ == "__main__":
    main()
