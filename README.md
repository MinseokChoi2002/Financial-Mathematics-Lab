# 📈 Financial Mathematics Lab

> **Python-based Quantitative Finance & Numerical Methods Engine**
> 
> 본 저장소는 금융수학(Financial Mathematics) 이론과 수치해석 기법을 바탕으로 유럽형 옵션 가격 결정 모델(Option Pricing Models), 민감도 지표(Greeks), 그리고 내재변동성(Implied Volatility) 수치해석 엔진을 Python 객체지향 구조로 구현하고 검증하는 연구 공간입니다.

---

## 1. 주요 구현 모듈 (Key Features)

| 파일명 | 기능 및 핵심 알고리즘 | 설명 |
| :--- | :--- | :--- |
| **`black_scholes.py`** | European Option Pricing & 5 Greeks Engine | Black-Scholes 공식을 이용한 Call/Put 옵션 가치 산출 및 5대 민감도 지표 ($\Delta, \Gamma, \nu, \Theta, \rho$) 산출 |
| **`implied_volatility.py`** | Newton-Raphson Implied Volatility Solver | 옵션의 시장 가격($C_{market}$)으로부터 내재변동성($\sigma$)을 역산하는 수치해석 엔진 |

---

## 2. 수학적 배경 (Mathematical Background)

### 1) Black-Scholes Model & Greeks (`black_scholes.py`)
유러피안 옵션의 이론가 $C, P$ 및 주요 민감도는 다음과 같습니다.

$$d_1 = \frac{\ln(S_0 / K) + \left(r + \frac{\sigma^2}{2}\right)T}{\sigma \sqrt{T}}, \quad d_2 = d_1 - \sigma \sqrt{T}$$

* **Call / Put Price**:
  $$C = S_0 N(d_1) - K e^{-rT} N(d_2), \quad P = K e^{-rT} N(-d_2) - S_0 N(-d_1)$$
* **Greeks (민감도 지표)**:
  * **Delta ($\Delta$)**: $\frac{\partial C}{\partial S} = N(d_1)$ (Call), $N(d_1) - 1$ (Put)
  * **Gamma ($\Gamma$)**: $\frac{\partial^2 C}{\partial S^2} = \frac{N'(d_1)}{S_0 \sigma \sqrt{T}}$
  * **Vega ($\nu$)**: $\frac{\partial C}{\partial \sigma} = S_0 N'(d_1) \sqrt{T} \times 0.01$ ($1\%p$ 변동 기준)
  * **Theta ($\Theta$)**: $\frac{\partial C}{\partial T} \times \frac{1}{365}$ ($1$일 경과 기준)
  * **Rho ($\rho$)**: $\frac{\partial C}{\partial r} \times 0.01$ (금리 $1\%p$ 변동 기준)

---

### 2) Newton-Raphson Method for Implied Volatility (`implied_volatility.py`)
내재변동성은 역함수 해(Closed-form solution)가 존재하지 않으므로, 아래 점화식을 통해 수치적으로 수렴시킵니다.

$$\sigma_{n+1} = \sigma_n - \frac{C_{BS}(\sigma_n) - C_{market}}{\text{Vega}(\sigma_n)}$$

---

## 3. 실행 및 검증 결과 (Case Studies)

### Case 1: 블랙-숄즈 가격 및 Greeks 산출 (`black_scholes.py`)
* **조건**: $S_0 = 100$, $K = 100$, $T = 1$년, $r = 5\%$, $\sigma = 20\%$

| Metric | Call Option | Put Option | 설명 |
| :--- | :---: | :---: | :--- |
| **Price** | **10.4506** | **5.5735** | 옵션 이론 가격 ($) |
| **Delta ($\Delta$)** | 0.6368 | -0.3632 | 주가 $1$달러 변동 시 옵션가 변동 폭 |
| **Gamma ($\Gamma$)** | 0.0188 | 0.0188 | 주가 $1$달러 변동 시 Delta 변동 폭 |
| **Vega ($\nu$, 1%p)** | 0.3752 | 0.3752 | 변동성 $1\%p$ 증가 시 옵션가 변동 폭 |
| **Theta ($\Theta$, 1일)** | -0.0176 | -0.0045 | $1$일 경과 시 시간가치 감소량 |
| **Rho ($\rho$, 1%p)** | 0.5323 | -0.4189 | 금리 $1\%p$ 인상 시 옵션가 변동 폭 |

---

### Case 2: 내재변동성 수치해석 수렴 과정 (`implied_volatility.py`)
* **조건**: $S_0 = 7800$, $K = 8000$, $T = 15/365$, $r = 3\%$, $C_{market} = 150$, $\sigma_0 = 30\%$

| Iteration | Sigma ($\sigma$) | BS Call Price | Error ($|C_{BS} - C_{market}|$) |
| :---: | :---: | :---: | :---: |
| **1** | 30.0000% | 111.2711원 | 38.7289 |
| **2** | 36.5638% | 150.5458원 | 0.5458 |
| **3** | **36.4737%** | **150.0001원** | **0.0001 (수렴 완료)** |

* **결과**: 단 3회 반복 만에 허용 오차($10^{-4}$) 이내로 수렴하여 **Implied Volatility = `36.47%`** 도출.

---

## 실행 방법 (Usage)

```bash
# Repository Clone
git clone [https://github.com/MinseokChoi2002/Financial-Mathematics-Lab.git](https://github.com/MinseokChoi2002/Financial-Mathematics-Lab.git)
cd Financial-Mathematics-Lab

# 1. Black-Scholes & Greeks 모듈 실행
python black_scholes.py

# 2. Implied Volatility Solver 실행
python implied_volatility.py
