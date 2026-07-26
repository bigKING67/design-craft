## 1. 证据等级与分数带

- **评审模式**：`design-craft / critique`，Surface mode=`Operate`
- **证据等级：L0 static**
  - 仅有文字描述。
  - 虽然已知产品、用户和任务语境，但没有截图，因此不能升级为 L1 contextual。
- **暂定 Product UI taste 分数带：60–74 / 100，Functional but ordinary**
  - 该分数只评价已描述的**信息架构与产品适配性**，不是对真实视觉实现的评分。
  - 已知结构具备 KPI、趋势、明细和辅助信息，基本模块齐全；但仍是典型的 `card soup + decorative chart + data dump + generic insight`，没有形成运营决策面。
  - 不给精确分数，因为排版、栅格、字体、色彩、状态和交互均没有可视证据。

## 2. Design read

> Reading this as：面向内部电商运营人员的收入运营指挥台，气质应克制、精确、数据密集但平静，优化目标是在三秒内发现最高优先级异常，并在一分钟内确认原因、责任人和下一步动作。

它首先应回答三个问题：

1. **现在最值得处理什么？**
2. **为什么现在处理，预计影响多少收入？**
3. **由谁采取什么动作，是否已在处理中？**

它不应优化为“展示业务全貌”，更不能像营销型数据大屏；它应优化为一个按风险、影响和紧迫度排序的 **decision surface**。

## 3. 最重要的层级与产品适配问题

### B1 · P1：12 个等权 KPI 形成 flat hierarchy

- 已知事实：顶部是 12 张尺寸相同的 KPI 卡。
- 影响：相同形状、面积和视觉权重会暗示相同重要性，运营人员必须逐张解释，而不是直接看到最高风险。
- 核心问题不是 KPI 太多，而是没有区分 `lead / supporting / diagnostic` 三个层级。

### B2 · P1：主要工作对象被概览模块压低

- 已知事实：账户表格位于 KPI 和装饰性图表之后。
- 产品风险：账户或 campaign 很可能才是用户真正需要判断和操作的对象，但当前结构先消耗大量首屏空间展示摘要。
- 表格的高密度本身不是问题；问题是它没有被确立为主要操作面。

### B3 · P1：图表没有承担明确的分析问题

- 已知事实：面积图被定义为 decorative。
- 影响：它占据高价值注意力，却没有说明趋势、异常、比较、阈值或原因，无法帮助用户确定下一步动作。
- 对 Operate 类表面，图表必须回答一个命名问题，而不是提供“数据感”。

### B4 · P1：generic tips 是无责任归属的伪洞察

- 已知事实：右栏内容是 generic tips。
- 影响：它既抢占表格宽度，也没有连接具体账户、变化、收入影响、负责人或动作。
- 如果提示不能进入受影响数据或触发动作，它就是 decoration disguised as analysis。

### B5 · P1：概念尚未定义从信号到动作的决策链

- 当前描述没有明确：时间窗、比较基准、告警阈值、数据新鲜度、预计收入影响、负责人、处理状态和下一步动作。
- 这些内容不能据此断言真实界面一定缺失，但它们必须在设计合同中被明确。
- 缺少这条链时，页面只能告诉用户“发生了什么”，不能帮助用户决定“下一小时做什么”。

## 4. Concrete design moves

### M1 · 建立 page command/context band

在页面顶部集中放置：

- 业务范围与账户/campaign 范围
- 决策时间窗与比较基准
- `Last refreshed`、时区和数据健康状态
- 只影响全局数据的筛选器

筛选器应靠近其影响范围；数据陈旧或部分失败必须显式呈现，不能让旧数据看起来像实时结论。

### M2 · 从 card soup 改为 `lead + support + action queue`

建议首屏顺序：

1. 一个 lead risk object：最高收入风险或最高优先级异常
2. 紧凑 supporting metric strip
3. exception/action queue
4. task-first account/campaign table
5. 仅在有诊断价值时保留图表

验收目标：用户无需逐项扫描，就能在三秒内指出当前第一优先事项及其原因。

### M3 · 将 12 个 KPI 分成明确层级

- 首屏只保留约 4–6 个直接影响短期决策的指标。
- 每个强调数字必须回答“相对什么”：上一时段、目标、阈值或同类基准。
- 其余 KPI 放入次级诊断区或可展开详情，不继续使用等权卡片。
- 数字使用 tabular numerals；颜色只表达语义状态，不用于装饰或区分普通指标。

### M4 · 把密集表格改成 task-first table

优先列顺序应围绕任务，而不是数据库字段顺序：

`Account/Campaign → Status/Risk → Revenue impact → Cause/Change → Owner/SLA → Next action`

同时：

- 文本左对齐，金额、比例和计数右对齐。
- 筛选、排序和 saved view 紧邻表格。
- 次要元数据进入详情或折叠列。
- 行动作应明确、可键盘访问，并在执行后给出与该行绑定的状态反馈。
- 长名称、空值和窄窗口应有有意设计的退化方式。

