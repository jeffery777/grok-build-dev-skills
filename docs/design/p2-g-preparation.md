# P2-G 準備設計 / Preparation design

[繁體中文](#design-zh) · [English](#design-en) · [資格紀錄 / Qualification](../verification/grok-control-qualification.md)

<a id="design-zh"></a>

## 繁體中文

### 範圍與前置

本文件是 [Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) 的設計提案，不是正式 Core 契約或 P3 實作。長期協調由あき負責，Grok repo 的有界文件由 Codex 單一 writer 處理。來源與 digest 見 [來源對照](../provenance/source-map.md)。

重用 P0 的相依盤點、責任邊界、遷移與負面案例。P0 當時延後 Grok runtime 是歷史狀態；本次授權允許第 7、8 節的有界 fixture 查核。這不修改 P0，也不授權提前 P3。P1 與 Codex P2 有其他 writer，本包只讀固定來源。

P3 的共同前置為：P1 已正式合併、必要審查完成、最終 Core immutable revision 與文件 digest 已固定、本設計已對齊，且另包 scope／ownership／DoD 成立。Grok 模型資格受阻時，Codex 仍可在上述前置成立後實作 Grok repo。

### 技能與程式責任

下表都是候選責任，尚未建立技能、程式、schema 或安裝器。

| 層 | Grok 接口責任與 P0 對照 |
| --- | --- |
| 技能入口 | 有界交付、規劃／實作、唯讀 review、文件、接續入口；對照 P0 E21–E24。每個入口明示適用契約、必讀 references、停止與證據要求，不整包搬 Codex SKILL.md |
| 程式適配 | 自己處理公開工具 schema、permission／deny、sandbox、model／effort 生效查核、session／cancel／resume／未知效果與 Git 外 checkpoint；不複製 Codex Desktop payload／profile 資格 |
| 驗證器 | 分開驗證固定文件／引用閉合、組裝 inventory／bytes／modes、授權身分、runtime 能力、review findings、exact-head；所有程式留 Grok repo，Core 只描述義務 |
| 審查與交付 | 作者與 reviewer 獨立。reviewer 唯讀；必要 scan 與 findings disposition 各自記錄。Grok 的 commit／push／PR／merge 由 Codex 入口統一執行 |
| 延後邊界 | Memory／Hooks／Schedulers、Orca、第三方模型映射、Codex→Grok／LiteLLM 路由、consumer rollout 均不納入 |

Grok 官方記載 project/user/plugin skill discovery；`allowed-tools` 不授予或限制工具，`model/effort/license/compatibility` 不會套用。因此技能 metadata 不能取代工具、模型與 license 的外部查核。[Skills](https://docs.x.ai/build/features/skills-plugins-marketplaces)

來源 Codex `verify-engineering-workflow.py` 只接受 Codex/Hermes synthetic label，固定回傳 runtime／identity／delivery readiness 為 false；不得改個 label 就宣稱 Grok 合格。其具體程式與測試不搬到 Core。

### 固定 Core 文件的消費設計

1. 在 Grok repo 維護建置用 lock 與驗證器；Core 不承載機器 schema 或組裝器。lock 記錄 Core repository、40 位 commit SHA、明確文件 allowlist、各檔 raw bytes 的 SHA-256、集合 digest、來源 notices，以及 Grok adapter revision／組裝器版本。
2. 先獨立核對 P1 merge 與 final SHA，再以 SHA 取得 snapshot。拒絕 branch／tag 浮動解析、未知契約版本、路徑穿越、symlink／非一般檔案與缺漏必讀文件。Runtime 只讀已驗證 snapshot，不連線追蹤 Core main。
3. 集合 digest 的提案算法：將每項寫為 `path + NUL + lowercase_sha256 + LF`，以 UTF-8 POSIX 相對路徑排序後串接，對串接 bytes 做 SHA-256。拒絕重複、非正規路徑、NUL／CR／LF。文件原 bytes 不做換行／Unicode／雙語正規化；算法須於 P3 固定及測試。
4. lock 包含被允許且閉合的 Markdown 相對引用與 notices。正式契約原 bytes／章節／語言權威不因展示需求改變；翻譯如需新增，另存清楚的非權威說明並維持對照。
5. Core 更新必須審查新舊義務與完整相依，重新做受影響遵循驗證；不可沿用舊 revision／digest 的 receipt。此處 P0 digest 僅為來源證據，不是 final runtime lock。

### 組裝與安裝設計

Grok 維持自己的 canonical skills/references 與明確 package allowlist，generated copies 由單一組裝器重建；參考 P0 E18–E20、E30–E33，不把 Codex catalog／installer 手寫清單直接當成 Grok 來源。

未來組裝先在臨時 staging 驗證 inventory、依賴閉合、bytes／modes、完整 notices、唯一 skill 名稱與 path safety。分別驗證 source、plugin 與臨時 filesystem 佈局；plugin 不得夾帶未授權 hooks／MCP 啟動器。Installer 先 preview 精確目標、碰撞、備份與來源版本，再處理核可臨時目標。不得覆寫既有技能、向父目錄擴權或自行 promotion。

驗收失敗保留 last verified revision/digest 與 staging 證據，不安裝、不 promotion。以舊固定 snapshot 在另一臨時目標重建作恢復設計；沒有測過的 rollback 不寫 Passed。正式資料刪除、全域安裝、consumer rollout 仍需另案授權。

### 負面驗證與停止

| 類別 | 必要案例與預期 |
| --- | --- |
| 文件／來源 | missing／tampered Markdown、wrong SHA／digest、未知 revision、漏必讀引用、broken anchor、混用來源：拒絕組裝 |
| 檔案安全 | traversal／absolute path／symlink／非一般檔案、duplicate skill、inventory 額外檔與 mode 漂移：停止，不覆寫 |
| 權限 | 同時 allow/deny 的無害動作必須 deny；sandbox 的 read/write/rename deny 必須各測；不得只測 read 工具 |
| 範圍 | 明列 CWD、Grok home、system 與 temp 授權；strict 不等於只可寫 CWD。在 temp 的「外部路徑」不能自動當成應阻擋案例 |
| 授權 | 缺原請求／session／action／path／revision、過期／更改請求、拒絕／cancel 後晚到同意、逾時／斷線：不得執行 |
| Session | 用完整 session ID 接續；不存在／錯誤 ID、錯 cwd／revision／owner、fork 身分變化、未知副作用：停止核對，不盲目重播 |
| 資格與證據 | help／API／exit 0、synthetic 成功、其他 runtime receipt、舊 head 的 review：不能推進 readiness |

資格計畫與實際結果分開，見 [控制介面查核](../verification/grok-control-qualification.md)。本包 Security Diff Scan 判為不適用：只新增設計 Markdown，沒有改 runtime、權限、資料邊界、依賴、程式或安裝。這不是 scan Passed。P3 若實作上述邊界須重新評估必要 scan。

<a id="design-en"></a>

## English

### Scope and prerequisites

This is the design proposal for [Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2). It is not a final Core contract or P3 implementation. あき retains coordination. One Codex writer owns these bounded Grok documents. See the [source map](../provenance/source-map.md) for fixed sources and digests.

Reuse the P0 inventory, boundaries, migration plan, and negative cases. P0 deferred Grok runtime work at that time. The current authorization permits bounded fixture checks under charter sections 7 and 8. It does not rewrite P0 or start P3. Other writers own P1 and Codex P2. This package reads fixed sources only.

P3 requires merged and reviewed P1 contracts, the final immutable Core revision and document digests, reviewed design alignment, and a separate package with scope, ownership, and DoD. A blocked Grok model route does not prevent Codex from implementing the Grok repository after those prerequisites hold.

### Skill and program ownership

These are proposed responsibilities. No skill, program, schema, or installer exists yet.

| Layer | Grok adapter responsibility and P0 link |
| --- | --- |
| Skills | Bounded delivery, planning/implementation, read-only review, docs, and continuation; P0 E21–E24. State required contracts, references, stop conditions, and evidence. Do not copy complete Codex skills |
| Programs | Own public tool schemas, permissions/deny, sandbox, effective model/effort checks, session/cancel/resume, uncertain effects, and private checkpoints. Do not copy Codex Desktop payloads or qualification |
| Validators | Separate document/reference checks, assembly inventory/bytes/modes, authorization identity, runtime checks, findings, and exact-head evidence. Keep all programs in Grok; Core states obligations only |
| Review and delivery | Keep reviewer and author independent. Reviewer is read-only. Record required scans and finding dispositions separately. Codex handles external Grok commits, pushes, PRs, and merges |
| Deferred | Memory, Hooks, Schedulers, Orca, third-party model mapping, Codex→Grok/LiteLLM routing, and consumer rollout |

Official skill documentation describes project, user, and plugin discovery. It does not apply tool restrictions or model, effort, license, and compatibility values from skill metadata. Verify those controls separately.[Skills](https://docs.x.ai/build/features/skills-plugins-marketplaces)

The Codex synthetic verifier accepts Codex/Hermes labels only and sets runtime, identity, and delivery readiness to false. A different label cannot qualify Grok. Its programs and tests stay outside Core.

### Fixed Core document consumption

1. Grok will own a build lock and validator. Core will not hold machine schemas or an assembler. Record the Core repository, full commit SHA, document allowlist, raw-byte SHA-256 for each file, set digest, source notices, adapter revision, and assembler version.
2. Verify the P1 merge and final SHA independently. Obtain a snapshot by SHA. Reject floating branches/tags, unknown contract versions, unsafe paths, symlinks, non-regular files, and missing required documents. Runtime reads verified local bytes and never follows Core main.
3. Proposed set digest: sort entries by UTF-8 POSIX relative path. Encode each as `path + NUL + lowercase_sha256 + LF`, concatenate, and apply SHA-256. Reject duplicates, noncanonical paths, and NUL/CR/LF. Do not normalize document bytes. P3 must fix and test the algorithm.
4. Include the allowed, complete Markdown reference closure and notices. Preserve contract bytes, sections, and language authority. Keep any added translation clearly non-authoritative and mapped to its source.
5. Review changed obligations and dependencies on each Core update. Repeat affected conformance checks. Old revision/digest receipts are invalid. P0 digests here are source evidence, not a final runtime lock.

### Assembly and installation

Grok will own canonical skills/references and an explicit package allowlist. One assembler will rebuild generated copies. Reuse P0 E18–E20 and E30–E33 as design evidence. Codex catalog and installer lists do not define Grok packages.

Build in temporary staging. Verify inventory, references, bytes/modes, full notices, unique skill names, and path safety. Check source, plugin, and temporary filesystem layouts separately. Plugins must not add unauthorized hooks or MCP launchers. Preview the exact install target, collisions, backup, and source version before an approved temporary installation. Do not overwrite existing skills, widen parent-directory access, or promote automatically.

On failure, retain the last verified revision/digest and staging evidence. Do not install or promote. Recovery design rebuilds the old snapshot in another temporary target. An untested rollback is not Passed. Data deletion, global installation, and consumer rollout require separate authorization.

### Negative cases and stops

| Category | Required case and result |
| --- | --- |
| Documents/sources | Missing/tampered files, wrong SHA/digest, unknown revision, missing references, broken anchors, mixed sources: reject assembly |
| File safety | Traversal, absolute paths, symlinks, non-regular files, duplicate skills, extra inventory, mode drift: stop without overwrite |
| Permission | Deny must beat allow for a harmless action. Test sandbox read, write, and rename deny independently across tools |
| Scope | Record CWD, Grok home, system, and temp grants. Strict does not mean CWD-only writes. An outside path in temp is not automatically a negative case |
| Authorization | Missing or changed request/session/action/path/revision, expired approval, late approval after reject/cancel, timeout/disconnect: do not execute |
| Session | Resume by full session ID. Missing/wrong ID, changed cwd/revision/owner, fork identity, or uncertain effects: stop and reconcile before replay |
| Evidence | Help/API/exit 0, synthetic success, another runtime receipt, or old-head review cannot advance readiness |

See [control qualification](../verification/grok-control-qualification.md) for separate planned and observed results. Security Diff Scan is not applicable to this package: only design Markdown is added. It changes no runtime, permission, data boundary, dependency, program, or installer. This is not scan Passed. Reassess scan requirements when P3 implements those boundaries.

### 文件品質 / Document quality

[ASD-STE100 官方入口](https://www.asd-ste100.org/) 與正式 PDF 本次回傳 403，未取得完整標準。英文依 ASD-STE100 原則編寫，尚未完成完整符合性驗證；繁體中文只採清晰性原則，不宣稱符合英文標準。

The official ASD-STE100 site and PDF returned 403. The full standard was not obtained. English follows ASD-STE100 principles; full conformity is unverified. Chinese uses clarity principles and does not claim conformity with an English standard.
