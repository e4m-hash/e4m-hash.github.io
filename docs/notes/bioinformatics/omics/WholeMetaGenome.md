# Bacteria

## Taxonomy


## Funtional
Bacterial functional profile은 세균 군집이나 세균 유전체를 특정 기능 단위별로 정량화한 프로파일

```text
                Sample 1   Sample 2   Sample 3
KO:K00844          120        35         80
GO:0006096          55        62         41
MetaCyc:GLYCOLYSIS  12.3       8.1       10.4
```

측정 단위
- 유전자 또는 단백질 family의 abundance
- 효소 기능
- 대사 pathway
- GO term
- DNA 기반 기능 잠재력
- RNA 기반 발현량

### 생물학적 계층
```text
read / contig
   ▼
gene / protein sequence
   ▼
gene/protein family
   ├─ UniRef
   ├─ KO
   ├─ COG/eggNOG
   ├─ Pfam
   └─ GO annotation
   ▼
enzyme / reaction
   ├─ EC number
   └─ MetaCyc reaction
   ▼
metabolic pathway / module
   ├─ MetaCyc pathway
   ├─ KEGG pathway
   └─ KEGG module
```

- GO·KO·UniRef : 개별 유전자/단백질 기능 표현
- pathway : 여러 유전자/효소가 구성하는 생화학적 과정   

