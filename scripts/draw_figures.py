#!/usr/bin/env python3
"""記事「AI駆動開発における生産性向上と、その裏側で増加するコストについて」の図版を決定論的に生成する。

体裁：幅1000px、最小フォント14px、注記16px、Python標準ライブラリのみ。
配色は役割で固定する（claudedocs/publication-plan.md §4.1）。
  NEUTRAL   従来の作業、人間の作業、区別を付けない基本要素
  PRIMARY   SUD（開発対象のシステム）とその成果物、開発フロー
  AI        ADS（SKILL・rules・ツール連携などAIによる開発を支える仕組み）とAIの生成
  POSITIVE  高速化・効果・再利用
  ATTENTION コスト・負債・制約・未検証（1図に1系統）
  INK       結論・題名の強調（色ではなく太字）
1図で使う色相は最大3（NEUTRALは数えない）、地の塗りは最大4種。文字と地色のコントラスト比は4.5以上。
数値を使う図は作らず、定性的な塗り分けと配置だけで示す。要素は2〜5個、矢印は1方向に限る。
"""
from __future__ import annotations
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'

# --- 中立 ---
BG = '#fcfdfd'; INK = '#18324b'; T1 = '#223e53'; T2 = '#36556d'; MUTED = '#55646d'
LINE = '#607a91'; STROKE = '#8ea6b2'; NEUTRAL = '#eef3f1'; WATER = '#d6e6f2'
# --- 役割色（地 / 線 / 文字） ---
PRIMARY = '#e1edf8'; PRI_TEXT = '#2b5f9e'
AI = '#e9e4f5'; AI_LINE = '#8a6cc1'; AI_TEXT = '#6a4ea6'
POSITIVE = '#e0f0e9'; POS_LINE = '#5aa06f'; POS_TEXT = '#2f6b45'
ATTENTION = '#f7e9d4'; ATT_LINE = '#c0604a'; ATT_TEXT = '#9c3f2a'

PALETTE = {BG, INK, T1, T2, MUTED, LINE, STROKE, NEUTRAL, WATER,
           PRIMARY, PRI_TEXT, AI, AI_LINE, AI_TEXT, POSITIVE, POS_LINE, POS_TEXT, ATTENTION, ATT_LINE, ATT_TEXT}
FONT = 'font-family="sans-serif"'
MIN_FONT = 14
NOTE_FONT = 16
CAPTION_MAX = 30  # キャプション（aria-label＝記事の alt）の最大文字数


def esc(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def est_w(s: str, size: float) -> float:
    """文字幅の保守的な概算。ASCIIは0.6em、それ以外（全角・矢印・記号）は1.0em。"""
    return sum(size * (0.6 if ord(c) < 0x80 else 1.0) for c in s)


def text(x, y, s, size=17, weight=400, fill=T2, anchor='middle', extra=''):
    size = max(size, MIN_FONT)
    w = f' font-weight="{weight}"' if weight != 400 else ''
    return f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" {FONT} font-size="{size:g}"{w} fill="{fill}"{extra}>{esc(s)}</text>'


def lines(x, y, rows, size=14, weight=400, fill=T2, anchor='middle', lh=None):
    """複数行テキスト。rows の各要素は文字列か (文字列, weight, fill) のタプル。"""
    lh = lh or size + 6
    out = []
    for i, r in enumerate(rows):
        if isinstance(r, tuple):
            s, wt, fl = r
        else:
            s, wt, fl = r, weight, fill
        if s:
            out.append(text(x, y + i * lh, s, size, wt, fl, anchor))
    return ''.join(out)


def title(s):
    """図の題名（結論文）。"""
    return text(50, 50, s, 24, 700, INK, 'start')


def rect(x, y, w, h, fill, stroke=STROKE, sw=1, rx=12, dashed=False):
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    return f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>'


def box(x, y, w, h, fill, head, sub=None, hs=20, ss=15, stroke=STROKE, sw=1, head_fill=T1):
    out = [rect(x, y, w, h, fill, stroke, sw)]
    cx = x + w / 2
    if sub:
        out.append(text(cx, y + h / 2 - 4, head, hs, 700, head_fill))
        out.append(text(cx, y + h / 2 + 20, sub, ss))
    else:
        out.append(text(cx, y + h / 2 + 7, head, hs, 700, head_fill))
    return ''.join(out)


def card(x, y, w, h, fill, head, rows, hs=18, rs=14, stroke=STROKE, sw=1, head_fill=T1, row_fill=T2, top=30, lh=22):
    """見出し＋複数行の箱。head は太字、rows は lines() の形式。"""
    return rect(x, y, w, h, fill, stroke, sw) + text(x + w / 2, y + top, head, hs, 700, head_fill) + lines(x + w / 2, y + top + 28, rows, rs, 400, row_fill, lh=lh)


def pill(x, y, w, h, s, fill=NEUTRAL, size=14, weight=400, color=T1, stroke=STROKE, sw=1):
    return rect(x, y, w, h, fill, stroke, sw, rx=h / 2) + text(x + w / 2, y + h / 2 + size * 0.36, s, size, weight, color)


def arrow(x1, y1, x2, y2, dashed=False, color=LINE, width=3):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    ex, ey = x2 - ux * 10, y2 - uy * 10
    nx, ny = -uy, ux
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    return (f'<path d="M{x1:.1f} {y1:.1f} L{ex:.1f} {ey:.1f}" stroke="{color}" stroke-width="{width}" fill="none"{dash}/>'
            f'<polygon points="{x2:.1f},{y2:.1f} {x2 - ux * 12 + nx * 7:.1f},{y2 - uy * 12 + ny * 7:.1f} {x2 - ux * 12 - nx * 7:.1f},{y2 - uy * 12 - ny * 7:.1f}" fill="{color}"/>')


def path_arrow(d, end, color=LINE, dashed=False, width=3):
    """任意の経路（d）の末尾に矢頭を付ける。end は (x, y, ux, uy)：矢頭の先端と向きの単位ベクトル。"""
    x, y, ux, uy = end; nx, ny = -uy, ux
    dash = ' stroke-dasharray="8 6"' if dashed else ''
    return (f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="none"{dash}/>'
            f'<polygon points="{x:.1f},{y:.1f} {x - ux * 12 + nx * 7:.1f},{y - uy * 12 + ny * 7:.1f} {x - ux * 12 - nx * 7:.1f},{y - uy * 12 - ny * 7:.1f}" fill="{color}"/>')


def bracket(x1, x2, y, label, color=LINE, size=15, weight=700, up=True, tick=12):
    """横方向のブラケット。up=True なら線の上にラベル。"""
    sgn = -1 if up else 1
    d = f'M{x1} {y + sgn * tick} V{y} H{x2} V{y + sgn * tick}'
    ly = y - tick - 10 if up else y + tick + size + 6
    return (f'<path d="{d}" stroke="{color}" stroke-width="2" fill="none"/>'
            + text((x1 + x2) / 2, ly, label, size, weight, color))


def note(y, s, size=NOTE_FONT):
    """図下部の注記。幅880pxを超える場合は句点（なければ中央付近の読点）で2行に折り返す。"""
    if est_w(s, size) <= 880:
        return text(500, y, s, size, 400, MUTED)
    cut = s.find('。')
    if not (0 < cut < len(s) - 1):
        cut = s.rfind('、', 0, len(s) // 2 + 6)
    parts = [s[:cut + 1], s[cut + 1:]]
    return lines(500, y, parts, size, 400, MUTED, lh=22)


def svg(w, h, caption, body, desc=''):
    """caption は図の主題を表す名詞句（全角30字以内、要素の列挙はしない）。記事の alt とキャプションになる。
    desc は図の内容の詳しい説明で、SVG を直接開いたときの支援技術向けに <desc> として残す。"""
    if len(caption) > CAPTION_MAX:
        raise ValueError(f'caption too long ({len(caption)} > {CAPTION_MAX}): {caption}')
    d = f'<desc id="desc">{esc(desc)}</desc>\n' if desc else ''
    aria = ' aria-describedby="desc"' if desc else ''
    content = '\n'.join(b for b in body if b)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(caption)}"{aria}>\n'
            f'{d}<rect width="100%" height="100%" fill="{BG}"/>\n' + content + '\n</svg>\n')


