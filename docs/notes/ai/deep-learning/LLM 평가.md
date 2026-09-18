---
type: ml-note
area: deep-learning
priority: P2
status: planned
updated: 2026-08-06
tags:
  - ml-engineering
  - study
---

# LLM 평가

LLM 평가는 정답 품질, 근거성, latency와 비용을 실제 task dataset에서 함께 봅니다.

## 핵심

- 대표 질문과 실패 사례를 versioned evaluation set으로 관리합니다.
- 자동 metric과 사람 평가 rubric의 역할을 구분합니다.
- RAG는 retrieval 품질과 generation 품질을 따로 측정합니다.

## 연습

- [ ] 질문 20개와 기대 근거를 담은 작은 RAG 평가셋을 만듭니다.

## 연결

- [[RAG]]
- [[VectorDB]]