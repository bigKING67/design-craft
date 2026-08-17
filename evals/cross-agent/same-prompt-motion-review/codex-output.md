# Gesture-sheet Motion Review

**结论：BLOCK。** 这段实现表达了“拖动后吸附”的意图，但尚未满足直接操控、可中断、交互物理和 Reduced Motion 的实施批准条件。

## 1. 证据级别与设计读法

- **证据级别：`L0 static`**——只有产品上下文与静态代码；没有浏览器计算样式、pointer trace、帧时间线、响应式状态或真实触屏证据。
- **Design read：**这是一个面向高频操作人员的 Web operations bottom sheet；气质应是冷静、克制、工具化，优化目标是让用户在 `collapsed / half / full` 之间移动时始终保持空间因果和任务上下文。
- **风格 authority：**以本 prompt 中的 calm utility、直接操控和 Reduced Motion 合同为准。
- **实际使用：**`design-craft` critique mode；读取了 `motion-quality`、`interaction-physics`、`motion-patterns`、`validation-contract`。
- **Route：**尝试执行 frontend route planner，但只读环境阻止其创建临时文件，报错 `Operation not permitted`；因此仅做人工路由：`platform=web / mode=critique / scope=component / main-owned`。
- 未编辑文件，未启用子代理，未执行浏览器或设备验证。

## 2. 哪些 motion 应存在

**应该存在：**

- Pointer-down 时的即时、局部反馈，用于确认手势已被接收。
- 拖动期间严格跟随手指的位移；这属于直接操控，不应被当作缓动动画。
- 松手后到合法 snap point 的短暂 settle motion，用于保持释放位置与最终状态之间的因果关系。
- 状态变化对应的轻量 scrim、handle 或状态标识反馈。

**不应该存在：**

- 拖动路径上的 CSS easing 或固定 `300ms` 跟随延迟。
- 对整张 sheet 及其任务内容做 `scale(0.96)`。
- `transition: all` 带来的无关属性动画。
- 高频交互中的固定 `480ms ease-in` 等待。
- 使用 `top` 驱动逐帧布局动画。
- 默认弹跳、装饰性 overshoot、内容独立漂移或错峰动画。
- Reduced Motion 下的大距离 settle travel、弹性边界或整面板缩放。

## 3. 阻断性 findings

### B1 · P0 — 手势所有权和坐标映射不成立

- **静态证据：**`startY` 被记录但从未使用；`pointermove` 无 active-drag/pointer-id 判断，直接执行 `top = event.clientY`；`pointerup` 也不要求存在有效 drag。
- **物理问题：**sheet 使用指针的绝对 viewport 坐标，而不是 `起始 sheet 位置 + 指针位移`；grab offset 无法保存。普通 hover move、tap 抖动或被拒绝的 pointer-down 后续事件都可能改变状态。
- **运行态未知：**实际跳变幅度及事件序列尚未捕获，但源码中的状态所有权缺口已经足以阻断批准。

### B2 · P1 — 拖动链路不是 1:1，并把布局属性放进热路径

- **静态证据：**每次 `pointermove` 写 `top`，同时 `.sheet` 声明 `transition: all 300ms`。
- **物理问题：**直接操控要求 pointer 与 presentation value 同步；这里却要求浏览器对连续的新 `top` 值进行过渡。`top` 还会进入布局路径，而非仅更新 compositor transform。
- **设计问题：**`:active { transform: scale(0.96) }` 缩放整个任务表面，会让内容和抓取几何一起收缩，更像按钮反馈而不是稳定的可拖拽平面。
- **运行态未知：**不能仅凭源码断言已经掉帧或“手感黏滞”；计算样式和 frame timeline 仍需验证。

### B3 · P1 — Settle 不可中断，presentation state 没有单一 owner

