## 结论摘要

- **使用 skill**：`design-craft`
- **审查模式**：`critique`，只读静态审查
- **证据等级**：**E0/E1，提示词级静态证据**。只有产品上下文和静态实现描述；没有源码、构建产物、截图、无障碍树或任何运行时证据。
- **解析平台**：`adaptive`
  - 来源：用户明确给出的 `PRODUCT.md platform: adaptive`
  - 置信度：**1.0**
  - 含义：同一产品分别在 iOS/iPadOS 和 Android 上交付平台正确的原生体验，而不是两端像素完全一致。
- **总体判定**：当前概念在静态层面同时违反 iOS、Android 和 adaptive 的核心契约，**不具备发布就绪条件**。
- **首要风险原则**：`Familiarity`、`Flexibility`、`Context resilience` 和 `Platform trust`。界面虽然共享了视觉外观，但没有共享正确的产品结果，也没有保留两端的系统行为。

> **Design read**：将其理解为一个面向一线操作员和管理者的跨平台原生任务界面，气质应当可信、克制、操作化，优先优化单手快速完成、可靠保存进度，以及在平板分屏/多窗口中高效复核。

---

# 1. Evidence level、resolved platform 与设计判断

## 1.1 Evidence level

本次只能成立以下证据链：

| 证据类型 | 状态 |
|---|---|
| 用户给出的产品上下文 | 有 |
| 用户给出的静态实现描述 | 有 |
| `PRODUCT.md` 实际文件 | 未读取 |
| `DESIGN.md` 实际文件 | 未读取 |
| React Native 源码 | 未读取 |
| iOS 原生工程配置 | 未读取 |
| Android 原生工程配置 | 未读取 |
| 构建/测试输出 | 无 |
| 截图或录屏 | 无 |
| VoiceOver/TalkBack 无障碍树 | 无 |
| iOS Simulator | 未运行 |
| Android Emulator | 未运行 |
| iPhone/iPad/Android 真机 | 未运行 |
| 旋转、Split View、多窗口、折叠屏 | 未运行 |

因此，本报告中的“存在问题”是对**题面所述实现事实**的设计与平台规范判断；不是对实际仓库、二进制或运行时行为的独立复核。

## 1.2 Resolved platform

**Resolved platform：`adaptive`**

该产品同时通过 iOS 和 Android 商店发布，且题面明确使用 React Native 屏幕，因此适用：

- iOS/iPadOS 原生导航、触控、Dynamic Type、VoiceOver、Reduce Motion、Split View 规则；
- Android 系统 Back、predictive Back、Material 控件、font scaling、TalkBack、Remove animations、多窗口/折叠屏规则；
- adaptive shared-versus-adapted 契约。

这里的 adaptive 不是：

- 把同一个 `390px` 手机画布居中显示；
- 在两端使用同一个 Cupertino 控件；
- 在所有尺寸上保留完全相同的底部标签栏；
- 用 JavaScript 统一接管操作系统导航。

## 1.3 设计判断

产品承诺是“trustworthy, calm, operationally native”，但静态实现呈现的是：

1. **视觉一致性高于平台正确性**；
2. **手机固定画布高于可用空间适配**；
3. **自定义导航高于系统导航契约**；
4. **固定字号高于用户无障碍设置**；
5. **装饰性 overshoot 高于高频任务效率与减弱动态要求**。

这会产生明显的“跨平台壳层”感：两端看起来相似，但熟悉各自平台的用户不能依赖系统已经建立的返回、控件、字号和窗口行为。

---

# 2. 平台一致性判定

## 2.1 iOS / iPadOS

### 判定：**不符合，存在发布阻断级问题**

