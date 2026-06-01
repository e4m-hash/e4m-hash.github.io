r"""MkDocs hook — Obsidian 마크다운을 Python-Markdown에 맞게 정규화.

Obsidian은 블록 요소($$ 수식, 표) 주위에 빈 줄을 요구하지 않지만,
Python-Markdown(및 pymdownx.arithmatex / tables 확장)은 빈 줄로 블록을
구분해야 한다. 빈 줄이 없으면:

  * `$$ ... $$` 디스플레이 수식이 블록으로 인식되지 못해 원문 그대로 출력된다.
  * 표가 종료되지 않아 바로 뒤의 `##` 헤더 등이 표에 흡수된다.

이 hook은 빌드 시 마크다운을 받아 다음만 보정한다(원문 내용은 변경하지 않음):

  1. 디스플레이 수식 블록(여는 `$$` ~ 닫는 `$$`) 앞뒤에 빈 줄 보장.
     - 단독 `$$` 줄, 그리고 `$$\Sigma = ...`처럼 내용이 붙은 여는 `$$` 모두 처리.
     - 한 줄에 `$$ ... $$`가 모두 있는 인라인 디스플레이는 arithmatex 인라인이
       처리하므로 건드리지 않는다.
  2. 표(행이 `|` 로 시작)가 비-표 줄과 맞닿으면 그 사이에 빈 줄 삽입.

펜스 코드블록(``` / ~~~) 내부는 건드리지 않는다.
"""

import re

_FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
_TABLE_ROW = re.compile(r"^\s*\|")


def on_page_markdown(markdown, **kwargs):
    lines = markdown.split("\n")
    out = []
    in_fence = False
    in_math = False
    in_table = False

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

        # ---- 수식 블록 내부: 닫는 $$ 만 찾는다 ----
        if in_math:
            out.append(line)
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

        # ---- 디스플레이 수식 여는 구분자 ----
        # 한 줄에 $$...$$ 가 다 있으면(내용 포함) 인라인 → 그대로 둠
        single_line = s.startswith("$$") and s.endswith("$$") and len(s) > 3
        if s.startswith("$$") and not single_line:
            if not last_blank():
                out.append("")
            out.append(line)
            in_math = True
            continue

        # ---- 표 시작: 앞 줄이 비어있지 않으면 빈 줄 삽입 ----
        if is_row and not in_table:
            if not last_blank():
                out.append("")
            in_table = True

        out.append(line)

    return "\n".join(out)
