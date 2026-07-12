## 1. 证据等级与设计判断

- **使用技能**：`design-craft`
- **评审模式**：`critique`，只读静态审查
- **平台 / 上下文**：Web；产品、频率、视觉基调和 Reduced Motion 要求均由提示明确提供
- **证据等级**：**静态源码证据**
  - 能确认：事件路径、动画属性、固定时长、缓动、输入锁、缺失的显式手势分支
  - 不能确认：真实延迟、帧率、视觉跳变幅度、触摸滚动冲突、设备手感、响应式几何
- **Design read**：这是一个供运营人员高频使用、承载当前任务上下文的底部 Sheet；应当表现为安静、直接、可随时接管的工具，而不是播放一段动画。
- **结论**：**Block，当前实现不应批准。** 问题不只是“不够顺滑”，而是直接操控、可中断性和状态物理模型尚未成立。

## 2. 哪些动效应该存在

**应该存在：**

- Pointer down 时，拖拽把手提供即时、轻微的接收反馈。
- 拖动期间，Sheet 与指针保持 1:1 的受控位移。
- 释放后，从当前屏幕位置和当前速度出发，短促地收敛到 `collapsed`、`half` 或 `full`。
- 状态完成时，可用把手颜色、状态标签或轻微明暗变化确认落点。

**不应动画：**

- 拖动更新不能经过 `300ms transition`；直接操控不是补间动画。
- 不应使用 `transition: all`，也不应逐帧动画 `top`。
- 不应把整个 Sheet 缩放到 `0.96`；这会让任务内容和文字一起“软掉”，破坏上下文稳定性。
- 底层任务画布不应增加缩放、模糊、视差或装饰性位移。
- 不应使用固定 `480ms ease-in`、默认弹跳或不可中断的自动行程。
- Reduced Motion 下不应产生释放后的大范围自主位移。

## 3. 阻断性发现（最多五项）

### P0-1：拖拽并未建立可靠的直接操控合同

- `pointermove` 没有检查 `dragging`、`pointerId` 或按键状态，因此提供的代码路径允许它在未开始拖拽时执行。
- `startY` 被记录但未使用，没有保存 grab offset；`sheet.style.top = event.clientY` 会把 Sheet 顶边对齐到手指，而不是保持用户抓住的位置。
- `clientY` 属于 viewport 坐标，而 `top` 通常属于 containing block 坐标；当前没有明确统一坐标空间。
- 没有 pointer capture，指针离开 Sheet 后不能保证继续收到 move/up。
- `transition: all 300ms` 会让每次 `top` 更新成为可补间变化，因此结构上不再是 1:1 跟手。

### P0-2：释放动画不可中断，且逻辑值与呈现值可能脱节

- `if (animating) return` 直接阻止用户在 480ms 收敛期间重新抓取。
- 高频工具中的 Sheet 必须允许用户随时改变主意；动画不能获得输入所有权。
- 新拖拽应从当前屏幕上的 presentation value 开始，而不是旧 snap point 或底层 inline `top`。
- `fill: "forwards"` 保留动画效果，但代码没有把最终位置同步回统一的状态所有者，也没有清理 Animation。
- `pointermove`、`pointerup` 又没有一致使用 `animating`/active-pointer 门禁，状态所有权存在交叉和重入风险。

### P0-3：释放物理与用户手势脱节

- 目标仅由 `nearestSnapPoint(sheet.offsetTop)` 决定，没有采样释放速度，也没有 projected endpoint。
- 快速向上甩与缓慢停在同一位置可能选择相同目标，违背用户表达的方向和力度。
- 动画从默认零速度启动，无法承接手指释放速度。
- `ease-in` 在释放后先慢后快，恰好延迟用户最关注的起始响应，并在接近端点时加速。
- 固定 `480ms` 对很短和很长的剩余距离一视同仁，不符合稳定的 Sheet 物理感。

