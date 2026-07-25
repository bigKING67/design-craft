# 结论

**暂不批准实现。** 三段式 sheet 的位移反馈有明确因果价值，但当前代码没有建立可靠的手势所有权、1:1 跟随、可中断结算、速度连续性和 Reduced Motion 路径。阻断结论来自静态代码契约，不是对实际帧率或真机手感的断言。

## 1. 证据层级与设计判断

- **评审模式**：`design-craft / critique`，平台为 Web。
- **证据层级**：仅有产品描述和局部静态代码；未运行 route、浏览器、设备或性能工具。
- **静态置信度**：对代码中明确存在或缺失的分支置信度高；对最终视觉手感、事件时序、浏览器合成行为和帧率置信度低。
- **Design read**：这是面向高频日常操作人员的 Web 运营工作台，以冷静克制的三段式直接操控维持任务上下文，而不是用动效制造表现力。

## 2. 哪些运动应该存在

**应该保留：**

- pointer-down 时对拖拽把手提供即时、微弱的确认反馈。
- 拖拽阶段让 sheet 与指针保持直接的空间因果关系。
- 释放后进行短促、可中断、继承速度的 snap settle，用于解释最终落在哪个状态。
- `collapsed / half / full` 的可见和程序化状态反馈。

**不应该动画：**

- 指针移动本身不应经过 `300ms` transition；它是直接映射，不是补间动画。
- 不应动画 `top`，也不应使用 `transition: all`。
- 不应把整个任务 sheet 缩放到 `0.96`；这会让内容和上下文一起收缩。
- 不应使用固定 `480ms ease-in` 处理高频释放动作。
- Reduced Motion 下不应出现大幅自动位移、惯性投射、弹性回弹或 overshoot。

## 3. 阻断发现

| 优先级 | 发现 | 直接操控 / 物理问题 |
|---|---|---|
| **P0 / B1** | `pointermove` 和 `pointerup` 没有检查 active drag、`pointerId` 或按下来源；`startY` 在所示代码中未被使用，也没有 pointer capture、`pointercancel` 或 `lostpointercapture` 清理。 | 仅把指针移过 sheet 就可能改写位置；离开元素后又可能丢失事件。手势没有明确所有者，不能形成可靠状态机。 |
| **P0 / B2** | 每次移动直接执行 `top = event.clientY`，没有 grab offset，也未把 viewport 坐标转换到 sheet containing block；同时 `transition: all 300ms` 会覆盖 `top` 变化。 | sheet 顶边可能跳到手指位置，并以约 300ms 追赶指针，而不是保持抓取点 1:1 跟随。`top` 还会进入 layout 热路径。 |
| **P0 / B3** | settle 时用 `animating` 拒绝新的 `pointerdown`；动画实例未保存，无法从当前 presentation value 中断。`fill: "forwards"` 后也没有明确 commit 最终状态并 cancel effect。 | 可抓取对象被锁定 480ms；重新抓取不能从当前屏幕位置和速度继续。底层 inline style、逻辑状态和持续的 WAAPI effect 存在分叉风险。 |
| **P1 / B4** | 固定 `480ms ease-in`、只按 release position 取最近 snap、没有速度采样或 initial-velocity handoff，拖拽范围也未约束。 | `ease-in` 在用户最关注的开头反而最慢；释放速度突然归零。快速 flick 与慢速释放无法获得连贯结果，sheet 还能越过自然边界。投射是否影响目标属于产品语义，当前证据不足以擅自改变。 |
| **P1 / B5** | 整个 `.sheet:active` 缩放至 `0.96`，且没有所示 Reduced Motion 分支。 | 高频运营界面会产生不必要的内容缩放和上下文位移；如果后续拖拽改用 `transform`，缩放与平移还会争夺同一属性。无障碍要求尚未落实。 |

## 4. 八个具体设计动作

1. **建立手势所有权和 pointer-down 反馈**  
   只允许 primary pointer 从明确的 drag handle 启动；记录 `pointerId`，调用 `setPointerCapture()`，在 `pointerup`、`pointercancel`、`lostpointercapture` 中统一清理，并忽略后续触点。仅在 handle 上配置合适的 `touch-action`，不要阻断 sheet 内容区的纵向滚动。按下时让 handle 在 `100–140ms` 内改变颜色/不透明度，或仅让 handle 子层缩放到约 `0.98`；不要缩放整个 sheet。

2. **保存 grab offset，并明确坐标空间**  
   pointer-down 时从当前屏幕位置计算  
   `grabOffset = pointerY - presentationY`。  
   所有采样统一使用 viewport CSS px 和单调时间戳；若最终写入 containing-block 坐标，先用其 `getBoundingClientRect()` 显式转换。经过约 `8–12 CSS px` 的方向意图阈值后，位置使用 `pointerY - grabOffset`，避免 sheet 跳到手指下方。

3. **让拖拽真正 1:1**  
   范围内 sheet 位移增量应等于指针位移增量；一帧只写一次 compositor-friendly `translateY(...)`。拖拽期间不使用 transition，不读取 `offsetTop` 进行逐帧布局计算，也不动画 `top`。删除宽泛的 `transition: all`，把 handle 的反馈 transform 放在独立子层，避免与 sheet translation 冲突。

4. **从 presentation value 中断，而不是锁输入**  
   保存 settle animation/spring 的位置和速度状态。新的 pointer-down 到来时，读取当前屏幕上的 translation 和当前 settle velocity，停止旧 settle，并以该值作为新 drag 起点；删除 `animating` 输入锁。到达 snap 后，把最终位置和 `collapsed / half / full` 写入 canonical state，再清除临时 animation effect，不依赖永久 `fill: forwards`。

