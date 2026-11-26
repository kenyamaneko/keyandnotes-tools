import pytest
from git_repository_support import (
    assert_output_line_written,
    assert_stopped_with_message,
    assert_succeeded,
    create_commits,
    create_repository,
    read_output_lines,
    resolve_commit_references,
    run_change_detection,
)


class Test本体__変更判定__業務処理__変更判定:
    @pytest.mark.parametrize(
        (
            "snapshots",
            "options",
            "expected_line",
            "given",
            "when",
            "then",
            "perspectives",
        ),
        [
            pytest.param(
                [{"README.md": "# 店舗\n"}, {"README.md": "# 店舗システム\n"}],
                ("--pull-request-base", "{0}"),
                "changed=false",
                "`README.md` の `# 店舗` が `# 店舗システム` に変更されているとき",
                "除外パスを足さず、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `changed=false` が書かれる",
                [],
                id="README_ドット_md_の_シャープ_店舗_が_シャープ_店舗システム_に変更されているとき_除外パスを足さず_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_changed_イコール_false_が書かれる",
            ),
            pytest.param(
                [{"src/price.ts": "const price = 100;\n"}, {"src/price.ts": "const price = 100; // 税抜\n"}],
                ("--pull-request-base", "{0}"),
                "changed=false",
                "`src/price.ts` の `const price = 100;` が `const price = 100; // 税抜` に変更されているとき",
                "除外パスを足さず、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `changed=false` が書かれる",
                [],
                id="src_スラッシュ_price_ドット_ts_の_const_price_イコール_100_セミコロン_が_const_price_イコール_100_セミコロン_スラッシュ_スラッシュ_税抜_に変更されているとき_除外パスを足さず_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_changed_イコール_false_が書かれる",
            ),
            pytest.param(
                [{"README.md": "# 店舗\n"}, {}],
                ("--pull-request-base", "{0}"),
                "changed=false",
                "変更が 0 件のとき",
                "除外パスを足さず、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `changed=false` が書かれる",
                ["件数・有無"],
                id="変更が_0_件のとき_除外パスを足さず_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_changed_イコール_false_が書かれる",
            ),
            pytest.param(
                [{"src/price.ts": "const price = 100;\n", "src/stock.ts": "const stock = 1;\n"}, {"src/price.ts": "const price = 100; // 税抜\n", "src/stock.ts": "const stock = 2;\n"}],
                ("--pull-request-base", "{0}"),
                "changed=true",
                "`src/price.ts` の `const price = 100;` が `const price = 100; // 税抜` に変更され、`src/stock.ts` の `const stock = 1;` が `const stock = 2;` に変更されているとき",
                "除外パスを足さず、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `changed=true` が書かれる",
                [],
                id="src_スラッシュ_price_ドット_ts_の_const_price_イコール_100_セミコロン_が_const_price_イコール_100_セミコロン_スラッシュ_スラッシュ_税抜_に変更され_src_スラッシュ_stock_ドット_ts_の_const_stock_イコール_1_セミコロン_が_const_stock_イコール_2_セミコロン_に変更されているとき_除外パスを足さず_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_changed_イコール_true_が書かれる",
            ),
            pytest.param(
                [{".github/workflows/deploy-dev.yml": "timeout-minutes: 10\n"}, {".github/workflows/deploy-dev.yml": "timeout-minutes: 20\n"}],
                ("--pull-request-base", "{0}"),
                "changed=true",
                "`.github/workflows/deploy-dev.yml` の `timeout-minutes: 10` が `timeout-minutes: 20` に変更されているとき",
                "除外パスを足さず、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `changed=true` が書かれる",
                [],
                id="ドット_github_スラッシュ_workflows_スラッシュ_deploy_ハイフン_dev_ドット_yml_の_timeout_ハイフン_minutes_コロン_10_が_timeout_ハイフン_minutes_コロン_20_に変更されているとき_除外パスを足さず_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_changed_イコール_true_が書かれる",
            ),
            pytest.param(
                [{".github/workflows/deploy-dev.yml": "timeout-minutes: 10\n"}, {".github/workflows/deploy-dev.yml": "timeout-minutes: 20\n"}],
                ("--excluded-path", ".github/workflows/deploy-*.yml", "--pull-request-base", "{0}"),
                "changed=false",
                "`.github/workflows/deploy-dev.yml` の `timeout-minutes: 10` が `timeout-minutes: 20` に変更されているとき",
                "除外パスに、`.github/workflows` の下にある `deploy-` で始まる YAML ファイルすべてを足して、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `changed=false` が書かれる",
                [],
                id="ドット_github_スラッシュ_workflows_スラッシュ_deploy_ハイフン_dev_ドット_yml_の_timeout_ハイフン_minutes_コロン_10_が_timeout_ハイフン_minutes_コロン_20_に変更されているとき_除外パスに_ドット_github_スラッシュ_workflows_の下にある_deploy_ハイフン_で始まる_YAML_ファイルすべてを足して_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_changed_イコール_false_が書かれる",
            ),
            pytest.param(
                [{"backend/src/price.ts": "const price = 100;\n", "frontend/src/cart.ts": "const quantity = 1;\n"}, {"backend/src/price.ts": "const price = 100; // 税抜\n", "frontend/src/cart.ts": "const quantity = 2;\n"}],
                ("--scope", "backend=backend/**", "--scope", "frontend=frontend/**", "--pull-request-base", "{0}"),
                "changed=true",
                "`backend/src/price.ts` の `const price = 100;` が `const price = 100; // 税抜` に、`frontend/src/cart.ts` の `const quantity = 1;` が `const quantity = 2;` に変更されているとき",
                "`backend` の下のすべてのファイルを範囲 `backend` に、`frontend` の下のすべてのファイルを範囲 `frontend` に指定して、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `changed=true` が書かれる",
                [],
                id="backend_スラッシュ_src_スラッシュ_price_ドット_ts_の_const_price_イコール_100_セミコロン_が_const_price_イコール_100_セミコロン_スラッシュ_スラッシュ_税抜_に_frontend_スラッシュ_src_スラッシュ_cart_ドット_ts_の_const_quantity_イコール_1_セミコロン_が_const_quantity_イコール_2_セミコロン_に変更されているとき_backend_の下のすべてのファイルを範囲_backend_に_frontend_の下のすべてのファイルを範囲_frontend_に指定して_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_changed_イコール_true_が書かれる",
            ),
            pytest.param(
                [{"backend/src/price.ts": "const price = 100;\n", "frontend/src/cart.ts": "const quantity = 1;\n"}, {"backend/src/price.ts": "const price = 100; // 税抜\n", "frontend/src/cart.ts": "const quantity = 2;\n"}],
                ("--scope", "backend=backend/**", "--scope", "frontend=frontend/**", "--pull-request-base", "{0}"),
                "backend=false",
                "`backend/src/price.ts` の `const price = 100;` が `const price = 100; // 税抜` に、`frontend/src/cart.ts` の `const quantity = 1;` が `const quantity = 2;` に変更されているとき",
                "`backend` の下のすべてのファイルを範囲 `backend` に、`frontend` の下のすべてのファイルを範囲 `frontend` に指定して、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `backend=false` が書かれる",
                [],
                id="backend_スラッシュ_src_スラッシュ_price_ドット_ts_の_const_price_イコール_100_セミコロン_が_const_price_イコール_100_セミコロン_スラッシュ_スラッシュ_税抜_に_frontend_スラッシュ_src_スラッシュ_cart_ドット_ts_の_const_quantity_イコール_1_セミコロン_が_const_quantity_イコール_2_セミコロン_に変更されているとき_backend_の下のすべてのファイルを範囲_backend_に_frontend_の下のすべてのファイルを範囲_frontend_に指定して_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_backend_イコール_false_が書かれる",
            ),
            pytest.param(
                [{"backend/src/price.ts": "const price = 100;\n", "frontend/src/cart.ts": "const quantity = 1;\n"}, {"backend/src/price.ts": "const price = 100; // 税抜\n", "frontend/src/cart.ts": "const quantity = 2;\n"}],
                ("--scope", "backend=backend/**", "--scope", "frontend=frontend/**", "--pull-request-base", "{0}"),
                "frontend=true",
                "`backend/src/price.ts` の `const price = 100;` が `const price = 100; // 税抜` に、`frontend/src/cart.ts` の `const quantity = 1;` が `const quantity = 2;` に変更されているとき",
                "`backend` の下のすべてのファイルを範囲 `backend` に、`frontend` の下のすべてのファイルを範囲 `frontend` に指定して、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `frontend=true` が書かれる",
                [],
                id="backend_スラッシュ_src_スラッシュ_price_ドット_ts_の_const_price_イコール_100_セミコロン_が_const_price_イコール_100_セミコロン_スラッシュ_スラッシュ_税抜_に_frontend_スラッシュ_src_スラッシュ_cart_ドット_ts_の_const_quantity_イコール_1_セミコロン_が_const_quantity_イコール_2_セミコロン_に変更されているとき_backend_の下のすべてのファイルを範囲_backend_に_frontend_の下のすべてのファイルを範囲_frontend_に指定して_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_frontend_イコール_true_が書かれる",
            ),
            pytest.param(
                [{"README.md": "# 店舗\n"}, {"README.md": "# 店舗システム\n"}],
                ("--scope", "backend=backend/**", "--pull-request-base", "{0}"),
                "changed=false",
                "`README.md` の `# 店舗` が `# 店舗システム` に変更されているとき",
                "`backend` の下のすべてのファイルを範囲 `backend` に指定して、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `changed=false` が書かれる",
                [],
                id="README_ドット_md_の_シャープ_店舗_が_シャープ_店舗システム_に変更されているとき_backend_の下のすべてのファイルを範囲_backend_に指定して_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_changed_イコール_false_が書かれる",
            ),
            pytest.param(
                [{"README.md": "# 店舗\n"}, {"README.md": "# 店舗システム\n"}],
                ("--scope", "backend=backend/**", "--pull-request-base", "{0}"),
                "backend=false",
                "`README.md` の `# 店舗` が `# 店舗システム` に変更されているとき",
                "`backend` の下のすべてのファイルを範囲 `backend` に指定して、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `backend=false` が書かれる",
                [],
                id="README_ドット_md_の_シャープ_店舗_が_シャープ_店舗システム_に変更されているとき_backend_の下のすべてのファイルを範囲_backend_に指定して_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_backend_イコール_false_が書かれる",
            ),
            pytest.param(
                [{"package.json": "{\n  \"name\": \"shop\"\n}\n"}, {"package.json": "{\n  \"name\": \"store\"\n}\n"}],
                ("--scope", "backend=backend/**", "--pull-request-base", "{0}"),
                "changed=true",
                "`package.json` の `\"name\": \"shop\"` が `\"name\": \"store\"` に変更されているとき",
                "`backend` の下のすべてのファイルを範囲 `backend` に指定して、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `changed=true` が書かれる",
                [],
                id="package_ドット_json_の_ダブルクォート_name_ダブルクォート_コロン_ダブルクォート_shop_ダブルクォート_が_ダブルクォート_name_ダブルクォート_コロン_ダブルクォート_store_ダブルクォート_に変更されているとき_backend_の下のすべてのファイルを範囲_backend_に指定して_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_changed_イコール_true_が書かれる",
            ),
            pytest.param(
                [{"package.json": "{\n  \"name\": \"shop\"\n}\n"}, {"package.json": "{\n  \"name\": \"store\"\n}\n"}],
                ("--scope", "backend=backend/**", "--pull-request-base", "{0}"),
                "backend=false",
                "`package.json` の `\"name\": \"shop\"` が `\"name\": \"store\"` に変更されているとき",
                "`backend` の下のすべてのファイルを範囲 `backend` に指定して、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `backend=false` が書かれる",
                [],
                id="package_ドット_json_の_ダブルクォート_name_ダブルクォート_コロン_ダブルクォート_shop_ダブルクォート_が_ダブルクォート_name_ダブルクォート_コロン_ダブルクォート_store_ダブルクォート_に変更されているとき_backend_の下のすべてのファイルを範囲_backend_に指定して_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_backend_イコール_false_が書かれる",
            ),
        ],
    )
    def test_change_detection(
        self,
        record_case,
        tmp_path,
        snapshots,
        options,
        expected_line,
        given,
        when,
        then,
        perspectives,
    ):
        record_case(
            kind="インフラ結合テスト",
            normal_or_abnormal="正常系",
            perspectives=perspectives,
            items=[("Given", given), ("When", when), ("Then", then)],
        )
        assert_output_line_written(tmp_path, snapshots, options, expected_line)


