# 구조
```nextflow
./
├── main.nf                    # 진입점 + 파라미터 초기화
├── nextflow.config            # 기본 설정
├── nextflow_schema.json       # 파라미터 스키마 (검증용)
│
├── workflows/
│   └── analysis.nf            # 워크플로우 정의
│
├── modules/
│   ├── local/
│   │   ├── process_a.nf
│   │   └── process_b.nf
│   └── nf-core/
│       └── (nf-core 모듈 재사용)
│
├── subworkflows/
│   ├── local/
│   │   ├── prepare_data.nf
│   │   └── quality_control.nf
│   └── nf-core/
│       └── (nf-core 모듈 재사용)
│
├── bin/
│   ├── script1.py
│   ├── script2.R
│   └── validate_input.sh
│
├── assets/
│   ├── reference.fa
│   ├── annotation.gff
│   └── design.csv
│
├── conf/
│   ├── base.config            # 기본 프로파일
│   ├── modules.config         # 프로세스별 리소스
│   ├── test.config            # 테스트 프로파일
│   ├── hpc.config             # HPC 클러스터 설정
│   └── docker.config          # Docker 설정
│
├── results/                   # 출력 디렉토리 (자동생성)
│   ├── qc/
│   ├── alignment/
│   └── reports/
│
├── docs/
│   ├── README.md
│   ├── INSTALL.md
│   └── USAGE.md
│
├── tests/
│   ├── test.nf                # 통합 테스트
│   └── test_data/
├── works/
│   ├── 00/
│      ├── Process HASH ID
│      ├── ...
│      └── Process HASH ID
│   ├── .../
│   └── ff/
│      ├── Process HASH ID
│      │    ├── Result Files
│      │    └── .command.sh
│      │
│      ├── ...
│      └── Process HASH ID
│
└── samplesheet.csv
└── .gitignore
```
###### SampleSheet.csv
nextflow 의 input 으로 사용되는 파일입니다.

| sample  | group | short_reads1     | short_reads2     | long_reads | short_reads_platform | long_reads_platform |
| ------- | ----- | ---------------- | ---------------- | ---------- | -------------------- | ------------------- |
| sample1 | 0     | path_1.fastaq.gz | path_2.fastaq.gz |            | ILLUMINA             |                     |
| sample2 | 1     | path_1.fastaq.gz | path_2.fastaq.gz |            | ILLUMINA             |                     |

# Script
```sh
nextflow log last -f hash,process,workdir
```
Nextflow의 `work` 폴더는 작업마다 고유한 해시(hash) 값으로 디렉토리가 생성되기 때문에
겉으로 봐서는 어떤 작업이 수행되었는지 알기 어렵습니다.

# Work
module ~ subworkflow 의 폴더로 계층화 하여
각 단계들의 작업과정이 저장된 폴더

```
├── works/
│   ├── 00/
│      ├── Process HASH ID
│      ├── ...
│      └── Process HASH ID
│   ├── .../
│   └── ff/
│      ├── Process HASH ID
│      │    ├── Result Files
│      │    └── .command.sh
│      │
│      ├── ...
│      └── Process HASH ID
```
- 00 ~ ff : Subworkflow 작업 단위
- Process HASH ID : Process 작업 단위
- Result Files : 중간 결과물
- .command.sh : Module 또는 Process 의 작업 명령어

### Config
#### nextflow.config
- param : 전역 변수 선언
- profiles : 프로세스 실행 환경 선언
- env : 환경 변수 선언
- plugins : nf-core plugin 선언
- includeConfig : 자원 할당 등 설정 로드

