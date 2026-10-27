# Derivatives Pricing & Monte Carlo Risk Engine

A Python-based quantitative finance project for European option pricing, Monte Carlo simulation, option Greeks, volatility analysis, and portfolio risk measurement.

## Key Features

- Black-Scholes pricing for European call and put options.
- Monte Carlo simulation for option pricing with standard error estimation.
- Option Greeks: Delta, Gamma, Theta, Vega, and Rho.
- Historical and rolling volatility analysis using SPY market data.
- Historical Value at Risk (VaR) and Expected Shortfall (ES).
- Automated tests for pricing and risk calculations.

## Technology Stack

- Python, NumPy, pandas, SciPy
- Matplotlib
- yfinance and pandas-datareader
- pytest

## Risk Analytics Results

Portfolio value: **,000**

| Confidence Level | Daily VaR | Daily Expected Shortfall |
|---|---:|---:|
| 95% | ,676.18 | ,515.95 |
| 99% | ,972.83 | ,958.76 |

VaR estimates a loss threshold at a specified confidence level. Expected Shortfall estimates the average loss in the tail beyond that threshold. These results are historical estimates and are not forecasts or investment advice.

