# Changelog / 更新紀錄

[繁體中文](#zh) · [English](#en)

<a id="zh"></a>

## 繁體中文

### 0.2.1 — 2026-10-19

- 修正複製式 Local plugin 的升級交付：原生同來源重裝被拒絕後，經明確授權保全、單產品卸載、零註冊讀回與固定新版安裝，在隔離 fixture 成功讀回唯一 0.2.1 與精確三十檔。見 [證據與限制](docs/verification/local-plugin-upgrade.md)。
- 更新 [安裝／失敗處理](docs/installation.md)、README 與 [0.2.1 說明](docs/releases/v0.2.1.md)。程式只改產品版本 literal、對應測試及衍生 manifest；技能、controller、Core、source locks、依賴與 MIT notices 不變。
- 發行不自動更新用戶安裝；正式新增信任另行確認。自訂資料、多產品、模型載入及原子 rollback 未資格化，離線 readiness 仍 false。保留歷史 0.2.0 說明與 tag／Release。

### 0.1.0 — 2026-10-17

首版產品提供官方 plugin 格式的離線工程技能套件。正式發布身分以 [GitHub Release](https://github.com/jeffery777/grok-build-dev-skills/releases/tag/v0.1.0)、annotated tag 及解析後的完整 commit 為準；來源版本字串本身不證明已發布或已安裝。

- 提供 `grok-engineering-workflow` 與 `grok-review-change` 兩個技能，消費固定 Core 的工作流、授權、審查／安全與 exact-head 契約。實際工具、模型、權限及 session 控制由 Grok host 負責。
- 採正式 Core v0.1.0 commit `174df2af8dedf813b9bd4e3c184a627ee87d3cd8`。保留十三份原檔、十二份 Markdown collection、獨立 LICENSE 與完整 notices；包含新 Core CHANGELOG／release notes 的完整相對引用閉合。使用者不必另裝 Core，版本不要求與 consumer 同步。
- 沿用標準函式庫的離線 verifier／fresh-stage assembler、能力目錄及 consumer evidence packet。固定 code anchors、allowlist、lock、逐檔與集合 digest、no-follow 讀取、全新目標／失敗保留及引用檢查；fixture／operator report 不升級為 runtime 證據。
- 沿用 [PR #25](https://github.com/jeffery777/grok-build-dev-skills/pull/25) 的官方 metadata 與可信來源／獨立 raw manifest digest。因 Core 閉合新增兩檔，bundle 從二十一增至二十三檔（二十二 payload＋manifest）；驗證／staging 算法與技能正文不改。
- 補齊中英文 [README](README.md)、[發行說明](docs/releases/v0.1.0.md)、[指定版本安裝／更新／回復](docs/installation.md)、依賴與 provenance；區分來源 archive、封閉 bundle、原生實裝及模型採用。受影響測試納入新增文件缺失及重算本地 manifest 後的 Core 竄改拒絕。

未發布的 `0.1.0-candidate.1` 與等待 pin 的準備狀態是開發歷史，並非先前正式版或已證原生 upgrade／downgrade。正式更新與回復須選各版本的可信固定來源／verifier／digest，保全既有／自訂／partial 內容，不疊放、不盲目重播或以卸載當 rollback。

依賴：既有 Python 3.10+ 標準函式庫、適用 POSIX 檔案操作，Git 供取得固定來源，既有 Grok CLI 供日後原生 plugin 管理。macOS 有離線證據，其他 POSIX 未資格化，Windows 不支援。目錄版本 `1.0.52 (0920c8169e27)` 與 2026-10-17 觀察到的 help `1.0.60 (01a8e1c591c0)` 分列，未認證相容版本範圍。沒有新增執行環境、服務、MCP／hooks、新模型投入、Reason 功能或 API 憑證。

本發行不修改用戶安裝／設定。原生目的地／bookkeeping／信任、整樹 Core closure、自訂檔保護及 native update／rollback 仍待最小實裝整合。Help、schema、inventory 或 exit 0 不代表安裝／模型採用；runtime、skill-loading、delegation、delivery readiness 均 false。[Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) 保留歷史 OPEN、設計完成且非阻擋；不重開整套 sandbox／deny／resume QA。英文採清晰寫作原則，完整 ASD-STE100 符合性未驗證。

[MIT License](LICENSE)、[完整上游 notices](docs/provenance/upstream-notices.md) 與 [來源／變更對照](docs/provenance/source-map.md) 保留；新 consumer 完整 diff 的檢查、獨立 review、安全證據、平台／exact-head 與發布收據另隨正式 Release／本地交接提供，既有 Core 或準備階段 scan 不代替。

<a id="en"></a>

## English

### 0.2.1 — 2026-10-19

- Correct copied Local plugin upgrade delivery. After native same-source reinstallation was rejected, explicitly authorized preservation, single-product uninstall, zero-registration readback and fixed-version installation produced exactly one 0.2.1 registration and all thirty files in an isolated fixture. See [evidence and limits](docs/verification/local-plugin-upgrade.md).
- Update [installation/failure handling](docs/installation.md), README and [0.2.1 notes](docs/releases/v0.2.1.md). Executable changes are the product-version literal only, its test expectation and derived manifest hashes. Skills, controller, Core, source locks, dependencies and MIT notices are unchanged.
- Publication does not update user installations or grant production trust. Custom data, multi-product behavior, model loading and atomic rollback remain unqualified; offline readiness stays false. Historical 0.2.0 notes and tag/Release are retained.

### 0.1.0 — 2026-10-17

The first product supplies an offline engineering-skills package in the native plugin format. Publication identity comes from the [GitHub Release](https://github.com/jeffery777/grok-build-dev-skills/releases/tag/v0.1.0), annotated tag and full resolved commit. A source version string alone proves neither publication nor installation.

- `grok-engineering-workflow` and `grok-review-change` consume fixed Core workflow, authorization, review/security and exact-head contracts. The Grok host retains actual tools, models, permissions and session controls.
- Formal Core v0.1.0 is pinned to `174df2af8dedf813b9bd4e3c184a627ee87d3cd8`. Thirteen raw files, the twelve-Markdown collection, separate LICENSE and full notices form complete relative-reference closure, including new Core CHANGELOG/release notes. Core needs no separate installation or matching consumer version.
- Existing standard-library verification, fresh staging, capability catalog and consumer evidence packets retain code anchors, allowlists, locks, file/set digests, no-follow reads, new-target/failure preservation and reference checks. Fixtures/operator reports never become runtime evidence.
- [PR #25](https://github.com/jeffery777/grok-build-dev-skills/pull/25) supplies native metadata and trusted-source/independent-manifest checks. Two new Core closure members expand the bundle from 21 to 23 files: twenty-two payload files plus manifest. Verification/staging algorithms and skill bodies remain unchanged.
- Bilingual [README](README.md), [release notes](docs/releases/v0.1.0.md), [exact-version installation/update/recovery](docs/installation.md), dependencies and provenance distinguish source archives, closed bundles, native installation and model adoption. Affected tests reject missing new documents and Core tampering despite rewritten local package hashes.

Unpublished `0.1.0-candidate.1` and the earlier waiting state are development history, not an earlier formal product or proved native upgrade/downgrade. Updates/recovery use each version's trusted fixed source/verifier/digest, preserving existing/custom/partial state without overlays, blind replay or uninstall-as-rollback.

Dependencies: existing Python 3.10+ standard-library support and suitable POSIX file operations; Git retrieves fixed source and an existing Grok CLI manages plugins later. macOS has offline evidence; other POSIX systems are unqualified and Windows is unsupported. Documented catalog `1.0.52 (0920c8169e27)` differs from help `1.0.60 (01a8e1c591c0)` observed on 2026-10-17; no compatibility range is certified. No runtime, service, MCP/hooks, new model work, Reason feature or API credential is added.

Publication changes no user installation/settings. Native destination/bookkeeping/trust, whole-tree Core closure, custom preservation and native update/rollback remain later minimum integration. Help, schema, inventory and exit 0 do not prove installation/model adoption. Runtime, skill-loading, delegation and delivery readiness stay false. [Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) remains design-complete historical OPEN tracking, nonblocking here; full sandbox/deny/resume QA is not reopened. English uses clarity principles; full ASD-STE100 conformity is unverified.

[MIT License](LICENSE), [full upstream notices](docs/provenance/upstream-notices.md) and [source/change records](docs/provenance/source-map.md) remain. The formal Release/local handoff binds checks, independent review, security evidence, platform/exact-head gates and publication readback for the complete consumer diff. Earlier Core/preparation scans do not replace that coverage.

## 0.2.0 — 未發行候選 / Unreleased candidate

- 保留兩技能，加入明確編排指派的 GitNexus 精確 1.6.12 inspect/plan/index-only refresh 入口；Codex 或 Grok 均可被指定為單一 index writer。配對 Codex 0.35.0 候選、Core 0.1.0；只重用固定 S/T 三模組及完整 MIT notice。
- 加入來源 lock／code anchors、30 檔候選套件及離線接入測試；profile 外部 digest、目標／角色、原鎖／receipt、失敗及未知效果保持界線。已有 2026-10-18 Grok 1.0.62 隔離 fixture 的有界原生唯讀觀察：完整讀兩技能及必要 Core、一次精確 plan、兩個假設停止情境；未做原生 refresh 或實際取消／恢復。既有 A02 controller 寫入及四項合成鎖證據分列於 [支援矩陣](docs/verification/gitnexus-operation-acceptance.md)。沒有安裝或發行，也不重驗 GitNexus 本體。
- 候選內容與限制見 [0.2.0 說明](docs/releases/v0.2.0.md)；不是 tag／Release 或安裝收據。
- Keep both skills and add explicitly assigned GitNexus 1.6.12 inspect/plan/index-only refresh. Either Codex or Grok can be the sole index writer. Pair with Codex 0.35.0 candidate and Core 0.1.0; reuse only fixed S/T modules and the full MIT notice.
- Add source pins/code anchors, a thirty-file candidate package and offline integration tests for profile/target/role, original locks/receipt and failure/unknown outcomes. A bounded native Grok 1.0.62 fixture observation on 2026-10-18 read both skills and required Core files, ran one exact read-only plan, and answered two hypothetical stop cases. Native refresh and actual cancel/recovery were not run. The [support matrix](docs/verification/gitnexus-operation-acceptance.md) separates inherited A02 controller-write evidence and four synthetic lock cases. No installation, publication or vendor-function retest occurred. See the [0.2.0 candidate notes](docs/releases/v0.2.0.md); these are not tag/Release or installation receipts.