class Test本体__変更判定__業務処理__比較元の決め方:
    @pytest.mark.parametrize(
        (
            "snapshots",
            "options",
            "expected_line",
            "given",
            "when",
            "then",
            "perspectives",
        ),
        [
            pytest.param(
                [{"README.md": "# 店舗\n", "src/price.ts": "const price = 100;\n"}, {"src/price.ts": "const price = 200;\n"}, {"README.md": "# 店舗システム\n"}],
                ("--pull-request-base", "{1}", "--pushed-before", "{0}"),
                "changed=false",
                "取り込み先のコミットとの差分は `README.md` の `# 店舗` から `# 店舗システム` への変更だけで、プッシュ前のコミットとの差分には `src/price.ts` の `const price = 100;` から `const price = 200;` への変更も含まれているとき",
                "取り込み先のコミットとプッシュ前のコミットをどちらも指定して、変更判定を実行する",
                "出力ファイルに `changed=false` が書かれる",
                [],
                id="取り込み先のコミットとの差分は_README_ドット_md_の_シャープ_店舗_から_シャープ_店舗システム_への変更だけで_プッシュ前のコミットとの差分には_src_スラッシュ_price_ドット_ts_の_const_price_イコール_100_セミコロン_から_const_price_イコール_200_セミコロン_への変更も含まれているとき_取り込み先のコミットとプッシュ前のコミットをどちらも指定して_変更判定を実行すると_出力ファイルに_changed_イコール_false_が書かれる",
            ),
            pytest.param(
                [{"src/price.ts": "const price = 100;\n"}, {"src/price.ts": "const price = 200;\n"}],
                ("--pushed-before", "{0}"),
                "changed=true",
                "プッシュ前のコミットとの差分に、`src/price.ts` の `const price = 100;` から `const price = 200;` への変更が含まれているとき",
                "取り込み先のコミットを指定せず、プッシュ前のコミットだけを指定して、変更判定を実行する",
                "出力ファイルに `changed=true` が書かれる",
                [],
                id="プッシュ前のコミットとの差分に_src_スラッシュ_price_ドット_ts_の_const_price_イコール_100_セミコロン_から_const_price_イコール_200_セミコロン_への変更が含まれているとき_取り込み先のコミットを指定せず_プッシュ前のコミットだけを指定して_変更判定を実行すると_出力ファイルに_changed_イコール_true_が書かれる",
            ),
            pytest.param(
                [{"README.md": "# 店舗\n"}],
                ("--pushed-before", "0000000000000000000000000000000000000000", "--scope", "backend=backend/**"),
                "changed=true",
                "新しいブランチがプッシュされているとき",
                "プッシュ前のコミットに `0000000000000000000000000000000000000000` を指定し、`backend` の下のすべてのファイルを範囲 `backend` に指定して、変更判定を実行する",
                "出力ファイルに `changed=true` が書かれる",
                [],
                id="新しいブランチがプッシュされているとき_プッシュ前のコミットに_0000000000000000000000000000000000000000_を指定し_backend_の下のすべてのファイルを範囲_backend_に指定して_変更判定を実行すると_出力ファイルに_changed_イコール_true_が書かれる",
            ),
            pytest.param(
                [{"README.md": "# 店舗\n"}],
                ("--pushed-before", "0000000000000000000000000000000000000000", "--scope", "backend=backend/**"),
                "backend=true",
                "新しいブランチがプッシュされているとき",
                "プッシュ前のコミットに `0000000000000000000000000000000000000000` を指定し、`backend` の下のすべてのファイルを範囲 `backend` に指定して、変更判定を実行する",
                "出力ファイルに `backend=true` が書かれる",
                [],
                id="新しいブランチがプッシュされているとき_プッシュ前のコミットに_0000000000000000000000000000000000000000_を指定し_backend_の下のすべてのファイルを範囲_backend_に指定して_変更判定を実行すると_出力ファイルに_backend_イコール_true_が書かれる",
            ),
        ],
    )
    def test_base_selection(
        self,
        record_case,
        tmp_path,
        snapshots,
        options,
        expected_line,
        given,
        when,
        then,
        perspectives,
    ):
        record_case(
            kind="インフラ結合テスト",
            normal_or_abnormal="正常系",
            perspectives=perspectives,
            items=[("Given", given), ("When", when), ("Then", then)],
        )
        assert_output_line_written(tmp_path, snapshots, options, expected_line)