| 领域 | 判定 | 静态依据 |
|---|---|---|
| 导航 | 不符合 | 自定义顶部栏和 JS Back 替代 iOS navigation stack |
| 返回手势 | 高风险 | 未保留或未证明保留系统左边缘返回手势及交互式转场 |
| 触控目标 | 不符合 | `40x40` 小于 iOS 推荐的 `44x44pt` |
| 字体缩放 | 不符合 | 固定 `fontSize: 14`，且禁用 font scaling |
| 语义颜色 | 不符合设计系统要求 | 使用 raw `#777777`、`#FFFFFF`，绕过语义角色 |
| 深浅外观 | 未达到可审计状态 | 相同 raw colors 用于两种 appearance，无法证明对比度和语义正确 |
| 原生控件 | 部分可能符合外形，但整体策略不符合 | Cupertino switch 可能接近 iOS 外形，但是否使用原生语义、状态和 accessibility 未知 |
| 图标 | 不符合平台适配方向 | 使用统一 web icon set，而非经过 iOS 语义和视觉校准的 SF Symbols/平台映射 |
| iPad 适配 | 不符合 | 强制宽度 `390` 并居中，不是 size-class 驱动的结构适配 |
| 标签导航 | 高风险/不符合 adaptive 目标 | phone、iPad、各窗口宽度使用同一个 bottom tab |
| 动效 | 不符合可访问性要求 | 500ms overshooting spring，无 Reduce Motion 替代 |
| 外接键盘 | 未验证 | 没有 focus order、键盘操作或可见焦点证据 |
| 中断恢复 | 未验证 | 没有草稿保存、恢复、幂等提交或后台切换证据 |

### iOS 关键问题

自定义 JS Back 不只是“视觉上不像 iOS”。它可能失去或破坏：

- navigation stack 的层级语义；
- 左边缘 interactive pop gesture；
- 交互式返回过程中的取消与恢复；
- VoiceOver 对导航结构和返回按钮的合理表达；
- iPad 外接键盘返回/关闭命令；
- UIKit/SwiftUI 导航状态恢复；
- 平台转场的对称性和可中断性。

题面没有运行时证据，所以不能断言所有这些都已经损坏；但当前结构没有证明它们被保留，且从描述看实现方向与 iOS 原生契约相冲突。

---

## 2.2 Android

### 判定：**严重不符合，系统 Back 是明确的发布阻断项**

| 领域 | 判定 | 静态依据 |
|---|---|---|
| 系统 Back | 严重不符合 | 空 `BackHandler` 消耗 Android Back |
| Predictive Back | 不符合 | 自定义 JS 返回和消费系统 Back，绕过系统返回契约 |
| 触控目标 | 不符合 | `40x40` 小于 Android 推荐的 `48x48dp` |
| 字体缩放 | 不符合 | 固定 `fontSize: 14` 且禁用 scaling |
| Material 控件 | 不符合 | 两端共用 Cupertino-shaped switch |
| 图标 | 不符合平台适配方向 | 使用统一 web icon set，而非 Material Symbols/Android 语义映射 |
| 主题 | 不符合设计系统要求 | raw hex 颜色绕过 Material semantic roles |
| 深色/高对比 | 未达到可审计状态 | 同样的 raw colors 用于两种 appearance |
| 大屏导航 | 不符合 | tablet 仍使用固定 `390` 画布和不变的 bottom tab |
| 多窗口/折叠屏 | 不符合实现方向 | 没有 window size class、hinge/posture 或可用空间适配 |
| 动效 | 不符合可访问性要求 | 无 Remove animations 替代 |
| TalkBack | 未验证 | 没有 role、state description、traversal、announcement 证据 |
| 键盘/D-pad | 未验证 | 没有 traversal、焦点或激活行为证据 |
| IME/insets | 未验证 | 没有 edge-to-edge、IME、状态栏、导航栏 inset 证据 |
| 中断恢复 | 未验证 | 没有进程重建、后台恢复或草稿持久化证据 |

### Android 关键问题

空 `BackHandler` 主动消费系统 Back 是当前最明确的 Android 平台违约：

- 用户执行返回手势或返回键时，界面可能没有可见反应；
- 系统 predictive Back 无法表达目标页面或退出结果；
- 返回路径与任务层级不一致；
- TalkBack、键盘和系统级导航习惯无法获得统一结果；
- 可能出现“看似卡住”的状态，直接损害 operational trust。

应删除“无条件消费且不处理”的 handler。只有当页面确实存在未保存修改或受控流程时，才应进行状态感知拦截，并且必须：

1. 明确说明返回会造成什么影响；
2. 提供保存草稿、放弃或继续编辑；
3. 与 Android predictive Back 生命周期协同；
4. 不在没有实际处理逻辑时吞掉 Back。

---

# 3. 按优先级排列的发现

## P0：发布阻断

### P0.1 Android Back 被空 handler 消费

**类别**：Navigation / Platform conformance

**证据**：题面明确指出 empty `BackHandler` consumes Android Back。

**用户影响**：

- 系统返回可能表现为无响应；
- 任务界面可能形成导航陷阱；
- predictive Back 无法成立；
- 用户中断或需要退回核对时，无法预测是否保存了进度。

**最小设计移动**：

