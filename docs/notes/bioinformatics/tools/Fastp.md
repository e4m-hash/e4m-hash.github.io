# Fastp

# 출처
[Paper](https://pubmed.ncbi.nlm.nih.gov/41112039/)
[Github](https://github.com/opengene/fastp)

# 정의
- fastp는 품질 관리(QC)와 트리밍(Trimming)을 통합한 전처리 도구
- Short-read Sequencing 데이터 분석에서 필수적으로 사용

# QC(Quality Control)

## 어댑터 트리밍

입력 데이터의 어댑터 서열을 자동으로 감지하여 제거
페어드 엔드(Paired-end) 데이터의 경우, 두 리드 간의 겹치는 영역(Overlap)을 분석하여 정밀한 어댑터 제거
이를 통해 거짓 양성(False positive) 제거 최소화

## 필터링
슬라이딩 윈도우(Sliding window) 방식
리드의 5' 및 3' 끝단에서 품질이 낮은 염기를 정밀하게 제거

- 낮은 품질의 염기(Low quality bases)가 많은 리드 제거
- 길이가 너무 짧은 리드 제거   
- 'N' 염기가 많이 포함된 리드 제거

## 중복 서열 평가 알고리즘
모든 읽기를 균일하게 샘플링하여 편향(Bias) 제거
이를 통해 더욱 정확한 시퀀스 중복도 분석이 가능

# Adapter Trimming 주요 기능

## Paired-end 데이터 오버랩 분석
페어드 엔드 데이터에서 Forward와 Reverse 리드가 겹치는 영역을 분석하여 어댑터의 위치와 길이를 정확히 파악

## Base Correction
두 리드가 겹치는 영역에서 염기 서열이 불일치할 경우, 품질 점수가 높은 쪽의 염기를 기준으로 데이터를 수정
이는 어셈블리(Assembly)와 분류(Taxonomy) 분석의 정확도 향상

## Sliding Window Quality Pruning
설정된 윈도우 크기로 리드를 스캔하면서 품질 점수가 임계값 이하인 구간을 자동으로 제거

# 특수 기능 알고리즘

## PolyG/PolyX 테일 트리밍
Illumina NovaSeq과 같은 최신 시퀀서에서 발생하는 PolyG 현상(G가 반복되는 오류)
자동으로 감지하고 제거
이를 통해 데이터 왜곡을 방지하고 분석 정확도를 높임

## 병렬 처리를 위한 데이터 분할(Data Splitting)
대용량의 메타게놈 데이터를 효율적으로 처리하기 위해 출력 파일을 여러 개의 작은 파일로 분할하여 병렬 분석이 가능하도록 지원

# Script
## Single-end
```sh
fastp -i input.fastq -o output.fastq
```
## Paired-end
```
fastp -i read1.fastq -I read2.fastq -o trimmed_1.fastq -O trimmed_2.fastq
```
## gzip
```
fastp --in1 reads_1.fastq.gz --in2 reads_2.fastq.gz \
      --out1 trimmed_1.fastq.gz --out2 trimmed_2.fastq.gz \
      --detect_adapter_for_pe
```

- `--detect_adapter_for_pe`: Paired-end 데이터에서 어댑터 자동 감지

## Quality Filtering
```sh
fastp --in1 reads_1.fastq.gz --in2 reads_2.fastq.gz \
      --out1 trimmed_1.fastq.gz --out2 trimmed_2.fastq.gz \
      --qualified_quality_phred 4 \
      --length_required 31
```
- `--qualified_quality_phred`: 
	- 품질 점수 임계값 (기본값: 15, 낮을수록 더 많은 저품질 기준 제거)
- `--length_required`: 최소 Reads 길이

## Base Repair
```sh
fastp --in1 reads_1.fastq.gz --in2 reads_2.fastq.gz \
      --out1 trimmed_1.fastq.gz --out2 trimmed_2.fastq.gz \
      --detect_adapter_for_pe \
      --qualified_quality_phred 4 \
      --length_required 31 \
      --correction
```
- `--correction`: 페어드 엔드 리드의 겹치는 영역에서 염기 교정 활성화

## QC Report
```sh
fastp --in1 reads_1.fastq.gz --in2 reads_2.fastq.gz \
      --out1 trimmed_1.fastq.gz --out2 trimmed_2.fastq.gz \
      --detect_adapter_for_pe \
      --qualified_quality_phred 4 \
      --length_required 31 \
      --correction \
      --json sample.fastp.json \
      --html sample.fastp.html
```
- `--json`: JSON 형식 리포트 파일명
- `--html`: HTML 형식 리포트 파일명

## QC Fail
한쪽 리드는 통과하고 다른 쪽은 실패한 경우를 처리합니다.

```sh
fastp --in1 reads_1.fastq.gz --in2 reads_2.fastq.gz \
      --out1 trimmed_1.fastq.gz --out2 trimmed_2.fastq.gz \
      --unpaired1 unpaired_1.fastq.gz \
      --unpaired2 unpaired_2.fastq.gz
```
- `--unpaired1`: Forward 리드 중 Reverse가 실패한 리드 출력
- `--unpaired2`: Reverse 리드 중 Forward가 실패한 리드 출력

## Poly G Tail Trim
Illumina NovaSeq에서 발생하는 PolyG 오류를 제거합니다.

```sh
fastp --in1 reads_1.fastq.gz --in2 reads_2.fastq.gz \
      --out1 trimmed_1.fastq.gz --out2 trimmed_2.fastq.gz \
      --detect_adapter_for_pe \
      --trim_poly_g \
      --poly_g_min_len 10
```

- `--trim_poly_g`: PolyG 테일 트리밍 활성화
- `--poly_g_min_len`: PolyG 최소 길이 (기본값: 10 bp)

## Multi Threading
```
fastp --in1 reads_1.fastq.gz --in2 reads_2.fastq.gz \
      --out1 trimmed_1.fastq.gz --out2 trimmed_2.fastq.gz \
      --thread 8
```
- `--thread`: 사용할 스레드 수 (기본값: 2)

## Custom Adapter Trim
```sh
fastp --in1 reads_1.fastq.gz --in2 reads_2.fastq.gz \
      --out1 trimmed_1.fastq.gz --out2 trimmed_2.fastq.gz \
      --adapter_sequence "AGATCGGAAGAGCACACGTC" \
      --adapter_sequence_r2 "AGATCGGAAGAGCGTCGTGT" \
      --qualified_quality_phred 20 \
      --length_required 40
```
- `--adapter_sequence`: Forward 어댑터 서열
- `--adapter_sequence_r2`: Reverse 어댑터 서열

## Load Adpater Fasta file
```sh
fastp --in1 reads_1.fastq.gz --in2 reads_2.fastq.gz \
      --out1 trimmed_1.fastq.gz --out2 trimmed_2.fastq.gz \
      --adapter_fasta adapters.fa \
      --detect_adapter_for_pe \
      --qualified_quality_phred 4 \
      --length_required 31
```
- `--adapter_fasta`: 어댑터 서열을 포함한 FASTA 파일

## Overrepresented
```sh
fastp --in1 reads_1.fastq.gz --in2 reads_2.fastq.gz \
      --out1 trimmed_1.fastq.gz --out2 trimmed_2.fastq.gz \
      --detect_adapter_for_pe \
      --overrepresentation_analysis \
      --overrepresentation_sampling 20 \
      --json sample.fastp.json \
      --html sample.fastp.html
```
- `--overrepresentation_analysis`: Overrepresented 서열 분석 활성화
- `--overrepresentation_sampling`: 샘플링 간격 (1~10000, 작을수록 정확하나 느림)
