# Codex observed output

- Agent: Codex CLI
- Version: `codex-cli 0.144.1`
- Date: 2026-07-10
- Command summary: `codex exec -C <repo> -s read-only --ephemeral -o /tmp/design-craft-native-codex.md with the source skill path`
- Skill path observed: `/Users/gaoqian/Documents/sixseven/codeproject/design-craft/skills/design-craft`
- Evidence boundary: read-only prompt/source review; runtime behavior remains unverified.
- Benchmark contract: output includes concrete design move recommendations.

## Output

## 1. Evidence、平台判定与 design read

- **Evidence level：`L0 static`**。现有材料只有产品上下文和静态实现描述；没有源码树、构建结果、截图、可访问性树或任何原生运行时证据。虽然上下文完整，但没有截图或运行态，因此不能提升为 `L1 contextual`。
- **Resolved platform：`adaptive`**
  - `platform_source=product_context`
  - 来源：题面引用的 `PRODUCT.md`
  - `platform_confidence=1.0`（仅针对本 benchmark 的平台分类；真实仓库内容仍未核对）
- **Design read：** Reading this as: 面向单手现场操作员和分屏审阅经理的跨平台任务应用，气质应可信、克制、具有平台原生感，核心优化目标是在频繁中断下快速完成、验证并可靠恢复任务进度。
- **总判定：Release Block。** 当前概念是“共享像素和控件外观”，而不是“共享产品意图、按平台适配行为”。这与 `PRODUCT.md` 的 `adaptive` 定义以及 `DESIGN.md` 明确允许平台原生差异的规则相冲突。

## 2. iOS 与 Android 平台符合性

| 平台 | 判定 | 关键依据 |
|---|---|---|
| **iOS / iPadOS** | **不符合，阻断发布** | 自定义顶栏和 JavaScript Back 取代原生导航栈，无法证明保留左侧边缘返回手势、原生转场与恢复语义；`40x40` 小于 iOS `44x44pt` 最小触控目标；固定 `fontSize: 14` 且禁用缩放直接违反 Dynamic Type 要求；固定 `390` 宽度和不变的底部 Tab 无法支持 iPad、Split View 和外接键盘场景；原始颜色值不能保证 light/dark/high-contrast；500ms overshoot spring 没有 Reduce Motion 分支。 |
| **Android** | **不符合，严重阻断发布** | 空 `BackHandler` 吞掉系统 Back，直接破坏系统导航和 predictive Back；JavaScript Back 不能替代 Android Back contract；`40x40` 小于 Android `48x48dp` 最小触控目标；禁用字体缩放违反 TalkBack/font scaling 发布要求；Cupertino switch 和 web icon set 不符合 Material 平台语义；固定手机画布、平板仍使用不变底部导航，不符合 window size class、多窗口和 fold posture 适配；没有 Remove animations 分支。 |

静态描述已经足以判定上述明确冲突；但手势体验、焦点顺序、屏幕阅读器输出、实际布局溢出和性能仍是 **unverified**，不能从本次材料推断为已经运行失败或运行通过。

## 3. 优先级发现

### P0 — 原生导航与进度恢复

**Evidence**

- iOS 原生导航栈被自定义顶栏和 JavaScript Back 替代。
- Android 系统 Back/predictive Back 被替代，且空 `BackHandler` 主动消费 Back。
- 产品核心任务要求“中断后不丢失进度”，但没有任何草稿持久化、生命周期恢复或离线恢复证据。

**用户影响**

- iOS 用户可能失去熟悉的边缘返回手势和空间连续性。
- Android 用户可能被困在页面内，predictive Back 预览和系统退出顺序失效。
- 用户在返回、切换应用、窗口调整或进程被回收时可能无法预测任务状态是否保留。

**design move**

- 共享“返回意图、路由语义和未完成任务状态机”，不要共享 Back 按钮实现。
- iOS 使用 native-stack-backed navigation，保留系统返回按钮、边缘返回手势、交互式取消和原生焦点行为。
- Android 接入系统 Back dispatcher 和 predictive Back；移除无条件消费事件的空 `BackHandler`。只有存在真正需要拦截的未保存破坏性状态时才参与 Back，并提供可预测的保存或确认路径。
- 将任务输入持续写入可恢复 draft；完成动作应幂等，避免中断重试产生重复提交。

