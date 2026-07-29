import numpy as np

class YieldCurve:
    """
    Computes discount factors, forward rates, and swap annuities from a given zero yield curve.
    """

    def __init__(self, maturities, zero_rates):
        """
        - maturities: Array of maturities in years (e.g. [0.5, 1.0, 2.0, 5,0]).
        - zero_rates: Array of continuously compounded zero rates (e.g. [0.025, 0.028, 0.030, 0.035])
        """
        
        self.maturities = np.array(maturities)
        self.zero_rates = np.array(zero_rates)

    def get_discount_factor(self, T: float) -> float:
        """
        Calculates the discount factor P(O, T) = exp(-r(T) * T) using linear interpolation.
        """

        # Linear interpolation for zero rate at maturity T
        r_T = np.interp(T, self.maturities, self.zero_rates)
        return np.exp(-r_T * T)
    
    def get_forward_rate(self, T1: float, T2: float) -> float:
        """
        Calculates the continuously compounded forward rate F(0; T1, T2).
        """

        if T2 <= T1:
            raise ValueError("T2 must be strictly greater than T1.")
        
        p1 = self.get_discount_factor(T1)
        p2 = self.get_discount_factor(T2)
        return np.log(p1 / p2) / (T2 - T1)
    
    def get_swap_annuity(self, T_start: float, T_end: float, freq: float = 0.5):
        """
        Calculates the forward swap rate and swap annuity (A).
        - freq : Payment frequency in years (default: 0.5 = 6 months).
        """

        patyment_times = np.arange(T_start + freq, T_end + 1e-6, freq)
        df_start = self.get_discount_factor(T_start)
        df_end = self.get_discount_factor(T_end)

        annuity = sum(freq * self.get_discount_factor(t) for t in patyment_times)
        forward_swap_rate = (df_start - df_end) / annuity
        return forward_swap_rate, annuity
        


        