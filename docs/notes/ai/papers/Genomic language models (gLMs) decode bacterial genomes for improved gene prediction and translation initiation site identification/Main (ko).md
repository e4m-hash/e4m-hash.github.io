---
title: "유전체 언어 모델(gLM)은 유전자 예측 및 번역 시작 부위 식별(PMC)을 개선하기 위해 박테리아 게놈을 해독합니다"
source: "https://pmc.ncbi.nlm.nih.gov/articles/PMC12222049/"
author:
  - "[[Genereux Akotenou]]"
  - "[[Achraf El Allali]]"
published:
created: 2026-05-26
description: "Accurate bacterial gene prediction is essential for understanding microbial functions and advancing biotechnology. Traditional methods based on sequence homology and statistical models often struggle with complex genetic variations and novel ..."
tags:
  - "clippings"
---
## 초록
정확한 박테리아 유전자 예측은 미생물 기능을 이해하고 생명공학을 발전시키는 데 필수적입니다. 서열 상동성과 통계 모델에 기반한 전통적인 방법들은 '유전자 언어' 해석 능력이 제한적이기 때문에 복잡한 유전적 변이와 새로운 서열에 어려움을 겪는 경우가 많습니다. 이러한 도전을 극복하기 위해, 우리는 자연어 처리의 대형 언어 모델에서 영감을 받은 유전체 언어 모델(gLM)을 탐구하여 박테리아 유전자 예측을 강화합니다. 이 모델들은 LLM이 인간 언어를 처리하는 방식과 유사하게 유전자 서열 내 패턴과 맥락적 의존성을 학습합니다. 우리는 특히 DNABERT를 사용하여 두 단계 프레임워크를 사용하여 박테리아 유전자 예측을 수행합니다: 먼저 코딩 서열(CDS) 영역을 식별하고, 그 다음에는 올바른 번역 시작 부위(TIS)를 식별하여 예측을 정제합니다. DNABERT는 선별된 NCBI 완전 박테리아 유전체 세트에서 k-mer 토큰라이저를 사용하여 서열 처리를 미세 조정합니다. 우리의 결과는 GeneLM이 유전자 예측 정확도를 크게 향상시킨다는 것을 보여줍니다. Prodigal, GeneMark-HMM, Glimmer 등 선도적인 원핵생물 유전자 탐색기와 비교할 때, GeneLM은 누락된 CDS 예측을 줄이고 일치하는 주석을 증가시킵니다. 더 주목할 만한 점은, 우리의 TIS 예측이 실험적으로 검증된 부위에서 기존 방법을 능가한다는 점입니다. GeneLM은 유전 정보 해독에서 gLM의 강력함을 입증하며, 박테리아 유전체 분석에서 최첨단 성능을 달성했습니다. 이러한 발전은 언어 모델이 유전체 주석을 혁신할 잠재력을 보여주며, 기존 도구를 능가하고 더 정밀한 유전적 통찰을 가능하게 합니다.

**키워드:** 유전자 예측, 번역 시작 부위, 대형 언어 모델, 유전체 언어 모델, BERT, 트랜스포머

## 소개

박테리아 유전자 예측은 계산 유전체학에서 오랫동안 집중되어 왔으며, 이 문제를 해결하기 위해 수많은 도구들이 개발되었습니다. 상당한 진전이 있었음에도 불구하고, 유전자 주석은 특히 코딩 서열(CDS)과 번역 시작 부위의 정확한 식별에서 계속 진화하는 문제로 남아 있습니다. Prodigal \[[^1]\], Glimmer \[[^2]\], GeneMark \[[^3]\]와 같은 전통적인 유전자 예측 기법은 박테리아 게놈 주석에 널리 사용되어 왔습니다. 이 도구들은 통계 모델, 휴리스틱 기반 규칙, 서열 상동성을 통해 유전자 구조를 추론하지만, 한계는 여전히 존재합니다. 게놈 주석의 주요 문제 중 하나는 구성과 조직의 변이성입니다. 예를 들어, 고GC 게놈은 잠재적 오픈 리딩 프레임(ORF)의 증가와 모호한 시작 코돈 선택으로 인해 예측 정확도가 저하되는 독특한 도전 과제를 안겨줍니다. 더불어, 번역 시작 부위의 주석은 여전히 어려운 과제인데, 시작 코돈 선택은 종마다 다양한 조절 메커니즘에 의해 영향을 받기 때문입니다. TiCO \[[^4]\]와 TriTISA \[[^5]\]와 같은 기존 도구들이 번역 시작 부위(TIS) 예측을 정교화하기 위해 개발되었지만, 이러한 접근법들은 실험적으로 검증된 데이터셋을 사용해 테스트할 때 여러 TIS 예측을 놓치고 있습니다. 또 다른 주요 과제는 유전자 예측에서 민감도와 특이성 간의 균형에 있습니다. 전통적인 방법은 종종 과도하게 예측하여 실험적 검증이 부족한 수많은 짧은 ORF를 자주 표시합니다. 더불어, 유전체 시퀀싱 분석 결과, 트랜스포존 시퀀싱 접근법을 통해 확인된 많은 필수 유전자들이 유전체 결실로 인한 위양성을 포함하고 있음을 보여주며\[[^6]\], 실제 유전자 주석을 희생하지 않으면서 정밀도를 높이는 방법의 필요성을 강조하고 있습니다.
 
인공지능과 머신러닝의 최근 발전은 방대한 유전체 데이터셋에서 의미 있는 특징을 추출할 수 있게 함으로써 서열 분석에 혁명을 일으켰습니다. 합성곱 신경망을 포함한 여러 딥러닝 기반 유전자 예측 모델이 제안되었습니다 \[[^7], [^8]\]. 자연어 처리에 성공적으로 적용된 자기 지도 학습은 순차적 패턴과 의존성을 이해하는 데 놀라운 능력을 보여주었습니다. 이러한 발전에 영감을 받아, 유전체 언어 모델(gLM)이 유망한 해결책으로 등장했으며, DNA 서열을 구조화된 언어 데이터로 다루어 유전자 주석을 향상시키고 있습니다 \[[^9]\]. 딥러닝 아키텍처를 활용해 이러한 모델은 전통적인 서열 정렬을 넘어 DNA 서열 내의 국소 및 전역 관계를 모두 포착할 수 있습니다. 이러한 아키텍처 중에서, 특히 양방향 인코더 표현(Transformers from Transformers)\[[^10]\]의 트랜스포머는 시퀀스 기반 작업에서 상당한 가능성을 보여주었습니다. 기존 유전자 예측 모델이 미리 정의된 특징 집합에 의존하는 것과 달리, BERT 기반 gLM은 자기 주의 메커니즘을 통해 서열 표현을 동적으로 학습합니다 \[[^11]\]. 이 능력 덕분에 박테리아 게놈 내 장거리 의존성을 모델링하여 유전자 구조를 더 정확하게 추론할 수 있습니다. 이러한 모델의 적용은 보다 적응적이고 정밀한 게놈 주석으로 나아가는 길을 제공합니다.

