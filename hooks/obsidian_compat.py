r"""MkDocs hook — Obsidian 마크다운을 Python-Markdown에 맞게 정규화.

Obsidian은 블록 요소($$ 수식, 표) 주위에 빈 줄을 요구하지 않지만,
Python-Markdown(및 pymdownx.arithmatex / tables 확장)은 빈 줄로 블록을
구분해야 한다. 또한 arithmatex 가 빌드 시 태깅하지 못한 수식은 MathJax
(`processHtmlClass: "arithmatex"`)가 끝내 렌더링하지 않으므로, 모든 `$$` 가
arithmatex 디스플레이 블록으로 인식되도록 보장하는 것이 무결성의 핵심이다.

이 hook은 빌드 시 마크다운을 받아 다음만 보정한다(수식 텍스트 내용은 변경하지
않음 — 빈 줄 삽입과 `$$` 블록 외곽 들여쓰기 제거만 수행):

  1. 디스플레이 수식 블록(여는 `$$` ~ 닫는 `$$`) 앞뒤에 빈 줄 보장.
     - 단독 `$$` 줄, 그리고 `$$\Sigma = ...`처럼 내용이 붙은 여는 `$$` 모두 처리.
  2. 한 줄짜리 단독 `$$ ... $$` 줄(그 줄 전체가 `$$...$$` 토큰)도 디스플레이
     블록으로 보장 — 앞뒤 빈 줄을 넣어 인라인이 아닌 중앙정렬 디스플레이로 렌더.
     줄에 다른 텍스트가 섞인 진짜 인라인 `$$...$$` 는 건드리지 않는다.
  3. 들여쓰기된 `$$` 블록(목록 항목 안 등) 디덴트. 4칸 이상 들여쓰기는
     Python-Markdown이 코드블록으로 처리해 수식이 깨지므로, 블록을 컬럼 0으로
     내려 arithmatex가 디스플레이 수식으로 인식하게 한다(내부 상대 들여쓰기 보존).
  4. 표(행이 `|` 로 시작)가 비-표 줄과 맞닿으면 그 사이에 빈 줄 삽입.

펜스 코드블록(``` / ~~~) 내부는 건드리지 않는다.
"""

import re

_FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
_TABLE_ROW = re.compile(r"^\s*\|")


def _dedent(line, width):
    """선두 공백을 최대 width 칸까지 제거(내부/이후 상대 들여쓰기는 보존)."""
    if width <= 0:
        return line
    n = 0
    while n < width and n < len(line) and line[n] == " ":
        n += 1
    return line[n:]


def on_page_markdown(markdown, **kwargs):
    lines = markdown.split("\n")
    out = []
    in_fence = False
    in_math = False
    in_table = False
    math_indent = 0

    def last_blank():
        return (not out) or out[-1].strip() == ""

    for i, line in enumerate(lines):
        # 펜스 코드블록: 원문 유지, 표 컨텍스트 종료
        if _FENCE.match(line):
            in_fence = not in_fence
            in_table = False
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        s = line.strip()

        # ---- 수식 블록 내부: 닫는 $$ 만 찾는다(여는 줄의 들여쓰기만큼 디덴트) ----
        if in_math:
            out.append(_dedent(line, math_indent))
            if s == "$$" or s.endswith("$$"):
                in_math = False
                nxt = lines[i + 1] if i + 1 < len(lines) else ""
                if i + 1 < len(lines) and nxt.strip() != "":
                    out.append("")
            continue

        is_blank = s == ""
        is_row = bool(_TABLE_ROW.match(line))

        # ---- 표 종료: 표 중간에 표 행도 빈 줄도 아닌 줄(예: ## 헤더)을 만나면 빈 줄 삽입 ----
        if in_table and not is_row and not is_blank:
            out.append("")
            in_table = False
        elif in_table and is_blank:
            in_table = False

        # ---- 디스플레이 수식 ----
        # 줄 전체가 한 줄짜리 $$...$$ 토큰이면 단독 디스플레이 → 앞뒤 빈 줄 보장
        standalone_single = (
            s.startswith("$$")
            and s.endswith("$$")
            and len(s) > 4
            and "$$" not in s[2:-2]
        )
        if standalone_single:
            indent = len(line) - len(line.lstrip())
            if not last_blank():
                out.append("")
            out.append(_dedent(line, indent))
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if i + 1 < len(lines) and nxt.strip() != "":
                out.append("")
            continue

        # 여러 줄 블록의 여는 구분자(단독 `$$` 또는 `$$\begin...`)
        if s.startswith("$$"):
            math_indent = len(line) - len(line.lstrip())
            if not last_blank():
                out.append("")
            out.append(_dedent(line, math_indent))
            in_math = True
            continue

        # ---- 표 시작: 앞 줄이 비어있지 않으면 빈 줄 삽입 ----
        if is_row and not in_table:
            if not last_blank():
                out.append("")
            in_table = True

        out.append(line)

    return "\n".join(out)
