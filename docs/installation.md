# Grok plugin 安裝、更新與回復 / Installation, updates and recovery

[繁體中文](#zh) · [English](#en)

<a id="zh"></a>

## 繁體中文

**0.2.2 為未發布、未安裝的來源準備。** 本輪只同步 Core v0.1.1 與離線封裝；以下原生程序是日後當次精確規劃的參考，不是本版已實測或安裝授權。既有 0.2.1 的正式磁碟安裝已由 [Issue #32](https://github.com/jeffery777/grok-build-dev-skills/issues/32) 驗收，不能據此宣稱已載入新 Core。

本來源為產品 `grok-build-dev-skills` **0.2.2**，內含固定 Core v0.1.1。來源版本由 [plugin.json](../plugin.json) 與 verifier 核對；正式發布須核對 [GitHub Release](https://github.com/jeffery777/grok-build-dev-skills/releases)、annotated tag 及解析後完整 commit。來源版本、合併或本文件不等於已發布／已安裝。本包不新增 installer，不自動更動使用者安裝。

| 固定身分 | 值 |
| --- | --- |
| 0.2.2 raw manifest SHA-256 | `127ec56cb5f03b1b7751ec03ce8e0a3e686d0def57d11d0415b13d1184e93d8e` |
| 正式 Core v0.1.1 commit | `7b66978a76597d09be1b55ad199a969b4ee59c0f` |
| Core Markdown collection SHA-256 | `ef0ed075dfbddd7504f65126deabe135632e4737f3148efaf19551224a577ea5`；LICENSE 分驗 |
| Grok 版本證據 | 目錄1.0.52；歷史 help1.0.60；歷史0.2.1單產品 fixture1.0.62；不認證版本範圍 |

Core 是隨包文件，不必另裝或與產品同步版本。套件保留兩技能、GitNexus 薄入口／固定 controller／source lock、兩個 verifier、Core lock／十四份原件及完整 MIT notices，總計30個 payload加manifest，共31檔。0.1.0的23檔及其 [歷史說明](releases/v0.1.0.md) 使用該版本可信 verifier，不混用版本。

### 準備固定離線包

先核對正式 tag 的完整四十位來源 commit、remote／tree／ownership／checkout 修改。不得猜 commit、把 tag object 當 commit 或以 moving main 代替 pin。使用該固定來源的既有 Python 3.10+標準函式庫；不執行待驗副本內的程式建立信任：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/core_snapshot.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify
```

將 `TRUSTED_MANIFEST_SHA256` 填為由可信發行來源獨立核對的 raw manifest digest，保存產品／Core／collection／manifest及完整來源 commit。`BUNDLE` 必須是尚不存在的完整包目標，位於 source repo、既有安裝及所有 discovery roots之外：

```sh
grel_parent="$(mktemp -d /private/tmp/grok-plugin.XXXXXX)"
BUNDLE="$grel_parent/package"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py stage \
  --expected-manifest-sha256 "$TRUSTED_MANIFEST_SHA256" --destination "$BUNDLE"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify \
  --root "$BUNDLE" --layout staging --expected-manifest-sha256 "$TRUSTED_MANIFEST_SHA256"
```

Stage guard強制 canonical系統暫存roots、排除傳入的source／執行repo並要求全新目標；不會辨識全部安裝或discovery roots。操作者另須核對並排除這些位置，不直接stage到既有安裝。保留相對目錄及31檔，不只複製SKILL或攤平Core。Source archive含開發檔，與封閉bundle不同。Extra／custom／混版／digest或Core不符都拒絕；PASS不是覆寫或信任授權。失敗保留partial，不盲目重播／刪除。

<a id="native-integration-zh"></a>

### 原生安裝與最小更新路線

[官方CLI](https://docs.x.ai/build/cli/reference)、[plugin文件](https://docs.x.ai/build/features/skills-plugins-marketplaces)與隨版guide列出 install／uninstall／update等管理命令。本次 [有界證據](verification/local-plugin-upgrade.md) 顯示：Grok 1.0.62的原生單產品Local copied安裝拒絕同來源直接重裝；先保全、卸載、零註冊讀回、再裝固定新版則成功。這不是所有版本／多產品／自訂內容的更新保證。

操作前由協調者核對實際 Grok binary、有效home／cwd／leader、source、native key／產品數／目的地與ownership、現有session及全部相關discovery roots。僅暫設 `GROK_HOME` 不能證明隔離，default leader可能共用；不得拿廣泛home權限替代精確作用範圍。未知／自訂／非套件／partial內容、外部或不明data、額外來源與ownership疑慮先停止；不擴成供應商QA。

安裝 `--trust` 是明確新增信任，可能啟用技能及該來源宣告的能力；0.1.0信任不自動涵蓋0.2.x的GitNexus寫索引入口。發行、verifier或fixture批准都不授權正式信任。先取得當次精確來源／能力／目的地的必要明確確認，不代答新授權。省略 `--trust` 也不是無副作用preview；原生拒絕案例仍寫log。套件本身沒有MCP／hooks／LSP／agent／額外command定義，不安裝runtime或新增API憑證。

**已驗程序只適用於整個選定Grok home恰一個repository、其中恰一個產品的Local copied layout。若home有任何其他獨立repo或同repo含多產品，在任何SOURCE替換或卸載前停止。0.2.1 曾有 [Issue #32](https://github.com/jeffery777/grok-build-dev-skills/issues/32) 的正式共存／新來源當次驗收；那份證據不涵蓋0.2.2或其他環境，仍須另行精確計畫與當次驗收；不得為達成全域空registry移除其他repo或產品。**

以下命令沿用此單repo／單產品前提；`SOURCE`為原registry記載的完整絕對來源，`LEADER_SOCKET`為已核對操作環境的專用路徑，不能猜值。依序進行，每次原生操作限一次、20秒執行及131072-byte合併輸出判定額度、關閉stdin／無TTY；保留完整問題與作用身分，失敗／未知立即停止：

1. 核對原產品與native key、registry／config、完整source／payload及其版本專屬digest。將舊source、舊payload與必要bookkeeping／data保全至所有探索root之外；保全不等於授權永久刪除。遇未知data或額外內容不繼續。
2. 將已驗固定新版完整31檔準備於**同一SOURCE路徑**，先保全再用全新樹替換，不疊放／不改registry；另保全新版來源。核對原installed舊payload／registry／config未被source替換影響。既有assembler guard不放寬，也不直接stage到該既有路徑。
3. 經精確移除範圍確認後，只卸載該產品。省略 `--confirm`，不跳過意外多產品確認：

```sh
grok --no-auto-update --leader-socket "$LEADER_SOCKET" \
  plugin uninstall grok-build-dev-skills --keep-data
```

4. 僅在上述單repo-home前提下，完整讀回有效空registry，或完整目錄遍歷成功後確認registry不存在且舊payload消失；讀取／解析錯誤不能算零筆。核對來源新31與舊／新保全全部完整，沒有其他有效舊版註冊／payload、未知路徑或非預期config／trust變動。本次fixture的config與enabled名稱未變；不能推論卸載撤銷所有信任。
5. 只有上一步全部通過，且固定新版信任已明確獲准，才執行：

```sh
grok --no-auto-update --leader-socket "$LEADER_SOCKET" \
  plugin install "$SOURCE" --trust
```

6. 讀回恰一個正確Local source／產品0.2.2註冊，記實際native key而不預設值；確認enabled且無disabled衝突。用可信固定來源verifier檢查讀回的 `PAYLOAD_ROOT`，不刪額外檔案強求PASS：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify \
  --root "$PAYLOAD_ROOT" --layout staging --expected-manifest-sha256 "$TRUSTED_MANIFEST_SHA256"
```

核對精確31個regular files／0644／owner／單一連結、source與installed inode獨立、兩技能、固定Core／引用，另記root外bookkeeping。未證明source獨立前保留來源，不刪暫存來源導致註冊失效。新裝若無既有註冊可直接用已驗 `BUNDLE` 代替SOURCE安裝，但同樣先核對寫入、信任與before/after。

Disk state／native inventory不代表session或模型已採用。Guide建議Plugins重新載入或新session；任何另授權模型／resume仍須每次顯式已驗sandbox profile、初始ask及可靠授權轉交通道。本發行沒有模型呼叫，readiness仍false。正式環境尚須自己的當次驗收，不能套用fixture成功。

### 失敗、data與回復界線

`--keep-data`的詳細help證據為1.0.60，1.0.62隨版guide列有此flag。本次無獨立持久data／custom內容；不推定它保留Local source、custom payload或所有trust，也不保證原子回復。若卸載成功但安裝失敗，可能暫時沒有有效外掛；保留partial、全部保全與錯誤，停止交回協調者。不自動重裝舊版、修registry、再卸載或重播。未知結果先調查是否已執行。

重組舊官方bytes使用各版本可信固定來源／verifier／manifest，向全新目標組裝；這不是已驗native降版／rollback，也不能重建custom資料或未知bookkeeping。本包沒有永久整包備份或歷史清理義務；保全留在探索roots之外，刪除另查授權／政策。

`plugin update`省略名稱會更新全部，本路線不使用update-all或把exit0當升級成功。不更動全域自動更新／共享技能路徑。GitNexus 1.6.12能力僅限 [明確技能／薄入口路徑](../references/gitnexus-operations.md)；舊Codex operator CLI仍限定1.6.9。Controller／S/T locks不變，Core固定更新至v0.1.1；沒有原生refresh或vendor資格升級。[Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) 保持歷史、設計完成且非本輪離線發行阻擋，不重開sandbox／deny／resume QA。

<a id="en"></a>

## English

**0.2.2 is unpublished, uninstalled source preparation.** This packet aligns Core v0.1.1 and offline packaging only. Native procedures below are references for a later exact plan, not tested behavior or installation authority for this version. [Issue #32](https://github.com/jeffery777/grok-build-dev-skills/issues/32) accepted the existing formal 0.2.1 disk installation; that does not load new Core.

This source is product **0.2.2**, with fixed Core v0.1.1. Read back [plugin.json](../plugin.json), trusted verifier output, the [formal Release](https://github.com/jeffery777/grok-build-dev-skills/releases), annotated tag and full resolved commit. Neither a version string, merge nor this guide establishes publication or installation. The identity table above applies to both languages; Core needs no separate installation.

### Prepare fixed offline bytes

Verify the formal full source commit, remote/tree/ownership and checkout changes. Use that version's trusted existing Python 3.10+ verifier, never code from a suspect copy to establish trust. The shared Core/package verification and stage commands above use an independently checked `TRUSTED_MANIFEST_SHA256` and a fresh `BUNDLE`. The stage guard enforces canonical system temporary roots, exclusion of supplied source/executing repos and a fresh target. It does not discover every installation or discovery root; the operator must separately check and exclude those locations. Do not widen it or stage into an existing source. Keep the full relative 31-file layout:30 payload files plus manifest, including both skills, fixed controller/source lock, verifiers, Core lock/fourteen originals and full MIT notices. Source archives include development files. Use `--layout staging` for the closed bundle; extras, custom files, mixed versions or wrong Core/digests stop. A PASS grants no replacement or trust authority. Preserve failed partial state.

<a id="native-integration-en"></a>

### Native installation and minimum upgrade route

The [official CLI](https://docs.x.ai/build/cli/reference), [plugin docs](https://docs.x.ai/build/features/skills-plugins-marketplaces) and bundled guide describe management commands. The [bounded fixture](verification/local-plugin-upgrade.md) shows that native Grok 1.0.62 rejects direct reinstallation of an existing same-source Local copy. Preservation, single-product uninstall, zero-registration readback and fixed-source installation succeeded. This does not qualify other versions, multi-product repositories or custom data.

Before action, the coordinator checks the actual binary, home/cwd/leader, source, native key/product count/destination/ownership, existing sessions and every discovery root. A temporary Grok home alone does not isolate the default leader. Stop for unknown, custom, extra, unowned or partial contents and external/unknown data; do not request broad home access or expand into vendor QA.

`--trust` grants explicit trust in the source's capabilities. Existing 0.1.0 trust does not cover the 0.2.x GitNexus index-write entry. Publication, verification and fixture consent grant no production trust. Obtain the necessary specific source/capability/destination confirmation first. An install without trust is not a no-write preview: the observed refusal wrote a log. The package adds no MCP/hooks/LSP/agents/extra-command definitions, runtime installation or API credentials.

**The observed procedure requires exactly one repository in the entire selected Grok home, containing exactly one product in a copied Local layout. Stop before any SOURCE replacement or uninstall if another independent repo or another product exists. Issue #32 accepted one formal 0.2.1 coexistence/new-source transition. It does not qualify 0.2.2 or other environments; coexistence needs a separate exact plan and current acceptance; never remove other repos/products to reach an empty global registry.**

Use the numbered Chinese sequence and exact shared commands above under this single-repo/single-product precondition and the same controls: each native operation once, 20 seconds execution, 131072-byte combined-output acceptance budget, closed stdin/no TTY. `SOURCE` must be the original registered absolute path; `LEADER_SOCKET` is the checked environment's dedicated path. Never guess either.

1. Verify old version, native key, registry/config, complete old source/payload and the version's trusted digest. Preserve source, payload and necessary bookkeeping/data outside all discovery roots; no permanent deletion authority is implied.
2. After preservation, put the verified new complete 31-file tree at the same source path without overlays or registry edits, and preserve the new source separately. Verify old installed payload/registry/config stayed unchanged. Do not bypass the assembler's staging guard.
3. Only with exact removal authority, run the named single-product uninstall--keep-data above, omitting--confirm. Stop for any new question.
4. Under that single-repo-home precondition only, require a valid empty registry, or complete successful traversal proving the registry absent and old payload gone. Unreadable/malformed data is not zero registrations. Verify new source, all recovery copies and unrelated state unchanged. In the observed fixture, config and its enabled name remained; do not infer all trust was revoked.
5. Only after that readback and explicit fixed-version trust, run the shared install command. Require exactly one Local registration/product0.2.2, correct source, actual native key and enabled state without a disabled conflict. Use the trusted fixed-source verifier against observed `PAYLOAD_ROOT`, never delete native extras to force PASS.
6. Check exact 31 regular 0644 files, owner/single hardlinks, separate source/installed inodes, both skills and Core/reference closure; record bookkeeping outside the payload. Keep source until independence is proved. Fresh installation can use verified `BUNDLE` instead of SOURCE only after equivalent scope/trust/before-state checks.

Disk state or native inventory does not prove session/model adoption. The guide suggests plugin reload or a new session. Any separately authorized model/resume still needs an explicit verified sandbox profile, initial ask and reliable approval forwarding on every run. This package starts no model and leaves readiness false. Production needs its own current acceptance; the fixture is not that receipt.

### Failure and recovery limits

Detailed keep-data semantics come from saved 1.0.60 help; the 1.0.62 guide lists the flag. No separate persistent data/custom content existed in this fixture. Do not assume Local source/custom payload/all trust preservation or atomic recovery. Installation failure after successful uninstall can leave zero active plugins: preserve partial state, copies and errors, then stop for the coordinator. No automatic old-version reinstall, registry repair, further uninstall or replay. Investigate uncertain outcomes before acting.

Reassemble old official bytes only from that version's trusted fixed source/verifier/manifest into a fresh target. That is not proved native downgrade/rollback and cannot reconstruct custom data or unknown bookkeeping. Backups remain outside discovery roots; no permanent whole-package retention or cleanup policy is added. Deletion requires its own applicable authority/policy.

Do not use update-all or treat exit0 as upgrade success. This package changes no global updater or shared skill path. GitNexus 1.6.12 support remains limited to the [explicit skill/thin-entry route](../references/gitnexus-operations.md); the older Codex operator CLI remains limited to 1.6.9. Controller/S/T locks stay unchanged; Core is updated to fixed v0.1.1. Native refresh and vendor qualification are not promoted. [Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) remains historical, design-complete and nonblocking for this offline publication; full sandbox/deny/resume QA is not reopened.