**验收条件**

- iOS 点击 Back、边缘滑动返回和取消返回均落到相同、正确的任务状态。
- Android 按键 Back、手势 Back 和 predictive Back 预览遵循同一路由层级，没有被空 handler 吞掉。
- 后台切换、进程终止、重新启动、旋转和多窗口尺寸变化后，未完成任务恢复到最后可靠状态。

---

### P0 — 字体缩放、触控目标和辅助技术

**Evidence**

- 所有主要操作都是 `40x40` pressable。
- 文本固定为 `fontSize: 14`，并禁用 font scaling。
- VoiceOver、TalkBack、外接键盘遍历是明确发布要求，但没有语义树或运行时证据。

**用户影响**

- `40x40` 低于 iOS `44x44pt` 和 Android `48x48dp` 的平台最低目标，对单手现场操作尤其容易误触或漏触。
- 禁用字体缩放使低视力用户无法完成核心流程。
- 固定字号在开启大字体后不能自然重排；标签、状态和主要动作可能截断或不可达。
- 即使视觉标签存在，也不能证明屏幕阅读器获得正确的 role、label、value、state 或 action。

**design move**

- iOS 使用 Dynamic Type 文本角色；Android 使用 Material type roles 和 `sp`/系统 font scale；React Native 文本允许字体缩放，避免未经验证的低上限。
- 布局必须允许多行、纵向增长和动作换行，不通过缩小字体或隐藏内容维持单行。
- iOS 交互区域至少 `44x44pt`；Android 至少 `48x48dp`，并保证相邻目标不重叠。视觉图标可以小于目标，但扩展后的命中区必须真实、独立且不与其他控件竞争。
- 为每个主要控件提供正确的 VoiceOver/TalkBack role、label、state/value 和必要的 announcement。
- 为平板和外接键盘提供稳定的焦点顺序、可见焦点状态与键盘激活路径。

**验收条件**

- iOS 最大 Accessibility Dynamic Type、Android 至少 200% font scale 下，核心内容不裁切、主要动作不丢失、页面仍可滚动和完成。
- 触控目标测量达到各平台最低要求。
- VoiceOver/TalkBack 能完整说明任务、进度、开关状态、错误和完成结果。
- 外接键盘可遍历、激活并退出所有核心交互，不产生焦点陷阱。

---

### P0 — Reduce Motion / Remove animations

**Evidence**

- 完成转场为固定 500ms overshoot spring。
- 没有 iOS Reduce Motion 或 Android Remove animations 替代方案。

**用户影响**

- 这是明确的发布级可访问性失败。
- Overshoot 与可信、克制的现场作业定位不一致。
- 任务完成是高频、功能性状态变化，不应让用户等待明显弹跳来确认结果。

**design move**

- 共享“完成已发生”的因果反馈，不共享相同动画曲线。
- 默认取消无因果依据的 overshoot，使用更短、不可阻塞的完成反馈。
- iOS 使用平台一致的短淡入淡出、状态替换和克制 haptic；开启 Reduce Motion 后移除大位移和弹性，使用短 cross-fade 或立即状态切换。
- Android 使用 Material-consistent fade-through、shared-axis 或直接状态更新；开启 Remove animations 后使用立即切换或最短非空间淡变。
- 动画不能延迟状态提交、禁用导航或阻止下一任务开始。

**验收条件**

- 两个平台的系统减弱/移除动画设置均能实际改变该转场。
- 减弱模式下没有 overshoot、大位移、弹性回弹或等待 500ms 才可继续操作。
- 完成状态、屏幕阅读器 announcement 和触觉反馈发生在真实状态提交时，而不是动画结束回调时。

---

### P0 — 手机、平板、分屏和多窗口适配

**Evidence**

- React Native 页面被强制为 `width: 390`，在平板上仅居中。
- Bottom tab bar 在手机、iPad 和 Android tablet 上完全不变。

**用户影响**

