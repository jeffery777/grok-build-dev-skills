# Grok consumer capability mapping

[繁體中文](#zh) · [English](#en)

<a id="zh"></a>

## 繁體中文

Core 的 [workflow](../vendor/engineering-workflow-core/contracts/workflow.md) 定義工程義務；各 consumer 自行核對及適配工具。`AGENTS.md`／Skill 只能引導，不能產生原生派工、授權或相容能力。本包沒有執行 Grok，也不將 Codex 工具名當作 Grok API。

| 義務 | Grok 文件映射 | 本包界線 |
| --- | --- | --- |
| 有界派工與回收 | 原生 `spawn_subagent`、`get_command_or_subagent_output`、`wait_commands_or_subagents`、`kill_command_or_subagent`；內部 ID 有 aliases | 文件記載，不是已取得的完整 schema 或實效證明；原生優先，不重造派工器 |
| 後續訊息 | `send_subagent_message` 預設關閉，並有 parent/child 限制 | 不自動啟用；沒有可靠問題轉交通道即停止相依執行 |
| Reviewer 唯讀 | 實際 tools／permissions／sandbox；作者與 reviewer 分離 | parent plan edit gate 不涵蓋子代理；persona／plan 名稱、Skill `allowed-tools` 不是技術隔離。角色工作約束仍須遵守 |
| 模型與工具 | 實際 loaded tool schema、model/effort 和 managed pins | Skill 的 model/effort metadata 不證明生效；不能只看 flag/parser/exit 0 |
| Session／ACP | 完整 ID 的 new/resume/fork；ACP 為本機 CLI stdio JSON-RPC | 不等同 Codex 話題服務或 durable hosted task；不接 live transport、API 或新付費服務 |

官方網站將 explore/plan 描述為不含 shell；1.0.52 隨版文件卻描述可執行 shell。網站 Headless 的 `-s` 說法亦與隨版 help／Sessions 不一致。保持 unknown，後續以實際載入 schema 與受控 deny／session 測試判定。只靠工具 allowlist 也不足：隨版文件記載 MCP meta-tools 的保留及未知 deny 名稱可無聲無效。

證據分三層：documented 是來源文字；schema-observed 是來源可追溯、仍需核對的實際介面觀察；runtime-verified 要有當前身分與實效測試。本包 consumer packet 只接收相關工具名稱的 fixture／operator report，既不驗完整 Grok schema，也不認證來源 digest。輸出保持所有 runtime、skill loading、delegation 與 delivery readiness 為 false；具體缺口見 [catalog](../capabilities/grok-build-1.0.52.json) 與 CLI blocked checks。

新授權需要保留完整問題與原請求、session／revision／action／canonical path、有效期限及限制，停止等待，交回協調者／使用者。拒絕、cancel、晚到／重複答覆、斷線、錯 ID／revision 與未知效果均不得觸發重播。沒有可靠接口先記 checkpoint；不得自造相容 schema、把新 session 當舊授權，或以 API 可用推定訂閱及付費授權。

每次模型執行與 resume 都須顯式帶已驗證的 sandbox profile，優先 strict，初始 permission 為 default／Ask。實效不明即停止該路線；不得改用 sandbox off、yolo、always-approve、bypassPermissions、廣泛 shell allow 或永久授權。macOS strict 不代表所有網路都被阻斷。

官方來源（2026-10-15 查讀）：[Skills](https://docs.x.ai/build/features/skills-plugins-marketplaces)、[Subagents](https://docs.x.ai/build/features/subagents)、[Plan Mode](https://docs.x.ai/build/features/plan-mode)、[Sessions](https://docs.x.ai/build/features/sessions)、[Headless](https://docs.x.ai/build/cli/headless-scripting)。固定隨版來源 digest 見 catalog；不分發第三方全文。

<a id="en"></a>

## English

Core defines obligations; each consumer owns its tool mapping. AGENTS/Skill instructions create no tool or authority. Prefer documented native Grok children and result/wait/cancel tools. Do not copy Codex dispatch names or build a replacement pool. Optional messaging is off by default and has parent/child limits. No reliable question channel means stop dependent execution.

Separate documented claims, actual schema observations and runtime verification. This consumer packet holds relevant tool-name fixtures or operator reports. It is not a Grok wire schema, source authentication or qualification receipt. Runtime, skill loading, delegation and delivery readiness remain false. See the [catalog](../capabilities/grok-build-1.0.52.json).

Parent plan edit gates do not constrain children. Persona/type labels and `allowed-tools` do not prove read-only enforcement; inspect actual shell/MCP access and permissions. Website and bundled explore/plan shell descriptions differ. Skill model/effort metadata does not establish effective settings. Unknown deny names may do nothing, and MCP meta-tools have separate exposure. Technical isolation is required only when the task requires it, and then needs real evidence.

Use full session IDs after qualification. Headless `-s` documentation conflicts; bundled help says new UUID only. ACP is a local CLI stdio interface, not a hosted durable-task service or Codex peer-thread API. This package implements no transport. API availability does not establish subscription, billing or action authority.

Forward new authorization questions intact with the original request and session/revision/action/path identity. Wait for the authorized decision; reject/cancel/late answers, disconnects and uncertain effects must not cause blind replay. Missing interfaces stay blocked. The official sources above are documentation evidence, not runtime receipts.

Every model run and resume must explicitly select a verified sandbox profile, preferably strict, and start with default/Ask permissions. Stop when effective protection is unknown. Do not widen permissions, persist grants or assume macOS strict blocks every network path.
