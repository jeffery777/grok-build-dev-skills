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

Active Core revision: `64b19bb5658432c42cd6a26aa357fd6b1d0fd857`，來自已合併的 [Core PR #16](https://github.com/jeffery777/engineering-workflow-core/pull/16)，由 [G-RF1 / Issue #22](https://github.com/jeffery777/grok-build-dev-skills/issues/22) 接入。G-SA1 原固定 `3a3fd41e5fb994b4429a67d76d1b0655d972d150`；[GG1 / Issue #18](https://github.com/jeffery777/grok-build-dev-skills/issues/18) 原固定 `784ed24f4a09ec35ac7209e0fd2287b214aea260`；G-W1 原固定 `345cd601bffbacc777f87fb24f22b5caefa30a3b`；P3-G1 原固定 P1 revision `b4c37798b6d3a9efd91c8c6d518093f2dd847a98`。上方 P0 與這些舊 pin 均為歷史來源。Core PR #16 is the current source; P0, P1, G-W1, GG1 and G-SA1 pins remain historical.

[core.lock.json](../../core.lock.json) 固定全部十份 Markdown digest 與另驗的 LICENSE；[snapshot](../../vendor/engineering-workflow-core/README.md) 是原 bytes 的 generated copy，唯一來源為該 Core revision，不手改副本。The lock pins all ten Markdown digests and a separate license digest. Generated copies retain exact upstream bytes and must not be hand-edited.

| Core 契約 / Contract | SHA-256 |
| --- | --- |
| [workflow](../../vendor/engineering-workflow-core/contracts/workflow.md) | `fd2af36d395a634a89f0de0a486efba19a4ec0d9e88cdda760bc87aa4e15b4d6` |
| [authorization-and-stops](../../vendor/engineering-workflow-core/contracts/authorization-and-stops.md) | `27f02076fdd034c090e341610d7e04f8e79143ec17c1d37a4b57629a04c5e699` |
| [review-and-security](../../vendor/engineering-workflow-core/contracts/review-and-security.md) | `a29ae05f7df55f8469235baff7c59c00a99a0fb9e697e47eb46a9be7c4b90b03` |
| [exact-head-and-evidence](../../vendor/engineering-workflow-core/contracts/exact-head-and-evidence.md) | `ba3419d7090fecce3e84f4ea35cd7695135fb7bbf8c1451502941163d8e873a4` |

集合算法為 `sha256-path-tab-sha256-lf-v1`，集合 SHA-256 為 `37ef5cbdfc9461b43dc76dcd1448943405daf8b6d2a77ee0c1857e7ba9088e15`，LICENSE 不在集合內。The collection algorithm uses TAB, not the historical NUL proposal; LICENSE is separate. [消費與限制 / Consumption and limits](../design/p3-g-core-consumption.md) 將原契約義務與本包的離線驗證分開，不宣稱 runtime 合格 / separates obligations from offline checks and makes no runtime qualification claim.

## P3-G2 能力映射 / Capability mapping

[Issue #6](https://github.com/jeffery777/grok-build-dev-skills/issues/6) 的兩份技能與 [Grok references](../../references/grok-capabilities.md) 為此 consumer 新寫的指引，不複製 Codex-specific tools 或重新實作原生 subagents。Core revision／lock／十一份原 bytes 及完整 notices 保持不變。The skill sources and mapping are original consumer guidance; the fixed Core and notices remain unchanged.

[Catalog](../../capabilities/grok-build-1.0.52.json) 記錄既有 1.0.52 help／隨版文件與 2026-10-15 官方研究；網站是可變文件，不是 runtime receipt。新增固定文件指紋：`16-subagents.md` 為 `6556ef4eab94ff5dc01343feedacf525334b23131d626b38b4cd752eeb6c8c78`，`08-skills.md` 為 `a37b169de29bd78160c0cd5c51490610e82a690fc2c866745a7456acdc5345bd`；`14-headless-mode.md` 沿用上方指紋。不分發第三方全文，不匯入其程式。The catalog distinguishes fixed bundled text from mutable websites and unauthenticated operator reports.

[組裝設計](../design/p3-g-skill-assembly.md) 與 [委派資格](../verification/grok-delegation-capabilities.md) 保留 documented／schema-observed／runtime-verified 的界線。Package manifest／packet 是 consumer 自有格式，沒有冒充 Grok 相容 schema；離線驗證不啟用服務、不證明訂閱／API entitlement，且所有 readiness 固定 false。

## G-W1 共用寫作接入 / Shared writing requirements

本包從 immutable Core tree `4a978ea6cb3b168882b2f6e90a4780055ce9b922` 取得十一份原檔，核對 Git blob 與 raw SHA-256，保留 0644 mode。相對原 pin 的五個 generated changes 為 README、workflow、source-map、migration-plan 與 project-split；後兩份包含前一個 Core 導讀包。其餘檔案及 LICENSE bytes 不變。This package consumes eleven immutable raw files with checked blob identities, SHA-256 digests and 0644 modes. Five generated files differ from the original pin; the other files and LICENSE retain their bytes.

Core 交付的十一檔 aggregate `269b1d5a05cc5c8ff9624b9988a0568073fd68ad6e9530ebae0da0286e9e2c12` 僅為來源比對；consumer 仍用上節十份 Markdown collection，LICENSE 分驗，不混用。The eleven-file source aggregate is not the consumer Markdown collection digest.

兩技能只引用 [Core 寫作條款](../../vendor/engineering-workflow-core/contracts/workflow.md#wf-writing)，在既有 Docs Sync／coherence review 記抽查與限制，不複製一套規則或新增 gate。新增條款來自使用者要求，見 Core 的 [更新來源](../../vendor/engineering-workflow-core/docs/provenance/source-map.md#plain-writing-update)，不是原 Codex P1 抽取內容。英文依 ASD-STE100 原則編寫，尚未完成完整符合性驗證；繁中採對應簡明原則，不宣稱符合英文標準。The skills refer to the shared clause within existing review. Its source is the accepted user requirement, not the original P1 extraction. English follows ASD-STE100 principles; full conformity is unverified. Traditional Chinese uses adapted clarity principles.

這次更新不改既有安裝或 trusted fixture，不啟動 Grok runtime；原資格記錄與 false readiness 保留。This update does not change existing installations or the trusted fixture, start Grok, or upgrade runtime qualification/readiness.

## GG1 治理契約接入 / Governance contract adoption

[Issue #18](https://github.com/jeffery777/grok-build-dev-skills/issues/18) 採 Core Issue9/PR10、Issue11/PR12 的最終 immutable revision `784ed24f4a09ec35ac7209e0fd2287b214aea260`，tree `100af4a54e1741bb0fc214ad2c1d664f4c065f81`。十一份 generated raw files 依 Git blob／SHA-256／size／100644 mode 核對；相對 G-W1 六檔變動：README、四契約及 Core source-map，其餘五檔與完整 notices 不變。This package adopts the final immutable Core revision after both governance packages; six generated files change and five retain their bytes.

十一檔 handoff aggregate `9517d611999058c1667eb255e38791f7189db501ca36d004759a62165d977b53` 只比對來源；consumer 使用上節十份 Markdown collection，LICENSE 仍分驗。The eleven-file aggregate is a source comparison, separate from the consumer collection and LICENSE.

現有 skills／README 接入 [風險與檢查時機](../../vendor/engineering-workflow-core/contracts/review-and-security.md#review-risk-timing) 及 [證據生命週期](../../vendor/engineering-workflow-core/contracts/workflow.md#wf-evidence-lifecycle)，不新增執行框架或改 schema。新共同義務來自使用者接受的要求，見 Core [lifecycle 來源](../../vendor/engineering-workflow-core/docs/provenance/source-map.md#evidence-lifecycle-update) 與 [risk 來源](../../vendor/engineering-workflow-core/docs/provenance/source-map.md#risk-review-update)；不倒寫成 P1 Codex 抽取義務，也不升級既有寫作符合性證據。Existing entry points consume both user-origin contracts without a new executor or schema. Prior provenance and writing/conformity limits remain.

本包先檢查敏感治理／信任邊界，依實質 diff 做比例安全檢查，再以最終候選核對必要證據。沒有全庫 deep scan 的通用要求或成本改善承諾；變更後須有受影響驗證及可證未變證據的重用理由。未執行 Grok／runtime、歷史 cleanup／搬移／歸檔／刪除、安裝或 global rollout；舊 trusted fixture 保持原 pin。This package performs no runtime, historical evidence cleanup or installed/global rollout.

## G-SA1 安全方法適配 / Security method adaptation

[Issue #20](https://github.com/jeffery777/grok-build-dev-skills/issues/20) 依使用者持續推進及區分 Grok／Codex 安全審查的要求，在兩個既有 skills 與 Grok mapping 補方法選取、政策／風險／coverage 充分性、findings 證據及缺失／拒絕狀態。R1／R2 當時沿用 GG1 的固定 Core，未改 vendor、lock、程式、測試或原生控制；manifest 只同步三份封裝指引的 digest。R1/R2 added method and evidence guidance while retaining the GG1 pin. The integration below supersedes that candidate state.

材料為使用者上傳的 `grok-build-security-review-2026-10-16(1).md`。協調父端完整閱讀 16,447 bytes 後提供核對摘要；本 executor 的支援 Library materialization 下載失敗，確認未產生目標檔，故依父端摘要形成 consumer 指引，不宣稱本人直接讀過全文或編造原檔 digest。The coordinator read the complete uploaded material and supplied the checked summary. This executor's Library download failed without a local target, so the adaptation uses that summary and makes no direct full-text or source-digest claim.

採納安全分析／scanner／品牌產品分流、source-to-sink 與信任邊界、severity／confidence／適用 CWE／前提／影響／驗證／補償控制、已做／未做與 coverage、共同盲點及資料傳輸／留存的區分。未採用新增共用 skill／.agents 路徑、Orca、每次 PR 一律 scanner、高風險只做輕量 review 或未核對命令。第三方技能僅供參考，沒有安裝授權；未複製第三方技能或程式。Adopted concepts cover method boundaries, security evidence, shared blind spots and transmission versus retention. Conflicting workflow, installation and command suggestions are not adopted; no third-party skill or program is copied.

2026-10-16 已查證 [Skills](https://docs.x.ai/build/features/skills-plugins-marketplaces)、[Subagents](https://docs.x.ai/build/features/subagents)、[Settings](https://docs.x.ai/build/settings/reference) 與 [Permissions](https://docs.x.ai/build/features/permissions)：技能 metadata 不建立工具／模型控制；原生子代理與有效設定由 runtime 提供。這些是可變官方文件，不證明專用 scanner 存在或本機新路線已實測。The official sources support documented native capabilities, not a dedicated scanner or a runtime qualification claim. No live Grok case, scanner installation, global change or cross-platform automatic fallback is included; offline readiness remains false. Earlier qualification and acceptance history is retained, not reset by this update.

使用者於 2026-10-16 09:25 UTC 補充：先按風險／變更及有效公司政策判斷必要方法，再查工具／插件；缺第三方能力須記錄並交接部門補查，不能令無相依開發停擺。兩語 mapping 與兩個入口因此補 NOT_RUN／UNAVAILABLE、原因／coverage／影響、受控交接內容與回收證據核對。真正強制 gate 等待外部證據或政策允許且有權者核准的例外，原缺件仍不算 Passed，低風險亦不自行免除公司強制項。This user clarification adds availability checks and a bounded handoff, preserving independent work while only dependent actions wait. A handoff or approved exception is not a completed scanner run or a self-authorized risk acceptance.

同次授權允許沿用原支援的 `/private/tmp` 全新隔離 tests／assembly，不放寬 guard、不改測試或安裝缺少的 yaml；先前 `~/projects/test` 目標遭 guard 拒絕的證據保留。這是本包驗證範圍的修正，不是可重用技能的固定測試目錄要求。The same authorization permits existing offline tests and assembly in fresh system-temp isolation. It does not authorize live Grok/model cases, installation, global changes or bypasses; the earlier guard refusal remains historical evidence.

後續澄清將有效政策判不需要的 scanner 記為 NOT_REQUIRED／NOT_APPLICABLE，與工具缺失／待補證據分開；可繼續開發不代表可發行，公司不可豁免規範仍有效。本包的共用政策／外部補查文字待 Core 原 owner 的最小 vendor-neutral 增量交付後改為引用，避免兩端永久複製。R2 當時尚未取得新 immutable pin，整合狀態為 pending，使用 `784ed24f4a09ec35ac7209e0fd2287b214aea260` 並保留本候選離線驗證，不手改 vendor 或宣稱已採新契約。Policy-supported nonrequirements are not missing-tool debt. Common policy/handoff guidance awaits the Core owner's increment and will become a reference to that fixed contract; R2 validation did not claim that integration was complete. The following adoption supersedes the pending state.

## G-SA1 Core Issue13 接入 / Core Issue13 adoption

2026-10-17 核對正式 PR #14 的 merged 狀態、merge revision `3a3fd41e5fb994b4429a67d76d1b0655d972d150`、reviewed source `139ef2ff29af70c7592910c2ec598a9943cc934f` 與共同 tree `83c9457a805a0aad204138543dc2f7ee77752735`。十一份 immutable raw blobs 的 Git blob 身分、size、SHA-256 與 100644 mode 均與持久 handoff 一致。相對 GG1 只有 review-and-security 與 Core source-map 變更，其他九檔及 LICENSE bytes 不變。Official PR, commit/tree identities and eleven raw files match the persistent Core handoff. Only the review/security contract and Core source map change from GG1.

十一檔來源 aggregate 為 `3ba2c2115bb582009c925148e0fda8708b4aed3d99f4eed6ed0e3b35b5246e2c`；G-SA1 當時的十份 Markdown collection 為 `cf5a027c818967a5c1bc46fabb36aba88b8264bde0c3ee81e2c4aff813d2a428`，LICENSE 分驗。Lock、程式常數、generated bytes、manifest、文件及受影響測試同包更新，驗證算法不變。The eleven-file source aggregate, ten-Markdown collection and separate LICENSE digest serve different checks; verifier algorithms are unchanged.

兩技能及 mapping 改引固定 Core 的 [安全適用性](../../vendor/engineering-workflow-core/contracts/review-and-security.md#review-security) 與 [證據及續行](../../vendor/engineering-workflow-core/contracts/review-and-security.md#review-evidence)，共用政策、能力缺口、外部補查與正式例外由 Core 持有；Grok 仍持有方法、實際工具／模型、資料與 session 控制適配。不把 Core 的安全掃描移作本候選的掃描證據；本候選審查與必要安全 gate 另綁完整 diff。Consumer entry points reference shared policy while retaining Grok-specific methods and controls. Core's scan is not this adapter candidate's scan. Runtime qualification and offline false readiness remain unchanged; no installed skill or global rollout is included.

## G-RF1 Core Issue15 接入 / Core Issue15 adoption

[Issue #22](https://github.com/jeffery777/grok-build-dev-skills/issues/22) 採已合併的 [Core PR #16](https://github.com/jeffery777/engineering-workflow-core/pull/16)：merge revision `64b19bb5658432c42cd6a26aa357fd6b1d0fd857`、reviewed source `8b546d8c27a3db416ef7021a01fdae3ffa572ec6`、共同 tree `28e39d4385090bb321aa80337ea74aad196e2042`。十一份原檔的 Git blob、size、SHA-256 與 100644 mode 已與 immutable tree 及持久 handoff 核對。相對 G-SA1 四檔改變：README、workflow、review-and-security、Core source-map；其餘七檔與完整 notices／LICENSE 保留原 bytes。The official merged source and eleven raw files match the persistent handoff. Only those four generated files differ from G-SA1.

十一檔來源 aggregate 為 `66f8aa3ef0ca4c02a5143bddf6f3e25b3c68493601c59ebd05950864f0f48986`；現行十份 Markdown collection 為 `37ef5cbdfc9461b43dc76dcd1448943405daf8b6d2a77ee0c1857e7ba9088e15`；LICENSE 仍分驗。Lock、兩個程式常數、manifest、文件及受影響測試同包同步，驗證算法不變。The source aggregate and consumer collection remain separate checks; verifier algorithms are unchanged.

新義務源於已接受的使用者要求，見 Core [前提與方案來源](../../vendor/engineering-workflow-core/docs/provenance/source-map.md#assumptions-options-update)。兩技能只於觸發時導讀 Core，相關前提／反證、採納／未採方案、獨特保障／成本／剩餘風險、改善判斷及停止／重評依據留在既有 plan／report。共用規則由 Core 持有；簡單低風險可簡短處理，改善分類不取代 findings disposition 或必要 gate。The accepted user requirement owns the new common obligation. Consumer entry points reference it proportionately without a second rule set or report framework.

本 consumer 的新 diff 須有自己的獨立審查與必要安全檢查；Core 或 G-SA1 的歷史掃描不作本候選的新掃描證據。離線結果只證明包內容、完整性及引用，未執行新 Grok／模型 runtime case，亦未改既有安裝、全域設定或資格／false readiness。This candidate needs its own review and applicable security evidence. Prior scans do not cover this new consumer diff. Offline verification does not qualify runtime or authorize rollout.

## G-PI1 官方 plugin 分發準備 / Official plugin distribution preparation

[Issue #24](https://github.com/jeffery777/grok-build-dev-skills/issues/24) 依已接受的使用者方案，優先官方 plugin metadata 與既有 assembler／validator，不為 Core 新增 installer。本候選基於 Grok main `2b0eb1629f86c5c6d30f71162652cccfc259f3fd`，產品 `0.1.0-candidate.1` 明確未發布；正式版本／Tag、發布來源與發布 Core pin 由協調者另定。本包完整保留現行 Core 十一檔、lock、Core verifier、兩技能及 notices bytes。This candidate follows the accepted native-plugin-first approach. The product version is unreleased; current fixed Core and skill bytes remain unchanged.

2026-10-17 重新查讀 [官方 Skills／Plugins](https://docs.x.ai/build/features/skills-plugins-marketplaces) 與 [CLI reference](https://docs.x.ai/build/cli/reference)，並查實際非模型 plugin help／version。觀察執行檔為 `1.0.60 (01a8e1c591c0)`，與既有能力目錄 `1.0.52 (0920c8169e27)` 分列；本次不回填舊 catalog 或升級資格。The websites are mutable documentation, and help/version is not a runtime receipt. Generic website flags can differ from the local CLI; no unsupported flag is inferred.

本機已存在的官方隨版 guide 分別讀取並記原 bytes 指紋；未證明由此次觀察的執行檔產生，也未提交其第三方全文。Installed official guides were read and fingerprinted independently; they are not proven to have been generated by the observed executable, and their full text is not redistributed.

| Guide | Bytes | SHA-256 |
| --- | --- | --- |
| `09-plugins.md` | 28001 | `867c8c39394ad4b30b8d38d19eee8f1895a06b37b3581f5f7d63e64f85826b5a` |
| `08-skills.md` | 13886 | `4afcd002489982e069e02dbb0d07fb490216035707fab208b36c434fe6852f1c` |

Guide 支持 root `plugin.json`、`skills/`、resources／helpers 隨包複製、版本顯示、完整 commit 來源及 fetch 後 SHA 核對。實際 install help 支持 Git／GitHub／local source、`@ref` 與 `#subdir`；`--trust` 跳過確認，未執行。原生 `validate` 只代表 manifest schema。Guide 的全域 session-start auto-update 設定不是已證逐 plugin 控制，且本包不改設定。These are documented/help-level facts, not installed-tree, model, entitlement or runtime qualification.

本包只新增最小官方 metadata，並延伸既有 verifier：產品／Core 身分讀回、exact 二十一檔及從可信固定來源另取得的 raw manifest digest 檢查。Manifest／packet 仍是 consumer 自有格式；可信來源 verifier 必須獨立於可疑副本。Source mode 允許開發檔，不驗 installed ownership。原生整樹／跨目錄引用、自訂檔保護、atomic update／rollback 與真正舊版重裝均未證。離線合成 fixture 僅驗拒絕／保留及全新重組；不把退出成功、help 或 schema validation 升格為實裝資格。See [installation preparation](../installation.md) for gaps, failure preservation and the stop before existing-plugin mutations. All readiness remains false; no installer/wrapper, native install/update/uninstall, settings or live Grok run is included.