# =====================================================================


# =====================================================================
# 共通部品：工程の鎖（01・03・08 で同じ形を使う）と SUD・ADS の2箱（06 で使う）
# =====================================================================
PHASES = ['前工程：準備', '実装：生成', '後工程：理解・検証']


def chain(x0, y, labels, total_w=880, gap=12, h=38, size=15, fills=None, colors=None, strokes=None):
    """工程のピルを横一列に並べ、背後に左から右への1本の矢印を引く。戻り値は (svg, [(x, w), ...])。
    fills / colors / strokes は {添字: 色} で個々のピルの地・文字・枠を上書きする（既定は NEUTRAL / T1 / STROKE）。"""
    n = len(labels)
    pw = (total_w - gap * (n - 1)) / n
    cy = y + h / 2
    out = [arrow(x0 + pw / 2, cy, x0 + total_w + 22, cy)]
    cols = []
    for i, s in enumerate(labels):
        x = x0 + i * (pw + gap)
        out.append(pill(x, y, pw, h, s, (fills or {}).get(i, NEUTRAL), size, 700, (colors or {}).get(i, T1), (strokes or {}).get(i, STROKE)))
        cols.append((x, pw))
    return ''.join(out), cols


def sud_ads(y, h=100, x1=190, x2=650):
    """SUD（PRIMARY、左）と ADS（AI、右）の2箱。幅 280、間の 180px に矢印とラベルを置く。
    左に行ラベルを置く図は x1=190、置かない図は x1=130 にして図全体を中央に揃える。"""
    return (box(x1, y, 280, h, PRIMARY, 'SUD', '開発対象のシステム', 22, 15, LINE, 1, PRI_TEXT)
            + box(x2, y, 280, h, AI, 'ADS', 'SKILL・rules・手順＋TAS', 22, 15, AI_LINE, 1, AI_TEXT))


# =====================================================================
# §1 効果とコストが発生する工程
# =====================================================================
def fig_01_effect_and_cost_timeline():
    body = [title('効果とコストは、同じ案件の中で異なる工程・時期に発生する')]
    ch, cols = chain(150, 96, PHASES, total_w=800)
    body.append(ch)
    pw = cols[0][1]
    cx = [x + w / 2 for x, w in cols]
    body.append(text(60, 187, '効果', 15, 700, POS_TEXT, 'start'))
    body.append(box(cols[1][0], 150, pw, 64, POSITIVE, '作業の高速化', '個々の作業時間が短くなる', 17, 14, POS_LINE, 1, POS_TEXT))
    body.append(text(60, 277, 'コスト', 15, 700, ATT_TEXT, 'start'))
    body.append(card(cols[0][0], 230, pw, 84, ATTENTION, '準備コスト', ['SKILL・rules・手順の整備', '試行錯誤と評価'], hs=17, rs=14, stroke=ATT_LINE, head_fill=ATT_TEXT, top=28, lh=20))
    body.append(card(cols[2][0], 230, pw, 84, ATTENTION, '理解・検証のコスト', ['成果物間の整合性確認', '設計判断の背景確認、手戻り'], hs=17, rs=14, stroke=ATT_LINE, head_fill=ATT_TEXT, top=28, lh=20))
    body.append(text(cx[1], 277, '（この期間はコストが見えにくい）', 14, 400, MUTED))
    body.append(note(350, '効果が見える工程だけを評価すると、案件全体の生産性向上を過大評価する'))
    return svg(1000, 380, '効果とコストが発生する工程', body,
               desc='前工程：準備、実装：生成、後工程：理解・検証の3工程を左から右へ1本の矢印でつなぎ、効果のレーンには実装の列にだけ「作業の高速化（個々の作業時間が短くなる）」を置く。コストのレーンには前工程の列に「準備コスト（SKILL・rules・手順の整備、試行錯誤と評価）」、後工程の列に「理解・検証のコスト（成果物間の整合性確認、設計判断の背景確認、手戻り）」を置き、実装の列は「この期間はコストが見えにくい」と空けた図')


# =====================================================================
# §3 生産性評価の対象期間
# =====================================================================
def fig_03_evaluation_window():
    body = [title('評価対象は、高速化の効果が大きく現れる期間だけに限られている')]
    ch, cols = chain(60, 100, ['1〜3月', '4〜7月', '結合テスト以降'])
    pw = cols[0][1]
    cx = [x + w / 2 for x, w in cols]
    body.append(rect(cols[1][0] - 12, 86, pw + 24, 196, BG, POS_LINE, 2, dashed=True))
    body.append(ch)
    body.append(card(cols[0][0], 160, pw, 96, NEUTRAL, 'AI活用の準備', ['環境整備、試行錯誤', 'SKILL・rulesの整備'], hs=17, rs=14, top=30, lh=22))
    body.append(card(cols[1][0], 160, pw, 96, POSITIVE, 'AIによる作業の高速化', ['実装、テストコード作成', '（結合テスト前まで）'], hs=17, rs=14, stroke=POS_LINE, head_fill=POS_TEXT, top=30, lh=22))
    body.append(card(cols[2][0], 160, pw, 96, NEUTRAL, '整合性確認と手戻り', ['不具合調査、修正', '成果物間の整合性確認'], hs=17, rs=14, top=30, lh=22))
    body.append(text(cx[0], 304, '対象外', 15, 700, ATT_TEXT))
    body.append(text(cx[1], 304, '生産性評価の対象', 15, 700, POS_TEXT))
    body.append(text(cx[2], 304, '対象外', 15, 700, ATT_TEXT))
    body.append(note(346, '前工程の準備コストと、後工程の検証・手戻りコストの両方が集計の外にある'))
    return svg(1000, 376, '生産性評価の対象期間と対象外の工程', body,
               desc='1〜3月、4〜7月、結合テスト以降の3期間を左から右へ1本の矢印でつなぎ、それぞれの下に「AI活用の準備（環境整備、試行錯誤、SKILL・rulesの整備）」「AIによる作業の高速化（実装、テストコード作成。結合テスト前まで）」「整合性確認と手戻り（不具合調査、修正、成果物間の整合性確認）」の箱を置く。4〜7月の列だけを破線の枠で囲んで「生産性評価の対象」とし、両端の列を「対象外」とした図')


