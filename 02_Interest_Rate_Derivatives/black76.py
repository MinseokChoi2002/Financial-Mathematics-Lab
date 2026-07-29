import numpy as np 
from scipy.stats import norm
from yield_curve import YieldCurve

class Black76Model:
    """
    Black-76 pricing engine for Caplets and Swaptions.
    """

    @staticmethod
    def option_price(F: float, K: float, T: float, sigma: float, df: float, option_type: str = 'call') -> float:
        """
        Computes standard Black_76 option prices on forward contracts.

        - F: Forward rate or price.
        - K : Strike rate or price.
        - T : Time to expiry in years.
        - sigma : Black implied volatility.
        - df : Discount factor P(0, T).
        """

        if T <= 0 or sigma <= 0:
            payoff = max(0.0, F - K) if option_type.lower() == 'call' else max(0.0, K - F)
            return df * payoff
        
        d1 = (np.log(F / K) + 0.5 * (sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if option_type.lower() == 'call':
            price = df * (F * norm.cdf(d1) - K * norm.cdf(d2))
        elif option_type.lower() == 'put':
            price = df * (K * norm.cdf(-d2) - F * norm.cdf(-d1))
        else:
            raise ValueError("option_type must be either 'call' or 'put'.")
        return price
    
    @staticmethod
    def caplet_price(K: float, T1: float, T2: float, sigma: float, curve: YieldCurve) -> float:
        """
        Price a single Caplet covering interval [T1, T2].
        - T1: Fixing date (expiry)
        - T2: Payment date
        - K: Strike rate
        """

        tau = T2 - T1 # Accrual period
        df_T2 = curve.get_discount_factor(T2)
        F = curve.get_forward_rate(T1, T2)
        caplet_val = tau * Black76Model.option_price(F, K, T1, sigma, df_T2, option_type='call')
        return caplet_val, F 

    @staticmethod
    def swaption_price(K: float, T_start: float, T_end: float, sigma: float, curve: YieldCurve, swaption_type: str = 'payer') -> float:
        """
        Price a European Swaption
        - payer : Right to pay fixed rate (Call option on swap rate)
        - receiver : Right to receive fixed rate (Put option on swap rate)
        """

        F_swap, annuity = curve.get_swap_annuity(T_start, T_end)
        option_type = 'call' if swaption_type.lower() == 'payer' else 'put'
        swaption_val = annuity * Black76Model.option_price(F_swap, K, T_start, sigma, df=1.0, option_type=option_type)
        return swaption_val, F_swap

if __name__ == "__main__":
    # --- Test Case ---
    # 1. Initialize market zero curve
    maturities = [0.5, 1.0, 2.0, 5.0]
    zero_rates = [0.025, 0.028, 0.032, 0.035]
    curve = YieldCurve(maturities, zero_rates)

    # 2. Caplet Test
    caplet_val, fwd_rate = Black76Model.caplet_price(K=0.030, T1=1.0, T2=1.5, sigma=0.20, curve=curve)
    print("=== Black-76 Caplet Pricing ===")
    print(f"Forward Rate: {fwd_rate * 100:.3f}% | Price: {caplet_val:.6f}")

    # 3. Payer Swaption Test
    swaption_val, fwd_swap = Black76Model.swaption_price(K=0.032, T_start=1.0, T_end=5.0, sigma=0.25, curve=curve, swaption_type='payer')
    print("\n=== Black-76 Payer Swaption Pricing ===")
    print(f"Forward Swap Rate: {fwd_swap * 100:.3f}% | Price: {swaption_val:.6f}")