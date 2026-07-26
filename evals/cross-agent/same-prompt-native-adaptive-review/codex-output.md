## 1. 证据等级、平台解析与设计解读

- **证据等级：`L0 static`**。依据仅为产品上下文和静态实现描述；没有截图、源码、构建产物、可访问性树或原生运行态，不能升级为 `L1 contextual` 或原生验证证据。
- **Resolved platform：`adaptive`**。来源是用户转述的 `PRODUCT.md` 声明，以及同时通过 iOS、Android 商店交付的产品事实；对目标平台判断为高置信度，但未由仓库或构建配置独立确认。
- **设计 authority：**用户转述的 `DESIGN.md` 要求共享语义色彩角色和内容层级，同时明确允许导航、控件、图标、材质和动效按平台适配。因此，当前的像素级同构不是设计规范要求。
- **实际使用：**`design-craft` 的 `critique` 模式及 iOS、Android、adaptive、design-system、motion、validation 合同。未使用子代理。
- **Route：**route planner 可用性检查因只读宿主无法创建临时文件而中止：`cannot create temp file for here document: Operation not permitted`；不声称获得了 route 结果。
- **设计解读：**这是一个面向单手现场操作员、同时服务平板审核经理的抗中断任务界面；气质应冷静、可信、平台原生，首要优化目标是快速完成、可靠保存并明确验证任务。

## 2. 分平台符合性结论

| 平台 | 静态符合性结论 | 决定性依据 |
|---|---|---|
| **iOS / iPadOS** | **不通过，存在发布阻断项** | 绕过导航栈、`40x40` 小于 `44x44pt`、禁用 Dynamic Type、固定手机画布、无 Reduce Motion 路径；iPad 结构没有随可用空间适配。 |
| **Android** | **不通过，存在发布阻断项** | `BackHandler` 吞掉系统 Back、破坏 predictive Back、`40x40` 小于 `48x48dp`、禁用字体缩放、使用 Cupertino/web 控件语言、无 Remove animations 路径。 |
| **Adaptive 总体** | **不通过** | 当前实现共享了不应共享的像素和控件外观，却没有共享好语义、状态恢复和可访问性结果，也没有建立明确的平台适配层。 |

以上是**基于给定静态事实的规范判定**，不是 Simulator、Emulator 或真机认证。

## 3. 优先级 findings

### Blocking，最多五项

1. **B1 — Accessibility / typography：字体缩放被主动禁用。**  
   固定 `fontSize: 14` 且关闭 font scaling，直接违背 Dynamic Type/Android font scaling 的发布要求。必须允许系统缩放，并确保最大支持字号下内容重排、操作仍可达。

2. **B2 — Accessibility / controls：所有主操作目标均过小。**  
   `40x40` 低于 iOS 的 `44x44pt` 和 Android 的 `48x48dp` 最低有效目标。不能只放大图标；需要扩大实际命中区域、避免相邻目标重叠，并保持键盘焦点可见。

3. **B3 — Navigation：平台 Back 合同被替换或吞掉。**  
   iOS 自定义顶部栏和 JavaScript Back 绕过导航栈及系统交互式返回保证；Android 空 `BackHandler` 明确消费系统 Back，并阻断 predictive Back。自定义 Back 也不能证明任务草稿会在返回、挂起或进程重建后保留。

4. **B4 — Adaptivity：固定 `390` 宽度不是平板适配。**  
   在平板居中显示手机画布，加上所有窗口尺寸保持同一底部 tab，未服务经理的 Split View/multi-window 审核工作。布局必须由可用宽度、窗口类别、姿态和输入模式驱动，而不是设备名称或固定宽度。

5. **B5 — Accessibility / motion：缺少系统减弱动效路径。**  
   `500ms` overshoot spring 没有 iOS Reduce Motion 或 Android Remove animations 分支，直接违反发布要求。常规路径的 500ms 回弹也与“冷静、快速、操作型”定位冲突；但是否实际显慢仍需运行态观察。

### High，但不凭静态描述升级为阻断事实

6. **H1 — Theming：字面颜色绕过语义角色。**  
   两种 appearance 直接使用 `#777777`、`#FFFFFF`，与 `DESIGN.md` 的语义 token 合同不符。实际颜色配对、对比度和暗色渲染未提供，因此不能声称某个具体对比度已经失败。

7. **H2 — Controls / native identity：错误地把外观一致当作体验一致。**  
   Android 使用 Cupertino switch 和两端共用 web icon set，削弱 Material 语义、状态和用户熟悉度；iOS 端的 web 图标及仿原生 switch 是否具有完整 native semantics 同样未经证明。

## 4. 八个具体设计 moves

1. **恢复平台导航。**iOS 使用原生 navigation stack 并保留交互式返回；Android 接入系统/predictive Back，删除无条件消费 Back 的 handler。任务草稿状态独立于页面实例和导航动画。
2. **建立可缩放字体角色。**共享 `heading/body/label/status` 语义；iOS 映射 Dynamic Type text styles，Android 映射 Material type roles 与 `sp`，在最大支持字号下允许换行和纵向增长。
3. **修复有效操作目标。**iOS 至少 `44x44pt`，Android 至少 `48x48dp`，Android 相邻操作通常保留约 `8dp` 间隔；图标可保持视觉尺寸，但完整 press area 必须可聚焦且不重叠。
4. **按窗口能力重构界面。**compact phone 使用单栏任务流；iPad/Split View 转为 sidebar 或 list-detail；Android medium/expanded 使用 navigation rail/drawer 与双栏审核，窄 multi-window 自动回落为单栏。
5. **使用平台控件和图标映射。**共享 switch 的业务值和事件，不共享外观实现；iOS 使用原生 switch、SF Symbols 和系统 material，Android 使用 Material 3 switch、Material Symbols 与 tonal elevation。
6. **落实语义主题层。**组件只消费 `surface/text/divider/action/success/warning/danger/focus` 等角色；这些角色分别映射 iOS system colors/materials 和 Android Material color scheme，并覆盖 light、dark、high contrast 与所有交互状态。
7. **把完成动效改为因果反馈。**默认路径缩短并去除不必要 overshoot；iOS Reduce Motion 使用短 cross-fade 或静态状态更新，Android Remove animations 使用即时变化或极短淡变，同时保留清晰的“已完成/待同步”反馈。
8. **补齐可访问性与抗中断状态。**定义 VoiceOver/TalkBack label、role、value、state announcement 和稳定 traversal；支持外接键盘/D-pad；自动保存草稿，并明确区分 `saving/saved/offline/pending verification/completed`，恢复后不得重复提交。

