---
type: ml-note
area: evaluation
priority: P0
status: planned
updated: 2026-08-06
tags:
  - ml-engineering
  - study
---

# 불균형 데이터와 Calibration

class imbalance는 accuracy보다 positive class의 발견 비용과 확률 품질을 보게 합니다.

## 핵심

- class weight와 resampling은 train fold 안에서만 적용합니다.
- calibration curve와 Brier score로 확률의 신뢰도를 봅니다.
- threshold는 validation에서 정하고 test에서 고정합니다.

## 연습

- [ ] 원래 prevalence를 유지한 test에서 calibration과 PR curve를 그립니다.

## 연결

- [[분류와 회귀 평가지표]]
- [[데이터 분할과 누수]]