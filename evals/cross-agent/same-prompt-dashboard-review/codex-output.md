## 1. 证据等级与评分区间

**Evidence level：L0 static**

依据仅为产品背景和概念描述，没有截图、DOM、computed style、设计 token、真实数据或运行态证据。虽然提示词提供了用户和任务上下文，但按 `design-craft` 的评分口径，**仅有 prose description 仍属于 L0**。

**暂定 Product UI taste score band：60–74 / 100，Functional but ordinary**

更可能落在 **低到中 60 分段**，但不应给出更精确的单点分数。当前能够判断的是信息架构层面的明显问题，而不是实际排版、色彩、间距或组件完成度。

主要加分项：

- 已有 KPI、趋势、账户明细等基本运营信息。
- 稠密企业控制台的方向与内部运营用户相符。
- 账户表至少提供了从总览进入对象级决策的潜在路径。

主要扣分项：

- 12 个等权 KPI 形成典型的 **dashboard card soup**。
- 页面没有明确的第一关注对象和下一步动作。
- 装饰性图表不承担诊断任务。
- 通用 tips 右栏占用高价值空间，却不推动当前小时内的决策。
- 密集表格被放在视觉竞争激烈的页面中，但未说明是否按运营任务组织。

> 该评分只针对描述中可以确认的结构意图。实际界面可能因 typography、spacing、tokens、表格实现或状态设计而明显高于或低于此区间。

---

## 2. Design read：这个仪表盘应该优化什么

**Reading this as：一个面向内部电商 Revenue Operations 操作员的高密度、克制、可信赖的运营控制台，优化目标是在 3 秒内识别未来一小时最值得处理的账户或活动，并快速理解原因、影响和下一步动作。**

它不应该主要优化：

- 展示所有可用指标；
- 给管理者做泛化经营汇报；
- 通过大图表营造“数据很多”的感觉；
- 让每个模块都获得相同曝光；
- 用卡片数量表达产品能力。

它应该优化一个连续的决策链：

1. **现在最需要处理什么？**
2. **为什么它比其他对象更优先？**
3. **不处理会造成多大影响？**
4. **异常由什么指标或事件驱动？**
5. **我下一步能采取什么动作？**
6. **动作完成后，如何返回队列继续处理？**

最关键的产品原则风险是 **Purpose / Task focus**：当前结构展示了信息，却没有证明它能有效地把用户带到“下一小时要处理的对象”。

---

## 3. 主要层级与产品匹配问题

### P1：12 个等权 KPI 抹平了运营优先级

所有 KPI 使用相同卡片尺寸和表面权重，会向用户传达“这些数字同等重要”。但 Revenue Operations 的真实优先级通常取决于：

- 异常严重度；
- 潜在收入影响；
- 时间敏感度；
- 可操作性；
- 置信度；
- 是否已有人处理。

因此，账户数、收入总额、预算消耗、转化率、异常活动数等指标不应该天然等权。

问题不是 KPI 数量本身，而是缺少：

- lead metric 或 lead operational state；
- 与基线、目标或上一周期的比较；
- 风险含义；
- 指标与受影响账户之间的路径；
- 指标对应的可执行动作。

**用户影响：**操作员需要先阅读和解释 12 个模块，自己建立优先级模型，增加 decision latency。

---

### P1：缺少明确的“异常队列 / 下一动作”作为第一任务面

页面已有总览和明细，却缺少两者之间最关键的一层：**经过优先级排序的异常或机会队列**。

Revenue Operations 首页更应该首先呈现对象级结论，例如：

- `3 campaigns need action in the next 60 min`
- `Account A: spend accelerated 42%, conversion fell 18%`
- `Campaign B: budget will exhaust in approximately 47 min`
- `Account C: tracking signal missing since 10:32`

每条对象至少应该回答：

- 对象是谁；
- 发生了什么；
- 严重程度；
- 预计收入或预算影响；
- 已持续多久；
- 为什么现在需要处理；
- 推荐动作或进入诊断的路径。

**用户影响：**当前布局可能让用户知道业务总体发生了变化，却不知道应该先处理哪一行。

---

### P1：装饰性 area chart 没有承担分析问题

