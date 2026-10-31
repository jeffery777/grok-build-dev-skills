# Core #24／#26 候選驗證／Candidate evaluation

## 繁體中文

[Issue #36](https://github.com/jeffery777/grok-build-dev-skills/issues/36) 依使用者澄清，在 Codex 候選包完成後接續 Grok，沒有豁免雙 consumer gate。[Codex draft #362](https://github.com/jeffery777/codex-dev-skills/pull/362) 的候選包完成不表示正式 adoption。本包固定 [Core draft #29](https://github.com/jeffery777/engineering-workflow-core/pull/29) 的 `87db5867fbed58c81e64f0c316168d537452425e`，基準為 v0.1.1 `7b66978a76597d09be1b55ad199a969b4ee59c0f`。候選內延後 Grok 的敘述保留為固定來源的點時歷史。

### 固定來源與執行邊界

[測試 lock](../../tests/fixtures/core-feedback-candidate.lock.json) 使用 `grok-core-feedback-test-pin/v1`、`accepted:false`，列出全部十五檔 SHA-256／size／Git mode，檔案逐 immutable Git blob 取得，含完整 LICENSE／notices／相對引用閉合。[離線工具](../../scripts/eval_core_feedback_candidate.py) 另固定 lock digest `bfe8a16bd98ea518ede04ae24638a0acf817c096b84d3a32cb5d6637f9e232c8` 與[九案](../../tests/fixtures/core-feedback-cases.json) digest `c3322e94283f67580b56a32ba185934c1658daedd2a390e2fec950dc48d541cd`；未知 manifest 不能成為新信任來源。

工具重用本端既有 core_snapshot 的 no-follow inventory／regular file／mode／hardlink／大小／讀取漂移及引用檢查。先驗正式 baseline，再以 raw bytes／完整行序確認十四個基準檔保留；LICENSE、authorization、exact-head、原 notices 四檔 equality。不做空白／換行／Unicode 正規化；新增句子完整性與語意一致性另由獨立 reviewer 判斷。

工具不啟動模型、不聯網、不執行 Markdown／shell／Git、不讀憑證、不安裝。支持的 `python3 -B` 入口不寫 bytecode；原生 Grok 可能寫 session／cache，不能宣稱整個程序零寫入。新 helper／fixtures／tests／本文件及 source provenance 不在產品 allowlist；正式 core.lock、vendor、validator、兩技能、plugin／manifest 與 31-file payload bytes／modes 保留，source/package version 仍 0.2.2。普通 loader 仍拒絕候選。

### 重跑與結果（2026-10-31）

在本 repository 根目錄使用 Python 3.10+ 標準函式庫，不新增依賴：

```bash
python3 -B scripts/eval_core_feedback_candidate.py
python3 -B scripts/eval_core_feedback_candidate.py --prompt
python3 -B scripts/eval_core_feedback_candidate.py --observations /absolute/path/to/actual-observations.json
python3 -B -m unittest discover -s tests -p test_core_feedback_candidate.py -v
python3 -B -m unittest discover -s tests -q
python3 -B scripts/core_snapshot.py verify
python3 -B scripts/grok_package.py verify --root /absolute/source/root
```

Prompt 提供完整四契約、情境與所需欄位，不含 expected。九案涵蓋範圍內修正、未決 gap、使用者納入後續輪次、錯標 unrelated 的安全 blocker、無需求 wrapper、既有 Core 義務、無關改善、保留 unrelated 的 gate-only blocker及獨立 severity／disposition／REQ-GAP 欄位。案例 bytes 與 Codex 相同，不可搬用 Codex 答案作 Grok 結果。

Scorer 只查觀測 JSON 的 exact revision、完整同序 IDs、精確欄位／型別及 outcomes；拒絕 duplicate keys、nonfinite JSON、遺漏／多件／錯序與 bool/int 混淆。Synthetic 成功只驗評分器；observations_scored 不認證模型來源。formal_core_adopted／runtime_qualified／merge_authorized 固定 false，單次文字成功也不證明完整 runtime、subagents、reviewer 技術隔離或安裝資格。

- Python 3.13.2：候選十五檔 integrity verified、正式十四檔 verified、產品三十一檔 verified。Manifest SHA-256 保持 `127ec56cb5f03b1b7751ec03ce8e0a3e686d0def57d11d0415b13d1184e93d8e`。
- 新增十六項 candidate tests 與全 suite 一百三十六項通過。首輪十六項有兩個 setup 失敗：未核實的 manifest 常數，以及對不存在字串 replace 而未實際 tamper。已改為讀回的固定 baseline digest與確定改變 bytes 的 fixture，同範圍重跑通過；不抹除原失敗，不把它們稱為模型 eval。
- Grok 1.0.70 公開 help及非模型 inspect 已讀。隔離 home／cwd 的 strict/default inspect 首次因外層 executor EPERM 拒絕；同一 strict/default 原生查核成功，runtime event 回報 strict／macos-seatbelt／enforced:true。未改用較寬 profile；這不驗 deny、網路或全平台資格。
- 乾淨隔離 home 無 hooks／MCP，但沒有本次可用既有登入；沒有複製／讀出 auth、登入或啟用 API fallback。既有登入 home 的同 cwd、strict/default inspect 無 hooks，但仍列兩個 stdio MCP servers 與啟用 plugins。暫時 fixture 的排除設定未取得生效讀回；沒有授予 folder trust、停用全域 hook、改使用者設定或擴權重試。
- 因此 **Grok 模型呼叫與實際答案評分 NOT_RUN／BLOCKED**：可用原生登入與必要來源控制尚未同時成立。不得用單元測試、Codex 9/9 或 strict inspect 代替。這只阻擋相依文字 eval，不重開 Issue #2 全套 sandbox／resume／subagent QA。

沒有新的模型／付費 API 呼叫、GitNexus 操作、Memory／hook／scheduler 啟用、全域安全／權限設定變更、正式安裝或 publication。原始 inspect／路徑／runtime metadata 留在受控工作證據，不提交公開 repo。以上是離線包結果，不是雙 consumer gate 通過。

### 正式採用接續與來源

先以同一 Core 候選完成實際 Grok 文字 eval，記公開入口、有效必要控制、prompt／觀測 digest、版本及可觀察 model／effort，unknown 保持 unknown。需要全域設定、信任、憑證或新服務變更時，先提交確切有界方案及可審查內容；本文件不授權它們。兩端證據充分後再準備 Core 接受／版本與來源身分，重評新 head 的影響，不自動沿用全部候選證據。

正式 Grok adoption 另同步 core.lock／code anchors／allowlist／vendor／manifest／plugin及版本宣稱、closure／notices，補受影響測試、review、必要 scan／CI／exact-head evidence，保留正常來源 fail-closed。Core 發行、consumer adoption、consumer 發行、現行安裝分開。本包止於 draft，不 merge／tag／Release／install。

Helper 的 JSON／scorer／prompt 及案例改編自 [codex-dev-skills@a48a30d](https://github.com/jeffery777/codex-dev-skills/tree/a48a30d7769a5d0f53fa4fa269151114ed624cff) 的 scripts/eval-core-feedback-candidate.py 與 tests/fixtures/core-feedback-cases.json。完整來源 MIT copyright／permission／warranty 已保留於 [upstream notices](../provenance/upstream-notices.md)。這是開發工具來源，不是 sibling checkout 或 runtime 依賴；沒有匯入 Codex 原生 API。

## English

The user clarified sequential work: finish the Codex candidate packet, then implement Grok. The original dual-consumer gate remains. This development-only packet pins all fifteen files of Core PR #29 at the exact revision above, with license/notices, raw digests, Git modes and reference closure. Its lock is not accepted formal Core. Historical deferral text inside that immutable source remains point-in-time data.

The helper separately pins the lock/case digests above, reuses Grok's existing no-follow inventory/file/reference primitives, verifies the formal baseline and preserves all original bytes and complete line order without normalization. Four protected files must remain equal. Independent review checks new sentence completeness and semantics. The helper starts no model/network/shell/Git, accesses no credentials and installs nothing. Supported python3 -B commands avoid bytecode writes; a native Grok process may write sessions/cache. Development files remain outside the product allowlist. Formal Core v0.1.1, both skills, validator and thirty-one-file product payload retain their bytes/modes; source/package version remains 0.2.2. Ordinary loading still rejects the candidate.

The prompt includes all four contracts and nine scenarios without expected outcomes. Cases cover in-scope work, gaps, approved later scope, safety blockers under corrected and retained unrelated labels, unsupported mechanisms, traceable Core duties, unrelated enhancements, and separate severity/disposition/REQ-GAP fields. Case bytes match Codex; its answers cannot substitute for Grok answers. Exact candidate binding, ordered IDs, fields, types and outcomes are scored. Duplicate/nonfinite JSON, missing/extra/reordered data and bool/int coercion fail. Synthetic tests verify scorer mechanics only. Scoring does not authenticate provenance; formal adoption, runtime qualification and merge-authority flags remain false.

Observed on Python 3.13.2: candidate fifteen-file integrity, formal fourteen-file snapshot and thirty-one-file package verification passed, with the unchanged manifest digest above. All sixteen new tests and all 136 suite tests passed. The first focused run had two setup failures: an unverified expected manifest digest and a replacement that did not alter the fixture. Both were corrected using the actual baseline digest and deterministic byte tampering, then rerun. These failures remain recorded and were not model evaluations.

Grok 1.0.70 help and non-model inspect were observed. The first isolated strict/default inspect failed with executor EPERM. The same strict/default native preflight succeeded with an enforced macOS seatbelt profile event; no weaker profile was used. This does not qualify deny, network, or other platforms. A clean isolated home had no hooks/MCP but no available existing native sign-in. No auth was copied/disclosed, no login/API fallback was started. The existing sign-in home had no hooks but still listed two stdio MCP servers and enabled plugins. Fixture-only exclusions did not produce confirming readback. No folder trust, global hook/configuration or security/permission setting changed.

Actual Grok model execution and answer scoring are **NOT_RUN/BLOCKED**: usable native sign-in and verified necessary source controls are not established together. Tests, Codex 9/9 and successful inspect cannot close this gap. This narrow stop does not reopen Issue #2's entire historical qualification checklist. No model/paid API, GitNexus, Memory/hook/scheduler activation, installation or publication action ran. Raw local paths/configuration/runtime evidence stay controlled outside this public repository.

Next, complete a bounded actual Grok text evaluation against the same pin, retaining source/prompt/answer digests, observed controls and honest model/effort limits. Any necessary global configuration, trust, credential or new-service change needs its own exact reviewed scope. With sufficient evidence from both consumers, prepare formal Core acceptance/versioning and reassess changed source identities. Formal Grok adoption separately aligns its lock, code anchors, allowlist, vendor, manifest, plugin/version claims, closure/notices and affected tests/reviews/scans/CI/exact-head evidence. Publication and installation remain separate actions. This packet stops at a draft.

The helper/scorer/prompt and cases adapt the fixed Codex developer source above, with its full MIT notice retained. Grok primitives remain adapter-owned; no Codex runtime API, sibling dependency, framework or generic candidate bypass is imported. English follows plain-writing principles; full ASD-STE100 conformance is unverified.
