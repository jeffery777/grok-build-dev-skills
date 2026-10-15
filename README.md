# grok-build-dev-skills

[繁體中文](#zh-tw) · [English](#en)

<a id="zh-tw"></a>
<details open>
<summary>繁體中文</summary>

## 用途與目前狀態

本專案準備讓 Grok Build 使用固定版本的共用工程規範，並在 Grok 端管理技能、工具適配、驗證及組裝安裝。

本專案適合維護 AI 開發流程的工程人員。例如，團隊想讓 Grok 在修改程式前讀取共同規範、在合併前保留審查證據，可先用這份設計確認所需能力與限制。

**目前支援 P3-G2 的離線技能原稿、能力證據格式與全新臨時組裝。** 技能尚未安裝／啟用；[Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) 的 Grok runtime 資格仍未完成。請閱讀 [技能組裝](docs/design/p3-g-skill-assembly.md)、[委派證據與缺口](docs/verification/grok-delegation-capabilities.md) 及 [固定 Core 消費](docs/design/p3-g-core-consumption.md)。

## 如何開始

P1 已抽取共用契約；本包以固定 commit revision 與內容指紋 digest 鎖定文件。使用既有 Python 標準函式庫，在 repo root 執行：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/core_snapshot.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py capabilities
```

Core 命令驗固定十一檔；package 命令驗二十檔 bundle。成功只證明離線內容與引用，不代表技能載入、原生委派或 runtime 合格。Packet 是 consumer 證據封裝，不是 Grok API schema；所有 readiness 保持 false。本階段不提供安裝或 live transport。原始 [P2-G 設計](docs/design/p2-g-preparation.md) 與 [來源對照](docs/provenance/source-map.md) 保留歷史與對齊資訊。

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

**P3-G2 provides offline skill sources, consumer capability evidence and fresh temporary assembly.** Skills are not installed or activated. Grok runtime qualification under [Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) is incomplete. Read [skill assembly](docs/design/p3-g-skill-assembly.md), [delegation evidence and gaps](docs/verification/grok-delegation-capabilities.md), and [fixed Core consumption](docs/design/p3-g-core-consumption.md).

## Getting started

P1 extracted the shared contracts. This package pins their commit revision and content fingerprints, called digests. Use an existing Python standard library from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/core_snapshot.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py capabilities
```

The Core command verifies eleven fixed files; the package command verifies a twenty-file bundle. Success proves offline bytes/references, not skill loading, native delegation or runtime qualification. The packet is a consumer evidence envelope, not a Grok API schema. All readiness flags stay false. There is no installer or live transport. The [P2-G design](docs/design/p2-g-preparation.md) and [source map](docs/provenance/source-map.md) retain history and alignment information.

[engineering-workflow-core](https://github.com/jeffery777/engineering-workflow-core) owns shared Markdown obligations. [codex-dev-skills](https://github.com/jeffery777/codex-dev-skills) and this project each own their adapter. Shared text does not prove equal tools, sandbox, permission, or session behavior.

## Limits and license

This package does not deploy, publish tags or releases, update existing skills or global settings, or enable Memory, Hooks, or Schedulers. Every model run and resume must specify a verified sandbox profile. Initial permission must be ask. Stop when no reliable authorization channel exists. Return new authorization requests to あき and the user. Silence and timeout do not grant permission.

This project uses the [MIT License](LICENSE). See [upstream notices](docs/provenance/upstream-notices.md) for the sources of this design.

</details>
