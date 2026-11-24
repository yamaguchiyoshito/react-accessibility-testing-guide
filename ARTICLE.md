# **React／Frontendにおけるアクセシビリティテストの整理**

## **1. アクセシビリティテストの全体像**

アクセシビリティテストは、単にHTMLやARIA属性が正しく記述されているかを確認するものではありません。

**実装の妥当性、情報の認識可能性、操作可能性、業務の遂行可能性**という4つの観点から検証する必要があります。

**01**

**実装の妥当性**

HTML・ARIA・アクセシブルネーム

静的解析・自動テスト

**02**

**情報の認識可能性**

コントラスト・拡大表示・読み上げ

自動テスト・目視確認

**03**

**操作可能性**

キーボード・フォーカス・入力操作

ブラウザテスト・手動操作

**04**

**業務の遂行可能性**

支援技術を利用した業務フローの完遂

シナリオテスト・利用者評価

前述のFrontendテストの分類と同様、アクセシビリティもコンポーネント単位、画面単位、業務シナリオ単位に分けて検証します。

すべてをシステムテスト工程で検証する必要はありません。

## **2. アクセシビリティテストの手段**

テスト手段は、大きく7種類に分類できます。

| 手段         | 確認対象                  | 主なツール                  | 自動化 |
| ---------- | --------------------- | ---------------------- | --- |
| 静的コード解析    | JSX・HTML・ARIA属性       | eslint-plugin-jsx-a11y | ◎   |
| DOM解析      | セマンティクス・ラベル・属性・コントラスト | axe-core               | ◎   |
| コンポーネントテスト | Role・Name・State・操作    | React Testing Library  | ◎   |
| ブラウザ操作テスト  | キーボード操作・フォーカス遷移       | Playwright             | ◎   |
| 視覚的検証      | 拡大表示・配色・リフロー          | Playwright・DevTools    | ○   |
| 支援技術による検証  | スクリーンリーダー・音声操作        | NVDA・VoiceOver         | △   |
| ユーザビリティ評価  | 理解・操作・業務遂行            | 利用者参加型テスト              | ―   |

凡例：◎ 自動化に適する／○ 部分的に自動化可能／△ 原則手動／― 人による評価

W3Cも、ツールだけではアクセシビリティ基準への適合を判断できず、人による評価が必要であるとしています。

