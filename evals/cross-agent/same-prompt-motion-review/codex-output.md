## 1. 证据等级与设计判读

- **实际使用**：`design-craft / critique`，读取了 motion quality、interaction physics、validation contract。
- **证据等级**：仅静态源码。代码结构、显式属性和缺失分支可高置信判断；手感、帧率、真实级联、触控冲突和设备表现均未验证。
- **Design read**：这是高频 Web 运营工作台中的可拖拽任务上下文面板，气质应是 calm utility，核心是让面板始终贴手、可随时重抓，并快速稳定到明确状态。
- **结论**：**阻止当前实现通过交互审批**。底部面板的因果性位移动效应该存在，但现有实现不具备可靠的直接操纵物理、可中断性或 Reduced Motion 路径。
- 本轮未运行 route、浏览器、模拟器或真实设备，也未生成截图、视频或性能 trace。

## 2. 哪些动效应该存在

**应该保留：**

- pointer-down 时即时、克制的抓取确认。
- 超过意图阈值后的 **1:1 用户驱动位移**；这不是装饰动画，不应被缓动。
- 松手后从当前呈现位置到合法 snap point 的短促 settle，用于完成因果闭环。
- 状态落定后的非空间反馈，例如 handle 颜色、状态名称或轻微 scrim 变化。

**不应该动画：**

- 不应对拖拽中的坐标更新应用 CSS transition。
- 不应动画 `top`、`left` 等布局属性，也不应保留 `transition: all`。
- 不应缩放整张 sheet；点击 sheet 内按钮时也不应触发面板整体 `scale(0.96)`。
- 不应有固定 480ms 的 `ease-in`、装饰性 bounce、内容重建/淡出或与手势无关的视差。
- 不应在 settle 期间锁住输入。
- Reduced Motion 下不应保留大范围自动位移、惯性投射、橡皮筋或 overshoot。

## 3. 阻塞性发现（按优先级）

### F1 — P0：没有可信的拖拽生命周期和坐标模型

- `pointermove` 无条件写入 `sheet.style.top`；没有 `dragging`、`pointerId` 或按键检查。
- `pointerup` 也没有确认本次是否实际开始过拖拽，因此普通点击也可能触发 settle。
- `startY` 在给定代码中没有被使用；没有保存 sheet 起点或 grab offset。
- `clientY` 是 viewport CSS px，而 `top`/`offsetTop` 可能属于 offset container；坐标空间是否一致未知。
- 结果风险：鼠标 hover/无关 pointer、sheet 内控件操作可能改位置；首次移动可能把 sheet 顶边跳到手指位置；离开元素后可能丢失跟踪。

### F2 — P0：跟踪不是 1:1，且属性所有权互相冲突

- `transition: all 300ms` 会把连续的 `top` 更新变成追赶指针的插值，而不是直接映射。
- 拖拽和 settle 都修改 `top`，属于高频布局路径；读取 `offsetTop` 还可能在写入后触发同步布局。
- `:active` 同时对整张 sheet 写 `transform: scale(0.96)`，产生与拖拽无关的空间变化。
- 这足以构成确定的实现风险；具体 lag、layout cost 和掉帧幅度仍需 trace 才能确认。

### F3 — P0：不支持 presentation-value interruption

- `animating` 直接拒绝 pointer-down，违反“运动中的对象仍可被抓住”。
- 但 `pointermove`/`pointerup` 没有同样的 guard，因此锁定并不完整，还可能与正在运行的 WAAPI 动画竞争。
- 返回的 `Animation` 没有保存、读取、取消或重新定向。
- `fill: "forwards"` 保留完成后的动画效果，却没有把目标提交到底层位置并取消 effect；后续 inline 写入可能被已填充动画遮蔽。
- `.finished.then(...)` 没有取消/拒绝清理路径，无法支撑安全中断和并发 settle。

### F4 — P0：松手物理与输入速度断裂

