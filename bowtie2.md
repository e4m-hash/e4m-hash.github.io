# 개요
[Paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC3322381/)

DNA 시퀀싱 읽기(reads)를 참조 게놈(reference genome)에 정렬하는 표준 도구입니다.
Nature Methods에 2012년 발표된 이 알고리즘은 초고속 성능과 메모리 효율성으로 인해 NGS(차세대 시퀀싱) 분석 파이프라인의 필수 단계가 되었습니다.

## 특징
현대 게놈 분석의 핵심 도구로, 특히 50-100bp 길이의 ShortRead 에서 우수한 성능 제공
FM 인덱스 기반의 효율적인 메모리 관리와 다양한 정렬 모드는
다양한 생명정보학 응용에 맞게 정렬 전략을 선택할 수 있게 합니다.

RNA-seq, ChIP-seq, 변이 호출 등 분석의 거의 모든 영역에서 필수적인 역할을 수행합니다.

기본 개념
Short-Read DNA 를 상당히 긴 참조 게놈에 정렬하도록 설계되었습니다.
인간 게놈에 대해 시간당 2,500만 개 이상의 35bp 읽기를 정렬할 수 있는 성능을 제공합니다.

메모리 효율성
FM 인덱스(Ferragina-Manzini Index)를 사용하여 메모리 사용량을 최소화합니다.
Burrows-Wheeler Transform(BWT)을 기반으로 하는 압축 인덱싱 기술입니다.
인간 게놈의 경우 메모리 요구량이 약 3.2GB 정도로, 다른 도구에 비해 상당히 효율적입니다.

정렬 알고리즘
Bowtie2는 4단계 프로세스로 읽기를 정렬합니다:​

1. Seed 추출: 읽기와 그 역보수(reverse complement)에서 부분 문자열(seed) 추출
2. Ungapped 정렬: FM 인덱스를 사용하여 gap 없이 seed 정렬
3. Seed 우선순위 결정: 가장 유망한 seed 정렬 위치 계산
4. 전체 정렬 확장: SIMD 가속 동적 프로그래밍을 사용하여 seed를 전체 정렬로 확장

멀티시드(multiseed) 정렬 접근 방식은 빠른 속도와 정확성 사이의 균형을 제공합니다.
## 정렬 모드

| 정렬 모드           | 특징                           | 사용 사례          |
| --------------- | ---------------------------- | -------------- |
| End-to-End (기본) | 읽기 전체가 참조에 정렬되어야 함 (클립 없음)   | 신뢰도 높은 정렬 필요 시 |
| Local           | 읽기의 양쪽 끝에서 소프트 클립 허용         | 낮은 품질 영역 처리    |
| Gapped          | Affine gap penalty를 사용한 갭 허용 | 삽입/결실 감지       |
| Paired-end      | 두 개의 읽기 쌍을 통합 정렬             | 메타게놈 분석        |

| 특성     | Bowtie2               | BWA               |
| ------ | --------------------- | ----------------- |
| 정렬 민감도 | 87% local mode        | 87%               |
| 속도     | short read 에서 3배 더 빠름 | long read 에서 더 빠름 |
| 긴 읽기   | 500bp 이상에서 느림         | 500bp 이상에서 최적화    |
| 메모리    | 2-4GB (효율적)           | 2-4GB             |

## 출력
Bowtie2는 SAM(Sequence Alignment Map) 형식으로 출력을 생성합니다.
이 형식은 대부분의 후속 분석 도구와 호환되어 다른 도구와 통합됩니다.

- SAMtools: SAM/BAM 파일 조작    
- GATK: 변이 호출
- Samstat: 정렬 품질 평가

## Script
### Index
- 기본 구축
```sh
bowtie2-build -f reference_genome.fasta index_prefix
```
- E. Coli Genome
```
bowtie2-build -f /data/Escherichia_coli.fasta /index/E_coli
```
- Human Genome
```sh
bowtie2-build -f /data/GRCh38.fasta /index/GRCh38
```
- Info
```sh
# 요약 정보 출력  
bowtie2-inspect --summary /home/index/E_coli  
  
# 참조 서열 이름만 출력
bowtie2-inspect --names /home/index/E_coli  
```
### Single End
- End to End
```
bowtie2 -x index_prefix -U reads.fastq -S output.sam
```
- Multi Processing
```sh
bowtie2 -x /index/E_coli -U /data/reads.fastq -S aligned.sam -p 8
```

### Pair End
- 단일 파일 정렬
```sh
bowtie2 -x index_prefix -1 reads_R1.fastq -2 reads_R2.fastq -S output.sam
```
- 다수 파일 정렬
```sh
bowtie2 -x /index/genome \  
-1 batch1_R1.fq,batch2_R1.fq,batch3_R1.fq \  
-2 batch1_R2.fq,batch2_R2.fq,batch3_R2.fq \  
-S combined_output.sam
```
##### 거리 및 오리엔테이션 설정
###### 거리
```sh
-l 50 -X 600
```
최소 거리 ('-l') : 50bp
최대 거리 ('-X') : 600bp

###### FR (forward-reverse)
```sh
--fr
```

###### FF (forward-standard)
```sh
--ff
```
### Alignment
- End to End (default)
모든 리드 문자가 정렬되어야 한다.
```sh
bowtie2 --end-to-end -x /index/genome -U reads.fastq -S output.sam
```
- Local
양쪽 끝에서 Soft Clipping 가능 (Gap 허용)
```
bowtie2 --local -x /index/genome -U reads.fastq -S output.sam
```
- Pair End Local
```sh
bowtie2 --local \
  -x /index/genome \
  -1 reads_R1.fastq \
  -2 reads_R2.fastq \
  -S output_local.sam
```
- 최대 N 개의 정렬 보고 ('-k')
```sh
bowtie2 -x /index/genome -U reads.fastq -S output.sam -k 4
```
- 모든 정렬 보고
```sh
bowtie2 -x /index/genome -U reads.fastq -S output.sam -a
```
### Sensitivity
```
bowtie2 --fast -x /index/genome -U reads.fastq -S output.sam
bowtie2 --sensitive -x /index/genome -U reads.fastq -S output.sam
bowtie2 --very-sensitive -x /index/genome -U reads.fastq -S output.sam
```

### Filtering & Trimming
##### 품질 기준
```sh
# Phred+33 형식 (최신 Illumina)
bowtie2 --phred33 -x /index/genome -U reads.fastq -S output.sam

# Phred+64 형식 (구형 Illumina)
bowtie2 --phred64 -x /index/genome -U reads.fastq -S output.sam
```

##### MAPQ Score
```sh
# Bowtie2 정렬 후 MAPQ >= 30인 리드만 유지
bowtie2 -x /index/genome -U reads.fastq | \
    samtools view -b -q 30 > high_quality.bam
```

### Read Length Limit
```sh
# 첫 10개 리드만 정렬
bowtie2 -x /index/genome -U reads.fastq -S output.sam --upto 10

# 처음 100개를 건너뛰고 정렬
bowtie2 -x /index/genome -U reads.fastq -S output.sam --skip 100

# 처음 1000개만 정렬
bowtie2 -x /index/genome -U reads.fastq -S output.sam --qupto 1000
```