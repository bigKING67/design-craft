## 结论

**当前结论：Block，不应进入实现批准。**

问题不是“参数不够精致”，而是这段实现违背了可拖拽物体的核心合同：**输入未被可靠拥有、拖动不是稳定的 1:1 映射、运动不可打断、释放意图未进入物理模型，也没有 Reduced Motion 路径。**

## 1. 证据级别与设计解读

- **证据级别：静态源码证据。**
- 对代码中明确存在的行为，例如 `transition: all 300ms`、`ease-in 480ms`、`animating` 输入锁、缺少速度采样，判断置信度高。
- 对实际延迟、掉帧、触摸手感、浏览器合成、滚动冲突和响应式几何，仅能判定为风险，不能声称已经发生或已经验证。
- 未修改文件，未执行浏览器、模拟器或真机验证。

**Design read：**这是一个供运营人员每天高频使用的 Web 工作面板，整体应当冷静、稳定、可预测；动效只负责维持手指、面板和状态之间的因果关系，首要目标是让用户在 `collapsed / half / full` 之间切换时始终保有控制权和任务上下文。

## 2. 哪些运动应该存在

**应该保留：**

- Pointer-down 时极短、局部的“已抓住”反馈。
- 拖动期间跟随输入的直接位移；这不是补间动画，而是 1:1 状态映射。
- 释放后到 snap point 的短促、可打断 settling。
- 状态改变时必要的 handle、标签、遮罩或层级反馈。

**不应动画：**

- 每一次 `pointermove` 之间不应有 CSS transition。
- 不应使用 `transition: all`。
- 不应动画 `top` 这类布局属性作为手势热路径。
- 不应在按下时缩放整个 sheet，尤其不是 `scale(0.96)`。
- 不应使用固定 `480ms ease-in` 让界面先慢后快。
- 不应在 settle 期间锁死下一次输入。
- sheet 内的任务内容和背景任务上下文不应独立缩放、漂移或弹跳。
- Reduced Motion 下不应有大距离自动滑行、橡皮筋或 overshoot。

## 3. 阻塞发现，按优先级排序

### 1. 拖动不满足直接操控合同

按所示代码，任何发生在 sheet 上的 `pointermove` 都会写入 `top`，没有 `dragging`、有效 `pointerId` 或按键状态检查。

同时：

- `startY` 被记录但没有参与位置计算。
- `top = event.clientY` 没有保留 grab offset，首次移动会把 sheet 顶边吸到指针位置。
- `clientY` 是 viewport 坐标，而 `top` 的坐标系取决于 containing block；两者未被明确统一。
- 没有 `setPointerCapture()`，指针离开 sheet 后无法保证继续收到 move/up。
- `.sheet { transition: all 300ms; }` 会使连续的 `top` 更新被补间，而不是贴住手指。

结果是用户操纵的是一个追赶指针的动画目标，而不是直接抓住的物体。

### 2. settle 期间完全不可打断

`if (animating) return` 明确拒绝用户在 480ms settle 期间重新抓取 sheet。

这对高频操作尤其严重：

- 用户无法即时修正错误释放。
- 快速反向操作被延迟。
- sheet 的逻辑状态优先于用户当前输入，控制权发生反转。
- 动画对象没有保存，无法读取、取消或重定向当前 presentation value。
- `fill: "forwards"` 保持动画效果，但代码没有显式提交最终状态并清理动画所有权；它与后续 inline `top` 更新如何交接尚未被处理。

可拖动 sheet 必须允许在任何运动阶段从当前屏幕位置重新接管。

### 3. 释放物理没有表达用户意图

释放时只执行：

```js
nearestSnapPoint(sheet.offsetTop)
```

缺失：

- 时间/位置历史。
- CSS px/s 的释放速度。
- 速度方向。
- projected endpoint。
- snap hysteresis。
- 当前动画速度的 handoff。

因此慢拖和快速 flick 在同一释放位置会得到同一结果。更糟的是，拖动期间存在 `top` transition，`offsetTop` 还可能对应落后于指针意图的呈现位置。

固定 `480ms ease-in` 也不合适：它在用户刚松手时反应最慢，距离和速度变化却始终使用同一时长。

### 4. 没有边界、手势仲裁或取消模型

给定片段中未见：

- `full` 与 `collapsed` 边界限制。
- 越界渐进阻力。
- `8–12px` 左右的意图阈值。
- 多指过滤。
- `pointercancel` / `lostpointercapture` 恢复。
- handle drag 与 full-state 内容滚动之间的仲裁。

直接采用 `clientY` 意味着 sheet 可以被拖出自然范围。硬 clamp 又会显得撞墙，因此需要有限、可预测的 soft boundary，而不是无限移动或突然停止。

### 5. 按下反馈与无障碍策略均不适合该表面

整个 sheet 使用 `scale(0.96)`：

- 4% 对大型面板不是微反馈，边缘可能产生明显位移。
- 内容和当前任务上下文一起缩放，削弱“抓住 handle”的空间因果关系。
- 该 transform 会与后续推荐的 `translateY()` 产生属性所有权冲突，除非拆分 wrapper。
- `transition: all 300ms` 使按下反馈过慢，可能在手指已经拖动时仍在补间。

同时未见 `prefers-reduced-motion` 分支，因此无法满足“保留状态反馈但避免大范围空间旅行”的要求。

## 4. 八个具体设计动作

