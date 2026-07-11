# Dashboard 设计评审

**方法**：`design-craft / critique`，单上下文、只读评审。
**证据来源**：仅用户提供的产品背景和结构描述；未读取代码、设计稿、截图、DOM 或运行态。

## 1. 证据等级与评分区间

- **Evidence level：L0 static**
  - 有产品、用户、任务和页面结构描述。
  - 但没有截图；按 `design-craft` 的证据分级，不能升级为 L1，因为 L1 至少需要截图与产品上下文。
- **暂定 Product UI taste band：75–84 / 100，较可能落在 78–82**
- **成熟度区间：Clean but generic（整洁但通用）**
- **置信度：中低**

这不是对实际像素质量的评分，而是对**已描述的信息架构和产品适配度**的概念级判断。

主要加分项：

- 产品用户和任务明确。
- 企业控制台方向明确。
- 已有 KPI、趋势和明细表，基础信息对象并不缺失。
- 明确要求 token-backed color，说明设计系统意识正确。

主要扣分项：

- `12 equal KPI cards` 是典型的 **flat KPI grid / card soup**。
- 装饰性图表不回答运营问题。
- 通用 tips 与当前账户、异常和决策脱节。
- 页面组织围绕“有什么数据”，而不是“下一小时应该处理什么”。
- 在“扁平层级或 card soup 仍是主要问题”的情况下，不应评到 85 分以上。

由于没有视觉和运行态证据，以下内容不进入评分：真实排版、间距、色彩、对比度、响应式、表格可读性、交互状态、无障碍和性能。

---

## 2. Design read：这个 dashboard 应优化什么工作

> **Reading this as:** 面向内部电商收入运营人员的高密度 revenue operations command center，视觉上克制、冷静、低装饰，优化目标是让用户在三秒内识别未来一小时最值得处理的账户或 campaign，并立即理解原因、潜在收入影响和下一步动作。

它的核心工作不是“展示经营概况”，而是完成以下决策闭环：

1. **哪里出现异常或机会？**
2. **哪一个最紧急、影响最大？**
3. **为什么被判定需要关注？**
4. **数据是否足够新、足够可信？**
5. **我现在能采取什么动作？**
6. **处理后如何知道状态发生了变化？**

`design-craft` 里最适合的结构模式是：

> **Ops command center + decision surface**
> `lead risk object + supporting metric strip + exception queue + diagnostic chart + task-first table`

最有风险的产品原则是 **Purpose**：当前模块存在，但首屏还没有围绕用户的主要工作组织。其次是 **Simplicity**：这里需要删除的是无关模块和无差别强调，而不是降低必要的数据密度。

---

## 3. 主要层级与产品适配问题

### P1 — 12 个等权 KPI 制造了“重要性民主化”

所有 KPI 使用相同尺寸、位置和表面权重，会让用户自己承担优先级计算。

运营人员需要的不是同时阅读 12 个数字，而是：

- 哪个指标现在越过阈值；
- 哪个指标与目标或基线偏差最大；
- 哪个偏差能够归因到具体账户或 campaign；
- 哪个问题具有最高收入影响；
- 哪个问题现在可操作。

如果 12 个指标同权，风险、机会、总量、效率和诊断指标会互相竞争。用户可能需要先扫完所有卡片，再进入表格寻找原因，增加了 decision latency。

**产品影响**：延迟定位、误判优先级、频繁在 KPI 和表格之间来回映射。

---

### P1 — 页面没有明确的“attention queue”

用户的主任务是判断“下一小时处理谁”，但现有结构中没有明确说明：

- 哪些账户或 campaign 需要关注；
- 为什么需要关注；
- 严重程度如何；
- 预计收入风险或机会是多少；
- 数据更新时间；
- 是否已有负责人；
- 下一步动作是什么。

密集表格可能包含这些数据，但“数据存在于列中”不等于“优先级已经被表达”。

**产品影响**：dashboard 更像分析数据库入口，而不是运营工作台。

---

### P1 — 装饰性 area chart 不具备诊断价值

图表必须回答一个明确问题，例如：

