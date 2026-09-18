---
type: design
status: planned
track: thesis
related_principles: "[[Design]]"
updated: 2026-08-05
---
# MycoTrust
## ML 기반 Shotgun Metagenomics 진균 검출 신뢰도 평가

이 문서는 [[Design|석사 학위 논문 설계 원칙]]을 현재 연구 주제에 적용한 상세
설계다.
진균 분석 문제의 정의, mapping evidence 기반 feature와 재현 가능한 비교 평가를 목적으로 한다.

## 문제

shotgun metagenomics에서 진균은 세균보다 적은 read로 관측되고 reference database도
제한적이다. 현재 데이터에서는 다음 현상이 관찰되었다.

- EukDetect는 124개 샘플 중 42개에서만 진균을 검출했다.
- CGF catalog 기반 분석에서는 *Aspergillus*가 중앙값 52% 이상을 차지했다.
- 이는 같은 검체의 ITS 결과 및 알려진 장내 진균 분포와 일치하지 않는다.

이 결과만으로 *Aspergillus*를 오검출이라고 단정할 수는 없다. shared gene, 보존 서열,
human·bacterial background, multi-mapping, reference 구성 또는 abundance 계산 방식 중
어떤 요인이 결과를 만들었는지 먼저 확인해야 한다.

## 연구 질문

> CGF pipeline이 만든 genus-level fungal candidate에 대해 mapping evidence를 학습한
> Random Forest가 고정 threshold보다 false-positive call을 줄일 수 있는가?

### 가설

- H1: 근거가 약한 call은 낮은 coverage breadth, 적은 unique gene 수, 높은
  multi-mapping 비율과 불균일한 gene coverage를 보인다.
- H2: 여러 evidence를 함께 사용하는 Random Forest는 단일 read count, abundance 또는
  coverage threshold보다 높은 precision과 F1을 보인다.
- H3: ML로 필터링한 CGF profile은 원본 profile보다 paired ITS와 높은 genus-level
  일치도를 보인다.

### 기여

1. 실제 샘플에서 CGF fungal call이 왜 과대 보고되는지 read·gene 수준에서 분석한다.
2. fungal call의 신뢰도를 판정하는 ML 후처리 모델을 구현한다.
3. 공개 mock과 paired shotgun–ITS 데이터로 기존 규칙과 ML을 비교한다.
4. 논문 결과를 재현할 수 있는 pipeline과 repository를 제공한다.

## 3. 범위

### 포함

- CGF catalog 기반 candidate 생성
- genus-level presence/absence 판정
- mapping·coverage evidence 생성
- 고정 rule, Logistic Regression, Random Forest 비교
- in-silico 학습과 공개 mock 평가
- 동일 검체 124개의 shotgun–ITS 일치도 평가
- Nextflow workflow, Python package, Docker와 CI smoke test

### 제외

- Deep Learning
- 새로운 fungal reference database 구축
- 완전한 species-level 분류
- 절대 abundance 추정
- 임상 진단 성능 주장
- 웹 UI, API, queue, monitoring, Kubernetes

## 4. 데이터와 레이블

### 4.1 연구 단위

한 행은 하나의 `sample_id × genus_id` candidate call이다. 행 수를 독립 표본 수로
해석하지 않으며 split과 bootstrap은 source genome 또는 community 단위를 보존한다.

### 4.2 학습 데이터

공개 fungal genome과 bacterial·human background를 이용해 abundance와 sequencing
depth가 다른 in-silico community를 만든다.

- positive: community 조성에 포함된 genus
- negative: candidate로 검출됐지만 실제 조성에는 없는 genus
- unsupported: 평가 database에 존재하지 않아 원칙적으로 검출할 수 없는 genus

동일 source genome에서 생성된 read는 하나의 split에만 포함한다.

### 4.3 공개 test