# =====================================================================
# §4.1 Issue と MR による開発レーンのヘルスチェック
# =====================================================================
def fig_04_issue_mr_health_check():
    body = [title('開発レーンの詰まりは、Issueの件数とMRの滞留に現れる')]
    body.append(bracket(80, 740, 108, '制約（TOC）が発生していないかのヘルスチェック', T2, 14, 700, up=True))
    body.append(card(80, 120, 240, 80, NEUTRAL, 'Issueの件数', ['積み上がっていないか'], hs=16, rs=14, top=30, lh=20))
    body.append(card(500, 120, 240, 80, NEUTRAL, 'MRの滞留', ['レビュー待ちが溜まっていないか'], hs=16, rs=14, top=30, lh=20))
    body.append(rect(60, 230, 880, 90, PRIMARY, LINE, 1))
    body.append(text(80, 256, '通常の開発レーン', 15, 700, PRI_TEXT, 'start'))
    body.append(arrow(170, 288, 905, 288))
    for x, s_ in ((80, 'Issue'), (290, '実装'), (500, 'MR（レビュー）'), (710, 'マージ')):
        body.append(pill(x, 270, 180, 36, s_, BG, 14, 700, T1, LINE))
    body.append(path_arrow('M200 200 V262', (200, 266, 0, 1), LINE, dashed=True, width=2))
    body.append(path_arrow('M620 200 V262', (620, 266, 0, 1), LINE, dashed=True, width=2))
    body.append(note(358, 'どこかが詰まれば件数と滞留に現れる。これは開発レーンの健全性を見る指標であり、成果物全体の品質保証の作業量は示さない'))
    return svg(1000, 400, 'IssueとMRによる開発レーンのヘルスチェック', body,
               desc='「通常の開発レーン」にIssue、実装、MR（レビュー）、マージを左から右へ並べ、Issueの上に「Issueの件数（積み上がっていないか）」、MRの上に「MRの滞留（レビュー待ちが溜まっていないか）」の箱を置いて破線で結び、2つの箱を「制約（TOC）が発生していないかのヘルスチェック」のブラケットで束ねた図')


# =====================================================================
# §4.2 計上されない統合・品質保証の繰り越し
# =====================================================================
def fig_04_uncounted_carry_over():
    body = [title('個々のタスクは順調でも、統合と品質保証の作業は計上されずに繰り越される')]
    cols = [(190, 'スプリント1'), (390, 'スプリント2'), (590, 'スプリント3')]
    for x, name in cols:
        body.append(pill(x, 96, 170, 32, name, BG, 14, 700, T1, STROKE))
        body.append(box(x, 145, 170, 60, PRIMARY, 'タスク', '順調に進む', 16, 14, LINE, 1, PRI_TEXT))
    body.append(pill(790, 96, 150, 32, 'リリーススプリント', BG, 14, 700, T1, STROKE))
    body.append(text(60, 180, '計上済み', 14, 700, T1, 'start'))
    body.append(text(60, 265, '未計上', 14, 700, ATT_TEXT, 'start'))
    body.append(rect(190, 230, 570, 60, BG, ATT_LINE, 2, dashed=True))
    body.append(lines(475, 256, [('統合して品質を保証する作業', 700, ATT_TEXT), ('タスクにもチームの必要工数にも入っていない', 400, T2)], 14, lh=18))
    body.append(arrow(760, 260, 790, 260, dashed=True, color=ATT_LINE, width=2))
    body.append(rect(790, 145, 150, 145, ATTENTION, ATT_LINE, 1))
    body.append(lines(865, 200, [('繰り越された', 700, ATT_TEXT), ('統合・品質保証の', 700, ATT_TEXT), ('作業が集中する', 700, ATT_TEXT)], 14, lh=20))
    body.append(text(475, 330, '順調なタスクの合計が必要工数に見えるが、将来の負荷はその外にある', 15, 700, T1))
    body.append(note(372, '繰り越しは開発が進むほど増え、リリーススプリントで想定を上回る人的コストとして現れる'))
    return svg(1000, 400, '計上されない統合・品質保証の繰り越し', body,
               desc='スプリント1〜3の各列で「タスク（順調に進む）」の箱を「計上済み」の行に置き、その下の「未計上」の行に「統合して品質を保証する作業（タスクにもチームの必要工数にも入っていない）」の破線枠を3列にまたがって置く。破線枠から右のリリーススプリントの列へ矢印が向かい、「繰り越された統合・品質保証の作業が集中する」とした図')


# =====================================================================
# §4.2 開発レーンの健全性と品質保証の作業量
# =====================================================================
def fig_04_flow_health_vs_qa_load():
    body = [title('タスクの進捗が健全でも、品質保証に必要な作業量は別に増えていく')]
    body.append(rect(60, 90, 880, 116, PRIMARY, LINE, 1))
    body.append(text(80, 116, '通常の開発レーン：IssueやMRの滞留を監視する', 15, 700, PRI_TEXT, 'start'))
    body.append(arrow(140, 158, 735, 158))
    for i, s in enumerate(['タスクA', 'タスクB', 'タスクC', 'タスクD']):
        body.append(pill(80 + i * 160, 140, 140, 36, s, BG, 14, 700, T1, LINE))
    body.append(pill(760, 140, 160, 36, '滞留なし・順調', POSITIVE, 14, 700, POS_TEXT, POS_LINE))
    body.append(arrow(500, 206, 500, 268, dashed=True, color=ATT_LINE, width=2))
    body.append(text(520, 243, '統合して品質を保証する作業は、まだタスク化されずに繰り越される', 14, 700, ATT_TEXT, 'start'))
    body.append(rect(60, 270, 880, 130, ATTENTION, ATT_LINE, 1))
    body.append(text(80, 296, 'リリーススプリント：成果物を横断した品質保証', 15, 700, ATT_TEXT, 'start'))
    for i, s in enumerate(['整合性確認', '依存関係の把握', '変更影響の分析', '回帰テスト', '不具合調査']):
        body.append(pill(80 + i * 170, 318, 160, 36, s, BG, 14, 700, ATT_TEXT, ATT_LINE))
    body.append(text(500, 384, '必要な作業量は事前に見積もりにくく、開発の進行とともに増える', 14, 400, T2))
    body.append(note(438, 'IssueやMRの滞留だけでは、まだタスク化されていない整合性確認や理解負債は見えない'))
    return svg(1000, 466, '開発レーンの健全性と品質保証の作業量', body,
               desc='上段の「通常の開発レーン：IssueやMRの滞留を監視する」ではタスクA〜Dが左から右へ順調に流れ、右端に「滞留なし・順調」とある。そこから下段へ「統合して品質を保証する作業は、まだタスク化されずに繰り越される」という破線の矢印が下り、下段の「リリーススプリント：成果物を横断した品質保証」には整合性確認、依存関係の把握、変更影響の分析、回帰テスト、不具合調査が並び、「必要な作業量は事前に見積もりにくく、開発の進行とともに増える」とした図')