Dashboard 中的图表必须回答一个具体问题，而不是填充版面。一个泛化面积图通常存在以下风险：

- 图形面积制造视觉重量，但没有增加判断价值；
- 缺少异常阈值、基线或对照系列；
- 不清楚用户应从趋势中得出什么结论；
- 与账户或活动表没有联动；
- 图表占据高层级空间，却不能产生动作。

它至少需要回答其中一个问题：

- 异常从什么时候开始？
- 当前变化是全局现象还是单一账户导致？
- 收入、花费和转化之间在哪个时间点发生背离？
- 当前表现偏离基线或目标多少？
- 风险是在扩大、稳定还是恢复？
- 哪个对象贡献了主要变化？

如果图表不能帮助用户判断原因、紧迫度或处理顺序，它应下移、缩小，或被更有效的诊断视图替代。

---

### P1：密集账户表可能是数据仓库顺序，而不是任务顺序

“Dense table”本身不是问题。对于企业运营工具，高密度通常比过度留白更合适。风险在于表格是否围绕操作员的决策顺序组织。

任务优先的列序通常应接近：

1. Account / Campaign identity
2. Status / Severity
3. Trigger or anomaly
4. Estimated revenue impact
5. Time sensitivity / Duration
6. Current versus baseline
7. Owner / Handling state
8. Recommended next action
9. Secondary metadata

如果列顺序按数据库 schema、组织报表或数据可得性排列，用户就需要横向解码才能判断优先级。

还缺少的信息包括：

- 默认排序是否按 attention priority；
- 是否能筛选 `Needs action`、`Unassigned`、`High impact`；
- 行选择和详情打开方式；
- 批量操作是否必要；
- 行动作是否明确；
- 是否有 sticky header / identifier；
- 数字是否右对齐并使用 tabular numerals；
- 长名称、缺失数据和大数值如何处理。

---

### P1：generic tips 右栏与小时级运营任务不匹配

通用 tips 通常既不与当前对象绑定，也不随实时状态变化。它们会产生持续的视觉成本，却很少推动成熟操作员行动。

右栏只有在内容具有以下特征时才值得保留：

- 与当前选中账户或异常上下文相关；
- 能解释当前风险；
- 有置信度或证据来源；
- 能产生明确动作；
- 能显示 ownership、SLA、最近变更或处理记录；
- 能在没有建议时自然折叠，而不是填充通用文案。

否则应：

- 删除；
- 改为 context-sensitive action rail；
- 改为选中行后的诊断详情；
- 改为 attention queue；
- 或把稀有帮助内容放入按需 disclosure，而非永久占用页面宽度。

---

### P1：页面缺少可验证的注意力顺序

理想扫描路径应该是：

1. 当前风险或机会概况；
2. 最优先对象；
3. 影响及异常原因；
4. 可执行动作；
5. 全量账户表；
6. 历史趋势与辅助信息。

当前描述更接近：

1. 12 个等权数字；
2. 一张视觉重量较大的趋势图；
3. 大量表格数据；
4. 通用建议。

这是一种“数据模块排列”，而不是“决策流程编排”。

---

### P2：企业控制台可能被过度卡片化

受限于没有截图，无法确认视觉表现，但 12 个 KPI card 加图表、表格、右栏，很容易出现：

- 每个区域都有边框、圆角和背景；
- 多层嵌套卡片；
- 表面数量过多；
- section hierarchy 依赖容器，而不是 typography、spacing 和 alignment；
- 低风险信息与高风险状态共享相同 elevation。

对于 **restrained enterprise console**，更适合：

- flat canvas；
- 少量真实 section container；
- subtle divider；
- compact type；
- disciplined grid；
- minimal elevation；
- semantic status treatment；
- elevation 只保留给 overlay、selected state 或真正需要抬升的对象。

---

### P1：时间窗口和比较语义可能不足

“未来一小时需要关注什么”要求所有数据具有明确时间语义。单独显示数字不够，每个关键指标应回答：

- 数据时间范围是什么；
- 最新更新时间是什么；
- 与什么比较；
- 是否处于实时、延迟或部分数据状态；
- 阈值来自哪里；
- 当前变化是否具有统计或业务意义。

例如，不应只显示：

