# GitNexus 操作對等支援 / Operation parity

[繁體中文](#zh-tw) · [English](#en)

<a id="zh-tw"></a>
<details open>
<summary>繁體中文</summary>

[Issue #28](https://github.com/jeffery777/grok-build-dev-skills/issues/28) 的 G-GN1 未提交候選，供維護者及編排方使用。配對為 Grok 0.2.0 候選、Codex 0.35.0 候選、Core 0.1.0、GitNexus 精確 1.6.12。不是發行或現行安裝變更。Core 固定 `174df2af8dedf813b9bd4e3c184a627ee87d3cd8`，不加入 executable 或反向執行相依。

保留兩個既有技能；[操作 reference](../../references/gitnexus-operations.md) 連到一個薄入口。執行技能按編排指派選目標及操作；review 技能只讀證據、不刷新索引。編排方每次決定由 Codex 或 Grok 操作，single writer 不屬於某一端。技能、flags、request ID、鎖或 receipt 均不創造使用者授權。

已接收 [Codex #355](https://github.com/jeffery777/codex-dev-skills/issues/355) 固定本地 S=`e23e18ed0512ece04ca6b6dceba3a6a1cf59b9fd`、T=`5b7cc2486df65366ae0f7bdaa78a23b7c2adf258`。只從 immutable Git objects 重用三 Python 模組及完整 MIT LICENSE；四 blobs 在 S/T 相同。固定 [來源 lock](../../gitnexus.lock.json) 與 code-owned digest 在載入前驗證捕獲 bytes；拒絕既有 bare-name dependency，不 import mutable checkout／用戶安裝。來源是未發行候選，不是正式發布。

`memory_contract.py` 是純資料契約依賴，不包含 Memory backend。沒有複製 Loop、installer、catalog、hooks、scheduler 或私人 profile，也不另建通用框架。T-TEST-001（Codex installer 舊版測試假設）與 T-DOC-001（installer/catalog 過時指引）未隨四檔移植，不直接改變這些 controller API。依編排方後續交接，兩項已在 Codex 五檔未提交候選修正，19 項定向測試及 code/docs review 通過；S/T 與四個 blobs 未變。這是交接狀態，不代表本端重驗 installer 整體或已發行。

薄入口只用 `qualify_local_1612` 重用獨立接受的 profile bytes／外部 SHA 及既有 probe receipts，不走一般 operator/probe 入口。完整目標、角色及 writer 由本端核對；刷新仍交原 `RefreshController.refresh`，不覆寫 runner/env/lock。共用 canonical R/UID lock、metadata、sidecar 與原 receipt 語意，外層只補 actor/request 綁定。失敗或未知效果停止並交回編排方，不盲目重播。

三 repo 責任：Core 保留 Markdown 義務；Codex 提供固定 controller 契約與原工具證據；Grok 維護兩技能、薄入口、source lock/notices、package/manifest 與自身接入驗收。詳見 [接入驗收](../verification/gitnexus-operation-acceptance.md)。驗收只涵蓋我們的技能／Agent 正確使用，不重驗 GitNexus 本體功能、bug 或 vendor sandbox。query/MCP 並存與自動刷新未納入。2026-10-18 的有界原生觀察已驗 Grok 1.0.62 在隔離 fixture 讀取兩技能／必要 Core，並精確呼叫一次唯讀 plan；未執行原生 refresh。接入驗收分開列原生 plan、既有 A02 controller 寫入與合成鎖證據。整體 readiness 不升級；追加原生調用仍須新的具體有界授權，本包保持未提交，不 push、PR、merge、發行或更動目前安裝。

</details>

<a id="en"></a>
<details>
<summary>English</summary>

G-GN1 under [Issue #28](https://github.com/jeffery777/grok-build-dev-skills/issues/28) is an uncommitted Grok 0.2.0 candidate, paired with Codex 0.35.0 candidate, Core 0.1.0 and GitNexus exactly 1.6.12. It is not published or installed. Core stays at `174df2af8dedf813b9bd4e3c184a627ee87d3cd8`, with no executable or reverse runtime dependency.

Keep both existing skills with one [reference](../../references/gitnexus-operations.md) and thin entry. The orchestrator assigns timing, exact target and either Codex or Grok as sole index writer. Reviewers read evidence without refreshing. Skills, flags, request IDs, locks and receipts grant no authority.

The [source lock](../../gitnexus.lock.json) pins local unreleased S=`e23e18ed0512ece04ca6b6dceba3a6a1cf59b9fd` and T=`5b7cc2486df65366ae0f7bdaa78a23b7c2adf258`. Only three Python modules and the complete MIT LICENSE were copied from immutable Git blobs; S/T have identical bytes. Code-owned digests validate captured bytes before execution; occupied sibling module names are rejected. No mutable checkout or installed source is imported.

The pure `memory_contract.py` dependency supplies data contracts, not a backend. No Loop, installer, catalog, hooks, scheduler or private profile is copied, and no general framework is added. T-TEST-001 concerns Codex installer old-version assumptions; T-DOC-001 concerns outdated installer/catalog guidance. Neither is copied or changes these controller APIs. The coordinator reports both fixed in five uncommitted Codex files, with 19 targeted tests and code/docs review passed; S/T and all four blobs remain unchanged. This records the handoff, not a new Grok-side installer verification or publication.

Use only `qualify_local_1612` with independently accepted profile bytes/external digest and existing probe receipts. The general operator/probe route is not used. Grok checks target, role and assigned writer, then delegates to the original `RefreshController.refresh` without runner/env/lock overrides. Canonical R/UID locks, metadata, sidecar and complete receipt semantics remain unchanged. The outer result adds actor/request binding only. Uncertain effects stop for reconciliation; no blind replay occurs.

Core owns Markdown duties; Codex owns fixed controller contracts and original tool evidence; Grok owns skills, entry, source pin/notices, package and [integration acceptance](../verification/gitnexus-operation-acceptance.md). Test our correct use, not GitNexus features, bugs or vendor sandbox. Query/MCP coexistence and automatic refresh remain outside scope. The bounded 2026-10-18 observation verified Grok 1.0.62 reading both skills and required Core files in an isolated fixture and invoking one exact read-only plan. Native refresh was not run. Acceptance separates that observation from inherited A02 controller-write and synthetic lock evidence. General readiness is unchanged. Additional native calls need new bounded authority. Keep this candidate uncommitted; no push, PR, merge, publication or current-installation change is authorized here.

English follows ASD-STE100 clarity principles; full conformance is unverified.

</details>
