---
type: ml-note
area: ml-systems
priority: P1
status: planned
updated: 2026-08-06
tags:
  - ml-engineering
  - study
---

# ML 시스템 설계와 용량 계획

system design은 model보다 데이터 흐름, SLO, 병목과 실패 복구를 설명하는 문제입니다.

## 핵심

- 요청량, payload, latency와 freshness 요구를 수치로 둡니다.
- online path와 offline training path의 storage와 compute를 나눕니다.
- peak load, queue, retry와 backpressure를 포함해 용량을 계산합니다.

## 연습

- [ ] 예상 QPS와 model latency로 필요한 동시 처리량을 계산합니다.

## 연결

- [[모델 서빙 패턴]]
- [[ML 시스템 디자인 면접]]