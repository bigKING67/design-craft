## 1. 证据级别与设计解读

**结论：Block，不建议进入实现批准。** 动效本身有正当目的，但当前静态实现把直接操控做成了慢、不可安全中断、坐标所有权不清晰的 `top` 动画。

- **Evidence level：Static-only / source evidence。**
- 使用：`design-craft`，模式为 `critique`，平台为 Web。
- 静态代码可以证明已声明的事件路径、属性和值，以及所给片段中缺失的分支；不能证明实际手感、帧率、computed style、浏览器合成行为或真机触控结果。
- **Design read：**这是一个供运营人员高频使用的 Web bottom sheet，风格是克制的工具型 UI，核心目标是在 `collapsed / half / full` 间移动时保持直接操控感和任务上下文。

## 2. 哪些动效应该存在

**应该存在：**

1. `pointerdown` 时的即时、轻量确认。
2. 拖动期间与指针严格对应的空间反馈——这是直接操控，不应被“缓动”。
3. 松手后到合法 snap point 的短促 settle，用来解释状态归位。
4. 被中途重新抓取时，从当前屏幕位置无跳变地交回控制权。

**不应该动画化：**

- 指针与 sheet 之间的跟随过程。
- 整张 sheet 的 `scale(0.96)` 按压效果及内部文字、控件的缩放。
- `top`、布局尺寸或 `transition: all`。
- 固定 `480ms ease-in` 的长距离归位。
- 装饰性 bounce、内容重排、与状态无关的视差。
- Reduced Motion 下的大距离自动位移、投射惯性和橡皮筋效果。

## 3. 阻塞发现，按优先级排序

### P0-1：事件路径不是一个受控的 drag session

`animating` 只阻止 `pointerdown`；`pointermove` 和 `pointerup` 没有 `dragging`、`pointerId` 或按钮状态门禁。任何送达该 listener 的 `pointermove` 都会改写 `top`，未开始拖动的 `pointerup` 也会触发 settle。

同时未看到 `setPointerCapture`、`pointercancel`、`lostpointercapture` 或多指过滤。指针离开 sheet 后可能丢失后续事件；这在静态层面已经不足以支撑可靠的直接操控。

### P0-2：没有保持 grab offset，也没有建立统一坐标系

`startY` 在所给证据中写入后未使用；`event.clientY` 是 viewport 坐标，却被直接赋给通常相对 containing block 的 `top`，而且指针位置被当成 sheet 顶边。

因此代码没有表达“用户抓住 sheet 的哪个位置”。若 containing block 不是 viewport 原点，或用户不是从顶边抓取，存在首帧跳变和持续偏移风险；实际偏移量仍需 runtime 验证。

### P0-3：声明的 CSS 会破坏 1:1 跟随，并建立 layout 热路径

`transition: all 300ms` 会把可过渡的 `top` 更新变成追赶指针的过渡，而不是直接跟随；每个 move 又写入布局属性 `top`。这同时带来输入滞后、CSS transition 与 WAAPI 所有权冲突，以及持续 layout/paint 的风险。

静态代码足以判定该属性策略不适合 drag；实际延迟、掉帧和重排成本尚未测量。

### P0-4：settle 不可中断，presentation value 与逻辑值没有统一所有者

`if (animating) return` 明确拒绝在 settle 中重新抓取。代码也没有取消旧动画、读取当前屏幕位置和速度、再把控制权交给新手势的路径。

`fill: "forwards"` 保持动画视觉结果，而 inline `top` 仍可能停留在释放位置；后续又混用 `offsetTop`。此外 `.finished.then(...)` 没有 cancellation/rejection cleanup。该结构无法可靠表达 presentation-value interruption。

### P1-5：释放物理和无障碍策略均不成立

固定 `480ms ease-in` 在高频工具界面中起步迟缓，并完全忽略释放速度。缺少 velocity handoff 是确定问题；是否用 projected endpoint 改变 snap 目标，则是尚未明确的产品语义，不能擅自替换当前 nearest-position 规则。

所给片段也没有 Reduced Motion 分支。整张 sheet 的 `scale(0.96)` 是大面积、非因果反馈，还会缩放任务内容；它不适合替代明确的抓取反馈。

## 4. 八个具体设计动作

1. **建立单一位置所有者。**  
   将 sheet 的布局基准固定，只由一个手势/动画控制器写入 `translateY`；删除 `transition: all` 和逐帧 `top` 动画。sheet 位移与 handle 按压反馈使用不同 wrapper，避免多个行为争用 `transform`。

2. **把 pointer-down 反馈限制在拖拽 handle。**  
   按下立即切换 `cursor: grabbing`，并用 handle 颜色、粗细或约 `scale(0.98)` 的 `80–120ms` 反馈确认抓取；不要缩放整张 sheet，也不要等待越过拖动阈值才反馈。

3. **实现完整的 1:1 drag session。**  
   记录唯一 `pointerId`、当前 presentation Y、containing-block 坐标和 `grabOffset`；以 `8–12 CSS px` 作为待实测的意图阈值，确认拖动后调用 `setPointerCapture`。仅处理该 pointer，并覆盖 `pointerup`、`pointercancel`、`lostpointercapture`；`touch-action: none` 只放在 handle，避免破坏 sheet 内容滚动。通过 display clock/rAF 合并更新，位置为同一坐标系中的 `pointerY - grabOffset`，不加 easing。

