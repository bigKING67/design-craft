## 1. 证据级别与设计解读

### 证据级别

**静态源码评审，证据等级：S1 / Static-only。**

现有证据只能确认给定片段中声明了什么，不能确认真实交互手感、帧率、浏览器合成路径或完整项目是否另有补偿逻辑。

- 已提供：产品语境、JavaScript 片段、CSS 片段。
- 未提供：pointer trace、computed style、完整事件生命周期、WAAPI animation 状态、Performance frame timeline、Reduced Motion 运行结果、响应式结果、真实触屏设备测试。
- 因此：
  - 对明确源码问题可以给出高置信判断。
  - 对“是否卡顿、是否跳动、是否跟手、触控是否与页面滚动冲突”等运行时体验，只能标为高风险，不能声称已经复现。

### Design read

> **Reading this as：一个面向高频日常操作的 Web operations app，以克制、稳定、可打断的直接操控为运动语言，优化目标是在 `collapsed`、`half`、`full` 之间切换时持续保留任务上下文。**

这不是展示型抽屉，也不是需要“表演入场”的营销动效。它应该像一个被用户直接抓住的物体：

1. 按下后立即确认“已抓住”；
2. 拖动期间与指针保持因果一致；
3. 松手后承接用户速度；
4. 随时可以重新抓住；
5. 到达状态后明确、安静地停下。

### 评审结论

**Block：当前方案不应进入实现批准。**

阻断原因不是“动效参数还可以再调”，而是当前模型破坏了直接操控的基本契约：

- 指针移动与 sheet 位置没有可靠的 drag 状态绑定；
- 不保留抓取偏移，可能把 sheet 顶边跳到指针位置；
- `transition: all` 与逐帧拖动冲突；
- settlement 被 `animating` 锁死，无法自然打断；
- 松手目标只看当前位置，不看释放速度和投影终点；
- 使用 `top` 驱动高频布局；
- 没有边界阻尼、意图阈值、pointer capture 或 Reduced Motion 策略；
- `480ms ease-in` 对高频操作来说迟缓，且在最需要立即响应的起始阶段故意加速缓慢。

---

## 2. 哪些运动应该存在，哪些不应该动画

## 应该存在

### A. 拖动中的空间移动

必须存在，因为 sheet 状态本身就是空间状态。这里的移动不是装饰，而是直接操控的主要反馈。

要求：

- 通过小幅意图阈值后，位置与指针位移保持近似 1:1；
- 保留用户按下位置相对于 sheet 的抓取偏移；
- 不对拖动位置增加 CSS transition；
- 不因动画正在进行而拒绝重新抓取。

### B. 松手后的短暂 settle

应该存在，用于：

- 把 sheet 收敛到合法 snap point；
- 延续用户释放时的方向和速度；
- 防止松手后瞬间跳到状态点；
- 解释最终落在哪个状态。

但它应该是：

- 可打断的；
- 从屏幕当前 presentation value 开始；
- 速度连续；
- 默认无明显弹跳；
- 距离越短，体感越快，而不是固定播放一段 `480ms` 时间轴。

### C. pointer-down 的轻微抓取反馈

应该存在，但只用于确认输入被接收，例如：

- drag handle 的颜色或对比度增强；
- handle 轻微增粗或极小的位移；
- sheet 边界/阴影轻微变化；
- 鼠标环境下切换为 `cursor: grabbing`。

建议反馈时间约 `80-140ms`，且不应延迟实际拖动。

### D. 状态落点反馈

可以存在，但应非常克制：

- handle、状态标签或边界颜色短暂变化；
- 无障碍状态文本/ARIA 状态同步；
- Reduced Motion 下用非大位移反馈确认 `collapsed`、`half`、`full`。

---

## 不应该动画

### A. 不应使用 `transition: all`

```css
.sheet {
  transition: all 300ms;
}
```

