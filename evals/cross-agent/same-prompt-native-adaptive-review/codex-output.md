## 1. 证据等级、平台解析与设计判断

- **使用方式**：`design-craft`，`mode=critique`；只读评审，未运行 route planner、源码扫描器或其他项目自动化。
- **证据等级**：**L0 static / prose-only**。虽然产品、用户和任务上下文充分，但没有截图、源码、DOM/无障碍树或运行态，因此不能升级为 L1-L4。
- **解析平台**：`adaptive`；来源是提示中明确给出的 `PRODUCT.md` 平台声明及 iOS/Android 双商店目标。对**目标平台**置信度高，但没有实际读取 `PRODUCT.md` 文件。
- **样式权威**：提示所述 `DESIGN.md` 允许平台原生导航、控件、图标、材料和动效，因此“业务语义一致、平台表现不同”符合项目权威；文件本身未核对。
- **Design read**：将其理解为面向单手现场操作员和分屏平板管理者的原生自适应任务完成/复核界面，气质应冷静、可信、操作化，优先保证快速完成、清晰验证与中断后无损恢复。
- **一句话诊断**：产品合同是 adaptive，但描述实现是固定宽度、Web/Cupertino 化的手机画布，并绕过两端系统导航和无障碍设置；当前屏幕不能作为 iOS 或 Android 发布合规版本通过。

## 2. 分平台合规结论

| 平台 | 静态结论 | 决定性冲突 |
|---|---|---|
| **iOS / iPadOS** | **BLOCK：该屏幕不合规** | 没有原生导航栈和边缘返回；标称 `40x40` 小于 `44x44pt`；Dynamic Type 被关闭；固定手机画布没有 iPad/分屏结构适配；完成动效不响应 Reduce Motion；控件和图标的 iOS 原生语义未获证明。 |
| **Android** | **BLOCK：该屏幕不合规** | 空 `BackHandler` 吞掉系统及 predictive Back；标称 `40x40` 小于 `48x48dp`；字体缩放被关闭；Cupertino 控件和 Web 图标不符合 Material 语法；固定手机画布/不变底栏未适应大窗口；动效不响应 Remove animations。 |

以上是**屏幕级静态合规判定**，不是整个应用、Simulator、Emulator 或真机的运行结论。

## 3. 优先阻断项

### B1 — P0：导航与退出/恢复路径失去系统所有权

- **证据**：自定义顶栏和 JavaScript 返回替代两端原生导航；Android 的空 `BackHandler` 主动消费 Back。
- **影响**：iOS 用户失去熟悉的边缘返回；Android 用户失去按钮/手势/predictive Back；用户无法可靠预测“返回会去哪里、任务进度是否保留”。
- **通过条件**：iOS 原生栈与交互式返回、Android 系统和 predictive Back 均能完成；返回期间草稿不丢失，不再存在无行为的消费型 handler。

### B2 — P0：字体缩放与主要操作目标违反发布无障碍合同

- **证据**：所有主要操作标称 `40x40`；正文固定 `fontSize: 14`，并禁止字体缩放。
- **影响**：直接违反 Dynamic Type/font scaling 发布要求；目标尺寸低于 iOS `44pt`、Android `48dp` 的平台基线。是否存在扩大有效命中区的 `hitSlop` 尚未由源码证明。
- **通过条件**：有效目标分别达到 `44x44pt`/`48x48dp`，且不会与邻近目标重叠；最大目标字号下文字重排、不截断、主要操作仍可达。

### B3 — P1 / 发布阻断：自适应结构与核心管理者场景不匹配

- **证据**：屏幕强制 `width: 390` 并在平板居中；底部 tab 在手机、iPad、Android 平板上完全不变。
- **影响**：大窗口只是展示手机画布，无法利用平板复核所需的主从信息、批注或验证上下文；分屏缩放也没有基于实际可用宽度的结构规则。
- **通过条件**：布局由窗口宽度、姿态和输入方式驱动；compact 保持单列，medium/expanded 在空间允许时采用列表-详情或任务-验证双栏，并选择适当的 sidebar/rail/drawer/tab 结构。

### B4 — P0：完成动效违反 Reduce Motion / Remove animations 要求

