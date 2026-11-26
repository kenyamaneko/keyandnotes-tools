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

CI で、コードの変更があるときだけテスト・ビルドのジョブを動かすために使う。コメントだけが変わった差分と、除外パスの変更は、コードの変更に数えない。

1. 本リポジトリをタグを指定してチェックアウトし、`pip install -r <チェックアウト先>/requirements.txt` を実行する
2. 各リポジトリの `git fetch` で、比較元のコミットを取得できるようにする (`actions/checkout` の `fetch-depth: 0`)
3. 各リポジトリのルートで、チェックアウト先を `PYTHONPATH` に通して `python -m change_detection` を実行する
4. 結果は出力ファイルに、`changed=true|false` と `<範囲名>=true|false` の行で追記される。GitHub Actions では、出力ファイルに `$GITHUB_OUTPUT` を指定する

| オプション | 内容 |
|---|---|
| `--pull-request-base` | 取り込み先のコミット。プルリクエストのときだけ指定する (空文字を渡さない) |
| `--pushed-before` | プッシュ前のコミット。プルリクエストでないとき指定する |
| `--head` | 変更後のコミット (必須) |
| `--output-file` | 結果を書くファイル (必須) |
| `--excluded-path` | 標準の除外パスに足すパターン。繰り返せる |
| `--scope` | `<範囲名>=<パスのパターン>`。繰り返せる |

標準の除外パスは次のとおり。

- `*.md`
- `docs/**`
- `rules/**`
- `.claude/**`
- `.vscode/**`
- `.gitignore`
- `LICENSE`