# =====================================================================
# §6 テスト自動化と AI 駆動開発の保守対象
# =====================================================================
def fig_06_sut_and_tas():
    body = [title('テスト自動化は、SUTとは別にTASという保守対象を生む')]
    body.append(box(130, 100, 280, 100, NEUTRAL, 'SUT', 'テスト対象のシステム', 22, 15, STROKE, 1, T1))
    body.append(box(590, 100, 280, 100, NEUTRAL, 'TAS', 'テストを自動実行・制御するシステム', 22, 15, STROKE, 1, T1))
    body.append(arrow(410, 150, 590, 150))
    body.append(text(500, 136, '変更に合わせて保守する', 14, 700, T2))
    body.append(text(500, 246, 'SUTが変われば、テストスクリプト・実行環境・データ・検証手順も変わる', 14, 700, T2))
    body.append(note(296, '手動テストの削減は、TASの構築・保守という新しい負担と交換されている'))
    return svg(1000, 326, 'SUTとTASの関係', body,
               desc='左に「SUT（テスト対象のシステム）」、右に「TAS（テストを自動実行・制御するシステム）」を置き、「変更に合わせて保守する」矢印で結ぶ。下に「SUTが変われば、テストスクリプト・実行環境・データ・検証手順も変わる」と記した図')


def fig_06_sud_and_ads():
    body = [title('AI駆動開発では、SUDとADSの両方を保守し、ADSはTASを内包する')]
    body.append(box(130, 121, 280, 100, PRIMARY, 'SUD', '開発対象のシステム', 22, 15, LINE, 1, PRI_TEXT))
    body.append(rect(590, 96, 280, 150, AI, AI_LINE, 1))
    body.append(text(730, 124, 'ADS', 22, 700, AI_TEXT))
    body.append(rect(605, 136, 250, 46, BG, AI_LINE, 1, rx=8))
    body.append(lines(730, 155, [('生成の仕組み', 700, AI_TEXT), ('SKILL・rules・手順', 400, T2)], 14, lh=18))
    body.append(rect(605, 190, 250, 46, BG, AI_LINE, 1, rx=8))
    body.append(lines(730, 209, [('検証の仕組み（TAS）', 700, AI_TEXT), ('実行基盤・テストデータ・接続', 400, T2)], 14, lh=18))
    body.append(arrow(410, 171, 590, 171))
    body.append(lines(500, 143, ['変化に合わせて', '両方を保守する'], 14, 700, T2, lh=18))
    body.append(bracket(130, 870, 262, '保守する対象が二重になり、ADSはTASを内包する', ATT_TEXT, 15, 700, up=False))
    body.append(note(334, 'SUDの変化はADSの生成と検証の両方の修正を要求し、ADSの変化はSUDの再検証を要求する'))
    return svg(1000, 364, 'AI駆動開発の保守対象', body,
               desc='左に「SUD（開発対象のシステム）」、右に「ADS」を置き、「変化に合わせて両方を保守する」矢印で結ぶ。ADSの箱は「生成の仕組み（SKILL・rules・手順）」と「検証の仕組み（TAS：実行基盤・テストデータ・接続）」の2区画に分かれ、2箱をブラケットで束ねて「保守する対象が二重になり、ADSはTASを内包する」とした図')


# =====================================================================
# §6 SUD と ADS の定義
# =====================================================================
def fig_06_sud_ads_definition():
    body = [title('開発対象のSUDと、生成と検証の仕組みからなるADS')]
    body.append(rect(60, 90, 420, 230, PRIMARY, LINE, 1))
    body.append(text(270, 150, 'SUD', 22, 700, PRI_TEXT))
    body.append(text(270, 176, 'System Under Development', 14, 400, T2))
    body.append(text(270, 206, '開発対象のシステム', 15, 700, T1))
    body.append(text(270, 246, 'ADSが生成し、動かし、確かめる対象', 14, 400, MUTED))
    body.append(rect(520, 90, 420, 230, AI, AI_LINE, 1))
    body.append(text(730, 118, 'ADS', 22, 700, AI_TEXT))
    body.append(text(730, 140, 'AI-driven Development System', 14, 400, T2))
    body.append(rect(540, 154, 380, 68, BG, AI_LINE, 1, rx=8))
    body.append(lines(730, 180, [('生成の仕組み', 700, AI_TEXT), ('SKILL・rules・入力ファイル・ツール連携・開発手順', 400, T1)], 14, lh=20))
    body.append(rect(540, 236, 380, 68, BG, AI_LINE, 1, rx=8))
    body.append(lines(730, 258, [('検証の仕組み（TAS）', 700, AI_TEXT), ('テスト実行基盤・テストデータ・結果取得', 400, T1), ('AIと対象環境の接続', 400, T1)], 14, lh=20))
    body.append(note(358, 'SUD・ADSは本稿での説明用の仮称。SUTとSUDは、同じシステムをテスト対象と開発対象のどちらから見るかの違い'))
    return svg(1000, 388, 'SUDとADSの定義', body,
               desc='左に「SUD（System Under Development）：開発対象のシステム。ADSが生成し、動かし、確かめる対象」、右に「ADS（AI-driven Development System）」を置き、ADSの中を「生成の仕組み（SKILL・rules・入力ファイル・ツール連携・開発手順）」と「検証の仕組み（TAS：テスト実行基盤・テストデータ・結果取得、AIと対象環境の接続）」の2区画で示した図')


# =====================================================================
# §6 AI と CI・テスト環境の接続（参考記事の図 07c に倣う）
# =====================================================================
def fig_06_ai_ci_test_env():
    body = [title('AIがCIとテスト環境につながって初めて、生成した成果物を動かし、確かめられる')]
    body.append(box(60, 150, 140, 80, NEUTRAL, 'CI', '定期実行・起動', 17, 14))
    body.append(arrow(200, 190, 320, 190, width=2))
    body.append(text(260, 174, 'CIとAIの接続', 14, 700, T1))
    body.append(rect(320, 130, 240, 120, AI, AI_LINE, 2))
    body.append(lines(440, 170, [('AIエージェント', 700, AI_TEXT), ('生成・実行・修復を担う', 400, T2), ('ADSの中核', 400, T2)], 15, lh=22))
    body.append(rect(640, 90, 300, 240, PRIMARY, LINE, 2))
    body.append(text(790, 118, 'テスト環境', 17, 700, PRI_TEXT))
    body.append(rect(660, 136, 260, 70, BG, STROKE, 1))
    body.append(lines(790, 162, [('ブラウザ・対象環境（SUD）', 700, T1), ('操作してSUDを動かせること', 400, T2)], 14, lh=20))
    body.append(rect(660, 236, 260, 70, BG, STROKE, 1))
    body.append(lines(790, 262, [('DB・バッチの実行結果', 700, T1), ('結果を確かめられること', 400, T2)], 14, lh=20))
    body.append(arrow(560, 170, 660, 171, width=2))
    body.append(text(610, 156, '動かす', 14, 700, T1))
    body.append(arrow(560, 210, 660, 271, width=2))
    body.append(text(596, 250, '確かめる', 14, 700, T1))
    body.append(rect(60, 350, 880, 56, BG, ATT_LINE, 2, dashed=True))
    body.append(lines(500, 373, [('この接続の構築と維持がTASの領域であり、ADSの一部', 700, ATT_TEXT), ('どれかが欠けると、AIは成果物を動かすことも、結果を確かめることもできない', 400, T2)], 14, lh=19))
    body.append(note(450, 'SKILLやrulesを整えるだけでは足りない。AIがCIとテスト環境につながる接続が、ADSの継続運用の要になる'))
    return svg(1000, 476, 'AIとCI・テスト環境の接続', body,
               desc='中央のAIエージェント（生成・実行・修復を担う、ADSの中核）に対して、左からCI（定期実行・起動）との接続、右へテスト環境との接続（SUDを動かすためのブラウザ・対象環境、結果を確かめるためのDB・バッチの実行結果）を描き、下段にこの接続の構築と維持がTASの領域でありADSの一部であることを示した図')