5. **分开处理速度测量、目标选择和速度交接**  
   保存释放前约 `80–120ms` 的位置历史，用 monotonic timestamp 计算纵向速度，单位明确为 **CSS px/s**，向下为正。先按产品规则选择 target，再把有上限的实测速度传给 settle；若 API 要求相对速度，使用 `velocity / (target - current)` 并处理零距离。冷静工具界面建议先试无 overshoot、接近临界阻尼的 spring，响应尺度约 `0.25–0.30s`，而非固定 480ms。

6. **把 projected endpoint 作为显式产品实验，而非暗改语义**  
   当前先保留 `nearestSnapPoint(current)`。若产品确认快速 flick 应推进到相邻状态，可审计候选为：  
   `projected = clamp(current + clamp(v * 0.18s, -oneSnapSpan, +oneSnapSpan), fullY, collapsedY)`  
   其中 `v` 为 CSS px/s；再从 `projected` 选择最近合法 snap。记录 horizon、速度上限、snap-range clamp 和是否允许跨越多个状态。无论是否启用投射，释放速度都仍应交给 settle。

7. **增加软边界和方向迟滞**  
   在 `[fullY, collapsedY]` 内保持 1:1；越界后使用渐进阻力，例如以 `constant ≈ 0.55` 的 rubber-band 函数起步，并把可见 overshoot 暂定限制在约 `24 CSS px`，等待真机调校。释放时始终回到合法 snap；边界外不得生成第四个隐式状态。Reduced Motion 下可以直接 hard clamp，避免弹性回返。

8. **提供非空间型 Reduced Motion 状态反馈**  
   `prefers-reduced-motion: reduce` 下保留用户主动控制的 1:1 跟随，但关闭 projected momentum、overshoot 和大距离自动 settle；释放时立即提交最近合法状态，或仅使用不超过约 `80–120ms` 的 handle 颜色/透明度和状态标签 cross-fade。最终状态应通过可见文本及组件既有的 ARIA 状态表达；只在 snap 完成后更新，避免拖动过程中连续播报，并保持焦点和任务内容不变。

## 5. 已验证与未验证

**由所给代码直接验证：**

- `pointermove` 没有 active-drag guard，会对送达 sheet 的每个 move 写入 `top`。
- `pointerup` 没有验证它是否属于已启动的 drag。
- `startY` 在所示逻辑里只写不读。
- 所示代码没有 pointer capture、pointer identity、cancel 清理、速度历史、范围约束或 Reduced Motion 分支。
- 位移使用 `top`；CSS 使用 `transition: all 300ms` 和整 sheet `scale(0.96)`。
- settle 使用 `480ms`、`ease-in`、`fill: forwards`，目标仅来自 `nearestSnapPoint(sheet.offsetTop)`。
- 新 pointer-down 在 `animating` 期间被拒绝；动画实例没有被保存、commit 或 cancel。

**仍未验证，不能据此宣称：**

- sheet 的实际 positioning context，以及 `clientY` 与 `top` 在当前 DOM 中的具体偏差。
- CSS transition、WAAPI animation cascade 和 `offsetTop` 在目标浏览器中的实际 presentation 行为。
- 是否真的出现跳动、滞后、卡帧、重排峰值、旧 fill effect 覆盖 inline style或下一次拖拽冻结。
- snap 点、内部滚动、背景遮罩和状态语义是否在未提供代码中另有补偿。
- `prefers-reduced-motion` 是否在其他样式或组件层处理。
- 响应式、小屏、触控冲突、60/120Hz 手感及真实设备表现。
- 因此本次没有浏览器、截图、trace、模拟器或真机验证结论。

## 6. 批准前的最小浏览器 / 设备验证计划

1. **加入临时观测**：记录每帧的 monotonic time、pointer Y、presentation Y、release velocity、projected endpoint、selected target 和 canonical state；不要只记录事件回调值。
2. **受支持的 Chromium + Safari/WebKit**：分别验证无按下移动、任意抓取点拖动、越出元素、`pointercancel`、第二触点、快速反向、settle 中重新抓取。通过标准：未启动 drag 时零位移；阈值后几何跟随误差约 `≤1 CSS px`，展示延迟不超过一帧；重新抓取没有视觉跳跃。
3. **释放矩阵**：在同一 release position 做慢速、快速向上和快速向下释放。确认 target 严格符合选定产品语义；settle 起始速度连续、无停顿后重启、无意外反向，projected endpoint 始终被合法范围约束。
4. **边界、滚动和响应式**：至少测试桌面和窄屏高度，覆盖三个 snap、full 状态内容滚动、上下越界、viewport resize/地址栏变化，并确认关键任务内容和操作始终可达。
5. **Reduced Motion**：通过浏览器媒体模拟和一台启用系统 Reduce Motion 的触控设备各跑一次；确认无惯性投射、弹性 overshoot 或大幅自动 travel，同时状态标签、ARIA 状态和焦点仍正确更新。
6. **真实触控与性能**：至少一台 iOS Safari 和一台 Android Chrome，按项目支持范围覆盖 60Hz；若高刷新设备属于正式支持范围，再加一台 120Hz。以代表性业务负载录制 Performance trace 和短视频，确认拖拽热路径没有同步 layout/长任务，并保留 trace、视频、设备/刷新率及 hash 作为批准证据。