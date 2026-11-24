# React／Frontendにおけるアクセシビリティテストの整理

**アクセシビリティテストは、静的解析・axe-core・Playwright・人と支援技術の4層で標準化し、共通コンポーネントが備える品質特性として開発中に継続的に保証する。後工程の検査項目にはしない。**

Reactを用いたFrontend開発で、アクセシビリティの「何を」「どうやって」「どの工程で」「誰が」確認するかを整理し、WCAG 2.2 AAを基本目標とした合否判定基準、CI/CDへの組み込み方までを1記事にまとめた社内向けの技術標準の資料。

[記事を読む](ARTICLE.md)

## 論旨の要約

1. アクセシビリティテストは、実装の妥当性、情報の認識可能性、操作可能性、業務の遂行可能性の4つの観点から検証する。上の観点ほど人の判断が要る。
2. 確認対象はWCAGの4原則をReactの開発現場で扱いやすい6分類24項目に分解し、手段は静的解析からユーザビリティ評価までの7種類に分ける。「有無」は機械で確認でき、「妥当性」は人が確認する。
3. axe-coreはある瞬間に描画されたDOMのルール違反を検出し、Playwrightは操作と状態遷移の成立を検証する。責務が異なり、片方で他方を代替できない。
4. アクセシビリティ上の不具合の多くはBackendの完成を待たずに検証できる。主戦場はPG・UT工程（FE単体テストとFE内部結合テスト）に置く。
5. 保証する品質をデザインシステム、個別画面、システムの3層に分け、共通コンポーネントで検証済みの振る舞いを画面ごとに再検証しない。画面数に比例してテスト工数が増える構造を抑える。
6. 自動テストはコミット時、PR／MR時、ビルド後の3段階で毎回実行し、リリース前に人と支援技術で主要業務を確認する。4層（静的解析・axe-core・Playwright・人と支援技術）は4つの観点に対応する。

本文は `ARTICLE.md` の1記事で、連載形式ではない。図版10点は `assets/` のSVGで、すべて `scripts/draw_figures.py` が生成する。社内向け資料のため、GitHub Pagesなどの外部公開は行わず、オフライン閲覧用の単一HTMLで配布する。

## ファイル構成

```text
Accessibility_test/
├── README.md                  # リポジトリ案内（本ファイル）
├── ARTICLE.md                 # 記事本文（Markdown）。閲覧サイトでは index.html になる
├── site.json                  # サイト定義（題名、版、日付、記事のパス）
├── assets/                    # 図（SVG、10点）と同名の PNG（幅2000px）。ファイル名は章番号で始める
├── dist/offline.html          # 配布用の単一HTML（ビルド成果物の控え。build_single.py が更新）
├── site-src/styles.css        # 閲覧サイトのスタイル（前の記事と共通）
├── scripts/
│   ├── draw_figures.py        # 全図版を決定論的に生成（Python標準ライブラリのみ）
│   ├── check_figures.py       # SVGの整形性・最小フォント・配色・コントラスト・箱からのはみ出し・文字重なりを検査
│   ├── export_png.py          # assets/*.svg → assets/*.png（rsvg-convert、幅2000px）。--check で存在と新しさを確認
│   ├── build.py               # ARTICLE.md → _site/（HTML）
│   ├── build_single.py        # _site/index.html → _site/offline.html と dist/offline.html（図を埋め込んだ単一HTML）
│   └── check_html.py          # _site/ のリンク・図版数・alt・スクリプト不在を検査
├── .claude/launch.json        # ローカル確認用のプレビューサーバー定義（_site/ を 8765 番で配信。git管理外）
└── claudedocs/                # 公開計画などの作業記録（サイトには載せない）
```

生成物 `_site/` は `.gitignore` で除外する。`dist/offline.html` だけは配布用に管理対象とする。

## GitLab・GitHubで読む

`ARTICLE.md` をリポジトリのPreviewで開く。図は相対リンク先のSVGとして表示される。閲覧のために専用アプリは必要ない。表のセルの縦結合（下記の編集ルール8）はPreviewでは行われない。

## ブラウザで読む（ローカル生成）

Python 3.11以降とPandoc 3.xを使う。Python標準ライブラリだけで動き、追加パッケージは不要である。PNG の書き出しだけは rsvg-convert（librsvg）を使う。この版はPython 3.13・Pandoc 3.7系・librsvg 2.60系で検証した。

```sh
python3 scripts/draw_figures.py    # 図版を再生成（図を変えたとき）
python3 scripts/check_figures.py   # 図版の検査
python3 scripts/export_png.py      # SVG と同名の PNG を書き出す（要 rsvg-convert：brew install librsvg）
python3 scripts/build.py
python3 scripts/build_single.py    # オフライン閲覧用の単一HTML（_site/offline.html と dist/offline.html）
python3 scripts/check_html.py
```

