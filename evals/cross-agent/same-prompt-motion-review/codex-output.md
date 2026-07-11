## 结论

**Evidence level：`L0 static`，context-informed。**

本次只有产品上下文和静态代码，没有截图、DOM/computed style、pointer trace、动画时间线、响应式状态或真机触控证据，因此不能升级到 `L2 browser` 或 `L3 resilient`。

**设计判断：Block，不建议按当前实现批准。**

问题不只是“480ms 有点慢”，而是当前实现没有建立可靠的直接操控模型：

- 非拖拽状态下的 `pointermove` 也会移动 sheet。
- 拖动位置没有保留抓取偏移，sheet 会尝试把自身 `top` 对齐到指针的 viewport Y。
- `transition: all 300ms` 会把逐帧拖动变成追赶指针的补间动画。
- 松手后的动画不可中断，也没有速度交接和 projected endpoint。
- 使用 `top` 驱动布局，且状态由 `fill: "forwards"` 暂时覆盖，没有清晰提交到持久位置。
- `.sheet:active { scale(0.96) }` 会让整个任务上下文在拖动时缩小并脱离手指，不符合 calm utility UI。
- Reduced Motion 在给出的证据中没有处理。

---

# 1. Evidence level 与 design read

### Evidence level

`L0 static`：

- 已检查：用户提供的产品语境、JavaScript 和 CSS。
- 未检查：实际 DOM、完整事件注册范围、computed style、手势轨迹、帧时间线、响应式、Reduced Motion、触控滚动竞争、浏览器差异、60/120 Hz 真机表现。
- 因而以下判断分为：
  - **源码可直接确认的实现事实**
  - **由实现推导出的高概率风险**
  - **必须运行时验证的体验结论**

### Design read

> Reading this as: 一个全天高频使用的 Web 运营工具，为需要持续保持任务上下文的操作人员提供三段式 bottom sheet；整体应当安静、确定、可预测，动效只用于维持手势因果关系和空间连续性。

由此得到的运动原则：

1. **手指控制阶段必须直接，不应有“动画感”。**
2. **松手后的 settle motion 可以存在，但必须短、可中断、继承速度。**
3. **高频操作不应伴随整体缩放、弹跳或装饰性过渡。**
4. **状态变化需要明确，但不能以牺牲任务上下文稳定性为代价。**

---

# 2. 哪些 motion 应该存在，哪些不应该动画

## 应该存在

### A. 手势直接追踪

拖动过程中的 sheet 位移需要存在，但它不是传统意义上的补间动画，而是：

- pointer position → sheet presentation position 的直接映射；
- 每个显示帧更新一次；
- 保留最初抓取点；
- 不使用 CSS transition 追赶输入。

这是维持直接操控因果关系的必要运动。

### B. 松手后的 snap settle

从松手位置进入 `collapsed`、`half` 或 `full` 应有一个短促 settle：

- 从当前屏幕位置开始；
- 继承松手速度；
- 允许用户在中途重新抓住；
- 默认无弹跳或接近临界阻尼；
- 典型起点可用：
  - damping ratio：约 `0.9-1.0`
  - response：约 `0.25-0.35s`

这些只是初始调参范围，必须通过真实手势验证，不是已验证参数。

### C. 与位置连续关联的辅助反馈

如果存在 scrim、阴影、drag handle 或状态标题，可以随 sheet 位置连续变化：

- scrim opacity 根据展开进度插值；
- shadow/elevation 在离开 collapsed 状态时轻微增强；
- handle 颜色或粗细用于表示已抓取；
- 状态标签在 snap 完成时更新。

这些变化应从同一个归一化进度派生，不应各自运行互相错位的固定时长动画。

---

## 不应该动画

### A. 不应对 `.sheet` 使用 `transition: all`

拖动热路径中的 `top`、尺寸、颜色、transform 等不应全部被一个 300ms transition 接管。

应删除：

```css
.sheet {
  transition: all 300ms;
}
```

至少不能在拖动状态下存在这种规则。更理想的是：

- sheet 位置完全由交互动画系统控制；
- CSS transition 只用于明确列出的非位置属性；
- 拖动期间禁用任何会造成位置滞后的补间。

### B. 不应缩放整个 sheet

当前：

