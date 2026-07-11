## 1. 证据级别、平台解析与设计判断

### 审查元数据

| 项目 | 结论 |
|---|---|
| 使用的 skill | `design-craft`，模式为只读 `critique` |
| 证据级别 | **L0 static / contextual prose**：有明确产品上下文和静态实现描述，但没有源码、截图、构建或运行时证据 |
| Resolved platform | **`adaptive`** |
| Platform source | 用户提供的 `PRODUCT.md` 摘要 |
| Platform confidence | **高**：明确为 React Native，同时发布 iOS 与 Android 商店，并覆盖手机、平板、Split View / multi-window |
| Style authority | 用户提供的 `DESIGN.md` 摘要；共享语义色彩角色与内容层级，但明确允许平台原生导航、控件、图标、材质和动效 |
| 设计系统判断 | 当前描述显示“共享语义层”被误实现成“共享像素和共享控件外观” |
| 运行时验证 | **未执行** |
| 截图验证 | **未执行；无截图 artifact** |
| 文件改动 | 无；本次为只读 benchmark |

### Design read

> **Reading this as:** 面向一线操作员和管理者的跨平台原生任务执行/复核界面，气质应可信、克制、稳定，首要优化目标是单手快速完成任务、被打断后无损恢复，以及在平板分屏中高效审核。

### 核心判断

这不是“小范围视觉不一致”，而是一个**平台契约与无障碍基础尚未成立**的问题。

当前实现将 adaptive 错误理解为：

- 固定一套手机画布；
- 固定一套导航；
- 固定一套控件外观；
- 固定字号和颜色；
- 然后同时打包到两个平台。

正确的 adaptive 应是：

- 共享业务意图、内容层级、状态机、语义 token 和结果；
- 根据 iOS、Android、窗口尺寸、输入方式和系统设置调整具体呈现与行为；
- 产品能力保持等价，但不要求像素相同。

**总体结论：当前静态证据不足以进入 iOS 或 Android 商店发布验收。**

---

## 2. iOS 与 Android 分平台合规结论

## iOS verdict：**Block / 不符合发布要求**

### 已由静态描述直接支持的阻断项

1. **原生导航栈和返回行为被自定义 JavaScript 顶栏替代**
   - 层级页面应由原生导航栈或能完整映射原生栈语义的 React Native 导航方案承载。
   - 当前实现可能破坏左边缘返回手势、交互式返回、转场连续性、状态恢复和无障碍导航语义。
   - “存在一个视觉上的返回按钮”不等于“保留了 iOS 返回契约”。

2. **`40x40` 主操作区域低于 iOS 最低 `44x44pt`**
   - 如果 `40x40` 只是视觉图标，而实际可点击区域通过 padding 或 `hitSlop` 扩大到至少 `44x44pt`，则可能合规。
   - 但当前描述称为 `40x40 pressables`，且没有扩大命中区证据，因此按现有证据判定不合格。

3. **固定 `fontSize: 14` 并禁用 font scaling**
   - 直接违背 Dynamic Type 发布要求。
   - 在大号辅助字号下无法保证任务内容、表单状态、主要操作和错误恢复路径可访问。
   - 这是 release blocker，不是视觉 polish 项。

4. **iPad / Split View 仍使用居中的 390pt 手机画布**
   - 不属于 adaptive layout。
   - 管理者的复核场景需要利用可用宽度形成主从栏、列表—详情或任务—证据结构，而不是在大窗口中央展示手机截图式界面。
   - iPad Split View 下还可能出现不必要留白、内容拥挤、弹层定位异常和外接键盘效率低下。

5. **平板继续使用完全不变的手机底部 tab bar**
   - Tab bar 在 iPhone 上可能合理，但不能无条件复制到所有 iPad 宽度。
   - iPad 上应根据 size class、窗口宽度和信息架构评估 sidebar、split view、tab/sidebar adaptation 或其他平台合适结构。

