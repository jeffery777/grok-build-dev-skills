# Core #21 窄版文字提案／Premise-failure text proposal

獨立人工核對 v2：十一案理由一致；失分案「已證明驗收條件有缺口」沒有明列它是既有已批准條件的缺陷，或尚未批准新增功能的空白。Expected 的 `premise` 適用前一讀法；Grok 理由採後一讀法，但這也不是題幹明說的事實。故仍無法排除測項歧義，不足判定明確的 Core 語義理解失敗。人工疑義不能替代固定全數通過門檻或追改分數。v1 在新 PDF 建議案失分、驗收缺口案正確；v2 前者正確、後者失分；其餘案例及授權／不得擅自實作欄位一致。此次是有效 capture 的評分不一致，不是 NOT_RUN 或權限拒絕。後續須先釐清測項，再另版取得兩端新證據；本輪沒有 v3 或新增模型重試。

Independent manual review agrees with eleven v2 reasons. The failed situation does not explicitly distinguish a defect in existing approved acceptance from an unapproved feature's absence. Expected premise fits the former; Grok chose the latter, which the situation also does not expressly establish. Item ambiguity remains unresolved, so a clear Core-rule comprehension failure is not established. Manual uncertainty cannot replace the fixed full-pass threshold or rewrite scores. V1 failed the PDF suggestion and passed the acceptance-gap case; v2 reversed those outcomes. Other cases and authority/no-implementation fields agree. This is a complete capture with a scoring mismatch, not NOT_RUN or a permission denial. Clarify the item before a separately versioned dual-consumer evaluation. No v3 or further model retry occurs in this packet.

2026-11-01 v2 完整觀測：先完成 Codex fresh v2 的機械與獨立理由 12/12，再以本端新 pin 及獨立原生回應執行同版 `core-premise-failure-cause/v2`，結果 11/12，未通過。原失分 `real-requirement-gap` 已符合預期；本次唯一差異是 `unauthorized-criterion-change` 的 cause，實際 `unproven`、預期 `premise`；該案的不得擅改需求、須等決策及不得實作均正確。有效完整擷取不代表全部語義通過，不宣稱模型已充分符合新義務。雙端 gate 未過，Core 權威原文不改；本輪不再改 prompt 或門檻重試求通過。完整答案、來源與各版結果留受控證據。

Complete v2 observation: after fresh Codex v2 scored12/12 with independent reasoning review, Grok used its own new pin and native response under the same `core-premise-failure-cause/v2` protocol. It scored11/12 and did not pass. The former real-requirement-gap mismatch resolved; only unauthorized-criterion-change differs, with unproven versus expected premise. Its no-unapproved-change, decision and no-implementation answers remain correct. Complete capture is not full semantic success. The dual-consumer gate is unmet; Core authority stays unchanged. Do not change this round's prompt or threshold and retry for a pass. Retain full observations, source and versioned results under controlled evidence.

v2 只新增協定欄位與根因定義及 scorer 的嚴格綁定；題目、expected、四契約、382-byte 引文與門檻不改。根因指既有行為／已批准規格、驗收、設計前提的缺陷或已證實環境失敗；靜態矛盾無須先有執行失敗，未批准新功能的缺席不自行證明缺陷。REQ-GAP 另行分類。缺漏、舊版、未知標籤均拒絕，舊答案不補標籤。此適配接續固定 Codex `ed441cf580a7b8798713d70b3c39c474867fe7b2`；下方 d700／v1／NOT_RUN 段落保留歷史，不代表 v2 結果。

V2 adds the protocol field, generic cause definition and strict scorer binding only. Cases, expected bytes, four contracts, quotation and threshold remain fixed. Cause refers to existing behavior/approved-specification/acceptance/design defects or evidenced environmental failures. Static contradictions need no prior executed failure; absence of an unapproved feature proves no defect by itself. Classify REQ-GAP separately. Reject missing, legacy and unknown tags; never relabel old answers. This adaptation follows fixed Codex `ed441cf580a7b8798713d70b3c39c474867fe7b2`; earlier d700/v1/NOT_RUN text remains historical.

