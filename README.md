# Obsidian 포트폴리오

[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

[Obsidian](https://obsidian.md/)으로 쓴 노트를 그대로 발행하는 **개인 포트폴리오** 템플릿입니다.
GitHub에 push하면 GitHub Actions가 자동으로 빌드해 GitHub Pages에 배포합니다.

## 주요 기능
- **포트폴리오 구조** — 홈 · 소개 · 프로젝트 · 노트 · 블로그 폴더가 그대로 사이드바 섹션이 됩니다.
- **위키링크** — `[[노트 이름]]` 링크가 발행 후에도 동작합니다 (`mkdocs-roamlinks-plugin`).
- **콘텐츠 기능** — LaTeX 수식(MathJax), Mermaid 다이어그램, 형광펜·체크리스트 등 서식, 라이트/다크 모드, 전체 검색, 블로그, RSS.

## 빠른 시작

### 1. 로컬에서 미리보기

```bash
pip install mkdocs-material mkdocs-roamlinks-plugin mkdocs-rss-plugin
mkdocs serve          # http://127.0.0.1:8000
```

### 2. 콘텐츠 채우기

- `docs/about.md` — 소개
- `docs/projects/` — 프로젝트를 마크다운 파일로 추가
- `docs/notes/` — Obsidian 노트를 드래그 앤 드롭으로 추가
- `docs/blog/posts/` — 블로그 글 추가
- `mkdocs.yml` — `site_name`, `site_url` 수정


## 프로젝트 구조

```
docs/
├─ index.md            # 홈
├─ about.md            # 소개
├─ projects/           # 프로젝트
├─ notes/              # Obsidian 노트 (디지털 가든)
│  ├─ features/        #   문법 데모 (수식·다이어그램·서식·위키링크)
│  └─ examples/        #   위키링크 예시
├─ blog/posts/         # 블로그
└─ javascripts/        # MathJax 설정
mkdocs.yml             # 사이트 설정
.github/workflows/     # 자동 배포 CI
```

## 크레딧
[jobindjohn/obsidian-publish-mkdocs](https://github.com/jobindjohn/obsidian-publish-mkdocs) 템플릿 기반.