6. **500ms overshoot spring 没有 Reduce Motion 替代**
   - 对高频任务完成动作而言过长且过于强调。
   - “任务完成”应优先传达确定性和状态落盘，而不是展示弹跳。
   - 缺少 Reduce Motion 分支直接违反已声明的发布要求。

### 需要进一步确认的 iOS 问题

- “Cupertino-shaped switch”是否真正使用了原生 `UISwitch` 语义、状态、焦点和 VoiceOver value，静态描述无法证明。
- Web icon set 是否有正确的 VoiceOver label、selected state 和 RTL 镜像处理，未验证。
- `#777777` / `#FFFFFF` 的实际用途和对比度上下文未知，不能仅凭颜色字面值断言所有对比度失败；但可以确认它们绕过了语义动态色契约。
- safe area、键盘避让、home indicator、横竖屏、状态恢复均无证据。

---

## Android verdict：**Block / 严重不符合发布要求**

Android 侧问题比 iOS 更严重，因为明确存在系统 Back 被吞掉的行为。

### 已由静态描述直接支持的阻断项

1. **空 `BackHandler` 消费 Android Back**
   - 这是最高优先级阻断项。
   - 它破坏 Android 系统 Back、手势返回和 predictive Back。
   - 用户可能无法按系统预期退出当前层级、关闭临时界面或返回前一任务状态。
   - 对“被打断后不丢失进度”的产品而言，这会进一步降低用户对状态和导航的信任。
   - 必须移除无条件消费；只有在确实处理了一个明确、可解释的导航状态时才允许拦截，并应把事件交给导航层或系统继续处理。

2. **自定义 JavaScript 返回按钮不能替代系统 Back**
   - Android 的视觉返回按钮与系统 Back 是两个需要协调的入口。
   - Toolbar up action、系统 Back、预测返回动画和导航栈必须指向一致的层级结果。
   - 仅提供自定义顶部返回按钮不构成 Android 导航合规。

3. **`40x40` 主操作区域低于 Android 最低 `48x48dp`**
   - 如果实际命中区域没有额外扩展，则不合格。
   - 主操作之间还应保持足够间距，避免单手操作误触。
   - 当前没有 `hitSlop`、父容器命中区或最小间隔证据。

4. **固定字号并禁用 font scaling**
   - 直接违反 Android system font scaling 与 TalkBack 发布要求。
   - 应使用可缩放文本单位/React Native scaling 机制，并在大字号下允许内容换行和结构重排。
   - 不得为了保持单行布局而关闭缩放。

5. **Cupertino switch 在 Android 上发布**
   - 这是明显的平台移植痕迹。
   - Android 应使用 Material switch 的视觉、状态层、触摸反馈、颜色、禁用态、焦点态和无障碍语义。
   - 共享业务组件可以存在，但渲染层必须映射为平台正确的控件。

6. **同一套 web icon 在 Android 发布**
   - 应优先使用 Material Symbols 或与 Material 语义、光学尺寸、线宽和状态一致的图标映射。
   - Web 图标可能造成方向、返回、更多、关闭、分享、筛选等动作的语义漂移。

7. **Android tablet 仍使用手机底部导航**
   - Compact width 可使用 bottom navigation。
   - Medium / expanded width 应评估 navigation rail、drawer 或 pane-based layout。
   - 应按 window size class 和可用宽度决策，而不是按设备名称或固定像素判断。

8. **缺少 Remove animations 替代**
   - Android 系统关闭动画时，应使用即时状态变化或非常克制的 cross-fade。
   - 500ms overshoot spring 不符合平静、任务导向的产品定位，也没有系统设置分支。

### 需要进一步确认的 Android 问题

- predictive Back API / React Native navigation library 的具体接入版本未知。
- edge-to-edge、status/navigation bar、IME、display cutout、hinge inset 处理未知。
- Dynamic Color 是否是产品要求未知；但至少必须有语义 Material color roles 和稳定 fallback。
- TalkBack state description、traversal order、announcements 未验证。
- 多窗口、旋转、折叠姿态、D-pad、硬件键盘均未验证。

---

## 3. 优先级排序的发现