- 平板经理只能看到居中的手机画布，无法利用横向空间进行列表与详情并行审阅。
- iPad Split View 和 Android multi-window 的窄宽度与全屏平板宽度可能得到同一结构，而不是根据可用空间变化。
- 固定宽度增加大字体、长语言、横屏、IME 和 foldable 场景下的裁切风险。
- 管理员的审阅任务与操作员的单手执行任务被迫使用同一信息结构。

**design move**

- 删除固定 `390` 布局约束，以 available width、size/window class、posture 和 input mode 驱动结构。
- Compact：保持单列任务流程；若有 3–5 个真正顶层目的地，可保留平台原生底部导航。
- Expanded：采用列表—详情双栏，让经理在一侧选择任务、另一侧查看证据和审核状态。
- iPad：根据 size class 使用 sidebar/split-view 式导航；Split View 缩窄后自动回落为单列。
- Android medium/expanded：根据 window size class 使用 navigation rail 或 drawer，并支持 list-detail pane；折叠设备考虑 hinge/posture。
- 不按“iPad”“Android tablet”等设备名称硬编码；同一设备在分屏后可能重新进入 compact 模式。

**验收条件**

- Compact phone、iPad 全屏与 Split View、Android tablet multi-window、横竖屏和至少一个 foldable posture 均保持核心任务可达。
- 扩展宽度用于提升审阅效率，而不是只增加空白。
- 窗口实时缩放不会丢失输入、重置任务或让当前选择消失。

---

### P1 — 控件、图标和平台熟悉度

**Evidence**

- 两个平台使用同一个 Cupertino-shaped switch。
- 两个平台使用同一套 web icon。
- `DESIGN.md` 明确允许原生控件、图标、材料和行为不同。

**用户影响**

- Android 用户会识别出 iOS/web port，降低平台信任。
- 外观相似的自定义控件未必保留平台原生语义、状态反馈、触控目标、键盘行为和辅助技术支持。
- Web 图标可能与 SF Symbols 或 Material Symbols 的平台含义、基线和笔画重量不匹配。

**design move**

- 共享控件的业务 API，例如 `checked`、`disabled`、`label`、`onChange` 和 analytics event；按平台渲染真实原生控件。
- iOS 使用原生 Switch 和 SF Symbols 或项目批准的 iOS-native icon mapping。
- Android 使用 Material 3 Switch 和 Material Symbols。
- 对跨平台品牌图标只共享语义名称，不强制共享 glyph；品牌专属资产可以共享，但系统行为图标应适配。

**验收条件**

- 每个平台上的 control role、state announcement、pressed/disabled/focus 行为符合本平台。
- Android 不再显示 Cupertino look-alike；iOS 不再依赖 web navigation glyph。
- 平台差异由明确 mapping 管理，而不是散落在页面条件判断中。

---

### P1 — 语义主题与高对比度

**Evidence**

- 两种 appearance 都直接使用 `#777777` 和 `#FFFFFF`。
- `DESIGN.md` 已经定义共享 semantic color roles。

**用户影响**

- 字面颜色绕过既有设计系统，无法可靠适配 light、dark、increased contrast 或 Android tonal elevation。
- `#777777` 的实际对比度取决于背景、文本大小和状态；当前材料不足以证明合格。
- `#FFFFFF` 在不同 surface 上可能造成内容消失、眩光或不符合平台材料层级。

**design move**

- 页面和共享组件只消费语义角色，例如 `text.primary`、`text.secondary`、`surface.base`、`surface.elevated`、`border.subtle`、`state.success`。
- iOS 将这些角色映射到 system colors/materials 和 increased-contrast variants。
- Android 将同一语义映射到 Material color scheme、surface container 和 tonal elevation。
- 共享 token 名称，但允许两平台的实际值不同；适配不等于逐像素相等。

**验收条件**

- 组件中不再存在无说明的主题字面颜色。
- light、dark 和高对比设置下分别测量文本、图标、边界和状态反馈。
- 不能只通过简单反色生成 dark theme。

## 4. 具体设计方向与 intentional parity matrix

首要整体 **design move**：把“固定 390px 手机页面”重构为一个共享任务状态机之上的 adaptive shell。共享任务内容、状态和设计语义；平台导航、控件、图标、材料、动效和窗口结构分别原生化。

