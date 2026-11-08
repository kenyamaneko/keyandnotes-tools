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

## バージョンタグを打つワークフロー

各リポのリリースのワークフローから、タグを指定して `create-version-tag.yml` を呼ぶ。デプロイのジョブは `needs` でつなぎ、打ったバージョンタグを `needs.<ジョブ名>.outputs.version_tag` で受け取る。`GITHUB_TOKEN` で打ち込んだタグは別のワークフローを起動しないため、同じワークフローの中でつなぐ。

```yaml
jobs:
  version_tag:
    uses: kenyamaneko/keyandnotes-tools/.github/workflows/create-version-tag.yml@vX.Y.Z
    permissions:
      contents: write
    with:
      bump_kind: ${{ inputs.bump_kind }}

  deploy:
    needs: version_tag
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Show deployed version tag
        env:
          VERSION_TAG: ${{ needs.version_tag.outputs.version_tag }}
        run: echo "$VERSION_TAG"
```

| 項目 | 内容 |
|---|---|
| 入力 `bump_kind` | バージョンアップの種類。`patch`・`minor`・`major` のいずれか |
| 出力 `version_tag` | 打ったバージョンタグ |
| タグを打つ先 | 呼び出し元のワークフローが実行されたコミット |
| 呼び出し元が与える権限 | `contents: write` |

リモートにバージョンタグ (`vX.Y.Z`) が 1 つも無いリポでは、失敗する。最初のバージョンタグは手で打つ。