# =====================================================================
# §6 ADS の構築・保守で発生する作業
# =====================================================================
def fig_06b_ads_maintenance_work():
    body = [title('ADSの保守は、SUDの機能開発ではないが、AI駆動開発を続けるために必要な作業')]
    body.append(rect(130, 90, 740, 44, PRIMARY, LINE, 1))
    body.append(text(500, 118, 'SUDの機能開発：成果物を直接作る作業（見積もりに入っている）', 15, 700, PRI_TEXT))
    body.append(rect(130, 156, 740, 230, AI, AI_LINE, 1))
    body.append(text(500, 182, 'ADSの構築・保守：開発を続けるために必要な作業', 15, 700, AI_TEXT))
    body.append(rect(150, 196, 350, 176, BG, AI_LINE, 1, rx=8))
    body.append(text(325, 220, '生成の仕組み', 15, 700, AI_TEXT))
    body.append(lines(325, 246, ['構成変更に合わせてSKILLを修正', '品質問題に応じてrulesを見直す', '入力ファイルの形式・構成を変更', 'モデル・ツール変更に合わせ手順を更新', 'ADS変更後の生成結果の劣化を検証'], 14, 400, T1, lh=22))
    body.append(rect(520, 196, 330, 176, BG, AI_LINE, 1, rx=8))
    body.append(text(685, 220, '検証の仕組み（TAS）', 15, 700, AI_TEXT))
    body.append(lines(685, 246, ['SUDの変更に合わせテストを修正', 'Runner・ブラウザ・ライブラリ・データの維持', 'AIがSUDを動かし結果を確かめる接続の維持'], 14, 400, T1, lh=22))
    body.append(text(500, 416, 'このコストはまだ十分に見積もれておらず、当初の想定より大きい可能性がある', 15, 700, ATT_TEXT))
    body.append(note(456, 'SUDが変わるたびに、生成の仕組みと検証の仕組みの両方に追従作業が発生する'))
    return svg(1000, 486, 'ADSの構築・保守で発生する作業', body,
               desc='上に「SUDの機能開発：成果物を直接作る作業（見積もりに入っている）」の帯、その下に「ADSの構築・保守：開発を続けるために必要な作業」の枠を置く。枠の中は左「生成の仕組み」（構成変更に合わせてSKILLを修正、品質問題に応じてrulesを見直す、入力ファイルの形式・構成を変更、モデル・ツール変更に合わせ手順を更新、ADS変更後の生成結果の劣化を検証）と右「検証の仕組み（TAS）」（SUDの変更に合わせテストを修正、Runner・ブラウザ・ライブラリ・データの維持、AIがSUDを動かし結果を確かめる接続の維持）に分かれ、下に「このコストはまだ十分に見積もれておらず、当初の想定より大きい可能性がある」と記した図')


# =====================================================================
# §6.1 AI が下げる費目と残る費目
# =====================================================================
def fig_06a_ads_cost_items():
    body = [title('AIが下げるのは作成の費目で、基盤・接続・運用の費目は残る')]
    body.append(pill(190, 90, 300, 34, 'AIが下げる費目', POSITIVE, 15, 700, POS_TEXT, POS_LINE))
    body.append(pill(520, 90, 420, 34, '残る費目', ATTENTION, 15, 700, ATT_TEXT, ATT_LINE))
    rows = [('TAS', 'テスト自動化', 140, ['テスト設計・実装', 'テスト修復'],
             ['実行基盤の構築', 'Runner・ブラウザ・データの維持', 'AIと環境の接続', '定期実行・障害対応、利用料']),
            ('ADS', 'AI駆動開発', 270, ['SKILL・rules・手順の作成', '生成結果の修正'],
             ['実行環境と接続の構築', 'モデル・ツール変更への追従', '生成・検証の運用と監視', '利用料'])]
    for head, sub, y, left, right in rows:
        body.append(lines(60, y + 52, [(head, 700, T1), (sub, 400, T2)], 15, anchor='start', lh=20))
        body.append(rect(190, y, 300, 110, NEUTRAL))
        body.append(lines(340, y + 60 - (len(left) - 1) * 11, left, 14, 400, T1, lh=22))
        body.append(rect(520, y, 420, 110, NEUTRAL))
        body.append(lines(730, y + 60 - (len(right) - 1) * 11, right, 14, 400, T1, lh=22))
    body.append(note(420, '費目の構造は同じで、AIが減らすのは左の列だけ。右の列を共通基盤に寄せられるかで案件の負担が変わる'))
    return svg(1000, 450, 'AIが下げる費目と残る費目', body,
               desc='「AIが下げる費目」と「残る費目」の2列に、TAS（テスト自動化）の行とADS（AI駆動開発）の行を並べる。TASの行は、下げる費目がテスト設計・実装とテスト修復、残る費目が実行基盤の構築、Runner・ブラウザ・データの維持、AIと環境の接続、定期実行・障害対応、利用料。ADSの行は、下げる費目がSKILL・rules・手順の作成と生成結果の修正、残る費目が実行環境と接続の構築、モデル・ツール変更への追従、生成・検証の運用と監視、利用料とした図')


# =====================================================================
# §6.1 CI/CD 成熟度と ADS の運用負荷（参考記事の図 07b に倣う）
# =====================================================================
def fig_06c_cicd_maturity():
    body = [title('CI/CD成熟度が低いと、生成を速くしてもADSの運用負荷は下がらない')]
    body.append(text(60, 92, 'CI/CD成熟度が低い組織の状態', 14, 700, MUTED, 'start'))
    for i, s_ in enumerate(['案件ごとにRunnerを立てる', '標準構成がない', 'パイプラインの失敗を診断できる人が限られる']):
        y = 108 + i * 64
        body.append(pill(60, y, 380, 40, s_, NEUTRAL, 14, 400, T1))
        body.append(arrow(440, y + 20, 520, 196, width=2))
    body.append(rect(520, 100, 420, 192, ATTENTION, ATT_LINE, 2))
    body.append(lines(730, 134, [('ADSの構築・保守コストは', 700, ATT_TEXT), ('案件ごとに高いまま', 700, ATT_TEXT)], 16, lh=22))
    body.append(lines(540, 192, ['・実行環境と接続の構築が案件ごとに発生する', '・設定の整備と更新を各案件が抱える', '・失敗時の切り分けが特定の人に集中する'], 14, anchor='start', lh=24))
    body.append(rect(520, 330, 280, 56, AI, AI_LINE, 2))
    body.append(lines(660, 352, [('SKILL・テストコードの生成', 700, AI_TEXT), ('AIエージェントで容易になった', 400, T2)], 14, lh=19))
    body.append(path_arrow('M660 330 V300', (660, 298, 0, -1), color=AI_LINE, dashed=True, width=2))
    body.append(text(816, 362, '下げるのは作成部分だけ', 14, 700, T1, 'start'))
    body.append(note(438, '共通の実行基盤・標準設定・運用手順・障害対応体制が整って初めて、残る費目を共通基盤に寄せられる'))
    return svg(1000, 464, 'CI/CD成熟度とADSの運用負荷', body,
               desc='案件ごとにRunnerを立てる、標準構成がない、パイプラインの失敗を診断できる人が限られる、という3つの状態からADSの構築・保守コストが案件ごとに高いままになること（実行環境と接続の構築が案件ごとに発生する、設定の整備と更新を各案件が抱える、失敗時の切り分けが特定の人に集中する）を示し、SKILL・テストコードの生成がAIで容易になっても下げるのは作成部分だけであることを添えた図')


