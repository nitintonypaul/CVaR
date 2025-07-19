# CVaR (Conditional Value at Risk)

This mini-project demonstrates the application of **Conditional Value at Risk (CVaR)** for portfolio optimization. CVaR, also known as Expected Shortfall, is a risk measure that quantifies the expected loss of a portfolio beyond a certain confidence level over a specific time horizon. It's particularly valuable because it considers the magnitude of losses in the tail end of the distribution, providing a more comprehensive view of downside risk compared to Value at Risk (VaR).

---

## How it Works

The project aims to determine an optimal asset allocation that minimizes the CVaR of a portfolio. This is achieved by:

* **Defining the Objective Function:** The core of the optimization is the CVaR function, which calculates the expected loss given that the loss exceeds a specified Value at Risk (VaR) threshold. Mathematically, for a portfolio loss $L(x, Y)$ where $x$ represents the portfolio weights and $Y$ is a random variable for market factors, the CVaR at a confidence level $\alpha$ is defined as:

$$
CVaR_\alpha(x) = \min_{x,v \in \mathbb{R}} { v + \frac{1}{1-\alpha} \mathbb{E} [\max(L(x, Y) - v, 0)]}
$$

Here, $v$ acts as an auxiliary variable representing the VaR. The optimization seeks to find the portfolio weights $x$ and the value $v$ that minimize this expression.

* **Historical Data Analysis:** The model uses historical stock data to understand asset price movements and calculate returns.
* **Optimization Algorithm:** An optimization algorithm is employed to find the portfolio weights that minimize the calculated CVaR, subject to constraints (e.g., portfolio weights summing to one, individual weights being non-negative).
* **Interpreting Results:** The output provides the optimized portfolio weights, indicating the proportion of investment that should be allocated to each asset to achieve the lowest CVaR at the given confidence level.

This project offers a practical example of how CVaR can be used to construct more robust portfolios, especially for risk-averse investors who want to manage potential extreme losses effectively.