```css
.sheet:active {
  transform: scale(0.96);
}
```

不适合这个组件：

- 整个任务上下文会明显缩小；
- sheet 边缘与手指之间产生视觉脱离；
- 缩放中心若在中央，顶部抓取点会发生额外位移；
- `transform` 同时需要承担 sheet 的平移，缩放会增加 transform 合成和中断复杂度；
- 高频运营场景中，4% 缩放过强，带有按钮式或娱乐式反馈。

建议不缩放 sheet 本体。pointer-down 反馈放在 drag handle、cursor、阴影或局部颜色上。

### C. 不应动画内部任务内容

拖动和 snap 时，不应对以下内容单独做 stagger、scale、fade：

- 表单字段；
- 数据表；
- 操作按钮；
- 标题和正文；
- 当前选中项；
- 用户正在查看或编辑的任务内容。

它们应该随 sheet 作为一个稳定空间整体移动，避免用户失去视觉锚点。

### D. 不应用 `top` 作为主要逐帧运动属性

`top` 会改变布局位置。对于频繁 pointer update，更合理的是：

```css
transform: translate3d(0, var(--sheet-y), 0);
```

或者由 JavaScript/动画库直接更新 `transform`。

这可以减少 layout hot path 风险。当前是否已经产生掉帧没有运行时证据，不能声称“已发生 jank”，但静态实现存在明显性能风险。

---

# 3. 按优先级排列的发现

## P0：`pointermove` 没有拖动状态门控

当前：

```js
sheet.addEventListener("pointermove", (event) => {
  sheet.style.top = `${event.clientY}px`;
});
```

这里没有检查：

- 是否发生过有效的 `pointerdown`；
- 是否是当前 active pointer；
- 是否超过手势意图阈值；
- 是否正在处理另一个 pointer；
- 是否是合法拖动区域。

因此，从提供的源码可以直接确认：**任何到达该 listener 的 `pointermove` 都会尝试修改 sheet 的位置。**

对鼠标而言，仅在 sheet 上移动指针就可能触发。对触控而言，其他 pointer sequence 也没有被明确排除。

这是功能正确性问题，不只是 motion polish。

### 设计影响

用户不能建立“只有抓住后才移动”的稳定因果模型。一个直接操控对象必须明确区分：

1. idle；
2. possible drag；
3. dragging；
4. settling；
5. interrupted/re-grabbed。

当前代码基本只有一个不完整的 `animating` 布尔值。

---

## P0：没有保留 grab offset，sheet 会向手指跳变

代码记录了：

```js
startY = event.clientY;
```

但 `startY` 没有被后续使用。

移动时直接设置：

```js
sheet.style.top = `${event.clientY}px`;
```

这意味着实现要求：

```text
sheetTop = pointerViewportY
```

而直接操控应当是：

```text
sheetTop = pointerViewportY - initialGrabOffset
```

其中：

```text
initialGrabOffset = pointerDownY - sheetPresentationTop
```

如果用户在 handle 中间或 sheet 内部某处按下，当前逻辑不会保持这个相对位置。源码能够确认“没有保留抓取偏移”；具体视觉跳动幅度取决于实际 sheet 位置、点击位置和 CSS，因此需要运行时量化。

---

## P0：`transition: all 300ms` 破坏 1:1 tracking

每次 `pointermove` 都改变 `top`，而 `.sheet` 又声明：

```css
transition: all 300ms;
```

因此浏览器可能持续把每一个新的 `top` 当作新的 transition target。结果不是对象贴着手指，而是对象不断追赶最新指针位置。

直接操控要求：

```text
pointer delta ≈ sheet delta
```

当前结构更接近：

```text
pointer delta → 300ms interpolation toward target
```

用户会感到：

- 拖动有重量但不是物理重量，而是输入延迟；
- 快速反向时 sheet 拖尾；
- 松手位置与实际屏幕位置可能不一致；
- snap target 可能基于逻辑位置而不是用户看到的位置。

这在手势 sheet 中属于阻断级问题。

---

## P0：动画期间拒绝新手势，违反 presentation-value interruption

当前：

```js
if (animating) return;
```

松手后 480ms 内，新的 `pointerdown` 被忽略。

一个可直接抓取的 sheet 必须允许用户在 settle 尚未结束时重新抓住。正确语义是：

