# Grok 委派能力與資格 / Delegation evidence and qualification

[繁體中文](#zh) · [English](#en)

<a id="zh"></a>

## 繁體中文

[Issue #6](https://github.com/jeffery777/grok-build-dev-skills/issues/6) 只驗證 [離線技能組裝](../design/p3-g-skill-assembly.md)。原 [Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) 的 strict／授權／session 資格仍未完成；本包沒有執行新 Grok 命令、模型或 API，也不重新解釋私人診斷。

### 已知與未知

1.0.52 (`0920c8169e27`) 的既有 help 列出 agents、subagents、tools、sandbox 及 session flags。固定 [catalog](../../capabilities/grok-build-1.0.52.json) 保存隨版文件 digest 及 2026-10-15 官方來源。這些是 documented 證據，不是實際 loaded schema 或 runtime receipt。

原生子代理有文件依據，因此 consumer 應優先適配它，不重造派工器。其完整參數／有效 tools、model/effort、設定優先序與實效仍 unknown。訊息工具預設關閉，不能為了傳授權問題自動啟用。ACP 僅是本機 CLI stdio 候選入口；不是 hosted task service，亦不證明 Codex 話題 API 等價或使用者具有新 API／訂閱／付費授權。

| 差異／義務 | 現有來源 | 後續必要證據 |
| --- | --- | --- |
| explore／plan 是否有 shell | 官網說無 shell，隨版 `16-subagents.md` 說可執行 shell | 每個實際 child 的 loaded tool schema、有效權限；受控 edit/shell/MCP deny 正負例 |
| parent plan mode | 官方 Plan Mode 說 edit gate 不涵蓋 child，permission mode 仍繼承；shell 亦可能寫入 | 不以 persona/plan 當保障；若任務要求技術唯讀，驗所有實際可寫入口。一般獨立角色約束不宣稱 OS 隔離 |
| Skill frontmatter | `allowed-tools` 不限制工具，model/effort 等不套用 | 核對外部有效設定，不從 metadata 推定 |
| tool filtering | 隨版 Headless 記載內部 ID／顯示 aliases、未知 deny 名稱可無聲無效、MCP meta-tools 保留 | 核對有效 tools/schema；不要只驗 flag 被接受 |
| `-s` 與 resume | 隨版 help／Sessions 說新 UUID；Headless 網頁另稱 create/resume | 以完整 ID、明確 profile／permission，驗 new/resume/fork 身分及錯誤案例 |
| native lifecycle | 隨版列出 spawn/output/wait/cancel；訊息 off-by-default 且有目標限制 | 精確 child/parent ownership、等待、實際結果與取消後 sentinel，不以 ID 或摘要代替完成 |

來源與細節集中於 [Grok mapping](../../references/grok-capabilities.md)，不將本表當可呼叫 schema。

### 仍阻擋 runtime readiness 的驗收

| ID | 狀態 | 成立條件（本包未執行） |
| --- | --- | --- |
| G2-R01 | BLOCKED／未驗證 | 能套用的已驗證 profile，優先 strict；每次 run/resume 明示 profile、初始 default/Ask；有效 read/write/rename/deny 正負例，納入 macOS 網路限制 |
| G2-R02 | 未驗證 | 合法入口讀回實際 tool schemas、model/effort、managed pins／優先序及有效 tools；無必要資料就 unknown |
| G2-R03 | 未驗證 | 原生 spawn/result/wait/cancel、深度／容量、作者與 reviewer 獨立及適用唯讀約束；source/head/ownership 不漂移 |
| G2-R04 | BLOCKED／未驗證 | 完整問題與原請求可轉交、保持等待、回答／拒絕、cancel／晚到／重複答覆／斷線；session/revision/action/path 身分綁定與副作用 sentinel |
| G2-R05 | 未驗證 | 完整 session ID resume/recovery，核對 cwd／owner／revision／pending requests；未知外部效果先讀回，不盲重播 |
| G2-R06 | 未驗證／未授權 | 真正 skill loading／執行遵循另測；API entitlement 與任何付費／安裝／rollout 另核對，不從文件或連線推定 |

以上項目由協調者安排新的有界資格工作；沒有可靠接口，保留具體 blocker 與 checkpoint。本包的 fake packet、有效 JSON、exit 0、synthetic tests 或 Code/docs review 都不能把它們升級 Passed。禁止降低 sandbox／permissions、永久授權、複製憑證、啟動新服務或把 ACP 假 transport 當 runtime。

<a id="en"></a>

## English

Issue #6 qualifies offline structure only. Existing strict, authorization-channel and session work under Issue #2 remains incomplete. The installed 1.0.52 help and pinned bundled-guide digests document native children; they do not prove current schemas or behavior. Prefer the native interface rather than a replacement pool.

The table records unresolved shell and session wording differences. Parent plan edit gates do not constrain children. Skill/persona/type names do not prove technical read-only behavior or effective model/effort. Inspect the actual child toolset, permission inheritance, shell/MCP exposure and any required isolation. Do not automatically enable optional messaging.

G2-R01–R06 remain unverified or blocked: effective sandbox/deny, loaded schemas and model, native child lifecycle, complete approval forwarding/waiting/rejection/cancellation, explicit-session recovery and actual skill loading/entitlement. Later tests need harmless fixtures, bound identities and readback. Every model run/resume must select a verified profile and default/Ask permissions. No channel or profile means stop dependent runtime work and retain a checkpoint.

The consumer packet accepts only documented relevant tool names as unauthenticated fixture/operator reports. It is not a Grok wire schema. No offline test, accepted flag or review can raise runtime readiness. ACP is a local stdio interface, not a durable hosted-task service. Availability does not grant subscription, API billing, installation or action authority. No live transport or new paid service is included.

English uses clarity/ASD-STE100 principles; full conformity is unverified.
