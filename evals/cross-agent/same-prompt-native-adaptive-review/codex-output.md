# Native Adaptive 静态评审

**结论：iOS 与 Android 均应阻断发布。** 当前实现不是“共享产品语义、适配平台行为”，而是把一套固定手机画布和近似原生控件同时移植到两端；它直接冲突于已声明的无障碍、原生信任和大屏工作流要求。

## 1. 证据等级、平台与设计解读

- **评审模式 / 实际 Skill：** `design-craft` / `critique`，只读；未修改文件。
- **证据等级：** **L0 static**。只有描述性静态证据；即使产品上下文充分，没有截图仍不能提升为要求“截图 + 上下文”的 L1。
- **PRODUCT authority：** 仅使用题述的 `PRODUCT.md` 摘要，未读取实际文件。
- **DESIGN authority：** 仅使用题述摘要；当前基线明确允许并要求平台原生导航、控件、图标、材质和动效，而不是像素级同构。
- **Resolved platform：** `adaptive`。对**产品目标**置信度高；React Native 工程结构和双端 target 未经源码核验。
- **Design read：** Reading this as: **面向单手现场操作员与平板复核经理的原生任务应用，气质可信、克制、运营化，优先保障快速完成、明确验证和中断后无损恢复。**

## 2. 分平台合规结论

| 平台 | 静态合规判定 | 决定性原因 |
|---|---|---|
| **iOS / iPadOS** | **Block — 不符合当前发布要求** | 原生导航栈和返回手势被替换；固定字号且禁止缩放；`40x40` 小于 `44x44pt` 控件边界；无 iPad/Split View 结构适配；仿原生开关和 Web 图标不能替代系统语义；未响应 Reduce Motion。 |
| **Android** | **Block — 不符合当前发布要求** | `BackHandler` 明确吞掉系统 Back，破坏 predictive Back；`40x40` 小于 `48x48dp` 控件边界；字体缩放被禁用；Cupertino 控件和 Web 图标违反 Material 语法；平板仍保留固定手机布局和底栏；未响应 Remove animations。 |

这些是**基于题述实现的静态发布阻断结论**，不是 Simulator、Emulator 或真机运行结论。

## 3. 最多五项阻断发现

### B1 — P0：无障碍基础与主操作几何不成立

- 固定 `fontSize: 14` 且关闭 font scaling，直接违反 Dynamic Type / Android font scaling 的明确发布要求。
- `40x40` Pressable 边界低于 iOS `44x44pt` 和 Android `48x48dp`；如另有 `hitSlop`，有效触控区可能更大，但当前证据没有证明。
- **影响：** 低视力用户可能无法阅读或操作；戴手套、移动中单手操作的误触风险也更高。
- VoiceOver、TalkBack、键盘遍历本身没有静态证据，必须保持 **unverified**，不能推断已支持。

### B2 — P0 Android / P1 iOS：导航和系统 Back 合同被破坏

- iOS 的自定义顶栏和 JavaScript Back 替代导航栈，无法静态证明系统返回语义、交互式左缘返回和焦点恢复。
- Android 的空 `BackHandler` 明确消费 Back，阻断系统返回和 predictive Back。
- **影响：** 用户无法依靠平台肌肉记忆离开或恢复，且可能被困在任务页；这与“可信、不中断丢进度”正面冲突。

### B3 — P1：布局只缩放手机画布，没有真正 adapt

- 固定 `width: 390` 并在平板居中，是窄手机画布封装，不是基于可用窗口的自适应结构。
- 底部 Tab 在 phone、iPad、Android tablet 完全不变，没有回应 iPad Split View、Android multi-window、横屏或 fold posture。
- **影响：** 经理无法利用平板并排查看任务、证据和验证状态；更窄的分屏或放大字体还可能造成裁切和不可达操作。

### B4 — P1：平台控件和主题映射被像素同构取代

