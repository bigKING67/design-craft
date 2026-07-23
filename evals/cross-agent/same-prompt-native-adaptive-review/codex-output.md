## 1. 证据等级、平台解析与设计读取

- **Evidence level：`L0 static`**——仅有题面和静态实现描述；没有读取项目源代码，也没有构建、截图、可访问性树或原生运行态证据。
- **Resolved platform：`adaptive`**——来源是题面所述 `PRODUCT.md platform: adaptive`；对产品意图置信度高，但实际 iOS/Android target 是否存在及其配置未验证。
- **Design authority：**题面所述 `DESIGN.md` 要求共享语义色彩角色与内容层级，同时明确允许原生导航、控件、图标、材质和动效。因此，**跨平台一致应是任务语义一致，而不是控件和像素完全相同**。
- **Selected skill：**`design-craft`，使用 `critique` 模式，并应用 iOS、Android、adaptive、motion、design-system 与 validation 合同；未运行实现型 route。
- **Design read：**将其读作一套面向单手现场操作员、同时服务平板审核经理的原生任务完成与核验界面，气质应冷静、可信、低干扰，优先保证快速完成、明确反馈和中断后可靠恢复。
- **一句话诊断：**产品语义适合共享，但当前实现是“固定宽度的同一套手机 UI 移植到两端”，未形成平台原生、无障碍或窗口自适应体验。

## 2. 分平台合规结论

| 平台 | 结论 | 决定性依据 |
|---|---|---|
| **iOS / iPadOS** | **Block：静态合规不通过，不具备 release-ready 证据** | `40x40` 小于 `44x44pt`；禁用 Dynamic Type；自定义顶栏和 JS 返回替代原生 navigation stack/边缘返回；iPad 固定 `390` 宽；缺少 Reduce Motion 分支。 |
| **Android** | **Block：静态合规不通过，不具备 release-ready 证据** | `40x40` 小于 `48x48dp`；空 `BackHandler` 吞掉 system/predictive Back；Cupertino 控件与 web 图标不符合 Material；平板仍用手机底栏；禁用 font scaling；缺少 Remove animations 分支。 |

这不是对 App Store 或 Google Play 审核结果的预测；结论仅表示实现描述与既定产品要求、iOS/Android 平台合同存在明确冲突。

## 3. 五项阻断问题

### B1 — Accessibility / Controls：文字缩放和操作目标直接违约

- **证据：**全部主操作为 `40x40`；固定 `fontSize: 14`；font scaling 被关闭。
- **影响：**两端均不满足最低目标尺寸；低视力用户无法使用 Dynamic Type/font scaling，放大文字后的重排、截断和可达性也无法成立。
- **平台差异：**iOS 至少 `44x44pt`；Android 至少 `48x48dp`，通常还需约 `8dp` 的目标间隔。
- **验收：**所有核心操作达到有效点击区域门槛；最大支持字号下核心任务、错误恢复和完成操作仍完整可达。

### B2 — Navigation / Interruption：破坏两端系统返回合同

- **证据：**自定义顶栏和 JS 返回替代 iOS navigation stack；Android `BackHandler` 无条件消费 Back。
- **影响：**iOS 用户失去可信的层级栈和边缘返回；Android 用户被困在页面内，predictive Back 也无法表达正确目的地预览。
- **边界：**题面没有证明任务进度一定丢失，但也没有任何草稿持久化、后台恢复或进程重建证据。
- **验收：**原生返回手势/按钮工作，离开路径可预测；只有确有未保存风险时才拦截；中断后恢复到相同任务、步骤和已录入状态。

### B3 — Adaptivity：平板和多窗口仍是居中的手机画布

- **证据：**单屏强制 `width: 390`；底部 tab 在手机、iPad、Android tablet 上完全不变。
- **影响：**经理审核任务时无法利用额外宽度并置清单、证据和审核操作；Split View/multi-window 缩放也不是结构自适应。
- **说明：**底部 tab 本身并非在所有平板场景都错误；错误在于它与固定画布一起对所有 window class 无条件保持不变。
- **验收：**布局由可用宽度、size/window class、posture 和输入方式驱动；expanded 状态提供双栏、sidebar、rail 或 drawer 等合适结构。