- 移除全局/无条件 Back 消费；
- 将任务详情挂入真实 navigation stack；
- Android 使用系统 Back/predictive Back 驱动同一导航状态；
- 如果存在未保存编辑，接入显式 dirty-state policy，而不是吞掉返回。

**接受条件**：

- Android gesture navigation 和三键导航均能正确返回；
- predictive Back 预览指向正确目的地；
- 有未保存内容时行为明确、可取消、可恢复；
- 没有修改时返回不出现额外确认；
- TalkBack 与硬件键盘触发相同的导航结果。

---

### P0.2 字体缩放被禁用

**类别**：Accessibility / Typography

**证据**：`fontSize: 14` 固定，font scaling disabled。

**用户影响**：

- 低视力用户无法使用系统字号偏好；
- 与题面列出的 Dynamic Type/font scaling 发布要求直接冲突；
- 固定高度控件中容易发生截断、重叠或操作不可达；
- 管理者在平板分屏中字体实际可用空间更小，风险进一步放大。

**最小设计移动**：

- 恢复 React Native 文本缩放；
- 用语义 type roles 代替全局固定 `14`；
- iOS 映射 Dynamic Type text styles；
- Android 映射 Material typography，并确保使用可缩放单位；
- 让行高、容器高度和操作区随内容增长；
- 不通过 `numberOfLines={1}` 或缩小字体掩盖布局问题。

**接受条件**：

- iOS accessibility Dynamic Type 尺寸下，核心信息和所有主操作仍可读取、触达；
- Android 至少覆盖常用大字号及发布要求所定义的最大 font scale；
- 不发生文字裁切、按钮消失、重叠或横向不可恢复溢出；
- 内容可滚动，但主要提交动作不能因缩放变得不可发现。

---

### P0.3 所有主操作只有 `40x40`

**类别**：Accessibility / Controls

**证据**：所有 primary actions 使用 `40x40` pressables。

**平台判定**：

- iOS：低于 `44x44pt`；
- Android：低于 `48x48dp`。

**用户影响**：

- 单手现场操作的误触率上升；
- 戴手套、移动中、疲劳状态或运动能力受限用户更难使用；
- 主要动作越频繁，累积操作成本越高。

**最小设计移动**：

- 可见图标不一定要变大，但可交互区域必须扩大；
- iOS interaction frame 至少 `44x44pt`；
- Android interaction frame 至少 `48x48dp`，并保留合理目标间距；
- React Native 中避免仅依赖不可审计的极小 `hitSlop`；布局、焦点框、波纹/高亮和可访问性边界应共同表达真实目标；
- 高频主动作优先使用带文本标签的完整按钮，而不是无标签小图标。

**接受条件**：

- 原生 accessibility frame/semantics bounds 达到平台要求；
- 相邻目标不会因扩大的 hit area 重叠；
- VoiceOver/TalkBack 聚焦区域与实际可激活区域一致；
- 单手主流程不要求精细瞄准。

---

### P0.4 没有 Reduce Motion / Remove animations 路径

**类别**：Accessibility / Motion

**证据**：完成转场为 500ms overshooting spring，没有替代方案。

**用户影响**：

- 与明确发布要求直接冲突；
- overshoot 可能引发前庭不适；
- 高频任务完成动作被 500ms 动画拖慢；
- “可信、克制”的产品定位被弹跳式反馈削弱。

**最小设计移动**：

- 建立共享的 semantic motion intent，例如 `taskCompletionFeedback`，而不是共享同一弹簧参数；
- 正常模式缩短并降低弹性；
- iOS Reduce Motion：使用短 cross-fade、颜色/状态替换或极小位移；
- Android Remove animations：立即状态变化，或在系统允许时使用非常短的 fade；
- 动画不能阻止下一步操作、保存或导航。

**接受条件**：

- 两端系统减弱/移除动画设置均能改变行为；
- completion state 在动画关闭时仍清晰可理解；
- 状态提交与持久化不依赖动画结束 callback；
- 连续快速完成任务不会排队播放动画。

---

## P1：高优先级平台与任务流问题

### P1.1 自定义顶部栏和 JS Back 替代原生导航

**类别**：Navigation / Platform trust

**问题**：

跨平台共享的应当是：

- 当前任务 ID；
- 层级和返回目的地；
- dirty/save 状态；
- 完成规则；
- 分析与业务事件语义。

不应共享成一个“看起来一样”的 JS 顶栏和返回实现。

**设计移动**：

