> NOTE: このファイルは原則として人間が運用する。例外的に許可があった場合のみClaude Codeが修正しても良い。

# keyandnotes-tools 固有ルール (overlay)

## [keyandnotes-tools] ブランチ戦略とデプロイ

- ブランチ戦略は keyandnotes-rules の GitHub Flow に従う
- デプロイ戦略は keyandnotes-rules の Artifact Publish に従う
- タグを打つと版が確定する。各リポジトリの CI は、タグを指定して本リポジトリを取得する

## [keyandnotes-tools] バージョニング

- 版は Git タグ `vX.Y.Z` で示す。上げ方は keyandnotes-rules のバージョニングとCI方針「直接のユーザーを想定しない場合」に従う

## [keyandnotes-tools] ブランチ保護 (GitHub Rulesets)

- main へのマージに必要なステータスチェック: `test`, `lint`