这会把任何可动画属性都纳入过渡，包含后续维护者可能新增的属性。对拖动物体尤其危险，因为每次更新 `top` 都可能成为新的过渡目标，让视觉位置追赶指针，而不是与指针同步。

应该将 drag tracking 与 visual-state transition 分开：

- 拖动位置：不使用 CSS transition；
- 非空间反馈：只声明具体属性，如 `border-color`、`box-shadow`、`background-color`；
- settle：交给可中断、支持速度的独立动画控制器。

### B. 不应动画整个 sheet 的 `scale(0.96)`

```css
.sheet:active {
  transform: scale(0.96);
}
```

对一个承载任务上下文的底部 sheet，整体缩小 4% 不是“小反馈”：

- 内容、文本和控件都会整体漂移；
- sheet 的左右边界与底边会移动；
- 用户抓住纵向移动对象时，会同时看到二维缩放；
- `transform` 还可能与未来用于拖动的 `translateY()` 冲突；
- 可能造成文字栅格化变化或视觉模糊；
- 不符合 calm utility UI。

整个 sheet 不应通过 scale 表示“被抓住”。把反馈集中到 drag handle 或边界层。

### C. 不应使用 `480ms ease-in` 作为高频松手响应

```js
{ duration: 480, easing: "ease-in", fill: "forwards" }
```

`ease-in` 在动画开始阶段最慢，而松手后的第一个瞬间恰恰是用户最关注因果连续性的阶段。它容易表现为：

1. 用户快速释放；
2. sheet 短暂显得迟钝；
3. 然后才逐渐加速；
4. 到终点又以较高速度结束。

这与“收敛到静止状态”的物理语言相反。若暂时不能使用 spring，至少应该采用短而强的 ease-out；更合适的是速度感知、近临界阻尼的 spring。

### D. 不应把拖动位置作为常规 `top` 动画

`top` 是布局属性。拖动热路径上反复写入 `top`，并在松手阶段继续动画 `top`，会带来布局、样式与绘制风险。

更合理的实现模型是：

- sheet 的布局位置保持稳定；
- 用 `translate3d(0, y, 0)` 或等效 compositor-friendly transform 表示当前 sheet position；
- drag 每帧只更新变换；
- settle 使用同一个位置通道；
- handle 的反馈不要覆盖位置 transform，可使用子元素或独立 CSS 变量组合。

---

## 3. 优先级问题

## P0 — 阻断：pointer move 没有受 drag session 约束

当前代码：

```js
sheet.addEventListener("pointermove", (event) => {
  sheet.style.top = `${event.clientY}px`;
});
```

这里没有检查：

- 是否发生过有效 `pointerdown`；
- 当前是否处于 dragging；
- `event.pointerId` 是否是发起拖动的指针；
- 是否已经通过 intent threshold；
- 是否正在处理 `pointercancel`；
- pointerdown 是否因 `animating` 被拒绝。

从给定片段看，任何到达该监听器的 `pointermove` 都会写入 sheet 位置。甚至在：

```js
if (animating) return;
```

拒绝 pointerdown 后，pointermove 仍没有相同保护。

**设计影响：**

交互没有稳定的“抓住—移动—释放”因果链。用户不应该仅仅移动指针就改变 sheet；sheet 只能响应一个明确建立的 drag session。

**设计移动：**

建立显式状态：

- `idle`
- `pending-intent`
- `dragging`
- `settling`

至少记录：

- `activePointerId`
- `pointerDownY`
- `startPosition`
- `grabOffset`
- `dragStarted`
- 最近若干个时间/位置样本

只有当前 active pointer 才能更新位置。

---

## P0 — 阻断：没有保留 grab offset，可能发生首帧跳动

代码记录了：

```js
startY = event.clientY;
```

但 `startY` 没有用于移动计算。随后直接执行：

```js
sheet.style.top = `${event.clientY}px`;
```

这意味着代码把 sheet 顶边直接设置为指针的 viewport Y，而不是：

```text
newPosition = startSheetPosition + (currentPointerY - pointerDownY)
```