# =====================================================================
# §7 3種類のコストの連鎖
# =====================================================================
def fig_07_three_costs_cycle():
    body = [title('3種類のコストは独立ではなく、連鎖する')]
    body.append(card(365, 90, 270, 90, AI, 'ADSの構築・保守コスト', ['SKILL・rules・手順の整備、', 'TASの構築・運用'], hs=17, rs=14, stroke=AI_LINE, head_fill=AI_TEXT, top=28, lh=20))
    body.append(card(670, 270, 270, 90, ATTENTION, 'SUDの理解負債に伴うコスト', ['設計意図の復元、依存関係の調査、', '変更影響の分析'], hs=17, rs=14, stroke=ATT_LINE, head_fill=ATT_TEXT, top=28, lh=20))
    body.append(card(60, 270, 270, 90, ATTENTION, '横断的な品質保証コスト', ['成果物間の整合性確認、', '回帰テスト、不具合調査'], hs=17, rs=14, stroke=ATT_LINE, head_fill=ATT_TEXT, top=28, lh=20))
    body.append(arrow(600, 180, 805, 270))
    body.append(lines(850, 196, ['ADSの品質が不十分だと', '理解負債が蓄積しやすい'], 14, 700, T2, lh=18))
    body.append(arrow(670, 315, 330, 315))
    body.append(text(500, 300, '理解負債が増えると、品質保証コストが増える', 14, 700, T2))
    body.append(arrow(195, 270, 365, 150, dashed=True))
    body.append(lines(150, 196, ['問題の解決には', 'ADSの修正が必要になる'], 14, 700, T2, lh=18))
    body.append(text(500, 254, '開発対象と開発する仕組みの両方を継続的に進化させる', 15, 700, T1))
    body.append(note(408, 'ADSを整備すればSUDの理解負債が自動的に解消されるわけではない。両者の品質をそれぞれ管理する'))
    return svg(1000, 440, '3種類のコストの連鎖', body,
               desc='上に「ADSの構築・保守コスト（SKILL・rules・ツール連携・開発手順の整備と更新）」、右下に「SUDの理解負債に伴うコスト（設計意図の復元、依存関係の調査、変更影響の分析）」、左下に「横断的な品質保証コスト（成果物間の整合性確認、回帰テスト、不具合調査）」を置き、「ADSの品質が不十分だと理解負債が蓄積しやすい」「理解負債が増えると、品質保証コストが増える」の矢印で順につなぎ、左下から上へ「問題の解決にはADSの修正が必要になる」という破線の矢印で戻る循環を示し、中央に「開発対象と開発する仕組みの両方を継続的に進化させる」と記した図')


# =====================================================================
# §8 工程間での制約の移動
# =====================================================================
def fig_08_constraint_shift():
    body = [title('実装の制約が解消されると、制約は統合・品質保証・リリースへ移動する')]
    body.append(text(60, 131, '従来', 15, 700, T1, 'start'))
    ch1, cols1 = chain(180, 106, ['設計', '実装（制約）', '統合', '品質保証', 'リリース'], total_w=760,
                       fills={1: ATTENTION}, colors={1: ATT_TEXT}, strokes={1: ATT_LINE})
    body.append(ch1)
    body.append(text(60, 251, 'AI駆動開発', 15, 700, T1, 'start'))
    att = {2: ATTENTION, 3: ATTENTION, 4: ATTENTION}
    ch2, cols2 = chain(180, 226, ['設計', '実装（高速化）', '統合（制約）', '品質保証（制約）', 'リリース（制約）'], total_w=760,
                       fills={1: POSITIVE, **att}, colors={1: POS_TEXT, 2: ATT_TEXT, 3: ATT_TEXT, 4: ATT_TEXT}, strokes={1: POS_LINE, 2: ATT_LINE, 3: ATT_LINE, 4: ATT_LINE})
    body.append(ch2)
    x_impl = cols1[1][0] + cols1[1][1] / 2
    x_qa = cols2[3][0] + cols2[3][1] / 2
    body.append(arrow(x_impl, 146, x_qa, 224, dashed=True, color=ATT_LINE, width=2))
    body.append(text(520, 170, '制約が移動する', 14, 700, ATT_TEXT, 'start'))
    body.append(bracket(cols2[2][0], cols2[4][0] + cols2[4][1], 280, '後続工程の処理能力を超えた生成は、未検証の成果物と整合性問題を蓄積する', ATT_TEXT, 14, 700, up=False))
    body.append(note(352, '生成量を増やすことが、必ずしも案件全体の生産性向上につながらない'))
    return svg(1000, 380, '工程間での制約の移動', body,
               desc='設計、実装、統合、品質保証、リリースの5工程を左から右へ1本の矢印でつないだ鎖を上下2段に並べる。上段「従来」では実装が制約、下段「AI駆動開発」では実装が高速化され、統合・品質保証・リリースが制約になる。上段の実装から下段の品質保証へ「制約が移動する」破線の矢印を引き、下段の統合〜リリースをブラケットで束ねて「後続工程の処理能力を超えた生成は、未検証の成果物と整合性問題を蓄積する」とした図')


# =====================================================================
# §2.3 準備コストと理解負債の変化
# =====================================================================
def fig_02_two_costs():
    body = [title('準備コストは再利用で小さくなり、理解負債は成果物の関係で増幅する')]
    # 左：案件を重ねるほど準備コストが下がる
    body.append(rect(60, 90, 420, 230, NEUTRAL))
    body.append(text(270, 116, '前工程の準備コスト：案件を重ねるほど小さくできる', 15, 700, T1))
    for i, h in enumerate((120, 90, 65)):
        x = 90 + i * 130
        body.append(rect(x, 290 - h, 90, h, ATTENTION, ATT_LINE, 1, rx=6))
        body.append(text(x + 45, 290 - h / 2 + 5, '準備コスト', 14, 700, ATT_TEXT))
        body.append(text(x + 45, 312, f'案件{i + 1}', 14, 400, T2))
    body.append(arrow(135, 160, 395, 218, dashed=True, color=POS_LINE, width=2))
    body.append(text(265, 150, 'SKILL・手順の再利用で低減', 14, 700, POS_TEXT))
    # 右：成果物とその関係が増えるほど理解負債が増幅する
    body.append(rect(520, 90, 420, 230, NEUTRAL))
    body.append(text(730, 116, '後工程の理解負債：成果物の関係で増幅する', 15, 700, T1))
    small = [(560, 170), (560, 230)]
    many = [(700, 150), (820, 150), (760, 200), (700, 250), (820, 250)]
    body.append(f'<path d="M595 200 V230" stroke="{ATT_LINE}" stroke-width="2" fill="none"/>')
    for i, (x1, y1) in enumerate(many):
        for x2, y2 in many[i + 1:]:
            body.append(f'<path d="M{x1 + 35} {y1 + 15} L{x2 + 35} {y2 + 15}" stroke="{ATT_LINE}" stroke-width="2" fill="none"/>')
    for x, y in small + many:
        body.append(rect(x, y, 70, 30, PRIMARY, LINE, 1, rx=6))
        body.append(text(x + 35, y + 20, '成果物', 14, 700, PRI_TEXT))
    body.append(arrow(640, 215, 690, 215))
    body.append(text(730, 312, '関係が増えるほど、どこに問題があるかの把握が難しくなる', 14, 400, T2))
    body.append(note(358, '標準化で下げられるのは準備コストの側であり、放置すると増幅するのは理解負債の側である'))
    return svg(1000, 388, '準備コストと理解負債の変化', body,
               desc='左の「前工程の準備コスト：案件を重ねるほど小さくできる」では、案件1・案件2・案件3の準備コストの箱が順に低くなり、「SKILL・手順の再利用で低減」の破線矢印が添えてある。右の「後工程の理解負債：成果物の関係で増幅する」では、成果物2つが1本の線でつながる状態から、成果物5つが互いに線でつながる状態へ矢印が向かい、「関係が増えるほど、どこに問題があるかの把握が難しくなる」とした図')