### Intentional parity matrix

| 领域 | 保持共享 | iOS / iPadOS 必须适配 | Android 必须适配 |
|---|---|---|---|
| 任务模型 | 字段、校验、完成条件、草稿和幂等规则 | 平台生命周期接入 | 进程重建与 saved-state 接入 |
| 内容层级 | 任务、证据、状态、主操作的优先级 | iPhone 单栏；iPad sidebar/list-detail | compact 单栏；medium/expanded 双栏 |
| 导航 | destination 与深链语义 | navigation stack、interactive Back、适合 iPad 的 sidebar/tab | NavHost、system/predictive Back、bar→rail/drawer |
| 控件与图标 | 值、动作、disabled/loading/error 语义 | 原生 Apple 控件、SF Symbols、system materials | Material 3 控件、Material Symbols、tonal elevation |
| 类型 | 角色和信息层级 | Dynamic Type、系统字体指标 | `sp`、Material type scale |
| 颜色 | semantic role 名称和状态含义 | system colors/materials 映射 | Material color scheme/Dynamic Color 策略 |
| 可访问性 | 等价任务结果、读序意图、动作命名 | VoiceOver、Switch Control、键盘焦点 | TalkBack、D-pad/键盘、state description |
| Motion/feedback | 完成、失败、保存等因果语义 | Apple 转场、Reduce Motion、平台 haptics | Material motion、Remove animations、平台 feedback |

## 5. 已验证与未验证边界

**本轮独立验证：**

- 没有对产品代码或运行态进行独立验证。
- 可以确定的是：如果提供的 `40x40`、禁用 font scaling、吞掉 Android Back、固定 `390` 宽度和缺少减弱动效分支均准确，那么它们分别违反上述平台合同。
- 用户提供的实现描述被作为本轮评审输入事实，而不是本机复现结果。

**明确未验证：**

- `PRODUCT.md`、`DESIGN.md` 和 React Native 源码的实际内容、分支覆盖及是否存在补偿实现。
- iOS safe area、interactive Back、状态恢复、Dynamic Type、VoiceOver、键盘和 Reduce Motion 的真实行为。
- Android insets、predictive Back、进程重建、font scaling、TalkBack、D-pad/键盘和 Remove animations 的真实行为。
- 旋转、iPad Split View、Android multi-window、平板、foldable/hinge posture 和 IME 布局。
- light/dark/high-contrast 的真实渲染、字面颜色的实际前景/背景配对及对比度。
- 动效流畅度、耗时感、可中断性、haptics、60/120Hz 性能。
- 截图、可访问性树、构建、单元测试、集成测试、商店包和真实硬件体验。

## 6. 最小源码、构建与运行态验证计划

1. **源码核对：**读取真实 `PRODUCT.md`、`DESIGN.md`、`package.json`、导航入口和 iOS/Android 工程；用  
   `rg -n "width:\\s*390|BackHandler|allowFontScaling|fontSize:\\s*14|#777777|#FFFFFF|Switch|spring|500"`  
   定位描述中的实现，同时追踪草稿保存、恢复、完成幂等和所有调用方。
2. **静态测试：**运行仓库已有的 typecheck、lint、React Native 单测和 accessibility/component tests；检查原生导航集成、语义属性、焦点顺序及主题 token，无脚本名称时先从 `package.json` 发现，不能假定测试已存在。
3. **iOS build：**发现真实 workspace/scheme 后运行  
   `xcodebuild -workspace <app>.xcworkspace -scheme <scheme> -sdk iphonesimulator build test`。  
   **当前：iOS build/test 未执行。**
4. **Android build：**运行  
   `./gradlew :app:assembleDebug :app:testDebugUnitTest :app:lintDebug`，并核对 predictive Back 配置。  
   **当前：Android build/test 未执行。**
5. **iOS runtime：**至少覆盖一台 iPhone Simulator 和一台 iPad Simulator；测试最大 Dynamic Type、VoiceOver、Reduce Motion、外接键盘、旋转、Split View、返回手势、后台中断和重启恢复。  
   **`iOS Simulator: unverified locally`。**
6. **Android runtime：**至少覆盖 phone、tablet/expanded 和 foldable 或 multi-window Emulator；测试最大 font scale、TalkBack、Remove animations、gesture navigation/predictive Back、IME、D-pad/键盘和进程重建恢复。  
   **`Android Emulator: unverified locally`。**
7. **真实设备发布门禁：**在代表性 iPhone/iPad 与至少一台 gesture-navigation Android 手机及一台 Android tablet/OEM 设备上验证单手可达性、系统 Back、haptics、性能、中断恢复和屏幕阅读器。  
   **iOS real-device、Android real-device 证据均缺失，不能声称真机或发布级原生验证。**