### M5 · 把面积图改成 diagnostic chart，或删除

图表必须先有一个具体问题，例如：

- “收入下降是集中在少数账户，还是系统性趋势？”
- “过去 60 分钟何时越过风险阈值？”
- “异常来自流量、转化率、客单价还是退款？”

保留时应提供时间范围、基准、阈值、直接标签、tooltip 和数据新鲜度；选择区间或实体后应能过滤对应表格。无法回答命名问题时，删除比美化更合适。

### M6 · 删除或重构 generic tips rail

只有符合以下结构的洞察才能保留：

`具体实体/分群 + 观测变化或阈值 + 收入影响/紧迫性 + owner + next action`

例如不是“关注转化率下降”，而是：

> Campaign A 在最近 30 分钟较七日同时间基准下降 18%，预计每小时少收入 ¥X；Owner：Li；查看异常订单。

若没有这种数据和动作闭环，应移除右栏，把宽度还给主要表格。

### M7 · 使用 `enterprise dense / ops command center` treatment

- 紧凑但不拥挤，以细分隔线和背景层级代替大量卡片、阴影和高圆角。
- 决策型表格正文暂以 `14px / 1.4` 为最低可读基线；`12–13px` 仅用于次级元数据。
- 使用 token-backed 的 `text / surface / border / status / focus` 角色，不直接添加任意色值。
- 高风险状态同时使用标签、图标或文案，不能只靠颜色。
- 普通正文对比度至少满足 WCAG normal-text 要求；动效保持安静且只表达状态变化。

### M8 · 在实现前定义 resilient state contract

至少覆盖：

- loading、empty、no-results
- error、partial-data、stale-data
- permission/ownership
- long account names、极端金额和空值
- selected、hover、focus、disabled、action-in-progress
- 窄窗口和表格横向溢出

错误和数据异常应在所属模块就地说明影响及恢复动作；窄窗口应保住异常队列和主要动作，仅把不可避免的横向溢出限制在数据表区域。

## 5. 已验证与未验证

### 由本提示确认的事实

- 目标是内部电商收入运营 dashboard。
- 主要用户需要判断下一小时应关注的账户或 campaign。
- 当前概念包含 12 个等权 KPI 卡、装饰性面积图、密集账户表格和 generic tips 右栏。
- 目标视觉权威是克制的企业控制台、密集但平静、非营销型、仅使用 token-backed color。

### 基于上述事实得出的设计判断

- 等权 KPI 会削弱注意力排序。
- decorative chart 与短时运营决策不匹配。
- generic tips 缺少具体实体和行动闭环。
- 当前模块顺序更像信息陈列，而不是从异常到动作的运营流程。

这些是对所述概念的产品与层级判断，不是对真实渲染结果的观察。

### 未验证

- 实际栅格、间距、字体、对齐、卡片尺寸、色彩和 token 使用情况
- 表格真实字段、排序、筛选、行操作、数据量与横向滚动
- 图表比例尺、标签、图例、tooltip、阈值和真实数据含义
- hover、focus、keyboard、selected、disabled 和 screen-reader 行为
- loading、empty、error、partial、permission 和 recovery 状态
- 响应式、窄窗口、长内容、缩放和浏览器性能
- 视觉完成度、可访问性对比度以及真实三秒识别效果

**本次未编辑文件、未打开浏览器、未生成截图，也未进行 DOM、responsive、focus 或交互验证。**

## 6. 实现前的最小验证计划

1. **确认决策模型**
   - 回看至少 5 个近期“下一小时需要处理”的真实案例。
   - 为每个案例记录实体、触发信号、时间窗、收入影响、紧迫度、数据置信度、owner 和采取的动作。
   - 由此锁定 exception queue 的排序规则。

2. **使用代表性真实数据制作低保真结构稿**
   - 覆盖正常、单点异常、系统性异常、长名称、零数据、陈旧数据和部分失败。
   - 至少提供主要桌面宽度和一个窄支持宽度。
   - 此阶段先验证信息顺序，不投入视觉装饰。

3. **进行 3–5 名目标运营人员的任务测试**
   - 任务一：指出现在最应处理的账户或 campaign。
   - 任务二：说明判断依据和预计影响。
   - 任务三：找到 owner 并启动下一步动作。
   - 最低标准：第一风险点约三秒可定位，选择结果与既定优先级一致，操作路径无需依赖 generic tips。

4. **冻结最小设计合同后再实现**
   - 明确 metric tiers、table column order、priority formula、chart question、insight schema、token roles 和 state matrix。
   - 实现完成后仍需补做 L2 DOM/token 检查及 L3 responsive、focus、keyboard、loading、empty、error 验证；这些验证本轮均未执行。