| 领域 | 保持共享 | iOS / iPadOS 必须适配 | Android 必须适配 |
|---|---|---|---|
| 产品流程 | 任务步骤、验证规则、完成条件、错误语义、analytics semantics | 使用 iOS 原生导航层级呈现 | 使用 Android Navigation 与 Back contract 呈现 |
| 进度恢复 | Draft schema、autosave 规则、幂等提交、同步状态 | 对接 iOS app lifecycle、scene restoration | 对接 Android lifecycle、process recreation、saved state |
| Compact 布局 | 内容优先级和核心动作顺序 | iPhone 单列、安全区域、必要时原生 tab bar | Phone 单列、edge-to-edge insets、必要时 Material navigation bar |
| Expanded 布局 | 列表—详情关系和审阅信息层级 | iPad size classes、sidebar/split view、Split View 回落 | Window size classes、navigation rail/drawer、list-detail、fold posture |
| Back 行为 | “返回上一层”和“退出未完成任务”的业务语义 | Native stack、系统 Back 按钮、边缘返回手势 | System Back、predictive Back、禁止空 handler 吞事件 |
| 控件 | `value`、`disabled`、验证规则、事件名 | Native Switch、iOS picker/sheet/alert | Material 3 Switch、picker/bottom sheet/dialog |
| 图标 | 语义名称和品牌专属资产 | SF Symbols 或 iOS mapping | Material Symbols 或 Android mapping |
| 颜色 | Semantic roles、状态含义、品牌意图 | System colors/materials、高对比映射 | Material color scheme、tonal elevation、Dynamic Color 策略 |
| 字体 | 内容层级、文案、语义 text roles | Dynamic Type 和 iOS text styles | Material type roles、`sp` 和系统 font scale |
| 触控与焦点 | 核心操作优先级、可访问名称 | 至少 `44x44pt`、VoiceOver、键盘/Switch Control | 至少 `48x48dp`、TalkBack、键盘/D-pad |
| Motion | 因果关系、完成状态、是否允许阻塞 | iOS 原生转场、Reduce Motion、克制 haptic | Material motion、Remove animations、Android feedback |
| 视觉 parity | 内容身份、状态含义和质量标准 | 不要求与 Android 像素相同 | 不要求与 iOS 像素相同 |

## 5. Verified 与 unverified

### 可从题面静态 Evidence 确认

以下仅表示“由 benchmark 明确给定”，不是通过源码或运行时独立验证：

- 产品平台声明为 `adaptive`。
- `DESIGN.md` 允许平台原生导航、控件、图标、材料和 motion。
- 至少一个 React Native 页面固定为 `width: 390`。
- 自定义顶栏和 JavaScript Back 替代了原生导航路径。
- Android 空 `BackHandler` 消费 Back。
- 主要 pressable 的描述尺寸为 `40x40`。
- 文本使用固定 `fontSize: 14` 且关闭字体缩放。
- 两种 appearance 使用原始 `#777777` 和 `#FFFFFF`。
- 两个平台共享 Cupertino-shaped switch、web icon set 和不变的 bottom tab。
- 完成转场是无 accessibility alternative 的 500ms overshoot spring。
- 如果 `40x40` 就是实际命中区域，则它小于 iOS `44pt` 和 Android `48dp` 最低目标。
- 禁用字体缩放和缺少 reduced-motion 分支与明确发布要求直接冲突。
- 空 `BackHandler` 与 Android system/predictive Back contract 直接冲突。

### 明确 unverified

- 题面描述是否与当前真实源码一致。
- `40x40` 是否另有不重叠的 `hitSlop` 扩展；没有源码不能断言。
- iOS 边缘返回手势当前是否完全失效，以及交互取消是否可用。
- predictive Back 的实际动画、返回目标和系统版本行为。
- VoiceOver/TalkBack 的 label、role、value、state、focus/traversal 和 announcement。
- 外接键盘、D-pad、Switch Control 的焦点路径。
- Dynamic Type/font scaling 下的裁切、重排、滚动和按钮可达性。
- `#777777` 与实际背景组合的精确对比度。
- safe area、status/navigation bar、IME、cutout、hinge 和 home indicator insets。
- 横竖屏、iPad Split View、Android multi-window 和 foldable posture 的实际行为。
- 任务草稿是否持久化，进程被回收后是否恢复，完成提交是否幂等。
- light/dark/high-contrast 的实际视觉结果。
- 动画是否阻塞输入、是否掉帧、是否可中断。
- 项目是否可以通过 TypeScript、iOS 或 Android 构建。
- 所有截图、可访问性树、Simulator、Emulator 和真实设备结果。