### HUMAnN
Link: [GitHub](https://github.com/biobakery/humann?utm_source=chatgpt.com "GitHub - biobakery/humann")

shotgun metagenome 또는 metatranscriptome 데이터로 미생물 군집의 gene family & metabolic pathway abundance를 추정하는 파이프라인

```text
FASTQ
  ▼
MetaPhlAn 종 조성 추정
  ▼
검출된 종의 pangenome에 nucleotide alignment
  ▼
남은 read를 UniRef protein database에 translated alignment
  ▼
UniRef gene-family abundance
  ▼
MetaCyc reaction으로 regroup
  ▼
MetaCyc pathway abundance 추정
```

taxonomic prescreen 이후 ChocoPhlAn pangenome & UniRef protein family
이용해 기능 추정

#### 출력
##### `genefamilies.tsv`

개별 gene family abundance
feature : UniRef90/50

```text
UniRef90_A0A123
UniRef90_A0A123|g__Bacteroides.s__Bacteroides_vulgatus
UniRef90_A0A123|unclassified
```

- `UniRef90_A0A123`: 군집 전체 abundance    
- `UniRef90_A0A123|species`: 해당 종이 기여한 abundance

- unstratified: 군집 전체
- stratified: taxon별 기여량


Gene-family abundance는 유전자 길이를 보정한 RPK 단위
이후 CPM 또는 relative abundance로 정규화할 수 있다.

###### 의미
Metagenome DNA를 입력했다면:
> 군집에 해당 gene family가 얼마나 존재하는지를 나타내는 기능적 잠재력

Metatranscriptome RNA를 입력했다면:
> 해당 gene family의 상대적인 전사 활동에 가까운 값

##### `pathabundance.tsv`

MetaCyc pathway의 abundance

```text
PWY-5484: glycolysis II
PWY-5484|g__Bacteroides.s__Bacteroides_caccae
```

gene family를 MetaCyc reaction에 연결하고
구성 reaction의 abundance와 pathway 구조를 이용해 pathway abundance를 계산한다.

Pathway abundance는 구성 유전자 abundance의 합이 아니다.

```text
Reaction 1 abundance = 100
Reaction 2 abundance = 10
Reaction 3 abundance = 12
```

pathway abundance는 100에 가까워지는 것이 아니라
필수 반응 중 부족한 부분에 더 크게 제한된다.

> 군집에 존재할 것으로 추정되는 완전한 pathway의 상대적 양

##### `pathcoverage.tsv`

완성도 / 검출 신뢰도 지표

- `pathabundance`: pathway가 얼마나 많은가
- `pathcoverage`: pathway 구성요소가 얼마나 충분히 검출되었는가


abundance가 낮아도 coverage가 상대적으로 높을 수 있고
특정 구성 유전자가 많이 검출되어도 pathway 전체 coverage는 낮을 수 있다.

##### 특수 feature

###### `UNMAPPED`/`READS_UNMAPPED`
reference gene/protein에 매핑되지 않은 read

값이 높다면 다음과 같은 가능성 존재

- reference database에 없는 미생물
- 새로운 단백질
- 낮은 품질 read
- 짧거나 보존성이 낮은 서열
- 비암호화 영역
- 바이러스 또는 진핵 DNA
- 데이터베이스 버전 또는 적용 범위 문제

###### `UNINTEGRATED`
gene family로 검출되었지만 HUMAnN의 pathway에 통합되지 않은 기능량
pathway에 기여하지 않은 gene abundance

```text
UNMAPPED
= 알려진 gene family에 연결되지 않음

UNINTEGRATED
= gene family에는 연결되었으나 MetaCyc pathway에는 포함되지 않음
```
##### KO/GO 관계

UniRef abundance를 다른 기능 체계로 regroup할 수 있다.

```text
UniRef -> KO
UniRef -> GO
UniRef -> EC
UniRef -> Pfam
UniRef -> eggNOG/COG
UniRef -> MetaCyc reaction
```

`humann_regroup_table` : UniRef feature들을 KO, GO, EC, Pfam 등의 annotation group으로 합산한다.

이 매핑은 주로 UniRef centroid의 UniProt annotation에서 유도된다.
([Galaxy Tool Shed](https://toolshed.g2.bx.psu.edu/repository/display_tool?changeset_revision=26ce946f4da9&render_repository_actions_for=tool_shed&repository_id=02b6c7be6dad442a&tool_config=%2Fsrv%2Ftoolshed-repos%2Fmain%2F005%2Frepo_5670%2Fhumann_regroup_table.xml&utm_source=chatgpt.com "What it does"))

```text
UniRef90_A -> K00001
UniRef90_B -> K00001
UniRef90_C -> K00002
```
```text
abundance(K00001)
= abundance(UniRef90_A) + abundance(UniRef90_B)
```

> UniRef abundance를 KO 단위로 재집계한 것

### GO

GO : Gene Ontology

유전자 산물의 기능을 표준화된 용어로 기술하는 계층적 ontology 세 가지 축으로 나뉜다.

| GO 범주                   | 의미                     | 예                                 |
| ----------------------- | ---------------------- | --------------------------------- |
| Molecular Function (MF) | 분자가 직접 수행하는 작용         | ATP binding, DNA-binding activity |
| Biological Process (BP) | 여러 분자 활동이 참여하는 생물학적 과정 | glycolytic process, DNA repair    |
| Cellular Component(CC)  | 기능이 일어나는 세포 위치\|구조     | ribosome, membrane, cytoplasm     |

#### 특징

### 하나의 유전자 : 여러 GO term

하나의 단백질은 동시에 여러 term을 가질 수 있다.

```text
ATP binding
protein kinase activity
signal transduction
membrane component
```

##### 계층 구조

좁은 term은 더 넓은 상위 term에 포함된다.

```text
carbohydrate metabolic process
  └─ glucose metabolic process
       └─ glycolytic process
```

##### pathway 와 차이점

명시하지 않는 정보 :

- 정확한 반응 순서
- 기질과 생성물
- 반응식
- 화학량론
- 필수 단계
- 대체 경로

기능 분류 | enrichment 분석 적합
대사 pathway reconstruction 부적합

### KO

KO : KEGG Orthology

```text
K00844
K00001
K01915
```

KO :  KEGG network 안에서 유사한 기능으로 정의된 functional ortholog group
KEGG : KO를 pathway map, module, BRITE hierarchy 등 node로 사용

> KO : KEGG에 포함된 기능 단위 | KEGG : 전체 데이터베이스 생태계
#### 의미

> 서로 다른 생물종에서 동일하거나 매우 유사한 기능을 수행하는 유전자 집단은 무엇인가?

하나의 KO : 특정 효소, transporter subunit, regulator | 복합체 구성요소에 대응할 수 있다.

| KEGG 객체  | 예          | 의미                             |
| -------- | ---------- | ------------------------------ |
| KO       | `K00844`   | functional ortholog group      |
| PATHWAY  | `map00010` | 대사·신호·세포 과정 network            |
| MODULE   | `M00001`   | 비교적 작은 기능적 단위 \| pathway block |
| REACTION | `Rxxxxx`   | 생화학 반응                         |
| COMPOUND | `Cxxxxx`   | 화합물                            |
| BRITE    | 계층 ID      | 기능적 분류체계                       |
| ENZYME   | EC 연계      | 효소 분류                          |

- KO abundance
- KEGG pathway abundance
- KEGG module completeness
- KEGG BRITE category abundance
- KEGG reaction abundance

#### 장점

- 종 간 비교가 쉬움
- KEGG pathway/module에 직접 연결 가능
- metagenome 기능 프로파일에 널리 사용됨
- 유전자 수준과 pathway 수준의 중간 연결점 역할

#### 한계

- 하나의 KO가 여러 pathway에 참여할 수 있음
- 하나의 반응을 여러 KO가 대체할 수 있음
- ortholog라고 해서 모든 환경에서 기능이 완전히 동일한 것은 아님
- 유전자 위치와 주변 유전자 구조는 표현하지 않음
- abundance만으로 pathway 완성 여부가 보장되지 않음

### 종합

| 항목              | GO               | KO                  | KEGG pathway/module   | HUMAnN pathway                |
| --------------- | ---------------- | ------------------- | --------------------- | ----------------------------- |
| 객체 수준           | 기능 term          | ortholog gene group | pathway/network       | 추정된 MetaCyc pathway abundance |
| 예시 ID           | `GO:0005524`     | `K00844`            | `map00010`, `M00001`  | `PWY-5484`                    |
| 개별 유전자 기반       | 예                | 예                   | KO를 통해 연결             | gene abundance에서 계산           |
| 계층 구조           | 강함, DAG          | BRITE 등과 연결         | pathway/module 구조     | reaction/pathway 구조           |
| genomic context | 없음               | 없음                  | 없음                    | 거의 없음                         |
| abundance 계산    | annotation 합산    | gene abundance 합산   | 방법에 따라 다름             | HUMAnN 알고리즘으로 추정              |
| 주요 용도           | 기능 분류·enrichment | 비교 유전체·대사 기능        | 시스템·대사 reconstruction | 군집 대사 잠재력                     |
| 주요 한계           | term 중복과 계층 의존성  | 기능과 orthology의 불완전성 | pathway 중복·크기 차이      | reference 및 inference 의존      |

# Fungi
# Taxonomuy
## Database
### CGF catalog

- 원 논문: [A genomic compendium of cultivated human gut fungi (Cell, 2024)](https://doi.org/10.1016/j.cell.2024.04.043)
- 원본 코드: <https://github.com/yexianingyue/Cultivated-Gut-Fungi>

#### 구축 원리와 검출 과정
```

[배양·시퀀싱] [유전자 예측] [클러스터링] [매핑/정량]
건강한 사람 분변 -> 760 진균 유전체 -> 비중복 유전자 -> 메타지놈 read 를
에서 진균 배양 각 유전체의 유전자 카탈로그(대표 서열) 유전자에 매핑 ->
(CDS) 예측 + 종(species) 연결 종별 상대 풍부도(%)
```
##### Curation

1. 배양(culture) : 건강한 사람의 분변에서 진균을 직접 배양한다.
2. 시퀀싱 & 어셈블리 : 배양한 균주를 시퀀싱해 유전체를 조립한다.
3. 규모 :최종적으로 760개 유전체 / 206 species / 48 families 가 모였고, 이 중 69 species 는 기존에 알려지지 않은 신규 종이다.
4. 분류(taxonomy) 부여. 각 유전체를 계통(kingdom->species)에 연결한다. -> `db.fungi.taxonomy.tsv`,`genomes_2_clu.tsv`.

##### 유전자 예측과 Clustering
###### 유전자 예측
각 유전체에서 단백질 코딩 유전자(CDS)의 핵산 서열을 예측한다. (원본 예제의 `genes/.ffn`)
###### MMseqs2
모든 진균 유전자 핵산 서열을 MMseqs2 로 클러스터링한다 :
```sh

mmseqs easy-cluster genes/ database/geneset tmp \
--min-seq-id 0.95 --cov-mode 1 -c 0.9 --cluster-mode 2 \
--cluster-reassign 1 --kmer-per-seq 200 --kmer-per-seq-scale 0.8
```

- `--min-seq-id 0.95` : 서열 유사도 95% 이상이면 같은 클러스터로 묶는다.
- `-c 0.9 --cov-mode 1` : 길이 90% 이상이 겹쳐야 묶는다(짧은 우연 일치 방지).
- 결과: 비슷한 유전자들이 하나의 클러스터로 합쳐지고, 각 클러스터에서 대표 서열 1개만 남긴

비중복 유전자 카탈로그(`db.fungi.fa.gz`)가 된다.
-> 매핑 reference 가 가벼워지고 중복 정렬이 줄어든다.
###### 고유(unique) / 공유(shared) 유전자

클러스터마다 "이 유전자가 어느 종에서 왔는가"를 유전체 분류 정보로 되짚는다.
```

gene -> cluster -> (그 클러스터에 속한 유전자들이 온) 종 목록

```
- 클러스터가 한 종에만 연결됨 -> 그 종의 고유(특이) 유전자 (정량의 핵심 근거)
- 클러스터가 여러 종에 연결됨 -> 공유 유전자 (어느 종인지 단정 불가, 나중에 비례 분배)

> 결과물:
> - `gene2clu.map` : gene -> cluster(들). 콤마면 여러 종에 걸친 공유 클러스터.
> - `clu.uniq_gene.sum` : 종별로, 그 종의 고유 유전자 클러스터들의 총 길이 합. -> 길이 정규화에 사용.

유전자가 길수록 read 가 우연히 더 많이 붙는다. 종마다 고유 유전자 총길이가 다르므로, `read 수 ÷ 고유 유전자 길이` 로 보정해야 종끼리 공정하게 비교된다.

##### Detection
전처리된 paired-end WMS read 를 받아, 불필요한 read 를 단계적으로 걸러낸 뒤 남은 read 로 종별 상대 풍부도를 계산한다. (read 는 R1/R2 를 묶지 않고 single-end 로 풀링: `-U R1,R2` )

###### 필터링
```
입력 read

│ STEP1 진균 유전자에 붙는 read 만 남김 (--al-gz, db.fungi.fa.gz)

▼

진균 후보 read

│ STEP2 사람(human/PhiX) 유래 제거 (--un-gz) ※기본 skip, 상류 전처리 전제
│ STEP3 세균(UHGG) 유래 제거 (--un-gz)
│ STEP4 rRNA 유래 제거 (--un-gz, db.fungi_target.fa.gz)

▼

깨끗한 진균 read

│ STEP5 진균 유전자에 재매핑, -k 1000 (다중 매핑까지 SAM 으로 확보)

▼

SAM -> GPA.py -> 종별 상대 풍부도(%) (.rc)
```

- STEP1 에서 먼저 진균만 추리는 이유:

진균 read 가 워낙 적어, 전체에서 바로 정량하면 노이즈에 묻힌다.
진균 유전자에 붙는 read 만 모은 뒤 오염원을 빼는 편이 효율적이고 민감하다.

- 제거 이유:
사람·세균·rRNA 서열은 보존도가 높아 진균 유전자에 우연히 교차 정렬되어 풍부도를 부풀린다.
특히 rRNA 는 다중 복제·고보존이라 반드시 제거한다.

- STEP5 `-k 1000`:

한 read 가 여러 유전자(여러 종)에 붙는 경우를 빠짐없이 SAM 에 남겨
다음 단계에서 공정하게 분배

###### 풍부도 계산 원리 (Gene/Genome Profiling Abundance)
"확실한 것(고유 유전자에 유일하게 붙은 read)으로 먼저 종 비율을 정하고
애매한 것(여러 종에 붙은 read)은 그 비율대로 나눠 준다."

1. 유사도 필터: 정렬 identity 가 95%(`-s 0.95`) 미만이면 버린다. (CIGAR 길이 대비 `MD:Z` 일치 염기 수로 계산)

2. fragment 단위 중복제거: R1/R2 는 같은 read 이름(QNAME)을 공유하므로, 같은 종에 붙은 mate 는 `{QNAME}{종}` 키로 한 번만 센다 -> 이중 계수 없음(= fragment 단위).

3. 유일 매핑 집계: 한 종의 고유 유전자에만 붙은 read -> 그 종에 직접 카운트.

4. 예비 상대 풍부도: 종별로 `유일매핑 read 수 ÷ 그 종의 고유 유전자 총길이`.

5. 다중 매핑 재분배: 여러 종에 붙은 read 는 4번에서 구한 종별 비율대로 비례 배분해 더한다.

(후보 종 모두 고유 매핑이 0이면 분배 불가 -> `1.vs.multiple.only` 로 따로 집계, 풍부도엔 미반영)

6. 정규화: `(유일 + 분배) ÷ 고유 유전자 길이` 를 전체 종에 대해 백분율(%) 로 환산.

-> `cluster<TAB>percent` 2열 TSV(`<sample>.rc`)로 출력.

##### 대응표

| DB                             | 만들어지는 단계        | 검출에서의 쓰임                       |
| ------------------------------ | --------------- | ------------------------------ |
| `760genomes/`, `.taxonomy.tsv` | Curation        | 종 분류의 원천                       |
| `db.fungi.fa.gz` (비중복 유전자)     | Clustering(2-2) | 진균 매핑 reference (STEP1·STEP5)  |
| `gene2clu.map`                 | Clustering(2-3) | gene->종 연결, 고유/공유 판별(GPA)      |
| `clu.uniq_gene.sum`            | Clustering(2-3) | 종별 고유 유전자 길이, 정규화(GPA)         |
| `db.fungi_target.fa.gz`        | (rRNA 등 target) | rRNA read 제거 reference (STEP4) |
##### 한계
- 배양 가능한 종만 포함:
배양 기반이라 배양이 안 되는 진균은 빠질 수 있다.

- 고유 유전자 의존: 고유 유전자가 거의 없는 매우 가까운 종들은 분해능이 떨어질 수 있다.