- 共享 navigation intent 和 route state；
- iOS 使用 iOS navigation stack、原生 back affordance 和 edge-swipe；
- Android 使用 navigation stack、系统 Back/predictive Back 和 Material top app bar；
- 自定义品牌只进入 title treatment、tint、内容 hierarchy，不替换系统行为。

---

### P1.2 `width: 390` 居中不是 tablet adaptation

**类别**：Adaptivity

**证据**：一个 React Native 屏幕强制 `width: 390`，在平板居中。

**用户影响**：

- 管理者在 iPad Split View 或 Android multi-window 中无法利用可用宽度；
- 宽屏出现巨大空白，但信息仍挤在手机宽度内；
- 复核任务需要在详情、证据、状态、备注之间反复跳转；
- 窗口窄于 390 或字体放大时还可能产生裁切或水平溢出；
- 不能覆盖折叠屏、横屏和动态窗口调整。

**设计移动**：

按**可用窗口宽度和输入模式**建立结构断点，不按设备名：

- **Compact**：单栏任务执行；主要动作靠近拇指区；次要信息渐进披露；
- **Medium**：导航 rail/sidebar 与内容区分离，或使用更宽但仍受控的内容列；
- **Expanded**：master-detail 双栏；左侧任务列表/步骤，右侧详情、证据或审核面板；
- **非常窄的分屏**：回退 compact，而不是维持 390 固定宽度；
- **foldable**：考虑 hinge/posture，避免关键控件横跨折痕；
- 内容可设置阅读宽度上限，但**结构容器不能固定为手机宽度**。

**接受条件**：

- iPad 全屏、Split View 各档位；
- Android tablet 全屏与 multi-window；
- 横竖屏；
- 窗口实时 resize；
- 放大字体；
- 键盘出现和外接键盘输入；
- 核心功能均不消失、不裁切、不依赖设备型号分支。

---

### P1.3 tablet 上仍使用不变的 bottom tab bar

**类别**：Navigation / Adaptivity

bottom tab 并非在平板上绝对禁止，但“所有尺寸不变”说明没有基于空间和工作模式做判断。

**建议**：

- iPhone compact：原生 tab bar，适合 2–5 个顶层目的地；
- Android compact：Material navigation bar；
- iPad regular/expanded：根据信息架构选择 sidebar、split view 或原生可适配 tab/sidebar 模式；
- Android medium/expanded：navigation rail 或 drawer；
- 若管理者的核心任务是“列表 → 详情审核”，平板应优先 master-detail，而不是只替换底部导航形态。

导航目的地及选中状态保持业务等价，但容器与交互模式必须适配平台和宽度。

---

### P1.4 Cupertino switch 在 Android 上发货

**类别**：Controls / Platform familiarity

**问题**：

- Android 用户得到 iOS 视觉语法；
- Material 状态、波纹、颜色、尺寸、TalkBack state description 可能不完整；
- 同一视觉组件不等于同一可访问性结果。

**设计移动**：

- 共享：布尔值、标签、帮助文本、验证规则、analytics event；
- iOS：原生 iOS switch；
- Android：Material switch；
- 只有确实存在可证明的业务优势时才自绘，并且必须分别保留两端的触控、焦点、语义和状态行为。

---

### P1.5 统一 web icon set

**类别**：Controls / Iconography

**问题**：

web icon set 可能：

- 与 SF Symbols 或 Material Symbols 的线宽、光学尺寸和填充状态不匹配；
- 返回、更多、分享、编辑等系统语义不符合平台习惯；
- 未提供正确 accessibility label；
- 在 RTL、选中态和 Dynamic Type 环境中缺少平台行为。

**设计移动**：

建立 semantic icon names，例如：

- `navigation.back`
- `task.complete`
- `task.more`
- `attachment.add`
- `status.warning`

然后分别映射：

- iOS → SF Symbols 或经过批准的 iOS-native asset；
- Android → Material Symbols 或经过批准的 Android-native vector；
- 品牌性、领域性图标可以共享，但应分别校准像素网格、基线和状态。

图标本身通常应被隐藏出 accessibility tree，由旁边文本或控件 label 承担语义，除非图标就是唯一控件表达。

---

## P1/P2：主题与颜色

### P1.6 raw `#777777` 和 `#FFFFFF` 绕过语义 token

**类别**：Theming / Accessibility

`DESIGN.md` 已声明 shared semantic color roles，因此直接在组件中使用 raw hex 是对现有设计契约的绕过。

问题不只是“有没有 dark mode”：

