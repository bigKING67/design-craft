# Codex observed output

- Agent: Codex CLI
- Version: `codex-cli 0.144.1`
- Date: 2026-07-10
- Command summary: `codex exec -C <repo> -s read-only --ephemeral -o /tmp/design-craft-motion-codex.md with the source skill path`
- Skill path observed: `/Users/gaoqian/Documents/sixseven/codeproject/design-craft/skills/design-craft`
- Evidence boundary: read-only prompt/source review; runtime behavior remains unverified.
- Benchmark contract: output includes concrete design move recommendations.

## Output

## 1. Evidence level 与 design read

- **Evidence level：`L0 / static-source only`。**现有 Evidence 仅包含产品上下文和静态代码；没有 pointer trace、computed style、frame timeline、Reduced Motion、响应式或真实触屏设备证据。
- **Design read：**`Reading this as: a high-frequency web operations bottom sheet for operators, with calm utility motion, optimized for direct manipulation and preserving task context across collapsed, half, and full states.`
- **结论：Block。**底部 Sheet 需要因果明确的直接操控与短促归位，但当前实现破坏了 1:1 跟手、可打断性、速度连续性和 Reduced Motion 要求，不应批准实现。

## 2. 哪些 motion 应存在，哪些不应动画

### 应存在

1. pointer-down 时立即出现轻量、非位移型的抓取反馈。
2. 拖动时 Sheet 与指针保持 1:1 位置关系；这是直接操控，不是独立播放的动画。
3. 松手后从当前屏幕位置短促归位到 `collapsed`、`half` 或 `full`。
4. Sheet handle、遮罩透明度或状态标识可以按拖动进度连续变化，但必须与 Sheet 位置绑定，而不是另行播放。
5. 到达外边界后的轻微阻尼可以帮助表达边界，但在 calm utility UI 中不应出现娱乐性弹跳。

### 不应动画

1. 拖动阶段不应对位置应用 `transition`、easing 或固定时长；否则 Sheet 会追赶指针，而不是跟随指针。
2. 不应动画 `top`，也不应使用 `transition: all`；应让专用 motion layer 使用 `translateY`。
3. 不应在抓取时将整个 Sheet `scale(0.96)`。它会缩放内容、改变触点与视觉几何关系，并制造不必要的任务上下文扰动。
4. 不应使用固定 `480ms ease-in` 归位。`ease-in` 在松手后先慢后快，削弱即时响应；固定时长也无法表达不同距离和释放速度。
5. Sheet 内部内容不应在拖动时缩放、模糊、淡出或反复重排。
6. Reduced Motion 下不应保留惯性投射、弹性越界、大幅自动滑行或 overshoot。

## 3. 优先级 findings

### P0 — pointer 生命周期不成立，无法保证直接操控

`pointermove` 没有检查当前是否处于 dragging，也没有检查 `pointerId`。因此，只要 Sheet 收到 pointer move，就会执行：

```js
sheet.style.top = `${event.clientY}px`;
```

`startY` 被记录但从未使用；没有保存 Sheet 起始位置，也没有保存抓取偏移量。结果是 Sheet 顶边被直接映射到 `clientY`，而不是保持用户实际抓住的位置：

```text
grabOffset = pointerY - presentationTop
nextTop = pointerY - grabOffset
```

此外，没有 `setPointerCapture()`、`pointercancel` 或 `lostpointercapture` 处理。指针离开 Sheet、浏览器接管触摸滚动、系统取消手势或出现第二个触点时，交互状态可能失去一致性。

### P0 — `transition: all` 直接破坏 1:1 tracking

每次 `pointermove` 都写入 `top`，而 `.sheet` 同时声明：

```css
transition: all 300ms;
```

这意味着拖动位置可能被 300ms transition 插值，Sheet 会滞后于手指。它还允许任何未来属性意外进入动画，并让 CSS transition 与 WAAPI 同时竞争 `top` 的控制权。

`top` 是 layout property；逐帧写 `top`，随后读取 `offsetTop`，会把布局计算放进手势热路径。静态代码能确认存在该风险，但实际掉帧程度仍是 **unverified**。

