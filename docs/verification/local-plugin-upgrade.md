# Local plugin 更新查核 / Local plugin upgrade checks

[Issue #32](https://github.com/jeffery777/grok-build-dev-skills/issues/32)；2026-10-19。

## 繁體中文

**有界單產品路線成功：保全 → 原生卸載 → 零註冊讀回 → 固定新版安裝 → 唯一註冊讀回。** 候選0.2.1沿用0.2.0兩技能、controller、固定Core及locks；本紀錄不證明正式安裝、模型採用、通用更新器或原子rollback。

執行檔為 Grok `1.0.62 (1474f9cbdd91)` stable，binary SHA-256為 `ec434e831afdcfce87780f2815fd732b1df8a4a8de96a491716ad75d13605a4e`。代表性fixture是 `~/projects/test/gupgrade-native-issue32-20261019-4076618a`，使用自己的 `grok-home`、`workspace`、專用leader socket路徑及固定 `local-source/package`。採明確環境allowlist，未繼承憑證或覆寫HOME。只在fixture關閉updater、managed config／MCP、remote fetch、telemetry、envrc及已文件化相容掃描；不宣稱OS全路徑／網路封鎖。

每次原生命令都有獨立設計審查與所需具體信任確認。每個名額各一次，20秒執行限時、131072-byte合併輸出判定額度、stdin關閉／無TTY，只收束自己的process group。逾限、新問題、非零退出、未知路徑／設定、不完整inventory或未收束程序都停止。沒有模型、技能／controller呼叫或索引更新。

| 階段 | 實際結果 |
| --- | --- |
| 固定舊來源原生 install --trust | exit0，原生建立唯一key `package-fb9d95f7`，獨立複製23檔；未人工建立registry |
| 保全舊source／payload後，同一來源換成新30檔，再 install --trust | exit1；`Error: repo 'package-fb9d95f7' already installed`。舊registry／config／installed23未變；原兩名額耗用，沒有重試 |
| 新確認下，另保全新source，再 uninstall grok-build-dev-skills --keep-data | exit0；stdout64bytes、stderr0；`Uninstalled 1 plugin(s): grok-build-dev-skills (data preserved)`。registry為version1／repos={}，舊payload實體目錄完全消失，source新30及recovery舊23＋23／新30完整 |
| 上一步完整讀回後，install 固定來源 --trust | exit0；stdout147bytes、stderr0；唯一實際key仍為 `package-fb9d95f7`，產品0.2.1／Local source正確／獨立複製精確30檔，沒有有效舊版註冊或payload |

後兩次耗時約0.216／0.271秒，程序均收束；不是效能保證。零註冊須完整成功遍歷與有效空registry；讀取／解析錯誤不能當零筆。新key從原生結果學取，不人工計算或預設必須相同。

Fixture config前後SHA-256均為 `f5a7c68b5b06c69fbc6d9b9eb6b85ad322f25ac1d3bd3a103dcb0e9eb7642559`，卸載後原enabled名稱仍保留。未出現獨立trust sidecar，不能推論卸載撤銷所有信任。本fixture沒有獨立持久data目錄或custom內容；`--keep-data`對真實使用者data／custom payload的行為未驗證，也不構成source保留的一般保證。

逐層完整核對來源新30、recovery舊23＋23／新30、14個原證據檔及固定27份guide Markdown／2個目錄；沒有未知新增路徑。新payload為精確30個regular files、0644、uid501、nlink1，與source inode獨立；目錄0755。保全均在discovery roots外，native bookkeeping與append-only log在payload外；沒有刪檔或放寬verifier強求PASS。正式registry／config及本產品舊source／payload bytes、modes、ownership每階段均不變，未讀其他plugin payload。

| 固定證據 | SHA-256 |
| --- | --- |
| 舊0.1.0 manifest，23檔 | `047ffdb0693f3ae1e322e46c1e80ec131334a351f1367896c3c7508fe09858b2` |
| 新0.2.1 manifest，30檔 | `b44a42dc01d221cdf88d2b27d7ca864d080816c59f593c117fd408862ce46864` |
| 卸載後空registry | `c2efcb3240fcb880f50265bf8a19046b6acadb40e27f0cd3cd48a305707a182e` |
| 最終唯一新版registry | `aa673033c9b67f5873ba03c0619f23ce2be0e1aa8758a948a7f1edf690bedb8c` |
| 實際driver | `b535997860452f262955d519dd6a34ebfbd8c02cf5977ffc4df47ed62dad79f2` |
| 已審plan | `3092e678010568c9fed7963abc3557fed77ed2970d6bdee4d8ab3d6aa5f3d324` |
| 211項原始基線，含原證據 | `f595d2df849703bb22615b73788d149738dc4b3299f1b08d568b52ce3937e5f2` |

原始本機證據保留於fixture的 `evidence/transition.{uninstall,install}.{attempt,result,accepted}.json` 與各自stdout／stderr，另有preparation、bookkeeping before、精確批准與獨立審查綁定。Driver只是操作證據，不隨產品交付，也不是新updater。

較早人工key fixture的named update曾exit0卻維持regular-file舊payload；無信任install曾exit1並寫log。人工舊key加不同新source的安裝形成兩筆，顯示該fixture身份不代表原生同來源案例。原始失敗、問題與logs均保留，不推論vendor bug或當成本次成功證據。上表後續案例改由原生建立registry，再分別明確授權有界替代路線。

Coverage限macOS／Grok 1.0.62／單產品／無custom的copied Local layout。正式舊版由1.0.60安裝，雖layout已核對，操作時仍須重新讀回。多產品、外部／未知data、native atomic update／downgrade／rollback、session cache與模型載入未驗證。若卸載成功但安裝失敗，停止保留零有效外掛現場，不自動回復或重播；保全bytes不等於原生bookkeeping可原子恢復。所有離線readiness仍false，正式新增信任仍另需確認。

## English

**The bounded single-product route succeeded:** preserve; native uninstall; verify zero registrations; install fixed source; verify exactly one registration. Product 0.2.1 retains the 0.2.0 skills, controller, fixed Core and locks. This does not qualify production installation, model adoption, a generic updater or atomic rollback.

The native-created fixture above used Grok 1.0.62, a separate home/cwd/leader socket and a fixed Local source. Its explicit environment inherited no credentials and did not override HOME. Updaters, managed configuration/MCP, remote fetch, telemetry, envrc and documented compatibility discovery were suppressed only in the fixture. This is not OS-wide filesystem/network confinement. Every native call had independent design review and applicable specific trust, one exclusive attempt, a 20-second execution budget, 131072-byte combined-output acceptance limit and closed stdin/no TTY. No model, skill/controller or index operation ran.

Native installation created the sole old key and independent 23-file payload. Direct reinstallation after switching the same source to new 30 failed with the already-installed error above; both original slots were consumed. A new confirmation authorized the later two operations. Uninstall--keep-data succeeded, leaving a valid empty registry and no old payload; new source and old23+23/new 30 recovery copies were intact. Only after that complete readback did fixed-version installation run once, producing exactly one 0.2.1 registration and independent exact 30-file payload. The observed key stayed equal; this was learned, not required or manually seeded. The table binds exact identities and results.

Config remained byte-identical, including the enabled name. No new trust sidecar appeared; this does not prove all trust was revoked. No separate persistent-data directory or custom content existed, so real user-data/custom-payload preservation remains untested. Source, three recovery trees, original 14 evidence files and pinned 27 guide files/2directories were preserved. New installed files were regular 0644, uid501, single hardlinks, separate source/installed inodes and 0755 directories. Bookkeeping and append-only log were outside the payload. No extras were deleted to force verification. Monitored production registry/config and this product's old source/payload remained unchanged; other plugin payloads were not read.

Raw attempt/result/acceptance, stdout/stderr, preparation/bookkeeping, exact approval and review bindings remain in the fixture evidence paths above. Earlier artificial-key/update/no-trust observations remain limited or unrepresentative evidence, not vendor-bug claims. This route adds no shipped wrapper or updater.

Coverage is only macOS/Grok 1.0.62, one product, no custom data, copied Local layout. Production was originally installed by 1.0.60 and needs current checks. Multi-product behavior, unknown/external data, atomic update/downgrade/recovery, session caches and model loading remain unqualified. After successful uninstall, a failed installation can leave zero active plugins: preserve state and stop without automatic retry/rollback. Preserved bytes do not guarantee atomic native-bookkeeping recovery. Offline readiness stays false; production trust requires separate confirmation.