- `#FFFFFF` 在浅色背景上可能不可见；
- `#777777` 的合规性取决于背景、字号、字重和状态；
- 同一值在 light/dark appearance 中无法表达不同语义；
- 无法支持 high contrast、系统颜色变化、disabled/pressed/focused/error 等状态；
- Android Dynamic Color 是否采用尚未决定；
- iOS Increase Contrast/Differentiate Without Color 是否支持未知。

**不能从题面直接断言** `#777777` 一定违反某个特定 WCAG 对比度，因为缺少背景和实际渲染尺寸；但可以确认它绕过了语义角色，且当前没有对比度证据。

**设计移动**：

组件只消费角色，例如：

- `surface.primary`
- `surface.secondary`
- `content.primary`
- `content.secondary`
- `content.onAccent`
- `border.subtle`
- `action.primary`
- `status.success`
- `status.warning`
- `focus.ring`

角色共享，平台值和 appearance 值可以不同：

- iOS 映射 system colors/materials/tint；
- Android 映射 Material color scheme/tonal elevation；
- 若 Android 使用 Dynamic Color，必须提供品牌认可的静态 fallback；
- light、dark、high-contrast 必须分别定义和测试。

---

## P2：任务连续性与状态反馈尚无证据

### P2.1 “被打断时不丢进度”没有实现证据

这是产品 purpose 的核心，不是可选 polish。目前没有以下证据：

- 字段是否增量保存；
- 应用进入后台时是否持久化；
- iOS memory pressure/termination 后是否恢复；
- Android activity/process recreation 后是否恢复；
- 离线提交、重试、冲突解决和幂等性；
- 完成动画中被打断是否已保存；
- 返回时 dirty-state 如何处理；
- manager 看到的是草稿、已完成还是待同步状态。

**建议状态模型**：

- `draft-local`
- `saving`
- `saved-local`
- `syncing`
- `synced`
- `sync-error`
- `completed-pending-sync`
- `completed-synced`

UI 应清楚区分“任务已完成”和“服务器已确认”。不要让 500ms 动画代替持久化反馈。

---

# 4. 具体设计方案与 intentional parity matrix

## 4.1 推荐的整体结构

### 操作员：compact phone

- 原生平台导航；
- 单栏、步骤导向；
- 当前步骤、任务状态和关键上下文保持清晰；
- 主要完成动作进入舒适的单手触达区域；
- 自动保存状态就地可见；
- 次要管理信息渐进披露；
- 中断后恢复到最近编辑位置，而不是只恢复到任务首页。

### 管理者：tablet / split-screen / multi-window

- 根据可用空间切换 master-detail；
- 一侧显示任务/步骤/异常列表；
- 另一侧显示详情、证据、备注和审核动作；
- 窗口变窄时平滑退回单栏；
- 外接键盘可按语义顺序遍历；
- 焦点不会在 pane 重构后丢失；
- 审核中途 resize 不丢选择状态或滚动上下文。

## 4.2 Intentional parity matrix

| 能力 | 保持共享 | iOS / iPadOS 适配 | Android 适配 |
|---|---|---|---|
| 产品目标 | 快速完成、复核、不中断丢失 | 相同结果 | 相同结果 |
| 领域模型 | task、step、evidence、completion、sync state | 共享 | 共享 |
| 内容层级 | 标题、状态、步骤、证据、操作优先级 | 共享语义 | 共享语义 |
| 业务规则 | 完成条件、权限、校验、保存与重试 | 共享 | 共享 |
| Analytics | 事件名称和业务含义 | 平台属性可追加 | 平台属性可追加 |
| 颜色 | semantic role names | system colors/materials/tint 映射 | Material color scheme/tonal elevation 映射 |
| Typography | 语义角色，如 body/label/title | Dynamic Type text styles | Material type roles + font scaling |
| 顶层导航目的地 | 信息架构、选中状态 | iPhone tab；iPad sidebar/split 视情况 | compact navigation bar；medium/expanded rail/drawer |
| 层级返回 | 返回目的地、dirty-state policy | navigation stack + edge swipe | system/predictive Back |
| 顶部栏内容 | 标题、状态和允许的操作 | native navigation bar | Material top app bar |
| Switch | 布尔状态、标签、说明 | iOS native switch | Material switch |
| Pickers/Dialogs/Sheets | 选择内容和业务结果 | iOS picker/sheet/alert 习惯 | Material picker/bottom sheet/dialog |
| 图标语义 | `back`、`complete`、`more` 等名称 | SF Symbols 映射 | Material Symbols 映射 |
| 触控结果 | 同样的任务动作 | 至少 `44x44pt` | 至少 `48x48dp` |
| 完成反馈 | 状态已经保存/完成的语义 | 克制的 iOS feedback，可选适当 haptic | Material state feedback，可选适当 haptic/snackbar |
| Motion intent | 完成、进入详情、错误提示的目的 | iOS transition 与 Reduce Motion | Material motion 与 Remove animations |
| Compact layout | 单栏、主要动作优先 | safe area / home indicator | system bars / IME / edge-to-edge insets |
| Expanded layout | master-detail 的信息关系 | iPad size class、Split View、sidebar | window size class、rail/drawer、multi-window/fold posture |
| Accessibility outcomes | label、role、value、order、announcement | VoiceOver custom actions/announcements | TalkBack state descriptions/custom actions |
| Keyboard | 语义 traversal 和可激活性 | iPad external keyboard conventions | keyboard/D-pad traversal |
| 离线与中断恢复 | 草稿、重试、冲突、幂等 | iOS lifecycle 恢复 | activity/process recreation 恢复 |
| Appearance | light/dark/high contrast 的业务语义 | iOS appearance/system contrast | Material light/dark/high contrast，Dynamic Color 可选 |
| 像素外观 | **不要求共享** | 平台正确优先 | 平台正确优先 |

