import numpy as np
from scipy.stats import norm


def calculate_greeks(S, K, T, r, sigma, option_type="call"):
    """Calculate Black-Scholes Greeks for a European option."""
    if S <= 0 or K <= 0:
        raise ValueError("S and K must be positive.")
    if T <= 0 or sigma <= 0:
        raise ValueError("T and sigma must be positive.")
    if option_type not in ("call", "put"):
        raise ValueError("option_type must be call or put.")

    sqrt_T = np.sqrt(T)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt_T)
    d2 = d1 - sigma * sqrt_T

    gamma = norm.pdf(d1) / (S * sigma * sqrt_T)
    vega = S * norm.pdf(d1) * sqrt_T / 100

    if option_type == "call":
        delta = norm.cdf(d1)
        theta = (
            -S * norm.pdf(d1) * sigma / (2 * sqrt_T)
            - r * K * np.exp(-r * T) * norm.cdf(d2)
        ) / 365
        rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
    else:
        delta = norm.cdf(d1) - 1
        theta = (
            -S * norm.pdf(d1) * sigma / (2 * sqrt_T)
            + r * K * np.exp(-r * T) * norm.cdf(-d2)
        ) / 365
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100

    return {
        "Delta": float(delta),
        "Gamma": float(gamma),
        "Theta_per_day": float(theta),
        "Vega_per_1pct": float(vega),
        "Rho_per_1pct": float(rho),
    }


if __name__ == "__main__":
    inputs = (500, 500, 0.5, 0.04, 0.25)

    for option_type in ("call", "put"):
        print(f"\n{option_type.upper()} OPTION GREEKS")
        for name, value in calculate_greeks(*inputs, option_type).items():
            print(f"{name}: {value:.6f}")
