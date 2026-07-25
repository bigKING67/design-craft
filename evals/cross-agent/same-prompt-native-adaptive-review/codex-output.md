# Native adaptive 静态评审

## 1. 证据等级、平台与设计解读

- **证据等级：`L0 static`**。只有产品上下文和静态实现描述；没有源码、截图、可访问性树或任何 native runtime 证据，因此不能升级为 L1-L4。
- **Resolved platform：`adaptive`**。依据题面中的 `PRODUCT.md platform: adaptive`、React Native，以及同时通过 iOS/Android 商店交付；对题面置信度为 `1.0`，但未对真实仓库核验。
- **产品 authority：**题面转述的 `PRODUCT.md` 管用户、任务、平台和无障碍要求；题面转述的 `DESIGN.md` 管共享语义角色，并明确允许平台原生分化。实际文件未读取。
- **实际使用：**`design-craft` 的 `critique` 模式，以及 iOS、Android、adaptive、motion、design-system、validation 规则。
- **Route 状态：**`frontend_route_plan.sh` 因只读环境无法创建临时文件，未产出 route JSON；未运行子代理、浏览器、Simulator、Emulator 或设备验证。
- **Design read：**Reading this as: 面向单手现场操作员和分屏平板管理者的任务完成/复核界面，气质可信、克制、平台原生，优化目标是快速完成、明确验证，并在中断后无损恢复。

**总体诊断：当前实现不是“共享产品语义、按平台适配”，而是把固定尺寸的 iPhone 风格画布移植到两个平台；按已给静态证据，iOS 和 Android 均应阻断设计发布门禁。**

## 2. 分平台 conformance verdict

| 平台 | Verdict | 关键依据 |
|---|---|---|
| **iOS / iPadOS** | **BLOCK** | 自定义 JS 返回替代 navigation stack，无法保证左缘返回手势和系统转场；`40x40` 低于 `44x44pt`；禁用 Dynamic Type；iPad 仍为居中的 390 宽手机画布；无 Reduce Motion 路径。 |
| **Android** | **BLOCK，偏差更严重** | 空 `BackHandler` 明确吞掉系统及 predictive Back；`40x40` 低于 `48x48dp`；Cupertino 控件和 web 图标未适配 Material；expanded width 仍用 phone bottom bar；禁用字体缩放且无 Remove animations 路径。 |

这是 **design-conformance/release gate** 结论，不是“必然被 App Store 或 Play Store 拒审”的断言。

## 3. 最多五项阻断发现

| ID | 优先级 | 发现、影响与证据边界 |
|---|---|---|
| **B1 无障碍基本尺寸与文字** | **P0** | 固定 `fontSize: 14` 且关闭 font scaling，直接违反 Dynamic Type/font scaling 要求；`40x40` 的 stated pressable box 同时低于 iOS `44pt` 和 Android `48dp`。若另有不重叠的 `hitSlop` 或更大语义父节点，可能改变有效触控面积，但题面没有该证据。VoiceOver、TalkBack、焦点顺序和键盘遍历也完全未验证。 |
| **B2 系统导航与 Back 合同** | **P0** | 自定义顶栏/JS Back 取代 iOS navigation stack；Android 空 handler 明确消费 Back。结果是平台熟悉性、iOS interactive pop、Android predictive Back、系统转场和退出恢复路径均不可信；无改动草稿是否被错误退出或困住也未知。 |
| **B3 自适应结构缺失** | **P0** | `width: 390` 居中不是 tablet adaptation。它浪费 iPad/Android tablet 空间，也无法服务管理者在 Split View/multi-window 中并排复核的核心任务；始终不变的 bottom tabs 没有体现 compact/medium/expanded 或实际可用宽度。 |
| **B4 控件、图标与主题是假统一** | **P1 Block** | Android 上的 Cupertino switch 是明确的平台偏差；一套 web 图标不能自动满足 SF Symbols/Material Symbols 的光学、语义、RTL 和状态合同。`#777777`、`#FFFFFF` 绕开 `DESIGN.md` 的语义角色，使 light/dark 对应关系不可审计；题面不足以断言具体色对的实际对比度。 |
| **B5 Motion 与中断恢复** | **P0** | 高频任务完成使用 `500ms` overshooting spring，与“calm/operational”不匹配，并且明确没有 Reduce Motion/Remove animations 分支，已违反发布要求。完成状态是否在动画前持久化、进程终止后能否恢复没有证据；不能假设动画导致丢失，也不能假设已经安全。 |