## P0：发布阻断——导航、无障碍和核心任务连续性

### P0.1 Android Back 被吞掉

**证据**

- 空 `BackHandler` 消费 Android Back。

**影响**

- 系统返回手势失效或行为不一致。
- predictive Back 无法正确预览目标。
- TalkBack、键盘或系统级导航路径可能与视觉按钮结果不一致。
- 用户可能被困在当前页面，或无法理解返回将发生什么。

**最小设计动作**

- 删除无条件消费 Back 的 handler。
- 让 React Navigation 或实际导航栈成为返回状态的唯一权威源。
- 仅在“存在未保存变更且返回会造成明确损失”等必要情况拦截。
- 若需确认离开，Android 使用平台合适的对话框/提示；如果任务已自动保存，则应直接返回并明确显示已保存状态。
- 验证 Toolbar up、系统 Back、手势 Back、predictive Back 都落到同一个目标。

**验收条件**

- Android 系统 Back 不被空 handler 吞掉。
- Android 新版系统可展示正确 predictive Back 目标。
- 返回过程中不会重复 pop、跳错页面或丢失任务进度。

---

### P0.2 iOS 原生导航栈被替代

**证据**

- 自定义顶栏和 JavaScript back 替代 iOS navigation stack。

**影响**

- 左边缘返回、交互式取消返回、转场连续性、标题层级和恢复行为无法得到保证。
- VoiceOver 用户可能缺少标准 Back button 语义。
- 自定义按钮和实际路由状态可能发生漂移。

**最小设计动作**

- 使用原生栈能力或能映射到原生导航控制器行为的导航方案。
- 页面标题、Back label、safe area、interactive pop 和状态恢复交给平台栈。
- 自定义品牌只应用于 tint、标题样式和允许定制的区域，不重写栈行为。

**验收条件**

- iOS 返回按钮和左边缘手势目标一致。
- 中途取消返回不会导致状态跳变。
- VoiceOver 正确识别返回按钮及其目标。
- 返回后任务草稿仍存在。

---

### P0.3 禁止文字缩放

**证据**

- `fontSize: 14` 固定。
- font scaling disabled。

**影响**

- VoiceOver/TalkBack 用户即使不直接依赖屏幕阅读器，也可能依赖更大字号。
- 任务说明、风险提示、证据说明和主要操作可能无法阅读。
- 关闭系统辅助功能以保护布局，是结构设计失败而非合理折衷。

**最小设计动作**

- 恢复 React Native 文本缩放。
- 将文本样式映射到语义角色，例如 title、body、label、metadata、status。
- iOS 映射 Dynamic Type text styles；Android 映射 Material type roles 和可缩放文本。
- 大字号时允许：
  - 标题换行；
  - 按钮高度增长；
  - 水平 action row 转为垂直；
  - metadata 从同一行拆分；
  - 平板 pane 调整最小宽度；
  - 内容滚动，但主要操作不能变得不可达。

**验收条件**

- iOS accessibility text sizes 下无核心信息裁剪或操作丢失。
- Android 至少在项目要求的最大 font scale 下无核心信息裁剪；建议把 200% 作为明确验收点。
- 不使用 `allowFontScaling={false}` 保护普通业务布局。

---

### P0.4 被打断后状态恢复没有任何证据

这不是已证明的实现缺陷，但它是产品首要目的，因此属于**必须验证的发布门禁**。

**需要证明**

- 应用切到后台、系统杀进程、来电/通知打断、旋转、窗口尺寸变化后，任务进度是否保留。
- “完成”动作在动画开始前、动画期间和动画结束后分别何时落盘。
- 网络中断时是否进入明确的 pending/syncing/failed 状态。
- 返回上一层是否会丢失未提交输入。
- 多窗口切换是否重新创建 screen 并丢失本地 state。

**设计原则**

任务进度不应依赖 screen component 是否仍挂载。关键草稿与完成状态应进入可恢复的业务状态层或持久化层，并显示明确状态：

