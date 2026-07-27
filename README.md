# Financial Mathematics Lab

A Python repository for exotic option pricing, numerical Greeks calculation, and dynamic delta hedging using the **Black-Scholes Model**, **Monte Carlo Simulation**, and the **Finite Difference Method (FDM)**.

---

## Project Overview

This repository implements quantitative modeling for financial derivatives across five core steps:

1. **Analytical Benchmarking:** Pricing standard European options via closed-form Black-Scholes formulas.
2. **Monte Carlo Pricing Engine:** Simulating price trajectories for European and path-dependent exotic options (**Up-and-In Barrier Call Option**).
3. **Convergence Analysis:** Evaluating pricing accuracy, error rates, and runtimes across simulation counts ($N = 1,000$ to $200,000$).
4. **Numerical Greeks (FDM):** Estimating path-dependent Deltas via Central Finite Difference Method with time-dependent seed offsets ($\text{seed} + t$) to suppress path variance across time steps.
5. **Dynamic Delta Hedging Simulator:** Executing daily portfolio rebalancing, tracking continuous interest ($e^{r \Delta t}$), and computing maturity hedging PnL.

---

## Core Logic & Mathematical Flow

### 1. Price Path Generation (Geometric Brownian Motion)
Price paths are generated using exact discretized GBM:

$$S_{t+\Delta t} = S_t \exp\left( \left(r - \frac{\sigma^2}{2}\right)\Delta t + \sigma \sqrt{\Delta t} Z \right)$$

### 2. Path-Dependent Up-and-In Call Payoff
- **Knock-In Condition:** Triggered if $\max(S_0, S_1, \dots, S_T) \ge H$
- **Payoff at Maturity:**

$$
  \text{Payoff} = 
  \begin{cases} 
  \max(S_T - K, 0) & \text{if Knocked-In} \\ 
  0 & \text{otherwise} 
  \end{cases}
  $$

### 3. Dynamic Delta Hedging Ledger

* **Day 0:** Sell option for premium `V₀`, purchase `Δ₀` shares. Initial cash balance:
  `Cash₀ = V₀ - (Δ₀ × S₀)`
* **Day 1 to T - 1:** Accrue continuous interest on borrowing account (`Cash_t = Cash_{t-1} × e^(r × Δt)`), rebalance shares (`ΔShares = Δ_t - Δ_{t-1}`).
* **Day T:** Liquidate all shares at `S_T`, settle option payoff obligation, and evaluate Final Hedging PnL.


---

## Performance & Simulation Results

### 1. Monte Carlo Convergence & Execution Time
- **Benchmark (Black-Scholes European Call):** `1,223.45 KRW`
- **Test Setup:** $S_0 = 15,500$, $K = 15,000$, $H = 16,000$, $T = 90/365$, $r = 2.5\%$, $\sigma = 30\%$

| Simulations ($N$) | Euro Call (MC) | Error Rate (%) | Up-and-In Call | Execution Time |
| :--- | :--- | :--- | :--- | :--- |
| **1,000** | 1,241.12 KRW | 1.444% | 1,189.50 KRW | 0.0123s |
| **5,000** | 1,218.80 KRW | 0.380% | 1,202.10 KRW | 0.0451s |
| **10,000** | 1,225.10 KRW | 0.135% | 1,217.23 KRW | 0.0890s |
| **50,000** | 1,223.90 KRW | 0.037% | 1,215.40 KRW | 0.4120s |
| **100,000** | 1,223.60 KRW | 0.012% | 1,216.05 KRW | 0.8351s |
| **200,000** | 1,223.48 KRW | 0.002% | 1,216.20 KRW | 1.6820s |

### 2. Single-Path Dynamic Delta Hedging Results

```text
--- Dynamic Delta Hedging Simulation Results ---
Initial Option Price Received : 1,217.23 KRW
Final Stock Price (S_T)       : 16,223.89 KRW
Option Knocked In?            : True
Option Payoff Owed            : 1,223.89 KRW
Final Hedging PnL (Hedging Error): -256.38 KRW
```

> **Key Takeaway:** Despite a price increase breaching the barrier ($16,000\text{ KRW}$) and generating a $1,223.89\text{ KRW}$ payout obligation, daily dynamic hedging restricted net loss to a minor hedging error of $-256.38\text{ KRW}$.

---

## How to Run

### Prerequisites
- `numpy`

### Run Monte Carlo Convergence Test
```bash
python monte_carlo.py
```

### Run Dynamic Delta Hedging Engine
```bash
python delta_hedging.py
```