[image](https://www.google.com/s2/favicons?domain=https://www.w3.org\&sz=32)

W3C+1



## **3. アクセシビリティテストの確認対象**

WCAGの4原則である「知覚可能」「操作可能」「理解可能」「堅牢」をベースに、Reactの開発現場で扱いやすい確認対象に分解します。

| 分類     | 確認対象            | 主な確認内容            |
| ------ | --------------- | ----------------- |
| HTML構造 | セマンティクス         | 適切なHTML要素の使用      |
| HTML構造 | 見出し             | 論理的な見出し階層         |
| HTML構造 | ランドマーク          | main・nav等による領域の識別 |
| HTML構造 | テーブル            | 見出しセルとデータの関連付け    |
| 情報伝達   | 代替テキスト          | 画像の意味をテキストで伝達     |
| 情報伝達   | ラベル             | 入力項目とラベルの関連付け     |
| 情報伝達   | 状態通知            | 読み込み・成功・失敗の通知     |
| 情報伝達   | エラー             | エラー箇所・原因・修正方法     |
| 視覚     | コントラスト          | 文字・背景・UI要素の識別     |
| 視覚     | 色への依存           | 色以外の手段による情報伝達     |
| 視覚     | 拡大・リフロー         | 拡大時の情報欠落・操作不能     |
| 視覚     | フォーカス表示         | 現在の操作位置の視認性       |
| 操作     | キーボード           | マウスなしでの操作         |
| 操作     | フォーカス順序         | 論理的な順番での移動        |
| 操作     | フォーカス管理         | モーダル開閉・画面遷移時の制御   |
| 操作     | ターゲットサイズ        | 操作対象の大きさ・間隔       |
| 操作     | 代替操作            | ドラッグ等に対する代替手段     |
| 操作     | 時間制限            | 制限時間の延長・解除        |
| 理解     | 一貫性             | ナビゲーション・名称・操作     |
| 理解     | 入力支援            | 入力形式・必須条件の説明      |
| 理解     | 認証              | 認知機能に過度に依存しない認証   |
| 支援技術   | Name・Role・Value | 要素の名称・役割・値の認識     |
| 支援技術   | 動的更新            | 非同期処理後の適切な情報通知    |
| 支援技術   | 読み上げ順序          | 意味の通る順序での読み上げ     |

## **4. 確認対象とテスト手段のマトリクス**

確認対象ごとに、どの手段で検証すべきかを整理します。

| 確認対象        | Lint | axe | 操作テスト | 目視 | 読み上げ |
| ----------- | ---- | --- | ----- | -- | ---- |
| HTMLセマンティクス | ◎    | ◎   | ―     | ○  | ○    |
| ARIA属性      | ◎    | ◎   | ○     | ―  | ○    |
| 見出し構造       | ○    | ◎   | ―     | ○  | ○    |
| ラベルの有無      | ◎    | ◎   | ○     | ―  | ○    |
| ラベルの意味・妥当性  | ―    | △   | ○     | ◎  | ○    |
| 代替テキストの有無   | ◎    | ◎   | ―     | ―  | ○    |
| 代替テキストの妥当性  | ―    | △   | ―     | ◎  | ○    |
| コントラスト      | ―    | ◎   | ―     | ○  | ―    |
| 色への依存       | ―    | △   | ―     | ◎  | ―    |
| キーボード操作     | △    | △   | ◎     | ○  | ○    |
| フォーカス順序     | △    | △   | ◎     | ○  | ○    |
| フォーカス管理     | ―    | △   | ◎     | ○  | ○    |
| フォーカス表示     | ―    | △   | ○     | ◎  | ―    |
| 拡大・リフロー     | ―    | △   | ○     | ◎  | ―    |
| ターゲットサイズ    | ―    | △   | ◎     | ○  | ―    |
| エラー箇所の通知    | ―    | △   | ◎     | ○  | ◎    |
| 動的な状態通知     | △    | △   | ◎     | ―  | ◎    |
| 読み上げ順序      | ―    | △   | ○     | ―  | ◎    |
| 操作・表現の一貫性   | ―    | ―   | ○     | ◎  | ○    |
| 業務遂行可能性     | ―    | ―   | ○     | ○  | ◎    |

凡例：◎ 主たる確認手段／○ 補完的な確認手段／△ 限定的に検出可能／― 原則対象外

特に重要なのは、**axe-coreによる自動検査と、Playwrightによる操作テストは異なる責務を持つ**という点です。

axe-coreではルール違反を検出し、Playwrightでは期待される操作や状態遷移が成立するかを検証します。

## **5. 自動テストの具体的な実装方法**

### **5.1 静的解析：eslint-plugin-jsx-a11y**

JSXのソースコードから問題を検出します。

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub



| 検出対象               | ルール                            |
| ------------------ | ------------------------------ |
| 画像の代替テキスト不足        | `alt-text`                     |
| 入力項目とラベルの未関連付け     | `label-has-associated-control` |
| 不正なARIA属性          | `aria-props`                   |
| 不正なRole            | `aria-role`                    |
| クリック操作に対するキーイベント不足 | `click-events-have-key-events` |
| フォーカス制御の問題         | `no-noninteractive-tabindex`   |

```
npm install -D eslint-plugin-jsx-a11y
```

実行環境を起動する必要がないため、実装時およびコミット時の品質チェックに適しています。

### **5.2 コンポーネント検査：Storybook＋axe-core**

Storybookで定義された各コンポーネントの状態を検査します。

```
npx storybook add @storybook/addon-a11y
```

StorybookのAccessibility Addonはaxe-coreを利用しており、描画されたDOMを検査できます。

[image](https://www.google.com/s2/favicons?domain=https://storybook.js.org\&sz=32)

Storybook docs



### **検査対象の例：入力コンポーネント**

Default

メールアドレス

user\@example.com

Required

メールアドレス \*

未入力

Error

メールアドレス

abc

形式が正しくありません

Disabled

メールアドレス

user\@example.com

**axe-coreによる各Storyの検査**

ラベル・ARIA属性・コントラスト等

正常状態だけでなく、エラー、非活性、Loading、モーダル表示など、状態ごとの検査を行うことが重要です。

### **5.3 セマンティクス検証：React Testing Library**

コンポーネントが期待する名称や役割を持っているか、状態が適切に表現されているかを検証します。

```
expect(
  screen.getByRole('button', { name: '検索' })
).toBeEnabled();

expect(
  screen.getByRole('textbox', { name: '顧客名' })
).toBeInTheDocument();

expect(
  screen.getByRole('checkbox', { name: '同意する' })
).toBeChecked();
```

`getByTestId`ではなく、原則として`getByRole`や`getByLabelText`を優先することで、通常の機能テストにもアクセシビリティの観点を組み込めます。

### **5.4 画面全体の検査：Playwright＋axe-core**

コンポーネント単体では発見できない、画面全体の構造や組み合わせによる問題を検出します。

```
npm install -D @axe-core/playwright
```

```
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('顧客検索画面のアクセシビリティ', async ({ page }) => {
  await page.goto('/customers');

  const results = await new AxeBuilder({ page })
    .withTags([
      'wcag2a',
      'wcag2aa',
      'wcag21a',
      'wcag21aa',
      'wcag22aa',
    ])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

既存の画面操作テストの途中にaxe-coreの検査を組み込むことも可能です。

[image](https://www.google.com/s2/favicons?domain=https://playwright.dev\&sz=32)

Playwright



ただし、指定したWCAGタグの違反が0件であっても、WCAG適合を保証するものではありません。

### **5.5 キーボード・フォーカス検証：Playwright**

例えば、モーダルダイアログのフォーカス制御を検証します。

```
const trigger = page.getByRole('button', { name: '編集' });

await trigger.click();

const dialog = page.getByRole('dialog');

await expect(dialog).toBeVisible();
await expect(
  dialog.getByRole('textbox', { name: '顧客名' })
).toBeFocused();

await page.keyboard.press('Tab');

await expect(
  dialog.getByRole('textbox', { name: 'メールアドレス' })
).toBeFocused();

await page.keyboard.press('Escape');

await expect(dialog).toBeHidden();
await expect(trigger).toBeFocused();
```

このような操作上の要件は、axe-coreだけでは十分に検証できません。

### **5.6 アクセシビリティツリーの検証：ARIA Snapshot**

PlaywrightのARIA Snapshotを利用すると、支援技術に公開されるアクセシビリティ構造を回帰テストの対象にできます。

[image](https://www.google.com/s2/favicons?domain=https://playwright.dev\&sz=32)

Playwright



```
await expect(
  page.getByRole('form', { name: '顧客検索' })
).toMatchAriaSnapshot(`
  - form "顧客検索":
    - textbox "顧客名"
    - combobox "顧客区分"
    - button "検索"
    - button "クリア"
`);
```

DOMの実装構造ではなく、Roleやアクセシブルネームを中心とした構造を検証します。

ただし、スナップショットの一致は、実際のスクリーンリーダーの読み上げ品質を保証するものではありません。

## **6. テスト工程ごとの責務分担**

前述のFrontend単体テストと結合テストの分類に対応させると、以下のようになります。

| 確認対象          | FE単体 | FE内部結合 | FE・BE結合 | ST |
| ------------- | ---- | ------ | ------- | -- |
| HTML・ARIA属性   | ◎    | ○      | ―       | ―  |
| コンポーネントの名称・役割 | ◎    | ○      | ―       | ―  |
| コンポーネントの操作    | ◎    | ○      | ―       | ―  |
| コントラスト        | ◎    | ◎      | ―       | ○  |
| 画面全体の構造       | ―    | ◎      | ―       | ○  |
| 画面内のフォーカス順序   | ○    | ◎      | ―       | ○  |
| 画面遷移後のフォーカス   | ―    | ◎      | ○       | ○  |
| 拡大・リフロー       | ○    | ◎      | ―       | ○  |
| APIエラー時の通知    | ○    | ◎      | ○       | ○  |
| 認証画面の操作       | ○    | ○      | ◎       | ○  |
| スクリーンリーダー操作   | ○    | ◎      | ○       | ◎  |
| 業務シナリオの完遂     | ―    | ○      | ○       | ◎  |

凡例：◎ 主たる検証工程／○ 補完的な検証／― 原則対象外

アクセシビリティ上の不具合の多くは、Backendの完成を待たずに検証できます。

そのため、**アクセシビリティテストの主戦場はPG・UT工程に置くべきです。**

## **7. デザインシステムと個別画面の責務分担**

React開発で共通コンポーネントを整備している場合、ここが特に重要になります。

**デザインシステム側で保証する品質**

Button

Input

Dialog

Select

Checkbox

Tabs

Role・ARIA・キー操作・フォーカス管理・基本配色

検証済みコンポーネントの再利用

**個別画面側で保証する品質**

顧客検索画面

顧客登録画面

契約一覧画面

契約詳細画面

文脈に応じたラベル・配置・画面遷移・エラー通知

**システム側で保証する品質**

支援技術を使用して業務を完遂できること

| 検証観点             | デザインシステム | 個別画面 |
| ---------------- | -------- | ---- |
| ボタンのキーボード操作      | ◎        | ―    |
| ダイアログのフォーカストラップ  | ◎        | ○    |
| Selectの矢印キー操作    | ◎        | ―    |
| 基本カラートークンのコントラスト | ◎        | ○    |
| 業務に応じたラベル        | ―        | ◎    |
| 項目のフォーカス順序       | ―        | ◎    |
| エラーメッセージの妥当性     | ―        | ◎    |
| 画面遷移後のフォーカス      | ―        | ◎    |
| ページ全体のリフロー       | ―        | ◎    |

共通コンポーネント側で検証済みの振る舞いについて、個別画面ごとに同じ詳細テストを作成する必要はありません。ただし、組み合わせによって生じる問題は個別画面で検証します。

例えば433画面を持つシステムであれば、ダイアログの基本的なキーボード操作を各画面で詳細に再検証するよりも、共通コンポーネントの回帰テストとして資産化する方が合理的です。

## **8. 合否判定基準**

新規React開発の技術標準としては、WCAG 2.2のレベルAAを基本目標とすることを推奨します。ただし、顧客要求や契約上の適合基準は別途確定させます。

[image](https://www.google.com/s2/favicons?domain=https://www.w3.org\&sz=32)

W3C



| 確認項目           | 判定基準                          |
| -------------- | ----------------------------- |
| 通常文字のコントラスト    | 4.5:1以上                       |
| 大きな文字のコントラスト   | 3:1以上                         |
| 対象となる非テキストUI要素 | 3:1以上                         |
| 文字拡大           | 200%で情報・機能の欠落がない              |
| リフロー           | 原則320 CSS px幅で横スクロール不要        |
| ターゲットサイズ       | 原則24×24 CSS px以上、または規定の間隔等を確保 |
| キーボード操作        | 対象機能をマウスなしで操作可能               |
| フォーカス          | 可視であり、他のコンテンツに完全に隠されない        |
| 自動検査           | 対象ルールの未解決違反0件                 |
| 手動検査           | 対象とする達成基準を満たす                 |

※WCAGには達成基準ごとに適用条件・例外規定があります。上表は代表的な基準であり、AA適合の全条件を網羅するものではありません。

## **9. CI/CDへの組み込み方**

実装・コミット時

**ESLint / jsx-a11y**

静的な実装ルール違反を検出

Pull Request / Merge Request

**Vitest / Storybook / axe-core**

コンポーネントの状態・操作・DOMを検証

Frontendビルド後

**Playwright / axe-core / MSW**

画面構造・キーボード操作・画面遷移を検証

リリース前

**NVDA / VoiceOver / 手動評価**

支援技術による主要業務の検証

| 実行タイミング | 品質ゲート                 |
| ------- | --------------------- |
| コミット時   | Lintエラー0件             |
| MR時     | コンポーネントテスト成功・自動検査違反0件 |
| ビルド後    | 画面操作テスト成功・自動検査違反0件    |
| リリース前   | 手動検査・支援技術検証・適合評価完了    |

既存システムに導入する場合は、既知の違反を管理した上で、新規違反を増やさない回帰防止方式から開始することも有効です。

## **10. AIによるアクセシビリティテスト支援**

AI支援については、次の5つの能力に分けて整備することを推奨します。

| Skill案                           | 責務               | 成果物              |
| -------------------------------- | ---------------- | ---------------- |
| `design-a11y-test`               | WCAGと画面仕様から観点を抽出 | テスト観点・ケース        |
| `generate-component-a11y-test`   | コンポーネントの検証コード生成  | Storybook・Vitest |
| `generate-page-a11y-test`        | 画面の構造・操作テスト生成    | Playwright       |
| `analyze-a11y-violations`        | 検査結果の分析・修正案生成    | 不具合一覧・修正案        |
| `generate-manual-a11y-checklist` | 自動化できない項目の整理     | 手動検査手順書          |

AIは、代替テキストやラベルの意味的な妥当性についてもレビューを支援できます。ただし、AIの判定だけで適合を確定してはいけません。

## **11. 参考資料**

| 資料                                                                                                                          | 用途              |
| --------------------------------------------------------------------------------------------------------------------------- | --------------- |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/?utm_source=chatgpt.com)                                                            | 適合基準            |
| [W3C Evaluating Web Accessibility](https://www.w3.org/WAI/test-evaluate/?utm_source=chatgpt.com)                            | 評価方法            |
| [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/?utm_source=chatgpt.com)                               | コンポーネントの操作・実装仕様 |
| [Playwright Accessibility Testing](https://playwright.dev/docs/accessibility-testing?utm_source=chatgpt.com)                | 画面自動検査          |
| [Playwright ARIA Snapshots](https://playwright.dev/docs/aria-snapshots?utm_source=chatgpt.com)                              | アクセシビリティ構造の回帰検証 |
| [Storybook Accessibility Testing](https://storybook.js.org/docs/writing-tests/accessibility-testing?utm_source=chatgpt.com) | コンポーネント自動検査     |
| [eslint-plugin-jsx-a11y](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y?utm_source=chatgpt.com)                       | 静的解析            |

## **結論**

アクセシビリティテストは、次の4層で標準化するべきです。

| 層          | 保証する品質               |
| ---------- | -------------------- |
| 静的解析       | 実装ルールに違反していない        |
| axe-core   | 描画されたUIに機械検出可能な違反がない |
| Playwright | 期待する操作・状態遷移が成立する     |
| 人・支援技術     | 情報を理解し、実際に業務を遂行できる   |

さらに、デザインシステム側と個別画面側の検証責務を分離することで、画面数に比例してテスト工数が増加する構造を抑制できます。

**アクセシビリティを後工程の検査項目として扱うのではなく、共通コンポーネントが備える品質特性として実装し、開発中に継続的に保証する。**

これが、React開発におけるアクセシビリティテストの標準化方針です。