### P0 — settling 完全不可打断

```js
if (animating) return;
```

明确禁止用户在归位过程中重新抓住 Sheet。对可直接操控对象，这是核心交互错误：用户看到的对象仍在运动，却不能接管它。

正确的 presentation-value interruption 应当：

1. 从当前屏幕上实际显示的位置重新接管，而不是从旧逻辑目标开始。
2. 取消当前 settle，但不产生视觉跳变。
3. 将当前运动速度传递给新的拖动或新目标。
4. 支持 `settling -> dragging`，而不是用布尔锁阻断输入。

当前代码既没有保存 animation 实例，也没有读取 presentation position 或 current velocity。

### P0 — `fill: "forwards"` 产生显示状态与底层状态分离

WAAPI 动画结束后，`fill: "forwards"` 会继续保留动画效果，但代码没有把 `target` 提交给持久位置状态，也没有清理动画：

```js
sheet.animate(..., { fill: "forwards" })
```

因此，屏幕显示位置可能已经在 `target`，但底层 `style.top` 仍是松手位置。后续指针写入、CSS transition 和新的 WAAPI animation 会面对多个位置真源，存在重新抓取跳变或输入看似无效的风险。

### P1 — snap 选择忽略释放速度和 projected endpoint

当前目标仅由松手时的 `offsetTop` 决定：

```js
nearestSnapPoint(sheet.offsetTop)
```

这会让同一松手位置上的慢放与快速 flick 得到同一结果，无法保留手势意图。应记录短时间的位置历史，计算 release velocity，并基于 projected endpoint 选择状态：

```text
projectedEndpoint = current + boundedProjection(releaseVelocity)
target = nearestSnapPoint(projectedEndpoint)
```

投射必须被边界和产品策略限制。对于需要保持任务上下文的运营界面，可以默认限制一次释放最多跨越一个相邻状态，除非真实使用证据证明跨多状态 flick 更高效。

### P1 — 归位速度曲线与产品语气不符

`480ms ease-in` 有三个问题：

1. 松手后的初始响应最慢，与用户刚刚施加的速度不连续。
2. 归位末端加速，视觉上像被目标吸走，而不是自然停止。
3. `animating` 在整个 480ms 内锁住重新抓取，放大了高频操作成本。

更适合的起点是无明显 bounce、接近临界阻尼的 interruptible spring，例如 damping ratio `0.9–1.0`、response 约 `0.25–0.35s`。这些只是调参起点，最终值需要真实 pointer trace 和设备观察。

### P1 — 没有 soft boundaries、intent threshold 或 hysteresis

当前实现允许 `clientY` 直接决定位置，没有：

- 拖动意图阈值；
- `full` 上界与 `collapsed` 下界的渐进阻力；
- 松手后的边界回弹；
- 状态阈值 hysteresis；
- pointer cancel 后的安全归位。

外侧边界应使用 progressive resistance，而不是无限拖出屏幕或突然硬停。`half` 等内部 snap point 应是目标而不是物理墙，拖动经过时不应卡住。

### P1 — Reduced Motion 路径在提供的 Evidence 中缺失

现有代码没有显示任何 `prefers-reduced-motion` 分支。Reduced Motion 不应删除用户主动控制的 1:1 拖动，但应减少松手后的自动空间移动：

- 禁用或大幅限制速度投射；
- 移除 rubber-band overshoot 和 bounce；
- 不使用 Sheet-wide scale；
- 归位到最近状态，采用即时更新或非常短、无 overshoot 的 settle；
- 用 handle 色彩、状态文字或其他静态反馈确认 `collapsed`、`half`、`full` 状态。

### P2 — pointer-down feedback 使用了错误对象和幅度

```css
.sheet:active {
  transform: scale(0.96);
}
```

整个 Sheet 缩小 4% 会让内容、边缘和触点关系一起变化。它不是“抓住 handle”的反馈，而像整张界面被按压。由于 `transition: all 300ms`，这一反馈还可能出现得过慢。

更合适的是只改变 handle 或 header 的局部属性，例如 handle tone、轻微 elevation、`cursor: grabbing` 或高对比 active state；Sheet 几何保持不变。

