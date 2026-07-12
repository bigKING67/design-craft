## 1. 证据级别、平台与设计解读

- **审查模式**：`critique`，只读；使用 `design-craft` 的 iOS、Android、adaptive 与验证合同。
- **证据级别**：**L0 static**——只有产品上下文和静态实现描述；没有源码、截图、构建或运行态证据。
- **解析平台**：`adaptive`，来源为题面给出的 `PRODUCT.md`；对“设计目标平台”的置信度高，但实际 iOS/Android target 未核验。
- **样式权威**：题面给出的 `DESIGN.md` 要求共享语义角色，同时明确允许平台原生导航、控件、图标、材质和动效；因此**体验等价不等于像素相同**。
- **Design read**：这是面向现场操作员与管理者的任务执行/复核界面，气质应可信、克制、可恢复，优先保障手机单手快速完成，以及平板并窗中的连续审阅。
- **一句诊断**：当前实现更像“固定宽度的共享手机皮肤”，而不是同时尊重 iOS、Android 和扩展窗口的 adaptive 原生产品。
- **文件/结构影响**：无；本次未编辑任何文件。

## 2. 分平台一致性结论

| 平台 | 结论 | 主要依据 |
|---|---|---|
| **iOS / iPadOS** | **阻断发布，平台一致性不通过** | 导航栈和交互式返回被 JS 替代；`40x40` 低于 `44x44pt`；Dynamic Type 被禁用；iPad 仍是居中的 390 宽手机画布；没有 Reduce Motion 路径。 |
| **Android** | **阻断发布，平台一致性不通过；导航问题尤其严重** | 空 `BackHandler` 主动吞掉系统 Back 和 predictive Back；`40x40` 低于 `48x48dp`；字体缩放被禁用；Cupertino 控件、固定底栏和非 Material 主题不能形成可信的 Android 体验。 |

以上是基于题面静态属性的**规范判定**，不是模拟器、设备或实际交互观察结果。

## 3. 最多五项阻断问题

1. **P0｜无障碍与控件尺寸**
   - 所有主操作为 `40x40`：低于 iOS `44pt` 和 Android `48dp` 的最低目标。
   - `fontSize: 14` 且关闭字体缩放，直接违背 Dynamic Type/font scaling 发布要求。
   - 即使存在未描述的 `hitSlop`，也仍需源码和无障碍检查证明有效点击区域；字体缩放禁用本身已经足以阻断。

2. **P0｜导航与系统 Back**
   - iOS：自定义顶栏和 JS 返回替代原生导航栈，破坏平台层级、交互式左缘返回和系统状态恢复语义。
   - Android：空 `BackHandler` 吞掉 Back，是明确的平台行为回归；predictive Back 的预览、取消和提交均无法成立。
   - 对容易被打断的现场流程，这还会削弱“可离开、可恢复、不会丢失”的信任。

3. **P0｜平板、分屏与多窗口适配**
   - 强制 `width: 390` 并居中不是 adaptive layout，只是把手机画布放到更大的窗口里。
   - 不变的底部 tab 没有回应 iPad Split View、Android multi-window、横屏、键盘输入或管理者的主从复核场景。
   - 窗口变化期间能否保留任务步骤、滚动位置和未提交输入完全未知。

4. **P1｜平台控件、图标与主题语义**
   - Cupertino 形态开关在 Android 上是明确的移植感；单一 web 图标集也没有证明系统动作在两端符合 SF Symbols/Material Symbols 语义。
   - `#777777`、`#FFFFFF` 绕过 `DESIGN.md` 的语义色角色，不能可靠适配 light/dark/high-contrast、Material tonal elevation 或 iOS system materials。
   - 目前不能据此断言具体对比度数值失败，但可以确认主题合同没有被正确消费。

5. **P1｜完成动效与减少动画**
   - `500ms` overshoot spring 对高频、严肃的现场完成动作偏慢且过度活跃；真正的发布阻断点是没有 Reduce Motion/Remove animations 路径。
   - 任务状态应先可靠提交并反馈，不能依赖动画结束；当前状态提交和动画是否耦合尚未验证。

## 4. 八项具体设计动作

1. **恢复平台导航所有权**
   - 使用 React Navigation native-stack 或等价原生栈；自定义视觉可以保留，但不能替代系统路由语义。
   - 移除吞 Back 的空处理器；验收 iOS 左缘返回及 Android predictive Back 的预览、取消、提交。

2. **删除固定 390 宽度**
   - 基于可用窗口、size class/window size class、方向和输入方式布局，不依据设备型号。
   - compact 为单栏任务流；expanded 为列表/任务上下文与详情/验证结果的双栏结构。

3. **按平台和宽度适配主导航**
   - compact phone 可以继续使用底部目的地导航。
   - iPad 优先 sidebar/navigation split；Android medium/expanded 使用 navigation rail 或 drawer，并保持目的地和分析语义一致。

4. **将共享组件改为“语义 API、原生渲染”**
   - 共享 `checked/value/disabled/error/onChange` 等业务合同。
   - iOS 映射原生 switch、picker、sheet、alert 与 SF Symbols；Android 映射 Material Switch、picker、bottom sheet/dialog 与 Material Symbols。

5. **重建无障碍尺寸、文字和遍历合同**
   - iOS 至少 `44x44pt`，Android 至少 `48x48dp`，同时检查相邻目标间距。
   - 启用 Dynamic Type/font scaling，至少验证 200% 和 iOS accessibility sizes。
   - 补齐 VoiceOver/TalkBack label、role、value、state、announcement、focus order，以及外接键盘/D-pad 遍历。

