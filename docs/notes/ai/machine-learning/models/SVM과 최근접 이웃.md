---
type: ml-note
area: modeling
priority: P1
status: planned
updated: 2026-08-06
tags:
  - ml-engineering
  - study
---

# SVM과 최근접 이웃

SVM과 KNN은 feature scale과 거리 정의의 영향을 크게 받습니다.

## 핵심

- SVM의 margin과 kernel이 만드는 결정 경계를 설명합니다.
- KNN은 inference 비용과 차원의 저주를 확인합니다.
- 둘 다 scaling을 train pipeline 안에서 수행합니다.

## 연습

- [ ] 표준화 전후의 SVM과 KNN 성능·latency를 비교합니다.

## 연결

- [[전처리와 특성 공학]]
- [[편향 분산과 일반화]]