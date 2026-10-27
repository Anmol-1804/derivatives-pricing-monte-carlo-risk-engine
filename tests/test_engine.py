import numpy as np
from src.black_scholes import black_scholes_price
from src.monte_carlo import monte_carlo_option_price
from src.risk_metrics import calculate_var, calculate_expected_shortfall

def test_black_scholes():
    call = black_scholes_price(100, 100, 1, 0.05, 0.2, "call")
    put = black_scholes_price(100, 100, 1, 0.05, 0.2, "put")
    assert abs(call - 10.4506) < 0.01
    assert abs(put - 5.5735) < 0.01
    print("PASS: Black-Scholes call and put pricing")

def test_monte_carlo():
    analytical = black_scholes_price(100, 100, 1, 0.05, 0.2, "call")
    result = monte_carlo_option_price(
        100, 100, 1, 0.05, 0.2, "call",
        simulations=200000, seed=42
    )
    assert abs(result["price"] - analytical) < 4 * result["standard_error"]
    print("PASS: Monte Carlo pricing agrees with Black-Scholes within four standard errors")

def test_risk_metrics():
    returns = np.array([-0.10, -0.05, -0.02, -0.01, 0.01, 0.02, 0.03, 0.04])
    var = calculate_var(returns, 0.95, 100000)
    es = calculate_expected_shortfall(returns, 0.95, 100000)
    assert var >= 0
    assert es >= var
    print("PASS: VaR and Expected Shortfall calculations")

if __name__ == "__main__":
    test_black_scholes()
    test_monte_carlo()
    test_risk_metrics()
    print("\nAll tests passed.")