1. 读取当前屏幕上的 presentation position；
2. 读取或估计 settle animation 当前速度；
3. 停止自动 settle；
4. 以当前位置和当前速度进入新手势；
5. 不产生跳变。

当前实现把对象锁住，直到动画完成。用户看到 sheet 正在移动，却不能重新控制它，这会打破直接操控感。

更严重的是，代码只在 `pointerdown` 上检查 `animating`，但 `pointermove` 并未检查它。也就是说，锁定策略本身并不一致：

- pointerdown 被拒绝；
- pointermove 仍会修改 inline `top`；
- WAAPI 的 `top` 动画与 inline style 改动可能同时存在。

具体合成结果依赖运行时和完整样式，尚未验证，但状态模型本身已经不可靠。

---

## P0：没有 pointer capture、pointer identity 和 cancel 路径

当前没有证据表明存在：

```js
sheet.setPointerCapture(event.pointerId);
```

也没有：

- `activePointerId`；
- `pointercancel`；
- `lostpointercapture`；
- 多触点过滤；
- 拖动生命周期清理。

如果指针离开 sheet 边界，`pointerup` 是否仍被当前元素收到不能依赖偶然行为。触控被系统滚动、通知手势或浏览器手势取消时，也需要恢复到稳定 snap state。

直接操控组件必须保证：

- 开始拖动后持续收到对应 pointer 的事件；
- 只处理最初的 pointer；
- cancel 后不会悬停在任意中间位置；
- animation/drag flags 一定清理。

---

## P1：480ms `ease-in` 与高频操作场景不匹配

当前：

```js
{ duration: 480, easing: "ease-in", fill: "forwards" }
```

存在两个问题。

### 480ms 太慢

Bottom sheet 的一次完整展开可能允许比按钮更长的运动，但这是全天反复使用的运营工具。每次松手锁定接近半秒，会累积为明显等待。

设计目标应更接近：

- 响应立即开始；
- 常规 snap 在约 `200-350ms` 的感知范围内稳定；
- 距离短则更快；
- 速度高则根据初速度自然收敛；
- 不使用固定 duration 让短距离和长距离都耗时 480ms。

### `ease-in` 起步最慢

用户松手后最关注的正是开始阶段。`ease-in` 会先慢后快，产生：

- 松手后短暂停顿感；
- 后半程突然加速；
- 到终点时仍带较高速度，停止显得生硬。

对于非物理 settle，至少应使用强 `ease-out`；但对于可抓取 sheet，更合适的是可中断、可接收初速度的 spring。

---

## P1：snap target 只取当前位置，没有速度投影

当前：

```js
const target = nearestSnapPoint(sheet.offsetTop);
```

只使用当前位置，不使用：

- release velocity；
- gesture direction；
- projected endpoint；
- 当前 snap state；
- hysteresis；
- 相邻状态承诺阈值。

因此一个快速向上 flick，即便意图明显，只要释放点还略靠近下方 snap，就可能返回原位。反过来，一个慢速、小幅越过中点的动作可能意外跨状态。

合理目标解析应综合：

```text
current presentation position
+ release velocity
+ projected endpoint
+ current state
+ direction
+ hysteresis
+ legal boundary
```

而不是只做几何最近点。

---

## P1：`offsetTop` 未必代表用户看到的 presentation value

这里同时存在：

- CSS transition on `top`；
- inline `style.top`；
- WAAPI `top` animation；
- `fill: "forwards"`。

`sheet.offsetTop`、inline target 和屏幕上正在插值的位置可能不是同一个值。

直接操控要求所有新操作都从 **当前屏幕呈现值** 开始，而不是从：

- 上一次 snap 的逻辑状态；
- 最新 inline target；
- 未完成 transition 的终点；
- 已结束但尚未提交的 WAAPI fill 值。

当前没有任何 presentation-value sampling 或统一的数值位置状态。

---

## P1：`fill: "forwards"` 被当作持久状态，状态提交不完整

动画结束后只做：

```js
animating = false;
```

没有明确：

- 将最终 target 写入持久 transform/style；
- `commitStyles()`；
- cancel/remove 已完成 animation；
- 更新语义状态为 `collapsed`、`half` 或 `full`；
- 清理 animation reference。