4. **允许从 presentation value 中断。**  
   新的 `pointerdown` 即使发生在 settle 中也必须生效：控制器冻结当前屏幕 Y 和当前动画速度，取消旧 settle，再从该值交给 drag；不得从旧 snap target 重启，也不得依赖 `animating` 输入锁。

5. **分离速度测量、目标选择和 settle。**  
   保留最近约 `80–120ms` 的单调时间戳样本，以 CSS px 和 `performance.now()` 计算 `releaseVelocity`，单位明确为 `CSS px/s`，并做安全限幅。先按产品规则选择 target，再把测得速度转换成动画 API 所需单位，作为 settle 的 initial velocity。以近临界阻尼、无 overshoot 的 spring 为起点，例如 `damping ratio ≈ 1.0`、`response ≈ 0.28–0.35s`，而不是固定 `480ms`。

6. **把 projected endpoint 作为独立、需授权的产品决策。**  
   若确认允许 flick/momentum targeting，可先实验：  
   `projectedY = clamp(currentY + velocityPxPerSec * 0.18s, minSnapY, maxSnapY)`，再选择最近 snap；默认限制一次只跨到相邻状态，除非产品明确允许跳过 `half`。若未授权，则继续用当前位置选择最近 snap，但仍必须传递 release velocity，不能把 target selection 与 velocity continuity 混为一件事。

7. **给自然边界增加渐进阻力。**  
   合法范围限定在 `minSnapY…maxSnapY`；越界距离为 `o` 时，可用  
   `resisted = (o * D * 0.55) / (D + 0.55 * abs(o))`  
   作为待实测起点，其中 `D` 是有效拖动跨度。松手后回到边界且不 bounce；不得直接让 `clientY` 把 sheet 拉到任意位置。

8. **提供明确的 Reduced Motion 路径。**  
   在 `prefers-reduced-motion: reduce` 下保留用户主动控制的 1:1 跟随，但关闭 projected momentum、橡皮筋和 overshoot。释放或程序化切换状态时，大距离几何变化直接完成；用短促的 handle 颜色/透明度变化、持久的状态标记以及可访问状态值反馈 `collapsed / half / full`，而不是播放大距离自动移动。

## 5. 已验证与未验证

**从所给代码中可确认：**

- `pointermove` 直接执行 `sheet.style.top = event.clientY`。
- `startY` 在所给片段中没有参与位置计算。
- 没有展示 drag-active、`pointerId`、pointer capture 或 cancel cleanup。
- settle 使用 `top`、`480ms`、`ease-in`、`fill: "forwards"`。
- settle 期间 `pointerdown` 被拒绝。
- CSS 声明了 `transition: all 300ms` 和整张 sheet 的 `scale(0.96)`。
- 所给 JS/CSS 中没有 Reduced Motion、速度采样、边界阻力或 presentation-value interruption 分支。

**本轮未验证：**

- 完整 CSS cascade、computed `transition-property`、containing block 和 snap-point 几何。
- 实际是否出现跳变、跟手延迟、layout thrash、掉帧或动画层冲突。
- 当前 nearest-position 语义是否为产品明确要求，以及是否允许 flick 跳过 `half`。
- 完整项目其他位置是否已有 pointer capture、Reduced Motion 或动画控制器。
- 响应式、内容滚动与 handle 手势仲裁。
- Chromium、Safari 及真实触控设备上的手感。
- 60Hz/120Hz 下的速度估计与 spring 参数。

## 6. 实现批准前的最小浏览器/设备验证计划

1. **桌面浏览器交互录制：**在主支持浏览器中记录 event timestamp、pointer Y、presentation Y、release velocity、projected endpoint、selected target；覆盖慢拖、快 flick、反向拖、越界、松手在元素外、`pointercancel`、第二指针和 settle 中重新抓取。
2. **computed style 与帧时间线：**确认 drag 期间只有一个位置控制器写 `transform`，不存在 `transition: all` 或逐帧 `top`；在代表性数据负载下录制 Performance trace，检查 gesture hot path 是否发生同步布局、长任务和持续掉帧。
3. **Reduced Motion 与响应式：**分别在正常/Reduced Motion 下验证三种状态、程序化切换、窄 viewport、桌面 viewport、resize/orientation 后 snap 重算；Reduced Motion 必须没有大距离自动 travel，状态反馈仍清楚。
4. **至少一台主要支持的真实触控设备：**验证 handle 与内容滚动的手势仲裁、抓取偏移、边界阻力、快速反向和中断。若产品同时正式支持 Safari 与 Chromium 移动端，则每个引擎至少一台；触控手感未通过真机前不批准。
5. **批准门槛：**重新抓取无可见跳变；抓取点不漂移；快速释放方向与 target 符合已批准语义；Reduced Motion 无大范围自动移动；trace 中无 drag 驱动的重复布局热路径。

本轮为纯静态只读评审：未修改文件，也未执行浏览器、响应式或真实设备验证。