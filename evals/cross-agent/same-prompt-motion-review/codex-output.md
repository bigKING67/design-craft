## 1. 证据等级与设计判断

- **采用**：`design-craft`，`critique` 模式，平台判定为 Web。
- **证据等级**：仅有局部静态源码。它可以证明当前控制流、属性写入和缺失的显式分支；不能证明实际延迟、掉帧、触摸手感或跨浏览器表现。
- **Design read**：这是一个面向高频运营人员的任务型底部面板，气质应当克制、稳定，以不中断上下文的直接操控为第一优先级。
- **结论：阻断实现批准。** 当前问题不是“动效不够精致”，而是拖拽状态机、视觉位置和释放物理没有形成一致的直接操控模型。

## 2. 哪些运动应该存在

**应该保留：**

- 用户控制下的 1:1 拖动；这不是装饰动画，而是输入与结果的因果映射。
- pointer-down 时轻微、即时的手柄反馈。
- 松手后到合法档位的短促、可打断 settle。
- `collapsed`、`half`、`full` 状态变化的清晰视觉和可访问反馈。

**不应该动画：**

- 不应使用 `transition: all`。
- 不应在拖拽热路径动画 `top` 或其他布局属性。
- 不应将整张 sheet 缩放到 `0.96`；它会让大面积内容和边缘脱离手指。
- 不应使用不可打断的固定 `480ms ease-in` 行程。
- sheet 内任务内容不应因为档位切换而重新淡入、缩放或重挂载。
- Reduced Motion 下不应有惯性长行程、橡皮筋、反弹或整面板缩放。

## 3. 优先级阻断项

### 1. P0：当前不是有效的拖拽会话

- `pointermove` 没有检查是否存在活动拖拽，鼠标仅在 sheet 上移动也会写入 `top`。
- `startY` 在给定片段中只写不读，未保存 sheet 初始位置或抓取偏移。
- `top = event.clientY` 把指针视口坐标直接当作 sheet 定位坐标；从非顶边抓取时会跳到手指下方，包含块不等于视口时还会产生坐标系错误。
- 未见 `pointerId`、pointer capture、意图阈值、`pointercancel` 或多指排除。
- 结果是“sheet 追指针绝对位置”，而不是“sheet 位移等于指针位移”。

### 2. P0：禁止打断，而且逻辑位置可能与呈现位置分离

- `if (animating) return` 明确拒绝在 settle 中重新抓取，用户最多被锁住 `480ms`。
- 但 `pointermove` 并未受该锁控制，仍可能修改底层 inline `top`，状态机互相矛盾。
- `fill: "forwards"` 只维持动画效果；片段中没有提交最终样式、更新三档状态、保存 Animation 句柄或清理旧动画。
- 下一次输入应从屏幕当前呈现值开始，而不是旧 inline 值、旧逻辑目标或上一次释放点。

### 3. P1：拖拽、CSS transition 和 WAAPI 在竞争同一个布局属性

- `transition: all 300ms` 会让可插值的 `top` 更新进入 transition，破坏 1:1 跟手。
- pointermove 和 WAAPI 都写 `top`，同时触发布局路径；这是高频手势中的结构性性能风险。
- `480ms ease-in` 起步最慢、到终点仍在加速，随后突然停止；与释放后的减速直觉相反。
- 是否已经出现掉帧或肉眼延迟仍需运行时证据，但当前属性所有权已足以阻断批准。

### 4. P1：没有速度连续性，投影目标语义也未定义

- 目标只根据释放位置的 `nearestSnapPoint(sheet.offsetTop)` 选择。
- 未见位置历史、释放速度单位、速度钳制或将速度交给 settle 的机制。
- 即使产品继续采用“离哪个档位近就去哪个档位”，释放速度也应作为 settle 的初始速度。
- 是否改成 momentum-based projected endpoint 属于产品语义变化，不能把“更物理”自动等同于“更正确”。

### 5. P1：反馈尺度和 Reduced Motion 都不适合高频工具

- `.sheet:active { transform: scale(0.96) }` 缩放的是整张任务面板，并由 `transition: all 300ms` 驱动，反馈过重且滞后。
- 未见 Reduced Motion、软边界、取消恢复或明确的三档状态反馈分支。
- 若后续用 `transform: translateY(...)` 修复拖动，当前 `scale(...)` 还会产生 transform 所有权冲突。

## 4. 八个具体设计动作

1. **建立真实手势会话和 pointer-down 反馈**  
   只在明确的 drag handle/header 上启动；记录活动 `pointerId`、单调时间戳、当前呈现位置、`startClientY` 和 grab offset，并调用 `setPointerCapture()`。手柄立即改变颜色/描边，可选 `scale(0.98)`、`100–140ms ease-out`；不要缩放整张 sheet。手柄使用经过验证的 `touch-action` 策略，避免与内容滚动争抢。

2. **以位移差实现 1:1 跟踪**  
   经过约 `8–12 CSS px` 的意图阈值后，使用  
   `sheetY = startPresentationY + (clientY - startClientY)`；  
   明确所有量都位于同一 CSS-pixel 坐标空间。只接受活动 pointer；保存最新事件并每个显示帧写一次 `translate3d(0, y, 0)`，拖拽期间不应用 transition。