`fill: "forwards"` 让 animation effect 继续覆盖底层值，但底层 inline `top` 仍可能是释放时的位置。下一次动画取消、style 更新或规则变化时，容易出现回跳。

设计上应把“presentation animation”和“持久组件状态”分开：

1. 动画从当前值到 target；
2. 完成后把 target 提交到唯一位置状态；
3. 更新 semantic snap state；
4. 移除旧 animation effect；
5. 即使被 cancel/reject，也通过 `finally` 清理生命周期。

---

## P1：没有速度采样，无法做 velocity handoff

当前没有保存一段时间内的位置历史。速度不能只靠最后两个不稳定事件猜测，也不能使用固定动画速度替代。

建议保留最近约 `60-100ms` 的有限样本：

```text
{ time, y }
```

松手时对近期样本计算过滤后的 `px/s`。具体采样窗口、滤波方式和阈值需要通过设备测试调整。

---

## P2：整个 sheet 的 `scale(0.96)` 是错误的 pointer-down 反馈

4% 的整体缩放对于大面积 sheet 很强，且与拖动平移共用 `transform`。

它更像一个大型按钮被按下，而不是一块可以移动的工作表面。对 calm utility UI，推荐：

- handle 颜色轻微增强；
- handle 宽度或 opacity 小幅变化；
- cursor 从 `grab` 变为 `grabbing`；
- 阴影轻微增强；
- 可选的 `1px` 局部高光变化；
- 不缩放 sheet 本体。

如果确实需要 scale，最多也应非常轻微，例如 `0.995-0.99`，且只在短 pointer-down 确认阶段；但在这个产品语境下，我建议完全不使用整体 scale。

---

## P2：没有 intent threshold 和滚动仲裁证据

手势开始前应有小幅 hysteresis，典型初始范围是 `8-12px`，用于区分：

- 点击 handle；
- 垂直拖动；
- sheet 内部内容滚动；
- 横向控件操作。

Bottom sheet 还需要处理 full 状态下的内部滚动：

- 内容 `scrollTop > 0` 时，下拉可能先滚动内容；
- 内容已到顶部且继续向下时，才把控制权交给 sheet；
- 从 handle 开始的拖动可以直接归 sheet；
- 不应在整个 sheet 上粗暴设置 `touch-action: none`，否则可能破坏内容滚动。

这些在静态片段中都没有证据，必须运行时验证。

---

## P2：没有 soft boundary

sheet 应在 `full` 和 `collapsed` 之外提供渐进阻力，而不是：

- 无限拖出合法范围；
- 突然硬截断；
- 让 `clientY` 任意控制 `top`。

推荐在越界时应用 rubber-band：

```text
resisted =
  (overshoot * dimension * constant) /
  (dimension + constant * abs(overshoot))
```

`constant ≈ 0.55` 可作为起点，但必须实测。对于严肃运营界面：

- 视觉越界量应很小；
- 松手后无弹跳地回到边界；
- Reduced Motion 下直接 clamp，不使用 rubber-band/overshoot。

---

# 4. 具体 design moves

## A. Pointer-down feedback

### 推荐行为

在 drag handle 上：

1. 记录 `pointerId`。
2. 读取 sheet 当前 presentation Y。
3. 中断正在进行的 settle，但保留当前位置。
4. 记录 grab offset。
5. 调用 pointer capture。
6. 将 handle 切换为 active/grabbing 状态。

视觉反馈：

```text
cursor: grab → grabbing
handle color: neutral → slightly stronger
shadow: very small increase
```

响应时间：

- pointer-down 的局部视觉反馈约 `80-120ms`；
- 不等待 drag threshold 才显示“已听到输入”；
- sheet 本体不缩放。

### 不推荐

```css
.sheet:active {
  transform: scale(0.96);
}
```

---

## B. 1:1 tracking

位置模型应统一为一个 `sheetY`，snap point 也使用同一个坐标空间。

手势开始：

```text
grabOffset = pointerY - presentationSheetY
```

拖动：

```text
rawY = pointerY - grabOffset
displayY = applyBoundaryResistance(rawY)
```

每个 animation frame：

```text
transform: translate3d(0, displayY, 0)
```

要求：

