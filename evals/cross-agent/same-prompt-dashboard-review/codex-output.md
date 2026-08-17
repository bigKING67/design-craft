# Dashboard 概念评审

**方法**：`design-craft / critique`；目标按 Web `Operate` 型内部控制台评审。  
**Authority**：仅采用本提示中的产品上下文与风格约束。  
**执行边界**：只读；未编辑文件，未运行 route、浏览器、DOM 检查或截图验证。

## 1. 证据等级与分数带

- **证据等级：L0 static**——只有文字描述。虽然提供了用户与任务上下文，但没有截图，因此不能升级为 L1 contextual。
- **暂定 Product UI taste band：60–74 / Functional but ordinary**。
- 该分数带只评价描述中的**信息架构和产品适配度**，不是对实际视觉执行的评分。
- 基本模块齐备，说明它可能具备“查看数据”的能力；但平铺 KPI、装饰图表和通用提示没有形成面向下一小时的决策链。
- 没有渲染证据，无法给出可信的精确分数，也无法确认它是否达到 75–84 的 “Clean but generic”。

## 2. Design read

> Reading this as: 面向内部电商运营人员的 restrained、dense-but-calm revenue operations console，优化目标是让用户立即回答“哪个账户或活动最需要关注、为什么、影响多大、接下来做什么”；当前概念更像指标陈列页，而不是 operational decision surface。

它应优先优化：

1. **发现异常**：现在最需要处理的对象是什么。
2. **理解理由**：触发条件、变化幅度、阈值和数据时效是什么。
3. **判断影响**：潜在收入损失、机会规模或 SLA 风险有多大。
4. **完成动作**：负责人是谁，可以直接采取什么行动。
5. **保留证据路径**：从优先队列进入趋势、明细和原始账户数据。

## 3. 阻塞性层级与产品适配问题

未从当前证据确认 P0；以下五项是概念层面的 **P1 delivery blockers**。

### B1 — 平铺注意力，没有 operational focal point

12 张等权 KPI 卡把重复性误当成层级：高风险、机会、常规总量和诊断指标获得相同 surface weight。  
结果是用户先解读一组数字，而不是先看到需要处理的账户或活动。

### B2 — 决策上下文未进入概念合同

描述中没有明确时间窗口、账户范围、比较基线、阈值、数据更新时间或时区。  
缺少这些信息时，即使数字准确，用户也无法判断变化是紧急、正常还是已经过时。

### B3 — 图表承担装饰而非诊断

面积图被明确描述为 decorative，没有对应的 operational question、异常标注或明细路径。  
它占据视觉注意力，却没有缩短判断或行动时间，形成 false hierarchy。

### B4 — 主要工作对象被降级为“密集明细”

账户表很可能才是核心操作面，但概念没有规定优先级排序、决策列、负责人、影响、触发原因和 next action。  
“Dense”本身不是问题；没有 task-first anatomy 的密集才是问题。

### B5 — Generic tips 不符合 insight contract

常驻右栏挤压核心表格宽度，却没有与当前账户、异常或选择状态绑定。  
通用提示缺少 `entity + evidence + impact + owner + action`，属于 decoration disguised as guidance。

## 4. Concrete design moves

### M1 — 建立紧凑的 command/context band〔覆盖 B2〕

顶部只放页面身份、当前业务范围、时间窗口/时区、数据新鲜度和影响全局的筛选器；不做 marketing hero。  
范围变化必须立即反映到 KPI、队列、图表和表格，并持续显示当前过滤上下文。

### M2 — 改为 `lead + support + action queue` 构图〔覆盖 B1、B4〕

把首要风险对象或“待处理账户/活动”设为第一视觉焦点；其后是紧凑 supporting-metric strip，再进入明细证据。  
验收目标是：正常桌面首屏内，运营人员能在约三秒内指出首要对象及其紧急原因。

### M3 — 将账户表升级为 task-first exception queue〔覆盖 B4〕

优先列建议为：`Account/Campaign → Trigger/Status → Impact → Delta/Threshold → Age/SLA → Owner → Next action`。  
次要元数据后置、分组或进入详情；筛选器贴近表格；文本左对齐，数字右对齐并使用 tabular numerals；行操作必须可见且键盘可达。

### M4 — 把 12 个 KPI 分成 lead、support、diagnostic 三层〔覆盖 B1、B2〕

首屏仅保留真正改变优先级的指标，其余进入紧凑分组或 progressive disclosure。  
每个强调数字必须回答“哪个期间、相比什么、阈值是什么”；默认使用 neutral tokens，只有状态变化使用 semantic tokens，且不得只靠颜色传达。

