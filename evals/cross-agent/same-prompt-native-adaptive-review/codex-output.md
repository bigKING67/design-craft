## 1. 证据等级、平台与设计判断

- **审查模式**：`design-craft / critique`，只读；未修改任何文件。
- **证据等级**：**L0 static / prose-only**。有明确产品上下文和静态实现描述，但没有源码实读、截图、构建或运行证据；因此不能升级为 L1/L2/L3。
- **Resolved platform**：`adaptive`。
- **平台来源**：题设中的 `PRODUCT.md platform: adaptive`，且产品明确通过 iOS、Android 商店交付 React Native 应用。
- **平台置信度**：对题设为 `1.0`；对真实仓库和产物仍未验证。
- **设计 authority**：题设描述的 `DESIGN.md`——共享语义色彩角色和内容层级，但明确允许、也要求平台原生导航、控件、图标、材质和动效差异。

> Reading this as: 面向单手执行任务的现场操作员、同时服务平板审阅经理的自适应原生任务界面；气质可信、平静、克制，优先保障快速完成、明确反馈与中断恢复。

**一句话诊断**：当前实现是“同一个 390 宽手机画布加跨平台外观复用”，不是有意设计的 adaptive 产品；按题设静态证据，iOS 与 Android 均应阻断发布合规结论。

## 2. 分平台合规判定

| 平台 | 判定 | 决定性原因 |
|---|---|---|
| **iOS / iPadOS** | **Block：静态不合规** | 非原生导航栈及返回路径破坏层级与边缘返回；禁用 Dynamic Type；声明的 `40x40` 控件小于 `44x44pt` 基线；固定手机宽度没有 iPad/Split View 结构适配；缺少 Reduce Motion 分支。 |
| **Android** | **Block：静态不合规** | 空 `BackHandler` 吞掉系统及 predictive Back；禁用字体缩放；声明的 `40x40` 控件小于 `48x48dp` 基线；Cupertino 控件和 Web 图标未适配 Material；平板仍使用手机底栏；缺少 Remove animations 分支。 |

这里的 **Block** 是对题设实现选择的静态合规判断，不代表已经观察到真机故障、手势体验、屏幕阅读器行为或性能问题。

## 3. 五项阻断发现

1. **B1 — 可访问性与控件尺寸**：`fontSize: 14` 且禁用字体缩放，直接违反 Dynamic Type/font scaling 发布要求；`40x40` 声明尺寸低于 iOS `44x44pt` 和 Android `48x48dp`。若存在 `hitSlop`，有效触控面积仍需源码及运行态确认，但字体缩放禁用本身已足以阻断。
2. **B2 — 导航与系统返回**：自定义顶部栏和 JavaScript 返回替代原生栈，使 iOS 的交互式边缘返回、状态恢复以及 Android predictive Back 无法由系统导航契约保障；空 `BackHandler` 主动吞掉 Android Back 是明确错误，而不是单纯风格差异。
3. **B3 — 自适应结构**：平板仍固定为居中的 `390` 宽单列，无法针对经理的 Split View/multi-window 审阅任务形成列表—详情、侧栏或双栏结构；不变的底部标签栏进一步表明布局由设备外观而非可用窗口宽度驱动。
4. **B4 — 控件、图标与主题体系**：跨平台复用 Cupertino 形状开关和 Web 图标，把像素一致误当成产品一致；原始 `#777777`、`#FFFFFF` 绕过 `DESIGN.md` 语义角色，不能证明深色、高对比度、禁用、按下及错误状态的主题一致性。其实际对比度是否失败还取决于颜色用途和组合，现有证据不足以断言。
5. **B5 — 动效与无障碍偏好**：任务完成是高频、结果导向状态，`500ms` 带 overshoot 的弹簧与“可信、平静、快速”定位不符；更关键的是没有 iOS Reduce Motion 或 Android Remove animations 分支，直接违反发布要求。静态证据不能证明卡顿，但可以证明替代路径缺失。

## 4. 八个具体设计动作

1. **恢复原生导航所有权**：使用 React Native 的 native-stack/等价原生导航；iOS 保留交互式边缘返回，Android 将返回交给系统与 predictive Back；删除吞事件的空 `BackHandler`，未保存内容通过受支持的导航 guard 处理。
2. **按窗口而非设备型号适配**：移除固定 `width: 390`；compact 使用单列任务流，medium/expanded 转为列表—详情或侧栏结构，并覆盖 iPad Split View、Android multi-window、横屏和折叠姿态。
3. **修正触控与排版基线**：iOS 有效目标至少 `44x44pt`，Android 至少 `48x48dp` 并保持合理间距；使用平台文本角色、允许字体缩放，确保最大支持字号下内容重排且主操作仍可达。
4. **拆分平台控件和系统图标**：共享 `Switch`、返回、更多操作等语义 API，但 iOS 渲染系统开关/SF Symbols，Android 渲染 Material 3 Switch/Material Symbols；品牌或领域专属图标可以共享。
5. **建立语义主题映射**：把 `surface`、`onSurface`、`secondaryText`、`accent`、`danger`、`disabled` 等共享角色分别映射到 iOS semantic colors/materials 与 Android Material color roles；覆盖 light/dark/high-contrast 和所有控件状态。
6. **重做完成反馈**：数据完成状态立即提交，不等待动画回调；默认使用短促、无 overshoot 的确认反馈，Reduce Motion/Remove animations 下改为短交叉淡化或即时状态变化，并同步屏幕阅读器公告。
7. **补齐语义和键盘路径**：为任务、状态、开关和操作提供 label、role、value/state、可预测遍历顺序和完成公告；验证 VoiceOver、TalkBack、外接键盘、D-pad/Switch Control，不依赖颜色或动效传达结果。
8. **把中断恢复做成核心状态机**：关键输入增量持久化，后台、进程终止、导航离开、离线重连后恢复同一任务；完成操作具备幂等性，并清楚显示草稿、同步中、冲突和已完成状态。

