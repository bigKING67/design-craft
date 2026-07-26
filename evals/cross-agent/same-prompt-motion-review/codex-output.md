## 1. 证据等级与设计判断

- **证据等级：静态源码证据。** 对明确代码事实置信度高；对手感、视觉延迟、掉帧、跨浏览器与真机行为不作已验证结论。
- **平台与 authority：** `web`、高频运营应用、`calm utility`、Reduced Motion 要求均来自题面；未使用项目 `PRODUCT.md` / `DESIGN.md`。
- **实际采用：** `design-craft` 的 `critique` 模式，以及 motion quality、interaction physics、validation contract。
- **Route：** 未生成有效 receipt；只读 sandbox 阻止 planner 创建临时文件，因此不虚构 `frontend_tier`。可写环境可补跑：  
  `bash ~/.codex/tools/frontend_route_plan.sh --surface app --intent high-motion --scope component --platform web --output compact-json`
- **Design read：** Reading this as: 高频使用的 Web 运营任务面板，采用克制的工具型动效，优化目标是在三档状态间持续、可逆地直接操控，同时保持内容、焦点和任务上下文稳定。
- **静态评审结论：Block。** Sheet 应有功能性 motion，但当前代码不具备可批准的直接操控、可中断物理和 Reduced Motion 合同。

## 2. 哪些 motion 应存在

**应该存在：**

- Pointer-down 时即时、局部的输入确认。
- 拖拽期间由指针直接驱动的位移；这是 **1:1 tracking，不是补间动画**。
- 松手后从当前位置和实测速率开始的短促、可中断 settle，用来解释三档状态归位。
- 超出自然边界时的轻度阻尼，仅用于表达边界。

**不应该动画：**

- 拖拽中的 `top`、`left` 或任何带 `300ms` 延迟的跟随。
- `transition: all`。
- 整张 sheet 的 `scale(0.96)`；它会移动视觉接触点并缩放任务内容。
- 固定 `480ms ease-in`、无法抓回的归位过程。
- 装饰性弹跳、惯性炫技、内部内容重挂载或导致滚动/焦点丢失的状态切换。
- Reduced Motion 下的大范围自动位移、弹性回弹和缩放。

## 3. 优先级 Findings

1. **P0 — 当前不是受控的 1:1 拖拽。**  
   `startY` 没有被使用；`pointermove` 无条件执行，也没有 active pointer、按键或 drag-state 判断。`top = clientY` 把 viewport 坐标直接当成 sheet 坐标，既不保留 grab offset，也不处理 containing block。与此同时 `transition: all 300ms` 会覆盖 `top`，在这些声明成立时不断把指针跟随改成追赶式补间。整张 sheet 缩放还会进一步移动手指下的视觉点。

2. **P0 — Presentation-value interruption 被锁死且存在双写风险。**  
   `animating` 只阻止 `pointerdown`，却不阻止 `pointermove` 或新的 `pointerup`；用户不能在 settle 中抓回，但样式写入仍可能和 WAAPI 竞争。Animation 没有被保存、取消或 `commitStyles()`，`fill: "forwards"` 可能留下持续占有 presentation value 的 effect。下一次交互是否跳变或被遮蔽需运行时验证，但所有权模型在静态代码中已经不完整。

3. **P1 — Settle 没有交互物理。**  
   `480ms ease-in` 在用户最关注的开头加速缓慢，不适合高频运营界面；它没有测量或传递 release velocity，并动画 layout 属性 `top`。`nearestSnapPoint(current)` 本身可能是合法产品规则，因此“投影选点”不是自动正确；但无论选点规则如何，settle 都应从当前 presentation value 继承有界速度。

4. **P1 — 缺少完整的手势生命周期与软边界。**  
   题示实现没有 intent threshold、pointer capture、pointer ID、多点处理、`pointercancel` / `lostpointercapture`、范围约束、边界阻尼或 sheet/内部滚动的仲裁。静态代码因此不能保证 taps 不被误拖、指针离开后仍连续、或 sheet 不越过 `full` / `collapsed`。

5. **P0 — Reduced Motion 合同缺失。**  
   CSS 和 JS 都没有可见的 `prefers-reduced-motion` 分支。按当前代码，长距离 `top` 动画和整张 sheet 缩放仍会执行，直接违反题面明确的无大范围空间旅行要求。

## 4. 八个具体设计动作

1. **Pointer-down feedback**  
   仅对 drag handle/grip 做即时反馈：颜色、描边或阴影在 `100–140ms ease-out` 内轻微变化；不要缩放整张 sheet。若保留 grip scale，放在独立 wrapper，避免与 sheet 的位移 `transform` 争夺同一属性。

2. **建立真正的 1:1 tracking**  
   Pointer-down 记录当前 presentation `sheetY`、`grabOffset = clientY - sheetY` 和 active pointer ID。超过约 `8–12 CSS px` 的意图阈值后 capture pointer，并在每个显示帧设置 `y = clientY - grabOffset`。只更新 `transform: translate3d(0, y, 0)`；拖拽期间禁用 transition，不读写 `top`。

