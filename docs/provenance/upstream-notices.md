# Upstream notices / 上游授權聲明

本來源現採正式 Core v0.2.0 `6887bfe6183465e9a9e6ccb4ccd7305a58b37302`，版本0.3.0，完整二十檔／十九份Markdown，封閉套件為36個payload加manifest共37檔；詳見 [0.3.0紀錄](../releases/v0.3.0.md)。下文舊版身分、數量、未發布及測試stub敘述保留各準備階段歷史，共同驗證與安全規則仍適用；現行身分與布局以本段及0.3.0紀錄為準。準備fixture的null出版欄位與false flags不改，不能判定後續發布狀態。兩端各一次9/9文字結果僅涵蓋相同四契約，不代表完整runtime資格；既有安裝未更新，四項readiness仍false。產品正式發布須另核對對應annotated tag及Release。

This source adopts published Core v0.2.0 `6887bfe6183465e9a9e6ccb4ccd7305a58b37302` and product version 0.3.0: twenty Core files, nineteen Markdown files and a 37-file closed bundle (36 payloads plus its manifest). See the [0.3.0 record](../releases/v0.3.0.md). Earlier identities, counts, unpublished-state claims and acceptance-stub descriptions below retain their preparation-stage meaning. Shared verification and safety rules still apply; this paragraph and the 0.3.0 record define the current identity and layout. Historical preparation null publication fields and false flags remain fixed and cannot determine later publication. Each consumer's single nine-case text result (9/9) covers only identical four-contract bytes, not full runtime qualification. Existing installations and all four false readiness flags remain unchanged. Product publication separately requires its annotated tag and Release.


2026-11-01採用準備helper與測試改編自codex-dev-skills `e83553f2bf907fe4afbbe6725a036d6cc569efd4` 的 scripts/verify-core-release-preparation.py 與 tests/test_core_release_preparation.py。下方完整Codex MIT notice涵蓋此改編；原notice每字保留。新增二十檔Core準備與十四檔歷史baseline各保留完整來源LICENSE／notices，不是正式runtime採用。

The adoption-preparation helper/tests adapt the fixed Codex sources above. Its complete MIT notice below covers this work unchanged. Both new Core snapshots retain source LICENSE/notices; neither preparation nor historical data is formal runtime adoption.

Issue #36 的開發 helper 與九案改編自 codex-dev-skills `a48a30d7769a5d0f53fa4fa269151114ed624cff` 的 scripts/eval-core-feedback-candidate.py 及 tests/fixtures/core-feedback-cases.json。下方完整 Codex MIT notice 同樣涵蓋此改編，原 notice 不改。Core 完整 LICENSE／notices 另隨十五檔 fixture 保留，這不是正式 runtime 採用。

The Issue #36 developer helper and nine cases adapt the fixed Codex sources above. The complete Codex MIT notice below also covers this adaptation with original text retained. The fifteen-file candidate separately keeps Core's full license/notices; it is not formal runtime adoption.

本包的設計整理自 [source map](source-map.md) 所列的固定 Core P0 與 Codex 來源；改寫內容為 Grok P2 準備設計，沒有搬移可執行程式。保留以下完整 MIT notices。根目錄 [LICENSE](../../LICENSE) 不取代來源 notices。未 vendor xAI 程式或完整文件；後續若引入第三方 substantial portions，必須另查授權與 notices，不能假設一律 MIT。

This design adapts the fixed Core P0 and Codex sources in the [source map](source-map.md) for Grok P2. It moves no executable code. The full source MIT notices follow. The root [LICENSE](../../LICENSE) does not replace them. No xAI source code or complete documentation is vendored. Future third-party substantial portions require their own license and notice review.

The original P3-G1 package additionally vendored the eleven fixed Core files at `b4c37798b6d3a9efd91c8c6d518093f2dd847a98`, with raw bytes unchanged. The [vendored LICENSE](../../vendor/engineering-workflow-core/LICENSE) and [upstream-notices](../../vendor/engineering-workflow-core/docs/provenance/upstream-notices.md) accompany the snapshot. The historical notices below remain intact. No Core executable is imported.

原 P3-G1 包另保留上述固定 P1 revision 的十一份原檔，不改 bytes；snapshot 隨附其 LICENSE 與完整 upstream notices。下方歷史 notices 原文保留；未引入 Core 執行程式。