6. **建立共享语义 token、平台映射值**
   - 共享 `surface.*`、`text.*`、`border.*`、`state.*` 等角色，而不是共享 `#777777`。
   - iOS 映射 semantic system colors/materials；Android 映射 Material 3 color scheme、tonal elevation，并为 Dynamic Color 提供明确 fallback。
   - 分别测量 light、dark、high-contrast 下的文本、图标、禁用和焦点状态。

7. **重做完成反馈**
   - 先提交并展示完成状态，再执行非阻塞反馈；不要等待动画回调才保存。
   - 默认采用短促、克制的平台过渡；取消明显 overshoot。
   - Reduce Motion 使用轻微 cross-fade 或即时切换，Android Remove animations 下不得依赖运动表达结果。

8. **把中断恢复设计成共享产品能力**
   - 在关键字段变化或步骤推进时持久化草稿、当前位置和提交状态。
   - 验证 background/foreground、进程终止重启、旋转、分屏尺寸变化及返回导航后恢复到同一任务状态。

## 5. Intentional parity matrix

| 维度 | 保持共享 | iOS / iPadOS 必须适配 | Android 必须适配 |
|---|---|---|---|
| 任务模型 | 步骤、完成条件、验证规则、草稿与错误语义 | iOS lifecycle/state restoration 接入 | Android lifecycle/saved state 接入 |
| 内容层级 | 标题、任务信息优先级、主操作含义 | compact 与 NavigationSplitView/sidebar 思路 | compact/medium/expanded window classes |
| 导航 | 目的地、路由身份、分析事件 | native stack、interactive pop、tab/sidebar | Navigation component、predictive Back、bar/rail/drawer |
| 控件与图标 | 组件语义、状态和业务回调 | 原生控件、SF Symbols、iOS sheets/alerts | Material 3 控件、Material Symbols、bottom sheets/dialogs |
| 颜色与文字 | semantic token 名称、内容等级、状态含义 | Dynamic Type、system colors/materials | `sp`/font scaling、Material type/color/elevation |
| 无障碍 | 操作结果、阅读顺序、标签内容、错误反馈 | VoiceOver、Switch Control、键盘焦点 | TalkBack、D-pad/键盘焦点、state descriptions |
| 动效反馈 | 因果顺序：提交→状态反馈→可选动效 | Reduce Motion、iOS transition/haptic | Remove animations、Material transition/haptic |

## 6. 已验证与未验证

**题面静态证据可判定，但未独立读取源码：**

- 平台意图为 `adaptive`，且设计权威允许平台差异。
- 描述中存在固定 `390` 宽度、自定义返回、空 `BackHandler`、`40x40` pressable、字体缩放禁用、literal colors、同一开关/图标、固定 tab 和无减弱路径的 500ms spring。
- 这些属性足以判定最低目标尺寸、文字缩放、系统 Back 和减少动画合同不符合要求。

**未验证：**

- 实际源码位置、React Native/导航库版本、iOS/Android target、原生配置及是否另有 `hitSlop`。
- VoiceOver/TalkBack 树、label/role/value、焦点顺序、公告和外接键盘遍历。
- 实际颜色组合及对比度；safe area、system bars、IME、cutout、hinge 和 fold posture。
- Dynamic Type/font scaling 后的换行、裁切、滚动和操作可达性。
- 旋转、iPad Split View、Android multi-window、foldable 和窗口实时 resize。
- 返回手势、predictive Back、动效观感、帧率、haptic、OEM 差异和性能。
- background/process death 后的任务恢复，以及动画是否与持久化耦合。
- 无截图、无 accessibility tree、无 build artifact；浏览器验证不适用于替代原生运行态验证。

## 7. 最小源码、构建和运行态验证计划

1. **源码定位**
   - 检查 `PRODUCT.md`、`DESIGN.md`、`package.json`、导航配置、`ios/`、`android/` 和 token/theme 层。
   - 定向搜索：`width: 390`、`BackHandler`、`allowFontScaling={false}`、`fontSize: 14`、两个 literal colors、switch/icon、tab 配置、spring/`500` 和 accessibility settings。
   - 确认有效点击区域、平台分支、持久化时点以及 Back handler 的返回值。

2. **静态与组件验证**
   - 运行项目已有 lint、typecheck、导航/状态恢复测试和 accessibility fixture。
   - 增加窗口尺寸、200% font scale、Reduce Motion、Back dispatch 和中断恢复的组件/集成测试。

3. **iOS 构建与运行**
   - 用实际 workspace/scheme 执行 `xcodebuild` 编译和测试。
   - Simulator 覆盖 iPhone compact、iPad 全屏与 Split View、横竖屏、Dynamic Type accessibility sizes、VoiceOver、Reduce Motion、外接键盘和交互式返回。
   - **iOS Simulator: unverified locally（本次未运行，证据缺失）。**

4. **Android 构建与运行**
   - 执行项目对应的 `./gradlew :app:assembleDebug :app:lintDebug :app:testDebugUnitTest`。
   - Emulator 覆盖 phone、tablet、foldable/expanded window、multi-window、gesture navigation/predictive Back、200% font scale、TalkBack、Remove animations、IME 和键盘/D-pad。
   - **Android Emulator: unverified locally（本次未运行，证据缺失）。**

5. **真实设备发布门禁**
   - 至少验证 iPhone 与 Android phone 的单手操作、返回手势、中断恢复、性能和触觉反馈。
   - 因管理者平板场景是核心需求，还需代表性 iPad 与 Android tablet/foldable 的分屏、多窗口和键盘验证。
   - **Real-device evidence: unverified；iPhone、iPad、Android phone、Android tablet/foldable 均未运行。**

**最终结论**：静态证据已足以阻断当前设计进入发布候选；只有在上述五项阻断修正，并取得两端 build、Simulator/Emulator 和代表性真实设备证据后，才能把结论升级为 adaptive 平台一致性通过。