- `Revenue: ¥1.28M`

而应更接近：

- `Revenue pace: -11.8% vs expected`
- `Updated 2 min ago`
- `Main driver: Account A`
- `Estimated hourly exposure: ¥42k`

指标是否越高越好也不能仅依赖红绿颜色表达。

---

## 4. 具体设计动作

### Move 1：从 equal KPI grid 改为 `lead + support + action queue`

建议的首屏结构：

#### A. Compact context bar

放在页面标题附近，而不是做营销式 hero：

- 当前业务范围；
- 时间窗口；
- 时区；
- 数据更新时间；
- 账户/渠道筛选；
- refresh 或 auto-refresh 状态；
- 数据延迟或质量警告。

保持紧凑，不使用超大标题或夸张留白。

#### B. Lead operational state

只突出一个当前最重要的运营结论，例如：

- `7 accounts need attention`
- `¥186k estimated hourly revenue at risk`
- `2 campaigns likely to exhaust budget within 60 min`

lead object 应包含：

- 当前值；
- 与基线或目标的比较；
- 影响范围；
- 更新时间；
- 进入异常队列的动作。

这不是 marketing hero，而是 **operational focal point**。

#### C. Supporting metric strip

将原 12 个 KPI 缩减为约 4–6 个决策相关指标，以紧凑 strip 呈现：

- At-risk revenue
- Accounts needing action
- Budget pacing exceptions
- Conversion anomalies
- Tracking/data-quality incidents
- Unassigned alerts

每个指标至少提供：

- label；
- value；
- comparison；
- semantic state；
- relevant scope。

其余指标移入：

- secondary overview；
- 可配置 metrics；
- detail drawer；
- 或更低层级的分析区域。

#### D. Exception queue

紧接 lead state，显示最优先的 3–7 个对象。采用 **ops command center** 的处理方式：

- blocker-first hierarchy；
- short labels；
- strong state semantics；
- queue/action grammar；
- minimal decoration。

验收标准应是：

> 用户进入页面后，不打开任何二级页面，能在三秒内指出第一处理对象以及原因。

---

### Move 2：建立明确的 priority model，而不是只做视觉排序

排序不能只是设计师手工把某一行放在前面。应定义可解释的优先级模型，例如：

`Priority = impact × urgency × anomaly confidence × actionability`

界面不一定展示完整公式，但应该让用户理解排序理由：

- `Critical · ¥42k/hr exposure · 18 min remaining`
- `High · Conversion down 23% · Spend still accelerating`
- `Medium · Tracking delayed · Revenue impact unknown`

同时提供：

- 默认排序 `Recommended priority`；
- 用户可改为 `Revenue impact`、`Urgency`、`Newest`；
- 排序规则说明；
- 人工 pin、assign、snooze 或 resolve 的能力；
- 已处理对象不应持续占据首位。

这是 **agency** 和 **responsibility** 的要求：系统可以推荐，但不能让优先级变成不可解释的黑箱。

---

### Move 3：把 generic tips 变为 contextual action rail

右栏可以保留，但职责必须重定义。

选中某个异常或表格行后，右栏显示：

- 异常摘要；
- 关键证据；
- 影响估算；
- 最近相关变更；
- 当前 owner；
- 推荐动作；
- 进入账户详情；
- assign / acknowledge / snooze / resolve；
- 风险估算或推荐的不确定性。

推荐文案应采用 action-object grammar，例如：

- `Review budget pacing`
- `Open conversion breakdown`
- `Assign to channel owner`
- `Snooze for 30 minutes`
- `Mark tracking issue resolved`

避免：

- `View`
- `Confirm`
- `Take action`
- `Optimize now`
- `Tip`

如果没有选中对象，右栏应显示真正的 attention queue，或收起释放表格宽度，而不是显示通用教育内容。

---

### Move 4：将 area chart 改为 diagnostic chart

先定义问题，再选图。

可考虑的诊断视图：

#### 趋势背离

显示：

- revenue pace；
- spend pace；
- conversion；
- baseline 或 expected range；
- 异常开始时刻；
- deploy、budget change 或 tracking event 注释。

用于回答：

> 当前收入风险从何时开始，是否由花费与转化背离导致？

