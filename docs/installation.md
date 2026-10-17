# Grok plugin 安裝準備與回復限制 / Installation preparation and recovery limits

[繁體中文](#zh) · [English](#en)

<a id="zh"></a>

## 繁體中文

本文件隨 [G-PI1 / Issue #24](https://github.com/jeffery777/grok-build-dev-skills/issues/24) 提供離線候選，**未發布、未安裝、未啟用**。正式產品版本／Tag、發布來源 commit 及發布時採用的 Core pin 仍由協調者決定。本包不提供一般 installer。

| 身分 | 本候選 |
| --- | --- |
| 產品 | `grok-build-dev-skills`，`0.1.0-candidate.1`（未發布） |
| 內含 Core revision | `64b19bb5658432c42cd6a26aa357fd6b1d0fd857` |
| Core Markdown collection SHA-256 | `37ef5cbdfc9461b43dc76dcd1448943405daf8b6d2a77ee0c1857e7ba9088e15`；LICENSE 分驗 |
| 能力目錄的 Grok 文件版本 | `1.0.52 (0920c8169e27)`，保留原資格界線 |
| 2026-10-17 非模型 help 觀察 | 執行檔 `1.0.60 (01a8e1c591c0)`，未做 runtime case |

Core 是隨包的共用文件，使用者不必另裝或另配版本。[plugin.json](../plugin.json) 顯示產品版本與固定 Core revision；離線 verifier 另輸出兩者及 collection digest。產品版本不表示 Grok CLI 版本或相容性認證。

### 準備可信的完整離線包

先取得經審查及核准的**完整四十位來源 commit**，讀回 remote／commit／tree／ownership，確認 checkout 無非預期修改。此候選尚無已發布來源，不可把 `main`、浮動 tag 或本文件中的產品字串當作可安裝發布。從該可信固定來源執行既有 Python 3.10+ 標準函式庫命令：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify
```

保存輸出中的 `manifest_sha256`、產品版本、Core revision／collection 與來源 commit。Raw manifest digest 必須來自可信來源，不能從待驗副本取值後自證。以下 `TRUSTED_MANIFEST_SHA256` 由操作者填入該已核對值；`BUNDLE` 是全新的完整包目錄，不能指向既有安裝或 discovery root：

```sh
gpi_parent="$(mktemp -d /private/tmp/grok-plugin.XXXXXX)"
BUNDLE="$gpi_parent/package"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py stage \
  --expected-manifest-sha256 "$TRUSTED_MANIFEST_SHA256" --destination "$BUNDLE"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify \
  --root "$BUNDLE" --layout staging --expected-manifest-sha256 "$TRUSTED_MANIFEST_SHA256"
```

組裝僅支援現有 guard 所允許的 canonical 系統暫存 roots，且必須在來源及執行程式 repo 之外。候選的隔離來源／報告 fixture 可放 `~/projects/test`；這不放寬 staging guard。命令不啟動 Grok、不覆寫已存在目標；任何失敗都保留 partial 狀態供查核，不盲目重播或刪除。

完整 bundle 是二十個 payload 加 `grok.package.json` 共二十一檔，包含 `plugin.json`、`skills/`、`references/`、`capabilities/`、兩個 verifier、Core lock、`vendor/engineering-workflow-core/` 及 LICENSE。保持相對佈局，不能只複製兩份 SKILL 或把 Core 扁平化。`--layout source` 容許開發文件；檢查準備好的包須用 `staging`。用可信來源的 verifier 查副本；不能執行可疑副本內的 verifier 建立信任。多餘、自訂、未知、metadata／Core／payload 不符或混合版本均拒絕；PASS 也不授予覆寫權。

### 官方 plugin 路線與目前缺口

2026-10-17 的 [官方 Skills／Plugins 文件](https://docs.x.ai/build/features/skills-plugins-marketplaces)、[CLI reference](https://docs.x.ai/build/cli/reference) 及有指紋的隨版 guide 支持 root metadata、`skills/` 與其他 resources／helpers 隨包分發、版本顯示及 `owner/repo@完整commit` 來源。實際 help 也列本地路徑、`@ref` 與 `#subdir`。這些是文件／help 證據；原生整包複製及跨目錄 Core 引用閉合仍未 live 驗證。

`grok plugin validate <bundle>` 僅供原生 manifest schema 檢查，不能取代 Core／整樹驗證、安裝成功、技能載入或 runtime 資格。安裝與信任是另一次有副作用的操作；本包未執行 install／update／uninstall。`--trust` 會跳過原生確認，不可由本包代為授權；沒有該參數也不當作無副作用 preview。

| 必要保障 | 現有證據與處置 |
| --- | --- |
| 指定版本並看見 Core | 離線 metadata／輸出可辨識；正式發布來源及原生顯示仍待決／驗證 |
| 保護自訂／未知內容 | 原生更新／移除無已證明保障；遇既有、額外、非套件或 ownership 不明內容即停止 |
| 避免失敗混裝及回復 | 原生 atomic update／rollback 未證；現有 helper 僅全新組裝，失敗如實保留 |
| 固定來源重建 | 可重建已審官方 bytes；無須強制永久整包備份；不等於已安裝 plugin 的降版成功 |
| 自動更新控制 | 隨版 guide 只有全域 session-start 設定，未證明逐 plugin 關閉；本包不改設定 |

因此，**任何既有 plugin 的更新、覆蓋、移除及重裝，先停下交回協調者決定保全自訂內容與原生 bookkeeping 的路線**。即使來源／digest 完整也不能跳過此點。Repo `@SHA` 分發可能包含開發檔；不能用 source PASS 代表原生安裝樹等於封閉二十一檔。若需補最小 wrapper，先評估其新維護、ownership、失敗及復原成本，再另行確認，不在此候選擴寫。

### 更新、降版與失敗處理

離線準備新版本或恢復舊官方原件時，選各自已審固定 commit，使用**該版本可信 verifier 及 raw manifest digest**，向另一個全新暫存目標重組並讀回版本、Core、inventory、bytes／modes。不可把新舊檔案疊放；不能用目前版本的 verifier 放行另一版本。合成的兩版本 fixture 只測身份拒絕與全新重組，不是已發布舊版或原生降版／rollback 實測。

自訂檔案不屬於可重建的官方原件。必要保全／暫存備份僅依另行核准的精確範圍，放在所有技能／plugin discovery roots（含使用者配置的額外 roots）之外，不能在技能旁留 `.backup` 副本。此處不建立永久整包備份義務，也不授權刪除自訂內容或清理歷史證據。

失敗時先記錄來源／產品／Core／session（若有）／action／path、exit／錯誤及可確認的部分結果。確認是否已產生副作用，保留 partial 與未知狀態，停止依賴操作並交回協調者；未知結果不盲目重播。真正安裝的更新／舊版重裝須等上述保全路線與原生實證具備後再做。本包所有 readiness 仍為 false，[Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) 保持未完成。

<a id="en"></a>

## English

[G-PI1 / Issue #24](https://github.com/jeffery777/grok-build-dev-skills/issues/24) prepares an **unreleased, uninstalled, inactive** offline candidate. The coordinator still owns the release version/tag, approved release source commit and release Core pin. This package adds no general installer.

| Identity | This candidate |
| --- | --- |
| Product | `grok-build-dev-skills`, `0.1.0-candidate.1` (unreleased) |
| Embedded Core revision | `64b19bb5658432c42cd6a26aa357fd6b1d0fd857` |
| Core Markdown collection SHA-256 | `37ef5cbdfc9461b43dc76dcd1448943405daf8b6d2a77ee0c1857e7ba9088e15`; LICENSE checked separately |
| Documented Grok catalog version | `1.0.52 (0920c8169e27)`; prior qualification limits retained |
| Non-model help observed on 2026-10-17 | Executable `1.0.60 (01a8e1c591c0)`; no runtime case |

Core travels as shared documents; users need no separate Core installation or version matching. [plugin.json](../plugin.json) exposes the product version and fixed Core revision. Offline output also includes the collection digest. The product version does not identify Grok CLI or certify compatibility.

### Prepare a trusted complete offline bundle

Select an approved, reviewed **full forty-character source commit**. Read back remote/commit/tree/ownership and check for unexpected checkout changes. No release source exists for this candidate yet. Do not treat `main`, a floating tag or the product string here as an available release. Run the existing Python 3.10+ standard-library verifier from that trusted fixed source:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify
```

Keep its `manifest_sha256`, product version, Core revision/collection and source commit. Obtain the raw manifest digest independently from the trusted source, never from a suspect copy as its own proof. Set `TRUSTED_MANIFEST_SHA256` to that checked value, then use the [shared preparation commands above](#zh). `BUNDLE` must be a fresh complete-package directory outside existing installations and discovery roots.

The existing guard permits staging only below canonical system temporary roots, outside the source and executing repository. Isolated source/report fixtures under `~/projects/test` do not widen that guard. Commands never start Grok or overwrite an existing target. Keep failed partial state for inspection; do not blindly replay or delete it.

The bundle has twenty payload files plus `grok.package.json`, twenty-one total. It includes `plugin.json`, `skills/`, `references/`, `capabilities/`, both verifiers, the Core lock, `vendor/engineering-workflow-core/` and LICENSE. Keep relative layout; do not copy just the two SKILL files or flatten Core. Source layout permits development files; check a prepared bundle with `--layout staging`. Use the trusted source's verifier with `--root` to inspect a copy. Never run a suspect copy's verifier to establish trust. Extra, custom, unknown, mismatched or mixed-version content fails. A PASS grants no replacement authority.

### Official plugin route and current gaps

The [official Skills/Plugins documentation](https://docs.x.ai/build/features/skills-plugins-marketplaces), [CLI reference](https://docs.x.ai/build/cli/reference) and fingerprinted bundled guide read on 2026-10-17 document root metadata, `skills/`, copied resources/helpers, displayed versions and `owner/repo@full-commit` sources. Actual help also lists local paths, `@ref` and `#subdir`. Documentation/help does not prove live whole-tree copying or cross-directory Core reference closure.

`grok plugin validate <bundle>` checks native manifest schema only. It cannot replace Core/whole-tree checks or establish installation, skill loading or runtime qualification. Installation and trust are separate actions with side effects; this package runs no install/update/uninstall. `--trust` skips native confirmation and cannot be granted by this package. Omitting it is not a proven non-mutating preview.

| Required protection | Evidence and action |
| --- | --- |
| Select version and identify Core | Offline metadata/output identifies both; release source and native display still need a decision/verification |
| Preserve custom/unknown content | No proven native update/uninstall guarantee; stop for any existing, extra, unowned or uncertain content |
| Avoid failed mixed installs and recover | Native atomic update/rollback is unproved; the helper only assembles fresh targets and retains failure state |
| Rebuild fixed official sources | Reviewed bytes can be reconstructed without mandatory permanent whole-package backups; this is not installed-plugin downgrade proof |
| Control automatic updates | The bundled guide documents a global session-start setting, with no proven per-plugin switch; this package changes no settings |

**Stop all updates, replacement, uninstall and reinstall of an existing plugin for the coordinator to select a route that preserves custom data and native bookkeeping.** Valid source/digests do not remove that requirement. Repo `@SHA` distribution may include development files; source PASS cannot prove an exact twenty-one-file installed tree. If a minimal wrapper is needed, assess its maintenance, ownership, failure and recovery costs before separate approval. This candidate does not expand into one.

### Updates, downgrade preparation and failures

For offline preparation of a new version or recovery of old official bytes, select each reviewed fixed source commit. Use **that version's trusted verifier and raw manifest digest** to assemble another fresh temporary target; read back product/Core identities, inventory, bytes and modes. Never overlay versions or ask the current verifier to accept another version. Synthetic two-version fixtures test identity rejection and fresh reassembly, not a released old product or native downgrade/rollback.

Custom files cannot be reconstructed from official sources. Any necessary preservation/temporary backup needs a separately approved exact scope and a location outside every skill/plugin discovery root, including configured extra roots. Do not leave `.backup` copies beside skills. This is no permanent whole-package backup mandate and no authority to delete custom content or historical evidence.

On failure, record source/product/Core/session (if any)/action/path identities, exit/error and confirmed partial results. Reconcile possible effects, preserve partial and uncertain state, stop dependent actions and return to the coordinator. Never blindly replay uncertain outcomes. Live updates or old-version reinstallation wait for the preservation route and native evidence above. All readiness flags remain false and [Issue #2](https://github.com/jeffery777/grok-build-dev-skills/issues/2) remains incomplete.
