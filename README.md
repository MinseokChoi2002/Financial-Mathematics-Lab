# 📈 Financial Mathematics Lab

> **Option Pricing Simulator for European & Exotic Options using Monte Carlo Simulation and Black-Scholes PDE in Python.**

본 저장소는 금융수학(Financial Mathematics) 이론을 바탕으로 옵션 가격 결정 모델(Option Pricing Models)을 Python으로 직접 구현하고 검증하는 공간입니다.

---

## 1. 주요 구현 기능 (Key Features)
* **Black-Scholes Closed-Form Model**: 유러피안 옵션의 해석적 해(Analytical Solution) 구하기
* **Monte Carlo Simulation**: 확률과정론(Geometric Brownian Motion) 기반의 옵션 가격 산정
* **Greeks Calculation**: Delta, Gamma, Vega 등 리스크 지표 산출

## 2. 수학적 배경 (Mathematical Background)
* **Geometric Brownian Motion (GBM)**:
  $$dS_t = \mu S_t dt + \sigma S_t dW_t$$

* **Black-Scholes PDE**:
  $$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + r S \frac{\partial V}{\partial S} - r V = 0$$

## 3. 파일 구조 (Repository Structure)
* `black_scholes.py` : Black-Scholes 공식 및 Greeks 구현 모듈
* `monte_carlo.py` : 몬테카를로 시뮬레이션 기반 프라이싱 모듈
* `main.py` : 실행 및 수렴도 비교 테스트 코드

---
✉️ **Contact**: Choi Min-Seok (가톨릭대학교 수학과 / 컴퓨터정보공학부)
