# Financial Mathematics Lab

Quantitative modeling engine for exotic option pricing, numerical Greeks calculation, multi-path dynamic delta hedging, and interest rate derivatives pricing using the **Black-Scholes Model**, **Monte Carlo Simulation**, **Finite Difference Method (FDM)**, and the **Black-Scholes / Black-76 Model**.

---

## Project Overview

This repository implements dynamic derivative pricing and hedging across two main modules:

### Module 01: Equity Option Pricing & Dynamic Delta Hedging
1. **Analytical Benchmarking:** Closed-form European option pricing via Black-Scholes formulas.
2. **Monte Carlo Pricing Engine:** Path generation for European and path-dependent exotic options (**Up-and-In Barrier Call Option**).
3. **Convergence Analysis:** Accuracy, error rate, and runtime benchmarking across simulation paths ($N = 1,000$ to $200,000$).
4. **Numerical Greeks (FDM):** Path-dependent Delta estimation via Central Finite Difference Method using time-dependent seed offsets ($\text{seed} + t$) to suppress variance.
5. **Dynamic Delta Hedging Simulator:** Daily rebalancing engine tracking continuous compounding cash balances ($e^{r \Delta t}$) across single and multi-path simulations.
6. **Risk & Error Analysis:** Empirical PnL error distribution, mean bias, and standard deviation analysis across simulated trajectories.

### Module 02: Interest Rate Derivatives & Yield Curve Engine
1. **Yield Curve Engine:** Zero yield curve construction, continuous discount factor derivation, and linear rate interpolation.
2. **Forward Rate & Swap Annuity:** Analytical forward rate calculation $F(0; T_1, T_2)$ and forward swap annuity $A(0)$ engine.
3. **Black-76 Pricing Engine:** Standardized option pricing for European **Caplets** and **Swaptions** (Payer / Receiver).

---

## Core Logic & Mathematical Flow

### 1. Equity Derivatives (GBM & Barrier Payoff)
Price paths are generated using discretized Geometric Brownian Motion (GBM):

$$
S_{t+\Delta t} = S_t \exp\left( \left(r - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} Z \right)
$$

* **Up-and-In Call Payoff:** Triggered if $\max(S_0, S_1, \dots, S_T) \ge H$

$$
\text{Payoff} = \begin{cases}
\max(S_T - K, 0) & \text{if Knocked-In} \\
0 & \text{otherwise}
\end{cases}
$$

### 2. Interest Rate Derivatives (Yield Curve & Black-76)
* **Discount Factor:** $P(0, T) = \exp(-r(T) \cdot T)$
* **Forward Rate:**

$$
F(0; T_1, T_2) = \frac{\ln\left(\frac{P(0, T_1)}{P(0, T_2)}\right)}{T_2 - T_1}
$$

* **Swap Annuity & Forward Swap Rate:**

$$
A = \sum_{i=1}^{N} \tau_i P(0, T_i), \quad S_{T_{\text{start}}, T_{\text{end}}} = \frac{P(0, T_{\text{start}}) - P(0, T_{\text{end}})}{A}
$$

* **Black-76 Formula:**

$$
d_1 = \frac{\ln(F/K) + \frac{1}{2}\sigma^2 T}{\sigma \sqrt{T}}, \quad d_2 = d_1 - \sigma \sqrt{T}
$$

$$
\text{Caplet Price} = \tau \cdot P(0, T_2) \left[ F \Phi(d_1) - K \Phi(d_2) \right]
$$

$$
\text{Swaption Price} = A \cdot \left[ S \Phi(d_1) - K \Phi(d_2) \right]
$$

---

## Performance & Simulation Results

### 1. Equity Derivatives Benchmark (Module 01)
* **Benchmark (Black-Scholes European Call):** `1,223.45 KRW`
* **Test Parameters:** $S_0 = 15,500$, $K = 15,000$, $H = 16,000$, $T = 90/365$, $r = 2.5\%$, $\sigma = 30\%$

| Simulations ($N$) | Euro Call (MC) | Error Rate (%) | Up-and-In Call | Execution Time |
| :---: | :---: | :---: | :---: | :---: |
| **1,000** | 1,241.12 KRW | 1.444% | 1,189.50 KRW | 0.0123s |
| **5,000** | 1,218.80 KRW | 0.380% | 1,202.10 KRW | 0.0451s |
| **10,000** | 1,225.10 KRW | 0.135% | 1,217.23 KRW | 0.0890s |
| **50,000** | 1,223.90 KRW | 0.037% | 1,215.40 KRW | 0.4120s |
| **100,000** | 1,223.60 KRW | 0.012% | 1,216.05 KRW | 0.8351s |
| **200,000** | 1,223.48 KRW | 0.002% | 1,216.20 KRW | 1.6820s |

#### Multi-Path Dynamic Delta Hedging Results (100 Paths)
- **Knock-In Ratio:** `76.0%`
- **Mean Hedging Error:** **`38.08 KRW`** (Near-zero expected loss)
- **Std Deviation (Risk):** `209.73 KRW` (Discretization & gamma risk)

![Multi-Path Delta Hedging PnL Error Distribution](./01_Option_Pricing_and_Hedging/hedging_pnl_distribution.png)

---

### 2. Interest Rate Derivatives Benchmark (Module 02)
* **Market Zero Curve:** `[0.5y: 2.5%, 1.0y: 2.8%, 2.0y: 3.2%, 5.0y: 3.5%]`

| Instrument | Parameters | Underlying Forward | Black-76 Price |
| :--- | :--- | :---: | :---: |
| **Caplet (1y $\to$ 1.5y)** | $K = 3.0\%$, $\sigma = 20\%$ | `3.400%` | **`0.002404`** |
| **Payer Swaption (1y $\to$ 5y)** | $K = 3.2\%$, $\sigma = 25\%$ | `3.703%` | **`0.023384`** |

---

## How to Run

### Requirements
* Python 3.8+
* `numpy`, `scipy`, `matplotlib`

### Module 01: Equity Options & Dynamic Hedging
```bash
# Monte Carlo Convergence
python 01_Option_Pricing_and_Hedging/monte_carlo.py

# Dynamic Delta Hedging Engine
python 01_Option_Pricing_and_Hedging/delta_hedging.py

# Generate PnL Distribution Chart
python 01_Option_Pricing_and_Hedging/plot_hedging.py
```

### Module 02: Interest Rate Derivatives
```bash
# Yield Curve & Black-76 Caplet / Swaption Pricing
python 02_Interest_Rate_Derivatives/black76.py
```