### B4 — Theming / Native controls：共享语义被误实现为共享外观

- **证据：**两种 appearance 直接使用 `#777777`、`#FFFFFF`；两端共用 Cupertino 形状开关和 web icon set。
- **影响：**绕过 `DESIGN.md` 的语义角色和主题映射；Android 明显呈现 iOS/web 移植感；iOS 上“长得像 UISwitch”也不能证明原生语义、焦点、状态和值播报。
- **边界：**缺少颜色使用上下文，不能据此声称具体对比度数值不合格；能确认的是语义 token 与平台映射合同被绕过。
- **验收：**共享 role 名称稳定，但分别映射到 iOS system colors/materials/SF Symbols 与 Material 3 roles/elevation/Material Symbols。

### B5 — Motion：无障碍动效设置缺失，完成反馈与产品气质冲突

- **证据：**任务完成使用 `500ms` overshooting spring，且没有 Reduce Motion/Remove animations 替代。
- **影响：**直接违反发布要求；长且过冲的完成动效还可能使高频操作显得拖沓、庆祝性过强，不符合“冷静、可信、操作型”定位。
- **边界：**静态描述不能证明卡顿、帧率、实际眩晕感或主观手感。
- **验收：**完成状态先可靠提交，再播放非阻塞反馈；iOS Reduce Motion 使用缩短位移或 cross-fade，Android Remove animations 使用 cross-fade 或即时状态变化。

## 4. 八个具体设计动作

1. **恢复平台导航合同：**iOS 使用原生 navigation stack 并保留边缘返回；Android 接入 system/predictive Back，移除无条件消费的 `BackHandler`。  
2. **把恢复能力独立于导航和动效：**任务草稿在关键字段变化、后台切换和步骤提交时原子 checkpoint；完成状态先落盘/入 outbox，再触发转场。  
3. **改用可缩放字体角色：**共享内容层级，iOS 映射 Dynamic Type text styles，Android 映射 Material type roles 和 `sp`；允许换行和容器重排。  
4. **建立交互无障碍合同：**有效目标分别达到 `44pt`/`48dp`；补齐 label、role、value/state、完成公告、逻辑 traversal，以及外接键盘/D-pad 的可见焦点。  
5. **落实语义主题映射：**删除组件中的主题 literal；共享 `surface/text/muted/accent/success/warning/error` 等角色，分别解析到平台 light/dark/high-contrast 资源。  
6. **建立平台组件层：**共享业务 props 和状态机，但 iOS 使用原生 switch、SF Symbols、sheet/context action；Android 使用 Material switch、Material Symbols、snackbar/bottom sheet。  
7. **按窗口能力重构布局：**compact 保持单栏快速完成；medium/expanded 转为 rail/sidebar 与 task-detail 双 pane，并覆盖 iPad Split View、Android multi-window、fold posture、IME/insets。  
8. **重做完成动效：**即时呈现状态变化，缩短或取消过冲；按平台使用合适的 push/fade-through/cross-fade，并实时读取 Reduce Motion/Remove animations。  

## 5. Intentional parity matrix

| 领域 | 必须共享 | iOS / iPadOS 必须适配 | Android 必须适配 |
|---|---|---|---|
| 任务模型 | 草稿、进行中、已完成、失败、待同步、恢复规则及 analytics 语义 | 使用 Apple lifecycle 下的可靠恢复入口 | 覆盖 background、activity/process recreation 与 outbox 恢复 |
| 内容层级 | 任务身份、步骤顺序、证据、状态、主操作和错误恢复语义 | 符合 iOS list/detail、sheet 与 toolbar 层级 | 符合 Material screen、top app bar、sheet/snackbar 层级 |
| 导航 | 相同目的地和离开结果 | navigation stack、tab/sidebar、edge-back | navigation bar/rail/drawer、system 与 predictive Back |
| 窗口布局 | 相同内容优先级，不要求像素相同 | size classes、iPad Split View、safe area、keyboard | window size classes、multi-window、fold/hinge、IME/insets |
| 控件与图标 | 相同动作、状态和业务含义 | 原生 controls、SF Symbols、Apple materials | Material controls、Material Symbols、tonal elevation |
| 字体与输入 | 相同信息完整性、朗读含义、遍历结果 | Dynamic Type、VoiceOver、Switch Control、hardware keyboard | `sp`/font scaling、TalkBack、D-pad/hardware keyboard |
| 主题 | 相同 semantic role 名称与品牌意图 | system colors/materials、tint、Apple high contrast | Material 3 roles、Dynamic Color 或明确 static fallback |
| 动效与反馈 | 相同因果状态、完成时机与不丢进度保证 | native push/sheet、Reduce Motion、克制 haptics | shared-axis/fade-through、Remove animations、Material feedback |