## 4. Concrete design move

| 需求 | Concrete design move | 预期结果 |
|---|---|---|
| Pointer-down feedback | 仅允许专用 drag handle 发起拖动；检查 primary pointer；若正在 settling，先接管当前 presentation value；保存 `pointerId` 和 `grabOffset`；调用 `setPointerCapture()`。立即改变 handle tone、elevation 或 grabbing cursor，不缩放整个 Sheet。只在 handle 上设置合适的 `touch-action`，不要禁止 Sheet 内容区正常滚动。 | 按下立即有反馈，内容和触点不发生几何位移。 |
| 1:1 tracking | 使用 `dragging` 状态和 active `pointerId`；经过约 `8–12px` 的方向意图阈值后，计算 `rawY = pointerY - grabOffset`。用 `requestAnimationFrame` 合并高频事件，并在专用 wrapper 上写 `translate3d(0, y, 0)`。拖动期间禁用位置 transition。 | Sheet 始终附着在抓取点上，没有追赶感，也不会仅因 hover/pointer move 而移动。 |
| Presentation-value interruption | 用 `idle / dragging / settling` 状态机替代 `animating` 锁。pointer-down 发生在 settle 中途时，读取当前屏幕位置和当前速度，停止 settle，将该 presentation position 作为新的 drag baseline。若继续使用 WAAPI，必须保存 Animation、提交当前样式后取消；更稳妥的是使用拥有 position/velocity 状态的 interruptible spring。不要依赖永久 `fill: forwards`。 | 用户可随时重新抓取，接管时无跳变，显示位置与逻辑状态保持单一真源。 |
| Velocity handoff | 保存最近约 `60–100ms` 的时间/位置样本，必要时读取 coalesced pointer events；从多个样本计算 px/s 速度，而不是使用单个事件。把 release velocity 作为 settle spring 的初始速度；中途重新定向时也保留当前 velocity。 | 快速 flick 与慢速放手产生不同但连续的结果。 |
| Projected endpoints | 先基于 release velocity 计算有界 projected endpoint，再选择最近 snap point；投射值必须 clamp 到安全范围，并结合移动方向和状态 hysteresis。低速时倾向最近状态，高速时允许进入相邻状态；是否允许一次跨越两个状态需要产品证据。 | snap 结果反映手势意图，而不是只看松手坐标。 |
| Soft boundaries | 仅在 `full` 和 `collapsed` 外侧使用渐进 rubber-band resistance；可以从常数约 `0.55` 的压缩函数开始调试。内部 `half` 状态不设硬墙。释放或 `pointercancel` 后，从当前位置无跳变地 settle 回合法范围。 | 用户能够感知边界，但不会突然撞墙或把 Sheet 拖出可恢复范围。 |
| Reduced Motion | 保留用户主动控制的 1:1 拖动；关闭 Sheet-wide scale、惯性长投射、弹性 overshoot 和 bounce。松手后优先选择最近状态，使用即时提交或约 `80–150ms`、无 overshoot 的短 settle；程序化跨状态变化可即时更新位置，并通过 handle/state label 的短色彩或 opacity 反馈确认结果。 | 状态变化仍清晰，但不会产生大幅、非用户控制的空间旅行。 |

建议的位置控制流程是：

```text
pointerdown:
  presentationY = currentVisiblePosition()
  interruptSettleWithoutJump()
  activePointer = pointerId
  grabOffset = pointerY - presentationY
  capturePointer()

pointermove:
  ignore unless pointerId == activePointer
  rawY = pointerY - grabOffset
  displayY = applyOuterBoundaryResistance(rawY)
  renderWithTranslateY(displayY)
  appendVelocitySample(time, displayY)

pointerup / pointercancel:
  velocity = estimateRecentVelocity()
  projectedY = clamp(project(displayY, velocity))
  target = chooseSnapWithHysteresis(projectedY, velocity)
  settleFrom(displayY, velocity, target)
```

## 5. Verified 与 unverified

### Verified from the supplied static code

