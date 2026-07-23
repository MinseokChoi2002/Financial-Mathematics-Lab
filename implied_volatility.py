import numpy as np
from scipy.stats import norm

def black_scholes_call(S0, K, T, r, sigma) :
  d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T)/(sigma * np.sqrt(T))
  d2 = d1 - sigma * np.sqrt(T)
  call_price = (S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
  return call_price

def bs_vega(S0, K, T, r, sigma) :
  d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T)/(sigma * np.sqrt(T))
  vega = S0 * np.sqrt(T) * norm.pdf(d1)
  return vega

def impl_vol_newton_raphson(S, K, T, r, C_market, sigma_init=0.3, tol=0.0001, max_iter=100):

    sigma = sigma_init
    
    print(f"{'Iter':<5} | {'Sigma':<10} | {'BS Call Price':<15} | {'Error':<10}")
    print("-" * 50)

    for i in range(max_iter) :
      price = black_scholes_call(S, K, T, r, sigma)
      vega = bs_vega(S, K, T, r, sigma)
      diff = price - C_market

      print(f"{i+1:<5} | {sigma:<10.6f} | {price:<15.4f} | {abs(diff):<10.6f}")

      if abs(diff) < tol :
        print("-" * 50)
        print(f"수렴 완료! 내재변동성 : {sigma:.6f} ({sigma*100:.2f}%)")
        return sigma
      
      if vega == 0:
        print("Vega가 0에 수렴하여 뉴턴 메소드를 계속할 수 없습니다.")
        return None

      sigma = sigma - diff/vega
    
    return vega

if __name__ == "__main__":
    S = 7800.0
    K = 8000.0
    r = 0.03
    T = 15.0 / 365.0
    C_market = 150.0
    
    print("=== Newton-Raphson Implied Volatility Solver Test ===")
    impl_vol_newton_raphson(S, K, T, r, C_market, sigma_init=0.30, tol=0.0001)
