# 來源對照 / Source map

## 範圍 / Scope

本包重用 P0，不重新盤點全部 Codex 程式。固定來源只讀；下列 digest 是來源證據，**不是 P1 final Core lock 或 runtime 資格**。新寫的設計依 P0 與使用者授權整理，未搬移程式或現有技能。完整 MIT notices 見 [upstream notices](upstream-notices.md)。

This package reuses P0 instead of repeating the complete Codex inventory. Fixed sources are read-only. These digests identify source evidence; **they are not a final P1 Core lock or runtime qualification**. The design adapts P0 and the authorized scope. No programs or installed skills were moved. See the [full MIT notices](upstream-notices.md).

## 固定來源 / Fixed sources

Core P0: `0815b74abe52d57efd032bd075e39c83c2ebf0d6`。
Codex: `993597561881d6ed8c552f9a18c59315015ad245`。
SHA-256 均針對 Git blob 的原 bytes / All SHA-256 values cover raw Git blob bytes.

| Repository / path | SHA-256 | 用途 / Use |
| --- | --- | --- |
| Core [dependency-inventory.md](https://github.com/jeffery777/engineering-workflow-core/blob/0815b74abe52d57efd032bd075e39c83c2ebf0d6/docs/architecture/dependency-inventory.md) | `4eed653daff28d5f494bd89445f7110183da032215c6104256795df38e671c47` | P0 E01–E35 相依與 ownership / dependencies and ownership |
| Core [migration-plan.md](https://github.com/jeffery777/engineering-workflow-core/blob/0815b74abe52d57efd032bd075e39c83c2ebf0d6/docs/architecture/migration-plan.md) | `6c6a85f49854a6d2f3ebc054d80d3d81c04780d0bc40d89365a7979497de280c` | lock／組裝／負面例設計 / lock, assembly, negative cases |
| Core [project-split.md](https://github.com/jeffery777/engineering-workflow-core/blob/0815b74abe52d57efd032bd075e39c83c2ebf0d6/docs/architecture/project-split.md) | `ed4877a577d6a8a55b3399c81a86f53da19e2e206a0089a5ba6e44be9be776c1` | 純 Markdown／單向依賴 / Markdown-only, one-way dependency |
| Core [LICENSE](https://github.com/jeffery777/engineering-workflow-core/blob/0815b74abe52d57efd032bd075e39c83c2ebf0d6/LICENSE) | `49d64e81e9fd3b12470c1da48367b120b28d404ca08edfdd950278e28e4da34f` | Core MIT notice |
| Codex [engineering-workflow-contract.md](https://github.com/jeffery777/codex-dev-skills/blob/993597561881d6ed8c552f9a18c59315015ad245/policies/engineering-workflow-contract.md) | `3dd926e8d584404e35abedfbcc8fa1b9c4e90243f421bad1cbea5b170af702d8` | 八階段／授權／獨立審查／停止 / stages, authority, review, stops |
| Codex [verify-engineering-workflow.py](https://github.com/jeffery777/codex-dev-skills/blob/993597561881d6ed8c552f9a18c59315015ad245/scripts/verify-engineering-workflow.py) | `41bf69dddbac3724007f0133616af12e87c0cd7cd4413346833e5307f2d0b176` | Codex/Hermes synthetic，readiness=false；不執行／不搬移 / not executed or moved |
| Codex [sync-plugin-package.py](https://github.com/jeffery777/codex-dev-skills/blob/993597561881d6ed8c552f9a18c59315015ad245/scripts/sync-plugin-package.py) | `4805ce5c82a031a7f982dbfa5a1e575799bdc394971bb18ecbf2051cc17971c8` | canonical source／allowlist／bytes/modes；只查讀 / read only |
| Codex [LICENSE](https://github.com/jeffery777/codex-dev-skills/blob/993597561881d6ed8c552f9a18c59315015ad245/LICENSE) | `a58ebea45ac922c21500dad64c6e5f54423f831d2dfdfd2b4c882aab29822d4e` | 原始來源 MIT notice / original source notice |

## 義務映射 / Obligation mapping

| P0 來源 / Source | Grok 準備設計 / Grok design |
| --- | --- |
| E01, E03, E04, E21–E24 | 各技能保留工作流、授權與停止；不把 shared 當 runtime 合格 / preserve workflow, authority, stops; shared is not qualification |
| E05–E11, E25–E27 | 程式、路由、profile、session 由接口自己持有；Core 不載程式 / adapter owns programs, routing, profiles, sessions |
| E12–E13, E28–E29 | 重用 operational evidence／improvement／candidate evaluation 的責任概念，具體 schemas 留接口，不啟用 memory / reuse responsibilities, keep schemas in adapter, memory stays off |
| E15–E17, E23, E31–E32 | 獨立 review、必要 scan、findings、exact-head；來源專用 GitHub App／ruleset 不默套 / independent review, scans, findings, exact head; no inherited provider profile |
| E18–E20, E30, E33–E35 | 組裝 inventory／bytes／modes、完整 notices、layout 分別驗證；synthetic 不替代 runtime / assembly, notices, layout checks; synthetic is not runtime |

## 官方與隨版證據 / Official and bundled evidence

2026-10-15 查讀 / Accessed 2026-10-15. Websites are mutable documentation, not runtime receipts.

- [Sandbox](https://docs.x.ai/build/features/sandbox), [Permissions](https://docs.x.ai/build/features/permissions), [Settings](https://docs.x.ai/build/settings), [Settings reference](https://docs.x.ai/build/settings/reference), [Enterprise](https://docs.x.ai/build/enterprise).
- [Headless](https://docs.x.ai/build/cli/headless-scripting), [CLI reference](https://docs.x.ai/build/cli/reference), [Skills](https://docs.x.ai/build/features/skills-plugins-marketplaces). Sessions 網頁未成功取得，本包以實際 help 與隨版文件補查；不宣稱已讀該網頁 / Sessions web retrieval failed; actual help and bundled docs were used instead.
- [GFM collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections): README 的 details/summary 只供展開收合，不是互斥 tabs 或自動語言判斷 / details/summary expand sections, not exclusive tabs or language detection.
- Grok `1.0.52 (0920c8169e27)` 在臨時 home 產生的隨版文件 / bundled docs created in the temporary home: `05-configuration.md` SHA-256 `98174c2ae094920a36382084af068c97e902af2cf96c28c7ab01cd7bfde1da50`; `14-headless-mode.md` `e7862bae7ef9e301c0b1448bcd33d35369949c661bdba0cc08b289972e6cb24a`; `18-sandbox.md` `a92e54fd4b542784fae750b1e150a218fc1c1aabb55d70c4f675427fc8908df7`. 未把這些第三方全文提交 / Full third-party docs were not committed.

文件差異與未驗證部分集中於 [資格紀錄](../verification/grok-control-qualification.md)。變更來源 revision 或執行環境時，重新核對受影響證據。

See the [qualification record](../verification/grok-control-qualification.md) for conflicts and unknowns. Recheck affected evidence when source revisions or execution conditions change.

## 現行固定消費 / Current pinned consumption

Active Core revision: `345cd601bffbacc777f87fb24f22b5caefa30a3b`，來自已合併的 [Core PR #8](https://github.com/jeffery777/engineering-workflow-core/pull/8)，由 [G-W1 / Issue #16](https://github.com/jeffery777/grok-build-dev-skills/issues/16) 接入。P3-G1 原固定 P1 revision `b4c37798b6d3a9efd91c8c6d518093f2dd847a98`；上方 P0 與原 P1 身分是歷史來源，不是現行 lock。Core PR #8 is the current source; P0 and the original P1 pin remain historical.

[core.lock.json](../../core.lock.json) 固定全部十份 Markdown digest 與另驗的 LICENSE；[snapshot](../../vendor/engineering-workflow-core/README.md) 是原 bytes 的 generated copy，唯一來源為該 Core revision，不手改副本。The lock pins all ten Markdown digests and a separate license digest. Generated copies retain exact upstream bytes and must not be hand-edited.

| Core 契約 / Contract | SHA-256 |
| --- | --- |
| [workflow](../../vendor/engineering-workflow-core/contracts/workflow.md) | `567a10e20aa91a5a1302f83b82dda69a5deea11fd4971813fa0c53767b4bf859` |
| [authorization-and-stops](../../vendor/engineering-workflow-core/contracts/authorization-and-stops.md) | `26924aba9211929583d2ae31c14a12f9c220c13c8dfbdc43ddf6970d9d5919d7` |
| [review-and-security](../../vendor/engineering-workflow-core/contracts/review-and-security.md) | `28acff344b14968ead954903fb6815d283ed1b4bb8dc2e977a3e37fca7845501` |
| [exact-head-and-evidence](../../vendor/engineering-workflow-core/contracts/exact-head-and-evidence.md) | `c55f08e77a47583485403f7318afe5f2ef1a90ff137279a0c0c59104d5c2e7de` |

集合算法為 `sha256-path-tab-sha256-lf-v1`，集合 SHA-256 為 `ba32220ff76ad4ee3b48195984cd653637a817268b6ed0876869486b81a5dc00`，LICENSE 不在集合內。The collection algorithm uses TAB, not the historical NUL proposal; LICENSE is separate. [消費與限制 / Consumption and limits](../design/p3-g-core-consumption.md) 將原契約義務與本包的離線驗證分開，不宣稱 runtime 合格 / separates obligations from offline checks and makes no runtime qualification claim.

## P3-G2 能力映射 / Capability mapping

[Issue #6](https://github.com/jeffery777/grok-build-dev-skills/issues/6) 的兩份技能與 [Grok references](../../references/grok-capabilities.md) 為此 consumer 新寫的指引，不複製 Codex-specific tools 或重新實作原生 subagents。Core revision／lock／十一份原 bytes 及完整 notices 保持不變。The skill sources and mapping are original consumer guidance; the fixed Core and notices remain unchanged.

[Catalog](../../capabilities/grok-build-1.0.52.json) 記錄既有 1.0.52 help／隨版文件與 2026-10-15 官方研究；網站是可變文件，不是 runtime receipt。新增固定文件指紋：`16-subagents.md` 為 `6556ef4eab94ff5dc01343feedacf525334b23131d626b38b4cd752eeb6c8c78`，`08-skills.md` 為 `a37b169de29bd78160c0cd5c51490610e82a690fc2c866745a7456acdc5345bd`；`14-headless-mode.md` 沿用上方指紋。不分發第三方全文，不匯入其程式。The catalog distinguishes fixed bundled text from mutable websites and unauthenticated operator reports.

[組裝設計](../design/p3-g-skill-assembly.md) 與 [委派資格](../verification/grok-delegation-capabilities.md) 保留 documented／schema-observed／runtime-verified 的界線。Package manifest／packet 是 consumer 自有格式，沒有冒充 Grok 相容 schema；離線驗證不啟用服務、不證明訂閱／API entitlement，且所有 readiness 固定 false。

## G-W1 共用寫作接入 / Shared writing requirements

本包從 immutable Core tree `4a978ea6cb3b168882b2f6e90a4780055ce9b922` 取得十一份原檔，核對 Git blob 與 raw SHA-256，保留 0644 mode。相對原 pin 的五個 generated changes 為 README、workflow、source-map、migration-plan 與 project-split；後兩份包含前一個 Core 導讀包。其餘檔案及 LICENSE bytes 不變。This package consumes eleven immutable raw files with checked blob identities, SHA-256 digests and 0644 modes. Five generated files differ from the original pin; the other files and LICENSE retain their bytes.

Core 交付的十一檔 aggregate `269b1d5a05cc5c8ff9624b9988a0568073fd68ad6e9530ebae0da0286e9e2c12` 僅為來源比對；consumer 仍用上節十份 Markdown collection，LICENSE 分驗，不混用。The eleven-file source aggregate is not the consumer Markdown collection digest.

兩技能只引用 [Core 寫作條款](../../vendor/engineering-workflow-core/contracts/workflow.md#wf-writing)，在既有 Docs Sync／coherence review 記抽查與限制，不複製一套規則或新增 gate。新增條款來自使用者要求，見 Core 的 [更新來源](../../vendor/engineering-workflow-core/docs/provenance/source-map.md#plain-writing-update)，不是原 Codex P1 抽取內容。英文依 ASD-STE100 原則編寫，尚未完成完整符合性驗證；繁中採對應簡明原則，不宣稱符合英文標準。The skills refer to the shared clause within existing review. Its source is the accepted user requirement, not the original P1 extraction. English follows ASD-STE100 principles; full conformity is unverified. Traditional Chinese uses adapted clarity principles.

這次更新不改既有安裝或 trusted fixture，不啟動 Grok runtime；原資格記錄與 false readiness 保留。This update does not change existing installations or the trusted fixture, start Grok, or upgrade runtime qualification/readiness.
