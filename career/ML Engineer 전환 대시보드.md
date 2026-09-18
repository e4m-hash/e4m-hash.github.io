---
type: dashboard
updated: 2026-08-05
---

# ML Engineer 전환 대시보드

공개 사이트에는 확인된 결과만 적고, 진행 중인 작업과 부족한 증거는 이곳에서 관리합니다.

![[ML Engineer Transition.base]]

## 문서 구조

- `career/`: 목표 직무, 역량 gap, 연구·실행 계획
- `docs/notes/ai/machine-learning/engineering/`: 재사용 가능한 ML Engineering 기술 문서
- `docs/projects/`: 구현 결과와 확인 가능한 증거
- `docs/domain/`: Bioinformatics 지식과 데이터 제약

같은 내용을 여러 폴더에 복사하지 않습니다. career 문서는 목표와 완료 조건을 적고,
기술 설명은 [[docs/notes/ai/machine-learning/engineering/index|ML Engineering]], 결과는 project 문서로 연결합니다.

## 현재 기준

- 목표 직무: 국내 주니어 ML Engineer
- 우선 보충 역량: [[Stack|ML Engineer Skill Stack]]의 P0
- 현재 연구 계획: [[MycoTrust 상세 설계|MycoTrust]]
- 도메인 기반: [Bioinformatics](../docs/domain/bioinformatics/index.md) — `docs/domain/bioinformatics/`에서 분리 관리
- 공개 조건: code, demo, benchmark 중 실제로 확인한 항목만 project frontmatter에 추가

석사 논문의 모델 개발과 ML Engineering 전환 계획은 분리합니다. 논문에서 검증된
model과 pipeline이 생성된 뒤 서빙·모니터링·배포 범위를 별도 milestone으로 추가합니다.

## 상태 변경 규칙

- `planned`: 완료 조건과 산출물만 정의됨
- `in-progress`: 실행 가능한 작업물 또는 실험 기록이 생성됨
- `completed`: 문서에 적은 완료 조건을 재현 명령으로 확인함

## 기술 문서

- [[데이터와 학습 파이프라인]]
- [[평가와 신뢰성]]
- [[실험 추적과 모델 패키징]]
- [[서빙과 운영]]