- `已保存`
- `正在同步`
- `离线保存`
- `同步失败，点按重试`

不能只显示一次短暂动画或 toast 后假设状态可靠。

---

## P1：发布阻断——触控目标与输入遍历

### P1.1 主操作尺寸不足

| 平台 | 当前描述 | 最低目标 | 结论 |
|---|---:|---:|---|
| iOS | `40x40` | `44x44pt` | 不合格，除非实际命中区另有扩展 |
| Android | `40x40` | `48x48dp` | 不合格，除非实际命中区另有扩展 |

**设计动作**

- 不必把图标本身放大到 44/48；应扩大 pressable 的实际命中盒。
- Android 还应检查相邻目标间距，避免拇指误触。
- 图标按钮必须有可访问名称，不能只依赖图形。
- loading、disabled、pressed、focused、selected 状态需要完整。

### P1.2 外接键盘、Switch Control 和 D-pad 没有证据

**设计动作**

- 定义稳定、符合视觉顺序的焦点遍历。
- 不把焦点停在纯装饰图标或重复文本上。
- 保证主要动作、返回、tab/rail、表单、错误恢复都能通过外部输入完成。
- iPad 验证 external keyboard 和 Switch Control。
- Android 验证 hardware keyboard、D-pad 和 TalkBack traversal。
- 焦点进入双栏布局时，顺序应根据内容关系决定，而不是简单按 React 节点偶然顺序。

---

## P1：平台控件与图标不合规

### Switch

- 共享的是 `enabled/disabled/on/off` 业务状态，不应共享 Cupertino 外形。
- iOS 渲染平台原生 switch。
- Android 渲染 Material switch。
- 两端都必须提供：
  - accessible label；
  - role；
  - on/off value 或 state description；
  - disabled state；
  - focus/pressed state；
  - 足够命中区域。

### Icons

建议建立语义图标层，而不是让业务代码直接引用某一 web icon：

```text
IconSemantic.Back
IconSemantic.Close
IconSemantic.More
IconSemantic.Complete
IconSemantic.Warning
IconSemantic.Attachment
IconSemantic.Filter
```

映射为：

- iOS：SF Symbols 或项目批准的 iOS-native mapping；
- Android：Material Symbols；
- 仅品牌专有、平台不存在对应语义时，才共享自定义资产。

返回、前进、撤销、重做、分享、更多等高熟悉度图标尤其不应任意共享。

---

## P1：主题与颜色体系失效

### 已能确定的事实

- `#777777` 与 `#FFFFFF` 是 raw literals。
- 它们在两种 appearance 中复用。
- 这违背了 `DESIGN.md` 所描述的共享**语义角色**模式。

### 不能确定的事实

由于没有组件上下文，不能断言每个 `#777777` 或 `#FFFFFF` 用例都一定违反对比度标准。需要知道：

- 是前景还是背景；
- 所在 surface；
- 字号和字重；
- enabled/disabled 状态；
- 深浅模式；
- 高对比度设置；
- 是否叠加透明度。

### 设计动作

业务层只使用语义角色，例如：

```text
color.text.primary
color.text.secondary
color.text.disabled
color.surface.base
color.surface.elevated
color.border.subtle
color.action.primary
color.status.success
color.status.warning
color.status.critical
color.focus
```

平台映射：

- iOS：semantic system colors、system materials、tint、高对比度变体；
- Android：Material color roles、surface container roles、tonal elevation，以及必要的静态 fallback。

共享的是角色和状态含义，不是强制两端使用同一个十六进制值。

**验收条件**

- 无普通业务组件直接引用未解释的 raw color。
- light/dark/high-contrast 下角色齐全。
- disabled、pressed、focused、selected、error、success 状态都有明确映射。
- 对比度由实际前景/背景组合验证，而不是仅审查 token 名称。

---

## P1：Motion 不符合产品定位与系统设置

### 当前问题

- 任务完成使用 `500ms` overshoot spring。
- 没有 iOS Reduce Motion 或 Android Remove animations 分支。
- 产品定位是 calm、trustworthy、operationally native。
- 完成任务属于操作员可能频繁执行的核心动作，不适合长时间弹跳。

