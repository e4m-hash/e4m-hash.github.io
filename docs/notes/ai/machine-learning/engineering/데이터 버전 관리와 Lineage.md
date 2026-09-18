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

# 데이터 버전 관리와 Lineage

배포된 model에서 사용한 원본 데이터와 feature artifact까지 역으로 찾을 수 있어야 합니다.

## 핵심

- dataset URI, checksum, schema와 split manifest를 기록합니다.
- immutable raw data와 재생성 가능한 derived data를 구분합니다.
- run metadata에 code, config, data와 model version을 연결합니다.

## 연습

- [ ] 한 model artifact에서 학습 dataset checksum까지 추적하는 manifest를 만듭니다.

## 연결

- [[실험 추적과 모델 패키징]]
- [[SQL과 학습 데이터셋]]