- **静态证据：**`animating` 在整个 settle 期间拒绝新的 `pointerdown`；动画为固定 `480ms ease-in`；使用 `fill: "forwards"`，但没有保存 animation handle、提交最终基础样式或取消填充层。
- **物理问题：**用户无法在运动中重新抓取；`ease-in` 从低速度开始，与手指释放速度不连续；固定时长也无法适应移动距离。
- **状态风险：**WAAPI presentation、inline `top` 和后续 pointer writes 可能形成多个属性 owner。跨多轮拖动是否产生冻结或跳变尚未运行验证。

### B4 · P1 — 速度、目标选择和边界物理未建模

- **静态证据：**目标只取 `nearestSnapPoint(sheet.offsetTop)`；没有位置历史、CSS px/s 速度、velocity handoff、projection、边界 clamp、软阻力、pointer capture 或 `pointercancel` 处理。
- **物理问题：**快速 flick 和慢速停在同一位置会得到相同目标；释放动画也从零速度开始。越过 `full/collapsed` 时没有连续阻力模型。
- **合同边界：**“最近当前位置”可能是合法产品规则；因此 velocity handoff 是必修复项，而 projected endpoint 是否参与选点必须作为单独产品决策，不能借“更物理”静默改语义。

### B5 · P1 — Reduced Motion 没有结构化分支

- **静态证据：**所给 CSS 没有 `prefers-reduced-motion`；JS settle 也没有 `matchMedia` 或等效偏好分支。
- **影响：**Reduced Motion 用户仍会收到整张 sheet 的缩放、固定 480ms 大距离 travel，以及可能的边界弹性。
- **运行态未知：**尚未运行系统偏好切换；这里只能确认所给实现没有相应代码路径，不能描述真实设备上的最终表现。

## 4. 八个具体 design moves

1. **Pointer-down feedback**
   - 只反馈 grab handle：立即提高 handle 对比度或底色；可选 `80–120ms` 的极轻局部 `scale(0.98)`。
   - 不缩放 sheet、内容或背景；Reduced Motion 下只保留颜色、描边或静态 pressed 状态。

2. **建立明确的 drag session**
   - 仅接受 primary pointer；记录 `pointerId`、`startPointerY`、当前 presentation Y、grab offset 和单调时间戳。
   - `setPointerCapture(pointerId)`；只有匹配的 active pointer 才能 move/up；处理 `pointercancel`、`lostpointercapture`，忽略额外触点。

3. **实现真正的 1:1 tracking**
   - 以约 `8–12 CSS px` 作为待实测的意图阈值；越过后使用 `startSheetY + (clientY - startPointerY)`，而不是绝对 `clientY`。
   - 阈值越过时仍从原始 down 点计算，避免 sheet 突跳；drag 期间禁止任何 easing。

4. **统一位置表达与逐帧写入**
   - 将 snap points 表达为同一坐标系中的 `translateY`，拖动时只更新 `transform`。
   - 用 display-clock/rAF 合并到每帧最后一个 pointer sample；删除 `transition: all`，内部任务内容保持静止、清晰、可读。

5. **Presentation-value interruption**
   - 保存当前 settle controller；新 pointer-down 不得被 `animating` 拒绝。
   - 从当前屏幕上的 transform 与速度开始接管，取消旧动画而不跳回逻辑目标；settle 完成后把目标写入基础状态并移除 animation fill，而非永久依赖 `fill: forwards`。

6. **Velocity handoff**
   - 保留最近约 `80–120ms` 的 `{y, monotonicTime}` 样本，以 **CSS px/s** 计算并限制 release velocity。
   - 将该速度交给 settle spring；calm utility 的初始试验值可用 damping ratio `0.9–1.0`、response `0.25–0.35s`、默认无 bounce，最终参数必须依据 runtime trace 调整。

7. **Projected endpoint 与目标语义分离**
   - 默认先保留当前 nearest-position 合同，但仍把速度交给 settle。
   - 若产品批准 flick-to-advance，再试验 `projectedY = currentY + clamp(v * 0.15s, -oneGap, +oneGap)`；随后 clamp 到合法区间并选择最近 snap point。默认每次最多跨一个状态，除非明确批准跳过 `half`。

