import time
import numpy as np
from black_scholes import BlackScholesModel

class MonteCarloOption:

    def __init__(self, S0, K, H, T_days, r, sigma, n_simulations=10000, seed=42):
        self.S0 = float(S0)  
        self.K = float(K)        
        self.H = float(H)            # 배리어 가격 
        self.T = T_days / 365.0      # 잔존기간 
        self.T_days = int(T_days)    # 일일 단위 경로 추적 수
        self.r = float(r)            
        self.sigma = float(sigma)    
        self.n_sims = int(n_simulations)     
        self.dt = self.T / self.T_days    # 일일 시간 간격 (dt)
        self.seed = seed
  
    def generate_paths(self):
        if self.seed is not None:
            np.random.seed(self.seed)
        
        Z = np.random.standard_normal((self.n_sims, self.T_days))

        term1 = (self.r - 0.5 * self.sigma ** 2) * self.dt
        term2 = self.sigma * np.sqrt(self.dt) * Z
        d_returns = np.exp(term1 + term2)

        # (n_sims, T_days + 1) 크기의 경로 행렬 생성 (0일차~90일차: 총 91개 기둥)
        price_paths = np.zeros((self.n_sims, self.T_days + 1))
        price_paths[:, 0] = self.S0
        price_paths[:, 1:] = self.S0 * np.cumprod(d_returns, axis=1)

        return price_paths

    def price_up_and_in_option(self):
        paths = self.generate_paths()
        max_prices = np.max(paths, axis=1)
        knock_in = max_prices >= self.H
        ST = paths[:, -1]

        payoffs = np.where(knock_in, np.maximum(ST - self.K, 0), 0.0)

        option_price = np.exp(-self.r * self.T) * np.mean(payoffs)
        knock_in_prob = np.mean(knock_in) * 100.0
        return option_price, knock_in_prob

    def price_european_call(self):
      # 몬테카를로 방식 유러피안 콜옵션 가격

      paths = self.generate_paths()
      ST = paths[:, -1]
      payoffs = np.maximum(ST - self.K, 0.0)
      mc_price = np.exp(-self.r * self.T) * np.mean(payoffs)
      return mc_price

    def black_scholes_call(self):
      # 블랙-숄즈 공식을 이용한 유러피안 콜옵션 이론적 정답

        bs_model = BlackScholesModel(
            S0=self.S0,
            K=self.K,
            T=self.T,
            r=self.r,
            sigma=self.sigma
        )

        return bs_model.price('call')

    

#--------------------------------------
# Test Case
#--------------------------------------

if __name__ == "__main__":
    # 시뮬레이션 횟수 테스트 리스트 (1,000회 ~ 200,000회)
    sim_counts = [1000, 5000, 10000, 50000, 100000, 200000]

    # 블랙-숄즈 이론가 기준점 계산
    bs_model = BlackScholesModel(
        S0=15500, K=15000, T=90 / 365.0, r=0.025, sigma=0.30
    )
    bs_price = bs_model.price("call")

    print("=== 몬테카를로 수렴도 및 실행시간 분석 ===")
    print(f"Black-Scholes 기준 정답 : {bs_price:,.2f} 원\n")
    print(
        f"{'Simulations (N)':>15} | {'Euro Call (MC)':>15} | {'오차율 (%)':>10} | {'Up-and-In Call':>15} | {'소요시간 (초)':>12}"
    )
    print("-" * 80)

    for n_sim in sim_counts:
        start_time = time.time()

        # 시뮬레이션 실행 (동일 조건 비교를 위해 seed 고정)
        mc = MonteCarloOption(
            S0=15500,
            K=15000,
            H=16000,
            T_days=90,
            r=0.025,
            sigma=0.30,
            n_simulations=n_sim,
            seed=42,
        )

        ui_price, _ = mc.price_up_and_in_option()
        mc_euro_price = mc.price_european_call()

        elapsed_time = time.time() - start_time
        error_rate = abs(mc_euro_price - bs_price) / bs_price * 100

        print(
            f"{n_sim:>15,}회 | {mc_euro_price:>15,.2f}원 | {error_rate:>9.3f}% | {ui_price:>15,.2f}원 | {elapsed_time:>11.4f}s"
        )
