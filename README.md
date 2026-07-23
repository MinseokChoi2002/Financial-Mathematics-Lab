# 📈 Financial Mathematics Lab

> **Python-based Quantitative Finance & Numerical Methods Engine**
> 
> 본 저장소는 금융수학(Financial Mathematics) 이론과 수치해석 기법을 바탕으로 옵션 가격 결정 모델(Option Pricing Models) 및 리스크 지표를 Python으로 직접 구현하고 검증하는 연구 공간입니다.

---

## 1. 주요 구현 기능 (Key Features)

* **Implied Volatility Solver (`implied_volatility.py`)**
  * 옵션의 시장 가격($C_{market}$)으로부터 내재변동성($\sigma$)을 역산하는 **Newton-Raphson 수치해석 엔진**
  * $f'(\sigma)$ 미분값으로 옵션 리스크 지표인 **베가(Vega)** 활용
  * 허용 오차(`tolerance`) 기반 자동 수렴 조건 및 예외 처리 구사

---

## 2. 수학적 배경 (Mathematical Background)

### Newton-Raphson Method for Implied Volatility
블랙-숄즈 공식은 변동성 $\sigma$에 대한 역함수(Closed-form solution)가 존재하지 않으므로, 아래의 점화식을 통해 수치적으로 해를 구합니다.

$$\sigma_{n+1} = \sigma_n - \frac{C_{BS}(\sigma_n) - C_{market}}{\text{Vega}(\sigma_n)}$$

* **Black-Scholes Call Option Price**:
  $$C_{BS}(\sigma) = S \cdot N(d_1) - K e^{-rT} N(d_2)$$
* **Vega (Derivative with respect to $\sigma$)**:
  $$\text{Vega} = \frac{\partial C_{BS}}{\partial \sigma} = S \cdot N'(d_1) \sqrt{T}$$

---

## 3. 수치해석 검증 예제 (Case Study & Verification)

학부 과정 및 실제 옵션 시장 조건의 문제 데이터를 기반으로 수치해석 엔진의 정상 작동 및 수렴 속도를 검증했습니다.

### 검증 조건 (Test Inputs)
* 현재 주가 ($S$): **7,800원**
* 행사가격 ($K$): **8,000원**
* 무위험 이자율 ($r$): **연 3.0%**
* 잔존만기 ($T$): **15일** ($15 / 365$년)
* 시장 옵션가 ($C_{market}$): **150원**
* 초기 추정 변동성 ($\sigma_0$): **30.0%**
* 허용 오차 (`tol`): **$0.0001$ ($10^{-4}$)**

### 계산 결과 (Convergence Log)

| Iteration | Sigma ($\sigma$) | BS Call Price | Error ($|C_{BS} - C_{market}|$) |
| :---: | :---: | :---: | :---: |
| **1** | 30.0000% | 111.2711원 | 38.7289 |
| **2** | 36.5638% | 150.5458원 | 0.5458 |
| **3** | **36.4737%** | **150.0001원** | **0.0001 (수렴 완료)** |

* **최종 내재변동성(IV)**: **`36.47%`** (단 3회 반복 만에 오차 $10^{-4}$ 이하 수렴)

---

## 실행 방법 (Usage)

```bash
# 저장소 복제 및 실행
git clone [https://github.com/MinseokChoi2002/Financial-Mathematics-Lab.git](https://github.com/MinseokChoi2002/Financial-Mathematics-Lab.git)
cd Financial-Mathematics-Lab

# 내재변동성 솔버 실행
python implied_volatility.py
