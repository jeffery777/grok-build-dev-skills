# Core v0.2.0 正式採用準備 / Formal adoption preparation

本來源準備 v0.4.0，普通 Core 固定正式 v0.3.0 commit 7efe4eea59031ed5f9ff9c4a8aef5b8f7d2be02e，完整二十三檔／二十二份 Markdown；封閉套件為39個 payload 加 manifest，共40檔。詳見 [v0.4.0 準備紀錄](../releases/v0.4.0.md)。下方 v0.3.0／Core v0.2.0 及更早的現行身分、數量與未採納說明，保留各來源階段歷史；共同安全、驗證與授權規則仍適用。既有 fixture／pin／分數及 false readiness 不改，消費端發行與安裝仍待另外授權。

This v0.4.0 source prepares published Core v0.3.0 at 7efe4eea59031ed5f9ff9c4a8aef5b8f7d2be02e: 23 Core files, 22 Markdown files and a 40-file closed bundle (39 payloads plus manifest). The linked record defines this source identity. Earlier current-version/count/non-adoption paragraphs retain their historical scope; shared safety, verification and authority rules still apply. Preserve historical fixtures, pins, scores and false readiness flags. Consumer publication and installed adoption remain separate.

本來源現採正式 Core v0.2.0 `6887bfe6183465e9a9e6ccb4ccd7305a58b37302`，版本0.3.0，完整二十檔／十九份Markdown，封閉套件為36個payload加manifest共37檔；詳見 [0.3.0紀錄](../releases/v0.3.0.md)。下文舊版身分、數量、未發布及測試stub敘述保留各準備階段歷史，共同驗證與安全規則仍適用；現行身分與布局以本段及0.3.0紀錄為準。準備fixture的null出版欄位與false flags不改，不能判定後續發布狀態。兩端各一次9/9文字結果僅涵蓋相同四契約，不代表完整runtime資格；既有安裝未更新，四項readiness仍false。產品正式發布須另核對對應annotated tag及Release。

This source adopts published Core v0.2.0 `6887bfe6183465e9a9e6ccb4ccd7305a58b37302` and product version 0.3.0: twenty Core files, nineteen Markdown files and a 37-file closed bundle (36 payloads plus its manifest). See the [0.3.0 record](../releases/v0.3.0.md). Earlier identities, counts, unpublished-state claims and acceptance-stub descriptions below retain their preparation-stage meaning. Shared verification and safety rules still apply; this paragraph and the 0.3.0 record define the current identity and layout. Historical preparation null publication fields and false flags remain fixed and cannot determine later publication. Each consumer's single nine-case text result (9/9) covers only identical four-contract bytes, not full runtime qualification. Existing installations and all four false readiness flags remain unchanged. Product publication separately requires its annotated tag and Release.


## 繁體中文