```groovy
params {
	input = null
}

profiles {
	docker {  
		docker.enabled = true  
		conda.enabled = false  
		singularity.enabled = false  
		podman.enabled = false  
		shifter.enabled = false  
		charliecloud.enabled = false  
		apptainer.enabled = false  
		docker.runOptions = '-u $(id -u):$(id -g)'  
	}
}

env {  
	PYTHONNOUSERSITE = 1  
	R_PROFILE_USER = "/.Rprofile"  
	R_ENVIRON_USER = "/.Renviron"  
	JULIA_DEPOT_PATH = "/usr/local/share/julia"  
}

plugins {
	id 'nf-schema@2.5.1'
}
docker.registry = 'quay.io'

includeConfig 'conf/base.config'
```
#### conf/base.config
- 프로세스 자원 할당 설정
```groovy
process {    
	cpus = { 1 * task.attempt }  
	memory = { 7.GB * task.attempt }  
	time = { 4.h * task.attempt }  
	  
	  
	errorStrategy = { task.exitStatus in ((130..145) + 104 + 175) ? 'retry' : 'finish' }
	
	maxRetries = 3  
	maxErrors = '-1'  
	  
	withLabel: process_single {  
		cpus = { 1 }  
		memory = { 6.GB * task.attempt }  
		time = { 4.h * task.attempt }  
	}

}
```
#### assets/input_schema.json
SampleSheet.csv 등 Input 에 대한 입력값 검증 설정

```json
{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://raw.githubusercontent.com/nf-core/mag/main/assets/schema_input.json",
    "title": "nf-core/mag pipeline - params.input schema",
    "description": "Schema for the file provided with params.input",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "sample": {
                "type": "string",
                "pattern": "^\\S+$",
                "meta": ["id"],
                "errorMessage": "Sample needs to be string or integer with no spaces!"
            },
            "run": {
                "type": ["string", "integer"],
                "pattern": "^\\S+$",
                "meta": ["run"],
                "unique": ["sample"],
                "errorMessage": "Run needs to be string or integer with no spaces!"
            },
            "group": {
                "type": ["string", "integer"],
                "pattern": "^\\S+$",
                "meta": ["group"],
                "errorMessage": "Group needs to be string or integer with no spaces!"
            },
            "short_reads_1": {
                "type": "string",
                "format": "file-path",
                "exists": true,
                "pattern": "^\\S+\\.f(ast)?q\\.gz$",
                "errorMessage": "short_reads_1 needs to be a file path with no spaces.\n\nFile needs to exist!"
            },
            "short_reads_2": {
                "type": "string",
                "format": "file-path",
                "exists": true,
                "pattern": "^\\S+\\.f(ast)?q\\.gz$",
                "errorMessage": "short_reads_2 needs to be a file path with no spaces.\n\nFile needs to exist!"
            },
            "short_reads_platform": {
                "type": "string",
                "enum": [
                    "ILLUMINA",
                    "BGISEQ",
                    "LS454",
                    "ION_TORRENT",
                    "DNBSEQ",
                    "ELEMENT",
                    "ULTIMA",
                    "VELA_DIAGNOSTICS",
                    "GENAPSYS",
                    "GENEMIND",
                    "TAPESTRI"
                ],
                "meta": ["sr_platform"]
            },
            "long_reads": {
                "type": "string",
                "format": "file-path",
                "exists": true,
                "pattern": "^\\S+\\.f(ast)?q\\.gz$"
            },
            "long_reads_platform": {
                "type": "string",
                "enum": ["OXFORD_NANOPORE", "OXFORD_NANOPORE_HQ", "PACBIO_CLR", "PACBIO_HIFI"],
                "meta": ["lr_platform"]
            }
        },
        "required": ["sample", "group"],
        "anyOf": [{ "required": ["short_reads_1"] }, { "required": ["long_reads"] }],
        "dependentRequired": {
            "short_reads_2": ["short_reads_1"],
            "short_reads_1": ["short_reads_platform"],
            "long_reads": ["long_reads_platform"]
        }
    },
    "uniqueEntries": ["sample", "run"]
}
```

### Dir
#### Modules
- Process 단위
- 서로 독립적
- 하나의 컨테이너에 매개변수를 입력받는 형태

###### Example
```groovy
process fastqc {
	container 'biocontainers/fastqc:0.11.9--hdfd78af_1'

	input:
	path reads
	
	output:
	path "*.html"
	
	script:
	"""
	fastqc ${reads}
	"""
```
#### Subworkflows
- 작업 (Workflow) 단위
- 서로 종속성을 가질 수 있다 

