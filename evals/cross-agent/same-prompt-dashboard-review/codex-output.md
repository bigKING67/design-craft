## 1. 证据等级与评分区间

- **评审模式**：`design-craft / critique`，仅基于提示词进行概念审查。
- **证据等级：L0 static**——只有产品描述和结构说明；没有截图、线框图、DOM、token、真实数据或运行态证据。虽然上下文较完整，但没有视觉载体，因此不能升为 L1。
- **概念评分区间：60–74 / 100，Functional but ordinary（可用但普通）**。
- **评分范围**：仅评估信息架构、任务聚焦和产品适配度，不是已渲染界面的完整 product UI taste score。
- **判断依据**：核心数据对象已经存在，但 12 个同权 KPI、装饰性图表和通用 tips 共同形成了明显的 **card soup / flat hierarchy**。
- **区间置信度：低到中**。实际字体、间距、对比度、token 使用、交互状态和响应式质量均无法计分。

## 2. Design read

> Reading this as：面向内部电商营收运营人员的 Web **Ops command center**，气质克制、密集但冷静，优化目标是在约 3 秒内识别未来一小时最需要处理的账户或 Campaign，理解“为什么现在要处理”，并直接进入下一动作。

它首先应是一个**异常分诊与行动界面**，其次才是经营概览。  
正确的阅读顺序应当是：

`当前范围与数据新鲜度 → 最紧急异常 → 影响和原因 → 负责人/时限 → 下一动作 → 支撑证据与完整账户列表`

而不是：

`十二个汇总数字 → 趋势装饰 → 数据表 → 通用建议`

## 3. 阻断性层级与产品适配问题

### B1 · P1：12 个同权 KPI 造成 flat hierarchy

所有指标具有相同面积和表面权重，会让常规总量、诊断指标和真正需要行动的风险看起来同等重要。  
这与“一小时内先处理谁”的任务相冲突；用户必须自行完成优先级计算。

### B2 · P1：主工作对象没有占据第一注意力

账户或 Campaign 才是可处理对象，但概念将密集表格置于 KPI 和图表之后。  
当前结构先展示“系统发生了什么”，再让用户寻找“具体该处理谁”，决策链路倒置。

### B3 · P1：装饰性面积图占用注意力，却没有明确分析问题

“面积图”是图形形式，不是业务问题。概念没有说明它用于发现趋势、阈值突破、异常加速还是账户比较，也没有说明如何从图表进入相关账户或 Campaign。  
因此它目前是 decoration disguised as analysis。

### B4 · P1：通用 tips 右栏不具备运营责任链

通用建议没有绑定实体、观测变化、阈值、业务影响、负责人和下一动作，会持续消耗横向空间与视觉注意力，却无法缩短处置时间。

### B5 · P1：缺少“为什么现在处理”的决策上下文

概念未定义优先级依据，例如预计收入影响、异常幅度、持续时间、置信度、SLA、负责人、数据新鲜度或处置权限。  
没有这些语义，即使视觉层级重做，也可能只是把错误的指标放大。

## 4. 八项具体设计动作

### M1 · 建立 page command/context band

在顶部提供紧凑的上下文带，而不是 hero：

- 当前时间范围、时区、账户/Campaign 范围；
- 数据更新时间与 stale 状态；
- 核心筛选条件和已应用筛选数量；
- “未来一小时”这一运营视角；
- 必要时显示告警规则或权限范围。

这些信息应靠近受其影响的数据，不应散落在卡片或页脚中。

### M2 · 将 card soup 改为 `lead + support + action queue`

把 12 张同权卡拆成三个层级：

- **Lead operational state**：一个最能回答“现在需要处理什么”的主指标或状态；
- **Supporting metric strip**：少量紧凑支撑指标；
- **Diagnostic metrics**：下沉到相应分析区域或按需展开。

每个被强调的数字必须同时回答：时间范围是什么、与什么比较、阈值是什么、是否需要行动。

### M3 · 把 exception queue 提到首屏核心位置

首屏主对象应是按行动价值排序的异常队列，而不是汇总卡片。每项至少呈现：

- Account / Campaign；
- 异常信号及触发原因；
- 预计收入或成本影响；
- 与基线或阈值的差异；
- 负责人、处置时限或 SLA；
- 明确的 verb-object 下一动作。

排序应围绕**影响 × 紧迫度 × 可行动性**建立，而不是只按抽象 severity 排序。

### M4 · 将图表从装饰改为 diagnostic evidence

先写出图表必须回答的问题，再选择图形，例如：

- 哪些异常正在相对基线加速？
- 哪个 Campaign 的收入风险在最近一小时扩大？
- 当前变化是全局问题还是单账户问题？

直接标记阈值突破和关键实体，并允许图表选择反向过滤异常队列或表格。若无法回答一个具体运营问题，则删除图表，而不是替换视觉样式。