8. **Soft boundaries 与 Reduced Motion**
   - 在 `[fullY, collapsedY]` 外使用渐进阻力，例如 `effective = (overshoot * D * 0.55) / (D + 0.55 * abs(overshoot))`；回到合法区间时连续，不硬撞边。
   - Reduced Motion 下保留用户主动控制的 1:1 drag，但禁用 projection、弹性、overshoot 和整面板 scale；松手后立即切到目标或使用至多约 `80ms` 的非弹性收口，并以 handle/状态标签及短颜色或 scrim cross-fade 表达 `collapsed / half / full`。

## 5. Verified 与 unverified

**由所给静态代码确认：**

- `pointermove` 无 drag guard，直接写绝对 `clientY`。
- `startY` 在所给代码中未参与位置计算。
- `animating` 会拒绝 settle 期间的新 `pointerdown`。
- settle 配置为 `top`、`480ms`、`ease-in`、`fill: forwards`。
- CSS 使用 `transition: all 300ms`，active 状态缩放整张 sheet 至 `0.96`。
- 所给代码没有 velocity history、pointer capture、soft boundary 或 Reduced Motion 分支。

**仍未验证：**

- 实际 pointer-to-sheet 延迟、跳变幅度、帧率和 forced-layout 成本。
- CSS transition、WAAPI fill 与 inline style 在目标浏览器中的跨轮交互。
- `offsetTop` 与实际 presentation value 在动画中是否连续。
- 鼠标、触控笔、真实触摸、浏览器滚动和 sheet 内部滚动的仲裁。
- 不同 viewport、方向变化和动态 viewport 下的三个 snap point。
- Spring、projection、边界阻力的真实手感及误触率。
- Reduced Motion 的最终视觉、可理解性和辅助技术状态反馈。

## 6. 最小浏览器/设备批准计划

1. **环境**
   - 一个生产主浏览器的桌面运行态，加一个生产支持矩阵内的真实触屏设备；记录浏览器版本、viewport、输入类型和刷新率。
   - 若生产明确支持多个浏览器引擎，再补一个第二引擎；不因普通 responsive Web 自动扩大为 iOS/Android native 验证。

2. **直接操控 trace**
   - 记录 pointer Y、presentation Y、grab offset、pointerId 和时间戳。
   - 覆盖不同抓取位置、慢拖、短拖、方向反转、pointer 离开边界、cancel/lost capture 和第二触点；要求无有效 drag 时 sheet 不移动，越过阈值后 grab offset 连续。

3. **中断与状态**
   - 分别在 settle 约 25%、50%、75% 时重新抓取并反向拖动。
   - 要求没有视觉跳回、输入锁、冻结或错误 snap；最终 semantic state 必须与屏幕 presentation 一致。

4. **速度、端点和边界**
   - 双向比较慢速释放与快速 flick；日志同时记录 release velocity、current Y、projected Y、selected target。
   - 分开评审 nearest-current 基线和 projection 实验；未经授权不得因实验结果直接改变产品选点语义。
   - 越过上下边界及 full-state 内容滚动交接必须连续、可逆且不会丢失任务上下文。

5. **性能、响应式与 Reduced Motion**
   - 捕获 drag/settle performance timeline，确认 move 热路径没有重复布局读取写入和明显 long task；不能只凭 transform 使用就宣称流畅。
   - 至少检查宽桌面、窄 viewport 和一次 resize/orientation change，确认保持当前 semantic state。
   - 系统 Reduced Motion 开/关各运行一次：开启后无大距离动画、弹跳或 sheet scale，但 pressed 状态、最终状态和可访问状态反馈仍明确。

批准所需最小证据：pointer trace、normal/reduced 两段短录屏、一次 performance timeline，以及真实触屏设备环境记录。在这些证据通过前，结论保持 **static-review blocked / runtime unverified**。

Memory: `user:global + project:design-craft + domain:codex`，3 hits；0 candidates，0 writes；仅用于确认 canonical motion 参考，所有交互结论均以本轮 prompt 和静态代码为准。

