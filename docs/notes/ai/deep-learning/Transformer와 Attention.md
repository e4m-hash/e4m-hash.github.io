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

# Transformer와 Attention

Transformer는 token 간 관계를 attention으로 계산하고 병렬적으로 표현을 갱신합니다.

## 핵심

- query, key, value의 shape과 attention score 흐름을 확인합니다.
- position 정보와 mask가 sequence 의미와 정보 접근 범위를 정합니다.
- context 길이는 memory와 latency 비용에 직접 연결됩니다.

## 연습

- [ ] 짧은 문장의 attention mask와 tensor shape을 손으로 적습니다.

## 연결

- [[신경망 기초]]
- [[전이 학습과 Fine-tuning]]