### 建议

默认状态：

- 在用户触发后立即更新可感知状态；
- 先确认状态提交，再进行非阻塞反馈；
- 使用约 `150–250ms` 的平台一致 transition；
- 以 opacity、颜色、check state 或轻微位置变化为主；
- 不使用明显 overshoot；
- 动画期间不锁住下一步操作。

iOS Reduce Motion：

- 使用短 cross-fade 或即时状态替换；
- 避免大幅位移、缩放和弹性过冲。

Android Remove animations：

- 即时完成状态变化，或使用极短、非位移型过渡；
- 不依赖 animation end callback 才落盘或导航。

**关键工程约束**

完成状态的业务提交不能绑定在动画完成回调上。动画被系统关闭、被中断或组件卸载时，任务仍必须正确完成或保持可恢复状态。

---

## P1：Adaptivity 失败

### 当前问题

- React Native screen 强制 `width: 390`。
- 平板只是居中手机 UI。
- phone、iPad、Android tablet 使用同一底部 tab。
- 没有 Split View / multi-window 结构适配证据。

### 设计动作：按窗口而不是设备名适配

避免：

```text
if (isTablet) ...
if (Platform.OS === ...)
width: 390
```

应基于：

- 当前 window width/height；
- size class / window size class；
- orientation；
- Split View / multi-window 实际可用尺寸；
- fold posture / hinge；
- 字号；
- input mode；
- safe area / system insets / IME。

### 建议结构

#### Compact phone

针对操作员单手任务：

- 单列任务流；
- 主要动作进入拇指可达区域；
- 顶部保留清晰任务上下文；
- 底部操作区不与系统手势区域冲突；
- 进度自动保存；
- 导航遵循各平台原生契约。

#### Medium width / 窄分屏

- 保持单列或有限双栏；
- 导航可切换为 rail/sidebar；
- 操作区根据可用宽度重排；
- 不因为“设备是平板”就强行双栏。

#### Expanded tablet / 宽分屏

针对管理者复核：

- 左侧：任务列表、队列或步骤目录；
- 右侧：任务详情、证据、验证状态和操作；
- 当前选择保持可见；
- 列表和详情的导航历史仍应符合平台；
- 外接键盘可在列表、详情和动作间稳定遍历。

390pt 可以作为内容栏的某个合理 `max-width` 参考，但不能成为整个 screen 的强制宽度。

---

## 4. 具体设计动作与 intentional parity matrix

### 最小纠正方向

1. 恢复两端原生导航和系统 Back。
2. 移除固定 390 宽度，建立基于可用窗口宽度的结构断点。
3. 恢复文字缩放，采用语义 typography roles。
4. 将主操作命中区提升到 iOS `44pt`、Android `48dp`。
5. 将 switch、icon、navigation、dialog/sheet 等拆成平台渲染层。
6. 把 raw colors 替换为共享语义角色，再分别映射平台主题。
7. 把完成动效缩短并去 overshoot，加入 Reduce Motion / Remove animations 分支。
8. 将草稿、完成和同步状态从 screen-local animation lifecycle 中剥离，确保可恢复。
9. 建立 VoiceOver/TalkBack/keyboard 的明确语义与遍历顺序。
10. 在 expanded width 提供真正的管理者复核结构，而不是居中手机画布。

### Intentional parity matrix