如果用户从 handle 或 sheet 内部任意位置按下，sheet 顶边都可能朝指针位置跳动。

**直接操控原则：**

用户抓住的是物体上的某个点，不是要求物体把自身原点移动到手指下。被抓住的局部点必须保持在指针下方。

**设计移动：**

pointerdown 时记录：

```text
startPointerY
startSheetY
grabOffset = startPointerY - startSheetY
```

拖动时使用：

```text
rawSheetY = currentPointerY - grabOffset
```

或者等价的 delta 模型：

```text
rawSheetY = startSheetY + (currentPointerY - startPointerY)
```

---

## P0 — 阻断：settle 动画不可打断

当前逻辑：

```js
if (animating) return;
```

用户在 sheet 从一个 snap point 移向另一个 snap point 时无法重新抓住它。对一个高频 bottom sheet，这是明显的 agency 损失。

正确的直接操控模型应该是：

1. sheet 正在 settle；
2. 用户再次按下；
3. 立即读取当前屏幕上的 presentation position；
4. 终止原 settle；
5. 从这个可见位置继续拖动；
6. 若可用，继承动画此刻的速度。

当前代码相反：动画播放期间拒绝新的按下，要求用户等待最多 `480ms`。如果用户一日操作几十次，这种锁定会反复积累成明显摩擦。

**设计移动：**

不要把 `animating` 当作输入锁。settling 应是可被 grabbing 覆盖的状态：

```text
settling --pointerdown--> dragging
```

而不是：

```text
settling --pointerdown--> ignored
```

---

## P0 — 阻断：`transition: all` 破坏 1:1 tracking

拖动期间每个 pointermove 都写 `top`，与此同时 `.sheet` 声明：

```css
transition: all 300ms;
```

如果 `top` 的 transition 在实际级联中生效，那么每次 pointermove 都会重新设置一个约 `300ms` 的追赶目标。表现风险包括：

- sheet 落后于指针；
- 快速反向时出现拖尾；
- 松手时视觉位置与逻辑位置不一致；
- pointermove 与 WAAPI 同时竞争；
- 不同浏览器在 transition/animation 组合下出现不同结果。

即便实际项目中某些样式优先级使它未生效，`transition: all` 仍然是结构性风险。

**设计移动：**

- drag state 下位置 transition 必须为 `none`；
- 更好的是从根本上不让通用 CSS transition 管理 sheet position；
- settle 由单一动画控制器负责，避免 CSS transition、WAAPI 和 pointermove 同时写同一属性。

---

## P1 — 高：松手没有 velocity handoff

当前目标：

```js
const target = nearestSnapPoint(sheet.offsetTop);
```

它只看松手位置，不看用户如何到达该位置。

因此以下两个手势可能得到相同结果：

- 慢慢拖到某个位置后停住；
- 在同一位置以很高速度向上 flick。

这不符合用户对动量的预期。快速向上释放应该更倾向于下一个更展开的状态；快速向下释放应该更倾向于收起。

**设计移动：**

在 drag 期间保留短时间窗口的采样，例如最近约 `60-120ms` 的位置与时间，计算 release velocity：

```text
velocityY = deltaPosition / deltaTime
```

松手后的 spring 初速度应继承该 velocity，而不是从零开始。

要避免只用最后两个噪声较大的事件；可以使用短历史窗口、加权线性估计或平台已有 gesture velocity tracker。

---

## P1 — 高：目标选择基于 release point，而不是 projected endpoint

`nearestSnapPoint(sheet.offsetTop)` 只能回答“当前离哪个点近”，不能回答“按照当前动量，它本来会朝哪里去”。

更符合物理直觉的模型：

```text
projectedY = currentY + project(releaseVelocity)
target = nearestSnapPoint(projectedY)
```

对于 calm utility UI，投影应克制且有边界：