#### 贡献分解

显示：

- 哪些账户贡献了收入下降；
- 哪些活动贡献了异常消耗；
- Top contributors 与 long tail。

用于回答：

> 当前全局异常主要由哪些对象造成？

#### 异常时间线

显示：

- alerts；
- configuration changes；
- budget edits；
- tracking failures；
- operator actions。

用于回答：

> 异常发生前后发生了什么？

图表应该具备：

- 明确标题，最好直接写出问题或结论；
- 正确 scale；
- baseline / target；
- 直接标签或清晰 legend；
- tooltip；
- 时间范围；
- 数据更新时间；
- 与队列或表格的 selection 联动；
- 非颜色唯一的异常标记。

如果暂时无法定义诊断问题，宁可把图表降级到下方辅助区域，也不要让装饰性面积图占据主要注意力。

---

### Move 5：把账户表改为 task-first table

建议表格 anatomy：

| Account / Campaign | Priority | Trigger | Impact | Time sensitivity | Current vs baseline | Owner | Next action |
|---|---|---|---:|---|---:|---|---|

具体原则：

- identity、status、risk、impact、next action 在无需横向滚动时可见；
- 数字右对齐；
- 使用 tabular numerals；
- 状态不只靠颜色；
- 主要标识可在纵向滚动时保持上下文；
- 筛选器紧邻表格；
- 默认筛选优先显示 `Needs attention`；
- row action 明确且键盘可达；
- secondary metadata 后置或进入详情；
- selected row 与 contextual rail 有清晰对应关系；
- 表格的空、加载、错误状态出现在表格自身范围内。

不要把每一行变成独立重阴影卡片。高密度表格更适合：

- flat rows；
- subtle dividers；
- restrained selected surface；
- 明确 hover / focus-visible / selected 区分；
- 极少量语义颜色。

---

### Move 6：用 density gradient，而不是让所有区域同密度、同权重

建议建立密度梯度：

- **顶部：**少量、高价值、可快速判断；
- **中部：**异常队列和诊断信息，中高密度；
- **下部：**完整任务表，高密度；
- **深层：**历史数据、详细指标、配置与说明，按需展开。

这样既保持 enterprise console 的信息密度，也避免首屏成为视觉墙。

---

### Move 7：通过 token roles 控制克制感

提示词明确要求 **token-backed color only**，因此设计阶段应定义语义角色，而不是为每个模块挑颜色。

至少需要：

- `surface.canvas`
- `surface.base`
- `surface.raised`
- `surface.selected`
- `surface.muted`
- `text.primary`
- `text.secondary`
- `text.muted`
- `border.subtle`
- `border.strong`
- `status.critical`
- `status.warning`
- `status.success`
- `status.info`
- `focus.ring`
- `action.primary`
- `action.secondary`

颜色只承担：

- 状态；
- 选择；
- 操作；
- 风险；
- 必要的图表编码。

不要用不同 accent color 区分 12 个 KPI。优先通过：

- placement；
- type weight；
- number size；
- proximity；
- density；
- divider；
- state label

建立层级。

---

### Move 8：使用适合数据控制台的 typography 与 alignment

推荐方向，不是已验证规格：

- 页面标题克制，避免 hero scale；
- 表格与高密度内容以约 14px 产品字体角色为基准；
- section title 与 body 建立明确但不过度的差异；
- KPI 数字使用 tabular numerals；
- 币种、百分比、时间单位保持一致格式；
- 正负变化同时使用符号、文案和语义状态；
- labels 避免全大写和过度 letter spacing；
- 数值精度按决策用途控制，避免无意义小数；
- 时间统一明确时区和相对/绝对表达。

例如：

- `Updated 2 min ago · 14:32 CST`
- `-11.8% vs expected pace`
- `¥42k estimated hourly exposure`

比单独的大数字更有决策意义。

---

### Move 9：删除装饰性动效，保留 causal motion

这是内部运营控制台，不需要营销式进入动画。动效只应帮助表达：

- 队列重新排序；
- 筛选生效；
- 选中行与右栏关联；
- 状态由 open 变为 acknowledged/resolved；
- 数据刷新；
- 新异常进入；
- drawer / popover 的空间关系。

