# セットアップ

## 前提条件

- Python 3.14
- Node.js (Tailwind で CSS を生成するときだけ必要)

## 開発環境

1. `pip install -r requirements-dev.txt`

## テストケースカタログの CSS

1. `npm ci`
2. `npm run build:css`

## 各リポジトリからの使い方

1. 本リポジトリをタグを指定してチェックアウトする
2. チェックアウトしたディレクトリで、「テストケースカタログの CSS」の手順を実行する
3. 各リポジトリに、変わらない項目 (`title`・`features`) だけを書いた JSON を置く
4. CI で、実行のたびに変わる項目 (`commit`・`results`・`css`) を `jq` で足した JSON を作る
5. `python <チェックアウト先>/test_case_catalog/generate_test_case_catalog.py --config <手順 4 の JSON のパス>` を実行する。カタログの HTML が標準出力へ出る

```sh
jq --arg commit "$GITHUB_SHA" --arg css "tools/test_case_catalog/test_case_catalog.css" \
  '. + {commit: $commit, css: $css, results: [{language: "TypeScript", path: "junit-backend/junit.xml"}, {language: "TypeScript", path: "junit-frontend/vitest-junit.xml"}]}' \
  catalog.base.json > catalog.json
```

設定の JSON の相対パスは、スクリプトを実行したディレクトリからのパスとして読む。項目は次のとおり。

| 項目 | 必須 | 内容 |
|---|---|---|
| `title` | ○ | カタログのページタイトル |
| `css` | ○ | 手順 2 で生成した CSS のパス |
| `results` | ○ | テスト結果の配列。要素は、言語 `language` (`TypeScript`・`Python`・`C#`・`Kotlin`・`Go`・`Dart` のいずれか) と、テスト結果のパス `path` |
| `features` | ○ | 区分ごとの、大機能の並びと中機能の並び。カタログはこの順に並ぶ。ここにない大機能・中機能のテストがあるとエラーになる |
| `commit` | | 生成元 commit の SHA。省略するとカタログに表示しない |

## 変更判定

CI で、コードの変更があるときだけテスト・ビルドのジョブを動かすために使う。コメントだけが変わった差分と、除外パスの変更は、コードの変更に数えない。除外パスでないファイルの権限の変更は、コードの変更に数える。

コメントだけが変わった差分を判定する対象言語は次のとおり。これ以外の言語のファイルの変更は、コードの変更に数える。対象言語のファイルを解析できないときは、コードの変更に数え、標準エラー出力に警告ログを出す。

- TypeScript (TSX を含む)
- JavaScript
- Go
- Python
- Dart
- C#
- Kotlin
- Terraform

1. 本リポジトリをタグを指定してチェックアウトし、`pip install -r <チェックアウト先>/requirements.txt` を実行する
2. 各リポジトリの `git fetch` で、比較元のコミットを取得できるようにする (`actions/checkout` の `fetch-depth: 0`)
3. 各リポジトリのルートで、チェックアウト先を `PYTHONPATH` に通して `python -m change_detection` を実行する
4. 結果は出力ファイルに、`changed=true|false` と `<範囲名>=true|false` の行で追記される。GitHub Actions では、出力ファイルに `$GITHUB_OUTPUT` を指定する

| オプション | 内容 |
|---|---|
| `--pull-request-base` | 取り込み先のコミット。指定があるときは、比較元に使う。空文字は指定なしとして扱う |
| `--pushed-before` | プッシュ前のコミット。取り込み先のコミットの指定がないときに、比較元に使う。空文字は指定なしとして扱う |
| `--head` | 変更後のコミット (必須)。リポジトリにないときは、エラーで終了する |
| `--output-file` | 結果を書くファイル (必須) |
| `--excluded-path` | 標準の除外パスに足すパターン。繰り返せる |
| `--scope` | `<範囲名>=<パスのパターン>`。繰り返せる。同じ範囲名を繰り返すと、その範囲にパターンが足される |

取り込み先のコミットもプッシュ前のコミットも指定がないときと、比較元のコミットがリポジトリにないとき (例: 新しいブランチのプッシュ) は、リポジトリ全体とすべての範囲に、コードの変更があるとみなす。このときは、標準エラー出力にログを出す。ログのレベルは、新しいブランチのプッシュでは情報、それ以外では警告になる。

パスのパターンの `*` は、`/` を含む任意の文字列に一致する。

標準の除外パスは次のとおり。

- `*.md`
- `docs/**`
- `rules/**`
- `.claude/**`
- `.vscode/**`
- `.gitignore`
- `LICENSE`

GitHub Actions で、判定の結果を後続のジョブと呼び出し元のワークフローに渡す部分は、次のように書く。

```yaml
on:
  workflow_call:
    outputs:
      code:
        value: ${{ jobs.changes.outputs.code }}

jobs:
  changes:
    outputs:
      code: ${{ steps.detect.outputs.changed }}
      backend: ${{ steps.detect.outputs.backend }}
    steps:
      - name: Detect code change
        id: detect
        env:
          PR_BASE_SHA: ${{ github.event.pull_request.base.sha }}
          PUSH_BEFORE_SHA: ${{ github.event.before }}
        run: |
          PYTHONPATH=<チェックアウト先> python -m change_detection \
            --pull-request-base "$PR_BASE_SHA" --pushed-before "$PUSH_BEFORE_SHA" \
            --head HEAD --output-file "$GITHUB_OUTPUT" \
            --scope 'backend=backend/*'
```
