---
type: ml-note
area: ml-systems
priority: P0
status: planned
updated: 2026-08-06
tags:
  - ml-engineering
  - study
---

# ML 테스트 전략

ML test는 함수 결과뿐 아니라 데이터 계약, artifact 호환성과 대표 prediction을 확인합니다.

## 핵심

- 작은 fixture로 feature 변환과 schema를 unit test합니다.
- train부터 package까지 smoke test를 둡니다.
- 저장한 bundle과 API가 같은 prediction을 내는지 contract test합니다.

## 연습

- [ ] 결측 column과 순서가 바뀐 column에 실패하는 test를 추가합니다.

## 연결

- [[Python 패키징과 CLI]]
- [[평가와 신뢰성]]