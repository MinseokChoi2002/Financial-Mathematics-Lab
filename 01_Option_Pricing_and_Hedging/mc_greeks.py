import numpy as np
from monte_carlo import MonteCarloOption


class MonteCarloGreeks:
    """
    Calculates Monte Carlo Greeks (Delta, Vega) for Exotic Options
    using Finite Difference Method (FDM) with Common Random Numbers (CRN).
    """

    def __init__(self, mc_engine: MonteCarloOption):
        self.mc = mc_engine

    def calculate_delta(self, dS_pct: float = 0.01) -> float:
        """
        Calculates Delta (dS_0 sensitivity) using Central Finite Difference with CRN.
        
        Parameters:
            dS_pct: Bump percentage for initial asset price S0 (default: 1%)
        Returns:
            Delta value (dOption_Price / dS_0)
        """
        dS = self.mc.S0 * dS_pct
        
        # 1. Bump S0 up & down
        S0_up = self.mc.S0 + dS
        S0_down = self.mc.S0 - dS
        
        # 2. Generate common random normal variables (CRN) to eliminate Monte Carlo noise
        np.random.seed(self.mc.seed)
        Z = np.random.standard_normal((self.mc.n_sims, self.mc.T_days))
        
        # 3. Simulate paths for S0_up with CRN
        paths_up = self._generate_paths_with_Z(S0_up, self.mc.r, self.mc.sigma, Z)
        payoffs_up = self._calculate_payoff(paths_up)
        price_up = np.exp(-self.mc.r * self.mc.T_days/365.0) * np.mean(payoffs_up)
        
        # 4. Simulate paths for S0_down with CRN
        paths_down = self._generate_paths_with_Z(S0_down, self.mc.r, self.mc.sigma, Z)
        payoffs_down = self._calculate_payoff(paths_down)
        price_down = np.exp(-self.mc.r * self.mc.T_days/365.0) * np.mean(payoffs_down)
        
        # 5. Central Difference Formula: (V_up - V_down) / (2 * dS)
        delta = (price_up - price_down) / (2 * dS)
        return delta

    def calculate_vega(self, dsigma: float = 0.01) -> float:
        """
        Calculates Vega (dVol sensitivity) using Central Finite Difference with CRN.
        
        Parameters:
            dsigma: Volatility bump amount (default: +1 percentage point = 0.01)
        Returns:
            Vega value (dOption_Price / dSigma)
        """
        sigma_up = self.mc.sigma + dsigma
        sigma_down = max(0.0001, self.mc.sigma - dsigma)
        
        np.random.seed(self.mc.seed)
        Z = np.random.standard_normal((self.mc.n_sims, self.mc.T_days))
        
        paths_up = self._generate_paths_with_Z(self.mc.S0, self.mc.r, sigma_up, Z)
        payoffs_up = self._calculate_payoff(paths_up)
        price_up = np.exp(-self.mc.r * self.mc.T_days/365.0) * np.mean(payoffs_up)
        
        paths_down = self._generate_paths_with_Z(self.mc.S0, self.mc.r, sigma_down, Z)
        payoffs_down = self._calculate_payoff(paths_down)
        price_down = np.exp(-self.mc.r * self.mc.T_days/365.0) * np.mean(payoffs_down)
        
        vega = (price_up - price_down) / (2 * dsigma)
        return vega

    def _generate_paths_with_Z(self, S0: float, r: float, sigma: float, Z: np.ndarray) -> np.ndarray:
        """Helper method to generate GBM paths using pre-computed random matrix Z."""
        dt = 1.0 / 365.0
        drift = (r - 0.5 * sigma**2) * dt
        diffusion = sigma * np.sqrt(dt) * Z
        
        daily_returns = np.exp(drift + diffusion)
        
        paths = np.zeros((self.mc.n_sims, self.mc.T_days + 1))
        paths[:, 0] = S0
        
        for t in range(1, self.mc.T_days + 1):
            paths[:, t] = paths[:, t - 1] * daily_returns[:, t - 1]
            
        return paths

    def _calculate_payoff(self, paths: np.ndarray) -> np.ndarray:
        """Helper method for Up-and-In Barrier Call payoff."""
        max_prices = np.max(paths, axis=1)
        knock_in_flags = max_prices >= self.mc.H
        
        ST = paths[:, -1]
        raw_payoffs = np.maximum(ST - self.mc.K, 0)
        
        return raw_payoffs * knock_in_flags


if __name__ == "__main__":
    # 1. Initialize Base Option Parameters
    mc = MonteCarloOption(
        S0=15500,
        K=15000,
        H=16000,
        T_days=90,
        r=0.025,
        sigma=0.30,
        n_simulations=100000,
        seed=42
    )

    # 2. Run Base Option Price
    base_price, _ = mc.price_up_and_in_option()
    print(f"--- Monte Carlo Greeks Engine Benchmark ---")
    print(f"Option Base Price (S0={mc.S0}): {base_price:,.2f} KRW")

    # 3. Calculate Greeks using FDM
    greeks_engine = MonteCarloGreeks(mc)
    
    delta = greeks_engine.calculate_delta(dS_pct=0.01)
    vega = greeks_engine.calculate_vega(dsigma=0.01)

    print(f"Calculated Delta (Δ): {delta:.4f}")
    print(f"Calculated Vega  (ν): {vega:.2f} KRW per 100% vol change ({vega/100:.2f} per 1% vol)")