###### Example
```groovy
include { MEGAHIT              } from '../../../modules/nf-core/megahit/main'
include { SPADES as METASPADES } from '../../../modules/nf-core/spades/main'

workflow SHORTREAD_ASSEMBLY {
    take:
    ch_short_reads_grouped // [val(meta), path(fastq1), path(fastq2)] (mandatory)
    ch_short_reads_spades  // [val(meta), path(fastq1)]               (mandatory)

    main:
    ch_versions = channel.empty()
    ch_assembled_contigs = channel.empty()

    if (!params.single_end && !params.skip_spades) {
        METASPADES(ch_short_reads_spades.map { meta, reads -> [meta, reads, [], []] }, [], [])
        ch_spades_assemblies = METASPADES.out.scaffolds.map { meta, assembly ->
            def meta_new = meta + [assembler: 'SPAdes']
            [meta_new, assembly]
        }
        ch_versions = ch_versions.mix(METASPADES.out.versions)

        ch_assembled_contigs = ch_assembled_contigs.mix(ch_spades_assemblies)
    }

    if (!params.skip_megahit) {
        MEGAHIT(ch_short_reads_grouped)
        ch_megahit_assemblies = MEGAHIT.out.contigs.map { meta, assembly ->
            def meta_new = meta + [assembler: 'MEGAHIT']
            [meta_new, assembly]
        }
        ch_versions = ch_versions.mix(MEGAHIT.out.versions)

        ch_assembled_contigs = ch_assembled_contigs.mix(ch_megahit_assemblies)
    }

    emit:
    assembled_contigs = ch_assembled_contigs
    versions          = ch_versions
}
```

#### Workflows
- 모든 Subworflow를 Include 한 하나의 실행 파일


## 문법
## 명시적 변수
| 변수명              | 설명                                          |
| ---------------- | ------------------------------------------- |
| **`projectDir`** | 메인 스크립트(`main.nf`)가 위치한 루트 디렉토리 경로입니다.​     |
| **`launchDir`**  | `nextflow run` 명령어를 실행한 현재 작업 디렉토리 경로입니다. ​ |
| **`workDir`**    | 프로세스의 중간 결과물이 저장되는 `work/` 디렉토리의 절대 경로입니다.​ |
| **`baseDir`**    | `projectDir`과 동일하며, 이전 버전과의 호환성을 위해 제공됩니다.​ |
| **`moduleDir`**  | 모듈 파일이 위치한 디렉토리 경로입니다. (DSL2 모듈 내에서 유효)​    |

## Process

```groovy
process {Named/Implicit} {
publishDir "${params.outdir}/fastqc", mode: 'copy'
// task : Directives 설정 - base.config
label 'process_single'

input:
 val sample_id
 path "*.fasta.gz"
 tuple val(meta_id), path(paired_reads)
 each method_name
output:
 val result, emit:
 path "*.html", emit: report_html
 stdout emit: command_log

when:
!params.skip_analysis && sample_id != 'EMPTY'

script:
"""
fastqc ${sample_id}
"""
}
```

### Directives
- Label 을 지정하고 nextflow.config / base.config 에서 라벨별로 자원을 할당한다.
##### Input
- val : 입력 값을 변수로 사용
- path : 입력된 경로의 파일을 실행환경으로 가져와 처리
- tuple : 값과 파일을 하나로 묶어 복합 데이터를 처리할때 사용
- each : 채널의 모든 항목에 대해 프로세스 반복 실행
##### Output
- val : 프로세스 내 특정 값 출력
- path : 생성된 결과 파일을 출력, 와일드카드 지원
- emit : 출력 채널에 이름을 부여, Workflow 에서 명시적 참조 가능하게 한다
##### When
- 특정 조건이 참일때만 Process 실행
##### Execution Block
- ./bin 폴더에 Script 를 저장하고 호출 가능
## Def
- Workflow Scope : Channel 을 변수에 할당하거나 일시적 연산 결과 저장
- Function Def : Script 상단에 공통적으로 사용할 정의 함수 선언

```groovy
def topic_versions = channel.topic("versions")
	.distinct()
	.branch { entry ->
		versions_file: entry instanceof Path
		versions_tuple: true
}
```
```groovy
def myFunction() {  
	def x = 10
	return x * 2  
}
```


## Workflow
```groovy
workflow {Named/Implicit} {
take:
// - 입력 채널
ch_fasta
main:
/*
- Process 호출
- 데이터 로직
*/
emit:
// - 실행 결과
table = MultiQC.out.table
versions = ch_versions
}
```