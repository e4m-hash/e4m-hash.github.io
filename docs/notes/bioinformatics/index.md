# 생물정보 (Bioinformatics)

데이터 분석 스택의 **도메인 계층**입니다. 메타지노믹스·마이크로바이옴을
중심으로, 시퀀싱 데이터를 분류·기능 단위로 해석합니다.

## 하위 분야

### OMICs
- [16S rRNA](<omics/16s rRNA.md>) — 앰플리콘 시퀀싱
- [Whole Metagenome](omics/WholeMetaGenome.md) — 샷건 메타지놈
- [single-cell RNA](omics/singlecell-RNA.md) — 단일세포 전사체

## 분석 단계 (참고)

- **전처리** — nf-core/ampliseq
- **분류 프로파일링** — Kraken2/Bracken, MetaPhlAn4 (HRGM2)
- **기능 프로파일링** — PICRUSt2, HUMAnN3 (ChocoPhlAn, UniRef90)

## 정리 예정 / 진행 중

- [ ] ITS 앰플리콘 워크플로
- [ ] 분류/기능 프로파일링 결과 해석 노트