- 收入损失从什么时候开始？
- 哪个账户贡献了主要偏差？
- 当前偏差是持续恶化、短时波动还是已经恢复？
- 与目标线、预算线或历史基线相比差多少？
- 某个异常是否与预算、流量、转化率或库存变化同期发生？

如果 area chart 只是展示总收入曲线，它会占据高级视觉位置，却不推动下一步决策。

**产品影响**：视觉显著性与操作价值不匹配，削弱首屏信噪比。

---

### P1 — 密集表格很可能是 schema-first，而非 task-first

仅知道表格“dense”，无法判断列结构；但在当前页面架构下，存在较高概率：

- 账户标识、严重程度和收入影响没有相邻；
- 诊断字段与行动字段分离；
- 默认排序不是按紧急性和影响；
- 行内没有解释“为什么被标记”；
- 用户需要横向扫描多个字段自行计算优先级；
- 筛选器与表格上下文脱节。

一个任务导向的表格应该先呈现：

`Identity → Status/Severity → Impact → Reason → Freshness → Owner → Next action`

而不是后端字段或报表字段的原始顺序。

---

### P1 — generic tips 右栏占据持续空间，却没有持续价值

“提高转化率”“关注预算消耗”“及时优化素材”一类泛化建议，无法帮助用户决定当前具体操作对象。

右栏是高成本位置，因为它：

- 持续压缩主表格横向空间；
- 容易制造第二条视觉扫描路径；
- 在没有选中对象时仍占据注意力；
- 如果内容不随账户、campaign 或异常变化，就没有上下文价值。

**产品影响**：降低数据区密度，却没有提供等价的决策价值。

---

### P2 — 缺少明确的时间语义与数据可信度

Revenue operations 特别依赖：

- 当前时间范围；
- 数据最新更新时间；
- 数据延迟；
- 与哪个基准比较；
- 目标、预算或阈值来源；
- 异常是否已恢复；
- 部分数据是否缺失。

如果 KPI 只有值和涨跌箭头，没有 period、comparison、threshold 和 freshness，数字会显得精确，却无法支撑可靠行动。

---

### P2 — 克制的企业风格容易被误解为“所有内容都一样轻”

“Dense but calm”不是降低所有对比度，而是：

- 大部分界面保持安静；
- 少数真正重要的异常具有清晰语义；
- 通过位置、排版、状态和内容建立层级；
- 不依赖彩色卡片或大面积背景制造优先级。

需要避免两种极端：

1. 12 个彩色 KPI 卡片造成噪声；
2. 所有模块都使用相同灰度和边框，导致异常也不突出。

---

## 4. 具体设计动作

## A. 将 `12-card grid` 改为 `lead + support + queue`

建议首屏结构：

```text
[Scope / time range / freshness / filters]

[Lead operational state]
需要关注 7 个账户 · 预计收入风险 ¥XXX,XXX · 3 个需在 30 分钟内处理

[Compact supporting metric strip]
GMV vs target | Spend pacing | Conversion variance | ROAS risk | Data freshness

[Exception queue / ranked attention list]
账户或 Campaign | 严重度 | 收入影响 | 触发原因 | 时效 | Owner | 下一步

[Diagnostic chart linked to current selection]

[Full task-first account table]
```

### Lead operational state

首屏最强对象不一定是“最大 GMV”，而应该是最能回答当前运营任务的状态：

- `7 accounts need attention`
- `¥428k revenue at risk`
- `3 campaigns likely to exhaust budget within 45 min`
- `2 anomalies currently worsening`

应同时显示：

- 时间范围；
- 相比目标或基线；
- 数据更新时间；
- 是否存在延迟或部分缺失。

这属于 **lead risk object**，而不是 marketing hero。字号可以有层级，但不应变成超大标题或品牌化首屏。

---

## B. 将剩余 KPI 压缩为 supporting metric strip

12 个指标不一定全部删除，但不应该全部成为独立、等权、带背景的卡片。

将指标分为三层：

1. **Lead**
   - 当前最关键的运营风险或机会。
2. **Supporting**
   - 4–6 个支撑整体判断的指标。