[113개 eukaryotic species 기반 공개 mock](https://zenodo.org/records/12090449)을 최종
정량 평가에 사용한다. 이 데이터는 학습과 hyperparameter 선택에 사용하지 않는다.

### 4.4 실제 데이터

동일 검체 124개의 shotgun과 ITS 결과를 외부 일치도 평가에 사용한다. ITS 미검출을
확정적인 음성 레이블로 사용하지 않는다.

- genus presence agreement
- Jaccard similarity
- prevalence 변화
- 공통 검출 genus의 abundance rank correlation

## 5. Feature schema

### 식별자와 버전

- `sample_id`
- `genus_id`
- `genus_name`
- `pipeline_version`
- `database_version`
- `feature_schema_version`

### 모델 입력

- read와 fragment 수
- library size로 정규화한 read 비율
- CGF relative abundance
- unique gene에 정렬된 read 수
- 검출된 unique gene 수
- unique gene coverage breadth
- gene별 coverage evenness
- 평균 및 하위 분위 alignment identity
- unique mapping 비율
- multi-mapping 비율과 entropy
- 가장 가까운 경쟁 genus와의 alignment score 차이
- human·bacterial background 교차 정렬 비율
- 해당 genus의 reference genome·unique gene 수
- sequencing depth

모든 feature는 candidate call을 생성한 데이터만으로 계산한다. test label이나 ITS 결과를
feature 생성에 사용하지 않는다.

## 6. 모델

### 6.1 비교군

1. 원본 CGF 출력
2. read count threshold
3. relative abundance threshold
4. coverage breadth threshold
5. Logistic Regression

threshold 값은 validation set에서 선택한 뒤 고정한다.

### 6.2 주 모델

주 모델은 Random Forest binary classifier로 고정한다.

선택 이유:

- 독립 community 수가 크지 않은 tabular data에 적용하기 쉽다.
- feature scaling 없이 비선형 관계와 interaction을 학습한다.
- bagging으로 개별 tree의 분산을 줄인다.
- class weight와 제한된 hyperparameter만으로 실험을 통제할 수 있다.
- 모델 선택과 실패 원인을 석사 논문에서 설명하기 쉽다.

기본 설정은 `n_estimators=500`, `class_weight="balanced_subsample"`, 고정 seed를 사용한다.
`max_depth`, `min_samples_leaf`, `max_features`만 community-aware validation에서 작은 grid로
선택한다. test 결과를 본 뒤 parameter를 다시 조정하지 않는다.

### 6.3 Feature ablation

- Model A: read count와 abundance만 사용
- Model B: mapping·coverage evidence 전체 사용

Model B가 개선되지 않으면 복잡한 feature가 필요하지 않거나 현재 evidence가 실제 오류를
설명하지 못한다는 결론을 기록한다.

## 7. 판정과 출력

validation set에서 원본 CGF 대비 recall 감소를 5%p 이내로 제한하면서 FDR이 가장 낮은
decision threshold를 선택한다.

```text
sample_id
genus_id
genus_name
raw_abundance
score
decision: detected | rejected
reason_codes
model_version
database_version
feature_schema_version
```

`reason_codes`에는 낮은 coverage, 높은 multi-mapping, 낮은 identity, background 교차
정렬처럼 결과 해석에 필요한 근거를 기록한다.

## 8. 실험

### 실험 0. 가장 싼 반증

2주 안에 *Aspergillus* candidate read를 확인한다.

- genome 또는 unique gene 전체에 고르게 정렬되는가?
- 소수의 shared gene, rRNA 또는 repeat에 몰리는가?
- human·bacterial reference에 더 잘 정렬되는가?
- multi-mapping 재분배가 abundance를 키우는가?
- 단순 coverage 또는 competitive mapping filter로 제거되는가?

ML로 결합할 복수의 신호가 없고 단일 규칙으로 안정적으로 해결되면 연구 질문을
`조건별 최적 threshold 예측`으로 줄이거나 주제를 중단한다.

### 실험 1. Baseline

원본 CGF와 세 가지 threshold, Logistic Regression을 같은 validation에서 평가한다.

### 실험 2. Random Forest

Random Forest를 학습하고 baseline과 precision, FDR, recall, F1, AUPRC를 비교한다.

### 실험 3. Feature ablation

Model A와 Model B를 비교해 mapping evidence의 추가 가치를 확인한다.

### 실험 4. 조건별 성능

sequencing depth, fungal abundance, genus와 reference 지원 정도에 따라 성능을 나누어
본다.

### 실험 5. 공개 mock

고정한 모델과 threshold를 공개 test에 한 번 적용한다.

### 실험 6. Paired ITS

원본 CGF와 ML-filtered CGF의 genus-level ITS 일치도를 비교한다. 이 결과는 실제
데이터에서의 일관성을 보여주지만 절대적인 정확도로 해석하지 않는다.

## 9. 평가

### 주요 지표

- Precision
- False Discovery Rate
- Recall
- F1
- AUPRC

### 보조 지표

- genus-level Jaccard similarity
- prevalence agreement
- Spearman abundance correlation
- runtime과 peak memory

confidence interval은 community 또는 sample 단위 bootstrap으로 계산한다. 다수의 모델을
추가하거나 복잡한 다중검정을 필수화하지 않는다.

## 10. 성공과 실패

### 성공

Random Forest가 공개 mock에서 가장 좋은 고정 threshold보다 FDR 또는 F1을 개선하고,
paired ITS와의 genus-level 일치도를 악화시키지 않는다.

### 실패

Random Forest가 단순 rule을 이기지 못하면 fungal call의 신뢰도가 모델보다 database
coverage나 특정 mapping rule에 의해 결정된다는 결과를 보고한다. 성능을 만들기 위해
모델 수를 늘리지 않는다.

## 11. Repository

Repository 이름은 `mycotrust`로 한다.

### 실행 경계

- Nextflow: 입력 검증, CGF 실행, evidence 생성
- Python: schema 검증, 학습, 예측, 평가
- Docker: 실행 환경과 database version 고정
- GitHub Actions: 작은 synthetic fixture smoke test

### CLI

```text
mycotrust evidence
mycotrust train
mycotrust predict
mycotrust evaluate
```

model bundle에는 model, decision threshold, feature schema, taxonomy mapping, database
version, training config와 metric을 포함한다.

### 재현 기준

- `make smoke`: 작은 fixture의 end-to-end 실행
- `make benchmark`: 공개 mock 평가 재현
- 연구실 FASTQ는 공개하지 않고 비식별 파생값과 schema를 제공
- data card, model card, limitations와 실패 사례 포함

## 12. 일정

| 기간 | 작업 | 완료 조건 |
| --- | --- | --- |
| 1–2개월 | 원인 분석과 데이터 계약 | 반증 실험, label·split 정의 |
| 3–4개월 | simulation과 baseline | 공개 mock pipeline, rule 결과 |
| 5–6개월 | Feature와 Logistic Regression | versioned evidence matrix |
| 7–8개월 | Random Forest와 ablation | 고정 model과 threshold |
| 9–10개월 | 공개 mock·paired ITS 평가 | 최종 표와 그림 |
| 11–12개월 | 논문과 repository | 재현 가능한 release |
