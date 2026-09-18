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

# Baseline과 실험 설계

새 모델의 가치는 단순 규칙과 기존 모델을 같은 조건에서 이길 때 설명할 수 있습니다.

## 핵심

- dummy, simple heuristic, linear model을 비교 기준으로 둡니다.
- 한 실험에서는 한 가설과 한 변경을 추적합니다.
- seed, split, data, code와 config version을 기록합니다.

## 연습

- [ ] 프로젝트에 dummy와 단순 모델 baseline 두 개를 추가합니다.

## 연결

- [[문제 정의와 성공 지표]]
- [[실험 추적과 모델 패키징]]