이러한 도전을 해결하기 위해, 우리는 박테리아 유전자 예측에 적합한 트랜스포머 기반 gLM을 도입합니다. 우리는 원핵생물 유전자 예측에서 서열 분류 작업을 수행하기 위해 BERT 기반 아키텍처를 사용합니다. 이 작업을 해결하기 위해 우리는 2단계의 분류 과정을 거칩니다. [보충 그림 S1](#sup1) 에서 볼 수 있듯이, 유전체가 주어지면 추출할 수 있는 많은 ORF가 존재합니다. 이 ORF 중 일부는 비코딩 영역을 포함하고, 다른 일부는 CDS에 해당합니다. 첫 번째 단계에서는 CDS를 분류합니다. 이 작업이 완료되면 두 번째 단계에서는 코딩 영역 내 TIS에 집중합니다. 구체적으로,

- 원핵생물 게놈에서 코딩 서열 영역을 식별하고 번역 시작 부위를 분류하기 위해 BERT 기반 gLM이 개발되었습니다.
- 이 모델은 처음에 인간 게놈 데이터셋에서 자가 지도 학습을 사용하여 DNA 조각 표현을 학습합니다. 그 후 유전자 주석 2단계 파이프라인을 통해 적응됩니다: 먼저 모델이 ORF를 CDS와 비CDS 영역으로 분류하고, 두 번째 모델이 진정한 TIS 부위를 식별하는 정교화 단계가 있습니다.
- 기존 유전자 예측 도구와 비교 평가를 수행하여 정밀도, 회상력, 확장성 향상을 평가합니다. 검증된 박테리아 게놈에 대한 사례 연구를 수행하여 실제 유전체 주석 작업에서 우리의 프레임워크가 적용 가능하고 견고함을 입증합니다.
- 모델의 의사결정 과정을 해석하기 위한 분석이 수행되며, 이는 유전체 연구의 필수적인 측면인 추론에 대한 통찰을 제공합니다.

## 재료 및 방법

### 자료 수집

견고하고 일반화된 모델을 개발하기 위해서는 포괄적이고 고품질의 데이터셋을 선별하는 것이 필수적입니다. 본 연구에서는 NCBI 아카이브에서 GenBank 데이터베이스를 통해 박테리아 유전체 데이터를 수집했습니다. 구체적으로, 어셈블리 요약 파일은 [ftp.ncbi.nih.gov/genomes/genbank/bacteria](https://ftp.ncbi.nih.gov/genomes/genbank/bacteria/assembly_summary.txt) FTP 사이트에서 다운로드되었습니다. 이 파일은 1GB 크기로, 주석, 조립 세부사항, 메타데이터 등 박테리아 유전체에 대한 광범위한 정보를 제공합니다. 데이터셋의 품질을 보장하기 위해 완전한 조립 상태의 게놈만 고려되었고, 필터링을 적용하여 "참조 게놈" 범주에 속한 것만 유지하였습니다. 이로 인해, 를 나타내는 데이터셋이 생성되었습니다. 필터링된 데이터셋 내 각 게놈에 대해 두 가지 필수 파일이 검색되었습니다: FASTA 형식의 완전한 뉴클레오타이드 서열을 포함하는 파일과 CDS 정보를 포함한 상세한 유전자 주석을 제공하는 파일입니다. GFF 파일은 유전체 특징을 구분하며, 하위 처리 및 모델 훈련에 필수적인 구조화된 주석 데이터를 제공합니다.5745 complete and annotated genomes 4823 unique organisms genome.fna annotation.gff

### 데이터 처리

번역 시작 지점과 CDS 분류 작업을 위한 고품질 데이터셋을 구축하기 위해 다단계 처리 파이프라인을 개발했습니다. 이 파이프라인은 박테리아 유전체에서 ORF를 추출하고, 유전체 주석을 기반으로 라벨을 할당하며, 견고한 모델 학습을 보장하기 위해 데이터셋을 균형 있게 조정합니다.

ORF를 추출하기 위해, 우리는 빠르고 유연한 Python 기반 ORF 추출 **도구를 사용하여 각** 게놈 서열의 순방향 및 역방향 가닥을 스캔하여 특정 시작 및 종료 코돈을 기반으로 잠재적 ORF를 식별했습니다. 시작 코돈 중 하나(,,, 또는 )로 시작해 종료 코돈(,,, 또는 )으로 끝나는 ORF를 필터링합니다. 중첩된 겹치는 ORF를 유지하여 포괄적인 유전체 커버리지를 제공하였습니다. 추출된 각 ORF는 해당 GFF 파일의 CDS 주석과 유전체 좌표를 비교하여 라벨을 부여받았습니다. 그 후 CDS용과 TIS 분류용 두 가지 유형의 데이터셋을 라벨링했습니다. CDS 데이터셋은 최대 길이 510개의 뉴클레오타이드 서열을 포함한 CSV 파일로 구성되며, 각 파일마다 양성()이나 음성으로 라벨이 붙습니다. 양성 라벨은 해당 서열이 GFF 참조 파일의 주석이 달린 CDS와 시작점 또는 종료 위치가 일치하는 가장 긴 절단된 ORF를 나타낸다는 것을 나타냅니다. 반면, TIS 데이터셋은 참조 파일의 CDS 서열과 일치하는 ORF의 서열만 포함하며, 서열에는 이진 레이블이 할당되어 진정한 TIS를 나타냅니다. 서열 맥락을 포착하기 위해, 각 TIS 중심 서열에는 상류와 하류에 각각 30개의 뉴클레오타이드가 포함되어 총 60개의 뉴클레오타이드 길이가 됩니다. 두 데이터셋의 전체 주석 처리 과정은 [보충 그림 S2](#sup1) 에 나와 있습니다.ATG TTG GTG CTG TAA TAG TGA

클래스 균형을 맞추고 모델 학습 중 잠재적 편향을 완화하기 위해 CDS와 TIS 데이터셋에 다양한 표본 추출 전략이 적용되었습니다. CDS 데이터셋의 경우, 음의 샘플은 양성 클래스의 분포에 맞게 서열 길이를 기준으로 다운샘플링되었습니다. 이 접근법은 분류의 난이도를 높이며, 모델이 CDS와 비CDS 영역을 구별하기 위해 서열 길이를 넘어 판별적 특징을 학습하도록 유도합니다. 반면, TIS 데이터셋에서는 모든 서열이 동일한 고정 길이를 가지므로, 추가 편향 없이 클래스 균형을 맞추기 위해 무작위 언더샘플링이 수행되었습니다. 데이터셋은 훈련, 테스트, 평가 세트로 나뉘었습니다. CDS 데이터셋의 클래스 균형 분산은 훈련, 테스트, 평가를 위한 시퀀스로 구성됩니다. 마찬가지로 TIS 데이터셋의 경우 분할은 학습, 테스트, 평가용 서열을 생성했습니다.14,975,672 2,181,188 4,253,562 14,544,028 2,199,192 4,136,340

### 토큰화 및 임베딩

훈련 중 DNA 서열을 효과적으로 처리하기 위해 DNABERT \[[^12]\] 프레임워크에서 사용하는 기법을 사용합니다. 이 방법에서는 DNA 서열을 길이 인 *k-mer* 로 겹치는 부분 서열로 나눕니다. 각 k-mer는 자연어 처리에서 단어처럼 개별 토큰 역할을 합니다. DNABERT 논문에 따르면,. 따라서 실험에서는 인코딩 방식을 사용합니다. 주어진 DNA 서열을 토큰 생성기는 이를 겹치는 6인(6) 토큰으로 나누어 CDS 분류 과제에서는 3 스트라이드로 설정하고, TIS 분류 시 기본 스트라이드 1을 사용합니다. 토큰화 후, 각 k-머는 사전 학습된 DNABERT 모델을 사용하여 수치 표현으로 변환됩니다. 각 k-머는 고정된 768차원 벡터에 매핑되며, 이는 BERT \[[^10]\] 아키텍처의 숨겨진 크기에 해당합니다. 또한, 각 시퀀스의 시작과 끝에 특별한 토큰을 포함하고 있습니다. 토큰은 전체 시퀀스에 대한 추가적인 맥락적 표현을 제공합니다. 따라서 CDS 분류 작업에서는 각 서열이 크기(512,768)의 행렬로 표현되는 반면, TIS 분류에서는 각 서열이 크기가 (62,768인 행렬로 표현됩니다. 이 전이 학습은 각 서열의 k-mer 표현이 의미 있고 맥락적으로 풍부한 정보를 포착할 수 있게 합니다. DNABERT 임베딩을 사용하여 토큰화된 서열이 후속 미세 조정을 위한 견고한 기반을 제공하도록 보장합니다.k-mer encoding \[CLS\] \[EOS\] \[CLS\]

### 모델

저희 모델은 DNABERT 프레임워크를 기반으로 하며, BERT를 유전체 서열까지 확장합니다. DNABERT는 사전 학습 및 미세 조정 패러다임을 따르며, 모델이 먼저 일반적인 DNA 서열 표현을 학습하고 이후 특정 후속 작업에 맞게 미세 조정됩니다. BERT와 동일한 트랜스포머 기반 아키텍처를 유지하고 있으며, 12개의 자기 주의 계층, 768개의 숨겨진 차원, 12개의 주의 헤드로 구성되어 있습니다[. 이는 그림 1에](#f1) 나타난 것입니다.

![유전체 서열 분류를 위한 트랜스포머 기반 BERT 모델 도식.](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/2a7d246608ef/bbaf311f1.jpg)

유전체 서열 분류에 사용되는 트랜스포머 기반 BERT 아키텍처의 일러스트.

k-머로 표현된 토큰화된 입력 서열이 주어졌을 때, 모델은 다중 헤드 자기 주의를 적용하여 서열 전반에 걸친 맥락적 관계를 학습합니다. 자기 주의 메커니즘은 공식적으로 다음과 같이 정의됩니다



$$
\begin{align}
\text{MultiHead(M)} = \text{ConCat}(\text{head}_1,\cdots,\text{head}_h)W^O
\end{align}
$$

여기서 각 주의 머리는 다음과 같이 계산된다.

$$
\begin{align}
\text{head}_i = \text{softmax}(\frac{MW^Q_i(MW^K_i)^T}{\sqrt{d_k}})MW^V_i
\end{align}
$$


여기서 $M$ 는 입력 토큰 임베딩을 나타내고,

Inline graphic

는 주의 헤드의 학습 가능한 쿼리, 키, 값 행렬입니다. 자기 주의 점수는 각 토큰이 시퀀스 내 다른 모든 토큰과 관련되어 있는 맥락적 관련성을 결정합니다. 트랜스포머 계층에서 나온 최종 숨겨진 표현은 시퀀스 수준 또는 토큰 수준 분류 작업에 사용됩니다.



### 미세 조정

주어진 시퀀스에 대해 토큰화된 입력 시퀀스에 분류 토큰을 앞에 붙인 후 DNABERT 기본 모델을 사용하여 그 임베딩 표현을 생성합니다. 자기 주의가 적용되며, 쿼리와 키 행렬 모두 시퀀스 자체에서 파생됩니다. [그림 2](#f2) 에서 볼 수 있듯이, 주의 메커니즘은 쿼리와 키 행렬 간의 점곱을 사용하여 주의 가중치를 계산합니다. softmax 함수가 이 가중치를 정규화하고, 결과에 값 행렬을 곱하여 원래 입력 임베딩을 조정합니다. 재가중치된 임베딩은 피드 포워드 계층을 거쳐 DNABERT 기본 아키텍처에 분류 헤드가 추가됩니다. 최종 분류 결정은 토큰의 임베딩에 기반하며, 이는 전역 시퀀스 특징을 집계합니다.\[CLS\] \[CLS\]

![자기 주의 메커니즘 도식.](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/2a80e2b93440/bbaf311f2.jpg)

쿼리, 키, 값 행렬에서 계산되고 softmax를 통해 정규화된 주의 점수가 k-mer 토큰에 동적 중요성을 부여하여 시퀀스 임베딩을 정제하는 방식을 보여주는 자기 주의 메커니즘.

우리의 미세 조정 접근법은 두 가지 핵심 분류 과제에 초점을 맞추고 있습니다: DNA 서열에서 코딩 서열 영역을 식별하는 것과 CDS 영역 내 번역 시작 부위 검출입니다. 미세 조정은 표준 BERT 기반 분류 절차를 따르며, 최종 숨겨진 토큰 표현이 시퀀스 수준 분류를 위해 완전 연결 계층을 통과합니다. 이를 가능하게 하기 위해 DNABERT는 다음과 같은 분류 헤드를 추가하여 확장합니다:\[CLS\]

- **풀러 계층**: 토큰 임베딩에서 정보를 집계하여 전체 시퀀스에 대해 고정 크기의 표현을 생성합니다.\[CLS\]
- **완전 연결 계층**: 풀된 표현을 출력 클래스에 매핑하는 하나 이상의 계층을 가진 피드 포워드 신경망입니다.
- **Softmax 레이어**: 출력 로그를 분류용 확률 점수로 변환합니다.

미세 조정의 목적 함수는 교차 엔트로피 손실이며, 다음과 같이 정의됩니다

| ![graphic file with name DmEquation3.gif](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/29b36b48de4e/DmEquation3.gif) | (3) |
| --- | --- |

여기서 는 근전 진실 레이블을 나타내며, 각 클래스에 대한 예측된 확률을 나타냅니다. 두 실험 모두 에서 입니다.

### 실험 설정

입력 토큰화와 임베딩 생성부터 최종 분류에 이르기까지 전체 워크플로우는 파이프라인 다이어그램([그림 3)](#f3) 에 요약되어 있습니다. 이 다이어그램은 DNABERT 모델, 트랜스포머 층, 분류 헤드를 포함한 모든 핵심 구성 요소를 개략적으로 설명합니다. 대규모 데이터셋을 고려할 때, PyTorch의 데이터 유틸리티를 활용해 반복 가능한 데이터셋을 구현하여 데이터 로딩과 배치 처리를 효율적으로 처리합니다. 모델은 선형 워밍업 전략을 사용하는 AdamW 옵티마이저를 사용하여 학습합니다. 학습 속도는 훈련 단계에서 초기화 되어 점차 0으로 감소합니다. 이 모델은 NVIDIA GPU 파티션에서 미세 조정을 거칩니다. 견고한 평가를 보장하기 위해 데이터셋을 훈련 및 검사 하위 집합으로 나누며, 테스트 세트에는 훈련 세트에 없는 생물만 포함합니다. 이 실험 설계는 모델의 성능을 이전에 본 적 없는 분류군에 대해 평가하여 일반화 능력을 효과적으로 평가하도록 보장합니다.

![TIS 및 CDS 파이프라인 미세 조정.](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/636f835293a7/bbaf311f3.jpg)

TIS 및 CDS 미세 조정 파이프라인은 박테리아 게놈에서 ORFs를 추출하고, k-mer 토큰화를 사용하며, 트랜스포머 기반 학습을 통한 유전체 영역 분류를 구현하며, 자기 주의는 장거리 의존성을 포착하여 예측 정확도를 높입니다.

1. **CDS 분류**
	이 작업의 목적은 유전체 데이터에서 CDS를 분류하는 것입니다. CDS 분류 실험은 [투브칼 슈퍼컴퓨터에서](https://cc.um6p.ma/toubkal-super-computer) 수행되었습니다. 훈련은 각각 80GB 메모리를 탑재한 두 대의 NVIDIA A100 GPU에서 수행되었습니다. 분산 학습은 두 GPU에 걸쳐 512개의 배치 크기로 구현되었으며, 두 에포크에 걸쳐 총 훈련 시간은 37시간이었습니다.
2. **TIS 분류**
	번역 시작 부위 분류를 위한 목표는 잠재적 번역 시작 부위를 중심으로 한 60-bp 서열을 분류하는 것입니다. 이 실험은 [컴퓨팅 대학 생물정보학 연구실](https://bioinformatics.um6p.ma/) 에서 24GB 메모리를 갖춘 단일 NVIDIA RTX A5000 GPU를 사용하여 수행되었습니다. 모델은 768개의 배치 크기로 학습되었으며, 3 에포크에 걸쳐 19시간 만에 훈련이 완료되었습니다.

### 평가 지표

우리는 표준 분류 지표 세트를 사용하여 개별 이진 분류기와 최종 분류기(스택 또는 최대 투표 방식)의 성능을 평가했습니다. 이 지표들은 모델이 단백질 전사인자 계열을 올바르게 분류하는 능력을 포괄적으로 보여줍니다. 다음과 같은 지표들이 계산되었습니다:

| ![graphic file with name DmEquation4.gif](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/c74e2219f70f/DmEquation4.gif) | (4) |
| --- | --- |

| ![graphic file with name DmEquation5.gif](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/5c745c7ff974/DmEquation5.gif) | (5) |
| --- | --- |

| ![graphic file with name DmEquation6.gif](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/b0d6c7692ffc/DmEquation6.gif) | (6) |
| --- | --- |

| ![graphic file with name DmEquation7.gif](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/a20d9e78527c/DmEquation7.gif) | (7) |
| --- | --- |

### 후처리

TIS 예측 후, 각 예측된 코딩 영역에 대해 가장 가능성 높은 번역 시작 부위를 선택하는 후처리 단계를 적용했습니다. 특정 ORF 그룹 내 모든 후보 TIS 직책 중에서, 가장 높은 예측 확률을 가진 사이트가 유지되었습니다. 이 결정은 이진 플래그(prediction\_max\_likelihood = 1)를 사용하여 기록되었으며, 각 지역별로 최적의 위치를 표시했습니다. 최종 주석 결과는 CSV 및 GFF 파일을 포함한 표준 출력으로 형식화되어 일반적인 유전체 주석 도구와의 호환성을 확인하고 후속 분석 또는 시각화를 위해 데이터를 준비했습니다.

## 결과

이 섹션에서는 실험에서 얻은 결과를 세 가지 주요 평가 단계로 구성하여 제시합니다. 먼저, 우리는 표준 평가 지표를 사용하여 모델 훈련과 테스트 중 성능을 보고하고, 그 효과를 평가합니다. 다음으로, 실험적으로 검증된 서열을 대상으로 모델을 실제 환경에서 평가하며, 실험실에서 검증된 생물학적 데이터에 대한 예측 정확도를 실질적으로 평가합니다. 마지막으로, 저희 접근법을 최신 유전자 주석 도구와 비교하여 정확성과 효율성을 벤치마크합니다. 이 평가들은 모델의 기능과 게놈 주석에서의 실용적 응용 가능성에 대한 포괄적인 이해를 제공합니다.

### 훈련 공연

이 섹션에서는 다양한 실험에서 모델을 훈련시켜 얻은 결과를 제시합니다.

1. **CDS 분류**
	[그림 4](#f4) 는 여러 단계에 걸친 훈련 손실 진행과 두 개의 미세 조정 시기에 걸친 평가 지표 비교를 보여줍니다. 초기에는 모델이 학습함에 따라 훈련 손실이 급격히 감소하여 수천 번의 반복 후 안정화됩니다. 그러나 어려운 예제를 가진 미니 배치 구성으로 인해 훈련 손실이 산발적으로 급증하는 현상이 관찰되었습니다. 이를 조사하기 위해 우리는 다양한 무작위 시드로 훈련을 반복하고 손실 역학을 분석하여 재현성 연구를 수행했습니다. [보충 섹션 S3과 S4](#sup1) 에 자세히 설명된 바와 같이, 모델은 시드 간 일관된 수렴 패턴을 보여주었습니다. 우리는 급증 수를 정량화하고 손실 분포 통계를 계산했으며, 이러한 변동이 불안정성을 나타내는 것이 아니라 훈련의 미세한 확률적 변동임을 확인했습니다. 이러한 변동에도 불구하고, 전반적인 추세는 손실이 일관되게 감소하고 있어 효과적인 학습을 뒷받침합니다. 두 번째 미세 조정 시기 이후에는 평가 지표에서 미미한 개선이 나타났습니다([표 1).](#TB1)
	추가 훈련이 수확 체감이나 과적합 위험을 초래할 수 있음을 시사하는 성능 향상과 추가 훈련의 계산 비용이 결합되어 2년 에포크에서 미세 조정을 중단했습니다. [표 1은](#TB1) 훈련 시기와 최종 테스트 세트 모두의 평가 지표를 보여줍니다. 모델은 정밀도, 호출율, 정확도 98%를 초과하는 높은 분류 성능을 달성했습니다. 평가 손실이 약간 감소한 것은 시기 간 안정적이고 효과적인 학습을 시사합니다. 최종 모델은 독립적인 테스트 세트에서 평가되었으며, 높은 정확도(99.43%)를 유지하면서 평가 손실은 0.0211이었습니다. 이 결과는 모델의 견고성과 일반화 능력을 확인시켜 줍니다.
2. **TIS 분류**
	[그림 5](#f5) 는 TIS 분류 실험의 훈련 손실 추세와 평가 지표를 보여줍니다. CDS 분류와 유사하게, 훈련 손실은 초기 급격한 감소를 보이지만 안정화되기 전에는 미세한 진동이 나타납니다. [표 2](#TB2) 의 평가 지표는 시기별로 일관된 성능 향상을 보여주며, 정밀도, 호출율, F1 점수가 각 반복마다 소폭 증가합니다. 그러나 그림에서 볼 수 있듯이, 이 지표들은 세 번째 에포크 이후에는 정체되어 추가적인 의미 있는 향상이 없어 과적합을 피하기 위해 에포크 3에서 조기 중단되었습니다. 최종 시험 평가에서 정확도(94.13%)와 평가 손실(0.1546)이 확인되었습니다.
	정확도 계산에 사용되는 TIS 주석은 NCBI에서 얻어졌으며, NCBI는 유전자 예측 도구를 사용해 항상 실제 정보를 반영하지 않을 수 있기 때문에, 우리는 박테리아 게놈에 대해 모든 실험적으로 검증된 TIS 데이터를 사용한 기존 방법과 도구를 벤치마킹했습니다.
![훈련 손실과 평가를 비교한 선도.](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/5e00066b1e85/bbaf311f4.jpg)

CDS 분류 실험을 위한 훈련 및 평가 지표 비교. 손실 변동에 대한 추가 분석은 보충 섹션 S3 에 제공된다.

#### 표 1.

CDS 분류를 위한 평가 및 테스트 세트 성능 지표

<table><colgroup><col align="left"> <col align="left"> <col align="left"> <col align="left"></colgroup><thead><tr><td rowspan="1" colspan="1"></td><th colspan="2" align="left" rowspan="1">평가 집합</th><th rowspan="1" colspan="1">테스트 세트</th></tr><tr><th rowspan="1" colspan="1">미터법</th><th rowspan="1" colspan="1">에포크 1</th><th rowspan="1" colspan="1">에포크 2</th><th rowspan="1" colspan="1">최종 점수</th></tr></thead><tbody><tr><td rowspan="1" colspan="1">손실</td><td rowspan="1" colspan="1">0.021233</td><td rowspan="1" colspan="1">0.020184</td><td rowspan="1" colspan="1">0.021132</td></tr><tr><td rowspan="1" colspan="1">정밀도</td><td rowspan="1" colspan="1">0.981846</td><td rowspan="1" colspan="1">0.983868</td><td rowspan="1" colspan="1">0.983253</td></tr><tr><td rowspan="1" colspan="1">F1</td><td rowspan="1" colspan="1">0.984364</td><td rowspan="1" colspan="1">0.985109</td><td rowspan="1" colspan="1">0.984544</td></tr><tr><td rowspan="1" colspan="1">정확성</td><td rowspan="1" colspan="1">0.994265</td><td rowspan="1" colspan="1">0.994553</td><td rowspan="1" colspan="1">0.994364</td></tr><tr><td rowspan="1" colspan="1">리콜</td><td rowspan="1" colspan="1">0.986916</td><td rowspan="1" colspan="1">0.986357</td><td rowspan="1" colspan="1">0.985844</td></tr></tbody></table>

[새 탭에서 열기](https://pmc.ncbi.nlm.nih.gov/articles/PMC12222049/table/TB1/)

참고: 표는 훈련 시기와 최종 테스트 세트 모두에 대한 평가 지표를 제시합니다. 이 모델은 정확도, 회상율, 정확도가 98%를 초과하는 분류 성능을 달성했습니다. 테스트 세트 평가는 손실이 최소화되고 정밀도가 높으며 모델의 일반화 능력을 확인합니다.

![훈련 손실과 평가 지표를 보여주는 선도.](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/8f0b669db237/bbaf311f5.jpg)

TIS 분류 실험을 위한 훈련 및 평가 지표 비교.

#### 표 2.

TIS 분류를 위한 평가 및 테스트 세트 성능 지표

<table><colgroup><col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"></colgroup><thead><tr><td rowspan="1" colspan="1"></td><th colspan="3" rowspan="1">평가 집합</th><th rowspan="1" colspan="1">테스트 세트</th></tr><tr><th rowspan="1" colspan="1">미터법</th><th rowspan="1" colspan="1">에포크 1</th><th rowspan="1" colspan="1">에포크 2</th><th rowspan="1" colspan="1">에포크 3</th><th rowspan="1" colspan="1">최종 점수</th></tr></thead><tbody><tr><td rowspan="1" colspan="1">손실</td><td rowspan="1" colspan="1">0.161598</td><td rowspan="1" colspan="1">0.158706</td><td rowspan="1" colspan="1">0.156721</td><td rowspan="1" colspan="1">0.154614</td></tr><tr><td rowspan="1" colspan="1">정밀도</td><td rowspan="1" colspan="1">0.938289</td><td rowspan="1" colspan="1">0.939115</td><td rowspan="1" colspan="1">0.939882</td><td rowspan="1" colspan="1">0.941508</td></tr><tr><td rowspan="1" colspan="1">F1 점수</td><td rowspan="1" colspan="1">0.937736</td><td rowspan="1" colspan="1">0.938943</td><td rowspan="1" colspan="1">0.939723</td><td rowspan="1" colspan="1">0.941359</td></tr><tr><td rowspan="1" colspan="1">정확성</td><td rowspan="1" colspan="1">0.937755</td><td rowspan="1" colspan="1">0.938949</td><td rowspan="1" colspan="1">0.939728</td><td rowspan="1" colspan="1">0.941364</td></tr><tr><td rowspan="1" colspan="1">리콜</td><td rowspan="1" colspan="1">0.937754</td><td rowspan="1" colspan="1">0.938948</td><td rowspan="1" colspan="1">0.939728</td><td rowspan="1" colspan="1">0.941363</td></tr></tbody></table>

[새 탭에서 열기](https://pmc.ncbi.nlm.nih.gov/articles/PMC12222049/table/TB2/)

참고: 표는 훈련 시기와 최종 테스트 세트 모두에 대한 평가 지표를 제시합니다. 이 모델은 93%를 넘는 정밀도, 회상 및 정확도로 분류 성능을 달성했습니다. 테스트 세트 평가는 일반화 능력을 최종 정확도 94.13%로 확인했습니다.

### CDS 분류에서 길이 편향과 과적합 평가

CDS 분류기의 견고성을 보장하고 ORF 길이와 같은 단순 특성에 대한 과적합 위험을 줄이기 위해, 우리는 훈련 중에 길이 인식 균형 전략을 도입했습니다. CDS 데이터셋에서는 음의 예시를 ORF 길이를 기준으로 양성(진짜 CDS) 예시의 길이 분포에 맞게 다운샘플링되었습니다. 이 접근법은 모델이 길이에 의존하는 것을 막고 판별적 서열 특징 학습을 촉진하기 위해 설계되었습니다. 모델이 얼마나 잘 일반화되는지, 그리고 예측 정확도가 ORF 길이에 따라 변하는지 평가하기 위해 길이 층화 추론 분석을 수행했습니다. 우리는 벤치마킹 데이터셋에서 검증된 CDS 주석을 가진 5개의 검증된 유전체를 사용했습니다. 모든 후보 ORF를 추출하고, 학습된 모델을 사용해 그 부호화 상태를 예측했으며, 실제 주석과 예측을 비교했습니다. ORF는 길이별로 네 개의 빈으로 그룹화되었으며, 짧은 길이(<300 bp)부터 매우 긴 길이(2000 bp)까지 다양했습니다. 각 빈에 대해 정밀도, 호출률, 정확도를 계산했고, 각 길이 범주에 속하는 ORF의 수도 세었습니다.

[그림 6](#f6) 에서 보듯, 분류기는 모든 ORF 길이에서 일관되게 높은 성능을 달성합니다. 하지만 특히 300 bp 미만의 짧은 ORF는 여전히 테스트 데이터에서 과소대표되어 있어 성능 지표에 대한 신뢰도가 제한될 수 있음을 관찰합니다. 이러한 한계에도 불구하고, 전체 결과는 모델이 분류에 있어 주로 ORF 길이에 의존하지 않는다는 강력한 증거를 제공합니다. 이는 훈련 중 사용되는 길이 균형 절차의 중요성과 효과를 확인시켜 주며, 길이 관련 편향을 완화하고 학습된 서열 표현의 생물학적 관련성을 높인다.

![ORF 길이 빈별 CDS 분류기 성능(왼쪽)과 해당 ORF 카운트 분포(오른쪽)를 보여주는 막대 차트.](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/2fb5b3229177/bbaf311f6.jpg)

왼쪽: 다섯 개의 검증된 유전체를 사용한 ORF 길이 빈 전반에 걸친 CDS 분류기 성능 지표(정밀도, 호출율, 정확성). 오른쪽: 길이별 ORF 분포.

### 실험적으로 검증된 유전체에 대한 성능 벤치마킹

GeneLM의 효과는 실험적으로 검증된 CDS를 사용하여 벤치마킹되었습니다. 실제 생물학적 데이터를 이용한 벤치마킹은 이전 연구들에서 확인된 것처럼 유전자 예측 방법 평가의 표준 관행입니다 \[[^1], [^5], [^13]\]. 이를 바탕으로, 우리는 GeneLM을 널리 사용되는 세 가지 원핵생물 유전자 예측 도구인 Prodigal \[[^1], GeneMark-HMM \[[^14]\], Glimmer3 \[[^15]\], 그리고 최근 딥러닝 기반 번역 시작 지점 예측기인 TITER \[[^16]\], DeepGSR \[[^17]\], DeepTIS \[[^18]\]와 비교했습니다. 평가는 N-말단 펩타이드 시퀀싱을 기반으로 실험적으로 검증된 TIS를 가진 다섯 개의 세균 및 고세균 유전체— *Escherichia coli*, *Halobacterium salinarum*, *Natronomonas pharaonis*, *Mycobacterium tuberculosis*, *Roseobacter denitrificans* —를 대상으로 수행되었습니다. 이들 유기체([표 3](#TB3) 에 나열됨)는 2841개의 검증된 유전자 테스트 세트를 포함해 주석이 달린 TIS가 가장 많았습니다 \[[^13]\].

#### 표 3.

다섯 쿼리 종의 참조 클레이드와 이들의 검증된 유전자 테스트 세트 크기, 총 2,841개의 유전자와 N-말단 시퀀싱으로 확인된 시작 부위 \[[^13]\].

<table><colgroup><col align="left"> <col align="left"> <col align="left"> <col align="left"></colgroup><thead><tr><th rowspan="1" colspan="1">종</th><th rowspan="1" colspan="1"><strong>클레이드</strong></th><th rowspan="1" colspan="1"><strong>계통군 내 게놈</strong></th><th rowspan="1" colspan="1"><strong>검증된 유전자</strong></th></tr></thead><tbody><tr><td rowspan="1" colspan="1"><em>대장균</em></td><td rowspan="1" colspan="1"><em>엔테로박테랄레스</em></td><td rowspan="1" colspan="1">6311</td><td rowspan="1" colspan="1">769</td></tr><tr><td rowspan="1" colspan="1"><em>H. 살리나룸</em></td><td rowspan="1" colspan="1"><em>고세균</em></td><td rowspan="1" colspan="1">1125</td><td rowspan="1" colspan="1">530</td></tr><tr><td rowspan="1" colspan="1"><em>N. 파라오니스</em></td><td rowspan="1" colspan="1"><em>고세균</em></td><td rowspan="1" colspan="1">1125</td><td rowspan="1" colspan="1">282</td></tr><tr><td rowspan="1" colspan="1"><em>결핵균사체</em></td><td rowspan="1" colspan="1"><em>방사세균</em></td><td rowspan="1" colspan="1">8097</td><td rowspan="1" colspan="1">701</td></tr><tr><td rowspan="1" colspan="1"><em>R. denitrificans</em></td><td rowspan="1" colspan="1"><em>알파프로테오박테리아</em></td><td rowspan="1" colspan="1">4720</td><td rowspan="1" colspan="1">526</td></tr></tbody></table>

[새 탭에서 열기](https://pmc.ncbi.nlm.nih.gov/articles/PMC12222049/table/TB3/)

참고 서열은 각 종의 검증된 주석 데이터셋\[[20–24](#ref20)\]에 대응하는 공개 유전체 데이터베이스에서 얻어졌으며, GeneLM 파이프라인과 비교 도구를 통해 처리되었습니다. 모든 도구는 각 방법의 모범 사례를 반영한 문서화되고 재현 가능한 명령줄 워크플로우를 사용하여 실행되었습니다(도구 설명 및 실행 세부 사항에 대한 자세한 내용은 [보충 섹션 S5](#sup1) 참조). 성능은 올바르게 예측된 TIS 위치와 예측된 총 CDS 수로 측정되었습니다([표 4](#TB4) 참조).

#### 표 4.

5개의 실험적으로 검증된 박테리아 유전체에 대한 전통적인 TIS 주석 도구의 벤치마킹 결과를 보여주는 검증된 주석과의 비교; 지표에는 일치한 TIS(5'+3' 말단과 3' 말단만)가 포함되며, 괄호 안에 올바르게 예측된 끝의 백분율이 표시되어 있고, 모든 생물체의 성능을 집계한 요약 행이 포함되어 있습니다.

<table><colgroup><col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"></colgroup><thead><tr><th rowspan="1" colspan="1"><strong>박테리아</strong></th><th rowspan="1" colspan="1"><strong>GC</strong></th><th rowspan="1" colspan="1"><strong>검증된 TIS</strong></th><th colspan="2" rowspan="1"><strong>제네LM</strong></th><th colspan="2" rowspan="1"><strong>프로디걸 v3.0</strong></th><th colspan="2" rowspan="1"><strong>GeneMark-HMM v2.8</strong></th><th colspan="2" rowspan="1"><strong>글리머 (스크래치)</strong></th><th colspan="2" rowspan="1"><strong>글리머 (반복)</strong></th></tr><tr><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td><th rowspan="1" colspan="1">매치 (5'+3')</th><th rowspan="1" colspan="1">매칭된 3' 엔드</th><th rowspan="1" colspan="1">매치 (5'+3')</th><th rowspan="1" colspan="1">매칭된 3' 엔드</th><th rowspan="1" colspan="1">매치 (5'+3')</th><th rowspan="1" colspan="1">매칭된 3' 엔드</th><th rowspan="1" colspan="1">매치 (5'+3')</th><th rowspan="1" colspan="1">매칭된 3' 엔드</th><th rowspan="1" colspan="1">매치 (5'+3')</th><th rowspan="1" colspan="1">매칭된 3' 엔드</th></tr></thead><tbody><tr><td rowspan="1" colspan="1">대장균</td><td rowspan="1" colspan="1">50.8</td><td rowspan="1" colspan="1">769</td><td rowspan="1" colspan="1"><strong>744 (96.7%)</strong></td><td rowspan="1" colspan="1"><strong>768 (99.9%)</strong></td><td rowspan="1" colspan="1">338 (44.0%)</td><td rowspan="1" colspan="1">345 (44.9%)</td><td rowspan="1" colspan="1">595 (77.4%)</td><td rowspan="1" colspan="1">759 (98.7%)</td><td rowspan="1" colspan="1">276 (35.9%)</td><td rowspan="1" colspan="1">366 (47.6%)</td><td rowspan="1" colspan="1">319 (41.5%)</td><td rowspan="1" colspan="1">369 (48.0%)</td></tr><tr><td rowspan="1" colspan="1">H. 살리나룸</td><td rowspan="1" colspan="1">65.7</td><td rowspan="1" colspan="1">530</td><td rowspan="1" colspan="1">438 (82.6%)</td><td rowspan="1" colspan="1">514 (97.0%)</td><td rowspan="1" colspan="1">243 (45.8%)</td><td rowspan="1" colspan="1">255 (48.1%)</td><td rowspan="1" colspan="1"><strong>493 (93.0%)</strong></td><td rowspan="1" colspan="1"><strong>530 (100%)</strong></td><td rowspan="1" colspan="1">220 (41.5%)</td><td rowspan="1" colspan="1">266 (50.2%)</td><td rowspan="1" colspan="1">220 (41.5%)</td><td rowspan="1" colspan="1">265 (50.0%)</td></tr><tr><td rowspan="1" colspan="1">결핵균사체</td><td rowspan="1" colspan="1">65.6</td><td rowspan="1" colspan="1">701</td><td rowspan="1" colspan="1"><strong>626 (89.3%)</strong></td><td rowspan="1" colspan="1"><strong>695 (99.1%)</strong></td><td rowspan="1" colspan="1">311 (44.4%)</td><td rowspan="1" colspan="1">342 (48.8%)</td><td rowspan="1" colspan="1">545 (77.7%)</td><td rowspan="1" colspan="1">694 (99.0%)</td><td rowspan="1" colspan="1">274 (39.1%)</td><td rowspan="1" colspan="1">353 (50.4%)</td><td rowspan="1" colspan="1">271 (38.7%)</td><td rowspan="1" colspan="1">352 (50.2%)</td></tr><tr><td rowspan="1" colspan="1">N. 파라오니스</td><td rowspan="1" colspan="1">63.1</td><td rowspan="1" colspan="1">315</td><td rowspan="1" colspan="1">248 (78.7%)</td><td rowspan="1" colspan="1">302 (95.9%)</td><td rowspan="1" colspan="1">169 (53.7%)</td><td rowspan="1" colspan="1">176 (55.9%)</td><td rowspan="1" colspan="1"><strong>302 (95.9%)</strong></td><td rowspan="1" colspan="1"><strong>314 (99.7%)</strong></td><td rowspan="1" colspan="1">164 (52.1%)</td><td rowspan="1" colspan="1">178 (56.5%)</td><td rowspan="1" colspan="1">163 (51.7%)</td><td rowspan="1" colspan="1">178 (56.5%)</td></tr><tr><td rowspan="1" colspan="1">R. denitrificans</td><td rowspan="1" colspan="1">58.9</td><td rowspan="1" colspan="1">526</td><td rowspan="1" colspan="1"><strong>492 (93.5%)</strong></td><td rowspan="1" colspan="1"><strong>523 (99.4%)</strong></td><td rowspan="1" colspan="1">0 (0.0%)</td><td rowspan="1" colspan="1">0 (0.0%)</td><td rowspan="1" colspan="1">0 (0.0%)</td><td rowspan="1" colspan="1">0 (0.0%)</td><td rowspan="1" colspan="1">204 (38.8%)</td><td rowspan="1" colspan="1">273 (51.9%)</td><td rowspan="1" colspan="1">233 (44.3%)</td><td rowspan="1" colspan="1">275 (52.3%)</td></tr><tr><td rowspan="1" colspan="1"><strong>모든 유전체</strong></td><td rowspan="1" colspan="1">–</td><td rowspan="1" colspan="1">2841</td><td rowspan="1" colspan="1"><strong>2548 (89.7%)</strong></td><td rowspan="1" colspan="1"><strong>2802 (98.6%)</strong></td><td rowspan="1" colspan="1">1061 (37.3%)</td><td rowspan="1" colspan="1">1118 (39.4%)</td><td rowspan="1" colspan="1">1935 (68.1%)</td><td rowspan="1" colspan="1">2297 (80.9%)</td><td rowspan="1" colspan="1">1138 (40.1%)</td><td rowspan="1" colspan="1">1436 (50.5%)</td><td rowspan="1" colspan="1">1206 (42.4%)</td><td rowspan="1" colspan="1">1439 (50.7%)</td></tr></tbody></table>

[새 탭에서 열기](https://pmc.ncbi.nlm.nih.gov/articles/PMC12222049/table/TB4/)

Prodigal, GeneMark, Glimmer: [표 4는](#TB4) 다섯 개의 유전체 전반에 걸친 성능을 요약합니다. GeneLM은 모든 지표에서 고전 기법을 꾸준히 능가했습니다. 특히, 5'와 3' 끝 모두에서 가장 많은 일치 TIS를 달성했으며, 예측 실패도 적었습니다. *E. coli K-12* 의 경우 GeneLM은 25개의 TIS만 놓쳤고 Prodigal은 431개의 실패를 기록했습니다. GeneMark-HMM은 특히 *M. tuberculosis* 와 *H. salinarum* 과 같은 고GC 게놈에서 경쟁력 있는 성능을 보였지만, 5' 시작 정밀도에서는 GeneLM에 뒤처졌습니다. Glimmer3는 역사적으로 중요했지만 두 구성 모두에서 성능이 약했습니다. 스크래치 기반 모델은 반복 변형보다 성능이 떨어져 상류 모티프 모델링이 유익함을 확인했으나, 두 방법 모두 GeneLM에 비해 성능이 떨어졌습니다. GenBank 주석에 대한 보다 광범위한 벤치마크는 [표 5](#TB5) 에 제시되어 예측된 유전자와 알려진 유전체 주석의 정렬을 강조하며, [표 6은](#TB6) 방법 전반에 걸쳐 예측된 CDS 총 수를 요약하여 유전체 전체 count 기반의 관점을 제공합니다.

#### 표 5.

GenBank 주석과의 비교: 5개 박테리아 게놈에 걸친 유전자 발견 알고리즘의 성능을 보여주며, 각 항목은 3' 끝에서 GenBank 주석과 일치하는 예측 유전자의 수와 비율을 보고하며, 완전(5'+3') 일치 여부를 보고합니다; 실험적으로 검증되지는 않았지만, 이 벤치마크는 완전한 유전체 전반에 걸친 광범위한 성능을 제공합니다.

<table><colgroup><col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"></colgroup><thead><tr><th rowspan="1" colspan="1"><strong>박테리아</strong></th><th rowspan="1" colspan="1"><strong>GC</strong></th><th rowspan="1" colspan="1"><strong>젠뱅크 TIS</strong></th><th colspan="2" rowspan="1"><strong>제네LM</strong></th><th colspan="2" rowspan="1"><strong>프로디걸 v3.0</strong></th><th colspan="2" rowspan="1"><strong>GeneMark-HMM v2.8</strong></th><th colspan="2" rowspan="1"><strong>글리머 (스크래치)</strong></th><th colspan="2" rowspan="1"><strong>글리머 (반복)</strong></th></tr><tr><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td><td rowspan="1" colspan="1"></td><th rowspan="1" colspan="1">매칭된 (5'+3') 엔드</th><th rowspan="1" colspan="1">매칭된 3' 엔드</th><th rowspan="1" colspan="1">매치 (5'+3')</th><th rowspan="1" colspan="1">매칭된 3' 엔드</th><th rowspan="1" colspan="1">매치 (5'+3')</th><th rowspan="1" colspan="1">매칭된 3' 엔드</th><th rowspan="1" colspan="1">매치 (5'+3')</th><th rowspan="1" colspan="1">매칭된 3' 엔드</th><th rowspan="1" colspan="1">매치 (5'+3')</th><th rowspan="1" colspan="1">매칭된 3' 엔드</th></tr></thead><tbody><tr><td rowspan="1" colspan="1"><em>대장균</em></td><td rowspan="1" colspan="1">50.8</td><td rowspan="1" colspan="1">4140</td><td rowspan="1" colspan="1"><strong>3767 (91.0%)</strong></td><td rowspan="1" colspan="1"><strong>4033 (97.5%)</strong></td><td rowspan="1" colspan="1">1863 (45.0%)</td><td rowspan="1" colspan="1">1968 (47.6%)</td><td rowspan="1" colspan="1">3098 (74.8%)</td><td rowspan="1" colspan="1">3973 (96.0%)</td><td rowspan="1" colspan="1">1474 (35.6%)</td><td rowspan="1" colspan="1">2013 (48.6%)</td><td rowspan="1" colspan="1">1724 (41.6%)</td><td rowspan="1" colspan="1">2026 (49.0%)</td></tr><tr><td rowspan="1" colspan="1"><em>H. 살리나룸</em></td><td rowspan="1" colspan="1">65.7</td><td rowspan="1" colspan="1">2749</td><td rowspan="1" colspan="1">1871 (68.1%)</td><td rowspan="1" colspan="1">2559 (93.1%)</td><td rowspan="1" colspan="1">1079 (39.3%)</td><td rowspan="1" colspan="1">1270 (46.2%)</td><td rowspan="1" colspan="1"><strong>2174 (79.1%)</strong></td><td rowspan="1" colspan="1"><strong>2590 (94.2%)</strong></td><td rowspan="1" colspan="1">886 (32.2%)</td><td rowspan="1" colspan="1">1244 (45.3%)</td><td rowspan="1" colspan="1">900 (32.7%)</td><td rowspan="1" colspan="1">1244 (45.3%)</td></tr><tr><td rowspan="1" colspan="1"><em>결핵균사체</em></td><td rowspan="1" colspan="1">65.6</td><td rowspan="1" colspan="1">3906</td><td rowspan="1" colspan="1"><strong>2664 (68.2%)</strong></td><td rowspan="1" colspan="1"><strong>3709 (95.0%)</strong></td><td rowspan="1" colspan="1">1432 (36.7%)</td><td rowspan="1" colspan="1">1904 (48.7%)</td><td rowspan="1" colspan="1">2507 (64.2%)</td><td rowspan="1" colspan="1">3745 (95.9%)</td><td rowspan="1" colspan="1">1251 (32.0%)</td><td rowspan="1" colspan="1">1931 (49.4%)</td><td rowspan="1" colspan="1">1264 (32.4%)</td><td rowspan="1" colspan="1">1939 (49.6%)</td></tr><tr><td rowspan="1" colspan="1"><em>N. 파라오니스</em></td><td rowspan="1" colspan="1">63.1</td><td rowspan="1" colspan="1">2820</td><td rowspan="1" colspan="1">1978 (70.1%)</td><td rowspan="1" colspan="1">2671 (94.7%)</td><td rowspan="1" colspan="1">1313 (46.6%)</td><td rowspan="1" colspan="1">1461 (51.8%)</td><td rowspan="1" colspan="1"><strong>2424 (86.0%)</strong></td><td rowspan="1" colspan="1"><strong>2748 (97.4%)</strong></td><td rowspan="1" colspan="1">1186 (42.1%)</td><td rowspan="1" colspan="1">1483 (52.6%)</td><td rowspan="1" colspan="1">1217 (43.2%)</td><td rowspan="1" colspan="1">1484 (52.6%)</td></tr><tr><td rowspan="1" colspan="1"><em>R. denitrificans</em></td><td rowspan="1" colspan="1">58.9</td><td rowspan="1" colspan="1">4057</td><td rowspan="1" colspan="1"><strong>3278 (80.8%)</strong></td><td rowspan="1" colspan="1"><strong>3927 (96.8%)</strong></td><td rowspan="1" colspan="1">0 (0.0%)</td><td rowspan="1" colspan="1">0 (0.0%)</td><td rowspan="1" colspan="1">0 (0.0%)</td><td rowspan="1" colspan="1">0 (0.0%)</td><td rowspan="1" colspan="1">1322 (32.6%)</td><td rowspan="1" colspan="1">2002 (49.3%)</td><td rowspan="1" colspan="1">1528 (37.7%)</td><td rowspan="1" colspan="1">2025 (49.9%)</td></tr><tr><td rowspan="1" colspan="1"><strong>모든 유전체</strong></td><td rowspan="1" colspan="1">–</td><td rowspan="1" colspan="1">17 672</td><td rowspan="1" colspan="1"><strong>13 558 (76.7%)</strong></td><td rowspan="1" colspan="1"><strong>16 899 (95.6%)</strong></td><td rowspan="1" colspan="1">5687 (32.2%)</td><td rowspan="1" colspan="1">6603 (37.4%)</td><td rowspan="1" colspan="1">10 203 (57.7%)</td><td rowspan="1" colspan="1">13 056 (73.9%)</td><td rowspan="1" colspan="1">6119 (34.6%)</td><td rowspan="1" colspan="1">8673 (49.1%)</td><td rowspan="1" colspan="1">6633 (37.5%)</td><td rowspan="1" colspan="1">8718 (49.3%)</td></tr></tbody></table>

[새 탭에서 열기](https://pmc.ncbi.nlm.nih.gov/articles/PMC12222049/table/TB5/)

#### 표 6.

총 예측 CDS: 다섯 개의 실험적으로 검증된 박테리아 유전체에 대한 다섯 가지 유전자 예측 도구 간 총 예측 CDS를 비교한 결과, 마지막 행은 모든 유전체에 걸친 총 CDS 예측을 보여줍니다.

<table><colgroup><col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"></colgroup><thead><tr><th rowspan="1" colspan="1"><strong>박테리아</strong></th><th rowspan="1" colspan="1"><strong>제네LM</strong></th><th rowspan="1" colspan="1"><strong>프로디걸 v3.0</strong></th><th rowspan="1" colspan="1"><strong>GeneMark-HMM v2.8</strong></th><th rowspan="1" colspan="1"><strong>글리머 (스크래치)</strong></th><th rowspan="1" colspan="1"><strong>글리머 (반복)</strong></th></tr></thead><tbody><tr><td rowspan="1" colspan="1">대장균</td><td rowspan="1" colspan="1">4213</td><td rowspan="1" colspan="1">4347</td><td rowspan="1" colspan="1">4308</td><td rowspan="1" colspan="1">4397</td><td rowspan="1" colspan="1">4478</td></tr><tr><td rowspan="1" colspan="1">H. 살리나룸</td><td rowspan="1" colspan="1">2659</td><td rowspan="1" colspan="1">2851</td><td rowspan="1" colspan="1">2762</td><td rowspan="1" colspan="1">2717</td><td rowspan="1" colspan="1">2762</td></tr><tr><td rowspan="1" colspan="1">결핵균사체</td><td rowspan="1" colspan="1">3853</td><td rowspan="1" colspan="1">4204</td><td rowspan="1" colspan="1">4029</td><td rowspan="1" colspan="1">4240</td><td rowspan="1" colspan="1">4349</td></tr><tr><td rowspan="1" colspan="1">N. 파라오니스</td><td rowspan="1" colspan="1">2737</td><td rowspan="1" colspan="1">2873</td><td rowspan="1" colspan="1">2826</td><td rowspan="1" colspan="1">2878</td><td rowspan="1" colspan="1">2894</td></tr><tr><td rowspan="1" colspan="1">R. denitrificans</td><td rowspan="1" colspan="1">4006</td><td rowspan="1" colspan="1">4120</td><td rowspan="1" colspan="1">4104</td><td rowspan="1" colspan="1">4260</td><td rowspan="1" colspan="1">4345</td></tr><tr><td rowspan="1" colspan="1"><strong>모든 유전체</strong></td><td rowspan="1" colspan="1">17 468</td><td rowspan="1" colspan="1">18 395</td><td rowspan="1" colspan="1">18 029</td><td rowspan="1" colspan="1">18 492</td><td rowspan="1" colspan="1">18 828</td></tr></tbody></table>

[새 탭에서 열기](https://pmc.ncbi.nlm.nih.gov/articles/PMC12222049/table/TB6/)

TITER, DeepGSR, DeepTIS:고전적 유전자 예측 도구 외에도, 우리는 GeneLM을 문헌에서 최근 심층 학습 접근법과 비교해 벤치마킹했습니다. 이 방법들은 직접 추론에 적합한 사전 학습 모델을 제공하지 않기 때문에, 우리는 TIS 예측이라는 특정 과제에 맞게 원핵생물 데이터셋에서 이들의 아키텍처를 재학습했습니다. 실험적으로 검증된 유전체에서 평가하기 전에, 우리는 먼저 표준 지표인 정밀도, 회상률, F1 점수를 사용하여 균형 잡힌 데이터셋에서 성능을 평가했습니다. [보충 그림 S5](#sup1) 에서 보듯, TITER는 더 높은 회상률(77.05%)을 달성했으나 정밀도는 낮은 66.03%를 기록했으며, 이는 양성 TIS 부위에 대해 과대예측하는 경향을 나타냅니다. 반면 DeepGSR은 더 균형 잡힌 성능(정밀도: 71.99%, 기억률: 73.11%)과 약간 더 높은 F1 점수를 제공했습니다. DeepGSR은 또한 더 긴 학습 시간(106.7시간)이 TITER(84.4시간)에 비해 필요했는데, 이는 더 깊이 있는 구조와 더 많은 매개변수 수 때문으로 보입니다. 이후 두 모델 모두 5개 박테리아 유전체에 걸쳐 실험적으로 검증된 TIS 데이터셋을 사용해 GeneLM과 함께 벤치마킹되었습니다([표 7](#TB7)). 공정성을 위해 동일한 데이터로 재학습했음에도 불구하고, TITER와 DeepGSR은 GeneLM에 비해 일관되게 낮은 성능을 보였습니다. 특히 두 모델 모두 *R. denitrificans* 에서 검증된 TIS 부위를 탐지하지 못했습니다. DeepTIS는 이전에 \[[^19]\]에서 보고한 바와 같이 아키텍처 및 훈련 정보가 불완전하여 평가할 수 없었습니다.

#### 표 7.

TIS 예측 과제에서 딥러닝 접근법과 비교하여 5개의 실험적으로 검증된 박테리아 유전체에서 올바르게 예측된 5' TI의 수와 비율을 보여줍니다.

<table><colgroup><col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"></colgroup><thead><tr><th rowspan="1" colspan="1"><strong>종</strong></th><th rowspan="1" colspan="1"><strong>GC</strong></th><th rowspan="1" colspan="1"><strong>검증된 TIS</strong></th><th rowspan="1" colspan="1"><strong>GeneLM (5' 엔드)</strong></th><th rowspan="1" colspan="1"><strong>타이터 (5피트 끝)</strong></th><th rowspan="1" colspan="1"><strong>딥GSR (5피트 끝)</strong></th></tr></thead><tbody><tr><td rowspan="1" colspan="1"><em>대장균</em></td><td rowspan="1" colspan="1">50.8</td><td rowspan="1" colspan="1">769</td><td rowspan="1" colspan="1"><strong>744 (96.7%)</strong></td><td rowspan="1" colspan="1">662 (86.1%)</td><td rowspan="1" colspan="1">647 (84.1%)</td></tr><tr><td rowspan="1" colspan="1"><em>H. 살리나룸</em></td><td rowspan="1" colspan="1">65.7</td><td rowspan="1" colspan="1">530</td><td rowspan="1" colspan="1"><strong>438 (82.6%)</strong></td><td rowspan="1" colspan="1">391 (73.8%)</td><td rowspan="1" colspan="1">395 (74.5%)</td></tr><tr><td rowspan="1" colspan="1"><em>결핵균사체</em></td><td rowspan="1" colspan="1">65.6</td><td rowspan="1" colspan="1">701</td><td rowspan="1" colspan="1"><strong>626 (89.3%)</strong></td><td rowspan="1" colspan="1">493 (70.3%)</td><td rowspan="1" colspan="1">459 (65.5%)</td></tr><tr><td rowspan="1" colspan="1"><em>N. 파라오니스</em></td><td rowspan="1" colspan="1">63.1</td><td rowspan="1" colspan="1">315</td><td rowspan="1" colspan="1"><strong>248 (78.7%)</strong></td><td rowspan="1" colspan="1">220 (69.8%)</td><td rowspan="1" colspan="1">208 (66.0%)</td></tr><tr><td rowspan="1" colspan="1"><em>R. denitrificans</em></td><td rowspan="1" colspan="1">58.9</td><td rowspan="1" colspan="1">526</td><td rowspan="1" colspan="1"><strong>492 (93.5%)</strong></td><td rowspan="1" colspan="1">0 (0.0%)</td><td rowspan="1" colspan="1">0 (0.0%)</td></tr><tr><td rowspan="1" colspan="1"><strong>모든 유전체</strong></td><td rowspan="1" colspan="1">–</td><td rowspan="1" colspan="1">2841</td><td rowspan="1" colspan="1"><strong>2548 (89.7%)</strong></td><td rowspan="1" colspan="1">1766 (62.2%)</td><td rowspan="1" colspan="1">1709 (60.2%)</td></tr></tbody></table>

[새 탭에서 열기](https://pmc.ncbi.nlm.nih.gov/articles/PMC12222049/table/TB7/)

Evo2: 최근 유전체 기초 모델의 발전으로 최대 100만 염기쌍을 모델링할 수 있는 장기 맥락 DNA 언어 모델인 Evo2 \[[^20]\]가 도입되었습니다. Evo2는 8.8조 뉴클레오타이드를 대상으로 생명 영역에 걸쳐 자기회귀적으로 사전 학습되었으며, 서열 생성 및 제로 샷 변이 효과 예측과 같은 작업을 위해 설계되었습니다. Evo2가 유전자 구조 모델링에 얼마나 중요한지 탐구하기 위해, 우리는 Arc Institute와 Goodfire가 개발한 Evo Mechanistic Interpretability Visualizer를 사용했습니다. 이 도구는 내부 Evo2 활성화를 이산적이고 해석 가능한 특징으로 해독하도록 훈련된 희소 오토인코더를 사용합니다. 100개의 박테리아 게놈을 기반으로 학습된 이 해석기는 CDS, tRNA, 2차 구조 모티프와 같은 알려진 유전체 개념과 강하게 일치하는 특징을 드러냅니다. 우리는 CDS를 매우 예측하는 것으로 확인된 Evo2 특징 **f/13606** 에 집중했습니다. 이 특성은 전송된 활성화 데이터를 사용하여 전체 대 *장균* K-12 유전체 서열을 조사하여 GeneLM 예측과 대응하는 Evo2 활성화 값을 비교했습니다.

[그림 7](#f7) 에서 보듯이, f/13606 활성화는 GeneLM CDS가 예측한 주석과 일관되게 겹쳤습니다. 특히, Evo2의 비감독 내부 표현은 GeneLM의 감독 출력과 강한 일치를 보였습니다. 이러한 관찰은 Evo2 특징 활성화가 CDS 주석 파이프라인에 효과적인 생물학적 사전 또는 품질 관리 신호로 작용할 수 있음을 시사합니다. 하지만 여러 실용적·방법론적 이유로 Evo 2를 벤치마크에 포함하지 않았습니다. Evo 2의 하드웨어 요구사항은 대부분의 연구소에 매우 부담스럽습니다: 7B 모델은 이미 고용량 GPU(완전 정밀도를 위해 40GB)를 필요로 하고, 40B 변형과 컨텍스트 확장 단계는 FP8 지원이 있는 H100 GPU와 Vortex 또는 BioNeMo 스택에 의존합니다. 반면 GeneLM은 A100 및 A5000급 GPU에서 효율적으로 동작하며, 파이프라인에 자동 배치 스케일링이 내장되어 있습니다. 마지막으로, Evo 2는 훨씬 더 큰 맥락 창을 제공하지만, DNABERT에 대한 현재 결과는 대부분의 원핵생물 CDS 영역과 주변 TIS 신호가 512 bp 한계 내에 충분히 있음을 시사합니다. 따라서 장기 맥락의 이점은 원핵생물 환경에서는 미미할 수 있으며 상당한 계산 비용이 따른다. Evo2는 해석 가능성에 대한 설득력 있는 인사이트를 제공하지만, 우리는 그 명확한 설계 목표와 계산 제약을 고려해 직접적인 벤치마크 경쟁자가 아닌 유전체 신호 이해를 위한 보완적 도구로 제시합니다. 그럼에도 불구하고 우리는 Evo 2가 CDS 분류를 향상시킬 잠재력을 인정하며, 향후 하이브리드 주석 작업 흐름 작업에서 임베딩과 맥락 기능을 탐색할 계획입니다.

![Evo2 특징 활성화와 대장균 유전체에 대한 GeneLM CDS 예측 간의 정렬을 보여주는 3패널 유전체 시각화.](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/d07223d7d65d/bbaf311f7.jpg)

Evo2 활성화와 GeneLM CDS 예측을 대장균 게놈에 비교하며, Evo2 특징 활성화(f/13606)의 다중 스케일 시각화를 GeneLM 예측 CDS 영역에 정렬시켰습니다. 상단 패널: Evo2 활성화와 GeneLM 예측 간의 일관된 대응 관계를 보여주는 전체 게놈 뷰. 중간 패널: 국소 활성화 밀도와 정제된 GeneLM 경계를 강조하는 1개의 Mbp 확대 사진. 하단 패널: Evo2 활성화와 GeneLM 예측 ORF 간의 근접 염기쌍 정렬을 보여주는 15 kbp 클로즈업(시각화 IGV.js \[ 21, 22 \]).

### 주의 기반 모티프 시각화와 주의 유도 시퀀스 교란을 통한 TIS 예측 설명


TIS 분류 작업은 TIS 부위 주변의 60-뉴클레오타이드 창을 분류하는 것입니다. 모델의 의사결정 과정을 이해하기 위해, 주의 메커니즘이 분류에 어떻게 기여하는지 분석합니다. [보조 그림 S6과 S7](#sup1) 에서 보듯, 모델은 주의 머리를 통해 뚜렷한 패턴을 포착합니다. 예를 들어, 1층에서 관찰된 11번째 헤드는 TIS 상류의 30염기쌍 영역에 집중되어 프로모터 부위의 존재를 나타낼 수 있습니다. 반면 2층은 상류 영역에 더 선택적으로 집중하며, 9층에서도 유사한 패턴이 관찰됩니다. 보다 일반적인 통찰을 도출하기 위해, 고립된 서열을 분석하는 대신, 검증된 테스트 세트의 모든 서열(다섯 종의 박테리아로 구성됨)에 대한 시각화를 확장합니다. 우리는 11층, 즉 최종 주의 층에 집중하며, 이 층은 이전에 학습된 모든 패턴을 집계하고 분류 머리에 직접적인 영향을 미치며, 최종 결정에 중요한 역할을 합니다. 진정한 TIS 사이트의 경우, TIS 예측 모델을 사용해 주의 가중치를 계산하여 11개의 고정 크기 텐서를 생성하고, 크기는. 평균 주의 가중치는 시퀀스당 11개 헤드 모두에 대해 계산된 후 모든 TIS 인스턴스에 걸쳐 평균화됩니다.

[그림 8](#f8) 은 각 박테리아 종별 주의 중치 지형을 보여줍니다. **(a),** **(b),** **(c), (****d),** **(e)** 로 표시된 히트맵은 각각 *대장균(Escherichia coli*), *살리나룸(Halobacterium salinarum*), *결핵균(Mycobacterium tuberculosis*), *나트로노모나스 파라오니스(Natronomonas pharaonis*), *로즈오박터 디니트리피칸(Roseobacter denitrificans)을 의미합니다.* 빨간 상자는 TIS를 둘러싼 즉각적인 영역을 강조하고, 파란 상자는 흥미로운 패턴을 보여줍니다: 분류(CLS) 토큰의 높은 관심을 받는 서열 영역을 표시합니다. 이러한 상류 영역에는 잠재적인 프로모터 요소가 포함될 수 있는데, 이는 CLS 토큰이 서열 수준의 분류를 담당하기 때문입니다. 이 패턴은 모든 박테리아 종에서 체계적으로 관찰되며, 프로모터 영역의 예상되는 생물학적 중요성과 일치합니다.

![다섯 종의 박테리아에 대한 최종 트랜스포머층에서의 주의 분포를 보여주는 열맵.](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/9efe6600225c/bbaf311f8.jpg)

검증된 박테리아 종 간 평균 주의 가중치 분포, 각 히트맵은 진짜 TIS로 표시된 서열의 평균 주의 가중치를 보여줍니다. 시각화는 최종 예측 시 분류 토큰이 가장 많이 다뤄지는 영역을 강조합니다. \[CLS\]

모델의 학습된 주의 패턴의 생물학적 관련성을 추가로 평가하기 위해 주의 유도 방해 실험을 수행했습니다. 목표는 모델의 주의 가중치에 의해 중요하다고 판단되는 시퀀스 영역의 교란에 대한 TIS 예측 점수의 민감도를 테스트하는 것이었습니다. 구체적으로, 검증된 TIS 포함 시퀀스마다 고주의 영역 또는 저주의 영역에서 체계적인 치환을 수행했습니다. 교란 비율은 0.0(수정 없음)에서 1.0(영역 완전 대체)까지 다양했으며, 각 비율에서 모델의 TIS 예측 확률을 기록했습니다. 두 가지 교란 모드가 적용되었습니다: **높은 주의력 교란(높은 주의력 교란**, 즉 가장 높은 주의 점수의 위치를 겨냥한 대체); 그리고 **낮은 주의력 교란** (가장 적은 주의 위치에 변화를 적용)입니다.

[그림 9](#f9) 에서 볼 수 있듯이, 고주의 영역을 방해하면 교란 비율이 증가함에 따라 TIS 예측 확률이 크게 감소합니다. 이는 모델이 분류 결정을 할 때 이 영역 내의 서열 정보에 크게 의존함을 시사합니다. 반면, 저주의 영역을 교란하는 것은 예측 점수에 거의 영향을 미치지 않았으며, 대부분의 출력은 원래 확률 분포에 가까웠습니다. 이 결과는 모델이 생물학적으로 정보 영역에 집중할 수 있음을 입증하고, 유전체 서열 분류 작업에서 주의 메커니즘의 해석 가능성을 더욱 뒷받침합니다.

![나란히 배치된 박스플롯은 고주의 영역과 저주의 영역의 교란이 TIS 예측 점수에 어떤 영향을 미치는지 보여줍니다.](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/a92f/12222049/cd2afeed8d7c/bbaf311f9.jpg)

주의 유도 서열 교란이 TIS 예측 확률에 미치는 영향. 왼쪽: 박스플롯은 집중이 높은 영역이 점점 더 교란됨에 따라 예측된 확률을 보여줍니다. 오른쪽: 박스플롯은 저주의 영역을 교란했을 때의 영향을 보여줍니다. 각 박스는 모든 서열에서 특정 교란 비율로 예측된 TIS 확률의 분포를 나타냅니다.

### GeneLM 추론 확장성과 GPU 자원 분석

우리는 NVIDIA A100(80GB), RTX A5000(24GB), RTX A2000(12GB)이라는 메모리 용량이 다른 세 가지 박테리아 유전체(267M에서 464M bp)에서 추론 성능을 벤치마킹하여 GeneLM의 확장성과 실용적 타당성을 평가했습니다. 동일한 모델 구성을 사용하여 각 GPU–유전체 조합의 배치 크기와 총 추론 시간을 기록했습니다([표 8](#TB8)). 효율성을 극대화하기 위해 GeneLM 파이프라인은 사용 가능한 GPU RAM을 기반으로 배치 크기를 자동으로 확장하여 다양한 하드웨어 설정에 대해 매우 적응성이 높습니다.

#### 표 8.

GeneLM의 다양한 GPU 모델과 박테리아 유전체 간 추론 벤치마킹을 수행하며, 테이블은 GPU 메모리, 배치 크기, 실행 시간(분 단위), 게놈 크기를 보고하여 자원 요구량과 성능 확장을 보여줍니다.

<table><colgroup><col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"> <col align="left"></colgroup><thead><tr><th rowspan="1" colspan="1"><strong>게놈</strong></th><th rowspan="1" colspan="1"><strong>GPU 이름</strong></th><th rowspan="1" colspan="1"><strong>메모리 (GB)</strong></th><th rowspan="1" colspan="1"><strong>배치 스제</strong></th><th rowspan="1" colspan="1"><strong>게놈 크기(bp)</strong></th><th rowspan="1" colspan="1"><strong>추론 시간 (분)</strong></th></tr></thead><tbody><tr><td rowspan="1" colspan="1">박테리아-1</td><td rowspan="1" colspan="1"><strong>A100</strong></td><td rowspan="1" colspan="1">79.15</td><td rowspan="1" colspan="1">5375</td><td rowspan="1" colspan="1">4641 652</td><td rowspan="1" colspan="1">21.12</td></tr><tr><td rowspan="1" colspan="1">박테리아-2</td><td rowspan="1" colspan="1"><strong>A100</strong></td><td rowspan="1" colspan="1">79.15</td><td rowspan="1" colspan="1">5375</td><td rowspan="1" colspan="1">2668 776</td><td rowspan="1" colspan="1">9.75</td></tr><tr><td rowspan="1" colspan="1">박테리아-3</td><td rowspan="1" colspan="1"><strong>A100</strong></td><td rowspan="1" colspan="1">79.15</td><td rowspan="1" colspan="1">5375</td><td rowspan="1" colspan="1">4411 532</td><td rowspan="1" colspan="1">21.73</td></tr><tr><td rowspan="1" colspan="1">박테리아-1</td><td rowspan="1" colspan="1"><strong>RTX A5000</strong></td><td rowspan="1" colspan="1">23.66</td><td rowspan="1" colspan="1">1556</td><td rowspan="1" colspan="1">4641 652</td><td rowspan="1" colspan="1">33.08</td></tr><tr><td rowspan="1" colspan="1">박테리아-2</td><td rowspan="1" colspan="1"><strong>RTX A5000</strong></td><td rowspan="1" colspan="1">23.66</td><td rowspan="1" colspan="1">1556</td><td rowspan="1" colspan="1">2668 776</td><td rowspan="1" colspan="1">15.60</td></tr><tr><td rowspan="1" colspan="1">박테리아-3</td><td rowspan="1" colspan="1"><strong>RTX A5000</strong></td><td rowspan="1" colspan="1">23.66</td><td rowspan="1" colspan="1">1556</td><td rowspan="1" colspan="1">4411 532</td><td rowspan="1" colspan="1">34.80</td></tr><tr><td rowspan="1" colspan="1">박테리아-1</td><td rowspan="1" colspan="1"><strong>RTX A2000</strong></td><td rowspan="1" colspan="1">11.65</td><td rowspan="1" colspan="1">710</td><td rowspan="1" colspan="1">4641 652</td><td rowspan="1" colspan="1">101.76</td></tr><tr><td rowspan="1" colspan="1">박테리아-2</td><td rowspan="1" colspan="1"><strong>RTX A2000</strong></td><td rowspan="1" colspan="1">11.65</td><td rowspan="1" colspan="1">710</td><td rowspan="1" colspan="1">2668 776</td><td rowspan="1" colspan="1">47.74</td></tr><tr><td rowspan="1" colspan="1">박테리아-3</td><td rowspan="1" colspan="1"><strong>RTX A2000</strong></td><td rowspan="1" colspan="1">11.65</td><td rowspan="1" colspan="1">710</td><td rowspan="1" colspan="1">4411 532</td><td rowspan="1" colspan="1">106.20</td></tr></tbody></table>

[새 탭에서 열기](https://pmc.ncbi.nlm.nih.gov/articles/PMC12222049/table/TB8/)

[표 8](#TB8) 에 나타난 바와 같이, GeneLM의 추론 시간은 게놈 크기와 GPU 메모리 모두에 따라 스케일링됩니다. A100에서는 배치 크기가 5000을 초과하여 빠른 주석 작성이 가능하며(450만 bp 이상의 게놈은 22분 미만). A5000은 비교적 좋은 성능을 보이며(33–35분), A2000은 더 작은 메모리와 낮은 배치 크기(710분)로 인해 훨씬 긴 실행 시간을 보여준다(최대 106분). 서로 다른 길이의 유전체에서 GPU 효율을 더 잘 비교하기 위해, 우리는 유전체 크기별로 추론 시간을 정규화했습니다(Mbp 단위). 이로 인해 A100의 평균 추론 속도는 Mbp당 4.5분으로, A5000은 7.5분, A2000은 22+ 분으로 Mbp당 Mbp당 22분입니다. 이 값들은 총 추론 시간을 수백만 염기쌍 단위의 게놈 길이로 나누어 산출됩니다(예: 21.12 min/4.64 Mbp, 4.55 min/Mbp).

이 성능 격차는 트랜스포머 기반 추론의 메모리 바운드 특성을 반영합니다: 더 큰 배치 크기는 패딩과 메모리 전송을 줄여 처리량을 높입니다. 그럼에도 불구하고 이 모델은 A5000과 같은 중급 GPU에서도 여전히 사용 가능하여 많은 연구소에서 접근성을 제공합니다.

향후 연구에서는 혼합정밀도 추론, 양자화, 모델 증류와 같은 기법을 적용하여 추론 속도를 더욱 향상시킬 수 있습니다. 이러한 개선은 계산 자원이 제한된 환경에 맞게 GeneLM을 적응시키는 데 도움을 주어 더 넓은 채택을 촉진할 것입니다.

### GeneLM 웹 도구: 웹 애플리케이션 및 API

GeneLM을 더 넓은 연구자와 생물정보학자 커뮤니티가 접근할 수 있도록 웹 기반 게놈 주석 인터페이스와 RESTful API를 개발했습니다. 이 도구들은 모델의 실용적 적용 사례로서, 사용자가 깊은 계산 전문 지식 없이도 GeneLM을 사용해 박테리아 게놈에 주석을 달 수 있게 합니다. 이 도구는 [github.com/Bioinformatics-UM6P/GeneLM GitHub](https://github.com/Bioinformatics-UM6P/GeneLM.git) 에서 공개되어 있습니다.

GeneLM 웹 도구는 두 가지 입력 모드를 지원합니다: 사용자가 제공된 텍스트 영역에 게놈 서열을 붙여넣을 수 있는 직접 입력 모드와, FASTA 파일을 업로드하여 처리할 수 있는 파일 업로드 방식입니다. 입력이 제공되면, 사용자는 원하는 출력 형식을 지정할 수 있으며, GFF 또는 CSV 중 하나를 선택할 수 있습니다. 제출 시 시스템은 주석을 처리하고 구조화된 출력 파일을 생성합니다. 사용자 친화적인 인터페이스는 연구자와 생물정보학자들의 접근성을 보장합니다. [보조 도표 S8과 S9는](#sup1) 각각 인터페이스의 스냅샷과 다운로드 가능한 주석 출력의 예시를 보여줍니다.

그래픽 인터페이스를 넘어, 유연한 게놈 주석을 위한 프로그래밍 접근을 가능하게 하는 RESTful API를 개발했습니다. 이 API는 사용자가 비동기적으로 주석 작업을 제출하고, 여러 주석 작업을 효율적으로 대기열에 넣으며, 주석 진행 상황을 추적하고, 주석이 달린 결과를 검색하며, 필요 시 주석 작업을 취소할 수 있게 합니다. API는 잘 문서화되어 있으며, 주석 제출, 결과 검색, 작업 관리를 위한 여러 엔드포인트를 제공합니다. 이로 인해 생물정보학 파이프라인에 원활하게 통합될 수 있고, 사용자가 Python 스크립트나 기타 계산 워크플로우를 통해 직접 유전체 주석을 수행할 수 있습니다. 이 통합 웹 기반 및 API 기반 주석 파이프라인은 효율적이고 확장 가능하며 사용자 친화적인 게놈 주석 솔루션을 제공하며, 머신러닝 기반 유전자 예측과 실제 생물학 연구 간의 간극을 메웁니다.

## 토론과 결론

이 연구는 트랜스포머 기반 gLM이 정확하고 해석 가능한 박테리아 유전자 주석을 위한 잠재력을 입증합니다. DNABERT 아키텍처를 기반으로 GeneLM은 CDS 식별과 TIS 정교화 작업을 분리하는 생물학적 구조화된 2단계 분류 파이프라인을 도입합니다. 이 모듈식 설계는 생물학적 유전자 구조와 일치하며 다양한 박테리아 종 전반에 걸쳐 예측 정밀도를 향상시키는 데 기여합니다.

GeneLM의 주요 강점은 높은 정확도와 기억력을 유지하면서도 다양한 생물체에 일반화할 수 있다는 점입니다. 이는 ORF 길이 편향을 완화하기 위한 길이 층별 표본추출을 포함한 신중하게 선별되고 균형 잡힌 데이터셋으로 뒷받침됩니다. 자기 주의 지도에 대한 정성적 및 정량적 분석 결과, 이 모델은 TIS 부위 근처의 생물학적으로 의미 있는 상류 영역에 일관되게 집중하여 프로모터 유사 모티프에 민감함을 시사합니다. 이러한 통찰은 주의 유도 시퀀스 교란 실험에 의해 강화되었으며, 이 실험은 고주의 영역을 교란하면 모델의 예측에 큰 변화를 준다는 것을 보여주었습니다.

이 모델은 초기에는 대규모 자가 지도 학습을 활용하기 위해 인간 게놈 서열을 사전 학습했지만, 진핵생물과 원핵생물 게놈 간의 상당한 진화적·조직적 차이를 인정합니다. 이 도메인 격차를 해소하기 위해 GeneLM은 방대하고 다양한 박테리아 데이터셋에서 광범위하게 미세 조정되어 원핵생물 특이적 특징에 적응할 수 있게 되었습니다. 고GC 함량을 가진 여러 박테리아 계통군에서 관찰된 강한 성능과 실험적으로 검증된 데이터셋과의 벤치마킹은 이러한 적응이 실제로 효과적임을 입증합니다.

실험적으로 검증된 유전체를 이용한 벤치마킹 실험에서 GeneLM은 Prodigal, GeneMark-HMM, Glimmer와 같은 고전 유전자 예측 도구와 비교해 주석이 달린 TIS 위치를 복원하고 오탐률을 줄이는 데 최첨단 성능을 달성했습니다. 또한, 세 가지 GPU 계층에 걸친 추론 확장성 평가 결과, GeneLM은 사용 가능한 메모리에 기반한 배치 크기를 조정하여 중급 하드웨어에서도 효율적인 배포를 가능하게 합니다. 접근성을 더욱 높이기 위해, GeneLM을 기존 주석 워크플로우와의 통합을 용이하게 하는 오픈 소스 웹 도구이자 API로 출시했습니다. 트랜스포머 기반 모델은 휴리스틱 방법보다 계산 요구량이 높지만, 향후 방향으로는 혼합정밀도 추론, 양자화, 그리고 자원 사용을 줄이기 위한 모델 증류가 포함됩니다.

요약하자면, GeneLM은 박테리아 유전자 경계 식별을 위한 재현 가능하고 해석 가능한 프레임워크를 제공합니다. 이 연구의 기여는 과제 설계, 데이터셋 설계, 생물학적 인사이트, 배포 준비 수준에 걸쳐 있으며, 자동화된 유전체 주석의 추가 발전과 비암호화 및 조절 영역 발견 확장을 위한 견고한 토대를 제공합니다.

### 주요 사항

- BERT 기반 게놈 언어 모델이 개발되어 원핵생물 게놈에서 코딩 서열 영역을 식별하고 번역 시작 부위를 분류합니다.
- 이 모델은 처음에 인간 게놈 데이터셋에서 자가 지도 학습을 통해 DNA 청크 표현을 학습합니다. 그 후 유전자 주석 주석을 위해 두 단계 파이프라인을 통해 적응됩니다: 첫째, 모델이 ORF를 CDS와 비CDS 영역으로 분류하고, 두 번째 모델이 진정한 TIS 부위를 식별하는 정교화 단계가 있습니다.
- 전통적인 유전자 예측 도구와 비교 평가를 수행하여 정밀도, 기억 및 확장성 향상을 평가합니다. 검증된 박테리아 유전체에 대한 사례 연구를 수행하여 모델이 실제 유전체 주석 작업에서 적용 가능하고 견고함을 입증합니다.

## 보조 자료

Supplementary\_Materials\_bbaf311

[supplementary\_materials\_bbaf311.pdf](https://pmc.ncbi.nlm.nih.gov/articles/instance/12222049/bin/supplementary_materials_bbaf311.pdf) <sup>(5MB, pdf)</sup>

## 감사의 글

저자들은 이 논문에서 제시된 연구를 수행하는 데 사용된 슈퍼컴퓨팅 자원(cc.um6p.ma/toubkal-super-computer)에 대한 접근을 제공해 준 모하메드 6세 공과대학 컴퓨팅 대학에 감사를 표합니다.

## 기여자 정보

제네뢰 아코테누, 모로코 모하메드 6세 폴리테크닉 대학교 컴퓨팅 대학 생물정보학 연구소, 660번지, Hay Moullay Rachid, Ben Guerir 43150.

아크라프 엘 알랄리, 모로코 모하메드 6세 폴리테크닉 대학교 컴퓨팅 대학 생물정보학 연구소, 660번지, Hay Moullay Rachid, Ben Guerir 43150.

## 저자 기여

제네뢰 아코테누(방법론, 형식적 분석, 원고 작성)와 아흐라프 엘 알랄리(개념화, 방법론, 형식적 분석, 검증). 모든 저자가 원고를 검토했습니다.

이해 상충: 신고 없음.

## 자금 조달

아무도 선언하지 않았다.

## 데이터 이용 가능성

현재 구현된 작업과 학습된 모델 및 그 가중치는 [github.com/Bioinformatics-UM6P/GeneLM](https://github.com/Bioinformatics-UM6P/GeneLM.git) 에서 확인할 수 있습니다.

## 참고문헌

## Associated Data

*This section collects any data citations, data availability statements, or supplementary materials included in this article.*

### Data Availability Statement

The current implementation of our work and the trained models and their weights are available at [github.com/Bioinformatics-UM6P/GeneLM](https://github.com/Bioinformatics-UM6P/GeneLM.git).

[^1]: 1\. Hyatt D, Chen G-L, LoCascio PF. 외. 탕자: 원핵생물 유전자 인식 및 번역 시작 부위 식별. *BMC 생물정보학* 2010; 11:119. 10.1186/1471-2105-11-119 \[[DOI](https://doi.org/10.1186/1471-2105-11-119)\] \[[PMC 무료 기사](https://pmc.ncbi.nlm.nih.gov/articles/PMC2848648/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/20211023/)\] \[[구글 스칼라](https://scholar.google.com/scholar_lookup?journal=BMC%20Bioinformatics&title=Prodigal:%20prokaryotic%20gene%20recognition%20and%20translation%20initiation%20site%20identification&volume=11&publication_year=2010&pages=119&pmid=20211023&doi=10.1186/1471-2105-11-119&)\]

[^2]: 2\. 델처 AL, 하먼 D, 카시프 S. 외. 글리머를 이용한 미생물 유전자 식별 향상. *핵산 연구*, 1999; 27:4636–41. 10.1093/nar/27.23.4636 \[[DOI](https://doi.org/10.1093/nar/27.23.4636)\] \[[PMC 무료 기사](https://pmc.ncbi.nlm.nih.gov/articles/PMC148753/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/10556321/)\] \[[구글 스칼라](https://scholar.google.com/scholar_lookup?journal=Nucleic%20Acids%20Res&title=Improved%20microbial%20gene%20identification%20with%20glimmer&volume=27&publication_year=1999&pages=4636-41&pmid=10556321&doi=10.1093/nar/27.23.4636&)\]

[^3]: 3\. 베세머 J, 롬사제 A, 보로도프스키 M. 유전자 표식: 미생물 게놈에서 유전자 시작을 예측하는 자가 학습 방법. 조절 영역에서 서열 모티프 발견에 대한 시사점. *핵산 연구(Nucleic Acids Res* 2001); 29:2607–18. 10.1093/nar/29.12.2607 \[[DOI](https://doi.org/10.1093/nar/29.12.2607)\] \[[PMC 무료 기사](https://pmc.ncbi.nlm.nih.gov/articles/PMC55746/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/11410670/)\] \[[구글 스칼라](https://scholar.google.com/scholar_lookup?journal=Nucleic%20Acids%20Res&title=GeneMarkS:%20a%20self-training%20method%20for%20prediction%20of%20gene%20starts%20in%20microbial%20genomes.%20Implications%20for%20finding%20sequence%20motifs%20in%20regulatory%20regions&volume=29&publication_year=2001&pages=2607-18&pmid=11410670&doi=10.1093/nar/29.12.2607&)\]

[^4]: 4\. Tech M, Pfeifer N, Morgenstern B. 외. TICO: 원핵생물 번역 시작 부위 예측 개선을 위한 도구. *생물정보학* 2005. 전자출판 2005년 6월 30일; 21:3568–9. 10.1093/bioinformatics/bti563 \[[DOI](https://doi.org/10.1093/bioinformatics/bti563)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/15994191/)\] \[[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Bioinformatics&title=TICO:%20a%20tool%20for%20improving%20predictions%20of%20prokaryotic%20translation%20initiation%20sites&volume=21&publication_year=2005&pages=3568-9&pmid=15994191&doi=10.1093/bioinformatics/bti563&)\]

[^5]: 5\. Gang-Qing H, Zheng X, Zhu H-Q. 외. TriTISA를 이용한 미생물 게놈의 번역 시작 부위 예측. *생물정보학* 2008; 25:123–5. \[[DOI](https://doi.org/10.1093/bioinformatics/btn576)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/19015130/)\] \[[구글 스칼라](https://scholar.google.com/scholar_lookup?journal=Bioinformatics&title=Prediction%20of%20translation%20initiation%20site%20for%20microbial%20genomes%20with%20TriTISA&volume=25&publication_year=2008&pages=123-5&pmid=19015130&doi=10.1093/bioinformatics/btn576&)\]

[^6]: 6\. 리이, 장비, 다이 W. 대규모 전체 유전체 시퀀싱 분석에서 박테리아 필수 유전자의 위양성이 밝혀집니다. *미생물학 바이오테크놀 2022;* 106:341–7. 10.1007/s00253-021-11702-3 \[[DOI](https://doi.org/10.1007/s00253-021-11702-3)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/34889987/)\] \[[구글 스칼라](https://scholar.google.com/scholar_lookup?journal=Appl%20Microbiol%20Biotechnol&title=A%20large-scale%20whole-genome%20sequencing%20analysis%20reveals%20false%20positives%20of%20bacterial%20essential%20genes&volume=106&publication_year=2022&pages=341-7&pmid=34889987&doi=10.1007/s00253-021-11702-3&)\]

[^7]: 7\. 알-아즐란 A, 엘 알랄리 A. CNN-MGP: 메타게노믹스 유전자 예측을 위한 합성곱 신경망. *학제간 과학* 2019; 11:628–35. 10.1007/s12539-018-0313-4 \[[DOI](https://doi.org/10.1007/s12539-018-0313-4)\] \[[PMC 무료 기사](https://pmc.ncbi.nlm.nih.gov/articles/PMC6841655/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/30588558/)\] \[[구글 스칼라](https://scholar.google.com/scholar_lookup?journal=Interdiscip%20Sci&title=CNN-MGP:%20convolutional%20neural%20networks%20for%20metagenomics%20gene%20prediction&volume=11&publication_year=2019&pages=628-35&pmid=30588558&doi=10.1007/s12539-018-0313-4&)\]

[^8]: 8\. 엘 알랄리 A, 로즈 주니어. MGC: 메타게놈 유전자 호출자. *BMC 바이오인포매틱스* 2013; 14:S6. 10.1186/1471-2105-14-S9-S6 \[[DOI](https://doi.org/10.1186/1471-2105-14-S9-S6)\] \[[PMC 무료 기사](https://pmc.ncbi.nlm.nih.gov/articles/PMC3698006/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/23901840/)\] \[[구글 스칼라](https://scholar.google.com/scholar_lookup?journal=BMC%20Bioinformatics&title=MGC:%20a%20metagenomic%20gene%20caller&volume=14&publication_year=2013&pages=S6&pmid=23901840&doi=10.1186/1471-2105-14-S9-S6&)\]

[^9]: 9\. Benegas G, Ye C, Albors C. 외. 유전체 언어 모델: 기회와 도전. 2024년 유전학 동향; 41:286–302. 10.1016/j.tig.2024.11.013 \[[DOI](https://doi.org/10.1016/j.tig.2024.11.013)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/39753409/)\] \[[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Trends%20in%20Genetics&title=Genomic%20language%20models:%20opportunities%20and%20challenges&volume=41&pmid=39753409&doi=10.1016/j.tig.2024.11.013&)\]

[^10]: 10\. Devlin J, Chang M-W, Lee K. 외. BERT: 언어 이해를 위한 딥 양방향 변환기의 사전 학습. 수록: Burstein J, Doran C, Solorio T (편), 2019년 계산언어학회 북미 지부 회의록: HumanLanguage Technologies, 1권 (Long and ShortPapers), 4171–486쪽. 미네소타주 미니애폴리스, 2019년 6월. 계산언어학 협회.

[^11]: 11\. 바스와니 A, 샤지르 N, 파르마르 N. 외. 관심만 있으면 돼. 수록: 가이온 I, 폰 럭스버그 U, 벵지오 S, 월라치 H, 퍼거스 R, 비슈와나탄 S, 가넷 R (편), 신경 정보 처리 시스템의 발전, 제30권. 커런 어소시에이츠, Inc., 2017.

[^12]: 13\. Ji Y, Zhou Z, Liu H. 외. DNABERT: 유전체 내 DNA-언어를 위한 트랜스포머 모델에서 사전 학습된 양방향 인코더 표현. *생물정보학* 2021; 37:2112–20. 10.1093/bioinformatics/btab083 \[[DOI](https://doi.org/10.1093/bioinformatics/btab083)\] \[[PMC 무료 기사](https://pmc.ncbi.nlm.nih.gov/articles/PMC11025658/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/33538820/)\] \[[구글 스칼라](https://scholar.google.com/scholar_lookup?journal=Bioinformatics&title=DNABERT:%20pre-trained%20bidirectional%20encoder%20representations%20from%20transformers%20model%20for%20DNA-language%20in%20genome&volume=37&publication_year=2021&pages=2112-20&pmid=33538820&doi=10.1093/bioinformatics/btab083&)\]

[^13]: 14\. Gemayel K, Lomsadze A, Borodovsky M. StarLlink 및 StartLink+: 원핵생물 게놈에서 유전자 시작 예측. *프론트 바이오인폼* 2021; 1:71–84. 10.3389/fbinf.2021.704157 \[[DOI](https://doi.org/10.3389/fbinf.2021.704157)\] \[[PMC 무료 기사](https://pmc.ncbi.nlm.nih.gov/articles/PMC9581028/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/36303749/)\] \[[구글 스칼라](https://scholar.google.com/scholar_lookup?journal=Front%20Bioinform&title=StarLlink%20and%20StartLink+:%20prediction%20of%20gene%20starts%20in%20prokaryotic%20genomes&volume=1&publication_year=2021&pmid=36303749&doi=10.3389/fbinf.2021.704157&)\]

[^14]: 15\. 루카신 AV, 보로드프스키 M. GeneMark.hmm: 유전자 발견을 위한 새로운 해법. *핵산 연구,* 1998; 26:1107–15. 10.1093/nar/26.4.1107 \[[DOI](https://doi.org/10.1093/nar/26.4.1107)\] \[[PMC 무료 기사](https://pmc.ncbi.nlm.nih.gov/articles/PMC147337/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/9461475/)\] \[[구글 스칼라](https://scholar.google.com/scholar_lookup?journal=Nucleic%20Acids%20Res&title=GeneMark.hmm:%20new%20solutions%20for%20gene%20finding&volume=26&publication_year=1998&pages=1107-15&pmid=9461475&doi=10.1093/nar/26.4.1107&)\]

[^15]: 16\. Delcher AL, Bratke KA, Powers EC. 외. 글리머로 박테리아 유전자 및 내공생체 DNA 식별. *생물정보학* 2007; 23:673–9. 10.1093/bioinformatics/btm009 \[[DOI](https://doi.org/10.1093/bioinformatics/btm009)\] \[[PMC 무료 기사](https://pmc.ncbi.nlm.nih.gov/articles/PMC2387122/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/17237039/)\] \[[구글 스칼라](https://scholar.google.com/scholar_lookup?journal=Bioinformatics&title=Identifying%20bacterial%20genes%20and%20endosymbiont%20DNA%20with%20glimmer&volume=23&publication_year=2007&pages=673-9&pmid=17237039&doi=10.1093/bioinformatics/btm009&)\]

[^16]: 17\. Zhang S, Hailin H, Jiang T. 외. TITER: 딥러닝을 통한 번역 시작 지점 예측. *생물정보학* 2018; 34:516–24. \[[DOI](https://doi.org/10.1093/bioinformatics/btx247)\] \[[PMC 무료 기사](https://pmc.ncbi.nlm.nih.gov/articles/PMC5870772/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/28881981/)\] \[[구글 스칼라](https://scholar.google.com/scholar_lookup?journal=Bioinformatics&title=TITER:%20predicting%20translation%20initiation%20sites%20by%20deep%20learning&volume=34&publication_year=2018&pages=516-24&pmid=28881981&doi=10.1093/bioinformatics/btx247&)\]

[^17]: 18\. 칼카타위 M, 마가나-모라 A, 얀코빅 B. 외. DeepGSR: 유전체 신호 및 영역 인식을 위한 최적화된 딥러닝 구조. *생물정보학* 2019; 35:1125–32. 10.1093/bioinformatics/bty752 \[[DOI](https://doi.org/10.1093/bioinformatics/bty752)\] \[[PMC 무료 기사](https://pmc.ncbi.nlm.nih.gov/articles/PMC6449759/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/30184052/)\] \[[구글 스칼라](https://scholar.google.com/scholar_lookup?journal=Bioinformatics&title=DeepGSR:%20an%20optimized%20deep-learning%20structure%20for%20the%20recognition%20of%20genomic%20signals%20and%20regions&volume=35&publication_year=2019&pages=1125-32&pmid=30184052&doi=10.1093/bioinformatics/bty752&)\]

[^18]: 19\. Wei C, Zhang J, Xiguo Y. DeepTIS: 2단계 딥러닝 모델을 통한 유전체 서열 내 번역 시작 부위 예측 개선. *디지트 신호 프로세스* 2021;117:103202. 10.1016/j.dsp.2021.103202 \[[DOI](https://doi.org/10.1016/j.dsp.2021.103202)\] \[[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Digit%20Signal%20Process&title=DeepTIS:%20improved%20translation%20initiation%20site%20prediction%20in%20genomic%20sequence%20via%20a%20two-stage%20deep%20learning%20model&volume=117&publication_year=2021&pages=103202&doi=10.1016/j.dsp.2021.103202&)\]

[^19]: 25\. Clauwaert J, McVey Z, Gupta R. et al. TIS Transformer: remapping the human proteome using deep learning. *NAR Genomics Bioinf* 2023;5:lqad021. \[[DOI](https://doi.org/10.1093/nargab/lqad021)\] \[[PMC free article](https://pmc.ncbi.nlm.nih.gov/articles/PMC9985340/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/36879896/)\] \[[Google Scholar](https://scholar.google.com/scholar_lookup?journal=NAR%20Genomics%20Bioinf&title=TIS%20Transformer:%20remapping%20the%20human%20proteome%20using%20deep%20learning&volume=5&publication_year=2023&pages=lqad021&pmid=36879896&doi=10.1093/nargab/lqad021&)\]

[^20]: 26\. Brixi G, Durrant MG, Ku J. et al. Genome modeling and design across all domains of life with Evo 2. bioRxiv 2025. 10.1101/2025.02.18.638918 \[[DOI](https://doi.org/10.1101/2025.02.18.638918)\]

[^21]: 27\. Thorvaldsdóttir H, Robinson JT, Mesirov JP. Integrative Genomics Viewer (IGV): high-performance genomics data visualization and exploration. *Brief Bioinform* 2013;14:178–92. 10.1093/bib/bbs017 \[[DOI](https://doi.org/10.1093/bib/bbs017)\] \[[PMC free article](https://pmc.ncbi.nlm.nih.gov/articles/PMC3603213/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/22517427/)\] \[[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Brief%20Bioinform&title=Integrative%20Genomics%20Viewer%20\(IGV\):%20high-performance%20genomics%20data%20visualization%20and%20exploration&volume=14&publication_year=2013&pages=178-92&pmid=22517427&doi=10.1093/bib/bbs017&)\]

[^22]: 28\. Robinson JT, Thorvaldsdóttir H, Turner D. et al. igv.Js: an embeddable JavaScript implementation of the Integrative Genomics Viewer (IGV). *Bioinformatics* 2023;39:btac830. 10.1093/bioinformatics/btac830 \[[DOI](https://doi.org/10.1093/bioinformatics/btac830)\] \[[PMC free article](https://pmc.ncbi.nlm.nih.gov/articles/PMC9825295/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/36562559/)\] \[[Google Scholar](https://scholar.google.com/scholar_lookup?journal=Bioinformatics&title=igv.Js:%20an%20embeddable%20JavaScript%20implementation%20of%20the%20Integrative%20Genomics%20Viewer%20\(IGV\)&volume=39&publication_year=2023&pmid=36562559&doi=10.1093/bioinformatics/btac830&)\]