# =====================================================================
# §9 4つの方向性が効く場所
# =====================================================================
def fig_09_directions():
    body = [title('4つの方向性は、SUD・ADS・その間・案件間のどこに効くかで整理できる')]
    body.append(card(130, 90, 280, 70, NEUTRAL, '成果物と設計判断を結び付ける', ['追跡・検証できる状態にする'], hs=15, rs=14, top=26, lh=20))
    body.append(card(590, 90, 280, 70, NEUTRAL, 'ADSに品質保証を組み込む', ['TASによる回帰テストと整合性チェック'], hs=15, rs=14, top=26, lh=20))
    body.append(arrow(270, 160, 270, 196, width=2))
    body.append(arrow(730, 160, 730, 196, width=2))
    body.append(sud_ads(200, x1=130, x2=590))
    body.append(arrow(410, 250, 590, 250))
    body.append(text(500, 236, '変化に合わせて保守', 14, 700, T2))
    body.append(card(130, 340, 280, 70, NEUTRAL, '品質保証の作業量を可視化する', ['SUDとADSの間で増える作業を観測する'], hs=15, rs=14, top=26, lh=20))
    body.append(path_arrow('M270 340 V322 H500 V266', (500, 262, 0, -1), LINE, dashed=True, width=2))
    body.append(card(590, 340, 280, 70, NEUTRAL, '改善を案件間で再利用する', ['TAS・CI/CDの共通基盤と運用チーム'], hs=15, rs=14, top=26, lh=20))
    body.append(arrow(730, 300, 730, 336, width=2))
    body.append(note(450, 'いずれも、理解負債を後工程でまとめて返済する運営からの転換を目指す'))
    return svg(1000, 480, '4つの方向性が効く場所', body,
               desc='中央に「SUD（開発対象のシステム）」と「ADS（SKILL・rules・手順＋TAS）」の2箱を置き、SUDの上から「成果物と設計判断を結び付ける（追跡・検証できる状態にする）」、ADSの上から「ADSに品質保証を組み込む（TASによる回帰テストと整合性チェック）」が矢印で各箱に向かう。SUDの下の「品質保証の作業量を可視化する（SUDとADSの間で増える作業を観測する）」は破線で2箱の間の矢印を指し、ADSの下の「改善を案件間で再利用する（TAS・CI/CDの共通基盤と運用チーム）」へはADSから矢印が出る図')


# =====================================================================
# §2.2 理解負債の定義
# =====================================================================
def fig_02a_understanding_debt():
    body = [title('生成は速く、理解・検証は遅い。その差は時間とともに積み上がる')]
    body.append(f'<polygon points="120,300 900,90 900,230" fill="{ATTENTION}"/>')
    body.append(f'<path d="M120 300 L900 90" stroke="{AI_LINE}" stroke-width="4" fill="none"/>')
    body.append(f'<path d="M120 300 L900 230" stroke="{LINE}" stroke-width="4" fill="none"/>')
    body.append(arrow(120, 300, 940, 300, color=STROKE, width=2))
    body.append(arrow(120, 300, 120, 94, color=STROKE, width=2))
    body.append(text(120, 84, '成果物の量', 14, 400, MUTED))
    body.append(text(530, 324, '開発の進行', 14, 400, MUTED))
    body.append(text(520, 150, '生成された成果物（AI）', 15, 700, AI_TEXT))
    body.append(text(600, 286, '理解・検証が済んだ成果物（人間）', 15, 700, T1))
    body.append(text(780, 190, '理解負債', 18, 700, ATT_TEXT))
    body.append(text(780, 210, '未理解・未検証の成果物の蓄積', 14, 400, ATT_TEXT))
    body.append(note(362, '生成が速いほど、理解・検証が追いつかない成果物が増える。この差が後工程のコストになる'))
    return svg(1000, 392, '生成と理解・検証の差の蓄積', body,
               desc='横軸を開発の進行、縦軸を成果物の量として、原点から「生成された成果物（AI）」の線が急な傾きで、「理解・検証が済んだ成果物（人間）」の線が緩い傾きで伸びる。2本の線の間の開きが時間とともに広がり、その領域を塗って「理解負債：未理解・未検証の成果物の蓄積」と記した図')


# =====================================================================
# §5 従来の保守開発と AI 駆動開発での顕在化の速さ
# =====================================================================
def fig_05_gradual_vs_compressed():
    body = [title('従来は徐々に顕在化していた問題が、AI駆動開発では短い期間に集中する')]
    panels = [(60, '従来の保守開発：徐々に顕在化', [85, 155, 225, 295, 365], 60, 230, '時間（数年）', '変更影響の調査・回帰テストの範囲が、年単位で広がる'),
              (520, 'AI駆動開発：短い期間に集中', [545, 603, 661, 719, 777], 56, 180, '時間（数か月）', '同じ範囲の広がりが、短い期間に集中して現れる')]
    for px, head, xs, w, wedge_top, unit, caption in panels:
        body.append(rect(px, 90, 420, 250, NEUTRAL))
        body.append(text(px + 210, 116, head, 15, 700, T1))
        last = xs[-1] + w
        body.append(f'<polygon points="{xs[0]},262 {last + 10},262 {last + 10},{wedge_top}" fill="{ATTENTION}"/>')
        for x in xs:
            body.append(rect(x, 150, w, 30, PRIMARY, LINE, 1, rx=6))
            body.append(text(x + w / 2, 170, '成果物', 14, 700, PRI_TEXT))
        body.append(arrow(px + 20, 270, px + 400, 270))
        body.append(text(px + 400, 292, unit, 14, 400, MUTED, 'end'))
        body.append(text(px + 210, 320, caption, 14, 700, ATT_TEXT))
    body.append(note(376, '従来の見積もり・管理の経験は参考になるが、体系化されていたわけではなく、生成速度の変化を前提に見直す'))
    return svg(1000, 404, '従来とAI駆動開発での顕在化の速さ', body,
               desc='左の「従来の保守開発：徐々に顕在化」では、時間軸の上に成果物の箱が間隔を空けて5つ並び、その下で「変更影響の調査・回帰テストの範囲」のくさびが年単位で緩やかに広がる。右の「AI駆動開発：短い期間に集中」では、同じ5つの箱が詰まって並び、くさびが短い区間で急に広がって「同じ範囲の広がりが、短い期間に集中して現れる」と記した図')