避免：

- KPI 逐张飞入；
- 图表反复绘制；
- 数字每次刷新都滚动计数；
- `transition-all`；
- 过度 scale；
- 高频脉冲告警。

高风险状态可以明确，但不应通过持续动画制造疲劳。

---

## 5. 已验证与未验证声明

### 可视为已知的输入事实

以下内容来自用户提供的概念描述，而不是运行态观察：

- 产品是内部电商团队使用的 Revenue Operations dashboard。
- 主要用户需要决定未来一小时应关注哪个账户或活动。
- 当前概念包含 12 个等权 KPI cards。
- 当前概念包含一个装饰性 area chart。
- 当前概念包含密集账户表。
- 当前概念包含 generic tips 右栏。
- 风格目标是克制、稠密但平静的 enterprise console。
- 不应使用 marketing hero treatment。
- 颜色必须来自 token-backed system。

### 可在概念层面成立的评审判断

基于上述结构描述，可以合理判断：

- 12 个等权 KPI 会削弱优先级表达。
- 装饰性图表与操作型仪表盘的主要任务不匹配。
- generic tips 不是最有效的永久右栏内容。
- 该页面需要从“指标总览”转为“决策与异常处理界面”。
- `lead + support + action queue` 比等权卡片网格更符合用户任务。
- 表格应按身份、风险、影响和下一动作组织，而不是按 schema 组织。

这些是设计建议，不是对现有实现行为的运行态证明。

### 未验证，不能作肯定声明的内容

以下全部未验证：

- 实际视觉质量和准确评分；
- spacing、grid、alignment、padding 和 component dimensions；
- typography、font weight、line-height 和 numeric alignment；
- 实际颜色、对比度和 token 使用情况；
- 是否存在硬编码颜色或 arbitrary values；
- 表格真实列顺序、排序、筛选和 pagination；
- 图表真实数据、scale、labels、tooltip 和 legend；
- hover、active、selected、disabled 状态；
- `:focus-visible`；
- keyboard navigation 和 focus order；
- screen-reader semantics；
- loading、empty、error、success、partial-data 状态；
- 数据刷新、延迟和 stale-data 行为；
- 表格长文本、大数值、缺失值表现；
- 响应式布局和窄视口降级；
- sticky header、sticky rail 或 overflow 行为；
- light/dark/high-contrast theme parity；
- 浏览器性能、表格虚拟化或图表渲染成本；
- 当前页面是否真的允许用户在三秒内识别首要对象；
- 推荐、优先级或风险估算是否可解释；
- 任何浏览器验证或截图验证。

**本次没有进行浏览器验证、截图验证、DOM 检查、focus walk 或 responsive run。**

---

## 6. 实施前所需的最小验证计划

目标不是先做完整研究，而是获得足够证据，将当前评审从 **L0 prose** 提升到至少 **L2 browser/contextual implementation evidence**，并避免按错误假设重构页面。

### A. 明确任务与数据语义

与产品或实际操作员确认以下最小问题：

1. 过去两周内，操作员最常见的前三类小时级动作是什么？
2. 什么条件使一个账户必须“现在”处理，而不是当天处理？
3. 优先级由 revenue impact、urgency、confidence、SLA 还是人工规则决定？
4. 每类异常对应的实际动作是什么？
5. 操作员处理完成后，如何 acknowledge、assign、snooze 或 resolve？
6. 哪些 KPI 是决策输入，哪些只是管理汇报指标？
7. tips 右栏目前是否被真实使用；如果使用，解决的是什么任务？

最低交付物应是：

- 3–5 个真实的 attention scenarios；
- 每个场景的 trigger、impact、urgency、next action；
- 明确的默认排序规则；
- 可解释的状态模型。

---

### B. 获取当前页面的静态与浏览器证据

实施前至少采集：

- 主桌面视口完整截图；
- KPI 区域截图；
- 表格首屏截图；
- 右栏展开状态；
- 当前 DOM 层级的关键片段；
- KPI、table、status、surface、color 的 computed-style/token evidence；
- 页面实际可用宽度和右栏宽度；
- 表格可见列、溢出及滚动方式。

需要核对：