| 领域 | 保持共享 | iOS 必须适配 | Android 必须适配 |
|---|---|---|---|
| 产品目标 | 快速完成、验证、不丢进度 | 相同结果 | 相同结果 |
| 业务状态机 | 草稿、已保存、同步中、完成、失败、重试 | 共享语义 | 共享语义 |
| 内容层级 | 任务标题、步骤、证据、状态、主要动作优先级 | 可用 iOS 排版和列表结构呈现 | 可用 Material 排版和容器结构呈现 |
| 数据持久化 | 草稿和完成状态的 durable contract | iOS lifecycle/background 恢复 | Android lifecycle/process recreation 恢复 |
| 导航目的地 | 顶级模块和详情层级 | Navigation stack、tab/sidebar、edge-back | Navigation graph、top app bar、system/predictive Back、bar/rail/drawer |
| 返回结果 | 返回到同一个逻辑目标 | Back button + left-edge gesture | Toolbar up + system Back + predictive Back |
| Phone layout | 单列任务执行流 | safe area、iOS toolbar/tab | edge-to-edge/insets、Material app bar/navigation bar |
| Tablet layout | 管理者列表—详情/任务—证据结构 | iPad size class、Split View、sidebar/split view | window size class、rail/drawer、multi-window/fold posture |
| 控件状态 | on/off、selected、disabled、loading、error | 原生 iOS switch、picker、sheet、alert、context action | Material switch、picker、bottom sheet、dialog、snackbar |
| 图标语义 | Back、Close、Complete、Warning 等语义名称 | SF Symbols mapping | Material Symbols mapping |
| 色彩语义 | text/surface/action/status/focus roles | semantic system colors、materials、tint | Material color roles、tonal elevation、可选 Dynamic Color |
| Typography | title/body/label/metadata/status roles | Dynamic Type text styles | Material type roles + system font scaling |
| 触控结果 | 操作可可靠触发 | 至少 `44x44pt` | 至少 `48x48dp`，并检查目标间距 |
| 无障碍结果 | 标签、角色、状态、顺序、错误恢复一致 | VoiceOver、Switch Control、Dynamic Type | TalkBack、D-pad、font scaling |
| Motion intent | 清楚确认任务状态，不阻塞流程 | iOS transition、Reduce Motion、适度 haptic | Material transition、Remove animations、平台反馈 |
| 完成反馈 | 都应明确“任务已完成/已保存/待同步” | iOS-native announcement/feedback | TalkBack announcement、必要时 snackbar |
| 分析与埋点 | 同一业务事件语义 | 平台实现可不同 | 平台实现可不同 |
| 像素外观 | **不要求共享** | 平台可信优先 | 平台可信优先 |

---

## 5. 已验证与未验证声明

## 可确认——仅基于用户提供的静态描述

以下不是我通过源码独立复核，而是由本题给出的实现事实直接导出的判断：

- 产品平台被明确解析为 `adaptive`。
- screen 被描述为强制 `width: 390`。
- iOS 原生导航栈和 Android 系统返回被自定义 JavaScript 行为替代。
- Android 空 `BackHandler` 被描述为消费 Back。
- 主操作 pressable 被描述为 `40x40`。
- 文本被描述为固定 `fontSize: 14` 且禁止缩放。
- 两种 appearance 中存在 raw `#777777` / `#FFFFFF`。
- 两个平台使用同一 Cupertino-shaped switch 和 web icon set。
- 手机和平板使用同一 bottom tab。
- 完成动效是 500ms overshoot spring，且没有系统减少动画分支。
- 根据这些事实，可以静态判定当前方案违反多个明确的平台和无障碍设计契约。

## 未验证

以下均不能宣称已经通过：

### Source

- 没有读取 React Native 源码。
- 没有确认 `hitSlop` 或父容器是否扩大触控区域。
- 没有确认 navigation library、screen options 或 native-stack 配置。
- 没有确认 switch 是真正原生控件还是自绘控件。
- 没有确认 icon accessibility labels。
- 没有确认持久化、离线、同步或恢复实现。
- 没有确认 safe-area、IME、cutout 或 hinge 处理。
- 没有确认颜色的具体前景/背景用途和对比度。
- 没有确认 test IDs、accessibility roles、values、actions 和 traversal 顺序。

### Build

- TypeScript type-check 未运行。
- ESLint 未运行。
- React Native bundling 未运行。
- iOS `xcodebuild` 未运行。
- Android Gradle compile/lint/test 未运行。
- Store/Release configuration 未检查。

### iOS runtime