## 6. 最小源码、构建和运行时验证计划

### A. 源码静态核对

1. 读取真实 `PRODUCT.md`、`DESIGN.md`、`package.json`、导航入口、主题入口和任务状态管理代码。
2. 使用 `rg` 定位：
   - `width: 390`
   - `BackHandler`
   - JavaScript Back handlers
   - `allowFontScaling={false}` 或等效设置
   - 固定 `fontSize: 14`
   - `#777777`、`#FFFFFF`
   - Cupertino switch 与 web icon imports
   - bottom-tab breakpoint/window logic
   - 500ms spring、overshoot 和 accessibility motion setting
3. 核对 pressable 是否有真实 `hitSlop`，并确认扩展目标不会与相邻控件重叠。
4. 核对 accessibility props、语义 grouping、live announcements、keyboard focus、draft persistence 和提交幂等逻辑。
5. 确认布局由 available width/window class 驱动，而不是设备名称或固定 canvas 驱动。

### B. 构建与静态测试

1. 先读取项目既有 scripts，再运行最小相关的 TypeScript/type-check、lint 和 unit tests；不得在未查看项目约定前假定命令。
2. iOS：
   - 用真实 workspace/project 和 scheme 执行 `xcodebuild` compile/test。
   - 增加导航恢复、Dynamic Type 布局和 motion-setting 分支测试。
3. Android：
   - 用真实 Gradle module 执行 lint、unit test 和 debug assemble。
   - 增加 Back dispatcher/predictive Back、font scale、window size class 和 saved-state 测试。
4. 构建成功只证明编译和静态契约，不证明原生交互符合性。

### C. iOS Simulator

**`iOS Simulator: unverified locally`**

最低运行矩阵：

- 一台 compact iPhone。
- 一台 iPad，全屏和至少一种 Split View 宽度。
- portrait/landscape。
- light/dark/increased contrast。
- 默认字号和 Accessibility Dynamic Type 最大档。
- VoiceOver。
- Reduce Motion。
- 外接键盘遍历。
- 点击 Back、边缘滑动、交互取消、后台恢复和进程重启。
- 完成任务后立即继续操作，确认 motion 不阻塞输入。

### D. Android Emulator

**`Android Emulator: unverified locally`**

最低运行矩阵：

- compact phone。
- expanded tablet。
- 至少一个 multi-window 状态；产品支持 foldable 时增加 foldable posture。
- 三键导航和 gesture navigation。
- predictive Back 预览、取消和完成。
- light/dark/high contrast 或系统支持的对比设置。
- 默认 font scale 和至少 200% font scale。
- TalkBack。
- Remove animations。
- hardware keyboard/D-pad。
- IME、system bars、cutout/hinge insets。
- 后台恢复、进程回收重建、离线和重试提交。

### E. 真实设备

**Real-device evidence：两平台均缺失且 unverified。**

发布前最低需要：

- iPhone 与 iPad：验证边缘返回、触觉反馈、VoiceOver、Dynamic Type、Split View、实际性能和生命周期恢复。
- Android phone 与 tablet；最好覆盖至少一个非参考 OEM：验证 gesture navigation、predictive Back、TalkBack、OEM font scaling、系统 insets、触觉反馈和多窗口。
- 如果 foldable 属于支持范围，至少一台真实 foldable 验证 hinge/posture。
- 真实硬件证据是最终判断手势、haptic、OEM 差异和持续性能的必要条件，Simulator/Emulator 不能替代。

在至少获得一套 iOS runtime、一套 Android runtime，并分别覆盖 compact 与 expanded/multi-window 状态之前，该 adaptive 评审只能保持为“静态证据下明确不符合，修复后的运行结果仍 unverified”，不能标记为完成或发布就绪。