- 不使用 position transition；
- 不逐帧更新 `top`；
- 不在 pointer hot path 读取 `offsetTop` 后立即写 style，避免 read/write layout 交错；
- pointer event 只更新最新输入值，由 `requestAnimationFrame` 或等价 display-clock primitive 提交；
- 同一个 active pointer 才能更新位置。

---

## C. Presentation-value interruption

组件应维护：

```text
phase:
  idle
  possible-drag
  dragging
  settling

presentationY
targetY
velocityY
activePointerId
```

用户在 settle 中重新按下时：

1. 读取动画当前显示位置；
2. 读取或保留动画当前速度；
3. 停止 settle；
4. 将当前显示位置提交为新 gesture 起点；
5. pointer move 后直接接管；
6. 不跳回旧 target，也不从零速度重新开始。

如果使用 WAAPI，需要谨慎处理：

- 读取当前 effect progress/computed transform；
- 将当前 transform 提交；
- cancel animation；
- 对 `.finished` rejection 使用 `catch/finally`；
- 不依赖 `fill: "forwards"` 维持组件真状态。

实践中，支持 spring、位置和速度读取的交互动画 primitive 会比当前固定 WAAPI duration 更适合。

---

## D. Velocity handoff

记录最近一小段指针历史：

```text
samples = [
  { time, y },
  ...
]
```

松手时计算：

```text
releaseVelocityPxPerSecond
```

settle spring 的初始速度使用该值，而不是固定从零开始。

体验要求：

- 慢拖慢放：稳定吸附到意图最近的状态；
- 快速 flick：保留方向和动量；
- 快速反向后松手：以最后有效手势方向为准；
- settle 中重新抓取：不丢失当前运动连续性；
- 默认不人为添加 bounce。

---

## E. Projected endpoints

目标选择可以采用以下过程：

```text
projectedY = currentY + project(releaseVelocity)
candidate = nearestSnapPoint(projectedY)
target = applyDirectionAndHysteresis(candidate)
```

一个可用于调参的投影形式是：

```text
projection(v, d) = (v / 1000) * d / (1 - d)
```

然后：

```text
projectedEndpoint = current + projection(releaseVelocity, d)
```

但不能直接无界使用：

- projection 必须 clamp；
- target 必须限制在合法 snap points；
- `d` 需要按产品调节；
- 对三段式运营 sheet，可以默认最多跨一个 snap；
- 只有速度明显超过高阈值且方向明确时，才允许一次跨两段；
- 接近当前 snap 时使用 hysteresis，避免轻微抖动导致状态翻转。

建议 target resolver 的优先级：

1. 非常低速度：位置 + 当前状态 hysteresis；
2. 中等速度：projected endpoint；
3. 高速度：手势方向优先，再结合 projected endpoint；
4. 越界：只回到最邻近合法边界；
5. Reduced Motion：仍可用手势方向选择状态，但取消惯性旅行。

具体速度阈值不能仅凭静态代码确定，应通过 pointer trace 和真机调参。

---

## F. Soft boundaries

`full` 之上和 `collapsed` 之下：

- 使用渐进阻力；
- 越拖越难，但仍能感到输入被接收；
- 限制最大视觉 overshoot；
- 松手后无弹跳回到边界；
- 不允许 sheet 永久停留在非法位置。

对于 calm utility UI，推荐：

- 阻力明显但不“果冻”；
- overshoot 小；
- settle 临界阻尼；
- 不使用多次回弹。

---

## G. Reduced Motion

Reduced Motion 不应该让状态变化变得不可理解，但应移除非必要的大范围自动位移。

### 用户直接拖动时

用户控制的 1:1 位移可以保留，因为这是操作本身，而不是系统强加的自动动画。但应：

- 不使用 rubber-band overshoot；
- 不继承惯性进行长距离滑行；
- 不添加弹跳；
- 松手后立即或近乎立即确定 snap state。

### 松手后

推荐策略：

```text
projection仍用于判断目标
→ 位置立即提交到目标，或使用极短且受限的 settle
→ handle/color/scrim 在 80-120ms 内提供状态反馈
```

如果 target 距离很远，优先直接提交位置，不播放完整跨屏旅行。

### 非手势触发的状态变化

例如键盘、按钮或程序触发：

