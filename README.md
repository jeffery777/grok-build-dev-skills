# grok-build-dev-skills

[繁體中文](#zh-tw) · [English](#en)

<a id="zh-tw"></a>
<details open>
<summary>繁體中文</summary>

## 用途與目前狀態

本專案準備讓 Grok Build 使用固定版本的共用工程規範，並在 Grok 端管理技能、工具適配、驗證及組裝安裝。

本專案適合維護 AI 開發流程的工程人員。例如，團隊想讓 Grok 在修改程式前讀取共同規範、在合併前保留審查證據，可先用這份設計確認所需能力與限制。

**目前只有 P2-G（Grok 前置設計階段）的設計與資格查核紀錄，沒有可安裝技能或執行程式。** [Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) 的 strict 啟動前檢查無法套用 sandbox，已停止模型路線；Grok runtime 尚未合格。請先閱讀 [控制介面查核](docs/verification/grok-control-qualification.md)。

## 如何開始

閱讀 [P2-G 準備設計](docs/design/p2-g-preparation.md) 與 [來源對照](docs/provenance/source-map.md)。本階段不提供安裝命令。P1 是共用契約抽取階段；正式 P3 接口實作須另立工作包，先確認 P1 已合併，並以不可變的 commit revision 與內容指紋 digest 固定 Core 文件，再完成設計對齊。

[engineering-workflow-core](https://github.com/jeffery777/engineering-workflow-core) 承載純 Markdown 共用義務；[codex-dev-skills](https://github.com/jeffery777/codex-dev-skills) 與本專案各自實作接口。共用文字不表示工具、sandbox、permission 或 session 行為相同。

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

**This repository contains design and qualification records for P2-G, the Grok preparation stage. It has no installable skills or executable adapter.** The strict startup check for [Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) could not apply the sandbox. The model route stopped. Grok runtime qualification remains blocked. Read the [control qualification record](docs/verification/grok-control-qualification.md) first.

## Getting started

Read the [P2-G design](docs/design/p2-g-preparation.md) and [source map](docs/provenance/source-map.md). There is no installation command at this stage. P1 extracts the shared contracts. P3 implements the adapters in separate work packages. It requires merged P1 contracts, a fixed Core commit revision and content fingerprints called digests, and reviewed design alignment.

[engineering-workflow-core](https://github.com/jeffery777/engineering-workflow-core) owns shared Markdown obligations. [codex-dev-skills](https://github.com/jeffery777/codex-dev-skills) and this project each own their adapter. Shared text does not prove equal tools, sandbox, permission, or session behavior.

## Limits and license

This package does not deploy, publish tags or releases, update existing skills or global settings, or enable Memory, Hooks, or Schedulers. Every model run and resume must specify a verified sandbox profile. Initial permission must be ask. Stop when no reliable authorization channel exists. Return new authorization requests to あき and the user. Silence and timeout do not grant permission.

This project uses the [MIT License](LICENSE). See [upstream notices](docs/provenance/upstream-notices.md) for the sources of this design.

</details>
