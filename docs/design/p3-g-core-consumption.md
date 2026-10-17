# 固定 Core 的離線消費 / Offline Core consumption

[繁體中文](#consumption-zh) · [English](#consumption-en)

<a id="consumption-zh"></a>

## 繁體中文

### 能做什麼

P3-G1 為 [Issue #4](https://github.com/jeffery777/grok-build-dev-skills/issues/4) 提供固定 Core snapshot、離線完整性驗證及新的臨時 staging。它不載入技能、不安裝、不下載、不啟動 Grok／模型／session，也不提供 permission 或 resume adapter。驗證成功只證明已列出的檔案與引用；runtime 與 delivery readiness 固定為 false。

[core.lock.json](../../core.lock.json) 鎖定 Core repository、完整 revision `174df2af8dedf813b9bd4e3c184a627ee87d3cd8`、繁中權威語言、十二份 Markdown 的 path/digest 與 LICENSE。程式另持有固定 revision、集合與 LICENSE digest，不能只改 lock 就切換信任來源。這些信任錨的更新必須有新的來源審查與受影響驗證。

[固定副本](../../vendor/engineering-workflow-core/README.md) 保留十三份 upstream 原 bytes，都是 generated copies。唯一來源是固定 Core revision；不可手改副本或插入翻譯／generated header。衍生標記、改寫說明及來源放在 lock 和 [provenance](../provenance/source-map.md)。保留 [Core LICENSE](../../vendor/engineering-workflow-core/LICENSE) 與 [完整來源 notices](../../vendor/engineering-workflow-core/docs/provenance/upstream-notices.md)。

[G-W1 / Issue #16](https://github.com/jeffery777/grok-build-dev-skills/issues/16) 將固定來源更新至 [Core PR #8](https://github.com/jeffery777/engineering-workflow-core/pull/8) 的 merge revision，讓 skills 引用 [共用寫作條款](../../vendor/engineering-workflow-core/contracts/workflow.md#wf-writing)。這次更新保留既有驗證算法、介面與 readiness 限制；詳細來源與 digest 見 [provenance](../provenance/source-map.md)。

[GG1 / Issue #18](https://github.com/jeffery777/grok-build-dev-skills/issues/18) 當時接入 [Core PR #12](https://github.com/jeffery777/engineering-workflow-core/pull/12) 的最終 revision，同包採用證據生命週期與風險優先審查；前述 G-W1 是先前寫作接入記錄。入口操作見 [專案政策](../../README.md#採用的工作流與專案政策)，現行 lock／程式 anchors／snapshot／manifest 一致更新，驗證算法與 false readiness 不變。

[G-SA1 / Issue #20](https://github.com/jeffery777/grok-build-dev-skills/issues/20) 當時採 [Core PR #14](https://github.com/jeffery777/engineering-workflow-core/pull/14) 的正式 merge revision，將共用安全適用性、能力缺口、外部補查與正式例外改為固定契約引用。Grok 方法及控制仍由接口適配；完整來源、兩檔差異與 digest 見 provenance。本更新不改驗證算法或 runtime readiness。

[G-RF1 / Issue #22](https://github.com/jeffery777/grok-build-dev-skills/issues/22) 當時採 [Core PR #16](https://github.com/jeffery777/engineering-workflow-core/pull/16) 的正式 merge revision。兩技能於適用情況導讀共用的 [前提、方案與停止條款](../../vendor/engineering-workflow-core/contracts/workflow.md#wf-assumptions-and-options)，沿用既有 plan／report；簡單低風險工作保留簡短處理，必要安全、授權、獨立審查與 exact-head gates 不因停止改善而解除。來源與四份 generated 差異見 provenance。

[G-REL1 / Issue #26](https://github.com/jeffery777/grok-build-dev-skills/issues/26) 採正式 Core v0.1.0：tag object `e984c880a05065c8bcd0d78e83d78220b05bfc32` 解析至上述 commit。十三檔 aggregate 為 `3c985420e8017bde6b59f2625d451686202e2f6a03d807a361df166634a88de9`，與十二份 Markdown collection 分列；Core 不必另裝，版本與 consumer 獨立。正式來源與四份 generated 變更見 [provenance](../provenance/source-map.md)。Formal Core adoption expands only the closed inventory and anchors, not verification algorithms, runtime controls or readiness. The four contracts and other protected files retain their bytes.

### 集合與引用

算法 ID：`sha256-path-tab-sha256-lf-v1`。

1. 僅對 lock 的十二份 Markdown，按 UTF-8 path bytes 排序。
2. 每筆編碼為 `path + TAB + lowercase_sha256 + LF`，不含 JSON 引號或空格。
3. 對十二筆串接的 1135 bytes 做 SHA-256，結果必須為 `484923e7dc1407dde1702cf88e93afb5a279b25f79a2c6ff9631d58d7589ab13`。
4. LICENSE 不計入此集合，另驗 SHA-256 `49d64e81e9fd3b12470c1da48367b120b28d404ca08edfdd950278e28e4da34f`。

P2 曾提出 NUL 分隔，沒有實作為正式 lock；P3-G1 明確採 TAB，不能混用 digest。Manifest path 限已核可的 ASCII POSIX 相對路徑，拒絕重複、空／點／父目錄片段、絕對／越界／未知路徑、反斜線及 TAB/LF/CR/NUL。每檔 digest 使用原 bytes，不做換行或 Unicode 正規化。

從 README 與四份契約出發，完整相對引用閉合為十二份 Markdown 與 LICENSE，共十三檔；新增 Core CHANGELOG／release notes 也保留原 bytes。這是檔案／引用閉合，不要求 runtime 每次載入全部文件。檢查本地檔案與 fragments，支持此固定集合所用的 inline/reference links、HTML href/src、explicit anchors 與 ATX headings。外部 URL 不連線。這不是通用 GFM validator；新 Core 內容或語法須重新審查 parser 與閉合。

### 契約義務映射

| Core 契約 | 本包消費方式與限制 |
| --- | --- |
| [workflow](../../vendor/engineering-workflow-core/contracts/workflow.md) | 完整 bytes／引用可用；技能入口必讀八階段、風險與檢查時機、證據生命週期、簡明寫作、能力與委派／Outcome 義務。本包沒有實作 workflow executor |
| [authorization-and-stops](../../vendor/engineering-workflow-core/contracts/authorization-and-stops.md) | 不推定外寫授權，不覆寫既有 staging，失敗保留新目標；沒有 approval engine |
| [review-and-security](../../vendor/engineering-workflow-core/contracts/review-and-security.md) | 程式與組裝邊界須獨立 review／適用 scan、findings disposition；不沿用 P2 的 scan N/A |
| [exact-head-and-evidence](../../vendor/engineering-workflow-core/contracts/exact-head-and-evidence.md) | 固定文件／notices／明確集合；正式交付另綁 exact Git range、coherence、平台與授權，不以 CLI bool 代替 |

### 使用與檔案安全

在 repo root 使用既有 Python 3.10+ 的標準函式庫，不安裝依賴。以本機已選定的 `python3` 執行：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/core_snapshot.py verify
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

macOS 臨時 staging 範例：

```sh
p3g_parent="$(mktemp -d /private/tmp/grok-core-stage.XXXXXX)"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/core_snapshot.py stage \
  --destination "$p3g_parent/core"
```

`--lock`、`--snapshot` 可選擇核可的本地副本；所有祖先與檔案都不得是 symlink。Snapshot 必須是 exact inventory、一般且非 hardlinked 的 0644 檔案；單檔上限 1 MiB。程式以 no-follow descriptors 讀取，核對讀取期間的檔案／目錄變化，完整驗證後才建立 staging，並使用已驗證的記憶體 bytes 寫入後讀回。

Staging 限系統 `/tmp` 或 `/var/tmp` 的 canonical 實體目錄下；不信任環境變數來擴大目的地。macOS 的 `/tmp` 本身是 symlink，範例因此使用 `/private/tmp`。父目錄必須已存在，目的地必須全新且位於 snapshot 之外。目錄為 0700，檔案為 0644；不採納、合併或覆寫既有目標。寫入失敗可能保留部分新目標；先檢視，不盲目重播、刪除或覆寫。

驗證成功 exit 0；輸入／檔案拒絕 exit 1；CLI 用法錯誤 exit 2。錯誤不回印輸入內容或完整路徑。輸出記錄 Core identity、lock/assembler digest、assembler format version、layout 與 Python version。Assembler version 不是軟體 Release。正式交付者另記 adapter repo 的 exact Git revision、dirty diff／source version（若有）、使用章節、驗證環境與審查；CLI 本身不證明 Git／forge 身分、啟動狀態或授權。

### 驗證邊界

正負例涵蓋集合順序、錯 identity／schema／算法、缺件／多件／tamper、LICENSE、非法／重複 path、symlink／hardlink／FIFO、mode／size、引用越界／missing anchors、既有目的地保留及 CLI staging 讀回。這些是普通離線程式測試，不證明 Grok 的 sandbox、模型、permission、獨立 reviewer 品質、skill loading 或 session 行為。

程式與信任錨必須可信；這不是對同一使用者可改寫程式或主機的攻擊者所建立的 sandbox。macOS 已做本包測試；其他 POSIX 平台仍須各自驗證。Windows 不在本包支援範圍。既有安裝與 runtime 診斷資料不納入產物。

<a id="consumption-en"></a>

## English

### Supported scope

[Issue #4](https://github.com/jeffery777/grok-build-dev-skills/issues/4) adds a pinned Core snapshot, offline verification, and fresh temporary staging. It does not load skills, install, download, start Grok/models/sessions, or implement permission/resume adapters. Success proves only the listed files and references. Runtime qualification and delivery readiness remain false.

The [lock](../../core.lock.json) pins the Core repository, revision `174df2af8dedf813b9bd4e3c184a627ee87d3cd8`, Chinese contract authority, twelve Markdown digests, and LICENSE. The verifier also fixes the revision and collection/license digests in code. Editing the lock alone cannot select another source. Anchor updates require source review and affected verification.

The thirteen [generated copies](../../vendor/engineering-workflow-core/README.md) retain raw upstream bytes. The fixed Core revision is the only source. Do not hand-edit copies or insert translations/generated headers. Keep modification and source records in the lock and [provenance](../provenance/source-map.md). Retain the [Core license](../../vendor/engineering-workflow-core/LICENSE) and [full upstream notices](../../vendor/engineering-workflow-core/docs/provenance/upstream-notices.md).

[G-W1 / Issue #16](https://github.com/jeffery777/grok-build-dev-skills/issues/16) updates the source to the [Core PR #8](https://github.com/jeffery777/engineering-workflow-core/pull/8) merge revision. The skills refer to the shared [plain-writing requirements](../../vendor/engineering-workflow-core/contracts/workflow.md#wf-writing). The verification algorithm, interfaces and readiness limits remain unchanged. See [provenance](../provenance/source-map.md) for source and digest details.

[GG1 / Issue #18](https://github.com/jeffery777/grok-build-dev-skills/issues/18) adopted evidence lifecycle and risk-first review from the final [Core PR #12](https://github.com/jeffery777/engineering-workflow-core/pull/12) revision. G-W1 above records the earlier writing update. See [project policy](../../README.md#adopted-workflow-and-project-policy) for entry-point behavior. The lock, code anchors, snapshot and manifest change together; verification algorithms and false readiness remain.

[G-SA1 / Issue #20](https://github.com/jeffery777/grok-build-dev-skills/issues/20) adopted the formal [Core PR #14](https://github.com/jeffery777/engineering-workflow-core/pull/14) merge revision. Entry points reference shared security applicability, capability-gap, external-check and formal-exception rules. Grok methods and controls remain adapter-owned. See provenance for the verified source, two-file change and digests. Verification algorithms and runtime readiness remain unchanged.

[G-RF1 / Issue #22](https://github.com/jeffery777/grok-build-dev-skills/issues/22) previously adopted the formal [Core PR #16](https://github.com/jeffery777/engineering-workflow-core/pull/16) merge revision. Both skills conditionally refer to the shared [assumptions, options and stopping rules](../../vendor/engineering-workflow-core/contracts/workflow.md#wf-assumptions-and-options) within the existing plan/report. Simple low-risk work stays brief. Stopping improvement does not release required security, authorization, independent review or exact-head gates. See provenance for the source and four generated changes.

### Collection and references

Algorithm ID: `sha256-path-tab-sha256-lf-v1`.

1. Sort the twelve Markdown entries by UTF-8 path bytes.
2. Encode each as `path + TAB + lowercase_sha256 + LF`, without JSON quotes or spaces.
3. Hash the concatenated 1135 bytes. Required SHA-256: `484923e7dc1407dde1702cf88e93afb5a279b25f79a2c6ff9631d58d7589ab13`.
4. Exclude LICENSE from that collection. Verify its separate SHA-256: `49d64e81e9fd3b12470c1da48367b120b28d404ca08edfdd950278e28e4da34f`.

P2 proposed NUL separation but did not implement a lock. P3-G1 selects TAB explicitly. The two digests are not interchangeable. Manifest paths are approved ASCII POSIX relative paths only. Reject duplicates, empty/dot/parent segments, absolute/escaping/unknown paths, backslashes, and TAB/LF/CR/NUL. Hash original bytes without newline or Unicode normalization.

README and the four contracts reach twelve Markdown files plus LICENSE, thirteen files in complete relative-reference closure. New Core CHANGELOG/release notes retain raw upstream bytes. Closure does not require loading every document on each runtime use. Check local files and fragments for the pinned collection's inline/reference links, HTML href/src, explicit anchors, and ATX headings. Never fetch external URLs. This is not a general GFM validator. Review parser coverage and closure when Core content or syntax changes.

### Contract mapping

| Contract | Consumption and limit |
| --- | --- |
| [workflow](../../vendor/engineering-workflow-core/contracts/workflow.md) | Complete bytes/references are available. Skill entry points must read stages, risk/timing, evidence lifecycle, plain-writing, capability/delegation, and Outcome obligations. No workflow executor is implemented |
| [authorization and stops](../../vendor/engineering-workflow-core/contracts/authorization-and-stops.md) | No inferred external-write authority; no overwrite; retain failed fresh staging. No approval engine |
| [review and security](../../vendor/engineering-workflow-core/contracts/review-and-security.md) | Independent review, applicable scan, and finding dispositions for program/assembly boundaries. P2 scan N/A is not reused |
| [exact head and evidence](../../vendor/engineering-workflow-core/contracts/exact-head-and-evidence.md) | Fixed documents/notices and defined set digest. Delivery separately binds Git range, coherence, platform, and authority; CLI booleans do not replace them |

### Use and file safety

Use an existing Python 3.10+ with its standard library from the repository root. Install no dependencies:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/core_snapshot.py verify
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Example for temporary staging on macOS:

```sh
p3g_parent="$(mktemp -d /private/tmp/grok-core-stage.XXXXXX)"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/core_snapshot.py stage \
  --destination "$p3g_parent/core"
```

Optional `--lock` and `--snapshot` select approved local copies. No path component may be a symlink. Require exact snapshot inventory, regular non-hardlinked 0644 files, and a 1 MiB limit per file. No-follow descriptors and change checks protect reads. Validate all bytes before creating staging, write the captured verified bytes, then read them back.

Stage only below canonical system `/tmp` or `/var/tmp` roots. Environment variables cannot widen the destination. The macOS example uses `/private/tmp` because `/tmp` is a symlink. The parent must exist; the target must be new and outside the snapshot. Directories use 0700 and files 0644. Never adopt, merge, or overwrite an existing target. A failed write can leave a partial fresh target. Inspect it before recovery; do not blindly replay, delete, or overwrite it.

Exit 0 means verification/staging succeeded; exit 1 rejects input/files; exit 2 is a CLI usage error. Errors do not echo input content or full paths. Output records Core identity, lock/assembler digests, assembler format version, layout, and Python version. The assembler version is not a Release. Delivery must separately record adapter Git revision, dirty diff/source version if any, consumed sections, environment, and reviews. CLI output does not attest Git/forge identity, runtime state, or authority.

### Validation limits

Tests cover ordering, identity/schema/algorithm errors, missing/extra/tampered files, LICENSE, unsafe/duplicate paths, symlinks/hardlinks/FIFOs, modes/sizes, reference escapes/anchors, existing-target preservation, and CLI staging readback. These are offline program tests. They do not qualify Grok sandbox, model, permission, reviewer quality, skill loading, or sessions.

Trust the program and its anchors. This tool does not sandbox an attacker who can rewrite the program or host as the same user. This package is tested on macOS; other POSIX platforms need separate verification. Windows is unsupported. Existing installations and private runtime diagnostic data are outside the output.

### 文件品質 / Document quality

英文依 ASD-STE100 原則編寫，完整符合性未驗證；繁中採清晰性原則。English follows ASD-STE100 principles; full conformity is unverified. Chinese uses clarity principles.