### M5 · 把 dense table 改造成 task-first table

按运营决策顺序组织列：

`Identity → Status/Risk → Impact → Delta vs baseline → Reason → Owner/SLA → Next action`

同时：

- 文本左对齐，数值右对齐并使用 tabular numerals；
- 次要元数据采用 progressive disclosure；
- 筛选、排序和批量动作紧邻表格；
- 行动作可发现，而不是只藏在 hover 菜单；
- sticky 行为只在确实改善扫描时使用；
- 保持长名称、极值和窄宽度下的身份可辨识性。

### M6 · 删除 generic tips，或改为 contextual action panel

右栏只有在能够绑定当前选择或当前异常时才保留。每条 insight 必须包含：

`实体 → 观测变化/阈值 → 业务影响 → 建议动作 → 负责人`

否则删除右栏，让主队列和表格获得更多宽度，降低 attention tax。

### M7 · 使用 enterprise-dense 的视觉语法

- 默认使用 flat surface 和轻量 divider，减少重复卡框及 elevation；
- 通过位置、字号、字重和密度梯度建立层级，避免靠彩色卡片制造重点；
- 只使用 token-backed semantic color 表达 warning、critical、positive、neutral；
- 状态不得只依赖颜色，还需文本、图标或形状编码；
- 相同组件共享 anatomy、间距、圆角、状态与交互规则；
- 保持紧凑，但不要让所有区域具有相同密度和对比度。

### M8 · 在组件合同中定义 resilient states

在实施前明确 KPI、队列、图表和表格各自的：

- loading / empty / error；
- stale / partial data；
- permission denied；
- disabled / success；
- long label / extreme value；
- focus-visible / keyboard；
- narrow viewport / overflow。

错误状态应保留当前筛选和上下文，说明发生了什么，并提供本地、具体的恢复动作；不能退化成空白卡片或泛化的 “Something went wrong”。

## 5. 已验证与未验证

### 已由提示词确认

- 产品是内部电商团队使用的 revenue operations dashboard。
- 首要用户要决定未来一小时应关注哪个账户或 Campaign。
- 当前概念包含 12 个同权 KPI 卡、装饰性面积图、密集账户表格和通用 tips 右栏。
- 风格权威是克制的 enterprise console，要求 dense but calm。
- 颜色应来自 token，不应使用任意硬编码色。
- 本轮只进行了只读、提示词级 `design-craft` critique。

### 尚未验证

- 实际布局、首屏高度、网格、间距、字体、字号、圆角、边框和 elevation。
- 是否真的存在视觉噪声、低对比度、任意颜色或 token 违规。
- KPI 的具体业务语义、优先级、时间范围、基准、阈值和数据新鲜度。
- 表格列顺序、排序、筛选、行选择、批量动作、固定列及横向滚动行为。
- 图表数据、比例尺、轴、图例、tooltip、异常标记和数据正确性。
- tips 是否可能已经与选中实体或告警上下文关联。
- hover、active、focus-visible、键盘顺序及屏幕阅读器语义。
- loading、empty、error、stale、partial、permission 和恢复状态。
- 桌面窄宽度、移动端、缩放、长文本与极端数据表现。
- 浏览器运行态、DOM、computed style、响应式、可访问性和性能。

**本轮没有执行 browser validation，也没有生成或检查截图。**

## 6. 实施前最小验证计划

1. **取得真实表面证据**  
   提供当前桌面截图或带尺寸的线框图，并附一组脱敏但真实分布的数据：长账户名、极值、零值、多个同时告警、无数据和 stale 数据。

2. **确认运营决策模型**  
   与至少一名目标 operator 确认：什么条件意味着“一小时内必须处理”、如何排序、影响如何估算、谁负责、允许采取哪些动作、动作失败后如何恢复。

3. **建立指标与图表语义表**  
   为每个 KPI 和图表记录定义、时间窗口、比较基线、阈值、刷新频率、数据源和点击后的 detail path；不能说明决策用途的模块先移除。

4. **验证低保真 hierarchy prototype**  
   用真实数据制作 `command band → lead/support → exception queue → diagnostic chart → task-first table` 原型，进行最小 3-second test：用户能否快速指出首要实体、原因和下一动作。

5. **冻结状态与可访问性验收合同**  
   在编码前明确 responsive order、table overflow、focus order、键盘动作，以及 loading/empty/error/stale/partial/permission 的渲染、恢复动作和上下文保留规则。

6. **预先约定实现后的浏览器门禁**  
   实现后再使用真实浏览器检查桌面与窄 viewport、DOM/computed token、focus walk、keyboard、hover、表格溢出、图表 tooltip/legend，以及全部关键数据状态；在这些检查完成前，不应将方案提升为 L2/L3 或宣称视觉质量已经验证。