1. **建立明确的 pointer-down 所有权。**  
   仅从 drag handle 或规定拖动区开始；记录 `pointerId`、`startPointerY`、当前 sheet presentation Y 和 grab offset，调用 `setPointerCapture()`。在 handle 上提供约 `100–140ms` 的颜色、描边、阴影或 grip 强调，不缩放整个 sheet。

2. **加入意图阈值和完整生命周期。**  
   在约 `8–12 CSS px` 之前仍视为可能的点击；越过阈值后才进入 dragging。move/up/cancel 只接受初始 `pointerId`，并处理 `pointercancel`、`lostpointercapture` 和额外触点。

3. **让拖动成为真正的 1:1 映射。**  
   使用同一坐标空间计算：
   `sheetY = startSheetY + (clientY - startPointerY)`。  
   拖动期间关闭补间，以 `translate3d(0, sheetY, 0)` 或等价单一 transform owner 更新；不要动画 `top`，不要使用 `transition: all`。

4. **支持从 presentation value 中断。**  
   移除 `animating` 输入锁。保存 settle controller；用户重新按下时读取当前屏幕位置和当前速度，取消旧运动，把该 presentation value 设为新的拖动起点，确保没有跳变或回到旧逻辑 target。

5. **测量并交接释放速度。**  
   保存最近约 `60–120ms` 的单调时间戳和 Y 样本，计算明确单位为 CSS px/s 的 release velocity。settle 的初速度来自手势，而不是从零重新启动。

6. **用 projected endpoint 选择状态。**  
   根据当前 Y 和衰减后的速度计算 `projectedY`，再从 `collapsed / half / full` 中选择目标；添加方向性 hysteresis，避免 half 附近轻微抖动导致状态来回翻转，并对极端 projection 做 clamp。

7. **采用克制的边界和 settle 物理。**  
   在 full/collapsed 之外施加渐进阻力，越界距离保持很小；释放后使用近临界阻尼 spring，例如 damping ratio 约 `0.9–1.0`、response 约 `0.3s` 作为调试起点。默认不弹跳，实际时长由距离和速度决定，而不是固定 480ms。

8. **提供独立 Reduced Motion 路径。**  
   保留用户主动拖动的 1:1 跟随，但取消 whole-sheet scale、rubber-band、overshoot 和长距离自动滑行。释放后可直接提交 snap，或仅在剩余距离很小时使用上限约 `80–120ms` 的短 ease-out；同时通过 handle 状态、状态文字、层级/颜色变化和可访问状态属性明确反馈 `collapsed / half / full`。

## 5. 已验证与未验证

**由给定源码直接确认：**

- settle 使用 `480ms`、`ease-in`、`fill: forwards`。
- `animating` 为 true 时 pointer-down 被拒绝。
- pointermove 没有可见的 dragging 或 pointer ID 条件。
- pointermove 直接把 `clientY` 写入 `top`。
- `startY` 在给定代码中没有被使用。
- snap 只基于 `sheet.offsetTop`，没有速度或 projection 输入。
- CSS 使用 `transition: all 300ms`。
- active 状态缩放整个 sheet 到 `0.96`。
- 给定证据中没有 pointer capture、边界阻力、hysteresis 或 Reduced Motion 分支。

**尚未验证：**

- 首次拖动的实际跳变量及 containing block 坐标关系。
- CSS transition、WAAPI 和 `fill: forwards` 在目标浏览器中的最终视觉竞争结果。
- 实际帧率、layout/style 开销、掉帧和长任务。
- 鼠标、触控板、触屏、手写笔之间的行为差异。
- full-state 内容滚动与 sheet drag 的冲突。
- Safari/Chromium 的 pointer capture、cancel 和 viewport 差异。
- 60Hz/120Hz 下的跟随感、速度阈值和 spring 手感。
- Reduced Motion、响应式尺寸和真实设备结果。
- 用户是否能在视觉上持续保有底层任务上下文。

## 6. 实现批准前的最小验证计划

1. **桌面 Chromium 指针测试**  
   覆盖无按下 move、handle 按下、慢拖、快速 flick、离开边界后释放；记录 `{timestamp, pointerY, sheetY, velocityY, projectedY, target}`。确认 grab offset 恒定、非活动指针不移动 sheet。

2. **中断测试**  
   在 settle 的早期、中段和接近结束时重新抓取，并立即反向拖动。验收标准是无输入锁、无位置跳变、无回到旧 target、速度方向连续合理。

3. **边界与滚动仲裁测试**  
   分别越过 full/collapsed 边界，触发 `pointercancel`，并在 full 状态滚动内部内容。确认阻力有限、取消后状态可恢复、内容滚动不会意外拖动 sheet。

4. **Performance trace**  
   在数据内容接近真实负载时录制拖动和 settle。确认手势帧主要更新 transform，没有逐帧 `top` 布局、明显 forced reflow 或长任务；分别观察普通 60Hz 和产品实际支持的高刷新率设备。

5. **Reduced Motion 与响应式**  
   在 `prefers-reduced-motion: reduce` 下完成三个状态的慢拖、flick 和中断；再在至少一个桌面尺寸和一个窄 viewport 检查 snap geometry。确认状态仍清晰，但无大距离自动滑行或弹性运动。

6. **真实触屏门槛**  
   至少在一个产品实际支持的真实触屏设备上测试；若同时正式支持 iOS Safari 与 Android Chrome，应各覆盖一台。重点判断拇指遮挡、滚动冲突、边界阻力、快速反向和重复使用后的疲劳感。