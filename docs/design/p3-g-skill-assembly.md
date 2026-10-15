# Grok 離線技能組裝 / Offline skill assembly

[繁體中文](#zh) · [English](#en)

<a id="zh"></a>

## 繁體中文

[Issue #6](https://github.com/jeffery777/grok-build-dev-skills/issues/6) 承接已驗收的 [P3-G1](p3-g-core-consumption.md)，提供兩個技能原稿、Grok 能力對照、consumer 證據格式及全新臨時組裝。Core 固定於 `b4c37798b6d3a9efd91c8c6d518093f2dd847a98`；lock、十一份原 bytes 與完整 notices 不變。協調入口見 [Program Open Issues](https://chatgpt.com/space/page_548d81ee2cf08191a144063ee8fe571b)。

### 來源與組裝

[workflow 技能](../../skills/grok-engineering-workflow/SKILL.md) 與 [review 技能](../../skills/grok-review-change/SKILL.md) 保留最小入口，必讀固定 Core 與 [Grok references](../../references/grok-capabilities.md)。原稿放在 `skills/`，沒有寫入 `.grok/skills`、使用者技能或 plugin discovery roots。Skill 觸發只載入指引，不產生工具、模型／effort 實效、runtime 資格或操作權。

[grok.package.json](../../grok.package.json) 是 consumer 自有 package format。它列出十九個 payload path／SHA-256；另隨包保留 manifest 原 bytes，因此 staging 共二十檔。Manifest 不 hash 自己；輸出另記其 raw SHA-256。來源 inventory 允許開發用 docs/tests，但 skills/references/capabilities 三個 owned roots 必須 exact。Staging 整個 root 必須 exact，不夾帶 hooks、MCP、credentials、cache 或其他檔案。

Manifest 必須來自已審的可信 Git revision；可同時改寫 manifest 與技能的同權限攻擊者不在其完整性保障內。Digest 不驗簽章、來源真實性或人類授權。Core 另由 G1 的 code-owned revision／集合／LICENSE anchors 驗證，不能靠改 package manifest 替換 Core。

共用 staging helper 先驗 captured bytes／canonical paths，僅在 canonical 系統暫存目錄下建立全新目標，且位於 configured source 及執行程式 repo 之外。No-follow descriptors、regular/single-link 0644 files、單檔 1 MiB、exclusive creation、0700 directories、讀回與 inode 查核維持。失敗保留新 partial target，先檢視，不盲目覆寫、刪除或重播。G1 CLI 原行為與固定來源保持。

### 離線命令

使用既有 Python 3.10+ 標準函式庫，不安裝依賴：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py verify
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py capabilities
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
p3g_parent="$(mktemp -d /private/tmp/grok-package.XXXXXX)"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/grok_package.py stage --destination "$p3g_parent/package"
PYTHONDONTWRITEBYTECODE=1 python3 "$p3g_parent/package/scripts/grok_package.py" verify --layout staging
```

Source 與 staging 的相對佈局相同；可搬移的 bundle 含兩個 verifier，沒有 installer 或 Grok launcher。CLI 不會執行 bundle 內的技能或其他程式。`--root` 選可信本地來源／副本，`--layout` 明選 source 或 staging。成功 exit 0 只證明該離線動作；受限 JSON／filesystem 拒絕 exit 1，用法錯誤 exit 2。錯誤不回印 packet 或 filesystem path；命令列用法診斷遵循 argparse。

### Consumer 證據 packet

此格式只封裝相關工具名稱的 fixture 或 operator report，**不是 Grok 相容 API schema**，不接受 session／approval／runtime-ready 欄位。假例：

```json
{"format":"grok-consumer-evidence/v1","runtime":"grok-build","documented_version":"1.0.52 (0920c8169e27)","source":{"kind":"fixture","sha256":"0000000000000000000000000000000000000000000000000000000000000000"},"observed_tool_names":["spawn_subagent"]}
```

以 `python3 scripts/grok_package.py packet --packet <local-file>` 驗其結構；packet 可為 0600 一般單連結檔，仍有 no-follow 與 size limit。來源 digest 是宣告，不驗證實際 capture 或完整 tool schema。輸出只標 `fixture_only`、`operator_report_unverified` 或 `not_supplied`；兩種 report 都不能升級 schema／runtime 資格。四個 readiness 欄位固定 false，G2-R01–R06 明列仍缺 sandbox/deny、loaded schema/model、派工、授權通道、session recovery、skill loading／entitlement。

### 驗收與邊界

測試涵蓋 source/staging、搬移後 verifier、manifest／Core／引用漂移、duplicate skill、非法 paths、symlink/hardlink/FIFO/modes、既有目標保留、packet 偽造／外來工具／重複 key／整數及 nesting 例外，以及永遠 false 的 readiness。Independent Codex forward-test 只測離線技能指引，不是 Grok skill-loading 或模型資格。

後續 [委派資格清單](../verification/grok-delegation-capabilities.md) 保持未測／blocked；沒有 live ACP、模型、API、訂閱／付費授權、全域設定、安裝或 rollout。Windows 不支援；其他 POSIX 平台未資格化。英文依清晰性／ASD-STE100 原則，完整符合性未驗證。

<a id="en"></a>

## English

Issue #6 adds two skill sources, focused Grok references, a consumer evidence envelope and fresh temporary assembly. The fixed Core revision, lock, eleven raw files and notices stay unchanged. Skills live under `skills/`; no discovery root or existing installation is updated. Triggering instructions creates no tools, authority or runtime qualification.

The consumer manifest hashes nineteen payload files and travels with them as file twenty. Its own raw hash is output separately. Trust the reviewed Git source and manifest; simultaneous manifest/source rewriting by the same authority is outside this integrity check. Core still has separate code-owned anchors. Source layout permits development docs/tests but requires exact owned skill/reference/catalog roots; staging requires the exact whole package.

Use the offline commands above with an existing Python 3.10+ standard library. Staging is new, below canonical system-temp roots and outside both source and executing repository. Captured bytes, no-follow regular/single-link checks, fixed file modes, exclusive creation and complete readback protect the copy. A failed fresh target can remain for inspection. Do not blindly replay, overwrite or delete it. The relocated package contains its verifiers; it contains no installer or Grok launcher.

The JSON example is an internal evidence envelope, not a Grok wire schema. A fixture or operator report cannot authenticate the supplied source digest, validate full tool parameters or prove effective controls. All runtime, skill-loading, delegation and delivery flags remain false. Exit 0 validates only the requested offline action; invalid data/files exit 1, usage errors exit 2. Data/file errors are bounded; argparse handles command-line usage diagnostics.

Tests and independent Codex forward-testing cover offline behavior, not Grok execution. The qualification checklist retains concrete blocked checks. No live transport, API calls, paid service, credentials, installation or global setting is involved. macOS is tested; other POSIX platforms need verification and Windows is unsupported. Full ASD-STE100 conformity is unverified.
