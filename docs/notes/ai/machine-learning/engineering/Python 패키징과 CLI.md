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

# Python 패키징과 CLI

notebook의 학습 코드를 import 가능한 package와 반복 실행 가능한 command로 옮깁니다.

## 핵심

- data loading, feature, train, evaluate 책임을 module로 나눕니다.
- config와 입력 경로를 CLI 인자로 받고 결과 경로를 명시합니다.
- dependency와 실행 command를 README와 artifact metadata에 남깁니다.

## 연습

- [ ] train과 predict command를 clean environment에서 한 번씩 실행합니다.

## 연결

- [[데이터와 학습 파이프라인]]
- [[ML 테스트 전략]]