3. **Diagnostic**
   - 只有进入账户、campaign 或异常分析时才展示。

每个被强调的指标至少要回答：

- 当前值是什么；
- 相比什么；
- 比较周期是什么；
- 是否越过阈值；
- 数据更新时间；
- 点击后会过滤或解释什么。

使用 tabular numerals；数值、单位、delta 和上下文应形成稳定 anatomy。颜色只表达语义状态，不用于给 12 个卡片做差异化装饰。

---

## C. 在首屏放置 exception queue

这是最重要的产品结构调整。

队列应该默认按照产品定义的注意力优先级排序，例如：

```text
Priority = urgency × estimated revenue impact × confidence × actionability
```

这只是结构示例，实际公式必须由业务语义验证，不能由视觉设计自行假定。

每一项至少应该说明：

- **对象**：账户、店铺或 campaign；
- **状态**：critical / warning / recovering / monitoring；
- **影响**：收入风险、机会或目标缺口；
- **触发原因**：例如 spend pacing、CVR drop、库存、拒审、投放停止；
- **趋势**：恶化、稳定、恢复；
- **新鲜度**：最后更新时间和数据延迟；
- **Owner**：当前负责人；
- **下一步**：查看详情、调整预算、检查素材、联系负责人等。

目标验收条件：

> 用户应能在三秒内指出“现在先处理谁”，并能在不打开详情的情况下说明原因。

---

## D. 把 area chart 改造成 diagnostic chart

图表应该跟随当前选择的账户、campaign 或异常，而不是独立存在。

可能的诊断模式：

- 实际收入与目标/基线的时间序列；
- spend、traffic、CVR、revenue 的相关变化；
- 偏差贡献拆分；
- 异常前后时间窗口；
- 预算消耗速度和预计耗尽时间；
- 账户或 campaign 对总缺口的贡献排名。

具体要求：

- 标题直接写成问题或结论，而不是只写“收入趋势”；
- 显示目标线、阈值线或基准区间；
- 标记异常开始、预算变更、暂停、恢复等事件；
- 使用直接标签或明确图例；
- tooltip 要包含时间、值、比较对象和变化；
- 色彩来自语义 token；
- 不使用渐变填充制造“高级感”；
- 如果图表不能比表格更快回答问题，应删除或下移。

---

## E. 把 dense table 改为 task-first table

建议列顺序：

1. 账户 / campaign 标识；
2. 状态与严重程度；
3. 预计收入影响或机会；
4. 与目标/基线的偏差；
5. 主要触发原因；
6. 趋势；
7. 数据新鲜度；
8. Owner；
9. 下一步动作；
10. 次要元数据。

具体设计动作：

- 默认按 attention priority 排序，而不是名称或创建时间；
- 数值右对齐并使用 tabular numerals；
- 严重程度不要只依赖颜色，同时使用文本、图标或状态形状；
- 风险原因用短句表达，避免只显示内部错误码；
- 将次要 metadata 放入展开区、列自定义或详情面板；
- filters 与表格相邻，并显示当前 filter scope；
- 支持保存视图时，可提供诸如：
  - `Needs attention`
  - `High revenue impact`
  - `Unassigned`
  - `Data stale`
  - `Recovering`
- 行操作应使用明确的 verb-object 文案，而不是泛化的 `View` 或 `Action`。

---

## F. 移除 generic tips，改为 contextual inspector

右栏有两个合理方向：

### 方向 1：默认取消常驻右栏

让主表格获得完整宽度。选择一行后，再打开 contextual drawer 或 detail pane。

适用于：

- 用户主要进行跨账户快速扫描；
- 列宽和横向比较非常重要；
- 详情不是持续并排阅读。

### 方向 2：保留可折叠 contextual inspector

仅当右栏会随当前选择实时变化时保留，内容包括：

- 为什么被标记；
- 影响估算及置信度；
- 最近发生的关键事件；
- 推荐动作；
- Owner 和处理状态；
- 相关账户或 campaign；
- 数据来源和更新时间。

右栏不应出现与当前对象无关的运营常识。

---