### 关键原则

**共享的是意图、语义、状态和结果；适配的是导航、控件、尺寸、材料、图标、动效和系统行为。**

---

# 5. Verified 与 unverified claims

## 5.1 可视为题面已提供的静态事实

以下内容是用户明确提供的证据，可用于本次静态判定，但没有通过源码独立复核：

- 产品平台声明为 `adaptive`；
- 产品面向现场操作员和管理者；
- iOS 与 Android 商店均为目标；
- React Native 屏幕被强制为 `width: 390`；
- tablet 上该屏幕居中；
- 自定义 top bar 和 JavaScript Back 替代平台导航；
- Android 空 `BackHandler` 消耗 Back；
- 所有 primary actions 为 `40x40`；
- 文本固定为 `fontSize: 14`；
- font scaling 被禁用；
- 两种 appearance 中直接使用 `#777777` 和 `#FFFFFF`；
- 两端使用相同 Cupertino-shaped switch；
- 两端使用相同 web icon set；
- phone、iPad 和 Android tablet 使用相同 bottom tab；
- 完成转场是 500ms overshooting spring；
- 没有 Reduced Motion/Remove animations 替代。

基于这些题面事实，可以静态确认：

- `40x40` 不满足 iOS `44x44pt` 与 Android `48x48dp` 的目标；
- 禁用字体缩放与明确的 accessibility release requirement 冲突；
- 空 handler 消耗 Android Back 与 Android 系统返回契约冲突；
- 固定 390 宽度不构成 adaptive tablet/window layout；
- 无减弱动态替代与两端发布要求冲突；
- raw color 使用绕过了题面所述的 shared semantic color roles；
- Cupertino switch 和统一 web icons 不是正确的跨平台控件适配策略。

## 5.2 未验证，不能宣称通过或失败的内容

### 无障碍

- VoiceOver label、trait、value、hint、custom action 和 focus order；
- TalkBack role、state description、traversal 和 announcement；
- 实际 accessibility frame 是否因 `hitSlop` 扩大；
- Dynamic Type/font scaling 下的真实裁切和重排；
- Switch Control、Voice Access、D-pad；
- 外接键盘 Tab/Shift+Tab、Enter/Space、Escape/Back；
- 焦点可见性；
- 高对比模式；
- 不依赖颜色传达状态。

### 导航

- iOS edge-swipe 是否完全失效；
- 自定义导航与原生 stack 是否仍存在隐藏集成；
- predictive Back 的实际运行表现；
- deep link、恢复和 modal dismissal；
- dirty-state 返回确认；
- 返回时草稿是否保存。

### 布局

- safe area；
- status/navigation bar insets；
- Dynamic Island、home indicator、cutout；
- IME/键盘遮挡；
- 横屏；
- iPad Split View；
- Android multi-window；
- foldable posture/hinge；
- 极窄窗口；
- localization expansion；
- 长内容和真实数据。

### 主题

- `#777777` 与实际背景的对比度；
- `#FFFFFF` 的实际用途；
- light/dark 截图结果；
- high contrast；
- Android Dynamic Color；
- pressed、focused、disabled、selected、error 状态。

