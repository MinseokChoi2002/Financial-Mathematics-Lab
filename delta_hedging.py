import numpy as np
from monte_carlo import MonteCarloOption
from mc_greeks import MonteCarloGreeks

class DeltaHedgingSimulator:
    """Simulates dynamic delta hedging for an Up-and-In barrier call option.

    Tracks daily rebalancing, stock transactions, and cash borrowing interest
    to calculate the final hedging error (PnL).
    """

    def __init__(self, mc_engine: MonteCarloOption):
        self.mc = mc_engine

    def _calculate_path_delta(self, S_current: float, days_remaining: int, t: int = 0) -> float:
        """Calculates dynamic delta at time t given remaining maturity."""
        if days_remaining <= 0:
            return 0.0

        sub_mc = MonteCarloOption(
            S0=S_current,
            K=self.mc.K,
            H=self.mc.H,
            T_days=days_remaining,
            r=self.mc.r,
            sigma=self.mc.sigma,
            n_simulations=self.mc.n_sims,
            seed=self.mc.seed + t + 1
        )

        sub_greeks = MonteCarloGreeks(sub_mc)
        return sub_greeks.calculate_delta(dS_pct=0.01)

    def simulate_single_path_hedging(self, path: np.ndarray) -> dict:
        """Simulates dynamic delta hedging along a single price path."""
        T_days = self.mc.T_days
        dt = 1.0 / 365.0
        r = self.mc.r

        # 1. Base option price at Day 0
        base_price, _ = self.mc.price_up_and_in_option()

        # Trajectory trackers
        stock_prices = path
        deltas = np.zeros(T_days + 1)
        shares_held = np.zeros(T_days + 1)
        cash_account = np.zeros(T_days + 1)

        # Check if path touched barrier
        knocked_in = np.max(path) >= self.mc.H

        # --- Day 0 Setup ---
        deltas[0] = self._calculate_path_delta(S_current=stock_prices[0], days_remaining=T_days, t=0)
        shares_held[0] = deltas[0]
        cash_account[0] = base_price - (shares_held[0] * stock_prices[0])

        # --- Day 1 to T-1 ---
        for t in range(1, T_days):
            S_t = stock_prices[t]
            days_remaining = T_days - t

            # Cash balance accrues interest
            cash_account[t] = cash_account[t - 1] * np.exp(r * dt)

            # Recalculate Delta at time t
            deltas[t] = self._calculate_path_delta(S_current=S_t, days_remaining=days_remaining, t=t)

            # Rebalancing stock holdings
            d_shares = deltas[t] - shares_held[t - 1]
            cash_account[t] -= d_shares * S_t
            shares_held[t] = deltas[t]

        # --- Day T ---
        S_T = stock_prices[-1]
        cash_account[T_days] = cash_account[T_days - 1] * np.exp(r * dt)
        cash_account[T_days] += shares_held[T_days - 1] * S_T

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

    def simulate_multi_path_hedging(self, paths: list) -> dict:
        """Simulates dynamic delta hedging across multiple price paths to aggregate performance metrics."""
        results_list = []
        num_paths = len(paths)

        print(f"Starting multi-path delta hedging simulation ({num_paths} paths)...")

        for i, path in enumerate(paths):
            res = self.simulate_single_path_hedging(path)
            results_list.append(res)

            # Print progress every 20 paths
            if (i + 1) % 20 == 0 or (i + 1) == num_paths:
                print(f"Processed {i + 1}/{num_paths} paths...")

        pnls = np.array([r['final_pnl'] for r in results_list])
        knocked_ins = np.array([r['knocked_in'] for r in results_list])

        summary = {
            "mean_pnl": np.mean(pnls),
            "std_pnl": np.std(pnls),
            "min_pnl": np.min(pnls),
            "max_pnl": np.max(pnls),
            "knock_in_rate": np.mean(knocked_ins) * 100,
            "all_pnls": pnls
        }
        return summary


if __name__ == "__main__":
    # Configure base option for hedging simulation
    mc = MonteCarloOption(
        S0=15500, K=15000, H=16000, T_days=90, r=0.025, sigma=0.30, n_simulations=2000, seed=42
    )

    # Generate 100 sample price paths
    num_test_paths = 100
    all_paths = mc.generate_paths()[:num_test_paths]

    # Instantiate and run multi-path hedging simulator
    simulator = DeltaHedgingSimulator(mc)
    summary = simulator.simulate_multi_path_hedging(all_paths)

    print("\n=== Multi-Path Delta Hedging Statistical Summary ===")
    print(f"Total Simulation Paths : {num_test_paths}")
    print(f"Knock-In Ratio         : {summary['knock_in_rate']:.1f}%")
    print(f"Mean Hedging Error     : {summary['mean_pnl']:,.2f} KRW")
    print(f"Std Deviation (Risk)   : {summary['std_pnl']:,.2f} KRW")
    print(f"Min PnL (Worst Case)   : {summary['min_pnl']:,.2f} KRW")
    print(f"Max PnL (Best Case)    : {summary['max_pnl']:,.2f} KRW")
