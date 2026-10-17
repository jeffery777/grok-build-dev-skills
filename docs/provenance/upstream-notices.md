# Upstream notices / 上游授權聲明

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

[G-RF1 / Issue #22](https://github.com/jeffery777/grok-build-dev-skills/issues/22) now consumes eleven raw Core files at `64b19bb5658432c42cd6a26aa357fd6b1d0fd857` from merged [PR #16](https://github.com/jeffery777/engineering-workflow-core/pull/16). README, workflow, review-and-security and Core source-map differ from G-SA1. The remaining files, LICENSE and full notices retain their bytes. New common rules retain accepted user provenance in the [Core source map](../../vendor/engineering-workflow-core/docs/provenance/source-map.md#assumptions-options-update). No Core executable or third-party skill is imported.

G-RF1 現採上述十一份 Core 原 bytes，只有所列四檔改變；其餘檔案、LICENSE 與完整 notices 保留。新義務的使用者來源另見固定 Core source-map，不倒寫為原 Codex P1 抽取內容；未匯入 Core 程式或第三方技能。

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