- 慢速拖动：主要由距离与状态中线决定；
- 快速 flick：允许跨过中线进入下一状态；
- 默认可限制到相邻 snap point，避免一个轻微误触从 `full` 直接坠到 `collapsed`；
- 只有速度和方向足够明确时才允许跨越多个状态；
- 在阈值附近使用 hysteresis，避免同一位置轻微抖动导致目标来回切换。

---

## P1 — 高：使用 `offsetTop` 读取逻辑位置，但 WAAPI 通过 `fill: "forwards"` 保持表现值

当前动画：

```js
sheet.animate(
  [{ top: `${sheet.offsetTop}px` }, { top: `${target}px` }],
  { duration: 480, easing: "ease-in", fill: "forwards" },
)
```

但动画完成后没有显示：

- 将最终位置写回持久样式；
- `commitStyles()`；
- cancel/清理已完成 animation；
- 更新唯一的逻辑 state；
- 同步 `collapsed`、`half`、`full` 状态模型。

`fill: "forwards"` 可能让 animation effect 继续控制 presentation value，而底层 inline `top` 仍停在释放位置。后续再读取 `offsetTop`、修改 inline style 或叠加新动画时，存在表现值与逻辑值不一致的风险。

不能仅凭片段确认具体浏览器中的最终几何读数，但可以确认：**这段代码没有显式完成 presentation-to-model reconciliation。**

**设计移动：**

保持一个单一位置真源：

- drag 和 settle 都更新同一个 `positionY`；
- 动画结束时明确提交 target；
- 清理旧 animation；
- 更新离散状态 `collapsed | half | full`；
- 新拖动以当前 presentation position 为起点。

---

## P1 — 高：没有 pointer capture 与异常结束处理

给定代码中没有：

```js
sheet.setPointerCapture(event.pointerId)
```

也没有处理：

- `pointercancel`
- `lostpointercapture`
- 窗口失焦
- 多指输入
- 非主按钮
- 组件卸载时 animation cleanup

没有 pointer capture 时，指针离开 sheet 的命中区域后，事件可能不再按预期送达。尤其当 sheet 正在快速移动，原命中几何也在变化，更容易导致拖动中断或缺失 pointerup。

**设计移动：**

- pointerdown 建立 drag session 后捕获 active pointer；
- 只接受相同 `pointerId`；
- 忽略后续触点；
- `pointerup`、`pointercancel`、`lostpointercapture` 统一进入清理路径；
- cancel 时根据产品策略返回最近稳定状态或从当前 presentation value settle；
- 验证 `touch-action` 与页面滚动的仲裁策略。

---

## P1 — 高：没有 drag intent threshold，tap 与 drag 未区分

当前 pointermove 第一个像素就会改变位置。

这会造成：

- 用户点击 sheet 内控件时产生微小位移；
- 触屏手指自然抖动被当作拖动；
- sheet 内纵向滚动内容与拖动 sheet 竞争；
- 可点击元素的 click/cancel 语义不稳定。

**设计移动：**

建议从约 `8-12px` 的位移范围开始实测，不把它当作固定魔法值：

1. pointerdown：进入 `pending-intent`；
2. 位移小于阈值：保持 tap 候选；
3. 明确纵向移动且超过阈值：进入 dragging；
4. 获胜后取消与之冲突的点击/内容滚动候选；
5. 如果 sheet 内部可滚动，必须定义：
   - 内容不在顶部且向下拖时，是滚内容还是拖 sheet；
   - 内容在顶部继续向下时，何时把控制权交给 sheet；
   - handle 区域是否始终优先拖 sheet。

---

## P1 — 高：没有自然边界和软阻尼

给定代码没有显示对 `full` 以上或 `collapsed` 以下的限制。直接把 `event.clientY` 写入位置意味着 sheet 可能被拖到合法范围外。

硬 clamp 虽然比无边界安全，但会让手指继续移动而 sheet 突然停止，产生“撞墙”感。

**设计移动：**

