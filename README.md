# 🌍 K-Means 클러스터링 기반 에너지 & 기후 데이터 분석 웹 서비스
> **AI 기반 국가별 에너지 효율성 진단 및 맞춤형 정책 제안 플랫폼**

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=flat&logo=flask&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=flat&logo=bootstrap&logoColor=white)

## 📖 프로젝트 개요 (Overview)
전 세계적으로 기후 변화 대응과 에너지 효율화가 시급한 과제입니다. 본 프로젝트는 국가별 기후 지표(온도, CO2)와 에너지 데이터(소비량, 가격)를 **K-Means 머신러닝 알고리즘**으로 분석하여, 국가들을 성향별로 군집화하고 **맞춤형 개선 전략(Action Plan)**을 제안하는 웹 서비스입니다.

### 🎯 주요 목표
* 복잡한 기후/에너지 데이터를 **3D 시각화**로 직관적으로 표현
* 데이터 기반의 객관적인 **국가별 그룹핑 (Clustering)**
* 단순 분석을 넘어선 실질적인 **정책 및 행동 지침 제안**

---

## 📸 주요 기능 및 실행 화면 (Screenshots)

### 1. 메인 대시보드 (Dashboard)
사용자가 CSV 데이터를 업로드하고 K값(그룹 수)을 설정하면, 실시간으로 분석된 결과가 3D 그래프와 리포트로 출력됩니다.
![Main Dashboard](images/main_dashboard.png)

### 2. 고해상도 3D 클러스터링 시각화
서버 사이드에서 렌더링된 4K급 고해상도 그래프를 통해 에너지 효율, CO2 배출량, 재생에너지 비중을 3차원으로 확인합니다.
![3D Visualization](images/3d_visualization.png)

### 3. AI 분석 리포트 & 개선 전략 (Action Plan)
각 그룹의 특성을 요약한 리포트를 제공하며, 클릭 시 해당 그룹에 맞는 **구체적인 개선 전략(전구 아이콘 💡)**을 제안합니다.
![AI Report](images/ai_report.png)

### 4. 상세 데이터 지표
영문 국가명을 한글로 자동 변환하여 제공하며, 각 국가의 세부 데이터를 표 형태로 확인할 수 있습니다.
![Data Table](images/data_table.png)

---

## 🛠 시스템 아키텍처 & 기술 스택

### 🏗 Architecture
본 서비스는 **MVC 패턴**을 기반으로 한 3-Tier 아키텍처로 설계되었습니다.
* **Client:** 사용자 입력을 받고 결과를 시각화 (Fetch API 비동기 통신)
* **Server:** 데이터 처리 및 AI 모델링 수행 (RESTful API)
* **Engine:** 데이터 전처리, 정규화, 군집화 연산

### 💻 Tech Stack
| 구분 | 기술 (Technology) | 설명 |
| :--- | :--- | :--- |
| **Backend** | Python, Flask | 웹 서버 및 API 구축 |
| **Data Analysis** | Pandas, NumPy | 데이터 전처리 및 파생변수 생성 |
| **ML & AI** | Scikit-learn | K-Means 클러스터링 모델 학습 |
| **Visualization** | Matplotlib | 서버 사이드 3D 그래프 렌더링 |
| **Frontend** | HTML5, Bootstrap 5, JS | 반응형 웹 UI 구성 |

---

## 🧠 데이터 분석 로직 (Analysis Logic)

### 1. 데이터 전처리
* 결측치 제거 및 데이터 정제
* **파생 변수 생성:** 단순 소비량이 아닌 효율성을 판단하기 위해 `에너지 효율성` 지표 생성
  > $Efficiency = (Industrial Activity Index / Energy Consumption) * 1000$

### 2. K-Means 클러스터링
* `StandardScaler`를 통한 데이터 정규화 (Normalization)
* **중앙값(Median) 기준 4분면 분석:** 단순 평균이 아닌 중앙값을 기준으로 그룹의 성격을 '친환경', '위기', '개발', '산업'형으로 명확히 정의

### 3. 한글 폰트 자동화
* 리눅스/도커 환경에서 Matplotlib 한글 깨짐 방지를 위해, 실행 시 **나눔고딕 폰트를 자동으로 다운로드 및 로드**하는 로직 구현

---

## 🚀 설치 및 실행 방법 (Installation)

### 1. 레포지토리 클론
```bash
git clone [https://github.com/YOUR_USERNAME/PROJECT_NAME.git](https://github.com/YOUR_USERNAME/PROJECT_NAME.git)
cd PROJECT_NAME