本包接續 [Issue #36](https://github.com/jeffery777/grok-build-dev-skills/issues/36)、Codex 候選與採用準備及 [Core PR29](https://github.com/jeffery777/engineering-workflow-core/pull/29)。固定 Core reviewed head `cbe3efa1ecc1d2ec04d2edc7078eb22c9dbec038`、tree `3acff4c9241800f47c9df0d642aa21258bab6f92` 的二十檔，含十九份 Markdown及LICENSE，共363639 bytes。完整 raw 集合為 `ff3b48febea205d5f6de33adbe387b420d96f8105b67eeb689bfc55c3e07cae4`；Markdown 集合為 `731b7bc86dade62fba5e59d75829fcf7f9dd746c66077f733e2e8e90016ee287`。這是發行準備來源；publication revision、tag object及Release ID保持 `null`，不可用draft head／tree代填。

[準備資料](../../tests/fixtures/core-release-preparation.lock.json) 固定每個path／raw digest／size／Git mode、集合與具體migration欄位。[唯讀開發驗證器](../../scripts/verify_core_release_preparation.py) 先核資料自身的獨立SHA，再沿用本端 `core_snapshot` 的 no-follow、精確inventory、file type／mode／hardlink／size／讀取漂移及引用檢查，驗raw集合、歷史原文保留與四契約equality。它不下載、不啟動模型、不寫檔、不選正式loader或安裝。來源及完整MIT notice見 [upstream notices](../provenance/upstream-notices.md)。

ADOPT-01 的歷史eval原以移動中的正式vendor比較舊候選；升級後可能把合法舊來源誤判為刪字。另固定v0.1.1十四檔baseline／lock，保留既有 `core.verify` 正式檢查後，逐字比較使用當次checkout的歷史bytes。舊十五檔候選、prompt／cases／scorer不改。臨時測試先要求真正現行loader拒絕二十檔tree，再只stub該測試邊界的未來正式接受，確認舊eval可重現且仍呼叫正式檢查；這不是正式採用或出版證據。

負例驗缺檔／額外項目／tamper、未知pin／虛構出版、unsafe modes／symlink／hardlink／FIFO／祖先symlink、strict JSON及安全拒絕。兩個plain-Python CLI不產生bytecode；此旗標不控制呼叫者import前或整個原生Grok程序的寫入。macOS有離線證據；其他POSIX未資格化，Windows不支援。

此前NOT_RUN／BLOCKED保留為當時歷史；其後同一候選 `87db5867` 已由Codex與Grok各完成一次真實九案文字eval，各9/9。雙consumer文字gate在此範圍內滿足，不代表完整runtime、工具隔離、native subagents或正式loader採用。本包只對逐byte相同的四契約重用；伴讀／清冊／發行文件另審。完整本機證據不公開。

從source checkout以現有Python3.10+標準函式庫執行：

```sh
python3 -B scripts/verify_core_release_preparation.py
python3 -B scripts/verify_core_release_preparation.py --require-publication
python3 -B -m unittest discover -s tests -p test_core_release_preparation.py -v
python3 -B -m unittest discover -s tests -q
python3 -B scripts/core_snapshot.py verify
python3 -B scripts/grok_package.py verify --root /absolute/source/root
```

第一個輸出 `prepared-publication-pending` 並exit0；第二個仍pending且exit1，不能把準備成功當出版。Core真正發行後，先核annotated tag、解參照的完整merge revision、非draft／非prerelease Release及已審tree／二十檔集合；未知保持未知，不追mutable main。若tree／契約改變，補受影響審查／eval。Grok普通lock硬錨是revision／Markdown collection／LICENSE；沒有Code的tag_object欄位。外部publication gate與snapshot驗證分開。

接續以真實publication revision同步 `core_snapshot.CORE_REVISION`、十九個 `MARKDOWN_PATHS`／二十個 `FILES`／衍生目錄、`COLLECTION_SHA256`、core.lock十九份Markdown records與集合、vendor／closure，保留LICENSE原bytes／digest。產品PATHS隨Core擴展，預期bundle31→37，需重建獨立manifest／hash、plugin描述／版本、loading／release文件、notices與依賴；建議consumer minor `0.3.0`。正式切換需驗未知來源拒絕、package parity／closure、fresh staging、失敗不promotion及必要review／安全／平台證據，不能以本helper取代。

當前正式Core仍v0.1.1，產品仍0.2.2與精確31檔，manifest SHA-256保持 `127ec56cb5f03b1b7751ec03ce8e0a3e686d0def57d11d0415b13d1184e93d8e`。兩技能、controller／S/T locks、正式vendor、plugin／manifest不變；開發helper／fixtures／tests／文件不入產品。沒有新模型／原生安裝測試或readiness升級。merge、正式APPROVE、Tag／Release及installed payload更新各須獨立授權；原生安裝／升級／回復須真實證據，不由離線staging推定。

## English

This development packet follows the Codex candidate/adoption-preparation work. It pins Core PR29 reviewed head `cbe3efa1ecc1d2ec04d2edc7078eb22c9dbec038`, tree `3acff4c9241800f47c9df0d642aa21258bab6f92`, and all twenty files: nineteen Markdown documents and LICENSE,363639 bytes. The Chinese section lists separate full and Markdown digests. Publication revision, tag object and Release ID remain null; a draft head/tree cannot prove publication.

Fixed data records every path/digest/size/mode, closure and concrete future migration fields. The developer-only verifier independently pins that data and reuses Grok's no-follow inventory/regular-file/reference controls. It checks collection algorithms, original text and evaluated-contract equality. It neither downloads, starts a model, writes files, selects formal source nor installs. Complete source attribution and MIT notices remain linked.

ADOPT-01 separates historical comparison from moving formal vendor bytes. The existing formal `core.verify` call remains; a fixed fourteen-file v0.1.1 baseline from the selected checkout supplies historical comparisons. The old candidate/prompt/cases/scorer remain unchanged. A temporary regression fixture requires real current-loader rejection, then stubs only a future formal-acceptance boundary and verifies the old eval still calls it. This is regression evidence, not adoption/publication. Negative tests cover corruption, unsafe files, unknown/falsely published pins, strict JSON, bytecode and safe errors. CLI flags do not control caller imports before execution or all native Grok writes. Offline evidence is on macOS; other POSIX remains unqualified, Windows unsupported.

Earlier NOT_RUN/BLOCKED statements remain historical. Subsequently each consumer completed one actual9/9 text evaluation against the same candidate87db5867. This satisfies that narrow dual-consumer gate, not full runtime, tool isolation, native subagents or formal loaders. Reuse covers only byte-identical four-contract semantics. New inventory, companions and release records need their own review; detailed local execution evidence is not published.

Use the commands above. Exit0 means prepared-publication-pending; requiring publication exits1. After actual Core publication, verify annotated tag, resolved full merge revision, formal Release and reviewed tree/set. Reassess changed criteria and rerun affected evals. Grok's ordinary lock pins revision/Markdown collection/LICENSE; tag/Release checks are external provenance gates, not Code's lock schema. Then align vendor, lock, independent constants/allowlist/digests, expected31→37 package closure, manifest, plugin description/version, notices, dependencies and active documents; proposed consumer minor is0.3.0. Verify unknown-source rejection, package parity/closure, fresh staging, no promotion on failure and applicable reviews/security/provider evidence.

Formal changes remain pending. Ordinary Core staysv0.1.1; product0.2.2 and its31files/manifest remain exact. Both skills, controller/S/T locks and normal loader/vendor are unchanged; development preparation stays outside product resources. No new model/native install tests or capability/readiness upgrades are implied. Merge, formal approval, publication and installed-payload updates need separate authority. Native install/upgrade/recovery needs actual evidence beyond offline staging. Full ASD-STE100 conformance is unverified.
