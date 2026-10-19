# Grok 離線技能組裝 / Offline skill assembly

目前來源準備／Current source preparation：`0.2.2`，Core v0.1.1 commit `7b66978a76597d09be1b55ad199a969b4ee59c0f`，十四份 Core／三十一檔 bundle。未發布或安裝／Not published or installed. 下列各 Issue 段落保留當時歷史；技術節說明現行佈局。Issue-specific paragraphs retain history; technical sections describe the current layout.
[繁體中文](#zh) · [English](#en)

<a id="zh"></a>

## 繁體中文

[Issue #6](https://github.com/jeffery777/grok-build-dev-skills/issues/6) 承接已驗收的 [P3-G1](p3-g-core-consumption.md)，提供兩個技能原稿、Grok 能力對照、consumer 證據格式及全新臨時組裝。Core 固定於 `b4c37798b6d3a9efd91c8c6d518093f2dd847a98`；lock、十一份原 bytes 與完整 notices 不變。協調入口見 [Program Open Issues](https://chatgpt.com/space/page_548d81ee2cf08191a144063ee8fe571b)。

上述 Issue #6 是原組裝包的歷史身分。[G-W1 / Issue #16](https://github.com/jeffery777/grok-build-dev-skills/issues/16) 當時將 Core 更新為 `345cd601bffbacc777f87fb24f22b5caefa30a3b`，並讓兩技能引用 [共用寫作條款](../../vendor/engineering-workflow-core/contracts/workflow.md#wf-writing)，沿用 Docs Sync 與 coherence review。Lock、原 bytes、code-owned anchors 與 manifest 同包更新；完整 notices、離線邊界與 readiness 限制保留。

[GG1 / Issue #18](https://github.com/jeffery777/grok-build-dev-skills/issues/18) 當時固定 Core `784ed24f4a09ec35ac7209e0fd2287b214aea260`，保留寫作採用，將風險起始／變動重評、早期設計／code／安全工作及證據替代／保護接入既有執行、委派 brief、review 與 closeout。有效 [專案政策](../../README.md#採用的工作流與專案政策) 在 mandatory obligations 內專化，不新增控制器、gate 或清理框架；snapshot／lock／程式 anchors／manifest／受影響測試同包對齊。

[G-SA1 / Issue #20](https://github.com/jeffery777/grok-build-dev-skills/issues/20) 當時固定 Core `3a3fd41e5fb994b4429a67d76d1b0655d972d150`。兩技能與 mapping 引用 Core 的安全適用性及證據／續行條款，保留 Grok 方法、工具、模型、資料與 session 邊界。Lock、兩份變更的 Core 原 bytes、程式常數、manifest 與受影響驗證同步；完整來源見 [provenance](../provenance/source-map.md)。不改組裝介面、演算法或 false readiness。

[G-RF1 / Issue #22](https://github.com/jeffery777/grok-build-dev-skills/issues/22) 當時固定 Core `64b19bb5658432c42cd6a26aa357fd6b1d0fd857`。兩技能在適用的規劃、續行與審查處導讀 [共用前提及方案條款](../../vendor/engineering-workflow-core/contracts/workflow.md#wf-assumptions-and-options)，將相關評估寫入既有 plan／report，不新增表單、schema 或 gate。四份 generated changes、lock、兩個程式常數與 manifest 同步；十九個 payload、完整 notices、組裝介面與 false readiness 保留。

[G-PI1 / Issue #24](https://github.com/jeffery777/grok-build-dev-skills/issues/24) 保留上述 Core 與兩技能原 bytes，新增官方 root [plugin.json](../../plugin.json) 與明確未發布的產品版本 `0.1.0-candidate.1`。沿用 verifier／staging helper，不新增 installer。上段十九個 payload 是 G-RF1 的歷史佈局；G-PI1 當時為二十個 payload 加 manifest 共二十一檔，後續 v0.1.0 當時為二十三檔。[安裝準備與回復限制](../installation.md) 說明官方路線的保障缺口及停止點。

### 來源與組裝

[workflow 技能](../../skills/grok-engineering-workflow/SKILL.md) 與 [review 技能](../../skills/grok-review-change/SKILL.md) 保留最小入口，必讀固定 Core 與 [Grok references](../../references/grok-capabilities.md)。原稿放在 `skills/`，沒有寫入 `.grok/skills`、使用者技能或 plugin discovery roots。Skill 觸發只載入指引，不產生工具、模型／effort 實效、runtime 資格或操作權。

[grok.package.json](../../grok.package.json) 是 consumer 自有 package format。它列出三十個 payload path／SHA-256；另隨包保留 manifest 原 bytes，因此 staging 共三十一檔。Manifest 不 hash 自己；輸出另記其 raw SHA-256、產品版本、Core revision／collection 與 Grok 文件版本。Plugin metadata 僅接受固定 name／version／description，不加入 hooks、MCP 或 permissions。來源 inventory 允許開發用 docs/tests，但 skills/references/capabilities 三個 owned roots 必須 exact。Staging 整個 root 必須 exact，不夾帶其他檔案；source PASS 不能用來放行既有安裝樹。

Manifest 與執行的 verifier 必須來自已審的可信固定 Git revision。檢查可疑副本時，執行可信來源的 verifier，以 `--root` 選副本、`--layout staging` 查整樹，並以 `--expected-manifest-sha256` 指定從可信來源另取得的 raw manifest digest；在解析 payload 與建立目標前即比對。不能用可疑副本自己的程式建立信任。若未提供可信 digest，可同時改寫 manifest 與技能的同權限攻擊者不在該檢查的完整性保障內。Digest 不驗簽章、來源真實性、ownership 或人類授權。Core 另由 G1 的 code-owned revision／集合／LICENSE anchors 驗證，不能靠改 package manifest 替換 Core。

共用 staging helper 先驗 captured bytes／canonical paths，僅在 canonical 系統暫存目錄下建立全新目標，且位於 configured source 及執行程式 repo 之外。No-follow descriptors、regular/single-link 0644 files、單檔 1 MiB、exclusive creation、0700 directories、讀回與 inode 查核維持。失敗保留新 partial target，先檢視，不盲目覆寫、刪除或重播。G1 CLI 行為保持；現行固定來源見 lock。

### 離線命令

使用既有 Python 3.10+ 標準函式庫，不安裝依賴。在 repo root 使用[共用離線命令](#offline-command-examples)，驗來源、檢視 documented 能力、執行測試、建立全新 staging 並驗搬移後的 package。

Source 與 staging 的相對佈局相同；可搬移的 bundle 含兩個 verifier，沒有 installer 或 Grok launcher。CLI 不會執行 bundle 內的技能或其他程式。`--root` 選可信本地來源／副本，`--layout` 明選 source 或 staging。成功 exit 0 只證明該離線動作；受限 JSON／filesystem 拒絕 exit 1，用法錯誤 exit 2。錯誤不回印 packet 或 filesystem path；命令列用法診斷遵循 argparse。

### Consumer 證據 packet

此格式只封裝相關工具名稱的 fixture 或 operator report，**不是 Grok 相容 API schema**，不接受 session／approval／runtime-ready 欄位。假例與命令見[共用 packet 範例](#consumer-packet-example)。

以共用範例中的 packet 命令驗其結構；packet 可為 0600 一般單連結檔，仍有 no-follow 與 size limit。來源 digest 是宣告，不驗證實際 capture 或完整 tool schema。輸出只標 `fixture_only`、`operator_report_unverified` 或 `not_supplied`；兩種 report 都不能升級 schema／runtime 資格。四個 readiness 欄位固定 false，G2-R01–R06 明列仍缺 sandbox/deny、loaded schema/model、派工、授權通道、session recovery、skill loading／entitlement。

### 驗收與邊界

測試涵蓋 source/staging、搬移後 verifier、manifest／Core／引用漂移、duplicate skill、非法 paths、symlink/hardlink/FIFO/modes、既有目標保留、packet 偽造／外來工具／重複 key／整數及 nesting 例外，以及永遠 false 的 readiness。Independent Codex forward-test 只測離線技能指引，不是 Grok skill-loading 或模型資格。

後續 [委派資格清單](../verification/grok-delegation-capabilities.md) 保持未測／blocked；沒有 live ACP、模型、API、訂閱／付費授權、全域設定、安裝或 rollout。Windows 不支援；其他 POSIX 平台未資格化。英文依清晰性／ASD-STE100 原則，完整符合性未驗證。

<a id="en"></a>

## English

[Issue #6](https://github.com/jeffery777/grok-build-dev-skills/issues/6) extends the accepted [P3-G1 package](p3-g-core-consumption.md). It adds two skill sources, focused Grok references, a consumer evidence envelope and fresh temporary assembly. Core stays fixed at `b4c37798b6d3a9efd91c8c6d518093f2dd847a98`; its lock, eleven raw files and complete notices do not change. See [Program Open Issues](https://chatgpt.com/space/page_548d81ee2cf08191a144063ee8fe571b) for coordination.

Issue #6 above identifies the original assembly package. [G-W1 / Issue #16](https://github.com/jeffery777/grok-build-dev-skills/issues/16) updated Core at that time to `345cd601bffbacc777f87fb24f22b5caefa30a3b`. Both skills refer to the shared [plain-writing requirements](../../vendor/engineering-workflow-core/contracts/workflow.md#wf-writing) within Docs Sync and coherence review. The lock, raw files, code-owned anchors and manifest change together. Complete notices, offline boundaries and readiness limits remain.

[GG1 / Issue #18](https://github.com/jeffery777/grok-build-dev-skills/issues/18) pinned Core `784ed24f4a09ec35ac7209e0fd2287b214aea260` and preserves writing adoption. Existing execution, delegation briefs, review and closeout now apply risk reassessment, early design/code/security work, evidence replacement coverage and retention protection. Valid [project policy](../../README.md#adopted-workflow-and-project-policy) specializes within mandatory obligations; no controller, gate or cleanup framework is added. Snapshot, lock, code anchors, manifest and affected tests change together.

[G-SA1 / Issue #20](https://github.com/jeffery777/grok-build-dev-skills/issues/20) pinned Core at that time to `3a3fd41e5fb994b4429a67d76d1b0655d972d150`. Both skills and the mapping reference shared security applicability and evidence/continuation rules while retaining Grok method, tool, model, data and session boundaries. The lock, two changed Core raw files, code constants, manifest and affected verification change together; see [provenance](../provenance/source-map.md). Assembly interfaces, algorithms and false readiness remain unchanged.

[G-RF1 / Issue #22](https://github.com/jeffery777/grok-build-dev-skills/issues/22) previously pinned Core `64b19bb5658432c42cd6a26aa357fd6b1d0fd857`. Both skills conditionally refer planning, continuation and review to the [shared assumptions and options clause](../../vendor/engineering-workflow-core/contracts/workflow.md#wf-assumptions-and-options). Relevant assessments stay in the existing plan/report, without a new form, schema or gate. Four generated changes, the lock, two code constants and manifest change together. The nineteen payload files, full notices, assembly interfaces and false readiness remain.

[G-PI1 / Issue #24](https://github.com/jeffery777/grok-build-dev-skills/issues/24) retains the Core and both skills byte for byte. It adds official root [plugin.json](../../plugin.json) metadata with the explicitly unreleased product version `0.1.0-candidate.1`. The existing verifier/staging helper remains; no installer is added. The nineteen payload files above describe G-RF1's historical layout. G-PI1 had twenty payload files plus the manifest, twenty-one total. The historical v0.1.0 release had twenty-two payload files plus the manifest, twenty-three total after formal Core closure expansion. See [installation preparation and recovery limits](../installation.md) for native-route gaps and stop conditions.

### Sources and assembly

The [workflow skill](../../skills/grok-engineering-workflow/SKILL.md) and [review skill](../../skills/grok-review-change/SKILL.md) are minimal entry points. They require the fixed Core contracts and [Grok references](../../references/grok-capabilities.md). Sources live under `skills/`; this package does not write to `.grok/skills`, user skills or plugin discovery roots. A skill trigger loads guidance. It creates no tools, effective model/effort setting, runtime qualification or action authority.

[grok.package.json](../../grok.package.json) is a consumer-owned format. It lists thirty payload paths and SHA-256 digests. The original manifest travels with them as file thirty-one; it does not hash itself. Output reports its raw SHA-256, product version, Core revision/collection and documented Grok version separately. Plugin metadata accepts only the fixed name/version/description, with no hooks, MCP or permissions. Source layout permits development docs/tests but requires exact `skills/`, `references/` and `capabilities/` roots. Staging requires the exact whole package with no extra files. A source PASS cannot clear an existing installed tree.

The manifest and executing verifier must come from a reviewed, trusted, fixed Git revision. Check a suspect copy with that trusted verifier: use `--root` for the copy, `--layout staging` for its whole tree and `--expected-manifest-sha256` for the raw manifest digest obtained independently from the trusted source. The digest is compared before payload parsing or target creation. Never establish trust by executing the suspect copy's own code. Without a trusted digest, an actor who can rewrite payload and manifest is outside that check's integrity guarantee. Digests do not establish signatures, source authenticity, ownership or human authorization. Core has separate G1 code-owned revision, collection and LICENSE anchors; changing package hashes alone cannot replace it.

The shared staging helper validates captured bytes and canonical paths before writing. It creates a new target below canonical system temporary roots, outside both the configured source and executing repository. It retains no-follow descriptors, regular single-link 0644 files, the 1 MiB per-file limit, exclusive creation, 0700 directories, complete readback and inode checks. A failed fresh target remains for inspection. Do not blindly replay, overwrite or delete it. G1 CLI behavior stays unchanged; the lock identifies the current fixed source.

### Offline commands

Use an existing Python 3.10+ and its standard library; install no dependencies. From the repository root, use the [shared offline commands](#offline-command-examples) to verify sources, inspect documented capabilities, run tests, create fresh staging and verify the relocated package.

Source and staging use the same relative layout. The relocated bundle contains both verifiers and no installer or Grok launcher. The CLI does not invoke skills or run other programs. `--root` selects a trusted local source or copy; `--layout` selects source or staging. Exit 0 validates only that offline action; invalid data/files exit 1, usage errors exit 2. Data/file errors do not echo packet contents or filesystem paths. Argparse handles command-line usage diagnostics.

### Consumer evidence packet

The packet holds only relevant tool names from a fixture or operator report. It is **not a Grok API schema** and accepts no session, approval or runtime-ready fields. See the [shared packet example and command](#consumer-packet-example).

A packet may be a 0600 regular single-link file; no-follow checks and the size limit still apply. Its source digest is a claim, not authentication of a capture or validation of the full tool schema. Output labels observations only as `fixture_only`, `operator_report_unverified` or `not_supplied`. Neither report type qualifies schemas or runtime behavior. All four runtime, skill-loading, delegation and delivery flags remain false. G2-R01–R06 retain the sandbox/deny, loaded schema/model, delegation, authorization-channel, session-recovery and loading/entitlement gaps.

### Verification and limits

Tests cover source/staging layouts, relocated verification, manifest/Core/reference drift, duplicate skill identities, unsafe paths, symlinks/hardlinks/FIFOs/modes, existing-target preservation, forged packets, foreign tools, duplicate keys, integer/nesting errors and false readiness. Independent Codex forward-testing checks offline skill guidance, not Grok skill loading or model qualification.

The [qualification checklist](../verification/grok-delegation-capabilities.md#en) remains untested or blocked. This package includes no live ACP, model or API execution, subscription/paid-service authorization, global setting, installation or rollout. macOS is tested; other POSIX platforms remain unqualified and Windows is unsupported. English follows clarity/ASD-STE100 principles; full conformity is unverified.

<a id="offline-command-examples"></a>

## 共用離線命令 / Shared offline commands

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py capabilities
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
p3g_parent="$(mktemp -d /private/tmp/grok-package.XXXXXX)"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py stage --destination "$p3g_parent/package"
PYTHONDONTWRITEBYTECODE=1 python3 "$p3g_parent/package/scripts/grok_package.py" verify --layout staging
```

<a id="consumer-packet-example"></a>

## 共用 packet 範例 / Shared packet example

```json
{"format":"grok-consumer-evidence/v1","runtime":"grok-build","documented_version":"1.0.52 (0920c8169e27)","source":{"kind":"fixture","sha256":"0000000000000000000000000000000000000000000000000000000000000000"},"observed_tool_names":["spawn_subagent"]}
```

Packet 命令 / Packet command: `python3 scripts/grok_package.py packet --packet <local-file>`.

## G-REL1 初步準備歷史 / Preliminary preparation history

[Issue #26](https://github.com/jeffery777/grok-build-dev-skills/issues/26) 基於已合併 PR25 的 main `e21a18bcd8ca833a590fcec1ba589d3529ab485a`，沿用兩技能、官方 plugin metadata 與二十一檔 bundle，不新增 installer。產品改為 `0.1.0`，狀態 **UNRELEASED／WAITING_CORE_PIN**；上方 `0.1.0-candidate.1` 是 G-PI1 歷史。Core `64b19bb5658432c42cd6a26aa357fd6b1d0fd857` 暫留，等待協調者提供 Core v0.1.0 正式 tag／完整 commit，並非最後發行 pin。This preparation retains the existing payload and algorithms. The product version is unreleased; historical candidate markers do not identify the active product. The final Core release identity is still pending.

新 [CHANGELOG](../../CHANGELOG.md)、[release notes 草稿](../releases/v0.1.0.md) 與 [安裝指引](../installation.md) 區分來源／離線套件可發布範圍及尚未執行的最小原生整合。新 metadata／描述及對應負例與 manifest 同步；既有 Core 原檔、lock、Core verifier、技能、catalog／mapping 與 runtime false flags 保持不變。本輪只讀本地 version／help，不執行 native validate／install、模型或設定變更，不重開 Issue #2。Bilingual release/install documents distinguish offline artifacts from future native writes, ownership, trust, payload/Core closure and recovery. New bytes need their own affected checks and independent review. Final release/security/exact-head gates must cover the eventual formal Core pin; this preparation is not that verdict.

## G-REL1 v0.1.0 正式相依 / Formal release dependency

[Issue #26](https://github.com/jeffery777/grok-build-dev-skills/issues/26) 已取得正式 Core v0.1.0，固定 commit `174df2af8dedf813b9bd4e3c184a627ee87d3cd8`；annotated tag object 為 `e984c880a05065c8bcd0d78e83d78220b05bfc32`，不可混作 commit。完整相對引用需要十三份 Core 原檔（十二份 Markdown＋LICENSE），因此當時 allowlist／lock／anchors／manifest 同步為二十二個 payload＋manifest，共二十三檔。其餘技能／catalog／mapping、parser、fresh staging 與 false readiness 不改；前節等待 pin 的二十一檔狀態保留為初步準備歷史。

The formal Core pin supersedes the preliminary waiting state. Complete closure of thirteen Core files expands the then-current bundle to 23 files without an installer or runtime algorithm change. Core and product versions are independent. Use the [release notes](../releases/v0.1.0.md) and [installation/update/recovery guide](../installation.md) for exact-source/digest selection and the later minimum native integration. Source/archive verification is distinct from installed-tree ownership, native trust, model adoption and runtime qualification; actual user installation remains a separate coordinated step.

## 0.2.2 接續規則配套 / Continuation alignment

[Issue #34](https://github.com/jeffery777/grok-build-dev-skills/issues/34) 固定 Core v0.1.1；兩技能仍必讀同一份完整 workflow，因此取得 Continue 的原 Session 優先及未知結果先核對指引。沒有改動技能正文、controller／S/T lock、組裝 API 或 false readiness；固定檔案與 digest 見 [來源對照](../provenance/source-map.md)。本輪僅 draft PR／發行準備，不寫入既有安裝。

Issue #34 pins Core v0.1.1. Both existing skills still require the complete workflow, including original-session preference and unknown-outcome checks. Skill bodies, controller/S/T lock, assembly APIs and false readiness remain unchanged. See [provenance](../provenance/source-map.md) for fixed files and digests. This packet stops at a draft PR/release preparation and changes no existing installation.