2026-11-01 v1 完整觀測：第二次執行已取得完整十二案答案，機械評分 11/12。未過案為 `real-requirement-gap` 的 cause：實際 `premise`、預期 `unproven`，其餘需求決策／不得實作欄位正確。原分數及第一次逾時均保留；沒有把完整擷取當全部語義通過。獨立核對認為 cause 的指涉仍有歧義，須明確區分有證據的既有缺陷與尚未批准的新功能建議。評估 protocol 後續另版處理，不補標籤重用舊答案，也不接受 Core 義務。下方進行中／NOT_RUN 段落保留先前準備歷史。

Complete v1 observation: the second attempt returned all twelve answers and scored11/12. Only the real-requirement-gap cause differs (premise versus expected unproven); requirement-decision/no-implementation fields are correct. Retain that result and the first timeout. Complete capture is not full semantic success. Independent review identified an ambiguous cause referent; a later protocol must distinguish evidenced existing defects from unapproved feature suggestions. Do not relabel/reuse old observations or accept Core duties. Earlier running/NOT_RUN statements below remain preparation history.

2026-11-01 接續狀態：已實際執行一次 Grok 原生測試，因時間上限中止，沒有完整答案，不計通過。已保留該失敗；另一次相同輸入及控制、較長時間上限的有界測試尚在執行。下文初始 NOT_RUN 保留準備階段狀態，不表示沒有嘗試。雙端門檻仍 pending，Core 權威原文未改。Codex 對應 head `d7002a3d45d33720a73874b186caee7575f7ed4c` 的 Repository Validation 後續已十五項全數成功；其 machine receipt gate 仍因缺 current receipt 未通過，並非正式合併就緒。

Continuation: one actual native Grok attempt reached its time limit without complete answers and is not a pass. Retain that failure. A second bounded attempt uses identical inputs/controls with a longer time limit and is still running. Initial NOT_RUN statements below retain preparation history. The dual-consumer gate remains pending and Core authority is unchanged. Codex's matching head later completed all fifteen Repository Validation jobs successfully; its missing-current-receipt gate still fails, so it is not formally merge-ready.

## 繁體中文