- 合法区间内：1:1 tracking；
- 越过 `full` 或 `collapsed` 边界：应用渐进阻力；
- 松手：回到边界 snap point；
- calm utility UI 默认不做明显弹跳；
- Reduced Motion 下移除 elastic overshoot，使用硬边界或极弱阻力并立即收敛。

一种可调 rubber-band 形式：

```text
resistedOvershoot =
  (overshoot * dimension * constant) /
  (dimension + constant * abs(overshoot))
```

可以从 `constant ≈ 0.55` 开始，但必须通过触屏实测调整，不能把公式参数当作已验证设计。

---

## P2 — 中：整体 `scale(0.96)` 与位置 transform 争用同一属性

如果后续把拖动从 `top` 改为：

```css
transform: translateY(...);
```

那么：

```css
.sheet:active {
  transform: scale(0.96);
}
```

会直接覆盖位置 transform，除非使用组合变换或嵌套层。

更好的职责拆分：

- 外层 sheet positioner：只负责 `translateY`；
- 内层 surface：负责边界、阴影、背景；
- drag handle：负责 pointer-down 反馈；
- 不对主内容层做整体 scale。

---

## P2 — 中：没有 Reduced Motion 策略

给定片段中没有出现：

```css
@media (prefers-reduced-motion: reduce)
```

也没有 JavaScript 对媒体查询或用户设置的处理。

需要注意：Reduced Motion 不等于取消用户主动拖动时的 1:1 tracking。用户正在移动手指时，sheet 跟随手指是因果反馈；把它取消反而会损害理解。

Reduced Motion 应主要改变：

- 松手后的长距离自动 travel；
- 弹性 overshoot；
- bounce；
- 大幅 scale；
- 较长 settlement；
- 非必要的背景/内容联动视差。

状态仍然需要清楚地改变。

---

## 4. 具体设计移动

| 当前方案 | 建议方案 | 原因 |
|---|---|---|
| `transition: all 300ms` | 位置不使用通用 transition；只对明确的非位置属性做短过渡 | 避免拖动落后、属性意外参与动画 |
| `top = event.clientY` | `startPosition + pointerDelta`，保留 grab offset | 防止首帧跳动，建立 1:1 因果 |
| 整个 sheet `scale(0.96)` | handle/边界/阴影的微弱反馈 | 保留任务上下文稳定性 |
| 动画期间拒绝 pointerdown | pointerdown 立即中断 settle，从当前 presentation value 接管 | 保留用户 agency |
| 固定 `480ms ease-in` | 速度感知、近临界阻尼 spring；或短 ease-out fallback | 快速响应并自然停稳 |
| `nearestSnapPoint(current)` | `nearestSnapPoint(projectedEndpoint)` 加方向、速度和 hysteresis | 区分快拖与慢拖 |
| 无边界处理 | 合法区间 1:1，越界渐进阻力 | 既反馈边界，又不突然撞墙 |
| 无 Reduced Motion | 保留直接拖动，移除 bounce/overshoot，显著缩短或取消自动 travel | 保留状态反馈，减少大空间运动 |

### 4.1 Pointer-down feedback

建议：

- pointerdown 立即改变 handle 的对比度；
- mouse 环境切换 `grab` → `grabbing`；
- 可轻微增强边界或阴影，但不改变 sheet 尺寸；
- 反馈时间约 `80-140ms`；
- 反馈与 drag session 同时开始，不等待 threshold 后才显示“已接收”；
- threshold 只决定是否开始移动，不决定是否确认按下。

不建议：

- 整体 scale；
- 较大的 elevation jump；
- 任何需要等待 `300ms` 才明显的反馈；
- 在 touch 环境依赖 `:active` 作为唯一状态真源。

### 4.2 1:1 tracking

核心关系：

```text
dragY = startSheetY + (currentPointerY - pointerDownY)
```

约束：

