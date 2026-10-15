# 離線初始化交換 / Offline initialize exchange

[繁體中文](#zh) · [English](#en) · [控制器契約 / Controller contract](probe-controller.md)

<a id="zh"></a>

## 繁體中文

### 範圍與呼叫

[Issue #12](https://github.com/jeffery777/grok-build-dev-skills/issues/12) 為開發用控制器新增 `run_probe(..., initialize_only=True)`。此選項只準備 initialize 形狀的離線交換；測試只執行固定的[無害 Python peer](../../tests/fixtures/initialize_stub.py)。沒有 Grok launcher、CLI、認證、session、模型 RPC 或 recovery，也不證明目前 Grok 或完整 ACP 協定相容。新檔案不加入既有二十檔 bundle，技能、Core lock／vendor 與 runtime 資格不變。

呼叫者仍須提供控制器要求的明確 argv、cwd、全新證據目錄、request/revision/action 身分及完整 env allowlist，且已有動作授權。`initialize_only` 須為 bool；啟用時拒絕非空 `input_data`，避免額外請求。沒有自動批准或重播。從 repo root 執行：

```sh
python3 -B -m unittest discover -s tests -p test_initialize_exchange.py -v
```

### 單次請求與解析邊界

控制器先持久保存 launch intent 與已觀察的本次 PID／PGID 身分，再寫入唯一固定請求及 LF：

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":1,"clientCapabilities":{}}}
```

送完後移除 stdin 的 write interest，保持 pipe 開啟，等到回覆、異常或期限才開始清理。這不驗證 peer 的 sandbox 或人類授權。

[解析器](../../scripts/initialize_exchange.py) 接受跨多次 read 的 UTF-8／LF JSON frame；每流累計最多 8192 bytes，先計數再緩衝。必須是 object、`jsonrpc="2.0"`、整數 `id=1`、object `result`、整數 `protocolVersion=1`；bool／float 不算整數。拒絕任何 `method` 或 `error` key（即使值為 null）、巢狀重複 key、非標準 NaN／Infinity、壞 UTF-8／JSON、過深結構、缺 LF 的 EOF 與過量資料。第一個 frame 後只允許 JSON 空白；第二個 frame、部分尾訊息或非空 stderr 都阻擋，包含清理期間晚到的資料。

JSON container 深度最多 32 層（root 為第一層），不依賴 interpreter 的遞迴上限。未知欄位與 `authMethods`／`agentInfo` 的值只在有界解析中暫存，不寫入證據。唯一可保存的 child 衍生內容是固定常數投影及固定 observation 欄位／原因 enum、bool、整數與 null：

```json
{"id":1,"jsonrpc":"2.0","result":{"protocolVersion":1}}
```

### 保存與完成判讀

此模式的 `stdout.bin` 只在解析接受、身分已保存、直屬 child 已回收、兩流 EOF、完整固定請求已送出且沒有已知錯誤後，才嘗試寫固定投影；`stderr.bin` 保持空。解析器持續工作到清理結束，晚到異常可撤銷先前觀察。原始 child stdout／stderr、任意 peer 字串及例外訊息不進入 journal、receipt 或回傳值。可信呼叫端提供的 argv、cwd、identity 仍依原控制器記錄；此選項不是通用 secret scrubber、記憶體抹除或防竄改機制。

`response_observed=true` 只表示曾看到符合形狀的回覆。`COMPLETE_INITIALIZE_DIRECT_CHILD_ONLY` 還要求 child 真實 return code 為 0，或本控制器成功送出的 SIGTERM 所造成的 `-SIGTERM`；保留原始負值，不改寫為 0。強制 KILL、非零退出、訊號拒絕／不明、截斷、保存失敗或觀測超時皆為 `BLOCKED`。所有四個 runtime／skill-loading／delegation／delivery flags 永遠 false，`descendant_stop=NOT_VERIFIED`。

寫投影前先保留 quota；部分寫入或寫後 fsync 失敗保留 consumed quota、`*_bytes_stored=null` 及 uncertainty。最終 journal、receipt、close 或總期限檢查仍可把結果降為 `BLOCKED`。因此磁碟上的投影、單一 status 或 journal 中較早的 observation 都不是完成證明；按[控制器契約](probe-controller.md#zh) 讀回完整證據並保留最終回傳值。磁碟 receipt 的時間截止於最後保存前，回傳值另量測總時間。

### 限制與後續門檻

繼承控制器的有界等待、可信暫存父目錄、單 writer、只管理本次仍持有 process group 與拒絕後不升級的限制。OS spawn、排程與核心 I/O 可能阻塞，沒有硬即時或整棵程序樹停止保證。不連網的 fixture 不證明網路隔離；也不證明 strict sandbox、permission 問題轉交／等待／回答／拒絕／cancel、session recovery、skill loading 或 entitlement。[Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) 的相依 runtime 缺口仍阻擋。任何新的真實 Grok probe 須先取得新的有界授權與適用的有效控制前置；本包沒有提供該授權。

<a id="en"></a>

## English

### Scope and use

[Issue #12](https://github.com/jeffery777/grok-build-dev-skills/issues/12) adds `run_probe(..., initialize_only=True)` to the developer controller. This is preparation for an initialize-shaped offline exchange. Tests run only the fixed [harmless Python peer](../../tests/fixtures/initialize_stub.py). There is no Grok launcher, CLI, authentication, session, model RPC or recovery. Results do not establish current Grok compatibility or full ACP conformance. New files stay outside the twenty-file bundle. Skills, Core lock/vendor and runtime qualification do not change.

The caller must already have action authority and supply explicit argv, cwd, a fresh evidence directory, request/revision/action identity and a full environment allowlist. The option must be a bool. Nonempty caller input is rejected in this mode. There is no automatic approval or replay. Use the test command above from the repository root.

### One request and bounded parsing

Persist launch intent and the observed current PID/PGID identity before sending the single fixed request shown above, followed by LF. Remove stdin write interest after that request, but keep the pipe open until a response, anomaly or deadline starts cleanup. This does not verify a peer sandbox or human approval.

The [parser](../../scripts/initialize_exchange.py) supports UTF-8/LF JSON frames split across reads. Each stream has an 8192-byte cumulative limit, counted before buffering. Require an object, `jsonrpc="2.0"`, integer `id=1`, object `result` and integer `protocolVersion=1`. Reject bool and float values for those integers. Reject any `method` or `error` key, including null values; nested duplicate keys; nonstandard NaN/Infinity; invalid UTF-8/JSON; excessive nesting; EOF without LF; and excess data. After the first frame, allow only JSON whitespace. A second frame, partial message tail or any nonempty stderr blocks completion, including data received during cleanup.

JSON container depth is at most 32 levels, with the root at level one, independent of the interpreter recursion limit. Unknown fields, `authMethods` and `agentInfo` values remain only in bounded parsing memory. The only child-derived evidence is the fixed projection above and fixed observation keys/reason enums, bools, integers and null. No peer text is copied into the projection.

### Persistence and completion

Only attempt the constant projection in `stdout.bin` after parsing succeeds, identity is saved, the direct child is reaped, both streams reach EOF, the full fixed request is sent and no known error remains. `stderr.bin` stays empty. Parse through cleanup so late anomalies can invalidate the earlier response. Raw child stdout/stderr, arbitrary peer strings and exception messages never enter evidence or the return value. Trusted caller argv, cwd and identity are still recorded under the controller contract. This option is not a general secret scrubber, memory eraser or tamper protection.

`response_observed=true` means only that a response of the required shape was seen. `COMPLETE_INITIALIZE_DIRECT_CHILD_ONLY` also requires actual child return code 0, or `-SIGTERM` after this controller successfully sent TERM. Preserve that negative code. Forced KILL, other nonzero exits, denied/uncertain signals, truncation, persistence failure and observed deadline misses remain `BLOCKED`. All four runtime/skill-loading/delegation/delivery flags stay false. `descendant_stop=NOT_VERIFIED` remains.

Reserve quota before projection writes. Partial writes or post-write fsync errors retain consumed quota, unknown stored counts and persistence uncertainty. Final journal, receipt, close or total-deadline checks can still downgrade the result. A saved projection, single status or earlier observation alone is insufficient. Read all evidence under the [controller contract](probe-controller.md#en) and retain the final return value. The disk receipt measures through cleanup before final persistence; the return value also measures total elapsed time.

### Limits and later gates

Inherit bounded waiting, trusted single-writer temporary parents, control of only the currently owned process group and no escalation after denied/uncertain signals. Spawn, scheduling and kernel I/O can block. There is no hard real-time or full descendant-stop guarantee. Offline fixtures prove no network isolation, strict sandbox, permission question handoff/wait/answer/deny/cancel, session recovery, skill loading or entitlement. Dependent runtime gaps in [Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) remain blocked. Any later real Grok probe needs new bounded approval and verified applicable controls. This package grants neither.

English follows clarity/ASD-STE100 principles; full conformity is unverified. 繁中採清晰性原則。