- **证据**：固定 `500ms`、带 overshoot 的 spring，没有任何降级路径。
- **影响**：明确违反两端发布要求；与高频、冷静的现场操作气质不符。是否造成掉帧、延迟提交或眩晕只能在运行态判断。
- **通过条件**：普通路径使用简短、无夸张反弹的因果反馈；Reduce Motion 使用低位移 cross-fade，Remove animations 可立即切换；提交、公告和触觉不依赖动画结束回调。

### B5 — P1 / 发布阻断：控件、图标与主题只有像素复用，没有平台语义复用

- **证据**：两端使用同一 Cupertino 形状 switch 和同一 Web 图标集；浅深外观均直接使用 `#777777`、`#FFFFFF`。
- **影响**：Android 明显像 iOS/Web 移植；iOS 上即使外形近似，也未证明原生角色、值和辅助技术行为。字面颜色绕过 `DESIGN.md` 语义角色及系统外观适配。
- **通过条件**：共享语义 API，但映射为平台控件、图标、材料和颜色角色；浅色、深色、增强对比及所有控件状态分别测量。当前证据不足以断言具体颜色组合的对比度数值。

## 4. 八项具体设计动作

1. **恢复平台导航所有权**：采用能接入原生栈的 RN 导航方案；保留品牌化顶栏视觉，但不得替代 iOS interactive pop 或 Android `OnBackInvoked`/predictive Back；删除空消费型 `BackHandler`。
2. **重建窗口自适应 shell**：移除 `width: 390`；使用可用窗口尺寸/size class，而非设备型号。compact 单列，medium/expanded 按任务复核需要变为双栏，并正确处理 safe area、IME、系统栏和 fold/hinge。
3. **建立无障碍 Action primitive**：视觉图标可保持紧凑，但有效命中区达到 iOS `44pt`、Android `48dp`；定义 label、role、value/state、disabled/loading、屏幕阅读器公告、键盘/D-pad 焦点和顺序。
4. **恢复可缩放排版**：以共享的 heading/body/label/metadata 角色取代固定字号；iOS 映射 Dynamic Type，Android 映射 Material type roles/`sp`；允许换行和纵向增长，不以固定高度压住文本。
5. **落实语义主题映射**：删除组件内 `#777777`/`#FFFFFF`；共享 `text.secondary`、`surface.base`、`divider`、`focus`、`success` 等角色，分别映射 iOS dynamic system colors/materials 与 Android Material 3 color/elevation roles。
6. **按平台分支控件与图标**：共享 switch 的值、禁用、错误和 analytics 语义；iOS 使用原生 switch/SF Symbols 语法，Android 使用 Material 3 switch/Material Symbols，并分别采用原生 sheet、dialog、picker 和反馈模式。
7. **把完成动画改为因果反馈**：任务状态先可靠提交并宣布，再播放约 `150-250ms` 的平台一致反馈（最终时长以运行评审为准）；默认去掉 overshoot，系统减少/移除动画时 cross-fade 或立即切换。
8. **证明或补齐中断持久化**：编辑过程中建立可恢复 checkpoint；前后台切换、进程回收、离线重试和返回导航均保留进度；完成操作应幂等，恢复时明确展示保存/待同步/已完成状态及下一步。

## 5. Intentional parity matrix

像素一致不是目标；共享的是任务含义和结果，适配的是系统行为。

| 层 | 保持共享 | iOS / iPadOS 必须适配 | Android 必须适配 |
|---|---|---|---|
| 任务与状态 | 领域模型、验证规则、草稿 checkpoint、幂等完成、analytics 语义 | 原生生命周期/恢复入口 | Activity/process recreation、离线/恢复入口 |
| 内容层级 | 任务身份、状态、证据、主操作顺序 | compact stack；regular width sidebar/split pattern | compact stack；medium/expanded rail/drawer/two-pane |
| 导航 | 目的地图和深链语义 | Navigation Stack、edge Back、平台 tab/sidebar | 系统及 predictive Back、navigation bar/rail/drawer |
| 窗口与 inset | compact/medium/expanded 的产品优先级 | size class、safe area、键盘、iPad Split View | window size class、edge-to-edge、IME、multi-window、hinge |
| 控件与图标 | label、value、validation、enabled/loading 状态 | 原生控件、SF Symbols、iOS sheet/menu/alert | Material 3 控件、Material Symbols、snackbar/bottom sheet/dialog |
| 字体与主题 | 语义文字/颜色角色和内容层级 | Dynamic Type、system colors/materials、Increase Contrast | `sp`/font scale、Material color scheme、tonal elevation |
| 无障碍输入 | 可访问名称、操作结果、逻辑顺序、相同任务能力 | VoiceOver traits/actions、外接键盘/Switch Control | TalkBack role/state description、键盘/D-pad/Switch Access |
| 动效与反馈 | 同一因果事件及“不得延迟提交”原则 | Reduce Motion、克制 haptic、iOS 转场 | Remove animations、Material motion、Android feedback |

