---
type: ml-note
area: data
priority: P1
status: planned
updated: 2026-08-06
tags:
  - ml-engineering
  - study
---

# SQL과 학습 데이터셋

학습용 query는 row의 grain과 시점 조건을 보존해야 재실행할 수 있습니다.

## 핵심

- 한 row가 sample, user, event 중 무엇인지 먼저 정합니다.
- join cardinality를 검사해 중복 증폭을 막습니다.
- 예측 시점 이후의 정보가 들어오지 않도록 time-aware join을 사용합니다.

## 연습

- [ ] CTE로 label과 feature 시점을 분리한 dataset query를 작성합니다.

## 연결

- [[데이터 버전 관리와 Lineage]]
- [[Python 코딩과 SQL 면접]]