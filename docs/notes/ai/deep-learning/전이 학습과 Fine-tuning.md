---
type: ml-note
area: deep-learning
priority: P1
status: planned
updated: 2026-08-06
tags:
  - ml-engineering
  - study
---

# 전이 학습과 Fine-tuning

사전학습 모델은 데이터 크기, latency와 배포 조건에 맞춰 feature extractor 또는 fine-tuning 방식으로 사용합니다.

## 핵심

- 먼저 frozen baseline을 만들고 full tuning 필요성을 확인합니다.
- 학습 데이터와 사전학습 데이터의 domain 차이를 기록합니다.
- parameter-efficient tuning도 base model과 adapter version을 함께 관리합니다.

## 연습

- [ ] frozen baseline과 일부 layer fine-tuning을 같은 split에서 비교합니다.

## 연결

- [[Transformer와 Attention]]
- [[평가와 신뢰성]]