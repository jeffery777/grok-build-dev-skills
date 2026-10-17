# grok-build-dev-skills

[繁體中文](#zh-tw) · [English](#en)

<a id="zh-tw"></a>
<details open>
<summary>繁體中文</summary>

## 用途與目前狀態

本專案準備讓 Grok Build 使用固定版本的共用工程規範，並在 Grok 端管理技能、工具適配、驗證及組裝安裝。

本專案適合維護 AI 開發流程的工程人員。例如，團隊想讓 Grok 在修改程式前讀取共同規範、在合併前保留審查證據，可先用這份設計確認所需能力與限制。

**目前提供官方 plugin 格式的離線候選 `0.1.0-candidate.1`，尚未發布。** 沿用兩個技能、能力證據格式與全新臨時組裝；技能尚未安裝／啟用，[Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) 的 Grok runtime 資格仍未完成。先讀 [安裝準備與回復限制](docs/installation.md)，再看 [技能組裝](docs/design/p3-g-skill-assembly.md)、[委派證據與缺口](docs/verification/grok-delegation-capabilities.md) 及 [固定 Core 消費](docs/design/p3-g-core-consumption.md)。

## 如何開始

P1 已抽取共用契約；本包以固定 commit revision 與內容指紋 digest 鎖定文件。使用既有 Python 3.10+ 及標準函式庫（[平台限制](docs/design/p3-g-core-consumption.md#驗證邊界)），在 repo root 執行：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/core_snapshot.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py capabilities
```

Core 命令驗固定十一檔；package 命令驗二十一檔 bundle，輸出產品版本、固定 Core revision／digest 及能力目錄的 Grok 文件版本。產品候選版本不等於 Grok CLI 版本；目錄仍記錄 `1.0.52 (0920c8169e27)`，本次非模型 help 觀察到的執行檔為 `1.0.60 (01a8e1c591c0)`。Core 固定 `64b19bb5658432c42cd6a26aa357fd6b1d0fd857`，使用者不必另外安裝 Core。

成功只證明離線內容與引用，不代表原生 plugin 安裝、技能載入、委派或 runtime 合格。Packet 是 consumer 證據封裝，不是 Grok API schema；所有 readiness 保持 false。官方 plugin 的自訂內容保護、更新失敗回復及避免混裝仍缺實證；既有安裝的更新／重裝路線須先另行決定。本包沿用驗證器，不新增 installer 或 live transport。原始 [P2-G 設計](docs/design/p2-g-preparation.md) 與 [來源對照](docs/provenance/source-map.md) 保留歷史與對齊資訊。

[engineering-workflow-core](https://github.com/jeffery777/engineering-workflow-core) 承載純 Markdown 共用義務；[codex-dev-skills](https://github.com/jeffery777/codex-dev-skills) 與本專案各自實作接口。共用文字不表示工具、sandbox、permission 或 session 行為相同。

## 採用的工作流與專案政策

兩個既有 [執行技能](skills/grok-engineering-workflow/SKILL.md) 與 [review 技能](skills/grok-review-change/SKILL.md) 已接入固定 Core 的 [風險與檢查時機](vendor/engineering-workflow-core/contracts/review-and-security.md#review-risk-timing) 及 [證據生命週期](vendor/engineering-workflow-core/contracts/workflow.md#wf-evidence-lifecycle)。先記任務風險及依據；資訊不足不默認低風險，scope／設計／影響變動就重評。高風險及早做獨立深入設計／code review 與安全分析，有實質 diff 就做必要比例掃描；開發中持續快速測試與適用廉價檢查，不等最終候選才開始深查。

有效專案政策可明定檢查時機、深度、判準及有理由的適用性例外，也可專化證據位置、保留期及歸檔方式；不得弱化必要安全、授權、保存、獨立 review、exact-head 或指令優先序。未選其他有效政策時，採固定 Core 的共用預設。最終候選綁定必要驗收證據；Merge Review 查充分性、當前性與完整範圍，不機械重做全庫 deep scan。變更後依影響補測／重審／必要重掃，記重用理由與 coverage；每個新 head 仍須完整 base-to-head review。

續行與結案保留精簡原因／修正／版本／scope／outcome／替代引用及必要實質證據。新成功須覆蓋原失敗與受影響邊界；無關 PASS 或間歇問題的一次成功不代表結清。保護未解、間歇、安全／資料遺失、共享／仍引用及 review／merge／acceptance 所需記錄。可先載入索引與必要來源；來源缺失須明記未驗證，摘要不升格為原證據。

本專案未設定通用保留天數或自動清理。缺有效 retention 政策或期間時，先保留來源並記待決事項；減少上下文載入不授權刪除。實際搬移／歸檔／清理前另查政策、保護例外、引用／其他使用者、精確 scope、授權與必要 preview／dry-run；不可逆刪除須操作當下確認。本包未執行歷史清理，也不要求每份 raw log 永久保存。

## 限制與授權

本包不部署、不發布 Tag／Release、不更新既有技能或全域設定，不啟用 Memory／Hooks／Schedulers。模型執行及 resume 必須顯式指定已驗證的 sandbox profile，初始 permission 為 ask；沒有可靠授權通道即停止。新的授權交回あき與使用者，不能以逾時或沉默代替同意。

本專案採 [MIT License](LICENSE)。衍生設計的來源 notices 見 [upstream notices](docs/provenance/upstream-notices.md)。

</details>

<a id="en"></a>
<details>
<summary>English</summary>

## Purpose and current state

This project prepares Grok Build to use a fixed set of shared engineering rules. The Grok adapter will own skills, tool integration, validation, assembly, and installation.

This project is for engineers who maintain AI development workflows. For example, a team can use this design to check what Grok needs to read shared rules before changing code and retain review evidence before a merge.

**The current official-plugin-format offline candidate is `0.1.0-candidate.1`, unreleased.** It retains two skill sources, consumer capability evidence and fresh temporary assembly. Skills are not installed or activated. Grok runtime qualification under [Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) is incomplete. Start with [installation preparation and recovery limits](docs/installation.md), then read [skill assembly](docs/design/p3-g-skill-assembly.md), [delegation evidence and gaps](docs/verification/grok-delegation-capabilities.md), and [fixed Core consumption](docs/design/p3-g-core-consumption.md).

## Getting started

P1 extracted the shared contracts. This package pins their commit revision and content fingerprints, called digests. Use an existing Python 3.10+ and its standard library from the repository root ([platform limits](docs/design/p3-g-core-consumption.md#validation-limits)):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/core_snapshot.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py capabilities
```

The Core command verifies eleven fixed files; the package command verifies a twenty-one-file bundle. Its output identifies the product version, fixed Core revision/digest and documented Grok catalog version. The product candidate is separate from Grok CLI: the catalog retains `1.0.52 (0920c8169e27)`, while this non-model help check observed executable `1.0.60 (01a8e1c591c0)`. Core stays pinned to `64b19bb5658432c42cd6a26aa357fd6b1d0fd857`; users need no separate Core installation.

Success proves offline bytes/references, not native plugin installation, skill loading, delegation or runtime qualification. The packet is a consumer evidence envelope, not a Grok API schema. All readiness flags stay false. Native custom-content preservation, failed-update recovery and prevention of mixed installs lack evidence; updating or reinstalling an existing installation needs a separate decision. This package reuses the verifier without an installer or live transport. The [P2-G design](docs/design/p2-g-preparation.md) and [source map](docs/provenance/source-map.md) retain history and alignment information.

[engineering-workflow-core](https://github.com/jeffery777/engineering-workflow-core) owns shared Markdown obligations. [codex-dev-skills](https://github.com/jeffery777/codex-dev-skills) and this project each own their adapter. Shared text does not prove equal tools, sandbox, permission, or session behavior.

## Adopted workflow and project policy

The existing [execution skill](skills/grok-engineering-workflow/SKILL.md) and [review skill](skills/grok-review-change/SKILL.md) now use the fixed Core [risk/timing rules](vendor/engineering-workflow-core/contracts/review-and-security.md#review-risk-timing) and [evidence lifecycle](vendor/engineering-workflow-core/contracts/workflow.md#wf-evidence-lifecycle). Record task risk and its basis first. Missing information is not low risk. Reassess scope, design or impact changes. High-risk work needs early independent in-depth design/code review and security analysis. Start required proportionate scans on a meaningful diff, with fast tests and cheap applicable checks during development. Do not wait for a final candidate to begin in-depth work.

A valid project policy may set check timing, depth, criteria and justified applicability exceptions, as well as evidence locations, retention periods and archive methods. It cannot weaken mandatory safety/security, authorization, retention, independent review, exact-head requirements or instruction priority. Use the fixed Core defaults when no other valid policy is selected. The final candidate binds acceptance evidence. Merge Review checks sufficient current coverage of the complete range; it does not automatically repeat a whole-repository deep scan. After changes, justify affected retests/reviews/necessary rescans and evidence reuse/coverage. Every changed head still needs complete base-to-head review.

At continuation and closeout, retain compact cause/fix/version/scope/outcome/replacement references and required substantive evidence. A success must cover the original failure and affected boundaries. An unrelated PASS or one success after an intermittent failure does not close it. Protect unresolved, intermittent, security/data-loss, shared, cited and review/merge/acceptance records. Load indexes and needed sources first. Mark missing sources unverified; summaries do not become original evidence.

This project sets no universal retention period or automatic cleanup. Without a valid retention policy or duration, keep sources and pending decisions. Loading less context does not authorize deletion. Actual movement/archive/cleanup requires policy, protection, references/other users, exact scope, authority and required preview/dry-run checks. Irreversible deletion needs confirmation at action time. This package performs no historical cleanup and does not require every raw log to be kept forever.

## Limits and license

This package does not deploy, publish tags or releases, update existing skills or global settings, or enable Memory, Hooks, or Schedulers. Every model run and resume must specify a verified sandbox profile. Initial permission must be ask. Stop when no reliable authorization channel exists. Return new authorization requests to あき and the user. Silence and timeout do not grant permission.

This project uses the [MIT License](LICENSE). See [upstream notices](docs/provenance/upstream-notices.md) for the sources of this design.

</details>