class Test本体__変更判定__業務処理__比較元の指定のやり直し:
    @pytest.mark.parametrize(
        (
            "first_options",
            "error_phrases",
            "second_options",
            "first_given",
            "first_when",
            "first_then",
            "second_when",
            "second_then",
        ),
        [
            pytest.param(
                (),
                ("比較元", "指定されていません"),
                ("--pull-request-base", "{0}"),
                "`README.md` の `# 店舗` が `# 店舗システム` に変更されているとき",
                "取り込み先のコミットもプッシュ前のコミットも指定せず、変更後のコミットで変更判定を実行する",
                "比較元が指定されていないことを示すエラーで終了する",
                "除外パスを足さず、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `changed=false` が書かれる",
                id="README_ドット_md_の_シャープ_店舗_が_シャープ_店舗システム_に変更されているとき_取り込み先のコミットもプッシュ前のコミットも指定せず_変更後のコミットで変更判定を実行すると_比較元が指定されていないことを示すエラーで終了する_除外パスを足さず_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_changed_イコール_false_が書かれる",
            ),
            pytest.param(
                ("--pull-request-base", "1234567890abcdef1234567890abcdef12345678"),
                ("取り込み先のコミット", "存在しません"),
                ("--pull-request-base", "{0}"),
                "`README.md` の `# 店舗` が `# 店舗システム` に変更され、コミット `1234567890abcdef1234567890abcdef12345678` がリポジトリにないとき",
                "取り込み先のコミットに `1234567890abcdef1234567890abcdef12345678` を指定して、変更後のコミットで変更判定を実行する",
                "取り込み先のコミットがリポジトリにないことを示すエラーで終了する",
                "除外パスを足さず、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `changed=false` が書かれる",
                id="README_ドット_md_の_シャープ_店舗_が_シャープ_店舗システム_に変更され_コミット_1234567890abcdef1234567890abcdef12345678_がリポジトリにないとき_取り込み先のコミットに_1234567890abcdef1234567890abcdef12345678_を指定して_変更後のコミットで変更判定を実行すると_取り込み先のコミットがリポジトリにないことを示すエラーで終了する_除外パスを足さず_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_changed_イコール_false_が書かれる",
            ),
            pytest.param(
                ("--pushed-before", "1234567890abcdef1234567890abcdef12345678"),
                ("プッシュ前のコミット", "存在しません"),
                ("--pushed-before", "{0}"),
                "`README.md` の `# 店舗` が `# 店舗システム` に変更され、コミット `1234567890abcdef1234567890abcdef12345678` がリポジトリにないとき",
                "プッシュ前のコミットに `1234567890abcdef1234567890abcdef12345678` を指定して、変更後のコミットで変更判定を実行する",
                "プッシュ前のコミットがリポジトリにないことを示すエラーで終了する",
                "除外パスを足さず、プッシュ前のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する",
                "出力ファイルに `changed=false` が書かれる",
                id="README_ドット_md_の_シャープ_店舗_が_シャープ_店舗システム_に変更され_コミット_1234567890abcdef1234567890abcdef12345678_がリポジトリにないとき_プッシュ前のコミットに_1234567890abcdef1234567890abcdef12345678_を指定して_変更後のコミットで変更判定を実行すると_プッシュ前のコミットがリポジトリにないことを示すエラーで終了する_除外パスを足さず_プッシュ前のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_changed_イコール_false_が書かれる",
            ),
        ],
    )
    def test_recovery_after_base_specification_error(
        self,
        record_case,
        tmp_path,
        first_options,
        error_phrases,
        second_options,
        first_given,
        first_when,
        first_then,
        second_when,
        second_then,
    ):
        record_case(
            kind="インフラ結合テスト",
            normal_or_abnormal="異常系",
            perspectives=["回復確認"],
            items=[
                ("Given", first_given),
                ("When", first_when),
                ("Then", first_then),
                ("When", second_when),
                ("Then", second_then),
            ],
        )
        repository = create_repository(tmp_path / "repository")
        output_file = tmp_path / "output.txt"
        commit_ids = create_commits(
            repository, [{"README.md": "# 店舗\n"}, {"README.md": "# 店舗システム\n"}]
        )
        first = run_change_detection(
            repository,
            [
                *resolve_commit_references(first_options, commit_ids),
                "--head",
                commit_ids[-1],
                "--output-file",
                str(output_file),
            ],
        )
        assert_stopped_with_message(first, *error_phrases)
        second = run_change_detection(
            repository,
            [
                *resolve_commit_references(second_options, commit_ids),
                "--head",
                commit_ids[-1],
                "--output-file",
                str(output_file),
            ],
        )
        assert_succeeded(second)
        assert "changed=false" in read_output_lines(output_file)