## G. 采用 `Enterprise dense + Ops command center` 视觉语法

视觉策略应是：

- 紧凑但清晰的类型层级；
- tabular numerals 用于指标和表格数值；
- subtle dividers 优先于大量卡片背景；
- minimal elevation；
- elevation 只用于 overlay、selection 或真正的层级关系；
- 普通区域保持中性；
- warning、critical、success、info 使用语义 token；
- 禁止用红绿以外观装饰，且状态不能只依赖颜色；
- 同类组件保持统一 anatomy；
- 通过内容层级、字重、间距和对齐建立秩序，而不是阴影和大圆角；
- motion 只表达选择、过滤、更新和状态变化，保持 quiet and state-oriented。

建议状态 token 角色，而不是具体色值：

```text
surface/base
surface/subtle
surface/selected
border/default
border/strong
text/primary
text/secondary
text/muted
status/critical
status/warning
status/success
status/info
focus/ring
```

所有实际颜色必须来自项目 design tokens；此处不建议任何硬编码色值。

---

## H. 明确反馈与处理闭环

“发现异常”之后还需要表示处理状态：

- `New`
- `Acknowledged`
- `Assigned`
- `In progress`
- `Monitoring`
- `Recovered`
- `Dismissed`

如果运营动作发生在外部系统，也至少应支持：

- 标记已知；
- 分配 owner；
- 添加备注；
- 暂时 snooze；
- 查看变化是否恢复；
- 保留变更记录。

这能避免用户每次刷新后重新判断同一个问题，也能让 dashboard 从“观察面板”升级为真正的 operations surface。

---

## 5. 已验证与未验证声明

### 基于提示词可以确认

以下仅表示“提示词明确提供”，不是运行态验证：

- 产品表面是内部 revenue operations dashboard。
- 主要用户是需要在下一小时决定关注对象的电商运营人员。
- 当前概念包含 12 个等权 KPI 卡片。
- 当前概念包含一个被描述为 decorative 的 area chart。
- 当前概念包含一张密集账户表。
- 当前概念包含 generic tips 右栏。
- 目标视觉方向是 restrained enterprise console。
- 目标密度是 dense but calm。
- 不应采用 marketing hero treatment。
- 颜色应由 tokens 驱动。
- 没有提供截图、DOM、响应式、focus、hover、loading 或 error 证据。

### 可以作出的概念级判断

- 当前结构与用户的“一小时内确定优先对象”任务匹配不足。
- 等权 KPI 会造成扁平优先级。
- decorative chart 不应占据高级视觉位置。
- generic tips 的产品价值低于 contextual actions 或 selection inspector。
- 页面更适合采用 blocker-first、exception-first 的 decision surface。
- 该结构符合 `card soup` 的典型风险特征。

### 未验证，不应被表述为事实

- KPI 卡片实际是否视觉杂乱；
- 当前配色是否符合 token authority；
- 字体、字号、行高、间距和对齐质量；
- 页面是否真的使用阴影、大圆角或硬编码颜色；
- 表格实际列顺序、默认排序、筛选能力和行操作；
- 图表的数据、坐标、tooltip、legend 和实际诊断价值；
- 是否存在数据刷新时间、阈值和比较基线；
- 桌面、窄屏或移动布局是否溢出；
- hover、selected、focus-visible、keyboard navigation；
- loading、empty、error、partial、stale 和 permission states；
- 颜色对比度和非颜色状态表达；
- 屏幕阅读器语义；
- 大数据量下的表格、筛选和图表性能；
- 用户能否在三秒内识别最高优先级对象；
- 当前实现是否“可用”“无障碍”“响应式”或“已通过浏览器验证”。

**本次没有进行浏览器验证，也没有产生截图 artifact。**

---

## 6. 实施前的最小验证计划

以下是开始设计实现前应补齐的最小证据，不需要先做完整重设计。

### 1. 现场基线采集

至少获得：

- 当前桌面主视口截图；
- KPI、图表、表格和右栏的完整结构；
- 主视口尺寸；
- 实际 DESIGN/token authority；
- 当前数据范围和刷新时间；
- 一组具有代表性的真实或脱敏数据。

