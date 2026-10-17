# Grok plugin 安裝、更新與回復 / Installation, updates and recovery

[繁體中文](#zh) · [English](#en)

<a id="zh"></a>

## 繁體中文

產品 `0.1.0` 沿用 [PR #25](https://github.com/jeffery777/grok-build-dev-skills/pull/25) 的官方 plugin 路線，由 [Issue #26](https://github.com/jeffery777/grok-build-dev-skills/issues/26) 接入正式 Core v0.1.0。先核對 [正式 Grok Release](https://github.com/jeffery777/grok-build-dev-skills/releases/tag/v0.1.0) 的 annotated tag、解析後完整 commit、產品及 bundle digests。發行提供來源與離線套件，實裝尚須下列最小整合；本次發布不修改用戶安裝，也不新增 installer。

| 身分 | 本候選 |
| --- | --- |
| 產品 | `grok-build-dev-skills`，`0.1.0` |
| 正式 Core v0.1.0 revision | `174df2af8dedf813b9bd4e3c184a627ee87d3cd8` |
| Core Markdown collection SHA-256 | `484923e7dc1407dde1702cf88e93afb5a279b25f79a2c6ff9631d58d7589ab13`；LICENSE 分驗 |
| 能力目錄的 Grok 文件版本 | `1.0.52 (0920c8169e27)`，保留原資格界線 |
| 2026-10-17 非模型 help 觀察 | 執行檔 `1.0.60 (01a8e1c591c0)`，未做 runtime case |

Core 是隨包的共用文件，使用者不必另裝或另配版本。[plugin.json](../plugin.json) 顯示產品版本與固定 Core revision；離線 verifier 另輸出兩者及 collection digest。產品版本不表示 Grok CLI 版本或相容性認證。

### 準備可信的完整離線包

先從正式發布資料核對產品 tag 指向的**完整四十位來源 commit**，讀回 remote／commit／tree／ownership，確認 checkout 無非預期修改。不得猜 tag／commit、把 tag object 當 commit，或以浮動 main 代替正式 pin。從該可信固定來源執行既有 Python 3.10+ 標準函式庫命令：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify
```

保存輸出中的 `manifest_sha256`、產品版本、Core revision／collection 與來源 commit。Raw manifest digest 必須來自可信來源，不能從待驗副本取值後自證。以下 `TRUSTED_MANIFEST_SHA256` 由操作者填入該已核對值；`BUNDLE` 是全新的完整包目錄，不能指向既有安裝或 discovery root：

```sh
grel_parent="$(mktemp -d /private/tmp/grok-plugin.XXXXXX)"
BUNDLE="$grel_parent/package"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py stage \
  --expected-manifest-sha256 "$TRUSTED_MANIFEST_SHA256" --destination "$BUNDLE"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify \
  --root "$BUNDLE" --layout staging --expected-manifest-sha256 "$TRUSTED_MANIFEST_SHA256"
```

組裝僅支援現有 guard 所允許的 canonical 系統暫存 roots，且必須在來源及執行程式 repo 之外。候選的隔離來源／報告 fixture 可放 `~/projects/test`；這不放寬 staging guard。命令不啟動 Grok、不覆寫已存在目標；任何失敗都保留 partial 狀態供查核，不盲目重播或刪除。

完整 bundle 是二十二個 payload 加 `grok.package.json` 共二十三檔，包含 `plugin.json`、`skills/`、`references/`、`capabilities/`、兩個 verifier、Core lock、`vendor/engineering-workflow-core/` 及 LICENSE。保持相對佈局，不能只複製兩份 SKILL 或把 Core 扁平化。`--layout source` 容許開發文件；檢查準備好的包須用 `staging`。用可信來源的 verifier 查副本；不能執行可疑副本內的 verifier 建立信任。多餘、自訂、未知、metadata／Core／payload 不符或混合版本均拒絕；PASS 也不授予覆寫權。

### 官方 plugin 路線與目前缺口

2026-10-17 的 [官方 Skills／Plugins 文件](https://docs.x.ai/build/features/skills-plugins-marketplaces)、[CLI reference](https://docs.x.ai/build/cli/reference) 及有指紋的隨版 guide 支持 root metadata、`skills/` 與其他 resources／helpers 隨包分發、版本顯示及 `owner/repo@完整commit` 來源。實際 help 也列本地路徑、`@ref` 與 `#subdir`。這些是文件／help 證據；原生整包複製及跨目錄 Core 引用閉合仍未 live 驗證。

`grok plugin validate <bundle>` 僅供原生 manifest schema 檢查，不能取代 Core／整樹驗證、安裝成功、技能載入或 runtime 資格。安裝與信任是另一次有副作用的操作；本包未執行 install／update／uninstall。`--trust` 會跳過原生確認，不可由本包代為授權；沒有該參數也不當作無副作用 preview。

| 必要保障 | 現有證據與處置 |
| --- | --- |
| 指定版本並看見 Core | 離線 metadata／輸出可辨識；正式來源由 Release／tag 核對；原生顯示仍待實裝讀回 |
| 保護自訂／未知內容 | 原生更新／移除無已證明保障；遇既有、額外、非套件或 ownership 不明內容即停止 |
| 避免失敗混裝及回復 | 原生 atomic update／rollback 未證；現有 helper 僅全新組裝，失敗如實保留 |
| 固定來源重建 | 可重建已審官方 bytes；無須強制永久整包備份；不等於已安裝 plugin 的降版成功 |
| 自動更新控制 | 隨版 guide 只有全域 session-start 設定，未證明逐 plugin 關閉；本包不改設定 |

因此，**任何既有 plugin 的更新、覆蓋、移除及重裝，先停下交回協調者決定保全自訂內容與原生 bookkeeping 的路線**。即使來源／digest 完整也不能跳過此點。Repo `@SHA` 分發可能包含開發檔；不能用 source PASS 代表原生安裝樹等於封閉二十三檔。沿用既有 assembler，不新增 wrapper 或 installer。

<a id="native-integration-zh"></a>

### 指定版本入口與實裝前最小整合項目（尚未執行）

首選入口是「正式來源完整 commit → 可信 verifier／獨立 manifest digest → 全新二十三檔 bundle → 官方本地 plugin install」。以下為**日後有副作用的安裝命令**，發布不執行此命令；只有核對正式來源與下列寫入／保全查核完成後，才由協調者依既有授權接續：

```sh
grok plugin install "$BUNDLE"
```

`BUNDLE` 的產品 `0.1.0`、Core revision、raw manifest digest 必須與正式發布資料相符；不能僅憑目錄名稱辨識版本。官方也記載 `owner/repo@完整commit`，但本方案用已驗的封閉 bundle，避免把來源 archive 的開發檔誤當已安裝 payload。Release source archive 與二十三檔 bundle 是不同內容；若日後附 bundle archive，須由同一個已驗 stage 產生並另記 artifact digest。

| 寫入或信任項目 | 已知事實／實裝前待確認 |
| --- | --- |
| 官方 payload | 預期只含 manifest 列的二十三檔；未證明 native install 實際複製或註冊哪些檔案 |
| 原生位置 | Guide 列出使用者 `~/.grok/plugins/`、專案 `.grok/plugins/` 及可設定的 discovery roots；這不是 install 寫入 leaf 的證據 |
| 設定／bookkeeping／cache／data | 精確路徑、copy 或 source registration、寫入順序與 atomicity 未驗；help 沒有 destination／scope／dry-run 選項，不能臆造 |
| 信任／啟用 | Guide 說使用者 plugin 自動受信任、專案 plugin 需信任；實際持久化位置及有效狀態待讀回。省略 `--trust` 不保證沒有寫入 |
| 權限／憑證 | Payload 不含 hooks／MCP／agent executable 或權限宣告，不新增 API 憑證需求；host／private Git 既有存取及 native 額外要求仍須逐項確認，不代創授權 |

1. 在實裝當下讀回來源／版本／digest、操作者、有效 Grok home、leader、原生路線、既有 plugin ID 與精確目標 ownership。僅設定暫存 `GROK_HOME` 不等於隔離，help 的 leader socket 預設仍可能共用。無法事先界定必要寫入範圍，或遇未知／自訂／partial 內容即停止，不用整個 home 的廣泛授權代替。
2. 保存相關路徑最小 before 清單與必要內容，確認不影響其他技能。日後執行安裝後，讀回 native plugin ID／產品／啟用／信任／實際 payload root 及 before/after 差異。判明持久複製或仍依賴 staged source；未確認前保留 stage，避免註冊暫存路徑後失效。
3. 從可信固定來源執行 verifier，將 `--root` 指向讀回的實際 payload root、使用 `--layout staging --expected-manifest-sha256`。核對 exact 二十三檔、0644 modes、digest、兩個 skill 身分、metadata 及十三份 Core／lock／跨目錄引用。Native bookkeeping 若在 payload root 外須另記；若混在 root 內而 verifier 拒絕，不刪除或放寬 inventory 強求 PASS，回報佈局相容性缺口。
4. `list`／`details` 只能佐證 discovery 與 inventory；不證明模型採用。這份最小整合不啟動模型、不重開 Issue #2 的 sandbox／deny／resume QA。若額外持久權限、新憑證、未知來源執行或新授權提示出現，保留完整問題與原請求、session／revision／action／path 身分，停止等待並交回協調者。

目前沒有 native install receipt；以上均為待執行計畫，不能把文件、help、schema 或 exit 0 記為實裝 PASS。

### 更新、降版與失敗處理

離線準備新版本或恢復舊官方原件時，選各自已審固定 commit，使用**該版本可信 verifier 及 raw manifest digest**，向另一個全新暫存目標重組並讀回版本、Core、inventory、bytes／modes。不可把新舊檔案疊放；不能用目前版本的 verifier 放行另一版本。合成的兩版本 fixture 只測身份拒絕與全新重組，不是已發布舊版或原生降版／rollback 實測。

自訂檔案不屬於可重建的官方原件。必要保全／暫存備份僅依另行核准的精確範圍，放在所有技能／plugin discovery roots（含使用者配置的額外 roots）之外，不能在技能旁留 `.backup` 副本。此處不建立永久整包備份義務，也不授權刪除自訂內容或清理歷史證據。

原生 `update [NAME]` 省略名稱會更新全部，本方案不使用 update-all。`uninstall --keep-data` 的 help 僅承諾保留 plugin persistent data，不證明保留自訂 payload 或提供 rollback，不能拿它當自動復原步驟。隨版 guide 的全域 auto-update 設定也不等於逐 plugin 固定版本保證，本發行不修改它。

失敗時先記錄來源／產品／Core／session（若有）／action／path、exit／錯誤及可確認的部分結果。確認是否已產生副作用，保留 partial 與未知狀態，停止依賴操作並交回協調者；不盲目重播、刪除或卸載。全新重組可還原官方 bytes，不能還原未知原生 bookkeeping。真正更新／舊版重裝須等保全路線與原生實證具備。所有 readiness 仍為 false；[Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) 是設計完成且歷史保留 OPEN 的非阻擋追蹤，不因本輪離線發行而升級或重開。

<a id="en"></a>

## English

Product `0.1.0` retains the native plugin route from [PR #25](https://github.com/jeffery777/grok-build-dev-skills/pull/25) and adopts formal Core v0.1.0 through [Issue #26](https://github.com/jeffery777/grok-build-dev-skills/issues/26). Read back the [formal Grok Release](https://github.com/jeffery777/grok-build-dev-skills/releases/tag/v0.1.0), annotated tag, full resolved commit and product/bundle digests. Publication supplies source and offline artifacts. Actual installation still needs the minimum integration below; publication changes no user installation and adds no installer.

| Identity | This candidate |
| --- | --- |
| Product | `grok-build-dev-skills`, `0.1.0`  |
| Formal Core v0.1.0 revision | `174df2af8dedf813b9bd4e3c184a627ee87d3cd8` |
| Core Markdown collection SHA-256 | `484923e7dc1407dde1702cf88e93afb5a279b25f79a2c6ff9631d58d7589ab13`; LICENSE checked separately |
| Documented Grok catalog version | `1.0.52 (0920c8169e27)`; prior qualification limits retained |
| Non-model help observed on 2026-10-17 | Executable `1.0.60 (01a8e1c591c0)`; no runtime case |

Core travels as shared documents; users need no separate Core installation or version matching. [plugin.json](../plugin.json) exposes the product version and fixed Core revision. Offline output also includes the collection digest. The product version does not identify Grok CLI or certify compatibility.

### Prepare a trusted complete offline bundle

Read the **full forty-character source commit** behind the product tag from the formal release records. Check remote/commit/tree/ownership and unexpected checkout changes. Never guess a tag/commit, mistake a tag object for its commit, or substitute moving main for the formal pin. Run the existing Python 3.10+ standard-library verifier from that trusted fixed source:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify
```

Keep its `manifest_sha256`, product version, Core revision/collection and source commit. Obtain the raw manifest digest independently from the trusted source, never from a suspect copy as its own proof. Set `TRUSTED_MANIFEST_SHA256` to that checked value, then use the [shared preparation commands above](#zh). `BUNDLE` must be a fresh complete-package directory outside existing installations and discovery roots.

The existing guard permits staging only below canonical system temporary roots, outside the source and executing repository. Isolated source/report fixtures under `~/projects/test` do not widen that guard. Commands never start Grok or overwrite an existing target. Keep failed partial state for inspection; do not blindly replay or delete it.

The bundle has twenty-two payload files plus `grok.package.json`, twenty-three total. It includes `plugin.json`, `skills/`, `references/`, `capabilities/`, both verifiers, the Core lock, `vendor/engineering-workflow-core/` and LICENSE. Keep relative layout; do not copy just the two SKILL files or flatten Core. Source layout permits development files; check a prepared bundle with `--layout staging`. Use the trusted source's verifier with `--root` to inspect a copy. Never run a suspect copy's verifier to establish trust. Extra, custom, unknown, mismatched or mixed-version content fails. A PASS grants no replacement authority.

### Official plugin route and current gaps

The [official Skills/Plugins documentation](https://docs.x.ai/build/features/skills-plugins-marketplaces), [CLI reference](https://docs.x.ai/build/cli/reference) and fingerprinted bundled guide read on 2026-10-17 document root metadata, `skills/`, copied resources/helpers, displayed versions and `owner/repo@full-commit` sources. Actual help also lists local paths, `@ref` and `#subdir`. Documentation/help does not prove live whole-tree copying or cross-directory Core reference closure.

`grok plugin validate <bundle>` checks native manifest schema only. It cannot replace Core/whole-tree checks or establish installation, skill loading or runtime qualification. Installation and trust are separate actions with side effects; this package runs no install/update/uninstall. `--trust` skips native confirmation and cannot be granted by this package. Omitting it is not a proven non-mutating preview.

| Required protection | Evidence and action |
| --- | --- |
| Select version and identify Core | Offline metadata/output identifies both; Release/tag identifies the formal source; native display still needs installed readback |
| Preserve custom/unknown content | No proven native update/uninstall guarantee; stop for any existing, extra, unowned or uncertain content |
| Avoid failed mixed installs and recover | Native atomic update/rollback is unproved; the helper only assembles fresh targets and retains failure state |
| Rebuild fixed official sources | Reviewed bytes can be reconstructed without mandatory permanent whole-package backups; this is not installed-plugin downgrade proof |
| Control automatic updates | The bundled guide documents a global session-start setting, with no proven per-plugin switch; this package changes no settings |

**Stop all updates, replacement, uninstall and reinstall of an existing plugin for the coordinator to select a route that preserves custom data and native bookkeeping.** Valid source/digests do not remove that requirement. Repo `@SHA` distribution may include development files; source PASS cannot prove an exact twenty-three-file installed tree. The release retains the existing assembler without a new wrapper or installer.

<a id="native-integration-en"></a>

### Exact-version entry and minimum native integration (not executed)

Prefer the formal full source commit, its trusted verifier and independently obtained manifest digest, then a fresh twenty-three-file bundle and the native local-path install. The shared `grok plugin install "$BUNDLE"` command above is a **future mutation**, not a preview. Run it only after verifying the formal source and the write/preservation checks below, in the coordinator's authorized sequence.

Match the bundle's product `0.1.0`, Core revision and raw manifest digest to the formal release records. A directory name does not identify a version. The guide also supports `owner/repo@full-commit`, but this route uses the verified closed bundle to avoid treating source-archive development files as installed payload. Source archives and the twenty-three-file bundle differ. Any later bundle archive must come from the same verified stage and have its own artifact digest.

| Write or trust item | Known fact / check before installation |
| --- | --- |
| Official payload | Twenty-three expected files; actual native copying or registration remains unverified |
| Native location | The guide lists user `~/.grok/plugins/`, project `.grok/plugins/` and configurable discovery roots; these do not prove the install destination leaf |
| Config/bookkeeping/cache/data | Exact paths, copying versus source registration, write order and atomicity are unknown; help has no destination/scope/dry-run option |
| Trust/enablement | The guide says user plugins are auto-trusted and project plugins require trust; effective state and persistent storage still need readback. Omitting `--trust` does not prove no writes |
| Permissions/credentials | The payload adds no hooks/MCP/agent executable, permission declaration or API credential requirement. Check existing host/private-Git access and any native requirements separately; do not create authorization |

1. At installation time, read back source/version/digests, operator, effective Grok home, leader, route, existing plugin ID and exact destination ownership. A temporary `GROK_HOME` alone does not prove isolation: the default leader socket may remain shared. Stop if the necessary write set is unclear or targets contain unknown, custom or partial state. Do not grant broad home access as a substitute.
2. Retain a minimal before inventory and necessary contents for relevant paths. After the later install, read back native plugin ID, version, enablement, trust, actual payload root and before/after changes. Determine durable copying versus registration of the staged source; retain that source until its independence is proved.
3. Use the trusted fixed-source verifier with `--root` pointing at the observed payload root and `--layout staging --expected-manifest-sha256`. Check exactly twenty-three files, 0644 modes, digests, both skill identities, metadata, thirteen Core files/lock and relative references. Record native bookkeeping outside that root separately. If native extras inside it cause rejection, report layout compatibility; never delete them or weaken inventory to force PASS.
4. Native `list`/`details` show discovery/inventory, not model adoption. This minimum integration starts no model and does not reopen Issue #2 sandbox/deny/resume QA. For extra persistent permission, new credentials, unknown-source execution or a new authorization prompt, preserve the complete question/original request and session/revision/action/path identities, stop and return to the coordinator.

No native install receipt exists. This is a pending plan. Documentation, help, schema checks and exit 0 are not installed-integration PASS.

### Updates, downgrade preparation and failures

For offline preparation of a new version or recovery of old official bytes, select each reviewed fixed source commit. Use **that version's trusted verifier and raw manifest digest** to assemble another fresh temporary target; read back product/Core identities, inventory, bytes and modes. Never overlay versions or ask the current verifier to accept another version. Synthetic two-version fixtures test identity rejection and fresh reassembly, not a released old product or native downgrade/rollback.

Custom files cannot be reconstructed from official sources. Any necessary preservation/temporary backup needs a separately approved exact scope and a location outside every skill/plugin discovery root, including configured extra roots. Do not leave `.backup` copies beside skills. This is no permanent whole-package backup mandate and no authority to delete custom content or historical evidence.

Native `update [NAME]` updates all plugins when the name is omitted; this plan does not use update-all. Uninstall help says `--keep-data` preserves plugin persistent data only. It does not prove custom payload preservation or rollback and is not an automatic recovery step. The guide's global auto-update setting does not establish a per-plugin version lock; this release changes no setting.

On failure, record source/product/Core/session (if any)/action/path identities, exit/error and confirmed partial results. Reconcile effects, preserve partial and uncertain state, stop dependent actions and return to the coordinator. Never blindly replay, delete or uninstall. Fresh reassembly recovers official bytes, not unknown native bookkeeping. Live updates and old-version reinstallation wait for preservation and native evidence. Readiness stays false. [Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) is design-complete historical OPEN tracking, nonblocking for this offline release preparation; this work neither promotes nor reopens its runtime qualification.