## 4. 八个具体设计动作

1. **M1 — 恢复平台导航所有权。**使用平台集成的 native stack；iOS 保留 interactive pop，Android 接入 system/predictive Back。删除空消费 handler，只在确实处理未保存状态时拦截，并提供明确的保存/放弃选择。
2. **M2 — 把恢复能力做成领域合同。**编辑过程增量持久化草稿；完成操作可重试且幂等；明确 `saving / saved / sync-pending / failed / completed` 状态。状态提交不得依赖动画结束回调。
3. **M3 — 修复操作目标与语义。**所有主操作的有效目标达到 iOS `44x44pt`、Android `48x48dp`，相邻目标不重叠；同时定义 accessible name、role、value/state、disabled/loading 状态和可见键盘/D-pad 焦点。
4. **M4 — 使用可缩放排版角色。**启用 RN font scaling；共享的是 `title/body/label/metadata` 语义，iOS 映射 Dynamic Type，Android 映射 Material type roles/`sp`。在 iOS accessibility sizes 和 Android 200% 测试点下允许换行、重排，不隐藏主操作。
5. **M5 — 以窗口能力重构布局。**移除固定 390 宽；compact 使用单栏完成流，expanded 使用适合管理复核的双栏/主从结构，例如任务内容与验证记录并置；Split View/multi-window 变窄时自动回到单栏。
6. **M6 — 建立平台 UI adapter。**共享业务组件接口和状态，分别渲染 iOS 原生 switch、菜单、sheet、符号及 Android Material 3 switch、dialog/bottom sheet、Material Symbols；导航 bar/tab/rail/sidebar 也按窗口与平台选择。
7. **M7 — 恢复语义主题。**以 `surface/text-primary/text-secondary/divider/action/success/warning` 等共享角色替代 raw hex；iOS 映射 system colors/materials/tint，Android 映射 Material color roles、tonal elevation，以及经批准的 Dynamic Color/fallback。
8. **M8 — 重写完成反馈的 motion policy。**普通路径采用短促、无夸张回弹的原生反馈，通常控制在约 `300ms` 内；iOS Reduce Motion 与 Android Remove animations 下使用即时状态变化或短 cross-fade，仍立即宣布“任务已完成”，不等待动画。

## 5. Intentional parity matrix

| 层 | 保持共享 | iOS / iPadOS 必须适配 | Android 必须适配 |
|---|---|---|---|
| 任务状态 | 字段、校验、完成规则、草稿/同步/重试语义、analytics event | scene/background 恢复及系统状态表达 | saved-state/process recreation、多窗口状态表达 |
| 内容层级 | 当前任务、必要步骤、验证结果和完成反馈的优先级 | iPhone 单栏；iPad 按 size class 使用 sidebar/split structure | 按 window size class 使用单栏、双栏、rail 或 drawer |
| 导航 | destination 含义与 route graph | navigation stack、tab/sidebar、interactive pop | system/predictive Back、navigation bar/rail/drawer |
| 控件与图标 | action、label、enabled/value 状态 | 原生 control 与 SF Symbols 语法 | Material 3 control 与 Material Symbols 语法 |
| 排版与无障碍 | 阅读顺序、操作名称、成功/错误结果 | Dynamic Type、VoiceOver、Switch Control/keyboard focus | `sp`/font scale、TalkBack、D-pad/keyboard focus |
| 颜色与材质 | semantic role 名称和状态含义 | system colors、materials、tint、iOS appearance | Material color roles、tonal elevation、可选 Dynamic Color |
| Motion | 因果关系、完成时机、Reduced Motion 结果 | native push/sheet/feedback；Reduce Motion 替代 | Material transition/predictive Back；Remove animations 替代 |
| 产品 parity | 两端都能完成、恢复和复核同一任务 | 不要求与 Android 像素一致 | 不要求复制 Cupertino 外观 |

