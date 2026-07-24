import numpy as np
from scipy.stats import norm

class BlackScholesModel :

  def __init__(self, S0, K, T, r, sigma) :
    self.S0 = float(S0)
    self.K = float(K)
    self.T = float(T)
    self.r = float(r)
    self.sigma = float(sigma)

    self.d1 = (np.log(self.S0 / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
    self.d2 = self.d1 - self.sigma * np.sqrt(self.T)

  def price(self, option_type) :
    if option_type == 'call' :
      return self.S0 * norm.cdf(self.d1)  - np.exp(-self.r * self.T) * self.K * norm.cdf(self.d2)
    elif option_type == 'put' :
      return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2) - self.S0 * norm.cdf(-self.d1)
    else :
      raise ValueError("option_type은 'call' 또는 'put'으로 입력하세요.")
  
  def delta(self, option_type) :
    if option_type == 'call' :
      return norm.cdf(self.d1)
    elif option_type == 'put' :
      return -norm.cdf(-self.d1)
  
  def gamma(self, option_type) :
    return norm.pdf(self.d1) / (self.S0 * self.sigma * np.sqrt(self.T))
  
  def vega(self, option_type) :
    return self.S0 * norm.pdf(self.d1) * np.sqrt(self.T) * 0.01

  def theta(self, option_type) :

    term1 = -self.S0 * norm.pdf(self.d1) * self.sigma / (2 * np.sqrt(self.T))

    if option_type == 'call' :
      term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
      theta_annual = term1 - term2
    elif option_type == 'put' :
      term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
      theta_annual = term1 + term2

    return theta_annual / 365.0

  def rho(self, option_type) :
    if option_type == 'call' :
      rho_annual = self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2)
    elif option_type == 'put' :
      rho_annual = -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
    
    return rho_annual * 0.01
  
  def get_all_greeks(self, option_type) :
    return {
        'Price' : self.price(option_type),
        'delta' : self.delta(option_type),
        'gamma' : self.gamma(option_type),
        'vega' : self.vega(option_type),
        'theta' : self.theta(option_type),
        'rho' : self.rho(option_type)
    }

# --------------------------------------
# Test Case
# --------------------------------------

if __name__ == "__main__":
  S_test = 100.0
  K_test = 100.0
  T_test = 1.0
  r_test = 0.05
  sigma_test = 0.20

  model = BlackScholesModel(S_test, K_test, T_test, r_test, sigma_test)
  greeks = model.get_all_greeks(option_type_test)

  print("=== Black-Scholes European Option Pricing & Greeks Engine ===")
  print(f"Inputs: S0={S_test}, K={K_test}, T={T_test}yr, r={r_test*100}%, sigma={sigma_test*100}%\n")

  print(f"{'Metric':<15} | {'Call Option':<15} | {'Put Option':<15}")
  print("-" * 50)

  call_greeks = model.get_all_greeks('call')
  put_greeks = model.get_all_greeks('put')

  for key in call_greeks.keys():
      print(f"{key:<15} | {call_greeks[key]:<15.4f} | {put_greeks[key]:<15.4f}")
