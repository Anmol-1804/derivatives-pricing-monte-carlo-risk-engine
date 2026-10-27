import numpy as np


def monte_carlo_option_price(
    S, K, T, r, sigma, option_type="call",
    simulations=100000, seed=42
):
    """Price a European option using risk-neutral Monte Carlo simulation."""
    if S <= 0 or K <= 0:
        raise ValueError("S and K must be positive.")
    if T < 0 or sigma < 0:
        raise ValueError("T and sigma cannot be negative.")
    if option_type not in ("call", "put"):
        raise ValueError("option_type must be call or put.")
    if simulations < 2:
        raise ValueError("At least two simulations are required.")

    if T == 0:
        payoff = max(S - K, 0.0) if option_type == "call" else max(K - S, 0.0)
        return {"price": payoff, "standard_error": 0.0}

    rng = np.random.default_rng(seed)
    z = rng.standard_normal(simulations)

    terminal_prices = S * np.exp(
        (r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * z
    )

    if option_type == "call":
        payoffs = np.maximum(terminal_prices - K, 0.0)
    else:
        payoffs = np.maximum(K - terminal_prices, 0.0)

    discounted_payoffs = np.exp(-r * T) * payoffs

    return {
        "price": float(discounted_payoffs.mean()),
        "standard_error": float(
            discounted_payoffs.std(ddof=1) / np.sqrt(simulations)
        ),
    }


if __name__ == "__main__":
    result_call = monte_carlo_option_price(500, 500, 0.5, 0.04, 0.25, "call")
    result_put = monte_carlo_option_price(500, 500, 0.5, 0.04, 0.25, "put")

    print("Monte Carlo European Option Pricing")
    print(f"Call price: ${result_call['price']:.4f}")
    print(f"Call standard error: ${result_call['standard_error']:.4f}")
    print(f"Put price: ${result_put['price']:.4f}")
    print(f"Put standard error: ${result_put['standard_error']:.4f}")