## 6. 已确认与未确认

**已确认——仅指题面明确给出的静态事实，并非独立源代码复核：**

- 产品意图是 `adaptive`，且允许平台原生差异。
- 固定 `390` 宽、JS 返回、吞 Back、`40x40` pressables、禁用字体缩放、literal colors、共享开关/图标、固定 tab 与无减弱分支的 `500ms` spring。
- 这些描述与两端最低目标尺寸、字体缩放、系统返回、语义主题、动效设置及自适应结构要求存在冲突。

**未确认：**

- 实际 iOS/Android target、React Native 与导航库版本、manifest、entitlements、Gradle/Xcode 配置及编译结果。
- 是否存在题面未提及的 `hitSlop`；因此真实 effective hit region 仍需源代码和运行态核验。
- VoiceOver/TalkBack label、role、value、announcement、focus/traversal 与 accessibility tree。
- 外接键盘、D-pad、Switch Control、焦点可见性和焦点恢复。
- safe area、system bar、cutout、IME、旋转、Split View、multi-window、foldable 和大字号实际布局。
- 各颜色的使用背景、对比度、dark/high-contrast 结果。
- 返回手势、predictive Back、动画流畅度、haptics、OEM 差异和真实单手可用性。
- 草稿持久化、离线 outbox、后台恢复、强制结束和进程重建后的进度保留。
- 任何商店审核、性能或真实设备质量结论。

## 7. 最小源代码、构建与运行态验证计划

1. **源代码检查：**定位 `width: 390`、`BackHandler`、`allowFontScaling`、`fontSize: 14`、literal colors、`hitSlop`、switch/icon imports、spring 参数、系统动效设置分支、window-class 分支及草稿持久化路径。  
2. **静态门禁：**运行仓库已有 typecheck、lint、unit/integration scripts；为 back routing、checkpoint/restore、theme mapping 和 accessibility-setting 分支补最小测试，不凭空假设脚本名称。  
3. **iOS build：**发现真实 workspace/project 与 scheme 后运行对应 `xcodebuild build/test`；构建成功只证明编译，不证明交互。  
4. **Android build：**运行项目实际 Gradle `lint`、unit test 与 debug assemble task；同样不能替代 Emulator。  
5. **`iOS Simulator: unverified locally`：**缺少 iPhone/iPad Simulator 运行；需覆盖 compact/regular、横竖屏、Split View、最大 Dynamic Type、VoiceOver、Reduce Motion、键盘、edge-back、后台/终止恢复。  
6. **`Android Emulator: unverified locally`：**缺少 phone/tablet/foldable Emulator 运行；需覆盖 multi-window、font scaling、TalkBack、predictive Back、Remove animations、键盘/D-pad、IME/insets 和 process recreation。  
7. **`iOS real device: no evidence`；`Android real device: no evidence`：**至少在代表性 iPhone/iPad 与 Android phone/tablet 上验证真实返回手势、单手可达性、haptics、OEM 行为、性能以及后台/强杀恢复。  
8. **发布判定门槛：**在两端构建、Simulator/Emulator 无障碍矩阵和代表性真机检查完成前，只能维持“静态阻断、运行态未验证”，不能宣称 native/adaptive release-ready。  

本轮未编辑任何文件，也未执行 source scan、build、截图、Simulator、Emulator 或真机验证。

