---
type: ml-note-index
status: active
updated: 2026-08-06
---

# ML Engineering

ML 프로젝트를 완성하기 위해 필요한 구현 기준을 정리합니다. 도구 목록보다
데이터가 들어와 예측이 나가고, 다시 관측되는 전체 경로를 우선합니다.

![[ml-engineering.base#ML Engineering 노트]]

## 구현 기준

| 축 | 구현 질문 | 노트 |
| --- | --- | --- |
| Scale | 입력 크기와 feature 수가 늘어날 때 어디가 병목인가 | [[데이터와 학습 파이프라인]] |
| Reliability | schema, split, artifact가 서로 맞는지 어떻게 확인하는가 | [[평가와 신뢰성]] |
| Reproducibility | 어떤 데이터·코드·설정이 이 model을 만들었는가 | [[실험 추적과 모델 패키징]] |
| Production Readiness | 긴 job과 짧은 prediction을 어떻게 나누고 관측하는가 | [[서빙과 운영]] |

## 구현 순서

1. manifest와 feature schema를 정의한다.
2. 작은 fixture로 end-to-end pipeline을 먼저 통과시킨다.
3. leakage-safe baseline과 cohort hold-out을 실행한다.
4. run metadata를 기록하고 preprocessing과 model을 versioned bundle로 만든다.
5. profile API와 raw-data async job을 분리한다.
6. latency, 실패율, schema mismatch, drift를 기록한다.

## 작성 규칙

- 한 노트는 lifecycle의 한 경계만 설명한다.
- 도구 사용법보다 입력, 출력, 실패 조건과 검증 방법을 먼저 쓴다.
- `planned`, `in-progress`, `completed`는 문서 분량이 아니라 재현 가능한 증거로 구분한다.
- 도메인 지식은 중복하지 않고 [[docs/domain/bioinformatics/index|Bioinformatics]]와 관련 논문으로 연결한다.

## 현재 증거

| 생명주기 | 프로젝트 | 상태 |
| --- | --- | --- |
| 원시 데이터 workflow | [[FunOMIC2 Nextflow Pipeline]] | 완료 |
| 모델과 애플리케이션 연결 | [[KT Aivle Big Project]] | 완료 |

## 기준 자료

- [Google Cloud — MLOps: Continuous delivery and automation pipelines](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning?hl=en)
- [Google for Developers — ML pipelines](https://developers.google.com/machine-learning/managing-ml-projects/pipelines)
- [AWS — ML Solution Monitoring, Maintenance, and Security](https://docs.aws.amazon.com/aws-certification/latest/machine-learning-engineer-associate-01/machine-learning-engineer-associate-01-domain4.html)
- [Hyperconnect — Machine Learning Software Engineer](https://career.hyperconnect.com/job/a8d9b01f-f11c-44f3-8e8b-a4c91e1331c8/)