- 同一 Cupertino-shaped switch 与 Web icon set 不能同时满足 iOS 系统控件语义和 Android Material 3 语义；“长得像”不等于保留系统状态、辅助技术和交互保证。
- `#777777`、`#FFFFFF` 在两种 appearance 中直接复用，绕过 `DESIGN.md` 的语义颜色角色和平台映射。
- **影响：** Android 明显呈现移植感，iOS 也只是仿原生；实际对比度、disabled/pressed/focus/high-contrast 状态因缺少渲染上下文而仍未验证。

### B5 — P0：完成动效违反减少动态效果要求

- `500ms`、带 overshoot 的 spring 对高频运营任务过长且过于活跃，不符合“calm”定位。
- 没有 iOS Reduce Motion 或 Android Remove animations 分支，是明确的发布要求缺失。
- **影响：** 前庭敏感用户无法关闭明显位移；如果持久化、返回或辅助技术 announcement 还依赖动画结束，则会进一步放大中断风险——该依赖关系目前未验证。

## 4. 八项具体设计改动

1. **恢复平台导航合同：** iOS 使用真实 navigation stack、系统 back item 与 interactive pop；Android 接入系统/predictive Back。删除空消费 handler，仅在确有未提交状态、打开的 sheet 等场景拦截，并在未处理时委托系统。
2. **建立 window-class 自适应骨架：** compact 使用单栏任务流；expanded 使用任务列表/任务内容/验证信息的两栏或主从结构。依据可用宽度、方向、输入方式和 fold posture，而非设备型号。
3. **扩大有效目标：** iOS 至少 `44x44pt`；Android 至少 `48x48dp`，通常保留约 `8dp` 控件间距。若视觉图标更小，必须用可测试的 hit region 扩大，并避免相邻区域重叠。
4. **恢复可缩放字体：** iOS 映射 Dynamic Type text styles；Android 映射 Material type roles 与 `sp`/系统 font scale。允许多行、内容增长和操作区重排，不用裁切或任意倍率上限掩盖布局问题。
5. **设置平台组件适配层：** iOS 使用原生 switch、SF Symbols、tab/sidebar/split-view 语法；Android 使用 Material 3 switch、Material Symbols、navigation bar/rail/drawer 和相应反馈组件。
6. **把颜色变为共享语义、平台解析：** 共享 `surface`、`text.primary`、`text.muted`、`action.primary`、`success` 等角色；iOS 映射系统动态颜色/材质，Android 映射 Material `colorScheme`，分别验证 light、dark、increased contrast/high contrast 和所有控件状态。
7. **重做完成反馈：** 数据状态立即提交并可恢复，视觉反馈采用克制、平台一致、通常不超过 `300ms` 的过渡且不 overshoot；iOS Reduce Motion 使用短 cross-fade，Android Remove animations 使用 cross-fade 或立即切换。
8. **把中断恢复与辅助技术作为状态机合同：** 每个有意义的编辑点持久化草稿；恢复时显示任务、同步和冲突状态；为控件提供 name/role/value/state，完成时进行 VoiceOver/TalkBack announcement，并维护键盘、D-pad 和屏幕阅读器的逻辑焦点。

## 5. Intentional parity matrix

| 能力 | 保持共享 | iOS / iPadOS 必须适配 | Android 必须适配 |
|---|---|---|---|
| 任务模型与恢复 | Task ID、步骤、校验、草稿、完成、冲突和离线语义 | 平台生命周期与安全存储接入 | 进程重建、生命周期与安全存储接入 |
| 内容与操作语义 | 内容优先级、主要动作结果、错误恢复、analytics semantics | 按 iOS 文案和菜单习惯呈现 | 按 Material 文案和反馈习惯呈现 |
| 导航 | 同一目的地与层级关系 | Navigation stack；compact tab；expanded sidebar/split structure；系统返回手势 | 系统/predictive Back；compact navigation bar；medium/expanded rail、drawer 或 list-detail |
| 控件与图标 | 控件业务含义、enabled/disabled/loading/error 状态 | 原生控件、SF Symbols、iOS sheets/alerts/context actions | Material 3 控件、Material Symbols、bottom sheets/dialogs/snackbars |
| 颜色与字体 | 语义 token 名、层级和品牌意图 | Dynamic Type、system colors/materials、iOS contrast settings | Material typography、`sp`、Material color scheme/Dynamic Color |
| 动效与反馈 | 因果关系、完成时机、无障碍结果 | Reduce Motion、iOS transition/haptic conventions | Remove animations、Material motion、Android feedback conventions |
| 无障碍 | 相同可理解结果、完整标签和可达任务流 | VoiceOver traits/actions、iOS keyboard focus | TalkBack state descriptions/actions、Tab/D-pad traversal |