- intent threshold 之前不移动；
- threshold 通过后，不重新把当前位置设为起点，否则会产生小跳；
- 合法边界内不增加 easing、lerp 或 CSS transition；
- 使用 active `pointerId`；
- 使用 pointer capture；
- 如更新频率较高，可将最新位置缓存，在 `requestAnimationFrame` 中写一次 transform；
- 避免在每次 pointermove 中同步读取 layout 再写 style。

### 4.3 Presentation-value interruption

当用户在 settle 中重新按下：

1. 获取当前屏幕位置，而不是上一个 snap target；
2. 获取当前动画速度或从相邻帧估计；
3. cancel 原动画；
4. 将当前 presentation position 固化为新的 drag 起点；
5. sheet 不发生视觉跳动；
6. 立即进入 pointer tracking；
7. 后续松手时把继承速度与新手势速度合理衔接。

验收标准：

- 在 sheet 移动到一半时重新抓住；
- 第一帧位置连续；
- 不跳向旧 target；
- 不等待原动画结束；
- 快速反向拖动时方向立即改变。

### 4.4 Velocity handoff

拖动期间记录短历史：

```text
[
  { time, y },
  { time, y },
  ...
]
```

松手时估算：

```text
releaseVelocityY
```

settle spring 的初速度使用该值。

需要防止：

- 使用单个 pointermove 差值导致速度噪声；
- pointer event 间隔过长时得到异常速度；
- 速度单位混淆，例如 px/ms 与 px/s；
- 极端速度导致跨越所有 snap points。

可以对速度做合理 clamp，但阈值必须通过设备实测确定。

### 4.5 Projected endpoints

概念模型：

```text
projectedY = currentY + projection(releaseVelocityY)
target = nearestSnapPoint(projectedY)
```

对三个状态建议加入状态约束：

- 低速释放：根据当前位置和当前状态的 hysteresis 区间判断；
- 中高速、方向明确：允许进入相邻状态；
- 极明确的高速 flick：是否允许跨两个状态，应由任务风险和实测决定；
- `half` 不应因为几像素噪声在 `collapsed`/`full` 之间不稳定；
- snap point 应根据当前 viewport、安全区和 sheet 内容需求计算，不应假设固定像素在所有尺寸上成立。

### 4.6 Soft boundaries

在 `[fullY, collapsedY]` 内：

```text
displayY = rawY
```

超出边界：

```text
displayY = boundary + resistedOvershoot
```

要求：

- 越界越远，增量越小；
- 阻力连续，不能在边界处改变斜率过于突兀；
- 松手后无明显娱乐性 bounce；
- 在业务工具中优先使用高阻尼、零或极小 overshoot；
- 边界阻力只表达“已经到底”，不用于制造玩具感。

### 4.7 Reduced Motion

建议策略：

#### 拖动期间

- 保留 1:1 tracking；
- 保留当前手指与 sheet 的直接空间关系；
- 移除或显著降低 rubber-band；
- 不做整体 scale；
- 不做内容视差、背景缩放或层级联动。

#### 松手后

可按距离分层：

- 距目标极近：短 `80-120ms` 收敛；
- 距离较远：立即切换或使用非常短、无 overshoot 的收敛；
- 禁止 bounce；
- 禁止长时间动量滑行；
- 不使用 `480ms` 大幅 travel。

#### 状态反馈

通过以下手段保留可理解性：

- handle 或状态指示的短色彩变化；
- 边界/阴影的短暂变化；
- 明确更新展开状态；
- 对辅助技术同步可访问状态；
- focus 保持在原任务上下文中，不因 sheet 状态变化随意丢失。

Reduced Motion 不应通过“什么都不反馈”实现。

---

## 5. 已验证与未验证

## 从给定静态代码可确认

以下是源码级确认，不依赖运行时推断：