`_site/index.html` をブラウザで開く。目次ドロワー（記事の章見出し）、相対リンクの図をローカルで表示する。`check_html.py` は `offline.html` へのリンクも検査するので、`build_single.py` の後に実行する。

## 配布する

`dist/offline.html` は記事をファイル1つにまとめたもので、図を data URI として埋め込み、インターネット接続なしでも開ける。社内への配布はこのファイル1つを共有すればよい。外部スクリプト・外部フォント・外部通信は使っていない。ビルド環境がなくても、GitHub のファイル表示（`dist/offline.html`）右上の「Download raw file」か、次の URL からそのまま取得できる。

https://github.com/yamaguchiyoshito/react-accessibility-testing-guide/raw/main/dist/offline.html

個別の図を別の資料に貼るときは `assets/` の PNG（SVG と同名、幅2000px）を使う。本文や図を変えたら `scripts/build_single.py` を実行して `dist/offline.html` も更新し、一緒にコミットする。

CIで検証する場合は、上記の6コマンドを順に実行し、いずれかが失敗したら配布しない。

## 編集ルール

1. 記事は単独で読めるように結論・前提・用語を記述する。未確定の事項は「※」で始まる段落に明記し、確定したら本文へ移す。社内の案件名や案件固有の数値（画面数など）は載せず、「数百画面を持つシステム」のように書く。
2. SVGのファイル名は図を置く章の番号で始める。
3. `assets/` の図はすべて `scripts/draw_figures.py` が生成し、PNG は `scripts/export_png.py` が SVG から書き出す。SVG も PNG も手で編集せず、スクリプトを直して再生成する。文字は14px以上、注記は16px（本文では720pxに縮小表示される）。
4. 図は定性的な配置と塗り分けで示し、根拠のない数値を描かない。要素は2〜5個、矢印は1方向に限る（戻りを示す図だけ、戻りの矢印を破線で1本足す）。テストレベルの鎖（FE単体→FE内部結合→FE・BE結合→ST）は `levels()`、縦積みの層（観点・4層）は `stack()` で描き、複数の図で同じ形を使う。
5. 色は役割で固定する。NEUTRAL（区別を付けない基本要素、画面・コンポーネントの箱）、PRIMARY（自動テスト＝Lint・axe-core・Testing Library・Playwright とその検出範囲）、HUMAN（人と支援技術＝スクリーンリーダー・目視・利用者評価）、POSITIVE（自動化できる・検証済みの資産として再利用できる）、ATTENTION（ツールでは保証できない・手動が要る・限界。1図に1系統）、INK（結論は色ではなく太字）。1図の地の塗りは4種以内、文字と地色のコントラスト比は4.5以上とし、`scripts/check_figures.py` が機械的に検査する。色だけで状態を伝える図には文字ラベルを併記する。実線は流れ、破線は戻り、2pxの細線はブラケットに使う。
6. 図のキャプション（Markdown の alt ＝ SVG の aria-label）は、図の主題を表す名詞句で全角30字以内とし、要素の列挙や「〜を示す図」で終える書き方はしない。図の内容の詳しい説明は SVG 内の `<desc>` に書く。長さは `scripts/check_figures.py` と `scripts/check_html.py` が機械的に検査する。
7. 冒頭の結論文は h1 直後の太字だけの段落として書く（CSS が導入文として整える）。本文中の強調は太字だけの段落にしてよいが、h3 直後には置かない（h3 直後の太字だけの段落は節のスコープ表示として小さく表示される）。
8. 表のセルの縦結合は `scripts/build.py` がビルド時に rowspan で行う。1列目は直前の行と同じ内容なら結合する（空欄と「—」は結合しない）。それ以外の列は、セルに「〃」（同上）と書くと直上のセルに結合する。Git のプレビューでは結合されず、同じ値がそのまま見える。結合した表は先頭列だけ折り返さない（CSS の `.table-grid td:first-child`）。
9. スマートフォン幅（360px）では、§6 の工程別の表と §10 のCI/CDの表、およびコードブロックが `.table-wrap`・`pre` の中で横スクロールになる。これは許容する。それ以外の表は横スクロールなしで収まることを確認する。
10. 表の記号 ◎○△― は表ごとに意味が異なるので、各表の直下に凡例を置く。
11. コードブロックには言語タグ（`bash`・`ts`・`tsx`）を付ける。
12. 出典と注記は、本文の該当文の末尾に Pandoc の脚注 `[^id]` を付け、記事末尾の「## 参考文献・注記」に `[^id]: 著者, *題名*（年）。要旨。URL` の形で書く。URL に `utm_source` などの追跡パラメータを付けない。この h2 は目次の章番号に含めず、目次ドロワーの下部からリンクする。
13. 題名・日付・版を変えたときは `site.json` と本READMEを更新し、`scripts/build.py` と `scripts/check_html.py` を通す。