**Parity 目标是任务结果和语义一致，不是像素、控件形状或导航位置一致。**

## 6. 已确认与未验证

### 已确认——仅限题述静态事实，未独立读取源码

- 产品意图被声明为 `adaptive`，且视觉 authority 允许平台原生差异。
- 题述实现包含固定 `390` 宽度、自定义返回、Android Back 消费、`40x40` Pressable、禁用字体缩放、literal colors、共享 Cupertino/Web 控件、固定 Tab 和无 reduced-motion 分支。
- 在这些事实成立的前提下，字体缩放、Android Back、减少动态效果和结构适配的合同冲突可以静态判定。
- `40x40` 组件边界低于两端平台基线；有效 hit area 是否被额外扩大尚未证明。

### 未验证

- 未读取源树，因此未排除 `hitSlop`、平台分支、原生 module、持久化层或其他补偿路径。
- 未验证 safe-area/insets、IME、旋转、Split View、multi-window、foldable、极窄窗口或大字体下的真实布局。
- 未验证实际颜色配对、对比度、pressed/disabled/error/high-contrast 状态。
- 未验证 VoiceOver/TalkBack tree、标签、角色、值、announcement、焦点顺序、键盘/D-pad 遍历。
- 未验证任务 autosave、离线、进程终止、冲突恢复或完成操作是否依赖动画结束。
- 未验证手势、haptics、帧率、触控感、OEM 差异或真机性能。

## 7. 最小 source / build / runtime 验证计划

1. **Source audit：** 在真实仓库运行平台扫描，并定向搜索 `width: 390`、`allowFontScaling`、`BackHandler`、`hitSlop`、`#777777`、`#FFFFFF`、spring/duration、`AccessibilityInfo`、window dimensions、navigation registration 和持久化调用。
2. **Contract tests：** 增加/检查导航返回、draft restore、process interruption、reduced-motion 分支、font-scale reflow、平台组件选择和 window-class 布局测试；随后运行仓库现有 typecheck、lint 和 unit/integration scripts。
3. **iOS build：** 使用仓库真实 workspace/project 与 scheme 执行 `xcodebuild ... -sdk iphonesimulator build` 和相关 tests；当前 **未执行，构建状态未知**。
4. **Android build：** 执行仓库真实 Gradle tasks，最低覆盖 `./gradlew test lint assembleDebug`；当前 **未执行，构建状态未知**。
5. **iOS Simulator：** iPhone compact 与 iPad expanded/Split View；light/dark、最大 Dynamic Type、Reduce Motion、VoiceOver、外接键盘、交互式返回、中断/恢复。**iOS Simulator: unverified locally**。
6. **Android Emulator：** phone、tablet、foldable/可调整窗口；gesture navigation/predictive Back、font scale、dark theme、Remove animations、TalkBack、Tab/D-pad、multi-window、进程终止/恢复。**Android Emulator: unverified locally**。
7. **真实设备：** 至少一台 iPhone、一台 iPad，以及一台手势导航 Android 和一台代表性 OEM/折叠设备；验证单手命中、系统手势、haptics、键盘、分屏、离线中断和持续性能。**iOS/iPadOS real-device evidence: none；Android real-device evidence: none**。
8. 只有上述双端 runtime matrix 通过后，才能把当前结论从“静态阻断及风险”升级为“adaptive release validated”；现阶段不得声称 Simulator、Emulator 或真机验证。