### P0-4：属性选择和反馈方式破坏稳定性

- 拖动和收敛都写入 `top`，同时读取 `offsetTop`；这是布局属性热路径，存在重复 style/layout 工作风险。
- 静态源码可以确认布局属性被使用，但不能据此声称已经发生掉帧。
- `transition: all` 会把未来新增的可动画属性也纳入运动，造成不可预测的属性耦合。
- 整体 `scale(0.96)` 对大型 Sheet 过强，会移动文字、边缘和内部控件。
- 若后续改用 `transform: translateY(...)`，现有 `:active` 的 `transform: scale(...)` 还会产生 transform 所有权冲突。

### P0-5：缺少边界、取消与 Reduced Motion 合同

- 提供片段中没有拖拽意图阈值、上下边界、软阻力、`pointercancel`、`lostpointercapture` 或多指规则。
- 未显示拖拽把手与内部滚动内容之间的 `touch-action`/手势仲裁策略。
- 没有 `prefers-reduced-motion` 分支。
- 对高频、长距离 Sheet 而言，Reduced Motion 不能只把 480ms 改成另一个时长；必须取消大范围自主旅行、惯性和弹性。

## 4. 具体设计动作（八项）

1. **Pointer-down 反馈**
   - 只反馈拖拽把手或顶部 affordance，不缩放整个 Sheet。
   - 可使用把手颜色加深、宽度轻微增加或表面边框变化，约 `80–120ms ease-out`。
   - 反馈在 down 时立即发生，tap 被取消时可逆；颜色反馈可在 Reduced Motion 下保留。

2. **建立 1:1 拖拽会话**
   - Pointer down 时保存 `pointerId`、当前 presentation `y`、容器几何和 `grabOffset`。
   - 使用 `setPointerCapture(pointerId)`；move/up/cancel 只响应当前 active pointer。
   - 采用约 `8–12 CSS px` 的起始意图阈值；超过阈值后保持抓取点不变。
   - `touch-action: none` 仅放在明确的拖拽把手上，Sheet 内容区域继续保留滚动能力。

3. **统一坐标与属性所有权**
   - 将指针和三个 snap points 转换到同一个容器局部 CSS-pixel 坐标空间。
   - 用专属 motion wrapper 的 `translate3d(0, y, 0)` 驱动位置；拖动期间禁用 transition。
   - 把手反馈放在内层元素，避免 `translateY` 与 `scale` 争夺同一个 `transform`。
   - 删除 `transition: all`；内部内容、尺寸和任务画布保持稳定。

4. **从 presentation value 中断**
   - 任意合法 pointer down 都应立即取消当前 settle，而不是检查 `animating` 后拒绝输入。
   - 读取动画引擎维护的当前 `y`，或在 down 时采样当前呈现 transform，作为新拖拽起点。
   - 保留当前速度并允许反向接管；中断点不得跳到上一个逻辑目标。
   - 不依赖永久 `fill: forwards`；最终 transform、逻辑状态和动画对象必须归一到同一状态所有者。

5. **测量并交接释放速度**
   - 保存最近约 `60–100ms` 的位置与 `performance.now()` 时间样本。
   - 以 CSS `px/s` 计算经过平滑的释放速度，而不是只看最后两个事件。
   - 收敛动画以该速度为初速度；手指向上释放时，Sheet 不应先停住再重新启动。

6. **使用 projected endpoint 选择状态**
   - 根据当前位置、释放速度和经过实测调节的衰减参数预测终点，再选择 `collapsed`、`half`、`full`。
   - 加入方向性和 hysteresis，避免在状态分界附近来回抖动。
   - 低速释放偏向最近状态；明确的快速 flick 可前往运动方向上的下一状态。
   - 对高频运营界面，除非速度和距离都表达强意图，否则不应轻易跨越两个状态。