- 目标只由 release 时的 `nearestSnapPoint(sheet.offsetTop)` 决定。
- 没有位置历史、速度单位、速度过滤、初速度传递或距离相关的 settle。
- 固定 `480ms ease-in` 会从零速缓慢启动并在末段加速，与手指释放时的速度方向和幅度脱节；短距离也要等待同样时长。
- projected endpoint 是否参与目标选择属于产品语义决策，不能未经授权替换现有 nearest-position 规则；但**速度传给 settle**不应因此省略。

### F5 — P0：边界约束和 Reduced Motion 契约缺失

- 给定代码没有 snap 范围限制、渐进阻力、意图阈值、`pointercancel` 或 `lostpointercapture` 恢复。
- `top` 可以被写到合法状态范围之外；硬边界和越界后的实际表现未知。
- 给定 CSS/JS 中没有 `prefers-reduced-motion` 分支，480ms 大范围空间运动仍会执行。
- 也没有看到独立于空间运动的 collapsed/half/full 状态反馈；完整组件是否另有处理尚未证明。

## 4. 八个具体设计动作

1. **收敛 pointer-down 反馈和手势区域**
   - 只让专用 drag handle 发起拖拽；`touch-action: none` 仅放在 handle，保留 sheet 内容滚动和控件交互。
   - down 时立即给 handle 约 `100–120ms` 的颜色、透明度或 1–2px grip 压缩反馈；不要缩放整张 sheet。
   - 只接受 primary pointer，并统一处理 `pointerup`、`pointercancel`、`lostpointercapture`。

2. **建立明确的 1:1 坐标模型**
   - 统一使用 viewport CSS px，或先把 `clientY` 转换到明确的容器坐标。
   - down 时记录 `grabOffset = pointerY - presentationSheetTop`。
   - 超过约 `8–12px` 的可调意图阈值后，令 `nextTop = pointerY - grabOffset`；自然范围内必须满足 `sheetDelta ≈ pointerDelta`。
   - 接受拖拽后调用 `setPointerCapture(pointerId)`，忽略其他 pointer。

3. **拆分位移与按压的属性所有权**
   - 用稳定布局位置加外层 `translate3d(0, y, 0)` 驱动 sheet，而不是逐帧写 `top`。
   - 外层只拥有 drag translation；内层 handle 才拥有 press feedback，避免两个行为竞争同一个 `transform`。
   - 删除 `transition: all`；拖拽期间不加 easing。snap bounds 在 drag 前或 resize 时计算，不在每个 pointermove 中读布局。

4. **实现 presentation-value interruption**
   - 保存当前 settle controller/animation；新 pointer-down 到来时，先取得当前屏幕位置和当前速度，再取消旧 settle。
   - 以这个 presentation value 作为新 drag 起点，不从旧逻辑 target 重置，也不使用全局 `animating` 锁。
   - settle 完成后把最终 transform 提交到底层状态并移除动画 effect；取消、替换、元素卸载都走 identity-safe cleanup。

5. **测量并交接释放速度**
   - 保留最近约 `80–120ms` 的 `(event.timeStamp, clientY)` 样本。
   - 以 monotonic 时间计算 `vY`，单位明确为 **CSS px/s**；过滤异常样本，并用真实 trace 调整速度上限。
   - 初始候选可将输入速度限制在约 `±2500 CSS px/s`，再转换为所选 spring API 的单位，作为 settle 的 initial velocity，而不是从零启动。

6. **把 projected endpoint 与目标语义分开**
   - 默认审批基线继续使用项目现有的 `nearestSnapPoint(currentY)`，直到产品确认快速 flick 应跨状态。
   - 若授权 momentum targeting，可先实验：
     `projectedY = clamp(currentY + clamp(vY, -2500, 2500) * 0.12, fullY, collapsedY)`，
     然后 `nearestSnapPoint(projectedY)`。
   - `0.12s` horizon、速度上限、是否最多跨一个状态和 midpoint hysteresis 都必须通过 pointer trace 调整，不能作为未经验证的常量固化。