- 是否真的所有 KPI 等权；
- 是否存在隐藏的层级或交互；
- 卡片是否过度依赖边框、阴影和圆角；
- 当前 design tokens 是否足以表达 proposed hierarchy；
- 现有组件能否通过 variant 调整完成，而不是重新建一套平行组件。

该步骤尚未执行，不能在本评审中宣称任何结果。

---

### C. 用真实或脱敏数据跑三个最小场景

至少验证：

#### 场景 1：一个明确高优先级异常

检查：

- 是否在三秒内被识别；
- 是否能理解原因和影响；
- 是否能直接进入下一动作。

#### 场景 2：没有需要处理的异常

检查：

- 页面是否仍然有用；
- 是否显示清晰的 all-clear 状态；
- 是否避免用空白卡片填充；
- 是否提供合理的下一检查时间或健康概况。

#### 场景 3：大量并发异常

检查：

- 队列排序是否稳定；
- 严重度是否可扫描；
- 表格是否仍可用；
- 右栏是否挤压关键列；
- 是否需要筛选、分组、分页或虚拟化。

最好再增加：

- 数据延迟或部分失败；
- 超长账户名称；
- 缺失影响估算；
- 已分配给其他 operator；
- 同一账户多异常。

---

### D. 在设计确认前做一张低保真结构稿

只验证信息顺序，不先投入视觉 polish。

建议低保真结构：

```text
[Page context / scope / time / freshness / filters]

[Lead operational state]
[Supporting metric strip]

[Priority exception queue] [Contextual action rail]

[Diagnostic chart or event timeline]

[Task-first account table]
```

用这张结构稿完成一次 task walkthrough：

> “现在是 14:30，你只有十分钟。请指出应该首先处理哪个账户、为什么，以及下一步做什么。”

接受条件：

- 用户三秒内找到首要对象；
- 十秒内说出原因和影响；
- 不需要先阅读全部 KPI；
- 不需要依赖通用 tips；
- 下一动作的位置和结果可预测。

---

### E. 实施前冻结最小组件与状态合同

至少定义以下组件责任：

- `OperationalLead`
- `MetricStrip`
- `ExceptionQueue`
- `ExceptionRow`
- `DiagnosticChart`
- `TaskTable`
- `ContextualActionRail`
- `DataFreshnessIndicator`

并为拥有状态的组件定义：

- default；
- hover；
- focus-visible；
- selected；
- disabled；
- loading；
- empty；
- error；
- success/resolved；
- stale/partial data；
- long-content；
- narrow viewport。

这一步应先建立合同，不代表状态已经在浏览器中验证。

---

### F. 确认最小响应式策略

即使主要使用桌面，也需要在实施前确认最低支持窗口宽度。至少定义：

- 宽屏：queue + table + contextual rail 如何分配空间；
- 中等宽度：右栏是否变为 drawer；
- 窄宽度：首要任务是否仍先于低优先级指标；
- 表格如何降级：列优先级、横向滚动、row detail 或 responsive table；
- sticky 元素是否遮挡内容；
- hover-only 行为是否存在替代路径。

不能简单地把桌面模块按原顺序纵向堆叠，因为这会把 12 个 KPI 继续放在核心任务之前。

---

## 实施前最低通过条件

在进入高保真实现前，至少应满足：

1. 已定义什么叫“未来一小时需要关注”。
2. 已定义默认 priority model 和排序理由。
3. 已确定 lead operational state。
4. 已将 12 个 KPI 分为 lead、support、secondary 三层。
5. 每个核心图表都有明确分析问题。
6. 表格列顺序按用户决策而不是 schema 排列。
7. 右栏已被删除或改为上下文相关的 action rail。
8. 已用至少三个真实数据场景验证信息结构。
9. 已定义 loading、empty、error、stale、selected 等状态合同。
10. 已取得当前界面的截图、DOM/token 证据，但尚不能把这些计划项写成已验证结果。

总体上，这个概念的问题不是“还不够漂亮”，而是**页面目前更像一个均匀展示数据的 dashboard，而不是一个帮助操作员分配下一小时注意力的 decision surface**。第一轮设计工作应优先重建 attention hierarchy 和 task flow，而不是先调整卡片样式、颜色或图表美化。