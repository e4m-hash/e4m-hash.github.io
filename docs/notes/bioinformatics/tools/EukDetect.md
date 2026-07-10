# EukDetect
Link : [Github](https://github.com/allind/EukDetect/)

# Intro

Metagenome Sequencing 에서 진핵생물을 검출하는 Marker gene 기반 도구

단일 카피 직교 유전자 \[ BUSCO(Benchmarking Universal Single-Copy Orthologs) \]를 마커로 삼아 정렬되는 리드의 유무와 양으로 종을 판정

- 재할당 과정
BUSCO 는 근연종 사이에 공유되므로 리드/염기 수가 가장 많은 genome 을 primary 로
secondary genome reads 를 재할당

한 속 안에 여러 종이 존재하는 경우 정렬 품질과 Marker 중복을 비교해서
secondary species reads 를 primary 종으로 재할당

# Workflow
- bowtie2 : --end-to-end --very-sensitive --no-discordant --no-unal -X 1000

- samtools : view -q 10

MAPQ >= 10, 정렬 길이가 리드 길이의 80% 이상인 것만 남긴다.

- complexity_filter.py

서열 고유 4-mer 수 / 서열 길이 < 0.5 저 복잡도 리드 제거

- bam_to_pid.py

마커별로 정렬 리드 수를 세고 일치/불일치 염기로부터 percent identity를 계산

## Columns

| 컬럼명                   | 단위       | 의미                                           | 역할 분류                |
| --------------------- | -------- | -------------------------------------------- | -------------------- |
| `Total_reads`         | reads    | 해당 종의 마커에 정렬되어 필터를 통과한 리드 수                  | 검출 강도 (quantity)     |
| `Reads_aligned`       | reads    | 정렬 단계에서 해당 종에 매핑된 필터 전 리드 수                  | 검출 강도 / 신뢰도 보조       |
| `Total_marker_length` | bp       | 리드가 1개 이상 정렬된 마커 유전자들의 길이 합                  | 정규화 분모 (denominator) |
| `RPKS`                | reads/kb | Reads Per Kilobase of Sequence, 마커 길이 보정 풍부도 | 정규화 풍부도 (abundance)  |
| `PID_aligned`         | %        | 정렬된 리드들의 평균 서열 일치도                           | 정렬 품질 / 종 동정 정확도     |
| `PID_reassigned`      | %        | 다중 매핑 재할당 후 해당 종 리드의 평균 일치도                  | 모호성 보정 후 품질          |
| `Reassigned_genomes`  | 목록       | 리드를 공유한 다른 참조 게놈(근연종) 정보                     | 분류학적 모호성 평가          |


- Redas total :

해당 taxon 마커에 재할당 과정을 거쳐 정렬된 총 리드 수 

- Total marker length :

Primary genome marker gene 의 전체 길이 (bp)

- RPKS ( Reads Per Kilobase of Sequence )

$$
\begin{align}

RPKS=\text{Total reads} \; / \; ( \text{Total marker length } / 1000 )

\end{align}
$$

- RPKSB ( Reads Per Kilobase of Sequence per Billion bases )

$$
\begin{align}

RPKSB \; = \; RPKS / ( \text{library size} / 10^9 )

\end{align}
$$

- Relative abundance

$$
\begin{align}
& s \; : \; \text{특정 종} \; , \; a \; : \; \text{모든 종}
\\

& \text{RelativeAbundance}=( RPKS_s \; / \; \sum \; RPKS_a ) \times 100

\end{align}
$$