### M5 — 将图表改为 diagnostic chart，否则删除〔覆盖 B3〕

先定义问题，例如：“过去 60 分钟什么变化导致当前收入风险上升？”再选择图形。  
保留时应有正确尺度、直接标签、阈值/异常注释，并能把用户带到对应的过滤队列；无法支持具体判断时应释放空间给主要工作对象。

### M6 — 删除常驻 generic tips rail，改为 contextual insight〔覆盖 B5〕

默认收回右栏宽度给队列和表格；确有价值时使用与当前选择绑定的 drawer 或 inline insight。  
每条 insight 必须包含具名对象、观测值或阈值、业务影响、负责人和可执行动作，否则不展示。

### M7 — 用密度梯度而非卡片装饰建立层级

使用一套安静背景、克制分隔线和有限 surface elevation；不靠大量圆角卡片、阴影或彩色边框组织页面。  
所有颜色必须来自 token role；决策型表格正文暂以 `14px / 1.4` 为可读性下限，`12–13px` 仅用于次要 metadata，并要求正常文本对比度达标。

### M8 — 在实现前定义 resilient state family

为 KPI、队列、图表和表格分别定义 `loading / empty / error / stale / permission / partial-data / long-content` 状态，说明保留哪些上下文以及如何恢复。  
同时声明主要和最小支持宽度、键盘顺序、focus-visible、hover/selected 状态、非颜色状态编码及窄宽度下的列降级规则。

## 5. Verified 与 unverified

### Prompt-established，但不是 runtime-verified

- 产品是内部电商 revenue operations dashboard。
- 主要用户要决定下一小时优先处理哪个账户或活动。
- 概念包含 12 张等权 KPI 卡、装饰性面积图、密集账户表和 generic tips 右栏。
- 风格方向是 restrained enterprise console、dense but calm、无营销 hero、颜色仅使用 tokens。
- 本次没有提供任何目标界面运行证据。

### Unverified，因此未计为已确认质量

- 实际首屏、滚动长度、布局轴线、间距、字体、边框、圆角和视觉噪声。
- KPI 的真实语义、阈值、比较周期和数据刷新机制。
- 图表尺度、标签、图例、tooltip、数据准确性及交互路径。
- 表格列顺序、排序、筛选、固定列、行操作和大数据量性能。
- token 是否真实存在并被一致应用，以及实际对比度。
- hover、focus、keyboard、screen-reader、loading、empty、error、stale 和 permission 行为。
- 长名称、极端数值、窄视口和响应式降级。
- 任何浏览器、截图、DOM、computed style 或真实运营任务表现。

**因此没有浏览器验证、响应式验证、可访问性通过或视觉验收通过的声明。**

## 6. 实现前的最小验证计划

1. **冻结 decision contract**  
   与主要运营人员确认优先级依据、触发阈值、影响口径、数据时效、负责人和允许执行的动作；使用 3–5 个真实或脱敏案例覆盖风险、机会和正常状态。

2. **取得当前 baseline**  
   在实际主要视口和最小支持视口捕获页面截图、首屏边界及完整滚动状态；同时检查 DOM/computed typography、spacing、token、表格列序和现有 decision path。若尚无页面，则用包含真实长度数据的低保真原型代替，但证据仍保持 L0/L1。

3. **验证关键任务，而不是审美偏好**  
   让代表性运营人员完成三步场景：找出首要对象、解释排序原因、进入或执行 next action。记录首次正确判断时间、误判点、所需滚动和无法解释的字段；未通过时先改 IA，不进入视觉精修。

4. **评审一个正常态和必要的异常态原型**  
   至少覆盖 normal、loading、empty、error/stale、permission 和长名称/极端数值；确认筛选范围在失败与恢复后仍然保留。

5. **设定 implementation entry gate**  
   只有在首要对象、排序理由、影响、owner 和 next action 都能在主要视口清晰形成一条决策链后再编码。实现后的真实浏览器、键盘、响应式和 visual review 是后续交付门禁，本次均未执行。

**结论**：保留“密集企业控制台”的方向，但应把页面从等权组件集合重构成 `context → priority → evidence → action` 决策表面；在这条链闭环前，不建议进入视觉 polish。

**Memory:** `user:global + project:design-craft` 命中 3 条；仅用于保持 evidence honesty 和 blocker-to-move 覆盖，不作为目标产品事实；候选 0，写入 0。

