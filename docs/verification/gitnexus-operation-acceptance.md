# GitNexus 接入驗收與支援矩陣 / Integration acceptance and support matrix

[繁體中文](#zh-tw) · [English](#en)

<a id="zh-tw"></a>
<details open>
<summary>繁體中文</summary>

## 驗收對象與目前狀態

本計畫對應 [Issue #28](https://github.com/jeffery777/grok-build-dev-skills/issues/28) 與 [最小設計](../design/gitnexus-operation-parity.md)，驗收 **本技能與 Agent 能正確使用 GitNexus**。配對為 Grok 0.2.0 候選、Codex 0.35.0 候選、Core 0.1.0、GitNexus 精確 1.6.12，並非發行宣告。

**有界原生唯讀 plan 已觀察成功；原生 refresh 及實際授權拒絕／取消／恢復未執行。** 2026-10-18 既有證據分三層列於下方，不把離線或 controller 證據當作 Grok 模型已完成所有操作。此次 Grok 觀察沒有執行 GitNexus version/help、analyze、status、query、Node 或 MCP。固定 S/T 已接收並記於設計與 source lock；僅採用三模組與 LICENSE。`tests/test_gitnexus_entry.py` 以 stub/captured API 驗本端選擇、profile 外部 digest、無 probe、原鎖路由、receipt 及失敗處置；package tests 另驗來源漂移與多餘檔案。原生 model 配額已用完；本記錄不授權追加調用。下表分開列必要流程與實際 coverage，不代表每項真實模型行為已觀察。

### 證據分層

- **N1：原生 Grok 唯讀使用。** Grok 1.0.62／macOS arm64，明確 `workspace`、初始 `default`／Ask；只用一次完整精確 plan 命令的 process-only allow。一次 inspect、一次 model；7 次 read_file 完整 bytes 符合 fixture 中兩技能、三份必要 Core 與兩份 reference，另有一次 foreground plan。Model 114.13 秒／上限 120 秒、CLI 最多 6 turns；4 個 assistant／usage cycles，1 個 user turn。總輸出 418,721 bytes／1 MiB，停止還原 0.019 秒／30 秒。沒有 retry／resume。Plan 為 `plan_only`，metadata `missing`，`authority_granted=false`、`gate_satisfied=false`；模型沒有把 exit 0 當 freshness、refresh 或任務完成。兩個假設案例分別保留 Codex writer 指派及未知前次效果的 reconcile／等待義務，沒有真的製造拒絕、取消或恢復。
- **A02：既有 controller 寫入。** 接收固定 adapter 的獨立覆核，支持指定安裝／profile、五個精確 coverage paths、乾淨 fixture 換 HEAD 後一次實際 1.6.12 controller rebuild，以及 sidecar 綁定的內部 freshness 與後續 file-only 讀回。原 worker 仍為 `STOPPED_NO_RETRY/AssertionError`：成功 controller 後的外層 Git-control baseline 比較失敗；兩份 Git index 只有一個檔案的 stat-cache 欄位不同，寫入者／機制未知。另一次 final freshness API 沒有執行；不得把整個 worker 改判 PASS。這不是 Grok 原生 refresh，也沒有追加 live 配額。
- **L1：合成鎖證據。** 固定 S 的四個既有 `ProcessAndOperatorTests` 方法重跑 4/4 PASS：同 repo contention／linked worktree、lock 檔案與目錄身分、跨 Python process 的 parent replacement／flock，以及跨 repo 共用 isolated home。使用合成 Git fixture 與真 Python 子程序，不啟動 GitNexus／Node／模型。首次因空 Git template 缺 info/exclude 而出現的 4 個 setup errors 保留；只修該 fixture 後重跑同四項。第五個 deadline 案例未跑；歷史 transitive deadline closure 不完全相同的限制也保留。配合本端 default-lock/no-override 路由，可支持合作式排他契約；不是原生 Grok/Codex 跨代理並行、耐久去重或 vendor DB concurrency 資格。

N1 在測試時綁定 manifest `247fb20b04e1e1aeb3f21c5000fdbf9edc035b340f6b20f2aa9310d126a8dd52`、薄入口 `db4c1629c41bd3ebdc384134c43e111f918b0b62a65314314c2a55aa560222a1` 及設計所列 S/T。之後只同步文件與 capability reference 的事後狀態段落，並更新其 manifest 項；技能、Core、入口、controller、lock 與程式不變，沒有重跑模型。不要將新 manifest 假稱為原生受測 bytes。

測試期間按明確授權只暫時信任該 fixture、完整停用 MCP config，並暫停一個既有全域 hook；原 hook 同 inode／bytes／mode 與原 trust bytes 均已還原。保存第一次 host checker 的錯判及修正：同一成功 inspect 的 trailing slash、同名 qualified plugin、缺省空陣列及 disabled MCP 列經離線重讀確認；未重跑 inspect。原生執行時 source 54 檔與 fixture 30 檔未變，未建立 index。原始 session／profile／本機路徑／工具串流及還原記錄留受控證據，公開庫只保留本摘要與必要固定身分。

## 必要使用流程

| 案例 | 可觀察的接入結果；不是 vendor 功能測試 | 已有證據與限制 |
| --- | --- | --- |
| G-USE-01 操作權責 | 執行技能保留原請求與編排指派；Codex/Grok 任一端可被指定為唯一 index writer。未指定、範圍衝突或 reviewer 路線均不刷新，交回編排方；欄位或自述不能製造授權。 | 離線負例；N1 正向指派與假設情境 A。未做原生衝突 writer 執行。 |
| G-USE-02 目標選擇 | 使用明確 repo/worktree/branch/HEAD 與索引身分。遇同名 repo、另一 checkout 或來源不符時停止相依動作，不借用其他目標的索引證據。 | 離線負例；N1 明確 fixture selectors 的正例。 |
| G-USE-03 固定入口與命令 | 薄入口選固定 controller 與其允許的 index-only 操作；不繞過 controller 直跑 analyze、不用 mutable sibling 或 latest。Missing／不相容來源在程序執行前被拒絕；由 stub/captured runner 查本端組參，不重驗 GitNexus 內部 flags。 | 離線 captured API；N1 真正一次 plan。A02 為既有 controller 寫入，不是 Grok 原生 refresh。 |
| G-USE-04 證據判讀 | 僅採用仍適用的來源、操作結果及 sidecar；缺件、過期、不完整或矛盾時保持相應狀態。Help、API、exit 0、metadata 或摘要單獨不能充作完成、review 或新的授權。 | N1 正確判讀 plan_only／missing／authority=false／gate=false；A02 原例外保留。 |
| G-USE-05 失敗與未知效果 | 拒絕、取消、timeout、partial 或未知結果不自動重試、不偽造成功；保留原請求、目標、action、session/revision（適用時）與可讀證據，先核對已知效果，再交回編排方。 | 離線失敗路徑與 N1 假設情境 B。原生拒絕／cancel／timeout／resume/recovery 未執行。 |
| G-USE-06 交接與共用 writer | 兩端選同一 controller 鎖及 sidecar 契約。使用本端 stub／既有鎖操作證據檢查重複指派時不進入第二次刷新；未知前次程序未結清時不偷鎖或交接。這不驗 DB 並行或 vendor lock bug。 | 本端預設鎖路由＋L1 四項合作鎖。沒有原生跨代理並行或耐久去重驗收。 |
| G-USE-07 封裝與聲明 | 來源／plugin 佈局、相對引用、固定檔案 digest/notices 與版本配對一致；明確區分 fixture、工具證據與真實 Agent 使用。不得把規劃、固定程式或原生 MCP discovery 宣稱為已完成技能操作驗收。 | 離線 package/digest/引用與 N1 local qualified skills 及完整讀取。正式 install/update/rollback 未執行。 |

案例實作與數量以固定來源的既有 coverage 決定；只補本接入缺口，不複製整套 provider 測試。Controller 的原始工具證據保留其限制；raw analyze 成功不代替本技能選擇／呼叫流程。缺來源或未覆蓋部分記 NOT_RUN／待補，不用無關 PASS 結清。

## 驗證方法與真正停止點

優先用純資料 fixture、stub/captured runner、package／引用／digest 檢查，測兩技能指引與薄入口的行為；不啟動真實 GitNexus，也不碰現行索引、用戶 registry、全域設定、目前安裝或其他 repo。需環境變更的驗證只在隔離測試專案；本端測試不得建立 hooks、scheduler、Memory、模型路由或新增憑證。

沿用可適用的既有 Grok 載入、Core／套件與工具操作證據。來源或規則未改的部分不機械重跑；新增／變動的指引與入口仍須有相應 coverage。沒有實際 Agent 使用觀察時，保持該範圍未驗證，不把腳本測試當作模型已採用。

任何追加原生 Grok 調用均先交編排方一份新的具體有界方案：固定候選與技能來源、確切 fixture／入口與 argv、正常 sandbox profile／初始 ask、允許工具／寫入集合、輸入與觀察、調用次數／時間／輸出預算、停止及證據保全。優先沿用既有工具證據配合無副作用的接入觀察；若仍需真實 GitNexus 操作，須另外列明並取得授權。未獲同意前不啟動，也不移用 Codex A02 或先前 live 配額；不做 vendor sandbox QA。

獨立 reviewer 依當前 diff 檢查上述流程、雙語義務與宣稱；deterministic checks 不取代該 review。按實際影響判定必要 Security Diff Scan。已支持的範圍只限上述列明 coverage；文件或既有證據不授權新 refresh 或其他原生調用。Commit、push、PR、merge、tag/Release、發行與現行安裝不在本包授權內。

</details>

<a id="en"></a>
<details>
<summary>English</summary>

## Scope and current state

This plan covers our skills and agents using GitNexus correctly under [Issue #28](https://github.com/jeffery777/grok-build-dev-skills/issues/28) and the [minimal design](../design/gitnexus-operation-parity.md). The planned pairing is Grok 0.2.0 candidate, Codex 0.35.0 candidate, Core 0.1.0 and GitNexus exactly 1.6.12. It is not a release announcement.

**Bounded native read-only plan use was observed successfully. Native refresh and actual approval/refusal/cancel/recovery remain unrun.** The 2026-10-18 records below separate three evidence layers. Offline or controller evidence does not prove all Grok model behavior. This Grok observation ran no GitNexus version/help, analyze, status, query, Node or MCP. Fixed S/T source is now recorded in the design/lock; only three modules and LICENSE are reused. `tests/test_gitnexus_entry.py` uses a stub/captured API for our selection, external profile digest, no-probe route, default lock routing, receipt and failure handling. Package tests cover source drift and extra files. The native model allowance is spent; this record grants no additional call. The table separates required behavior from observed coverage.

### Evidence layers

- **N1: native Grok read-only use.** Grok 1.0.62 on macOS arm64 explicitly used `workspace`, initial `default`/Ask, and one process-only allow for the exact complete plan command. One inspect and one model session produced seven complete read_file payloads matching both fixture skills, three required Core contracts and two references, plus one foreground plan. The model took 114.13 of 120 seconds with CLI max-turns 6: four assistant/usage cycles and one user turn. Combined output was 418,721 of 1 MiB; stop/restoration took 0.019 of 30 seconds. No retry/resume occurred. The result was `plan_only`, metadata `missing`, `authority_granted=false` and `gate_satisfied=false`. The model did not confuse exit 0 with freshness, refresh or task completion. Two hypothetical cases respected Codex writer assignment and required reconciliation/waiting for unknown prior effects. They were not actual refusal, cancellation or recovery tests.
- **A02: inherited controller write.** Independent evidence review accepts one actual 1.6.12 controller rebuild at the specified installation/profile and five exact coverage paths, after a clean fixture changed HEAD, with sidecar-bound internal freshness and later file-only readback. The original worker remains `STOPPED_NO_RETRY/AssertionError`: an outer Git-control baseline comparison failed after the successful controller. The two saved Git indexes differ only in one file's stat-cache fields; the writer/mechanism is unknown. A separate final freshness API was not run. Do not mark the whole worker PASS. This was not native Grok refresh and grants no further live calls.
- **L1: synthetic lock evidence.** Four existing pinned-S `ProcessAndOperatorTests` methods passed: same-root contention/linked worktree, lock file/directory identity, cross-process parent replacement/flock, and isolated-home exclusion across repositories. They use synthetic Git fixtures and real Python children, without GitNexus/Node/models. Preserve the first four setup errors caused by a missing info/exclude in an empty Git template; only that fixture was corrected before rerunning the same four methods. The fifth deadline case was not run, and historical transitive deadline-closure limits remain. With Grok default-lock/no-override routing, this supports cooperative exclusion, not native cross-agent concurrency, durable deduplication or vendor DB concurrency.

N1 bound test-time manifest `247fb20b04e1e1aeb3f21c5000fdbf9edc035b340f6b20f2aa9310d126a8dd52`, entry `db4c1629c41bd3ebdc384134c43e111f918b0b62a65314314c2a55aa560222a1`, and the design's S/T sources. Later changes only sync docs and a retrospective capability-reference status paragraph, with its manifest entry. Skills, Core, entry, controller, lock and code remain unchanged; the model was not rerun. Do not label the new manifest as native-tested bytes.

Explicit test authority temporarily trusted only the fixture, fully disabled its MCP config, and paused one existing global hook. The hook's inode/bytes/mode and original trust bytes were verified restored. Retain the first host-checker error and correction: offline rereading of the same successful inspect handled a trailing slash, same-name qualified plugin entries, omitted empty arrays and disabled MCP rows; inspect was not rerun. All 54 source files and 30 fixture payload files were unchanged during the native run; no index was created. Raw session/profile/local-path/tool-stream and restoration records stay controlled. This public repository contains only this safe summary and necessary fixed identities.

## Required observable behavior

| Case | Integration acceptance, not a vendor test | Evidence and limits |
| --- | --- | --- |
| G-USE-01 Authority | Preserve the original request and orchestrator assignment. Either Codex or Grok can be the sole index writer. Missing/conflicting assignment or a review route performs no refresh and returns to the orchestrator. Fields or self-reports grant no authority. | Offline negatives; N1 positive assignment and hypothetical case A, without a native conflicting-writer execution. |
| G-USE-02 Target | Bind repo/worktree/branch/HEAD and index identity explicitly. Conflicting names, checkouts or source stop dependent operations; do not borrow another target's index evidence. | Offline negatives; N1 positive exact fixture selectors. |
| G-USE-03 Entry/command | Use the fixed controller's permitted index-only route. Do not run analyze directly, import a mutable sibling or select latest. Reject missing/incompatible source before process execution. A stub/captured runner checks our argument construction, not GitNexus flag internals. | Offline captured API and N1 actual single plan. A02 is inherited controller write, not native Grok refresh. |
| G-USE-04 Evidence | Use only applicable source, results and sidecar evidence. Keep missing/stale/incomplete/conflicting states explicit. Help, API success, exit 0, metadata or summaries alone prove neither completion nor review or new authority. | N1 correct plan_only/missing/authority=false/gate=false interpretation; original A02 exception retained. |
| G-USE-05 Failure | Rejection, cancel, timeout, partial or uncertain outcomes do not trigger retries or fabricated success. Preserve request, target, action, applicable session/revision and readable evidence; reconcile effects before returning to the orchestrator. | Offline failure paths and N1 hypothetical case B. Actual native refusal/cancel/timeout/resume/recovery remain unrun. |
| G-USE-06 Handoff | Both adapters select the same lock and sidecar contract. Use our stub or applicable existing lock evidence to check that duplicate assignments cannot start a second refresh. No lock stealing or handoff while the previous process is uncertain. This does not test DB concurrency or vendor lock bugs. | Default lock routing plus L1 four cooperative-lock cases; no native cross-agent or durable-dedup acceptance. |
| G-USE-07 Package/claims | Source/plugin layout, relative references, pinned digests/notices and versions agree. Distinguish fixtures, tool evidence and actual agent use. Plans, fixed code or MCP discovery are not completed skill-operation acceptance. | Offline package/digest/reference checks; N1 qualified local skills and full reads. Formal install/update/rollback remain unrun. |

Choose actual cases from coverage in the fixed source. Add only integration gaps, not a duplicate provider suite. Preserve original limits. Raw analyze success does not prove skill selection or invocation. Missing or uncovered evidence stays NOT_RUN/pending; unrelated PASS cannot close it.

## Method and stops

Prefer data fixtures, stubs/captured runners and package/reference/digest checks without starting GitNexus. Do not change current indexes, the user registry, global settings, installed content or another repo. Environment-changing checks use only an isolated test project. Do not activate hooks, schedulers, Memory, model routing or credentials.

Reuse applicable existing Grok loading, Core/package and tool-operation evidence. Do not rerun unchanged coverage mechanically; changed guidance and entries still need matching evidence. Without actual agent-use observation, keep that scope unverified rather than equating script success with model adoption.

For any additional native Grok invocation, first submit a new bounded proposal with fixed candidate/skill sources, exact fixture/entry/argv, normal sandbox profile with initial ask, allowed tools/writes, inputs/observations, invocation/time/output limits and stop/evidence-preservation behavior to the orchestrator. Prefer existing tool evidence with a harmless integration observation. Any remaining live GitNexus action must be separately identified and authorized. Do not reuse Codex A02 or earlier live-call budgets; do not perform vendor sandbox QA.

Independent review checks current behavior, bilingual duties and claims. Deterministic checks do not replace it. Assess Security Diff Scan from actual impact; the supported scope is limited to the coverage above. Documents and inherited evidence authorize neither refresh nor another native call. This package grants no commit, push, PR, merge, tag/Release, publication or current-installation change.

English follows ASD-STE100 clarity principles; full conformance is unverified. Traditional Chinese uses the fixed Core plain-writing adaptation.

</details>