### 动效与性能

- 动画实际帧率；
- JS/UI thread 是否卡顿；
- spring 是否可中断；
- 完成动画是否阻塞交互；
- 系统动画设置是否被底层库间接处理；
- haptic timing；
- 低端 Android 和旧 iPhone 的性能。

### 可靠性

- 自动保存；
- 离线恢复；
- app background/foreground；
- iOS termination；
- Android activity/process recreation；
- 同步重试和冲突处理；
- 重复提交幂等性；
- 任务完成与服务器确认的区别。

---

# 6. 最小 source / build / runtime 验证计划

## 阶段 A：源码静态验证

目标是先确认题面描述与真实实现是否一致，并定位影响范围。

### A1. 平台和导航

检查：

- React Navigation、Expo Router 或其他 navigation 配置；
- 自定义 header 的注册方式；
- `BackHandler.addEventListener` 的所有调用点；
- handler 是否始终返回 `true`；
- iOS gesture、`gestureEnabled`、interactive pop 配置；
- Android predictive Back 配置和 target SDK；
- deep link、modal、nested stack；
- dirty-state 和保存状态如何影响返回。

建议搜索项：

```bash
rg -n "BackHandler|hardwareBackPress|gestureEnabled|headerShown|headerLeft|goBack|popTo|navigation"
```

### A2. 尺寸、字体和触控目标

检查：

```bash
rg -n "width:\\s*390|fontSize:\\s*14|allowFontScaling|maxFontSizeMultiplier|hitSlop|Pressable|Touchable"
```

需要确认：

- `40x40` 是视觉尺寸还是实际 accessibility/interaction bounds；
- 是否存在相邻 hit area 重叠；
- 是否有固定高度造成大字号裁切；
- 是否大量依赖单行截断；
- 屏幕是否使用 `useWindowDimensions`、window/size classes 或等价抽象。

### A3. 颜色和主题

检查：

```bash
rg -n "#777777|#FFFFFF|useColorScheme|Appearance|theme|colorScheme|semantic"
```

需要生成：

- raw color inventory；
- semantic token mapping；
- light/dark/high-contrast role 表；
- 每个文本状态的前景/背景组合；
- Android Dynamic Color 是否启用及 fallback。

### A4. 控件与图标

检查：

- Switch 的实际组件来源；
- iOS/Android 是否有平台分支；
- icon package、图标语义和 accessibility exposure；
- picker、dialog、sheet、snackbar/toast 是否也存在跨平台视觉替代。

建议搜索：

```bash
rg -n "Switch|Platform\\.OS|Platform\\.select|Icon|Svg|accessibilityLabel|accessibilityRole|accessibilityState"
```

### A5. Motion 与系统偏好

检查：

```bash
rg -n "Animated|spring|withSpring|duration|500|overshoot|ReduceMotion|reduceMotion|AccessibilityInfo"
```

需要确认：

- motion preference 的读取路径；
- 用户改变系统设置后是否动态更新；
- 完成状态是否依赖动画结束；
- animation disabled 时是否立即呈现最终状态；
- 是否有连续触发队列或重复提交风险。

### A6. 中断恢复

查明：

- task draft 存储位置；
- 本地持久化频率；
- server sync state；
- Android process death 恢复；
- iOS termination/scene restoration；
- 离线队列；
- retry/idempotency；
- completion transition 与持久化提交的先后关系。

---

## 阶段 B：构建与静态质量门禁

至少执行项目真实存在的命令，不应凭空假设脚本名称。React Native 常见候选包括：

```bash
npm test
npm run lint
npm run typecheck
```

或对应的 Yarn/pnpm 命令。

### iOS 构建

在真实工程 scheme 确认后执行等价的：

```bash
xcodebuild \
  -workspace <App>.xcworkspace \
  -scheme <Scheme> \
  -sdk iphonesimulator \
  -configuration Debug \
  build
```

验证：

- iPhone Simulator build；
- iPad Simulator build；
- deployment target；
- native navigation integration；
- accessibility 和 appearance API 是否正确链接。

### Android 构建

执行项目实际存在的 Gradle 任务，例如：

```bash
./gradlew assembleDebug
./gradlew testDebugUnitTest
./gradlew lintDebug
```

同时确认：

- `targetSdkVersion`；
- predictive Back 相关 manifest/configuration；
- Material theme；
- edge-to-edge/insets；
- release 与 debug 的行为差异。

**本次没有运行以上任何构建命令。**