[Issue #38](https://github.com/jeffery777/grok-build-dev-skills/issues/38) 先於遠端 Issue 分支與來源修改建立，接續 [Codex #364](https://github.com/jeffery777/codex-dev-skills/pull/364) 已完成的候選 pin／十二案文字觀測。Codex 完整 CI 的安裝分片尚在執行時，不宣稱其全部 gates 已通過；Grok 這包仍獨立驗證，沒有重用 Codex 答案。

[測試 pin](../../tests/fixtures/core-premise-candidate.lock.json) 固定 [Core #30](https://github.com/jeffery777/engineering-workflow-core/pull/30) `9cec34449cc9557d78842c01d88f3ab561c5823b` 的四完整契約與 [382-byte 原字引文](../../tests/fixtures/core-premise-proposal.txt)，含原提案文件 digest。只去除 Markdown 引句的 `> ` 前綴，原字及 LF 不變。這五份選定語意輸入不是完整二十二檔 Core snapshot／相依閉包、正式採納或普通 loader bypass。

四契約重用既有固定二十檔歷史準備 fixture，先用 Grok 原 `core_snapshot`／準備 helper 驗完整清冊及 raw bytes，再比對本次四個 hash；不跟普通 vendor 前進，也不複製整份來源。舊 reviewed-head／null publication 欄位保留其準備歷史，不改稱已發布證據。候選四契約與已發布 Core v0.2.0 的四契約相同，待測文字仍只在資料檔，未插入權威規則。

[開發 helper](../../scripts/eval_core_premise_candidate.py) 與 [七項測試](../../tests/test_core_premise_candidate.py) 改編固定 Codex `d7002a3d45d33720a73874b186caee7575f7ed4c`，只用 Grok 自己的安全讀取／固定 fixture／JSON 機制；沒有 Codex runtime API 或 sibling 執行依賴。來源與現有完整 MIT notice 見 [source map](../provenance/source-map.md)。候選 source entries 要求 regular、single-link、0644，拒絕 symlink 祖先／final entry、FIFO、不安全 mode、超限與變動讀取。Observation 保持有界嚴格 JSON 資料，不執行、不回貼原始 reason，也不認證真正模型來源。

[十二案](../../tests/fixtures/core-premise-cases.json) 與 Codex 的案例 bytes 相同，涵蓋矛盾驗收、需求缺口與未證實根因的區分、純實作／混合原因、無證據猜測、重評順序、授權、兩輪重評、blocker、評估後模型選擇與環境問題。Prompt 給四契約全文、未生效提案及情境／所需欄位，不給 expected 值。機械評分核對候選、順序、精確欄位／型別及非空簡短理由；理由另須人工查核。合成預期答案只測 scorer，不能當模型回應。舊 #24／#26 九案不能覆蓋這次語義。

目前七項離線測試與固定輸入檢驗已通過；Grok 原生模型觀測為 NOT_RUN。真實執行前須核對本次既有控制的實效、資料範圍及有界輸出／時間，缺件便停止相依執行。這不授權新登入、複製憑證、修改持久安全設定、啟動無關服務或擴權；詳細執行資料留受控位置，公開只列候選、範圍、結果、限制與待辦。

```bash
python3 -B scripts/eval_core_premise_candidate.py
python3 -B scripts/eval_core_premise_candidate.py --prompt
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -B -m unittest discover -s tests -p test_core_premise_candidate.py -v
```

使用 `--observations` 只會評分已取得的 JSON，不啟動模型；不可和 `--prompt` 同用。採納、runtime、merge 授權及 observation 來源認證旗標永遠 false，不拿它們查實際發行狀態。普通 Core v0.2.0／產品 0.3.0、37 檔封閉套件、四項 readiness 與已安裝技能不變。文字結果也不代表完整 runtime／技術唯讀資格。本包只準備 draft，不合併、formal approval、發行或安裝；後續若接受新義務，再依三 repo 獨立版本政策準備相依升級。英文依 ASD-STE100 原則編寫，尚未完成完整符合性驗證。

## English

Issue #38 preceded its remote branch and edits. This follows Codex #364's completed candidate pin and twelve-case text observation. Codex's remaining installer CI shard was still running at preparation; no claim that all its gates passed follows. Grok evaluates independently and never reuses Codex answers.

The pin selects four complete unchanged contracts and the exact 382-byte quotation from Core `9cec34449cc9557d78842c01d88f3ab561c5823b`, with its source-document digest. Remove only the Markdown `> ` prefix; preserve text and LF. These five inputs are not the full twenty-two-file snapshot/closure, formal adoption or a loader bypass. Reuse the independently fixed historical twenty-file fixture, checking it through Grok's existing safe inventory/read helpers and then comparing four selected hashes. Do not follow ordinary vendor changes or duplicate the source. Keep historical reviewed-head/null publication fields unchanged.

The developer helper and seven tests adapt fixed Codex `d7002a3d45d33720a73874b186caee7575f7ed4c` using Grok-owned controls, not a Codex runtime API or sibling dependency. Fixed source files require regular single-link0644 entries; reject symlinks/ancestors, FIFO, unsafe modes, excessive or unstable reads. Observations remain bounded strict JSON data. The scorer executes no answer, echoes no raw reason and authenticates no model provenance.

Twelve case bytes match Codex, covering contradiction/gap/unknown cause, implementation/mixed causes, speculation, reassessment ordering, authority, two-round assessment, blockers, later model choice and environment failure. Prompts omit expected values and contain all four contracts, inactive quotation and requested fields. Scoring checks binding/order/exact fields/types and short reasons; humans must review reasons. Synthetic answers test mechanics only. Old nine-case results cannot cover this proposal.

Seven offline tests and fixed-input checks passed; native Grok model observation remains NOT_RUN. Verify effective existing controls, bounded input/output/time and authority before an actual run, or stop dependent execution. No new login, credential copying, persistent safety change, unrelated service or widened permission is authorized. Detailed execution data stay controlled; public records contain safe candidate/scope/results/limits/TODO only.

Helper adoption/runtime/merge/provenance-authentication flags always remain false and do not represent publication state. Ordinary Core v0.2.0/product0.3.0, the37-file closed bundle, four false readiness fields and installed skills stay unchanged. Text success does not qualify a full runtime or technical read-only control. Draft only: no merge, formal approval, publication or installation. Later acceptance needs separately prepared dependent versions. Keep the existing MIT notices. Full ASD-STE100 conformance is unverified.