3. **Presentation-value interruption**  
   保存 settle driver/Animation。新的 pointer-down 到来时，先读取驱动器维护的当前可见 `y` 和速度，立即取消 settle，把 model position 同步到该 `y`，随后进入 drag；不要使用 `animating` 输入锁。任何 WAAPI fallback 都应在完成时 commit 最终样式并取消 filled effect。

4. **Velocity handoff**  
   保存最近约 `80–100ms` 的 `{clientY, performance.now()}` 样本，用加权平均或回归得到 **CSS px/s**，而不是只比较最后两个事件。松手时把经过安全限幅的速度传给 settle；若 API 需要相对速度，则显式转换为 `velocity / (target - current)`。

5. **Projected endpoint 与产品语义分离**  
   先确认产品是否允许“快速 flick 改变目标”。若允许，可从 `projectedY = clamp(currentY + velocity * 0.14s, fullY, collapsedY)` 起步，再选择最近 snap，并通过运行时调节 projection horizon；对于 calm utility，默认限制到相邻状态，只有明确的高速手势才允许跨过 `half`。若未授权 momentum targeting，继续以当前位置/阈值选点，但仍把速度交给 settle。

6. **Soft boundaries 与滚动仲裁**  
   合法区间内保持严格 1:1；越界部分使用渐进阻力，例如  
   `resisted = overshoot * dimension * 0.55 / (dimension + 0.55 * abs(overshoot))`。  
   松手后回到最近边界且不做装饰性 bounce。若 full sheet 内部可滚动，只有内容已到顶部且手势向下时才把控制权交给 sheet；不要对整个可滚动内容区粗暴设置 `touch-action: none`。

7. **重做 settle**  
   使用可读写位置和速度的 spring/interactive animator，建议从 damping ratio `1.0`、response 约 `0.3s`、无 overshoot 起步；由运行时手感调节，而不是固定等候 `480ms`。只移动 sheet shell，保持内部 DOM、输入值、焦点、选择和滚动上下文不被重建。

8. **Reduced Motion**  
   CSS 与 JS 同时响应 `prefers-reduced-motion: reduce`。用户主动拖拽仍可保持 1:1，因为位移由用户直接控制；松手时关闭惯性投影、弹性 overshoot、整面缩放和长距离补间，直接提交 snap position，并用 `80–120ms` 的 handle 颜色、边框、scrim 或状态标签 cross-fade 表达 `collapsed` / `half` / `full` 已生效。

## 5. 已验证与未验证

**由题示源码确认：**

- `startY` 被赋值但未参与位置计算。
- `pointermove` 不检查是否正在拖拽或是否为 active pointer。
- 位移写入 `top`，值直接来自 `event.clientY`。
- Snap 使用 `sheet.offsetTop` 和当前位置最近点。
- Settle 为 `480ms`、`ease-in`、`fill: forwards`。
- CSS 使用 `transition: all 300ms` 和整张 sheet `scale(0.96)`。
- 题示范围内没有 velocity history、pointer capture、soft bounds、取消路径或 Reduced Motion 分支。
- 本次没有编辑任何文件。

**仍未验证：**

- 实际 lag、跳变、frame pacing、layout cost 或 dropped frames。
- `offsetTop`、CSS transition 与 filled WAAPI effect 在目标浏览器中的实际竞争结果。
- Snap 几何、容器坐标系、内容滚动和 viewport resize 行为。
- 中途抓回、快速反向、离开边界、第二触点和 pointer cancellation。
- Reduced Motion 的 computed style 与最终状态反馈。
- 窄屏、横竖屏、60/120Hz、真实触摸设备手感。
- 外围代码是否另有状态机或补偿逻辑；题面未提供，不能假定存在或不存在。

## 6. 实现批准前的最小验证计划

1. **主浏览器 instrumentation：** 在真实运营数据负载下记录 sampled pointer Y、presentation Y、grab offset、CSS px/s、projected endpoint、选中 snap 和 settle velocity；同时保存短视频与 Performance trace。
2. **核心手势矩阵：** 从三种状态分别做慢拖、双向 flick、中点松手、方向反转、settle 中重新抓取、越界后回入、指针离开、`pointercancel` 和第二触点。验收条件是无输入锁/视觉跳点、位移遵循最新采样点减 grab offset、只落到合法 snap。
3. **桌面与真实触摸：** 至少覆盖一个主要桌面浏览器和一台受支持的真实触摸设备；验证 full-state 内容滚动与 sheet drag 的所有权。若目标设备包含 120Hz，再补一台 120Hz 设备，不能用桌面模拟替代。
4. **Responsive：** 在最窄支持宽度、常用桌面宽度、横竖屏/viewport resize 后重算 snap points，确认内容、焦点、滚动位置和主任务状态均保留。
5. **Reduced Motion：** 在浏览器模拟和真实系统设置各跑一次；确认没有 sheet scale、惯性投影、弹性回弹或长距离 settle，同时三个状态仍有清楚的非空间反馈。
6. **批准门禁：** Trace 中 gesture hot path 不再逐帧动画 `top` 或进行同步布局测量；中途抓回、目标选择、边界、Reduced Motion 和真实触摸滚动仲裁全部通过，并保留浏览器/设备版本、视频与 trace artifact 后再批准。

