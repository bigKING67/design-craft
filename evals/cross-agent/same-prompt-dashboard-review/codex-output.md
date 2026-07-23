**方法与边界**

- 使用：`design-craft`
- 模式：`critique`
- Surface：`dashboard`，产品模式为 `Operate`
- Platform：`web`，仅按普通企业 Dashboard 默认推断
- Style authority：仅采用题述的“克制、密集但平静、无营销 Hero、颜色全部来自 Token”
- 本轮未读取项目、未编辑文件、未运行前端 route planner，也未进行截图、浏览器、DOM 或响应式验证

## 1. 证据等级与评分区间

- **证据等级：L0 static**
  - 虽然题述包含产品、用户和任务背景，但没有截图；按 `design-craft` 证据分级，仍属于“prose description only”，不能提升到 L1。
- **暂定概念评分区间：60–74 / 100，Functional but ordinary**
  - 更可能落在该区间的中低段。
  - 这是对**已描述的信息架构和产品适配度**的评分，不是对实际视觉成品的评分。
- 主要加分：用户、时效任务和风格约束清楚。
- 主要扣分：典型 `card soup`、没有明确的注意力队列、装饰性分析模块、表格尚未被定义为行动工具。
- 字体、间距、对齐、色彩、Token 执行、交互状态和响应式质量均未计为已验证能力。

## 2. Design read

**Reading this as：面向内部电商运营人员的 revenue-operations triage console，克制、精确、密集但平静，优化目标不是“浏览全部指标”，而是“在数秒内识别下一小时最值得处理的账户或活动，并理解原因、影响、负责人和下一步动作”。**

理想核心循环应是：

`发现异常 → 判断优先级 → 查看证据 → 执行/分派动作 → 确认状态`

当前概念更像“经营概览页”，而不是“下一小时行动决策面”。

## 3. 最重要的层级与产品适配问题

以下是**阻断设计批准的 P1 问题**，不是已经通过运行态复现的缺陷：

1. **12 张等权 KPI 卡形成 flat hierarchy**
   - 等尺寸、等表面权重意味着所有指标都在争夺注意力。
   - 运营人员无法立即区分“需要现在处理的风险”和“只是值得知道的总量”。
   - 数字若没有比较周期、阈值、业务含义和更新时间，也无法解释“为什么现在要行动”。

2. **缺少明确的 operational priority object**
   - 页面提供了指标和账户数据，却没有把“谁需要先处理”塑造成首要对象。
   - 对该用户而言，主对象应是透明排序的异常/行动队列，而不是 KPI 集合或概览图。

3. **面积图和 generic tips 属于非行动型信息**
   - 题述已将面积图定义为 decorative，说明它没有承担明确分析问题。
   - Generic tips 没有绑定实体、触发条件、业务影响、负责人或下一步动作，却占用了首屏注意力和横向空间。
   - 两者都属于“decoration disguised as analysis”的高风险区域。

4. **Dense table 尚未具备 task-first anatomy**
   - 高密度本身适合企业运营，但题述没有证明列顺序、默认排序和行操作是按决策路径组织的。
   - 如果不能连续扫描 `实体 → 状态 → 触发原因 → 影响 → 负责人 → 下一步动作`，它仍只是 data dump。

5. **关键运营语义与状态合同未定义**
   - 当前没有说明时间窗口、数据新鲜度、异常阈值、优先级规则、影响口径和 owner。
   - Loading、empty、error、partial、stale、permission、long-content、keyboard 和窄屏行为均未定义。
   - 对时效型运营台，“数据已过期”应是明确状态，不能和正常数据共用静默外观。

## 4. 八个具体 Design Moves

1. **建立 compact command/context band**
   - 首行只放页面身份、当前范围、时间窗口、筛选视图、数据更新时间和刷新/错误状态。
   - 让用户始终知道：“我正在看什么范围、什么时间的数据、数据是否足够新。”
   - 不使用大标题、欢迎语或 Hero 式留白。

2. **把 12 张 KPI 卡重构为 `lead + support` 层级**
   - Lead 不应是随意放大的营收数字，而应是 operational state，例如：
     - `需要关注的账户`
     - `Revenue at risk`
     - `未分派的高优先级异常`
     - `最久未处理的阈值突破`
   - 其余指标压缩为 4–6 项 supporting metric strip；诊断性指标移到下层或按需展开。
   - 每个强调指标至少提供：`当前值 + 比较对象/周期 + 阈值或方向含义 + freshness`。

3. **让同一张主表成为 ranked attention queue**
   - 默认视图为 `Needs attention`，`All accounts/campaigns` 作为次级视图，而不是再新增一张重复队列表。
   - 排序依据必须透明，例如：`严重度 → revenue impact → breach age`。
   - 避免无法解释的综合“AI priority score”；若使用评分，必须显示构成和排序理由。
   - 首屏验收标准：三秒内可以指出最高优先事项。

4. **采用 task-first table anatomy**
   - 推荐主列顺序：
     - `Account / Campaign`
     - `Status`
     - `Trigger`
     - `Business impact`
     - `Δ vs threshold`
     - `Last changed`
     - `Owner`
     - `Next action`
   - 文本左对齐；数值右对齐并使用 tabular numerals。
   - 筛选器紧邻表格；默认筛选应服务于 `critical / unowned / stale / revenue at risk`。
   - 行动使用明确的 verb-object 文案，如 `Assign owner`、`Review budget`，不要只依赖隐藏的 kebab menu。