### Intentional parity matrix

| 层面 | 保持共享 | iOS / iPadOS 必须适配 | Android 必须适配 |
|---|---|---|---|
| 任务模型 | 任务字段、验证规则、完成状态机、持久化语义 | iOS lifecycle/state restoration 接入 | Android activity/process recreation 接入 |
| 内容层级 | 标题、步骤、证据、状态、主次操作 | NavigationStack；regular width 使用 sidebar/split structure | NavHost；compact bar、medium rail、expanded drawer/list-detail |
| 返回行为 | “返回/取消/保存草稿”的产品规则 | 系统导航栈与边缘返回 | 系统 Back、predictive Back 与手势进度 |
| 主题 | 语义角色、品牌 tint、状态含义 | semantic colors、system materials、SF typography | Material 3 roles、tonal elevation、Material typography |
| 控件与图标 | 意图、文案、analytics、业务状态 | 原生 controls、SF Symbols、平台菜单/弹层 | Material controls、Material Symbols、snackbar/sheet/dialog |
| 无障碍 | 相同任务结果、标签含义、无功能损失 | VoiceOver、Dynamic Type、Switch Control | TalkBack、`sp`/font scale、D-pad |
| 动效 | 完成因果关系和状态顺序 | iOS transition/haptics；Reduce Motion | Material transition/feedback；Remove animations |
| 自适应 | compact/expanded 的信息优先级 | iPad size class、Split View、键盘导航 | window size class、multi-window、fold posture |

## 5. 已验证与未验证

**已验证——仅指题设明确提供的事实，并非本地独立验证：**

- 产品目标平台、用户、任务、定位、无障碍要求，以及 `DESIGN.md` 允许平台原生适配。
- 题设列出的固定宽度、返回拦截、控件尺寸、字体缩放禁用、原始色值、共享控件/图标、固定底栏和无减弱动效分支。
- 上述明确实现选择与 iOS/Android 原生尺寸、返回、字体缩放和 motion-accessibility 契约之间的静态冲突。

**未验证：**

- 真实源码是否与描述完全一致，以及是否存在未提及的 `hitSlop`、平台分支或补偿逻辑。
- VoiceOver/TalkBack 的 label、trait/role、value、遍历、焦点恢复和公告。
- 外接键盘、D-pad、Switch Control 的实际遍历顺序与焦点可见性。
- 色值的实际用途、背景组合、对比度、深色模式和高对比度最终渲染。
- safe area、IME、旋转、Split View、multi-window、foldable 和大字号下的实际布局。
- 自动保存、后台恢复、进程终止恢复、离线同步和完成幂等性。
- predictive Back、iOS 边缘返回、动画顺滑度、性能、触觉反馈及真机手感。
- 构建、截图、Simulator、Emulator 或任何真实设备结果。

## 6. 最小源码、构建与运行验证计划

1. **源码确认**：读取真实 `PRODUCT.md`、`DESIGN.md`、`package.json`、导航入口、目标 screen、theme/tokens、持久化层及 iOS/Android 工程配置；定位 `BackHandler`、`allowFontScaling`、`fontSize`、`width: 390`、原始色值、switch/icon、tab 和 spring 实现。
2. **静态平台扫描**：对真实仓库运行 `design_craft_platform_scan.py --target <repo> --platform adaptive --json`，再人工核对每项命中；扫描结果只能作为源码证据，不能替代运行验证。
3. **共享构建门禁**：按真实 `package.json` 选择现有 type-check、lint、unit/integration test；为草稿恢复、幂等完成和平台组件选择补 targeted tests。
4. **iOS 构建**：使用真实 workspace/scheme 执行 `xcodebuild` build/test；这只能证明编译和测试，不能证明手势、VoiceOver或 iPad 窗口行为。
5. **Android 构建**：使用真实 module 执行 Gradle assemble、lint 和 unit/instrumentation tests；同样不能替代 predictive Back、TalkBack 和 multi-window 观察。
6. **iOS Simulator**：至少覆盖 iPhone 与 iPad、compact/regular、横竖屏或可调整窗口、最大 Dynamic Type、VoiceOver、Reduce Motion、外接键盘、边缘返回、后台及重新启动恢复。
7. **Android Emulator**：至少覆盖 API 34+ gesture-navigation phone、tablet 和 foldable profile，测试 predictive Back、multi-window、200% font scale、TalkBack、Remove animations、键盘/D-pad、activity/process recreation。
8. **真实设备发布门禁**：代表性 iPhone、iPad、Android gesture-navigation phone 和 Android 大屏设备上验证单手可达性、系统返回、屏幕阅读器、键盘、生命周期中断、OEM 差异、触觉反馈和持续性能。

当前证据状态明确为：

- **iOS Simulator: unverified locally**
- **Android Emulator: unverified locally**
- **iOS real device: unverified**
- **Android real device: unverified**
- **真实 iPad/Android tablet split-screen 或 multi-window: unverified**
- **截图与 accessibility tree artifact: none**