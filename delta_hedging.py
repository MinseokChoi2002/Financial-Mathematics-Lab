import numpy as np
from monte_carlo import MonteCarloOption
from mc_greeks import MonteCarloGreeks

class DeltaHedgingSimulator :
  """ Simulates dynamic delta hedging for an Up-and-In barrier call option.

  Tracks daily rebalancing, stock transactions, and cash borrowing interest
  to calculate the final hedging error (PnL).
  """

  def __init__(self, mc_engine: MonteCarloOption):
    self.mc = mc_engine
    self.greeks_engine = MonteCarloGreeks(mc_engine)

  def simulate_single_path_hedging(self, path: np.ndarray) -> dict:
    """ Simulates dynamic delta hedging along a single price path.

    Args:
      path (array-like) : Stock price array of length (T_days + 1).
    returns:
      dict : Hedging performance metrics and daily trajectory logs.
    """

    T_days = self.mc.T_days
    dt = 1.0 / 365.0
    r = self.mc.r

    # 1. Base option price at Day 0
    base_price,_ = self.mc.price_up_and_in_option()

    # Trajectory trackers
    stock_prices = path
    deltas = np.zeros(T_days + 1)
    shares_held = np.zeros(T_days + 1)
    cash_account = np.zeros(T_days + 1)

    # Check if path touched barrier
    knocked_in = np.max(path) >= self.mc.H

    # --- Day0 Setup ---
    deltas[0] = self._calculate_path_delta(S_current = stock_prices[0], days_remaining = T_days)
    shares_held[0] = deltas[0]
    # Cash = Option premium received - Cost of buying initial stock shares
    cash_account[0] = base_price - (shares_held[0] * stock_prices[0])

    # --- Day1 to T-1 ---
    for t in range(1, T_days):
      S_t = stock_prices[t]
      days_remaining = T_days - t

      # Cash balance accures interest
      cash_account[t] = cash_account[t-1] * np.exp(-r * dt)

      # Recalculate Delta at time t
      deltas[t] = self._calculate_path_delta(S_current = S_t, days_remaining = days_remaining)

      # Rebalancing stock holdings
      d_shares = deltas[t] - shares_held[t-1]
      cash_account[t] -= d_shares * S_t
      shares_held[t] = deltas[t]
    
    # --- Day T ---
    S_T = stock_prices[-1]
    cash_account[T_days] = cash_account[T_days-1] * np.exp(-r * dt)
    cash_account[T_days] += shares_held[T_days-1] * S_T
    
    payoff = max(S_T - self.mc.K, 0.0) if knocked_in else 0.0
    
    final_pnl = cash_account[T_days] - payoff

    return {
        "initial_option_price": base_price,
        "final_stock_price": S_T,
        "knocked_in": knocked_in,
        "payoff": payoff,
        "final_pnl": final_pnl,
        "stock_prices": stock_prices,
        "deltas": deltas,
        "cash_account": cash_account
        
    }

  def _calculate_path_delta(self, S_current: float, days_remaining: int) -> float:
    """Calculates dynamic delta at time t given remaining maturity."""

    if days_remaining == 0:
      return 0.0
    
    sub_mc = MonteCarloOption(
        S0 = S_current,
        K = self.mc.K,
        H = self.mc.H,
        T_days = days_remaining,
        r = self.mc.r,
        sigma = self.mc.sigma,
        n_simulations = self.mc.n_sims,
        seed = self.mc.seed + t + 1
    )
    
    sub_greeks = MonteCarloGreeks(sub_mc)

    return sub_greeks.calculate_delta(dS_pct = 0.01)
  
if __name__ == "__main__":
    # 1. Base Setup
    mc = MonteCarloOption(
        S0=15500, K=15000, H=16000, T_days=90, r=0.025, sigma=0.30, n_simulations=10000, seed=42
    )
    
    # 2. Generate a single sample price path (90 days)
    np.random.seed(123)
    dt = 1.0 / 365.0
    Z = np.random.standard_normal(90)
    drift = (mc.r - 0.5 * mc.sigma**2) * dt
    diffusion = mc.sigma * np.sqrt(dt) * Z
    
    sample_path = np.zeros(91)
    sample_path[0] = mc.S0
    for t in range(1, 91):
        sample_path[t] = sample_path[t - 1] * np.exp(drift + diffusion[t - 1])
        
    # 3. Run Delta Hedging Simulation
    simulator = DeltaHedgingSimulator(mc)
    results = simulator.simulate_single_path_hedging(sample_path)
    
    print("--- Dynamic Delta Hedging Simulation Results ---")
    print(f"Initial Option Price Received : {results['initial_option_price']:,.2f} KRW")
    print(f"Final Stock Price (S_T)       : {results['final_stock_price']:,.2f} KRW")
    print(f"Option Knocked In?            : {results['knocked_in']}")
    print(f"Option Payoff Owed            : {results['payoff']:,.2f} KRW")
    print(f"Final Hedging PnL (Hedging Error): {results['final_pnl']:,.2f} KRW")