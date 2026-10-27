import numpy as np
from scipy.stats import norm


def black_scholes_price(S, K, T, r, sigma, option_type="call"):
    """Calculate the Black-Scholes price of a European option."""
    if S <= 0 or K <= 0:
        raise ValueError("S and K must be positive.")
    if T < 0 or sigma < 0:
        raise ValueError("T and sigma cannot be negative.")
    if option_type not in ("call", "put"):
        raise ValueError("option_type must be call or put.")

    if T == 0:
        return max(S - K, 0.0) if option_type == "call" else max(K - S, 0.0)

    if sigma == 0:
        discounted_strike = K * np.exp(-r * T)
        if option_type == "call":
            return float(max(S - discounted_strike, 0.0))
        return float(max(discounted_strike - S, 0.0))

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return float(price)


if __name__ == "__main__":
    S, K, T, r, sigma = 500.0, 500.0, 0.5, 0.04, 0.25

    call = black_scholes_price(S, K, T, r, sigma, "call")
    put = black_scholes_price(S, K, T, r, sigma, "put")

    print(f"Underlying price: ${S:.2f}")
    print(f"Strike price: ${K:.2f}")
    print(f"Time to maturity: {T:.2f} years")
    print(f"Risk-free rate: {r:.2%}")
    print(f"Volatility: {sigma:.2%}")
    print(f"European call price: ${call:.4f}")
    print(f"European put price: ${put:.4f}")