## 6. 已验证与未验证边界

**在本次证据包内可确认：**

- 提示明确声明目标是 `adaptive`，用户任务和无障碍要求清晰。
- 提示明确列出了固定宽度、返回处理、尺寸、字体、颜色、控件、tab 和 spring 配置；本评审将它们作为已给定事实。
- 假设这些事实准确，它们与上述 iOS/Android 平台合同和项目自身发布要求的冲突可由静态设计规则直接判定。

**仍未验证：**

- `PRODUCT.md`、`DESIGN.md` 和实现源码是否真实包含这些内容，或是否存在未描述的平台分支、`hitSlop`、主题映射及补偿逻辑。
- 实际布局、safe area、IME、旋转、iPad Split View、Android multi-window、foldable、长文案和本地化表现。
- VoiceOver/TalkBack 名称、角色、值、焦点顺序、公告，以及外接键盘/D-pad/Switch Control 遍历。
- 实际颜色组合和对比度；不能只凭两个色值推断它们在何种前景、背景、状态中配对。
- 返回手势、predictive Back、动画观感/流畅度、任务持久化、离线恢复、进程回收和重复完成行为。
- iOS/Android 编译、测试、商店配置、性能、触觉及任何 OEM/硬件差异。

## 7. 最小源码、构建与运行验证计划

**A. 源码门禁**

1. 读取真实 `PRODUCT.md`、`DESIGN.md`、导航入口、目标屏幕、主题层和草稿存储层，确认文档与当前实现是否一致。
2. 在解析出的源码目录运行定向搜索，例如：`rg -n 'width\\s*:\\s*390|allowFontScaling|BackHandler|#777777|#FFFFFF|Animated\\.spring|Switch|useWindowDimensions|AccessibilityInfo' <source-roots>`。
3. 检查有效 hit area、无障碍 props、平台分支、window class、Reduce Motion/Remove animations 监听，以及后台/进程回收后的 rehydration；为平台映射和持久化补最小单元测试。

**B. 构建门禁**

4. 先从 `package.json`/项目工具链发现并运行现有 typecheck、lint 和 targeted tests，不臆造脚本名称。
5. iOS 使用 `xcodebuild -list` 发现 workspace/project 与 scheme，再做对应 Simulator compile/test；Android 用 `./gradlew tasks` 确认模块后运行相应 `lintDebug`、unit test 和 debug assemble 任务。

**C. 原生运行门禁**

6. **iOS Simulator**：iPhone compact 与 iPad；测试 portrait/landscape、Split View 各宽度、浅深外观、最大辅助字号、Reduce Motion、VoiceOver、外接键盘、edge Back、后台及进程恢复。
7. **Android Emulator**：phone、tablet，并在适用时加入 foldable；测试 gesture navigation/predictive Back、multi-window、200% font scale、TalkBack、Remove animations、键盘/D-pad、IME/insets 和 process recreation。
8. **真机**：至少代表性 iPhone、iPad、Android phone 及目标市场的 Android tablet/foldable；验证手势、触觉、触控命中、OEM 差异和中断恢复。
9. 端到端验收应复现：操作员单手开始并部分完成任务 → 应用被打断/回收 → 恢复到准确进度 → 完成一次且不重复提交 → 管理者在平板分屏/多窗口中复核同一任务。

**当前缺失证据：**

- `iOS Simulator: unverified locally`；没有 Simulator 运行、截图、无障碍遍历或日志。
- `Android Emulator: unverified locally`；没有 Emulator/`adb` 运行、截图、无障碍遍历或日志。
- `Real-device evidence: missing`；未在 iPhone、iPad、Android phone、Android tablet/foldable 上验证。
- 源码、构建、测试、截图和无障碍树证据也全部缺失；本次未编辑任何文件。