- pointerdown 在 `animating === true` 时直接返回。
- `startY` 被赋值，但在给定片段中没有用于位置计算。
- pointermove 直接将 `event.clientY` 写入 `sheet.style.top`。
- pointermove 没有显示检查 dragging 状态或 active pointer。
- 松手目标由 `nearestSnapPoint(sheet.offsetTop)` 选择。
- settle 使用 `top` 属性。
- settle 配置为固定 `480ms`、`ease-in`、`fill: "forwards"`。
- `.sheet` 声明了 `transition: all 300ms`。
- `.sheet:active` 声明了 `transform: scale(0.96)`。
- 给定片段中没有显示 pointer capture。
- 给定片段中没有显示 release velocity、projected endpoint、hysteresis 或 soft boundary。
- 给定片段中没有显示 `pointercancel`、`lostpointercapture` 或多指管理。
- 给定片段中没有显示 Reduced Motion 分支。

## 静态证据支持的高置信设计判断

- `480ms ease-in` 不符合高频、直接响应型 operations UI 的运动目标。
- `transition: all` 不适合管理可拖动 sheet 的位置。
- 整体 `scale(0.96)` 对大面积 sheet 来说过强且与 calm utility 风格不匹配。
- 通过 `animating` 锁住输入不符合可打断直接操控。
- 仅根据 release position 选择 target 无法表达速度意图。
- 使用 layout property `top` 作为拖动热路径存在不必要的性能风险。
- 没有显式 drag session 和 grab-offset 模型，交互架构不完整。

## 未验证，不能声称已经发生

本次没有运行浏览器或设备，因此不能声称：

- sheet 在实际页面中一定会在 hover/pointermove 时移动；
- 第一帧一定出现可见跳动；
- CSS transition 在完整级联中一定作用于 `top`；
- 实际帧率低于 60 FPS；
- 已观察到 layout thrashing；
- WAAPI 与 CSS transition 在目标浏览器中出现了具体冲突；
- pointer capture 缺失已经导致真实丢帧或丢失 pointerup；
- 真实触屏上已发生页面滚动冲突；
- `:active` 在目标浏览器和触摸设备上的具体持续时间；
- Reduced Motion 在完整项目中完全没有其他全局处理；
- 响应式 snap point 有错误；
- 60 Hz 或 120 Hz 设备上的手感；
- 辅助技术当前如何朗读 sheet 状态；
- sheet 内容中的滚动、点击、选择文本和表单控件如何与拖动竞争。

换言之：**源码已经足以阻止批准当前方案，但不足以证明某一种具体运行时故障表现。**

---

## 6. 实现批准前的最小浏览器/设备验证计划

不需要做大规模 E2E；需要一份能够证明直接操控契约的最小验证包。

## A. 桌面浏览器：基础拖动与中断

**目标环境：**

- Chromium 桌面浏览器；
- 鼠标或触控板；
- 正常 Motion 设置。

**至少验证：**

1. 从 drag handle 顶部、中部、边缘分别按下：
   - sheet 第一帧不跳；
   - 抓取偏移保持不变。
2. 缓慢上下拖动：
   - 合法范围内近似 1:1；
   - sheet 不明显落后指针；
   - 内容不发生整体 scale。
3. 快速反向：
   - sheet 立即跟随反向；
   - 无 transition 拖尾。
4. 松手后立即重新抓住：
   - settle 被立即打断；
   - 不跳向旧目标；
   - 不等待动画结束。
5. 指针拖出 sheet 边界后释放：
   - pointer capture 保持追踪；
   - 状态正确清理。
6. `pointercancel` 或窗口失焦：
   - 不残留 `dragging` / `grabbing` 状态；
   - 后续可以正常再次拖动。

**建议证据：**

- 一段包含“拖动—松手—中途重抓—反向”的短录屏；
- DevTools 中的 pointer event/state 日志；
- 当前 position、velocity、projected target、final state 的非敏感调试记录。

## B. 目标选择矩阵

从每个状态分别测试：

- `collapsed → half`
- `half → collapsed`
- `half → full`
- `full → half`

每条至少覆盖：

1. 慢拖、低速释放；
2. 同一释放位置、向上快速 flick；
3. 同一释放位置、向下快速 flick；
4. snap threshold 附近的小幅往返；
5. 极端高速释放。