- 直接切换位置；
- 用短 opacity/color/elevation 反馈确认状态；
- 保持焦点；
- 更新可访问状态名称，例如 `Collapsed`、`Half expanded`、`Fully expanded`；
- 不依赖运动本身传达状态。

示意：

```css
@media (prefers-reduced-motion: reduce) {
  .sheet {
    transition: none;
  }

  .sheet__handle,
  .sheet__state-indicator {
    transition:
      color 100ms linear,
      opacity 100ms linear;
  }
}
```

实际实现还需要保证 JS settle engine 同样读取 `matchMedia("(prefers-reduced-motion: reduce)")`，不能只关闭 CSS transition。

---

# 5. Verified 与 unverified claims

## 由提供代码直接确认

以下是静态证据可以确认的事实：

- `pointermove` 没有检查 drag 是否已经开始。
- `pointermove` 没有检查 `animating`。
- `startY` 被赋值但没有在给出的代码中使用。
- sheet 的 `top` 被直接设为 `event.clientY`。
- 没有看到 grab offset 计算。
- 没有看到 `activePointerId`。
- 没有看到 pointer capture。
- 没有看到 `pointercancel` 或 `lostpointercapture`。
- settle target 仅由 `nearestSnapPoint(sheet.offsetTop)` 决定。
- 没有看到速度采样、速度交接或 projected endpoint。
- pointer-down 在 `animating` 时被拒绝。
- settle 使用固定 `480ms` 和 `ease-in`。
- WAAPI 使用 `top`。
- WAAPI 使用 `fill: "forwards"`。
- animation 完成后只将 `animating` 设为 `false`。
- CSS 对 sheet 使用 `transition: all 300ms`。
- active 状态把整个 sheet 缩放到 `0.96`。
- 提供的代码中没有 Reduced Motion 分支。

## 高可信静态推断，但尚未运行时验证

以下是高概率风险，不应表述为已经观测到：

- `transition: all` 会使 sheet 追赶 pointer，造成明显拖尾。
- 抓取非 sheet 顶边位置时会产生视觉跳变。
- `top` 动画会增加 layout/style 工作并可能掉帧。
- CSS transition、inline `top` 与 WAAPI `top` 可能导致逻辑值和 presentation value 不一致。
- `fill: "forwards"` 可能导致后续中断或 style 更新时回跳。
- pointer 离开元素后可能丢失完成事件。
- 整体 `scale(0.96)` 会造成视觉上下文不稳定和抓取点脱离感。
- 480ms `ease-in` 会被高频用户感知为迟缓。
- 鼠标悬停移动可能直接改变 sheet 位置；这取决于 listener 所在实际元素、完整页面结构和其他未提供代码，但给出的 handler 本身没有门控。

## 完全未验证

本次不能声称以下任何内容已经通过：

- 实际拖动是否顺滑或卡顿；
- 60 Hz / 120 Hz 帧稳定性；
- Chrome、Safari、Firefox 的具体表现；
- iOS Safari 或 Android Chrome 触控行为；
- pointer capture 丢失行为；
- 内容滚动与 sheet drag 的仲裁；
- viewport resize、横竖屏、软键盘和 safe-area 行为；
- `offsetTop` 在该页面完整样式下与视觉位置的实际差值；
- Reduced Motion 实际结果；
- `collapsed`、`half`、`full` 的真实 snap geometry；
- 动画是否遮挡操作、破坏焦点或影响可访问树；
- `.sheet:active` 与完整 transform 栈的最终 computed style；
- 任何 real-device touch feel。

---

# 6. 实现批准前的最小浏览器/设备验证计划

## A. Desktop browser：基础状态机与 interruption

至少在桌面 Chromium 中完成一轮，使用 mouse/trackpad，并记录 pointer trace。

### 必测路径

1. 不按下，仅在 sheet 上移动鼠标：
   - sheet 不得移动。
2. 从 handle 不同 Y 位置按下：
   - sheet 不得跳到 pointer 下方；
   - grab offset 保持稳定。
3. 慢拖到三个 snap 附近后松手：
   - target 稳定、无中点抖动。
4. 快速向上、向下 flick：
   - 目标体现速度和方向。
5. 拖动中反向再松手：
   - 以近期有效速度为准。
6. settle 中重新抓住：
   - 输入立即生效；
   - 不等待旧动画结束；
   - 不跳到旧逻辑值。