- **iOS Simulator: unverified locally**
- 未验证 iPhone compact width。
- 未验证 iPad full-screen。
- 未验证 iPad Split View。
- 未验证横竖屏。
- 未验证 Dynamic Type accessibility sizes。
- 未验证 VoiceOver。
- 未验证 Reduce Motion。
- 未验证左边缘交互式返回。
- 未验证外接键盘或 Switch Control。
- 未验证后台/进程终止后的任务恢复。

### Android runtime

- **Android Emulator: unverified locally**
- 未验证 phone compact width。
- 未验证 tablet expanded width。
- 未验证 multi-window。
- 未验证 foldable posture。
- 未验证 TalkBack。
- 未验证 font scaling。
- 未验证 Remove animations。
- 未验证 gesture navigation 或 predictive Back。
- 未验证 hardware keyboard / D-pad。
- 未验证进程重建后的状态恢复。

### Real devices

- **iOS real-device evidence: missing**
- **Android real-device evidence: missing**
- 没有真机手势、触控舒适度、haptic、OEM 差异、性能、内存压力、后台切换、热状态或持续任务证据。
- 因此不能宣称 operationally native、gesture-correct、performance-ready 或 store-release-ready。

---

## 6. 最小 source / build / runtime 验证计划

## A. Source validation

先做定向静态核查，不需要广泛扫描：

1. **平台与导航**
   - 确认使用的 React Native / Expo / navigation library 和版本。
   - 搜索 `BackHandler`、自定义 header、`goBack`、`beforeRemove`、gesture 配置。
   - 证明 iOS native stack、Android system/predictive Back 的实际调用链。
   - 检查是否有重复导航状态源。

2. **尺寸与 adaptivity**
   - 搜索 `width: 390`、固定 screen widths、`Dimensions.get()`、`useWindowDimensions()`。
   - 检查是否基于 window size，而非设备名称判断 tablet。
   - 检查 iPad Split View、Android multi-window、orientation 和 fold posture 下是否会重新布局。
   - 检查 bottom tab 是否有 rail/sidebar/drawer adaptation。

3. **Accessibility**
   - 搜索 `allowFontScaling={false}`、`maxFontSizeMultiplier`、固定高度、单行截断。
   - 检查 `accessible`、`accessibilityLabel`、`accessibilityRole`、`accessibilityState`、`accessibilityValue`、live region/announcement。
   - 检查外接键盘焦点和 Android D-pad focus。
   - 检查所有主要 action 的实际 hit rectangle，而不只看 icon dimensions。

4. **Theme**
   - 搜索 raw hex colors，区分 token 定义与组件内 literal。
   - 检查 light/dark/high-contrast role parity。
   - 对实际前景/背景组合计算对比度。

5. **Controls/icons**
   - 确认 switch 的底层实现。
   - 建立 semantic icon mapping，检查 SF Symbols / Material Symbols 分支。
   - 检查 dialogs、sheets、pickers、snackbars/alerts 是否平台正确。

6. **Motion/state**
   - 搜索 500ms spring、overshoot/bounce 参数。
   - 检查 iOS Reduce Motion 和 Android Remove animations 的读取方式。
   - 确认任务完成提交不依赖 animation completion callback。
   - 检查动画被取消、screen unmount、应用后台化时的状态一致性。

## B. Minimal build/static checks

优先使用仓库已有脚本；若项目没有统一脚本，再使用对应平台工具：

### Shared React Native

- TypeScript type-check。
- ESLint。
- 相关 navigation、persistence、adaptive layout 和 accessibility 单元测试。
- iOS/Android bundle generation。
- 检查 release build 是否存在平台条件分支遗漏。

### iOS build

最低限度：

- 列出 workspace/project 和 schemes；
- 使用 `xcodebuild` 编译 Debug Simulator target；
- 若存在测试 target，运行相关 unit/UI tests；
- 单独确认 Release configuration 能编译。

这里的 `xcodebuild` 通过只能证明编译，不证明导航手势、VoiceOver、Dynamic Type 或 Split View 正确。

### Android build