---

## 阶段 C：iOS Simulator 验证

### 当前缺失证据

**没有任何 iOS Simulator 运行证据。**

最低覆盖：

1. iPhone compact portrait；
2. iPhone landscape；
3. iPad full screen；
4. iPad Split View 的窄、中、宽状态；
5. light/dark；
6. Dynamic Type 默认、大号、accessibility 大号；
7. Reduce Motion；
8. VoiceOver；
9. 外接键盘 traversal；
10. app background/foreground 和重新启动恢复。

关键断言：

- back button、edge swipe 和 navigation title 一致；
- 放大字号后无裁切和不可达动作；
- 触控目标至少 `44x44pt`；
- Split View resize 时结构重排，不是固定 390 宽居中；
- Reduce Motion 下没有 overshoot/大位移；
- VoiceOver 顺序、label、trait、value 和 completion announcement 正确；
- 任务编辑后中断可恢复；
- 自动保存状态与完成状态可区分。

---

## 阶段 D：Android Emulator 验证

### 当前缺失证据

**没有任何 Android Emulator 运行证据。**

最低覆盖：

1. compact phone；
2. Android tablet；
3. multi-window 窄/宽状态；
4. 至少一个 foldable profile；
5. gesture navigation；
6. 三键导航；
7. predictive Back；
8. light/dark；
9. 多档 font scale；
10. Remove animations；
11. TalkBack；
12. hardware keyboard/D-pad；
13. activity recreation 和 process death 恢复。

关键断言：

- Back 不被空 handler 吞掉；
- predictive Back 预览和提交目的地正确；
- 触控目标至少 `48x48dp`，目标之间不重叠；
- 使用 Material switch 和导航模式；
- expanded width 使用 rail/drawer/master-detail，而非固定手机画布；
- TalkBack 能读出 switch 状态、保存状态和完成反馈；
- Remove animations 下立即或温和完成状态变化；
- activity/process recreation 后草稿和当前位置恢复；
- IME、system bars、cutout、hinge 不遮挡主要操作。

---

## 阶段 E：真机验证

### 当前缺失证据

**没有 iPhone、iPad、Android phone、Android tablet 或 foldable 真机证据。**

在最终发布声明前，至少需要：

### iOS 真机

- 一台代表性 iPhone；
- 一台 iPad，尤其验证 Split View 和外接键盘；
- edge swipe 手感；
- 实际触控可达性；
- VoiceOver；
- Reduce Motion；
- haptic timing；
- 后台切换、系统中断、性能和内存压力。

### Android 真机

- 一台 gesture-navigation Android phone；
- 一台代表性 Android tablet，或至少真实大屏设备；
- 如果 foldable 是支持范围，至少一台真实折叠设备；
- predictive Back；
- OEM 导航差异；
- TalkBack；
- font scaling；
- Remove animations；
- process recreation；
- 低端设备 JS/UI thread 性能；
- 真实键盘、IME 和系统 inset 行为。

真机之前不能宣称：

- 手势体验已经正确；
- haptic 已经正确；
- 动画“流畅”；
- OEM 行为一致；
- 单手操作已经通过；
- tablet split-screen 已达到发布质量；
- 长时运行、热量、电量或低端机性能已经验证。

---

# 最小修复顺序

1. **恢复 Android system/predictive Back，移除空 Back 消费。**
2. **恢复字体缩放，改为两端语义 typography。**
3. **将主操作目标扩大到 iOS `44x44pt`、Android `48x48dp`。**
4. **为 Reduce Motion/Remove animations 建立真实替代路径。**
5. **移除固定 `width: 390`，以 window size/available space 驱动 compact、medium、expanded 结构。**
6. **将 phone/tablet 导航容器平台化：iOS tab/sidebar/split，Android navigation bar/rail/drawer。**
7. **将 Switch、图标、top bar 和系统反馈分别映射到 iOS 与 Android 原生语法。**
8. **将 raw hex 迁移到 shared semantic roles，并分别实现两端 appearance mapping。**
9. **验证草稿保存、后台中断、进程重建、离线同步和幂等完成。**
10. **完成 iOS Simulator、Android Emulator 和两端代表性真机验证后，再做发布就绪判断。**

最终目标不应是“iOS 和 Android 看起来完全一样”，而应是：**同一个任务、同一个状态、同一个完成结果，在两个平台上都让熟悉该平台的用户感到自然、可预测、可访问，并且在窗口和中断变化中不丢失工作。**