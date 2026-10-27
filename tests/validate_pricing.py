from src.black_scholes import black_scholes_price
from src.monte_carlo import monte_carlo_option_price

S = 500
K = 500
T = 0.5
r = 0.04
sigma = 0.25

print("=" * 55)
print("BLACK-SCHOLES VS MONTE CARLO VALIDATION")
print("=" * 55)

for option_type in ("call", "put"):
    analytical_price = black_scholes_price(
        S, K, T, r, sigma, option_type
    )

    mc_result = monte_carlo_option_price(
        S, K, T, r, sigma, option_type,
        simulations=200000,
        seed=42,
    )

    difference = mc_result["price"] - analytical_price
    standard_error = mc_result["standard_error"]

    print(f"\nOption: {option_type.upper()}")
    print(f"Black-Scholes price: ${analytical_price:.4f}")
    print(f"Monte Carlo price:   ${mc_result['price']:.4f}")
    print(f"Monte Carlo standard error: ${standard_error:.4f}")
    print(f"Price difference: ${difference:.4f}")

    if abs(difference) <= 3 * standard_error:
        print("Validation: PASS (within 3 Monte Carlo standard errors)")
    else:
        print("Validation: CHECK (outside 3 Monte Carlo standard errors)")