目的：把当前 L0 提升至至少 L1 contextual，并避免仅凭文字描述误判实际视觉层级。

---

### 2. 验证一个真实的一小时决策场景

让目标运营人员用当前 dashboard 完成一次具体任务：

> “现在是某个明确时间点，请指出未来一小时最需要处理的三个账户或 campaign，解释原因并说明下一步。”

记录：

- 找到第一个对象所需时间；
- 用户先查看哪个模块；
- 用户为了判断优先级读取了哪些字段；
- 是否需要在 KPI、图表和表格之间反复切换；
- 哪些信息缺失；
- 用户如何判断风险、影响和紧急程度；
- 操作最终在哪里执行。

这是判断 IA 是否正确的最小产品证据。

---

### 3. 确认 attention priority 的业务语义

实施 exception queue 前，必须确认：

- 什么条件代表“需要关注”；
- 紧急程度如何定义；
- 收入影响如何估算；
- 机会与风险是否使用同一排序逻辑；
- 数据延迟如何影响置信度；
- 哪些问题真正可操作；
- 已分配或已确认的问题如何降权；
- 恢复中的异常如何表达；
- 排序公式是否需要业务可解释性。

不要让前端通过任意权重自行创造业务优先级。

---

### 4. 确认模块与数据契约

为每个首屏对象建立最小数据清单：

- value；
- comparison；
- period；
- threshold；
- severity；
- reason；
- estimated impact；
- trend；
- freshness；
- confidence；
- owner；
- next action；
- handling state。

缺少这些字段时，应先调整产品契约，而不是只重排组件。

---

### 5. 低保真结构验证

使用代表性数据制作一个低保真方案：

```text
lead risk object
supporting metric strip
exception queue
selection-linked diagnostic chart
task-first table
contextual inspector
```

至少验证两个问题：

1. 用户是否能在三秒内指出最高优先级对象；
2. 用户是否能在十秒内解释其原因、影响和下一步动作。

如果不能，不应进入高保真视觉实现。

---

### 6. 定义必须覆盖的状态矩阵

实施验收范围至少应包含：

- normal；
- loading；
- empty；
- error；
- partial data；
- stale data；
- delayed data；
- permission-limited；
- no items requiring attention；
- many critical items；
- long account/campaign names；
- large positive/negative numbers；
- missing owner；
- missing impact estimate；
- recovering anomaly。

还需要定义 hover、selected、focus-visible、sort、filter、row expansion 和 drawer 的状态契约，但本次没有验证这些状态。

---

### 7. 定义最小运行态验证范围

实现完成后，最低验证应包括：

- 主要桌面运营视口；
- 一个较窄的桌面窗口；
- 表格长文本和大数据量；
- exception selection 到 chart/table/inspector 的联动；
- sort、filter、row action；
- keyboard focus walk；
- hover、selected、focus-visible；
- loading、empty、error、stale；
- semantic status color 的对比度与非颜色表达；
- 图表 tooltip、legend、axis 和容器缩放；
- 表格滚动和 sticky 行为；
- 代表性真实内容下的扫描时间。

是否需要移动端，应由真实使用环境决定；内部运营控制台不应为了形式完整强行做“桌面布局纵向堆叠”的移动版，但必须验证产品支持的最小窗口宽度。

---

## 结论

当前概念最大的问题不是视觉不够高级，而是**页面没有把“下一小时处理谁”提升为首要信息对象**。建议停止继续美化 12 个等权 KPI 卡片，先完成以下结构转换：

> **从 overview dashboard 转为 exception-first decision surface：一个主风险状态、一个紧凑指标带、一条排序清晰的 attention queue、一张用于解释当前选择的诊断图表，以及一张围绕影响和下一步动作组织的 task-first table。**

右栏只有在成为选中对象的 contextual inspector 时才应保留；否则应移除，把横向空间还给决策表格。视觉上保持 enterprise dense、低装饰和 token-backed semantic color，但关键异常必须通过位置、文字、数值上下文和状态语义明确突出，而不是让所有模块一起“安静”。