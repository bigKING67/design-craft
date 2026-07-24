## 1. 证据等级与分数区间

- **评审模式**：`design-craft / critique`
- **Surface route**：Web 桌面端、`Operate` 型 dashboard；本轮不是 L1+ 实现任务，因此未运行 frontend route planner。
- **实际采用的方向**：`Enterprise dense` + `Ops command center`
- **证据等级**：**L0 static**。只有产品说明和界面结构描述；没有截图、DOM、computed style、设计 Token 源码或浏览器证据。
- **暂定 Product UI taste score band**：**60–74 / 100，Functional but ordinary**
- **置信度**：低到中。该区间只评价概念层的产品适配、信息顺序和注意力控制，不评价实际排版、字体、间距、颜色、交互或响应式质量。
- **主要加分**：KPI、趋势和账户明细等基础数据对象齐全。
- **主要扣分**：结构更像“展示全部数据”，而不是“告诉运营下一小时先处理什么”。

没有足够证据判定 P0；以下五项均按 **P1 概念阻塞项**处理。

## 2. Design read

> Reading this as: 面向内部电商运营的收入运营决策台，以克制、紧凑、低装饰的企业控制台为基调，优化目标是在数秒内识别最高影响的账户或 Campaign 异常、理解原因，并进入下一步处置。

它首先是一个**分诊与行动界面**，其次才是经营概览；不应采用营销 Hero、展示型大图或均匀卡片陈列逻辑。

## 3. Top hierarchy / product-fit issues

1. **[P1] 12 张等权 KPI 形成 card soup**
   - 等尺寸、等位置、等表面权重意味着没有明确的 lead signal。
   - 用户必须自行在 12 个数字之间推导优先级，界面没有承担注意力排序责任。

2. **[P1] 核心工作对象被埋在概览之后**
   - 对“下一小时处理哪个账户或 Campaign”而言，异常对象或处置队列应是首要内容。
   - 当前 dense table 很可能是真正的工作面，却位于 KPI 和装饰图之后，且没有描述任务优先排序。

3. **[P1] Area chart 没有承担诊断问题**
   - 已被定义为 decorative，说明它消耗首屏注意力，却没有回答“哪里异常、何时开始、偏离多少、是否越过阈值”。
   - 这会把趋势展示误当成决策支持。

4. **[P1] Generic tips right rail 是伪洞察**
   - 通用建议没有绑定具体实体、变化证据、业务影响、负责人或下一动作。
   - 它长期占用横向空间，并与真正的异常和行级操作竞争注意力。

5. **[P1] 决策语义没有被概念明确**
   - 尚未定义时间窗口、对比基线、告警阈值、数据新鲜度、影响金额、负责人和下一动作。
   - 这是概念规格不足，不是对现有实现“缺失这些能力”的运行态断言。

## 4. Concrete design moves

1. **建立 page command/context band**
   - 在顶部集中展示业务范围、时间窗口、对比口径、关键筛选、数据更新时间和 stale 状态。
   - 筛选器应靠近它实际影响的数据，不要散落在卡片和表格之间。

2. **从 equal grid 改成 `lead + support` hierarchy**
   - 提升一个经过业务确认的 lead risk object，例如“收入风险最高的异常”或“即将超 SLA 的账户”。
   - 只将会改变分诊决定的指标保留为 compact supporting metric strip；其他 KPI 降级到可展开详情。
   - 所有强调数字必须回答“与什么时间段、基线或目标相比”。

3. **把 exception queue 放在决策面顶部**
   - 按已确认的业务规则排列需关注的账户或 Campaign，而不是使用无法解释的黑箱分数。
   - 每项至少包含：实体、触发原因、影响、紧急度、负责人、异常持续时间和下一动作。
   - 目标是让用户在约三秒内找到首要处理对象。

4. **将 dense table 重构为 task-first table**
   - 建议顺序：`Account/Campaign → Status → Trigger → Revenue impact → Delta vs baseline → Owner → Freshness → Next action`。
   - 数值右对齐并使用 tabular numerals；标识和文本左对齐；次要元数据进入展开层。
   - 排序、筛选和批量操作与表格贴近；行级动作必须明确、可发现且可通过键盘到达。

