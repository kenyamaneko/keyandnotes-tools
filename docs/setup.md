# セットアップ

## 前提条件

- Python 3.14
- Node.js (Tailwind で CSS を生成するときだけ必要)

## 開発環境

1. `pip install -r requirements-dev.txt`

## テストケースカタログの CSS

1. `npm ci`
2. `npm run build:css`

## 各リポからの使い方

1. 本リポをタグを指定してチェックアウトする
2. チェックアウトしたディレクトリで、「テストケースカタログの CSS」の手順を実行する
3. 各リポに、変わらない項目 (`title`・`features`) だけを書いた JSON を置く
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