3. **拆分属性所有权**  
   外层 mover 唯一拥有 `translateY`；内层 handle 可以拥有 press `scale`/颜色；任务内容不参与 transform。移除 `transition: all`，只为确实需要的非拖拽属性列出 transition。逻辑状态单独保存为 `collapsed | half | full`。

4. **从呈现值打断 settle**  
   不使用 `animating` 输入锁。保存当前 Animation/spring 句柄；settle 中 pointer-down 时读取当前屏幕 `translateY` 和运动速度，停止旧 settle，将模型同步到该呈现值，再从同一位置接管拖动。完成、取消和异常都通过统一 cleanup/`finally` 清理状态。

5. **独立完成速度交接**  
   保留最近约 `80–120ms` 的 `{y, performance.now()}` 样本，计算并记录释放速度 `v`，单位为 **CSS px/s**，先以例如 `±3000 px/s` 作为待实测的安全钳制值。目标选定后，将 `v` 作为 settle 的初始速度；若动画 API 使用相对速度，则显式转换为 `v / (targetY - currentY)`，并处理零距离情况。

6. **把 projected endpoint 作为受控产品选择**  
   基线先保留现有“离释放位置最近”的语义。若产品确认快速 flick 应影响档位，可实验：  
   `projectedY = clamp(currentY + v * 0.18s, fullY, collapsedY)`，  
   再对 `projectedY` 取最近档位；默认最多跨一个相邻档位，除非产品明确允许从 `collapsed` 一次甩到 `full`。投影只负责选目标，不替代速度交接。

7. **增加软边界、取消路径和克制 settle**  
   合法范围内保持严格 1:1；超过 `full`/`collapsed` 后使用渐进阻力，例如以 `0.55` 为初始 rubber-band 常数。`pointercancel`、`lostpointercapture` 和边界释放都必须收敛到合法状态。settle 使用可打断、可接收初速度的近临界阻尼模型，初始可评估阻尼比 `0.9–1.0`、response `0.28–0.35s`，默认无反弹。

8. **设计独立的 Reduced Motion 路径**  
   保留用户主动控制的 1:1 拖动，因为它维持因果关系；关闭投影惯性、橡皮筋、反弹和长距离自动 settle。释放后立即提交目标几何状态，或只保留不超过 `80–120ms` 的手柄颜色/状态文字交叉淡变。同步更新可见的档位名称及项目既有的可访问状态；若手柄是三档控件，还需提供等价键盘操作和状态文本。

## 5. 已验证与未验证

**由给定源码直接验证：**

- pointer-down 在 `animating` 时返回。
- pointermove 无活动拖拽判断，并直接写 `event.clientY` 到 `top`。
- 给定片段中 `startY` 未被读取。
- 使用 `transition: all 300ms`、整 sheet `scale(0.96)`。
- settle 使用 `top`、`480ms`、`ease-in`、`fill: forwards`。
- 目标由当前 `offsetTop` 的最近档位确定。
- 给定范围内未见 pointer capture、velocity history、projection、soft boundary、pointer-cancel、最终状态提交或 Reduced Motion 分支。

**尚未验证，不应表述成事实：**

- 实际视觉跳动、延迟量、掉帧率或主线程成本。
- `top` 的实际包含块、完整 snap-point 几何和内容滚动仲裁。
- settle 完成后是否在目标位置卡住、回跳或被旧动画遮蔽。
- 项目其他代码是否补充了状态、ARIA、Reduced Motion 或取消处理。
- Chromium、Safari、Firefox 的 computed style/WAAPI 差异。
- 窄屏、横竖屏、60Hz/120Hz 和真实触摸设备手感。

## 6. 实现批准前的最小浏览器/设备验证计划

1. 在主力桌面 Chromium 的真实页面上采集屏幕录制、pointer/presentation-position 日志和 Performance trace；另选支持矩阵中的一个非 Chromium 浏览器复核 WAAPI/transform 行为。
2. 从三个档位分别执行慢拖、快速上下 flick、方向反转，以及在 settle 的约 25%/50%/75% 位置重新抓取；验收为无输入锁、无位置跳变、grab offset 恒定。
3. 测试释放到组件外、`pointercancel`、`lostpointercapture`、第二根手指、手柄点击与 sheet 内容滚动；确认只有获胜手势驱动 sheet。
4. 日志记录 `currentY`、`v CSS px/s`、`projectedY`、chosen target 和 settle initial velocity；核对位置选靶与投影选靶的差异符合已经批准的产品语义。
5. 在窄/宽视口及至少一台真实的主力触摸设备上测试边界、滚动竞争和上下文保持；若支持范围包含 120Hz 设备，补一台 120Hz 验证。
6. 同时进行系统 Reduced Motion 和 `prefers-reduced-motion` 运行：确认无惯性、弹性和大行程自动动画，且 `collapsed`/`half`/`full` 的可见与可访问状态仍然明确。
7. 性能验收应确认拖拽热路径由 transform 驱动、没有归因于手势帧的重复 Layout/长任务，并在代表性数据负载下保持稳定；实际阈值按目标设备刷新率记录。

本次仅完成静态 critique；**未进行浏览器、响应式或真机验证，也未修改任何文件。**