# =====================================================================
# §9.1 成果物と情報が結びついた状態
# =====================================================================
def fig_09a_traceable_artifacts():
    body = [title('必要な情報が成果物と結びつき、変更時にも追跡・検証できる状態')]
    body.append(bracket(60, 940, 100, 'SSoT：唯一の正本として管理し、成果物からたどれるようにする', T2, 14, 700, up=True))
    boxes = [('要求', 'どの要求に基づくか', NEUTRAL, STROKE, T1), ('設計判断', '背景と意図の記録', NEUTRAL, STROKE, T1),
             ('成果物', 'AIが生成したもの', PRIMARY, LINE, PRI_TEXT), ('検証結果・未解決事項', '何が未検証か', NEUTRAL, STROKE, T1)]
    for i, (head, sub, fill, stroke, hf) in enumerate(boxes):
        x = 60 + i * 230
        body.append(box(x, 120, 200, 80, fill, head, sub, 18, 14, stroke, 1, hf))
        if i < 3:
            body.append(arrow(x + 200, 160, x + 230, 160))
    body.append(pill(290, 240, 190, 34, '設計判断の変更', ATTENTION, 14, 700, ATT_TEXT, ATT_LINE))
    body.append(path_arrow('M480 252 H620 V204', (620, 204, 0, -1), ATT_LINE, dashed=True, width=2))
    body.append(path_arrow('M480 262 H850 V204', (850, 204, 0, -1), ATT_LINE, dashed=True, width=2))
    body.append(text(680, 290, '影響する成果物と検証結果を特定し、再検証する', 14, 700, ATT_TEXT))
    body.append(note(336, 'ドキュメントを増やすのではなく、成果物と情報の結びつきを保つことで、後工程でまとめて返済する運営から転換する'))
    return svg(1000, 366, '成果物と情報が結びついた状態', body,
               desc='「要求（どの要求に基づくか）」「設計判断（背景と意図の記録）」「成果物（AIが生成したもの）」「検証結果・未解決事項（何が未検証か）」の4箱を左から右へ矢印でつなぎ、全体の上に「SSoT：唯一の正本として管理し、成果物からたどれるようにする」のブラケットを置く。設計判断の下の「設計判断の変更」から成果物と検証結果へ破線の矢印を引き、「影響する成果物と検証結果を特定し、再検証する」と記した図')


# =====================================================================
# §10 従来と AI 駆動開発の原価の積み上げ
# =====================================================================
def fig_10_estimate_structure():
    body = [title('実装の削減だけでなく、前工程・後工程・ADSの増加を別々に積み上げる')]
    base = 430
    def stack(x, segs, label):
        y = base
        out = []
        for name, h, fill, stroke, color in segs:
            y -= h
            out.append(rect(x, y, 200, h, fill, stroke, 1, rx=4))
            out.append(text(x + 100, y + h / 2 + 5, name, 14, 700, color))
        out.append(text(x + 100, base + 24, label, 15, 700, T1))
        return ''.join(out), y
    left, top_l = stack(230, [('設計', 50, NEUTRAL, STROKE, T1), ('実装', 110, NEUTRAL, STROKE, T1), ('テスト', 70, NEUTRAL, STROKE, T1), ('リリース', 40, NEUTRAL, STROKE, T1)], '従来の積み上げ')
    right, top_r = stack(570, [('設計', 42, NEUTRAL, STROKE, T1), ('実装（削減）', 26, POSITIVE, POS_LINE, POS_TEXT), ('テスト', 46, NEUTRAL, STROKE, T1), ('リリース', 26, NEUTRAL, STROKE, T1),
                               ('ADSの整備・保守', 26, ATTENTION, ATT_LINE, ATT_TEXT), ('検証基盤（TAS）', 24, ATTENTION, ATT_LINE, ATT_TEXT), ('横断的な品質保証の枠', 26, ATTENTION, ATT_LINE, ATT_TEXT)], 'AI駆動開発の積み上げ')
    body.append(f'<path d="M230 {top_l} H560 M770 {top_l} H790" stroke="{LINE}" stroke-width="2" stroke-dasharray="8 6" fill="none"/>')
    body.append(left); body.append(right)
    body.append(text(800, top_l + 5, '従来の総工数', 14, 400, MUTED, 'start'))
    body.append(text(800, top_r + 24, '増える項目', 14, 700, ATT_TEXT, 'start'))
    body.append(text(800, base - 42 - 26 / 2 + 5, '減る項目', 14, 700, POS_TEXT, 'start'))
    body.append(note(486, '相殺後の差額ではなく、削減される工数と増える工数を別々の行で示し、再利用できるADSは案件間で償却する'))
    return svg(1000, 516, '従来とAI駆動開発の原価の積み上げ', body,
               desc='左の「従来の積み上げ」は設計・実装・テスト・リリースの4段。右の「AI駆動開発の積み上げ」は実装が削減で薄くなる一方、ADSの整備・保守、検証基盤（TAS）、横断的な品質保証の枠の3段が加わる。従来の総工数の高さを破線で示し、右の総量はそれより低い。右側に「減る項目」「増える項目」を記した図。高さは定性的なもので実測値ではない')


FIGURES = {
    '01-effect-and-cost-timeline': fig_01_effect_and_cost_timeline,
    '02-two-costs': fig_02_two_costs,
    '02a-understanding-debt': fig_02a_understanding_debt,
    '03-evaluation-window': fig_03_evaluation_window,
    '04-issue-mr-health-check': fig_04_issue_mr_health_check,
    '04-flow-health-vs-qa-load': fig_04_flow_health_vs_qa_load,
    '04-uncounted-carry-over': fig_04_uncounted_carry_over,
    '05-gradual-vs-compressed': fig_05_gradual_vs_compressed,
    '06-sud-ads-definition': fig_06_sud_ads_definition,
    '06-ai-ci-test-env': fig_06_ai_ci_test_env,
    '06-sud-and-ads': fig_06_sud_and_ads,
    '06-sut-and-tas': fig_06_sut_and_tas,
    '06a-ads-cost-items': fig_06a_ads_cost_items,
    '06b-ads-maintenance-work': fig_06b_ads_maintenance_work,
    '06c-cicd-maturity': fig_06c_cicd_maturity,
    '07-three-costs-cycle': fig_07_three_costs_cycle,
    '08-constraint-shift': fig_08_constraint_shift,
    '09-directions': fig_09_directions,
    '09a-traceable-artifacts': fig_09a_traceable_artifacts,
    '10-estimate-structure': fig_10_estimate_structure,
}


def main():
    ASSETS.mkdir(exist_ok=True)
    for name, fn in FIGURES.items():
        (ASSETS / f'{name}.svg').write_text(fn(), encoding='utf-8')
        print('wrote', name)


if __name__ == '__main__':
    main()