7. **加入 soft boundaries 和克制的 settle**
   - 在 full/collapsed 外使用渐进阻力，而不是无限拖动或硬停；候选 rubber-band constant 可从 `0.55` 开始。
   - 松手目标必须落在三个合法 snap point 之一。
   - calm utility 起点可用接近 critically damped 的 spring：`damping ratio ≈ 1.0`、`response ≈ 0.28–0.35s`、无装饰性 bounce，并限制高速 overshoot。
   - 若技术栈没有可中断 spring，至少使用能读取当前位置、重新定向并继承速度的显示时钟驱动实现，而不是固定 WAAPI `ease-in`。

8. **提供非空间化 Reduced Motion 路径**
   - JS settle 逻辑也要监听 `matchMedia("(prefers-reduced-motion: reduce)")`，不能只改 CSS。
   - 用户直接拖动仍保持 1:1，因为它由用户控制；松手后禁用投射、橡皮筋和 overshoot，并直接提交最近状态，不播放大范围空间插值。
   - 用约 `80–120ms` 的 handle 颜色/透明度反馈、持久的状态名称以及可访问状态值（例如 `aria-valuetext`）确认 collapsed/half/full；焦点反馈不得依赖 motion。

## 5. 已验证与未验证

**静态代码已证实：**

- `pointermove` 无 drag gate，并直接把 `clientY` 写成 `top`。
- `startY` 在给定片段中未被消费。
- pointer-down 在 `animating` 时返回，但 move/up 没有对应生命周期约束。
- settle 使用 `top`、`480ms`、`ease-in`、`fill: forwards` 和 release-position nearest snap。
- CSS 使用 `transition: all 300ms`，`:active` 缩放整张 sheet。
- 给定片段中没有 pointer capture、grab offset、速度、边界、取消处理或 Reduced Motion 分支。

**未验证，不能作为事实宣称：**

- 实际拖拽延迟、跳变幅度、帧率、layout/compositor 成本或触控手感。
- `top` 的 containing block、snap point 顺序/数值、其他 CSS 覆盖和真实 computed style。
- `fill: forwards` 在目标支持浏览器中是否实际遮蔽下一次 inline drag。
- sheet 内滚动、按钮、文本选择、multi-touch、pointer cancellation 的真实冲突。
- Reduced Motion 是否在片段外另有全局实现。
- collapsed/half/full 的响应式位置、横竖屏表现以及 60/120Hz 设备差异。

## 6. 实现批准前的最小浏览器/设备验证计划

1. **桌面支持浏览器**：记录 pointerY、presentationY、velocity、projectedY、selected target；测试慢拖、短拖、快速 flick、反向拖动、settle 中重抓、移出 handle、cancel，以及连续 20 次三态循环。
2. **直接操纵验收**：意图阈值之后，除 soft-boundary 区域外，下一显示帧中的 sheet delta 应与 pointer delta 等量；grab offset 不变化，重抓无视觉跳跃，结束状态始终是三个合法 snap point 之一。
3. **内容上下文验收**：操作 sheet 内按钮、选择文本和滚动内容不得移动 sheet；只从 handle 拖动。窄 viewport、宽 viewport和方向变化后重新验证三个 snap point。
4. **运行态检查**：DevTools computed style 与 Performance/Animation trace 应证明拖拽热路径只改变 compositor-friendly transform，没有 `top` transition、重复强制布局、遗留 filled animation 或系统性追赶指针。
5. **真实触控设备**：至少一台产品支持的 iOS Safari 或 Android Chrome，记录刷新率；复测 pointer capture、scroll/drag 冲突、快速 flick、settle 中重抓、multi-touch 和边界阻力。若发布对 120Hz 手感敏感，再补一台 120Hz 设备。
6. **Reduced Motion**：先用浏览器媒体模拟，再用真实设备系统设置复测；验收标准是直接拖动仍可控、松手无大范围自动 travel/elastic overshoot，并能通过静态视觉和可访问状态值明确辨认三态。
7. 保存最小证据包：事件 trace、短视频、Performance trace、浏览器/设备/刷新率，以及关键 artifact 的路径和 SHA-256；这些产物出现前只能标记为 `runtime unverified`。