[G-W1 / Issue #16](https://github.com/jeffery777/grok-build-dev-skills/issues/16) updated the snapshot at that time to Core `345cd601bffbacc777f87fb24f22b5caefa30a3b`. All eleven files retain their raw bytes from that revision. The new writing clause follows the accepted user requirement recorded in [Core provenance](../../vendor/engineering-workflow-core/docs/provenance/source-map.md#plain-writing-update). The complete Core and historical notices remain; no full ASD-STE100 standard is reproduced.

G-W1 當時將 snapshot 更新至上述 Core revision，保留十一份原 bytes。新寫作條款另記使用者需求來源，完整 Core 與歷史 notices 保留；未重製完整 ASD-STE100 標準。

[GG1 / Issue #18](https://github.com/jeffery777/grok-build-dev-skills/issues/18) updated the snapshot at that time to Core `784ed24f4a09ec35ac7209e0fd2287b214aea260`. All eleven files are raw copies of that revision. New evidence-lifecycle and risk-first-review clauses retain their user-origin provenance in the [Core source map](../../vendor/engineering-workflow-core/docs/provenance/source-map.md#evidence-lifecycle-update). Full Core and historical MIT notices remain unchanged; no Core executable or complete ASD standard is imported.

GG1 當時將 snapshot 更新至上述最終 revision，保留十一份原 bytes、新義務的使用者來源與完整 MIT notices；既有寫作及符合性限制保留，不引入 Core 程式或完整 ASD 標準。

[G-SA1 / Issue #20](https://github.com/jeffery777/grok-build-dev-skills/issues/20) consumed at that time the eleven raw Core files at `3a3fd41e5fb994b4429a67d76d1b0655d972d150` from merged [PR #14](https://github.com/jeffery777/engineering-workflow-core/pull/14). Only review-and-security and Core source-map differ from GG1. The LICENSE and complete notices retain their bytes. Shared policy changes retain their user-origin provenance in the [Core source map](../../vendor/engineering-workflow-core/docs/provenance/source-map.md). No third-party skill or executable is imported.

G-SA1 當時採上述十一份 Core 原 bytes，只有 review-and-security 與 Core source-map 改變；LICENSE、完整 notices 及新共同義務的使用者來源保留。未匯入第三方技能或程式。

[G-RF1 / Issue #22](https://github.com/jeffery777/grok-build-dev-skills/issues/22) consumed at that time eleven raw Core files at `64b19bb5658432c42cd6a26aa357fd6b1d0fd857` from merged [PR #16](https://github.com/jeffery777/engineering-workflow-core/pull/16). README, workflow, review-and-security and Core source-map differ from G-SA1. The remaining files, LICENSE and full notices retain their bytes. New common rules retain accepted user provenance in the [Core source map](../../vendor/engineering-workflow-core/docs/provenance/source-map.md#assumptions-options-update). No Core executable or third-party skill is imported.

G-RF1 當時採上述十一份 Core 原 bytes，只有所列四檔改變；其餘檔案、LICENSE 與完整 notices 保留。新義務的使用者來源另見固定 Core source-map，不倒寫為原 Codex P1 抽取內容；未匯入 Core 程式或第三方技能。

[G-REL1 / Issue #26](https://github.com/jeffery777/grok-build-dev-skills/issues/26) now consumes thirteen exact raw files from formal [Core v0.1.0](https://github.com/jeffery777/engineering-workflow-core/releases/tag/v0.1.0), commit `174df2af8dedf813b9bd4e3c184a627ee87d3cd8`, resolved from annotated tag object `e984c880a05065c8bcd0d78e83d78220b05bfc32`. README/source-map change and CHANGELOG/release notes are added; nine existing files retain bytes/modes, including all four contracts, LICENSE and full upstream notices. No executable, third-party skill or new runtime function is imported.

G-REL1 採上述正式十三份原檔，完整相對引用閉合及十二份 Markdown collection 已同步 lock／allowlist／anchors／manifest。保留所有完整 MIT copyright／permission／warranty notices、原始來源與歷史；generated bytes 不插入 header，消費端接入說明留在本文件與 [source map](source-map.md)。

## engineering-workflow-core

Source: [LICENSE at 0815b74abe52d57efd032bd075e39c83c2ebf0d6](https://github.com/jeffery777/engineering-workflow-core/blob/0815b74abe52d57efd032bd075e39c83c2ebf0d6/LICENSE).

```text
MIT License

Copyright (c) 2026 jeffery777

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## codex-dev-skills

Source: [LICENSE at 993597561881d6ed8c552f9a18c59315015ad245](https://github.com/jeffery777/codex-dev-skills/blob/993597561881d6ed8c552f9a18c59315015ad245/LICENSE).

```text
MIT License

Copyright (c) 2026 YANG CHUN CHIH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## G-GN1 / 0.2.0 candidate

G-GN1 重用 jeffery777/codex-dev-skills 固定 S/T 的三個 Python 模組，完整 MIT copyright／permission notice 原樣保留於 [LICENSE](../../vendor/gitnexus-index-controller/LICENSE)。不封裝 GitNexus/npm/Node 執行檔、私人 profile 或 Memory backend；原有 Core／上游 notices 保留。

G-GN1 reuses three Python modules from fixed Codex S/T. The complete MIT copyright/permission notice is preserved unchanged in [LICENSE](../../vendor/gitnexus-index-controller/LICENSE). GitNexus/npm/Node executables, private profiles and Memory backends are not bundled. Existing Core/upstream notices remain.