- `pointermove` 没有 dragging 或 `pointerId` guard。
- `startY` 被赋值但没有参与位置计算。
- 没有 pointer capture、`pointercancel` 或 velocity history。
- Sheet 的位置由 `event.clientY` 直接写入 `top`，无法保留任意抓取偏移。
- `.sheet` 使用 `transition: all 300ms`。
- active 状态请求对整个 Sheet 使用 `scale(0.96)`。
- release 使用 `offsetTop` 的最近 snap point，没有 projected endpoint。
- settle 使用固定 `480ms ease-in`。
- `animating` 阻止 settle 期间的 pointer-down。
- WAAPI 使用 `fill: "forwards"`，但没有提交持久目标位置或清理动画。
- 提供的代码中没有 Reduced Motion 分支。

### 当前仍为 unverified

- 实际浏览器中 Sheet 跳变或滞后的像素幅度。
- CSS transition、WAAPI 和其他未提供样式之间的最终优先级表现。
- `top` 更新在真实 Sheet 内容量下造成的 frame drop、layout 或 paint 成本。
- pointer 离开元素、触屏滚动、第二触点和系统取消时的实际行为。
- 不同释放速度是否能被用户稳定控制。
- snap point 在窄视口、软键盘、旋转或动态 viewport 下是否正确。
- `480ms` 在目标设备上的主观体感。
- Reduced Motion 的真实运行结果。
- iOS Safari、Android Chrome、60Hz 或 120Hz 设备上的触摸手感。

## 6. 实现批准前的最小浏览器／设备验证计划

1. **桌面 Chromium 基线**
   - 使用真实页面和代表性运营内容。
   - 记录 `pointerY`、presentation `getBoundingClientRect().top`、grab offset、release velocity、projected endpoint 和最终 state。
   - 验证按下后没有位置跳变；越过 intent threshold 后，grab-offset 误差持续稳定且没有 300ms 追赶。
   - 将指针拖出 handle/Sheet 边界，确认 pointer capture 仍保持跟踪。
   - 在没有 pointer-down 时移动鼠标，确认 Sheet 完全不动。

2. **Interruption 测试**
   - 分别在 settle 约 25%、50%、75% 进度时重新抓取。
   - 快速执行 `drag → release → regrab → reverse → release`。
   - 验收条件：从当前屏幕位置接管，无一帧跳回旧目标，无输入锁死，反向时速度连续。

3. **Velocity 与 snap 测试**
   - 从相同释放位置分别执行慢速放手、快速向上 flick、快速向下 flick。
   - 验证低速选择最近状态，高速结果反映方向和 projected endpoint。
   - 在 snap 阈值附近反复小幅移动，确认 hysteresis 防止状态抖动。
   - 验证异常高速度经过 clamp 后不会越过安全边界或意外跨越过多状态。

4. **Boundary 与取消测试**
   - 超出 `full` 和 `collapsed` 外边界拖动，检查阻力是否渐进、松手是否平稳返回。
   - 测试 `pointercancel`、失焦、窗口边缘、第二触点以及内容区滚动。
   - 确认只有 drag handle 接管垂直拖动，Sheet 内可滚动内容仍可正常滚动。

5. **Reduced Motion**
   - 使用 DevTools media emulation，并至少在一个启用系统 Reduced Motion 的实际环境复核。
   - 验证主动拖动仍是 1:1；没有 Sheet scale、长距离惯性、elastic overshoot 或 bounce。
   - 验证状态仍通过稳定的 handle、状态文字或等价非大幅位移反馈表达。
   - 检查焦点和任务上下文在三个状态间保持稳定。

6. **性能与真实触屏**
   - 在代表性数据负载下录制 Performance trace，确认 pointer hot path 不逐帧读取布局、不动画 `top`，主要更新为 compositor-friendly transform。
   - 至少在一个真实触屏设备上测试；若产品明确支持 iOS Safari 和 Android Chrome，则两者都必须覆盖。
   - 若交互手感对发布关键，补充 60Hz 与 120Hz 对比。
   - 保存短视频或 frame timeline、pointer trace、Performance trace、浏览器／设备版本和 Reduced Motion 设置作为批准 Evidence；在这些检查完成前，交互质量保持 **unverified**。