最低限度：

- Gradle compile / assemble debug；
- Android lint；
- unit tests；
- 如已有 instrumentation tests，运行导航和状态恢复相关用例；
- 确认 release variant 至少能配置和编译。

Gradle 通过同样不能证明 TalkBack、predictive Back 或 multi-window 正确。

## C. iOS Simulator validation

需要补齐，目前明确缺失：

> **iOS Simulator: unverified locally**

最小设备/窗口矩阵：

1. 一台 compact iPhone。
2. 一台 iPad full-screen。
3. 同一 iPad 的窄 Split View。
4. 同一 iPad 的宽 Split View 或等效 expanded state。

最小状态矩阵：

- 默认字号；
- 至少一个 accessibility Dynamic Type size，最终应覆盖最大目标；
- light/dark；
- Reduce Motion on/off；
- portrait/landscape；
- keyboard visible；
- VoiceOver traversal；
- external keyboard traversal；
- 前进、顶部 Back、左边缘 Back、取消交互式 Back；
- 任务进行中切后台再回来；
- 完成动画期间切后台或改变窗口；
- 离线、同步失败、重试；
- 长标题、长步骤、错误文本和本地化扩展。

## D. Android Emulator validation

需要补齐，目前明确缺失：

> **Android Emulator: unverified locally**

最小 profile：

1. 一台现代 API 的 compact phone，启用 gesture navigation。
2. 一台 tablet / expanded profile。
3. tablet multi-window。
4. 若产品承诺 foldable 支持，增加 foldable/hinge profile。

最小状态矩阵：

- system Back；
- Toolbar up；
- predictive Back；
- TalkBack traversal；
- 默认与放大 font scale，最终覆盖项目声明的最大比例；
- Remove animations on/off；
- light/dark；
- portrait/landscape；
- IME visible；
- hardware keyboard / D-pad；
- multi-window resize；
- 进程后台化与 activity/process recreation；
- 离线、同步失败、恢复；
- 长文本和 localization expansion。

## E. Real-device validation

在发布前至少补齐：

### iOS real device

- 边缘返回手势与取消；
- VoiceOver；
- Dynamic Type；
- Reduce Motion；
- 单手触控可达性；
- 键盘出现/隐藏；
- haptic 时机；
- 后台、中断、内存压力后的恢复；
- 较长现场任务中的性能、电量和热状态。

### Android real device

至少覆盖一台有代表性的 gesture-navigation 设备；更理想的是两个不同 OEM：

- system/predictive Back；
- TalkBack；
- font scaling；
- Remove animations；
- 触控目标和误触；
- IME/insets；
- OEM navigation bar 和 edge-to-edge 差异；
- activity/process recreation；
- 后台中断、同步和恢复；
- 持续操作性能。

### 最终证据要求

在没有以下三类证据前，结果只能保持为“静态审查未通过，运行时部分未验证”：

- iOS Simulator evidence；
- Android Emulator evidence；
- 两个平台具有代表性的 real-device evidence。

---

## 最终结论

当前概念的业务方向清楚，但实现没有兑现“trustworthy、calm、operationally native”的定位。最严重的问题不是视觉风格，而是：

1. Android 系统 Back 被吞掉；
2. iOS 原生导航栈被替代；
3. Dynamic Type/font scaling 被禁用；
4. 主操作触控目标不足；
5. 平板只是居中的固定手机画布；
6. 平台控件、图标和导航没有适配；
7. 完成动效缺少 Reduce Motion/Remove animations 分支；
8. “被打断后不丢进度”尚无任何 source 或 runtime 证据。

因此：

- **iOS：Block**
- **Android：Block**
- **Adaptive parity：未成立**
- **Store release readiness：不能声明**
- **Simulator / Emulator / real-device validation：全部缺失**

最小正确修复顺序是：**导航契约 → 文字缩放与触控目标 → 状态持久化/中断恢复 → window-class adaptivity → 平台控件和图标 → semantic theming → reduced-motion motion policy → 双平台运行时与真机验证。**