7. pointer 移出 handle/sheet 后松手：
   - 仍正确结束或取消。
8. `pointercancel`：
   - 回到合法状态；
   - 不留下 stuck `dragging/animating`。
9. 越过 full/collapsed 边界：
   - 有渐进阻力；
   - 不永久停在非法位置。
10. 快速连续操作：
   - 没有 promise rejection 导致的锁死；
   - 没有旧 animation 覆盖新状态。

### 最小接受标准

- 超过 intent threshold 后，sheet 在下一个显示帧跟随最新 pointer；
- pointer 与抓取点之间的相对偏移保持稳定；
- 重新抓取时没有可见位置跳变；
- 所有结束和取消路径最终落到合法 snap；
- settle 不阻止新输入。

---

## B. Performance timeline

使用浏览器 Performance panel 记录：

- 连续拖动；
- 快速反向；
- settle；
- settle 中 interruption；
- 页面同时有典型运营数据渲染时的拖动。

检查：

- gesture hot path 是否逐帧触发 Layout；
- 是否存在 forced synchronous layout；
- 是否因 `offsetTop` read + style write 形成 layout thrashing；
- 是否存在长任务；
- transform 是否在 compositor 路径；
- 60 Hz 下是否稳定；
- 若产品真实用户大量使用高刷设备，再补 120 Hz 真机验证。

批准前不能只看“动画看起来差不多”，至少要确认没有持续 layout-property animation。

---

## C. Reduced Motion

在浏览器 DevTools 模拟 `prefers-reduced-motion: reduce`，并至少在一个真实操作系统设置下复核。

必测：

1. 直接拖动仍然保留可理解的 1:1 控制。
2. 无 rubber-band overshoot。
3. 无弹跳。
4. 松手后无长距离惯性旅行。
5. 程序化切换三个状态时没有大范围空间动画。
6. 状态仍通过 handle、颜色、标题或静态状态文本明确反馈。
7. 焦点不丢失。

---

## D. 最小真机矩阵

至少：

- **iOS Safari，真实触控设备**
- **Android Chrome，真实触控设备**

如果只能做最小范围，优先各测一台常见 60 Hz 设备；若这是发布关键交互，再增加一台 120 Hz 设备。

真机重点不是截图，而是：

- 手指遮挡下的抓取稳定性；
- pointer/touch cancel；
- 系统浏览器手势冲突；
- 页面滚动与 sheet drag 仲裁；
- full 状态内部内容滚动；
- 地址栏动态高度和 viewport 变化；
- 横竖屏；
- safe-area；
- 软键盘出现时的 snap point 重算；
- 快速 flick 和中途重抓的触感。

---

## E. 响应式与内容滚动

最少覆盖：

- 窄手机 viewport；
- 常规桌面 viewport；
- 高度较短的 viewport；
- full sheet 内部内容可滚动；
- 内容顶部/中部/底部的拖动；
- snap points 因 viewport resize 变化后的重新计算。

特别验证：

```text
full state + content scrollTop > 0
```

此时用户在内容区向下拖动，是先滚内容还是收起 sheet，必须有明确仲裁规则。建议：

- handle 始终控制 sheet；
- 内容区优先滚动内容；
- 内容到顶后继续下拉，才把控制权交给 sheet；
- handoff 时保持手势连续，不能突然跳位。

---

## 审批条件摘要

当前状态：**Block**。

至少满足以下条件后再批准实现：

- 移除无门控 `pointermove`。
- 使用明确 gesture state 和 active pointer。
- 保留 grab offset。
- 使用 pointer capture，并处理 cancel。
- 拖动阶段无 CSS position transition。
- 使用 transform/display-clock 更新位置。
- settle 可中断并从 presentation value 接管。
- 采样 release velocity。
- 基于 projected endpoint + hysteresis 选择 snap。
- 合法边界外使用克制的渐进阻力。
- 不缩放整个 sheet。
- Reduced Motion 移除惯性、弹跳和大范围自动旅行，同时保留状态反馈。
- 完成至少一轮浏览器 pointer trace、性能时间线、Reduced Motion 和 iOS/Android 真机触控验证。

本次未修改任何文件，也未进行浏览器、模拟器或真实设备验证。