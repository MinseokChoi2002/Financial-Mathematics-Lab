# Financial Mathematics Lab
> **Python-based Quantitative Finance & Numerical Methods Engine**

An object-oriented Python engine for pricing European options, calculating sensitivities (Greeks), solving implied volatility, and simulating Monte Carlo barrier options grounded in financial mathematics and numerical analysis.

---

## 1. Key Features

| File | Module / Algorithm | Description |
| :--- | :--- | :--- |
| `black_scholes.py` | European Option Pricing & 5 Greeks Engine | Prices European Call/Put options and calculates 5 key Greeks ($\Delta, \Gamma, \nu, \Theta, \rho$) via the Black-Scholes formula. |
| `implied_volatility.py` | Newton-Raphson Implied Volatility Solver | Back-calculates implied volatility ($\sigma$) from market prices ($C_{\text{market}}$) using the Newton-Raphson method. |
| `monte_carlo.py` | Monte Carlo Barrier Option & Convergence Engine | Generates Geometric Brownian Motion (GBM) price paths, prices Up-and-In Call options, and benchmarks convergence. |
| `visualization.py` | Trajectory Plotting & Visualizer | Visualizes knock-in vs. non-knock-in trajectories and exports high-resolution plots. |

---

## 2. Mathematical Background

### 1) Black-Scholes Model & Greeks (`black_scholes.py`)
Analytical closed-form solutions for European Call ($C$) and Put ($P$) options:

$$d_1 = \frac{\ln(S_0 / K) + \left(r + \frac{\sigma^2}{2}\right)T}{\sigma \sqrt{T}}, \quad d_2 = d_1 - \sigma \sqrt{T}$$

$$C = S_0 N(d_1) - K e^{-rT} N(d_2)$$

$$P = K e^{-rT} N(-d_2) - S_0 N(-d_1)$$

### 2) Monte Carlo Engine & GBM (`monte_carlo.py`)
Underlying asset dynamics follow Geometric Brownian Motion (GBM):

$$dS_t = r S_t dt + \sigma S_t dW_t \implies S_{t+\Delta t} = S_t \exp\left( \left(r - \frac{\sigma^2}{2}\right)\Delta t + \sigma \sqrt{\Delta t} Z \right)$$

*(where $Z \sim N(0,1)$ is a standard normal random variable)*

**Up-and-In Barrier Call Option Payoff:** Payoff triggers only if the underlying price reaches or exceeds barrier $H$ before maturity $T$:

$$\text{Payoff} = \max(S_T - K, 0) \times \mathbb{I}\left(\max_{0 \le t \le T} S_t \ge H\right)$$

---

## 3. Simulation & Visualization Results

### 1) Path Trajectory Visualization (`visualization.py`)
- **Simulation Parameters:** $S_0 = 15,500$ KRW, $K = 15,000$ KRW, $H = 16,000$ KRW, $T = 90$ days, $r = 2.5\%$, $\sigma = 30\%$
- **Knock-In (Red Lines):** Paths where the asset reaches barrier $H=16,000$ KRW, activating the option.
- **Non-Knock-In (Grey Lines):** Paths that fail to reach the barrier and expire worthless.

### 2) Convergence Benchmark Results (`monte_carlo.py`)
Convergence toward the Black-Scholes theoretical price (1,229.45 KRW) and execution time as simulation count ($N$) increases:

| Simulations ($N$) | Monte Carlo Price (MC) | Error Rate | Up-and-In Call Price | Elapsed Time |
| :--- | :--- | :--- | :--- | :--- |
| 1,000 | 1,257.38 KRW | 2.271% | 1,247.04 KRW | 0.0113s |
| 5,000 | 1,232.21 KRW | 0.224% | 1,224.46 KRW | 0.0421s |
| 10,000 | 1,224.83 KRW | 0.376% | 1,217.23 KRW | 0.1008s |
| 50,000 | 1,223.37 KRW | 0.495% | 1,214.60 KRW | 0.5952s |
| 100,000 | 1,222.55 KRW | 0.562% | 1,213.94 KRW | 1.0282s |

---

## 4. Getting Started

### Prerequisites
```bash
pip install numpy scipy matplotlib
