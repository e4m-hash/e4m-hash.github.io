# Bioinformatics

ML 프로젝트의 입력 데이터와 제약을 설명하는 domain layer입니다. 이 탭은 생물학 자체를
포트폴리오의 중심으로 두기보다, ML pipeline과 평가 설계에 영향을 주는 조건을 기록합니다.

## ML 프로젝트에 필요한 도메인 제약

- FASTQ와 sample metadata의 pair·checksum·identifier 검증
- reference DB와 profiling pipeline에 따라 달라지는 feature schema
- compositional, sparse, high-dimensional abundance data
- subject 중복과 cohort·batch effect에 의한 leakage
- 신규 cohort에서의 generalization과 calibration

## Data Sources

- [NCBI](data/ncbi/main.md) — sequence와 metadata 수집
- [curatedMetagenomicData](data/curatedMetagenomicData/main.md) — 공개 cohort와 feature matrix

## OMICs

- [16S rRNA](<omics/16s rRNA.md>) — amplicon sequencing
- [Whole Metagenome](omics/WholeMetaGenome.md) — shotgun metagenomics
- [single-cell RNA](omics/singlecell-RNA.md) — single-cell transcriptomics

## Tools

- QC·filtering — [Fastp](tools/Fastp.md), [BBDuk](tools/BBduk.md)
- alignment — [Bowtie2](tools/bowtie2.md)
- taxonomy — [Kraken2](tools/Kracken2.md), [Bracken](tools/Bracken.md), [MetaPhlAn](tools/MetaPhlan.md), [EukDetect](tools/EukDetect.md)

## Papers

- [Microbiome ML best practices](<../../papers/Best practices for developing microbiome-based disease diagnostic classifiers through machine learning.md>)
- [Genomic language models](<../../papers/Genomic language models (gLMs) decode bacterial genomes for improved gene prediction and translation initiation site identification/Summary.md>)

→ [논문 리뷰 전체](../../papers/index.md)
