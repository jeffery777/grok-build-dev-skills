# grok-build-dev-skills

[繁體中文](#zh-tw) · [English](#en)

<a id="zh-tw"></a>
<details open>
<summary>繁體中文</summary>

## 用途與目前狀態

**目前工作候選為 0.2.0，尚未發行或更新現行安裝。** 新增兩個既有技能的 [GitNexus 操作入口](references/gitnexus-operations.md)，配對 Codex 0.35.0 候選、Core 0.1.0、GitNexus 精確 1.6.12。編排方指定時機及 Codex/Grok 任一端為唯一 index writer。2026-10-18 在隔離 fixture 的 Grok 1.0.62 原生觀察已完整讀取兩技能及必要 Core，並精確執行一次唯讀 plan；這不代表原生 refresh 或整體 runtime 合格。證據分層與支援矩陣見 [候選設計](docs/design/gitnexus-operation-parity.md) 與 [驗收範圍](docs/verification/gitnexus-operation-acceptance.md)。另見 [0.2.0 候選說明](docs/releases/v0.2.0.md)。下列 0.1.0 發行資訊保留歷史。

本專案準備讓 Grok Build 使用固定版本的共用工程規範，並在 Grok 端管理技能、工具適配、驗證及組裝安裝。

本專案適合維護 AI 開發流程的工程人員。例如，團隊想讓 Grok 在修改程式前讀取共同規範、在合併前保留審查證據，可先用這份設計確認所需能力與限制。

**版本 `0.1.0` 提供官方 plugin 格式的兩個技能與二十三檔離線套件，內含正式 Core v0.1.0。** 固定 Core commit `174df2af8dedf813b9bd4e3c184a627ee87d3cd8`；不必另外安裝 Core，兩專案各自管理版本。從 [正式 Release](https://github.com/jeffery777/grok-build-dev-skills/releases/tag/v0.1.0) 核對產品 tag 解析後的完整來源 commit 與 digest，再讀 [更新紀錄](CHANGELOG.md)、[發行說明](docs/releases/v0.1.0.md) 及 [安裝／更新／回復](docs/installation.md)。技能與離線介面見 [組裝設計](docs/design/p3-g-skill-assembly.md)、[委派證據與缺口](docs/verification/grok-delegation-capabilities.md) 及 [固定 Core 消費](docs/design/p3-g-core-consumption.md)。

[Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) 為設計完成、保留歷史且仍 OPEN 的非阻擋追蹤案。離線來源／套件發行不要求重跑官方 sandbox／deny／resume QA；此次有界 plan 觀察不升級整體 runtime 資格或離線 packet 的 false readiness。

## 如何開始

P1 已抽取共用契約；本包以固定 commit revision 與內容指紋 digest 鎖定文件。使用既有 Python 3.10+ 及標準函式庫（[平台限制](docs/design/p3-g-core-consumption.md#驗證邊界)），在 repo root 執行：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/core_snapshot.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py capabilities
```

Core 命令驗十三檔，package 命令驗三十檔候選 bundle，分別輸出產品版本、Core revision／digest 及 Grok 文件版本。能力目錄保留 `1.0.52 (0920c8169e27)`；2026-10-17 非模型 help 觀察為 `1.0.60 (01a8e1c591c0)`，兩者皆非相容版本範圍認證。正式 Core tag object `e984c880a05065c8bcd0d78e83d78220b05bfc32` 解析至上述 commit；lock 固定 commit 與十二份 Markdown collection，不追蹤 moving main 或動態 tag。十三檔形成完整相對引用閉合，不表示 runtime 每次載入全部文件。

成功只證明離線內容與引用，不代表原生 plugin 安裝、技能載入、委派或 runtime 合格。Packet 是 consumer 證據封裝，不是 Grok API schema；所有 readiness 保持 false。發行範圍是已核驗來源與離線套件。實裝前另核對原生寫入集合、ownership、信任、payload／Core 引用及失敗保全，詳見 [最小整合項目](docs/installation.md#native-integration-zh)。未實測不列為 PASS，也不冒稱缺陷；[P2-G 設計](docs/design/p2-g-preparation.md) 與 [來源對照](docs/provenance/source-map.md) 保留歷史。

依賴為既有 Python 3.10+ 標準函式庫及適用的 POSIX 檔案系統；macOS 已有離線證據，其他 POSIX 未資格化、Windows 不支援。Git 供取得固定來源；Grok CLI 供之後原生 plugin 管理。套件不交付 Python／Grok 執行檔，不新增 MCP、hooks、服務或 API 憑證。Plugin 會與其他技能來源並列，不會替使用者修改共享技能搜尋路徑。

[engineering-workflow-core](https://github.com/jeffery777/engineering-workflow-core) 承載純 Markdown 共用義務；[codex-dev-skills](https://github.com/jeffery777/codex-dev-skills) 與本專案各自實作接口。共用文字不表示工具、sandbox、permission 或 session 行為相同。

## 採用的工作流與專案政策

兩個既有 [執行技能](skills/grok-engineering-workflow/SKILL.md) 與 [review 技能](skills/grok-review-change/SKILL.md) 已接入固定 Core 的 [風險與檢查時機](vendor/engineering-workflow-core/contracts/review-and-security.md#review-risk-timing) 及 [證據生命週期](vendor/engineering-workflow-core/contracts/workflow.md#wf-evidence-lifecycle)。先記任務風險及依據；資訊不足不默認低風險，scope／設計／影響變動就重評。高風險及早做獨立深入設計／code review 與安全分析，有實質 diff 就做必要比例掃描；開發中持續快速測試與適用廉價檢查，不等最終候選才開始深查。

有效專案政策可明定檢查時機、深度、判準及有理由的適用性例外，也可專化證據位置、保留期及歸檔方式；不得弱化必要安全、授權、保存、獨立 review、exact-head 或指令優先序。未選其他有效政策時，採固定 Core 的共用預設。最終候選綁定必要驗收證據；Merge Review 查充分性、當前性與完整範圍，不機械重做全庫 deep scan。變更後依影響補測／重審／必要重掃，記重用理由與 coverage；每個新 head 仍須完整 base-to-head review。

續行與結案保留精簡原因／修正／版本／scope／outcome／替代引用及必要實質證據。新成功須覆蓋原失敗與受影響邊界；無關 PASS 或間歇問題的一次成功不代表結清。保護未解、間歇、安全／資料遺失、共享／仍引用及 review／merge／acceptance 所需記錄。可先載入索引與必要來源；來源缺失須明記未驗證，摘要不升格為原證據。

本專案未設定通用保留天數或自動清理。缺有效 retention 政策或期間時，先保留來源並記待決事項；減少上下文載入不授權刪除。實際搬移／歸檔／清理前另查政策、保護例外、引用／其他使用者、精確 scope、授權與必要 preview／dry-run；不可逆刪除須操作當下確認。本包未執行歷史清理，也不要求每份 raw log 永久保存。

## 限制與授權

本發行不自動安裝或修改用戶設定、共享技能路徑及既有內容。後續實裝由協調者安排精確寫入範圍與資料保護；發行／掃描不代替安裝證據。本產品不新增 Reason 功能、Memory／Hooks／Schedulers、模型路由或服務；上述一次有界原生觀察是驗收活動，不代表新增產品能力或追加模型授權。若日後另獲授權執行模型／resume，每次必須顯式指定已驗證 sandbox profile、初始 ask，並有可靠的授權轉交／停止通道；不可因本發行推定資格或新授權。

本專案採 [MIT License](LICENSE)。衍生設計的來源 notices 見 [upstream notices](docs/provenance/upstream-notices.md)。

</details>

<a id="en"></a>
<details>
<summary>English</summary>

## Purpose and current state

**The current working candidate is 0.2.0, not released or installed.** It adds an explicit [GitNexus entry](references/gitnexus-operations.md) to the two existing skills, paired with Codex 0.35.0 candidate, Core 0.1.0 and GitNexus exactly 1.6.12. The orchestrator chooses timing and either Codex or Grok as the sole index writer. On 2026-10-18, Grok 1.0.62 read both skills and required Core files in an isolated fixture, then ran one exact read-only plan. This does not qualify native refresh or the whole runtime. See the [design](docs/design/gitnexus-operation-parity.md) and [acceptance scope](docs/verification/gitnexus-operation-acceptance.md). See also the [0.2.0 candidate notes](docs/releases/v0.2.0.md). The 0.1.0 publication information below is historical.

This project prepares Grok Build to use a fixed set of shared engineering rules. The Grok adapter will own skills, tool integration, validation, assembly, and installation.

This project is for engineers who maintain AI development workflows. For example, a team can use this design to check what Grok needs to read shared rules before changing code and retain review evidence before a merge.

**Version `0.1.0` supplies two native-plugin-format skills and a twenty-three-file offline bundle containing formal Core v0.1.0.** Core is fixed at `174df2af8dedf813b9bd4e3c184a627ee87d3cd8` and needs no separate installation; product and Core versions are independent. Read back the full product commit behind the tag and its digests in the [formal Release](https://github.com/jeffery777/grok-build-dev-skills/releases/tag/v0.1.0), then see the [changelog](CHANGELOG.md), [release notes](docs/releases/v0.1.0.md) and [installation/update/recovery guide](docs/installation.md). See [assembly](docs/design/p3-g-skill-assembly.md), [delegation evidence/gaps](docs/verification/grok-delegation-capabilities.md) and [fixed Core consumption](docs/design/p3-g-core-consumption.md) for interfaces and limits.

[Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) remains OPEN historical tracking with its design complete. It does not block offline source/package publication or require new native sandbox/deny/resume QA. The bounded plan observation does not promote general runtime qualification or the offline packet's false readiness.

## Getting started

P1 extracted the shared contracts. This package pins their commit revision and content fingerprints, called digests. Use an existing Python 3.10+ and its standard library from the repository root ([platform limits](docs/design/p3-g-core-consumption.md#validation-limits)):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/core_snapshot.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py capabilities
```

The Core command checks thirteen files; the package command checks thirty candidate files instead of the historical twenty-three. Output separates product, Core revision/digest and documented Grok version. The catalog retains `1.0.52 (0920c8169e27)`; non-model help on 2026-10-17 observed `1.0.60 (01a8e1c591c0)`. Neither certifies a compatibility range. Formal Core tag object `e984c880a05065c8bcd0d78e83d78220b05bfc32` resolves to the fixed commit above. The lock binds that commit and twelve-Markdown collection, never moving main or a dynamic tag. Complete thirteen-file reference closure does not mean loading every document on each runtime use.

Success proves offline bytes/references, not native installation, skill loading, delegation or runtime qualification. The packet is a consumer evidence envelope, not a Grok API schema. All readiness flags remain false. Publication covers verified source and offline artifacts. Actual installation separately needs write-set, ownership, trust, payload/Core and failure-preservation checks in the [minimum integration plan](docs/installation.md#native-integration-en). Untested behavior is neither PASS nor a confirmed defect. The [P2-G design](docs/design/p2-g-preparation.md) and [source map](docs/provenance/source-map.md) retain history.

Dependencies are existing Python 3.10+ standard-library support and suitable POSIX filesystem behavior. macOS has offline evidence; other POSIX systems are unqualified and Windows is unsupported. Git obtains fixed sources; an existing Grok CLI manages plugins later. This package ships neither runtime and adds no MCP, hooks, services or API credentials. Plugins appear alongside other skill sources and do not change shared discovery paths.

[engineering-workflow-core](https://github.com/jeffery777/engineering-workflow-core) owns shared Markdown obligations. [codex-dev-skills](https://github.com/jeffery777/codex-dev-skills) and this project each own their adapter. Shared text does not prove equal tools, sandbox, permission, or session behavior.

## Adopted workflow and project policy

The existing [execution skill](skills/grok-engineering-workflow/SKILL.md) and [review skill](skills/grok-review-change/SKILL.md) now use the fixed Core [risk/timing rules](vendor/engineering-workflow-core/contracts/review-and-security.md#review-risk-timing) and [evidence lifecycle](vendor/engineering-workflow-core/contracts/workflow.md#wf-evidence-lifecycle). Record task risk and its basis first. Missing information is not low risk. Reassess scope, design or impact changes. High-risk work needs early independent in-depth design/code review and security analysis. Start required proportionate scans on a meaningful diff, with fast tests and cheap applicable checks during development. Do not wait for a final candidate to begin in-depth work.

A valid project policy may set check timing, depth, criteria and justified applicability exceptions, as well as evidence locations, retention periods and archive methods. It cannot weaken mandatory safety/security, authorization, retention, independent review, exact-head requirements or instruction priority. Use the fixed Core defaults when no other valid policy is selected. The final candidate binds acceptance evidence. Merge Review checks sufficient current coverage of the complete range; it does not automatically repeat a whole-repository deep scan. After changes, justify affected retests/reviews/necessary rescans and evidence reuse/coverage. Every changed head still needs complete base-to-head review.

At continuation and closeout, retain compact cause/fix/version/scope/outcome/replacement references and required substantive evidence. A success must cover the original failure and affected boundaries. An unrelated PASS or one success after an intermittent failure does not close it. Protect unresolved, intermittent, security/data-loss, shared, cited and review/merge/acceptance records. Load indexes and needed sources first. Mark missing sources unverified; summaries do not become original evidence.

This project sets no universal retention period or automatic cleanup. Without a valid retention policy or duration, keep sources and pending decisions. Loading less context does not authorize deletion. Actual movement/archive/cleanup requires policy, protection, references/other users, exact scope, authority and required preview/dry-run checks. Irreversible deletion needs confirmation at action time. This package performs no historical cleanup and does not require every raw log to be kept forever.

## Limits and license

This release does not automatically install, change user settings/shared skill paths or replace existing contents. The coordinator sequences later installation with exact writes and data protection. Publication/scanning cannot replace installation evidence. The product adds no Reason feature, Memory/Hooks/Schedulers, model routing or service. The bounded native observation above is acceptance work, not a new product capability or authority for another model call. Any separately authorized future model run/resume needs an explicit verified sandbox profile, initial ask and reliable approval-forwarding/stop channel on every execution. This release grants no runtime qualification or new authorization.

This project uses the [MIT License](LICENSE). See [upstream notices](docs/provenance/upstream-notices.md) for the sources of this design.

</details>