class Test本体__変更判定__業務処理__出力ファイルの指定:
    @pytest.mark.parametrize(
        "snapshots",
        [
            pytest.param(
                [{"README.md": "# 店舗\n"}, {"README.md": "# 店舗システム\n"}],
                id="README_ドット_md_の_シャープ_店舗_が_シャープ_店舗システム_に変更されているとき_出力ファイルを指定せず_除外パスを足さず_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルが指定されていないことを示すエラーで終了する_出力ファイルを指定し_除外パスを足さず_取り込み先のコミットに変更前のコミットを指定して_変更後のコミットで変更判定を実行すると_出力ファイルに_changed_イコール_false_が書かれる",
            ),
        ],
    )
    def test_output_file_specification(self, record_case, tmp_path, snapshots):
        record_case(
            kind="インフラ結合テスト",
            normal_or_abnormal="異常系",
            perspectives=["回復確認"],
            items=[
                ("Given", "`README.md` の `# 店舗` が `# 店舗システム` に変更されているとき"),
                ("When", "出力ファイルを指定せず、除外パスを足さず、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する"),
                ("Then", "出力ファイルが指定されていないことを示すエラーで終了する"),
                ("When", "出力ファイルを指定し、除外パスを足さず、取り込み先のコミットに変更前のコミットを指定して、変更後のコミットで変更判定を実行する"),
                ("Then", "出力ファイルに `changed=false` が書かれる"),
            ],
        )
        repository = create_repository(tmp_path / "repository")
        output_file = tmp_path / "output.txt"
        commit_ids = create_commits(repository, snapshots)
        first = run_change_detection(
            repository, ["--pull-request-base", commit_ids[0], "--head", commit_ids[-1]]
        )
        assert_stopped_with_message(first, *("出力ファイル", "指定されていません"))
        second = run_change_detection(
            repository,
            [
                "--pull-request-base",
                commit_ids[0],
                "--head",
                commit_ids[-1],
                "--output-file",
                str(output_file),
            ],
        )
        assert_succeeded(second)
        assert "changed=false" in read_output_lines(output_file)
