# 有界 probe 控制器 / Bounded probe controller

[繁體中文](#zh) · [English](#en) · [資格限制 / Qualification limits](grok-delegation-capabilities.md)

<a id="zh"></a>

## 繁體中文

### 用途與執行

[Issue #10](https://github.com/jeffery777/grok-build-dev-skills/issues/10) 補足開發測試的程序身分、期限與證據保留邊界。[控制器](../../scripts/probe_controller.py) 是 Python 3.10+／POSIX 的函式工具，沒有 CLI 或 Grok、ACP、模型、授權及 recovery 接口，也不在既有二十檔 bundle。技能、manifest、Core lock／vendor 與 G2-R01–R06 狀態不變。

從 repo root 執行既有標準函式庫測試；測試只啟動固定的[無害 Python stub](../../tests/fixtures/probe_stub.py)，不啟動 Grok、不查其他程序、不讀憑證、不連網、不安裝軟體：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_probe_controller.py -v
```

函式 `run_probe` 需要明確 argv、可信 cwd、全新系統暫存證據目錄、request/revision/action 身分、完整 env allowlist 及有界 input。呼叫者必須已有該動作授權；這些輸入只是宣告，不驗證人類授權、來源 revision、有效 child UID 或 sandbox。範例呼叫見[測試](../../tests/test_probe_controller.py)，沒有可直接啟動 Grok 的命令。新實際 probe 必須先取得新的有界批准及適用 sandbox／permission 前置。

### 證據與判讀

每次只建立全新 0700 目錄、0600 exclusive/no-follow 檔案，拒絕既有目標、symlink 祖先及系統暫存目錄以外的位置；保留失敗的新目錄，不覆寫或自動重播。只使用可信、單一 writer 的暫存父目錄。此檔案處理不是防禦可改寫主機或同權限父目錄的攻擊者的 sandbox。

| 記錄 | 用途與限制 |
| --- | --- |
| `journal.jsonl` | 逐筆 flush/fsync 的啟動意圖、PID／PGID、controller UID、request/revision/action/cwd、signal 意圖／結果與收尾。PID 事件完成後才可寫 stdin；不完整尾筆或缺終筆不是完成 |
| `stdout.bin`、`stderr.bin` | 每次讀取後增量保存原 bytes，單流預設 64 KiB、上限 256 KiB，總保留上限為兩倍單流上限。寫入前先保留額度；失敗不重用額度。`*_bytes_reserved` 是已使用的額度，儲存量不確定時 `*_bytes_stored=null`、`output_persistence_uncertain=true`。沒有通用 secret scrubber，只用無害資料；不得提交私人輸出 |
| `receipt.json` | 整理截至清理完成的結果，尚未量測最後保存；寫入失敗仍嘗試在 journal 留下失敗事件。磁碟整體失效時不能保證完整 receipt。先查 journal，再看 receipt，不能只讀一個 status |
| 函式回傳值 | 另量測包含 receipt 保存的總 elapsed/deadline；磁碟 receipt 的 `cleanup_elapsed_seconds`／`cleanup_deadline_met` 涵蓋前置作業與清理，截止於最後 journal／receipt 保存之前。呼叫端須保留最後回傳值；不能把前一時間當成全部保存時間 |

`COMPLETE_DIRECT_CHILD_ONLY` 只表示直屬 child 正常退出、已回收、已知 input 已寫入 pipe、兩流 EOF、證據無已知錯誤且控制器觀測未逾期；寫入 pipe 不證明 child 接受或執行。非零退出、timeout、截斷、寫入／訊號錯誤、身分未保存或停止不明皆為 `BLOCKED`。Child return code 與控制器結果分開。四個 runtime／skill-loading／delegation／delivery flags 永遠 false。

### 期限、清理與停止

全流程共用 monotonic deadline（0.5–30 秒），預留清理時間。stdin 上限 4 KiB；stdout/stderr 交錯小塊讀取。TERM 與必要時 KILL 各最多一次，只對本次仍持有的 child／原生新 process group。訊號被拒絕或結果不明後，不重試、不升級、不改用其他入口。Child 一旦被回收，不再用其數字 PID／PGID 發訊號；不載入舊 PID、不掃描程序、不以 journal 自動接管。

`Popen` 到 PID 落盤仍有間隙；stdin 前保存不阻止 child 啟動時自行產生副作用。OS spawn、fsync、排程與核心 I/O 可能阻塞，所以這是有界等待策略，不是硬即時保證。Python 例外／KeyboardInterrupt 會嘗試有界清理及保存；控制器被 SIGKILL 或主機斷電時，只能依賴已持久保存的 journal／輸出。

`direct_child_reaped` 只證明直屬 child 已回收；signal 成功不證明子孫已停止。子孫可離開 group 或提早關閉 pipe；`descendant_stop=NOT_VERIFIED` 永遠保留。不以這個工具證明程序樹隔離、Grok strict、授權等待／cancel 或 session recovery。發生 Unknown／Blocked 時保留 checkpoint，交回協調者；禁止盲重播。

### 缺口與後續

現有技能入口、固定 Core 與組裝驗證已存在。本工具只補先保存身分、清理失敗仍保留證據的必要接點。G2-R01／R02 的 sandbox／工具實效、R03 的原生委派、R04 的完整授權通道、R05 的明確 session recovery、R06 的 skill loading／entitlement 都仍須官方入口的實際證據。沒有可靠接口就停止相依 runtime 工作；不新增替代派工器、批准引擎、安裝器或假 ACP transport。

<a id="en"></a>

## English

### Purpose and use

[Issue #10](https://github.com/jeffery777/grok-build-dev-skills/issues/10) adds process identity, time limits and evidence retention for developer tests. The [controller](../../scripts/probe_controller.py) is a Python 3.10+/POSIX function helper. It has no CLI, Grok, ACP, model, approval or recovery integration. It is excluded from the existing twenty-file bundle. Skills, manifest, Core lock/vendor and G2-R01–R06 states do not change.

Run the shared command in the Chinese section from the repository root. It runs only the fixed [harmless Python stub](../../tests/fixtures/probe_stub.py). Tests start no Grok process, inspect no unrelated process, read no credentials, use no network and install nothing.

`run_probe` requires explicit argv, trusted cwd, a new system-temporary evidence directory, request/revision/action identity, a complete environment allowlist and bounded input. The caller must already have action authority. Inputs are claims, not authentication of approval, revision, child UID or sandbox. See the [tests](../../tests/test_probe_controller.py) for calls; there is no Grok launch command. A later real probe needs new bounded approval and applicable sandbox/permission prerequisites.

### Evidence and interpretation

Each attempt creates a new 0700 directory and exclusive no-follow 0600 files. Existing targets, symlink ancestors and destinations outside system temporary roots are rejected. Preserve failed fresh directories. Never overwrite or replay them. Use a trusted temporary parent with one writer. This is not a sandbox against an actor who can rewrite the host or parent directory with the same permissions.

| Record | Meaning and limit |
| --- | --- |
| `journal.jsonl` | Flush/fsync each launch intent, PID/PGID, controller UID, request/revision/action/cwd, signal intent/result and finish event. Persist the PID event before stdin. A partial final line or missing finish is incomplete |
| `stdout.bin`, `stderr.bin` | Save raw bytes after each read. Default 64 KiB per stream; maximum 256 KiB each, twice that limit in total. Reserve quota before writing; never reuse it after failure. `*_bytes_reserved` is consumed quota. Uncertain storage gives `*_bytes_stored=null` and `output_persistence_uncertain=true`. There is no general secret scrubber. Use harmless inputs and keep private output out of Git |
| `receipt.json` | Summarize the result through cleanup, before measuring final persistence. On receipt failure, attempt a journal failure event. Total storage failure can prevent a complete receipt. Read the journal first; status alone is insufficient |
| Function return | Also measure total elapsed/deadline through receipt persistence. On-disk `cleanup_elapsed_seconds`/`cleanup_deadline_met` include setup and cleanup, stopping before final journal/receipt persistence. Retain the return value; the earlier measurement does not cover all saving time |

`COMPLETE_DIRECT_CHILD_ONLY` means a zero-exit direct child was reaped, known input was written to its pipe, both streams reached EOF, evidence has no known error and the controller observed no deadline miss. Pipe writes do not prove acceptance or execution. Nonzero exit, timeout, truncation, write/signal errors, missing persisted identity or uncertain stop produce `BLOCKED`. Child return code is separate. Runtime, skill-loading, delegation and delivery flags always stay false.

### Deadline, cleanup and stops

One monotonic deadline covers execution and cleanup, with a cleanup reserve, for budgets of 0.5–30 seconds. Input is at most 4 KiB. Read both output streams in small interleaved chunks. Send TERM and, when required, one KILL only to the child/new process group owned by this call. A denied or uncertain signal stops further signal attempts and escalation. Never signal the numerical PID/PGID after reaping. Do not import old PIDs, enumerate processes or adopt a process from its journal.

There is a gap between `Popen` and persisted PID evidence. Saving before stdin cannot prevent startup effects. OS spawn, fsync, scheduling and kernel I/O can block; this is a bounded waiting policy, not a hard real-time guarantee. Python exceptions/KeyboardInterrupt trigger bounded cleanup and saving attempts. After controller SIGKILL or host power loss, only previously durable journal/output can remain.

`direct_child_reaped` attests only the direct child. Accepted signals do not prove descendant termination. Descendants can leave the group or close pipes early; `descendant_stop=NOT_VERIFIED` remains. The helper proves no process-tree isolation, Grok strict controls, approval waiting/cancel or session recovery. Preserve a checkpoint and return Unknown/Blocked to the coordinator. Never replay uncertain effects.

### Remaining interfaces

Skill entry points, pinned Core consumption and assembly verification already exist. This helper only adds durable identity and evidence despite cleanup failure. G2-R01/R02 still need effective sandbox/tool evidence, R03 native delegation, R04 the full approval channel, R05 explicit-session recovery and R06 loading/entitlement. Use actual official surfaces for that evidence. Stop dependent runtime work when no reliable interface exists. Add no replacement pool, approval engine, installer or fake ACP transport.

English follows clarity/ASD-STE100 principles; full conformity is unverified. 繁中採清晰性原則。

## 官方依據 / Official references

- [Python 3.13 subprocess](https://docs.python.org/3.13/library/subprocess.html): native argv/environment/session and timeout limits.
- [Python 3.13 os.killpg](https://docs.python.org/3.13/library/os.html#os.killpg): POSIX process-group signal interface.
- [Python 3.13 time.monotonic](https://docs.python.org/3.13/library/time.html#time.monotonic): clock for elapsed deadlines.
