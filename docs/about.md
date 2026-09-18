# 소개

안녕하세요. 백희선입니다.

BDLS Lab에서 metagenomics와 microbiome 데이터를 다루고 있습니다. 현재 목표는
분석을 수행하는 데서 끝나지 않고, 큰 원시 데이터가 들어와 검증된 예측과 운영 지표로
나가기까지의 전체 경로를 설계하고 구현하는 ML Engineer입니다.

## 작업 기준

### Scale

- FASTQ와 고차원·희소 feature 처리
- sample 단위 병렬 workflow와 resource 측정
- Parquet 기반 산출물과 재실행 가능한 pipeline

### Reliability

- manifest와 feature schema validation
- subject·cohort 단위 split과 fold 내부 preprocessing
- code, data, reference DB, model version 분리
- 작은 입력으로 전체 경로를 확인하는 smoke test

### Production Readiness

- preprocessing과 model을 하나의 artifact bundle로 관리
- 짧은 profile prediction과 긴 raw-data job의 API 경계 분리
- latency, 실패율, schema mismatch, drift 관측
- CI와 재현 명령으로 release 검증

## 현재 근거

| 경험 | 확인 가능한 내용 |
| --- | --- |
| [[FunOMIC2 Nextflow Pipeline]] | Nextflow DSL2, container, resume |
| [[KT Aivle Big Project]] | 데이터 수집, tabular ML, 웹 연동 |
| Bioinformatics 연구 | 원시 sequence와 reference DB 이해 |

## 기술

| 영역 | 사용 경험 |
| --- | --- |
| Language | Python, R, C++ |
| Data/ML | pandas, NumPy, SciPy, scikit-learn, XGBoost, CatBoost, PyTorch |
| Workflow | Nextflow, nf-core, Selenium |
| Runtime | Docker, Podman, Apptainer, Linux |
| Domain | metagenomics, microbiome statistics |

## 이력

| 기간 | 내용 |
| --- | --- |
| 2025 ~ 현재 | BDLS Lab — metagenomics·microbiome 분석 |
| 2024 ~ 2025 | KT Aivle — AI 개발 과정 및 팀 프로젝트 |
| 2022 ~ 2024 | 병역 의무 이행 |
| 2023 ~ 2024 | KLAS 서지정보 입력 자동화 프로젝트 |

## Contact

- GitHub: [@e4m-hash](https://github.com/e4m-hash)
- Email: `e4m98s@gmail.com`
