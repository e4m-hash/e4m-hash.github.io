---
type: skill-map
status: active
target_role: junior-ml-engineer
updated: 2026-08-06
---

# ML Engineer Skill Stack

도구를 아는지보다 작은 ML 시스템을 끝까지 구현하고 실패 원인을 설명할 수 있는지를
기준으로 관리한다. 현재 프로젝트 근거는 [[FunOMIC2 Nextflow Pipeline]]과
[[KT Aivle Big Project]], 연구 계획은 [[MycoTrust 상세 설계]]에 연결한다.

## 우선순위

| 우선순위 | 역량 | 현재 근거 | 다음 완료 조건 |
| --- | --- | --- | --- |
| P0 | Python 패키징·테스트 | 분석·pipeline 코드 | CLI로 학습을 재현하고 unit·smoke test를 CI에서 실행 |
| P0 | 데이터 계약·feature pipeline | Nextflow, container | manifest/schema 검증과 versioned feature artifact 생성 |
| P0 | 누수 없는 학습·평가 | tabular ML, 통계 | `Pipeline`과 group split으로 baseline·calibration·오류 분석 보고 |
| P0 | 실험·모델 lineage | 없음 | data/code/config/model version을 한 run에서 추적 |
| P1 | API·batch inference | 애플리케이션 연동 | 같은 model bundle로 batch와 API prediction contract test 통과 |
| P1 | Docker·CI/CD | Docker/Podman | image build, test, tag를 GitHub Actions에서 자동화 |
| P1 | 관측성 | 없음 | latency/error/schema mismatch/drift 지표와 장애 기록 제시 |
| P1 | SQL·object storage | 기초 | metadata query와 immutable artifact 경로를 함께 사용 |
| P2 | Cloud·Kubernetes | 기초 | 단일 서비스 배포 후 probe, resource limit, rollback 확인 |
| P2 | 분산 처리·GPU platform | 없음 | 데이터나 부하가 단일 노드 한계를 넘을 때만 추가 |

> [!important] 학습 순서
> P0 하나를 코드·테스트·측정 결과로 닫기 전에는 P2 도구를 늘리지 않는다.

## 최소 기술 기준

### Python과 ML

- notebook 밖에서 `train`, `evaluate`, `predict`를 실행한다.
- preprocessing과 estimator를 하나의 pipeline으로 묶는다.
- subject, cohort, time처럼 실제 일반화 단위를 split에 반영한다.
- AUROC 하나가 아니라 prevalence, AUPRC, calibration, subgroup 결과를 남긴다.
- model만 저장하지 않고 input schema, class mapping, dependency와 평가 결과를 묶는다.

### Data와 system

- sample manifest, schema, checksum, source/version을 입력 계약으로 둔다.
- pipeline 단계마다 재시작 가능한 명시적 artifact를 만든다.
- online prediction, batch inference, 긴 raw-data job의 경계를 구분한다.
- latency, throughput, error, resource, drift를 관측하고 비용과 실패 조건을 기록한다.

## 도구 선택

| 문제 | 기본 선택 | 추가 시점 |
| --- | --- | --- |
| tabular pipeline | scikit-learn `Pipeline` | custom training loop가 필요할 때 PyTorch |
| 실험 기록 | 파일 manifest + MLflow local tracking | 여러 사용자가 공유할 때 remote backend |
| API | FastAPI | CPU-bound 확장이 측정될 때 worker/queue |
| workflow | 기존 Nextflow | ML task orchestration 요구가 분리될 때 Airflow/Kubeflow |
| 배포 | Docker + GitHub Actions | 여러 replica와 rollout이 필요할 때 Kubernetes |
| 관측 | structured log + 기본 metric | 운영 부하가 생길 때 Prometheus/Grafana |

Kafka, Spark, Kubernetes, feature store는 채용 공고에 있다는 이유만으로 먼저 만들지
않는다. 현재 프로젝트의 데이터 크기, 처리량 또는 협업 방식이 필요성을 증명할 때 추가한다.

## 근거 자료

- [Hyperconnect — Senior Machine Learning Software Engineer (ML Platform)](https://career.hyperconnect.com/job/eedc3c02-640e-4770-b228-dc209c4548d5)
- [Google Cloud — MLOps: Continuous delivery and automation pipelines](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
- [AWS — ML Engineer Associate, monitoring·maintenance·security](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-01/machine-learning-engineer-associate-01-domain4.html)
- [scikit-learn — Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html)

