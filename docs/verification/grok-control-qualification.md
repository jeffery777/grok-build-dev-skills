# Grok 控制介面查核 / Control qualification

[繁體中文](#qualification-zh) · [English](#qualification-en) · [設計 / Design](../design/p2-g-preparation.md)

<a id="qualification-zh"></a>

## 繁體中文

### 結論與範圍

2026-10-15 UTC，Issue #2 的本機 fixture preflight **Blocked**。實讀版本為 `grok 1.0.52 (0920c8169e27)`。本次沒有送出模型 prompt，也沒有啟動 resume。無法套用 strict，依章程第 7.3 節停止 Grok 路線；未擴權重試、改用較寬 profile 或安裝新軟體／認證。

這是目前 executor 的結果，不能推論 Grok 在所有主機都不支援 strict。精確根因尚未確認；錯誤本身不足以證明是哪一層 OS／executor 限制。未提供 runtime session ID，不能虛構一個。

### 實際觀察

| 項目 | 結果與限制 |
| --- | --- |
| 版本與 help | 已實讀 version、top-level/help、inspect/agent/sessions help；這只確認公開介面 |
| strict preflight | 在無害的臨時 workspace 與隔離 Grok home，以 `--sandbox strict --permission-mode default inspect --json` 啟動非模型查核；exit 1，stdout 0 bytes |
| 錯誤全文 | `sandbox initialization failed: Operation not permitted`；`error: could not apply the 'strict' sandbox profile; see the warning above for the cause. Refusing to start with its protections missing.` |
| 臨時副作用 | sandbox 套用前產生了臨時 Grok home 的 bootstrap 設定、trust／hooks-paths 與隨版文件。這些不是成功 session 證據；沒有提交至 Git |
| 程序控制 | 以 process-scoped `GROK_HOME` 指向臨時目錄；`GROK_DISABLE_AUTOUPDATER=1`、`GROK_MEMORY=0`、`GROK_SUBAGENTS=0`、`GROK_SANDBOX_AUTO_ALLOW_BASH=0`。未讀／複製既有 auth 或修改全域設定；因 preflight 失敗，不能宣稱全部設定生效 |
| updater | `--no-auto-update` 未列 top-level help，但帶 strict/default 的 help parser 檢查 exit 0。隨版 headless 文件也記載此旗標及環境變數；updater 實效未驗證 |
| permission | CLI 接受 `default`，網站稱預設為 Ask。未得到 effective readback，不能認定每個工具都會詢問；隨版文件另列 read-only auto-approvals |
| 未進行 | 正負讀寫／rename／deny、有效 model/effort、網路實測、問題轉交／等待／回答／拒絕、cancel、session resume／recovery。全部尚未驗證，不是 Passed |

私人執行紀錄保留精確 command、路徑與轉錄錯誤；此公開文件只保留必要且去識別的摘要。Help、API 回應或 exit 0 都不是 runtime 驗收。

開發用[有界 probe 控制器](probe-controller.md#zh) 以無害 stub 驗證先存 PID、期限、清理錯誤與輸出保留；它沒有 Grok 執行入口，不改變本頁或 G2-R01–R06 的 runtime 資格。新的實際 probe 仍需另行批准。

### 文件差異與優先序

官方 [Sandbox](https://docs.x.ai/build/features/sandbox) 明示 macOS strict/read-only 的子程序網路限制為 no-op，in-process model/web 網路也不受該限制；strict 不代表離線。網站的 write 範圍描述比隨版文件粗略，後者區分 sessions 與 daemon 目錄。實際有效範圍仍未驗證。

[Enterprise](https://docs.x.ai/build/enterprise) 記載 requirements pins 可壓過環境與其他設定，Sandbox 頁也記載 managed pin 可覆蓋 CLI。隨版 `05-configuration.md` 的通用順序卻列 CLI、env、requirements、overlay、config、managed、defaults。因此不得採一個通用順序當成實效；後續須對 sandbox、permission、model/effort、updater 分別用無害衝突值 readback，且不得自行解除 managed pins。

[Permissions](https://docs.x.ai/build/features/permissions) 記載 deny 優先於 allow；隨版文件另列 ask 與 remembered grants 的順序。這是文件依據，不是本 executor 的 deny 實測。

網站 [Headless](https://docs.x.ai/build/cli/headless-scripting) 稱 `-s` 可建立／接續 named session；實際 help 與隨版文件說 `-s` 只能建立新 UUID，resume 必須 `-r`。後續應用完整 UUID，禁止依「最近」或模糊 title 選 session；本次沒有以模型呼叫解決此差異。

### 可恢復後的有界資格計畫

先由あき確認一個已授權且能實際套用 strict 的入口；本包不自行擴權。下列案例尚未執行，不能用模擬通過取代真實 Grok 證據。

| 順序 | fixture、可觀察證據與停止條件 |
| --- | --- |
| 1：環境 | 只用臨時 CWD、核可 snapshot、假資料與隔離 Grok home；檢視實際 discovery／managed pins。讀回 profile 與有效範圍、禁用額外 hooks/MCP/Memory/Schedulers；profile 無法套用即停止 |
| 2：sandbox | 允許 fixture 的 read/write；用 reviewed strict-derived deny profile 測假 sentinel 的 read/write/rename、symlink／child shell 繞路。以工具結果、OS 拒絕及獨立 before/after hash／inventory 證明；不得探測真憑證。temp 預設 grant 必須納入，不假設父目錄必定拒絕 |
| 3：permission | 以 default/ask 開始；對精確無害動作測 allow+deny 衝突、未授權動作等待與拒絕。不能固定餵 y、廣泛 shell allow 或保存 always-allow |
| 4：問題通道 | 正式 TUI/PTY/ACP 逐入口證明完整問題與 payload 可取得、會保持等待、可送回回答、對應原 session/request、且能確認結果。不能因 initialize 成功而通過 |
| 5：授權身分 | 私人 checkpoint 綁定原請求、完整問題、session/host、revision、action、canonical path/scope、有效期限與限制。文件能回答的既定事實由 Codex 查核；新授權停止相依操作並完整交回あき／使用者 |
| 6：拒絕與 cancel | 原請求拒絕、cancel 等待中請求、晚到或重複答覆、逾時、斷線：副作用 sentinel 不變。cancel 只表示收到控制訊號仍不夠，須核對已停止與未完成動作 |
| 7：resume/recovery | 每次顯式帶同一已驗證 profile 與 permission、完整原 session ID；核對 cwd、revision、owner、檔案 hash 與 pending requests。未知效果先核對，不重播。request/session/revision/action/path 改變使舊同意失效 |
| 8：完結 | 記錄完成／失敗／等待／失聯各狀態與證據、保留 checkpoint。沒有可靠授權通道就停止 Grok 模型工作；Codex 繼續已授權 repo 工作 |

若入口只能拒絕或結束，先保存 checkpoint，取得決策後以已驗證方式與明確 session ID 恢復；這也是待驗證路線。不得把新 session 當成舊請求的同意。

<a id="qualification-en"></a>

## English

### Result and scope

The local fixture preflight for Issue #2 was **Blocked** on 2026-10-15 UTC. The observed version was `grok 1.0.52 (0920c8169e27)`. No model prompt or resume was started. Strict could not be applied. Charter section 7.3 required the Grok route to stop. There was no retry with wider permissions, weaker profiles, new software, or new authentication.

This result applies to this executor. It does not prove that strict is unavailable on every host. The exact OS/executor cause remains unknown. No runtime session ID was returned.

### Observations

| Check | Result and limit |
| --- | --- |
| Version/help | Read version and top-level, inspect, agent, and sessions help. These confirm interface text only |
| Strict preflight | Temporary harmless workspace and isolated Grok home; `--sandbox strict --permission-mode default inspect --json`; exit 1 and empty stdout |
| Full error | `sandbox initialization failed: Operation not permitted`; `error: could not apply the 'strict' sandbox profile; see the warning above for the cause. Refusing to start with its protections missing.` |
| Temporary effects | Grok home bootstrap config, trust/hooks-paths files, and bundled docs were created before sandbox failure. They do not prove a successful session and were not committed |
| Process controls | Temporary `GROK_HOME`; `GROK_DISABLE_AUTOUPDATER=1`, `GROK_MEMORY=0`, `GROK_SUBAGENTS=0`, `GROK_SANDBOX_AUTO_ALLOW_BASH=0`. Existing auth was not read/copied and global settings were not changed. Effective settings remain unverified |
| Updater | The help parser accepted `--no-auto-update` with strict/default and exited 0, although help does not list it. Bundled docs describe both suppression controls. Update suppression itself is unverified |
| Permission | CLI accepts `default`; the website calls the default Ask. No effective readback was obtained. Bundled docs also describe automatic approval of read-only operations |
| Not run | Read/write/rename/deny positives and negatives, effective model/effort, network tests, forwarding/wait/answer/reject, cancel, and session resume/recovery. None is Passed |

Private evidence retains exact command, paths, and the transcribed error. This public record contains a sanitized summary. Help, API responses, and exit 0 do not establish runtime qualification.

The developer [bounded probe controller](probe-controller.md#en) tests persisted PID identity, deadlines, cleanup errors and output retention with harmless stubs. It has no Grok entry point and does not qualify this page's runtime checks or G2-R01–R06. A new real probe still needs separate approval.

### Documentation and precedence gaps

Official [Sandbox](https://docs.x.ai/build/features/sandbox) states that child-network blocking is a no-op on macOS and that in-process model/web traffic is outside that control. Strict is not an offline guarantee. Bundled docs describe narrower sessions/daemon writes than the website summary. Effective paths remain unverified.

[Enterprise](https://docs.x.ai/build/enterprise) and the Sandbox page describe requirements pins overriding environment or CLI settings. Bundled configuration docs list CLI, env, requirements, overlay, config, managed, then defaults. Do not treat a generic order as verified behavior. Test sandbox, permission, model/effort, and updater controls separately with harmless conflicting values and readback. Do not remove managed pins.

[Permissions](https://docs.x.ai/build/features/permissions) states that deny wins over allow. Bundled docs also describe ask and remembered grants. This is documentation evidence, not a deny test on this executor.

The website [Headless](https://docs.x.ai/build/cli/headless-scripting) says `-s` can create/resume a named session. Actual help and bundled docs say it creates a new UUID only; use `-r` to resume. Future tests must select full IDs, never an implicit latest session or ambiguous title. No model call was used to resolve this gap.

### Bounded plan after the environment is restored

あき must first confirm an authorized entry point that can apply strict. This package does not widen access. All cases below are unexecuted.

| Order | Fixture, evidence, and stop |
| --- | --- |
| 1: Environment | Temporary CWD, approved snapshot, fake data, isolated Grok home. Inspect discovery and managed pins. Read back profile and effective grants; exclude extra hooks/MCP/Memory/Schedulers. Stop if sandbox cannot apply |
| 2: Sandbox | Allow fixture read/write. Use a reviewed strict-derived deny profile for fake-sentinel read/write/rename and symlink/child-shell paths. Compare OS/tool results and independent hashes/inventory. Do not probe real credentials. Account for temp grants |
| 3: Permission | Start in default/ask. Test exact harmless allow+deny conflict, waiting, and rejection. No fixed y, broad shell allow, or persistent always-allow |
| 4: Channel | For each TUI/PTY/ACP entry point, prove complete question/payload capture, waiting, answer delivery, original session/request binding, and result confirmation. Initialize success is insufficient |
| 5: Authorization | Private checkpoint binds the original request/question, session/host, revision, action, canonical path/scope, expiry, and limits. Codex may verify existing facts. Stop dependent actions and return new permission requests to あき and the user |
| 6: Reject/cancel | Test rejection, cancel while waiting, late/duplicate answers, timeout, and disconnect. The side-effect sentinel must stay unchanged. Verify actual stop and outstanding actions |
| 7: Resume/recovery | Explicit verified profile and permission on every resume, full original session ID, and current cwd/revision/owner/hashes/pending requests. Reconcile uncertain effects before replay. Changed request/session/revision/action/path invalidates old approval |
| 8: Completion | Preserve evidence and checkpoints for completed/failed/waiting/disconnected states. Stop model work if the authorization channel is unreliable. Codex may continue authorized repository work |

If an entry point can only reject or exit, save a checkpoint, obtain the decision, and recover by a verified method with an explicit session ID. This route is also unverified. A new session does not inherit consent for an old request.