5. **把图表降级为 selected-exception diagnostic**
   - 图表应回答一个命名问题，例如：“该 Campaign 为什么在过去 6 小时突破 ROAS 阈值？”
   - 绑定当前选中的异常，显示比较基线、阈值、重要事件和时间范围。
   - 如果图表不能改变优先级判断或下一步动作，则删除，而不是继续占据固定首页区域。
   - 不用渐变面积、装饰曲线或无解释的颜色制造“数据感”。

6. **删除 generic tips，必要时改为 contextual action rail**
   - 宽屏下，右侧区域只显示当前选中实体的：
     - 触发证据
     - 业务影响
     - 推荐/可用动作
     - Owner 与处理状态
   - 没有选择时可以保持关闭，以换取表格宽度。
   - 窄屏下改为 drawer/detail panel，不能永久挤压主表。
   - 每条保留的 insight 必须包含 `entity + observed change/threshold + impact + action/owner`。

7. **采用 enterprise-dense、低表面噪声的视觉处理**
   - 主内容保持 flat surface，以 subtle divider 和 spacing rhythm 分组；只为 overlay 或明确选中层使用 elevation。
   - 使用紧凑但可读的类型层级、稳定行高和统一数字基线。
   - 颜色只来自语义 Token，如 `text/*`、`surface/*`、`border/*`、`status/*`。
   - 不做指标彩虹；状态除颜色外还必须有标签、图标或形状。
   - “增长”不自动等于绿色、“下降”不自动等于红色，颜色必须依据业务含义。

8. **在编码前定义完整的 resilience contract**
   - 至少覆盖：loading、empty、error、partial data、stale data、permission、无 owner、长名称、极大/负数、窄屏和高行数。
   - 定义可见的 `focus-visible`、键盘排序/筛选/行选择/行操作路径。
   - 关键行动不能只在 hover 时出现；Tooltip 不能承载唯一信息。
   - 明确主表、上下文栏和筛选器在最小支持宽度下如何重排或折叠。

## 5. 已验证与未验证

**仅由题述确认：**

- 产品是内部电商团队的 revenue operations dashboard。
- 主要用户需要决定下一小时优先处理哪个账户或 Campaign。
- 概念包含 12 张等权 KPI 卡、装饰性面积图、密集账户表和 generic tips 右栏。
- 目标风格是 restrained enterprise console，颜色应完全 Token-backed。

**设计推断，而非运行态事实：**

- 等权 KPI 很可能削弱运营优先级。
- 装饰图表和 generic tips 很可能拖慢首屏扫描。
- 当前概念更接近 overview，而非 triage/action surface。
- 密集表格是否真是 data dump，仍取决于真实列、排序、筛选和行动设计。

**完全未验证：**

- 实际页面是否与题述一致。
- 真实视觉层级、字体、间距、对齐、边框、颜色、对比度及 Token 使用。
- KPI 定义、数据质量、刷新时延、阈值和业务影响口径。
- 表格排序、筛选、sticky 行为、行操作、选择和批量操作。
- 图表刻度、标签、Tooltip、数据真实性和诊断价值。
- Hover、focus、keyboard、screen reader、loading、empty、error、stale 和 permission 状态。
- 响应式、长文本、窄屏、性能及真实运营人员的任务完成情况。
- **本轮浏览器/runtime 验证：无。**

## 6. 实施前的最小验证计划

1. **确认运营优先级语义**
   - 与至少一名实际 operator 和数据 owner 确认：什么条件构成“需要下一小时处理”、严重度、影响金额、阈值、数据时效、owner 和允许执行的动作。
   - 若这些定义不清楚，应先停止布局实施；视觉设计无法替代优先级模型。

2. **取得当前基线证据**
   - 获取真实桌面截图、最小支持宽度截图，以及必要的 DOM/computed-style/Token 来源。
   - 记录实际路由、数据时间、viewport 和登录/权限状态。
   - 该步骤完成前不得把本次 L0 判断描述为现有页面审计。

3. **建立代表性数据与边界 fixture**
   - 覆盖正常数据、高优先级异常、空值、负值、超长名称、无 owner、数据过期、部分失败及大量行。
   - 用真实口径验证排序是否把正确实体放到首位，而不只是让界面“看起来紧急”。

4. **先验证低保真 decision flow**
   - 用包含真实字段和操作的线框/可点击原型测试 3–5 名代表性 operator。
   - 最低通过标准：
     - 3 秒内识别最高优先项；
     - 能说明触发原因、影响和 owner；
     - 能在不中断上下文的情况下找到下一步动作；
     - 不把普通波动误判为异常。

5. **形成实施验收矩阵**
   - 明确桌面与最小支持宽度、键盘顺序、focus、排序/筛选、行选择、rail/drawer、Tooltip，以及 loading/empty/error/stale/permission 的预期。
   - 同时完成 Token 角色映射，禁止在实施阶段临时引入硬编码状态色。
   - 实施完成后仍需单独进行真实浏览器、响应式和交互状态验证；本轮没有提供这些证据。