5. **把 decorative chart 改为 diagnostic chart，不能改就删除**
   - 图表必须回答一个命名问题，例如“收入下降从何时开始”或“哪些对象已越过风险阈值”。
   - 标注基线、阈值、异常区间和当前选择对象，并允许 queue/table selection 驱动图表上下文。
   - 如果看图不会改变下一步动作，则不值得占据首屏。

6. **移除 generic tips，或改为 contextual action rail**
   - 右栏只在选中异常对象时出现，结构固定为：`观察证据 → 业务影响 → 建议动作 → Owner/SLA`。
   - 如果无法提供实体级、可执行信息，应回收空间给异常队列和主表。

7. **采用克制的 token-backed enterprise treatment**
   - 使用紧凑字号、细分隔线、低 elevation 和稳定对齐轴；不要通过大量圆角卡片制造层级。
   - 颜色只绑定语义角色，如 critical、warning、success、neutral；不得为 KPI 分类任意着色。
   - 状态同时使用标签、图标或文本，不依赖颜色单独传达。

8. **在实现合同中补齐 resilience family**
   - 明确定义 loading、empty、error/retry、partial data、stale data、permission、长名称、极端数值和无负责人状态。
   - 同时规定窄视口信息降级、键盘顺序、`focus-visible`、tooltip 可达性和非颜色状态表达。

## 5. Verified versus unverified

### 由提示明确给出的事实，但未被运行态独立验证

- 产品是内部电商团队使用的 revenue operations dashboard。
- 主要任务是决定下一小时优先处理哪个账户或 Campaign。
- 当前概念包含 12 张等权 KPI、装饰性 area chart、dense account table 和 generic tips rail。
- 风格权威是 restrained enterprise console、dense but calm、无营销 Hero、颜色必须由 Token 支撑。

### 未验证，不能据此宣称优劣或完成

- 实际视觉层级、间距、字体、边框、圆角、对齐和信息密度。
- KPI 的真实口径、时间范围、比较基线、阈值、数据新鲜度及业务正确性。
- 图表比例尺、轴、标签、legend、tooltip、异常标记和数据准确性。
- 表格列顺序、排序、筛选、固定列、行操作、溢出及长数据表现。
- Token 是否真实使用、语义颜色和对比度是否合格。
- Hover、focus、active、disabled、loading、empty、error 和 permission 状态。
- 键盘导航、焦点顺序、屏幕阅读器语义和非颜色状态表达。
- 窄视口、移动端、缩放、长文案、极端数值及真实数据表现。
- 页面性能、图表重绘、表格滚动或任何浏览器行为。

**本轮没有打开浏览器、没有检查 DOM、没有执行响应式或状态验证，也没有编辑任何文件。**

## 6. 实现前最低验证计划

1. **建立当前状态基线**
   - 获取至少一张代表性桌面截图、页面 DOM/组件结构和实际 Token 来源。
   - 确认 12 个 KPI、图表、表格和右栏在真实页面上的位置、占用面积和数据关系。

2. **确认运营决策合同**
   - 与实际运营确认三个问题：什么情况必须在一小时内处理、优先级如何计算、用户能从页面直接执行什么动作。
   - 明确阈值、影响口径、负责人、SLA、更新时间和默认排序；在此之前不要自行发明 lead metric。

3. **使用真实形态数据制作低保真决策原型**
   - 覆盖正常、严重异常、stale、缺失字段、无负责人、长名称、极端金额和大量行。
   - 至少设计 desktop 主布局和一个受限宽度布局，以及 loading、empty、error、partial-data 四类关键状态。

4. **执行最小任务测试**
   - 让 2–3 名目标运营完成：找到最高优先级对象、解释为什么、进入或分配下一动作。
   - 建议验收基线：约三秒内识别首要对象；无需横向解码即可说明触发原因、影响和负责人。
   - 若多人选择不同对象，先修正优先级语义，不要先做视觉抛光。

5. **编码前冻结验收矩阵**
   - 明确需要验证的 desktop/narrow viewport、真实数据 fixture、状态清单、键盘路径、焦点和对比度规则。
   - 实现后必须再通过真实浏览器截图、DOM/computed-style、状态与响应式检查；当前 L0 评审不能替代这些证据。