验收重点：

- 相同位置、不同速度可以得到符合方向意图的不同目标；
- 阈值附近不抖动；
- 不因轻微速度噪声跨越多个状态；
- 最终状态与视觉位置一致。

## C. 边界与内容竞争

测试：

- 在 `full` 以上继续上拖；
- 在 `collapsed` 以下继续下拖；
- 越界后反向回到合法区域；
- sheet 内可滚动内容在顶部与非顶部时分别拖动；
- 点击 sheet 内按钮、输入框或选择文本时，微小移动不应误启 drag；
- 多指进入时只认 active pointer。

验收重点：

- 越界阻力连续；
- 没有硬撞墙或夸张弹跳；
- tap/scroll/drag 的意图仲裁稳定；
- 不丢失内容操作能力。

## D. Performance timeline

至少录制一次连续快速拖动和多次 snap：

关注：

- 每帧是否反复触发 Layout；
- 主线程是否有长任务；
- pointermove 是否进行同步 layout read/write 往返；
- 是否稳定使用 transform/compositor 路径；
- 数据密集页面渲染时是否仍能保持可接受响应；
- animation 被中断后是否残留旧 WAAPI effect。

最低通过标准不应只写“看起来流畅”；应有 timeline 或 frame evidence 支撑。

## E. Reduced Motion

在浏览器模拟或系统设置中启用 `prefers-reduced-motion: reduce`，验证：

- 主动拖动仍与指针同步；
- 没有 bounce；
- 没有 elastic overshoot，或已显著减弱；
- 松手不会播放长距离 `480ms` travel；
- 状态改变仍清楚可辨；
- focus 和任务上下文保持稳定；
- 状态语义仍同步更新。

需要分别记录 normal motion 与 Reduced Motion 的行为差异，而不是只确认 media query 被匹配。

## F. 响应式

至少验证：

- 一个典型桌面 viewport；
- 一个窄移动 viewport；
- viewport 高度较短的情况；
- 浏览器地址栏或可视 viewport 高度变化场景，如目标产品覆盖移动 Web。

确认：

- 三个 snap point 都合法；
- `full` 不遮挡必要安全区域；
- `collapsed` 仍保留足够可识别入口；
- `half` 不落在任务内容不可用的尴尬位置；
- resize 后当前状态重新映射到新几何，不保留过期像素位置。

## G. 真实触屏设备

**实现批准前至少需要一次真实触屏测试。**

最低配置：

- 一台产品实际支持的手机或触屏设备；
- 记录浏览器、设备、系统版本；
- 已知时记录刷新率，至少覆盖 60 Hz；
- 如果该交互为核心高频路径且产品支持高刷设备，补一次 120 Hz 验证。

重点检查：

- 手指遮挡下是否仍容易抓到 handle；
- touch slop 是否合适；
- 页面滚动与 sheet drag 是否争抢；
- 快速 flick 的速度估算；
- 边界阻力；
- 中途重抓；
- Reduced Motion；
- 长时间重复操作是否显得迟缓或疲劳。

---

## 最终批准条件

以下条件全部满足后，才建议批准实现：

- drag session 明确，只响应 active pointer；
- grab offset 被保留，首帧无跳动；
- 合法范围内为 1:1 tracking；
- 位置不受 `transition: all` 影响；
- settle 可被任意时刻重新抓取；
- interruption 从 presentation value 开始；
- release velocity 被测量并交给 settle；
- target 基于 projected endpoint，并有 hysteresis；
- 边界有克制的软阻力；
- 默认无娱乐性 bounce；
- 不整体缩放 sheet；
- Reduced Motion 保留状态反馈并去除大幅自动 travel；
- 桌面浏览器完成交互与性能验证；
- 至少完成一次真实触屏设备验证。

本次仅完成静态设计评审；**没有进行浏览器、截图、录屏、Performance timeline、响应式或真实设备验证。**