7. **软边界与平静的收敛**
   - 合法范围内保持 1:1；超过 `full`/`collapsed` 后使用渐进式 rubber-band 阻力，而非硬停或无限越界。
   - `pointercancel`、capture 丢失或窗口失焦时，从当前位置安全收敛到合法状态。
   - Sheet settle 可从近临界阻尼开始调试，例如 damping ratio `0.9–1.0`、response `0.25–0.35s`。
   - Calm utility 默认无弹跳；只有用户真实释放速度导致的轻微连续性可以保留。

8. **Reduced Motion**
   - 保留用户主动控制的直接跟手，但移除释放后的惯性投射、rubber-band 和 overshoot。
   - 释放时立即提交目标状态；只有剩余距离非常小时才允许不超过约 `80ms` 的短收敛。
   - 程序化切换状态时直接切换位置，以 `80–120ms` 的把手颜色、状态文字或边框变化确认结果。
   - 不缩放整个 Sheet，不让内部任务内容淡出，也不播放大范围自主位移。

## 5. 已验证与未验证

**由提供源码可确认：**

- 存在 `480ms`、`ease-in`、`fill: "forwards"` 的 `top` 动画。
- Pointer down 在 `animating` 时被拒绝。
- `startY` 在片段内未参与位置计算。
- Pointer move 直接把 `clientY` 写入 `top`，且未显示 active-pointer 门禁或 pointer capture。
- Snap 目标只使用释放时的 `offsetTop`，未显示速度采样或投射。
- CSS 使用 `transition: all 300ms` 和整 Sheet `scale(0.96)`。
- 片段内未提供 Reduced Motion、软边界或取消处理。

**本轮没有验证：**

- 实际 computed style、定位 containing block、snap point 几何和动画叠加结果。
- 是否真的出现掉帧、拖尾、跳变、抖动或动画完成后位置粘滞。
- 触摸滚动、系统手势、文本选择和 pointer cancellation 的实际冲突。
- 60Hz/120Hz 帧节奏、主线程负载和布局成本。
- 不同视口高度、缩放、方向、安全区或虚拟键盘下的三个状态。
- Reduced Motion 的系统运行结果。
- Chrome、Safari、Firefox 或真实触摸设备上的手感。
- 片段以外是否另有补充事件处理或 CSS 覆盖。

## 6. 实现批准前的最小浏览器 / 设备验证计划

1. **桌面主浏览器**
   - 用鼠标和触控板验证：hover 不移动 Sheet、tap 不误拖、grab offset 固定、指针离开把手后仍持续追踪。

2. **中断测试**
   - 在收敛进程约 20%、50%、80% 时重新抓取并反向拖动。
   - 验收条件：立即响应、呈现位置连续、无视觉跳点、没有 480ms 输入锁。

3. **释放矩阵**
   - 从三个状态分别测试慢拖、短快 flick、长快 flick，并覆盖上下两个方向。
   - 记录 release velocity、projected endpoint、最终状态，确认 hysteresis 和跨状态策略符合预期。

4. **真实触摸设备**
   - 至少一台真实 iOS Safari 或 Android Chrome 设备。
   - 验证把手拖拽、内部内容滚动、边界阻力、拖出元素、`pointercancel`、第二触点和系统手势竞争。

5. **Reduced Motion 与响应式**
   - 在系统 Reduced Motion 开启状态下运行完整状态切换。
   - 覆盖短视口、长视口和方向变化；确认没有大范围自主旅行，且三个状态仍有清晰反馈。

6. **性能轨迹**
   - 在代表性的运营页面负载下录制 pointer trace 和 Performance/Frame timeline。
   - 验证 move 热路径没有逐帧 `top`/`offsetTop` 布局工作、长任务或明显 frame pacing 波动。
   - 若产品支持多个浏览器引擎，再在主要次级引擎执行一次核心中断与触摸流程。

**本轮未编辑任何文件，也未运行上述浏览器、响应式、Reduced Motion 或真实设备验证。**