## 6. 已验证与未验证边界

**可据此判定，但仅限题面静态记录：**

- 平台和产品要求被描述为 adaptive、单手 phone 操作和 tablet 分屏复核。
- 固定 390 宽、JS Back、空 `BackHandler`、`40x40`、固定 14/禁用缩放、raw colors、共享 Cupertino/web controls、不变 tabs、500ms overshoot、缺少 reduced-motion 分支。
- 这些陈述足以形成静态 conformance blocker，但不是源码或运行时观察。

**未验证：**

- 是否存在题面未列出的 platform branch、`hitSlop`、native component mapping、语义 token 或替代导航路径。
- VoiceOver/TalkBack labels、traits/roles、announcements、实际 traversal，以及外接键盘/D-pad/Switch Control 行为。
- safe-area、status/navigation/IME/hinge insets、旋转、Split View、multi-window、fold posture、RTL 和本地化膨胀。
- 草稿持久化、离线/失败重试、后台恢复、进程被杀、跨设备同步和重复完成保护。
- 实际颜色组合及对比度、截图层级、动画流畅度、手势手感、haptics、性能与商店构建。
- **iOS Simulator、Android Emulator、iOS real device、Android real device：全部无证据。**

## 7. 最小 source/build/runtime 验证计划

1. **Source audit：**读取真实 `PRODUCT.md`、`DESIGN.md`、导航配置及 native 工程；针对 `width: 390`、`allowFontScaling`、`BackHandler`、`hitSlop`、literal colors、switch/icon adapter、window-size branch、reduced-motion subscription 和持久化调用做 targeted `rg`，确认是否存在补偿路径。
2. **Static/unit：**测试 Back 仅在真实处理时消费；测试完成命令幂等、草稿重载；对 compact/medium/expanded 与放大字体渲染分支做组件测试。静态测试只证明分支，不证明设备行为。
3. **Build：**使用项目实际 scheme/task 运行 iOS `xcodebuild` compile/test，以及 Android Gradle compile/unit/lint；当前没有源码，不能负责任地填入真实 workspace、scheme 或 module 名。
4. **iOS Simulator — 当前缺失：**至少验证一台 iPhone 和一台 iPad；覆盖 portrait/landscape、iPad Split View、accessibility Dynamic Type、light/dark、Reduce Motion、VoiceOver、外接键盘、左缘返回、后台/终止后恢复。
5. **Android Emulator — 当前缺失：**至少验证 phone 与 expanded tablet profile；覆盖 compact/medium/expanded、multi-window、font scale、Remove animations、TalkBack、键盘/D-pad、gesture navigation、predictive Back、IME 和 process recreation。
6. **Real-device evidence — 当前缺失：**至少一台 iPhone、一台 iPad、一台 Android phone 和一台 Android tablet；验证单手可达性、真实返回手势、OEM 差异、haptics、性能，以及在完成前后被电话/锁屏/切后台打断时不丢进度。若 foldable 属于发布范围，再增加真实 foldable。
7. **放行条件：**两个平台构建通过；同一任务可在 phone 完成、在 tablet 分屏复核；每个关键步骤被中断后可恢复；目标尺寸、字体缩放、读屏、键盘 traversal 和 reduced-motion 矩阵全部有具名 runtime 结果与 artifact。Browser 或静态截图不能替代上述 native evidence。

本次未编辑任何产品文件，也未声称 Simulator、Emulator 或真机验证完成。

