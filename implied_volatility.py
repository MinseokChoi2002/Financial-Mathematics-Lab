import numpy as np
from black_scholes import BlackScholesModel

def implied_volatility_newton(S0, K, T, r, C_market, sigma_init=0.30, tol=1e-4, max_iter=100):

    sigma = sigma_init
    
    print(f"{'Iter':<5} | {'Sigma':<10} | {'BS Call Price':<15} | {'Error':<10}")
    print("-" * 55)
    
    for i in range(1, max_iter + 1):
        bs = BlackScholesModel(S0=S0, K=K, T=T, r=r, sigma=sigma)
        price = bs.price('call')
        vega_derivative = bs.vega('call') * 100.0
        diff = price - C_market
        error = abs(diff)
        
        print(f"{i:<5} | {sigma:<10.6f} | {price:<15.4f} | {error:<10.6f}")
        
        if error < tol:
            print("-" * 55)
            print(f"수렴 완료! 내재변동성(IV) = {sigma:.6f} ({sigma * 100:.2f}%)")
            return sigma
        
        if vega_derivative == 0:
            print("Vega가 0에 가까워 수치해석을 중단합니다.")
            return None
            
        sigma = sigma - diff / vega_derivative

    print("최대 반복 횟수 내에 수렴하지 못했습니다.")
    return None


# ---------------------------------------------------------
# Test Case
# ---------------------------------------------------------
if __name__ == "__main__":
    S_test = 7800.0
    K_test = 8000.0
    r_test = 0.03
    T_test = 15.0 / 365.0
    C_market_test = 150.0

    print("Implied Volatility Solver (Powered by BlackScholesModel)\n")
    iv = implied_volatility_newton(
        S0=S_test, 
        K=K_test, 
        T=T_test, 
        r=r_test, 
        C_market=C_market_test
    )
