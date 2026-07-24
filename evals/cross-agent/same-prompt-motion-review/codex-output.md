## 1. 证据等级与设计判断

**结论：Block，不应批准当前交互实现。**

- **证据等级**：静态源码级证据，接近 `L0 static`；只能证明所示处理器、属性和显式缺失分支，不能证明实际手感、帧率或设备行为。
- **评审模式**：`design-craft / critique`；实际应用了 `motion-quality`、`interaction-physics`、`validation-contract`。
- **Design read**：这是一个供高频操作人员全天重复使用的 Web operations surface，气质应是 calm utility，核心是让三档 sheet 始终像被手直接控制，同时保持任务内容稳定、方向明确。
- **Authority**：本题产品约束和静态代码高于通用 motion 建议；没有项目 `DESIGN.md` 或运行态可供交叉验证。
- 本轮未编辑文件、未运行浏览器、未做 responsive、Reduced Motion 或真实设备验证；非实现任务，未运行 frontend route planner。

## 2. 哪些动效应该存在

**应该存在：**

- pointer-down 的即时、微弱反馈；
- 拖动中的无缓动 1:1 跟随；
- 从释放位置到合法 snap point 的短促、可中断 settle；
- `collapsed / half / full` 状态提交后的非空间状态反馈。

**不应该存在：**

- 整张 sheet 的 `scale(0.96)`；
- `transition: all`；
- 拖动期间对 `top` 做 300ms 插值；
- 固定 `480ms ease-in` 的强制等待；
- settle 期间锁死重新抓取；
- task content 的独立缩放、淡化、重排或装饰性弹跳；
- Reduced Motion 下的惯性投射、橡皮筋回弹和大距离自动滑行。

这里的拖动不是“娱乐性动画”，而是直接操控；需要设计的是因果反馈和释放后的收束。

## 3. 阻塞发现（最多五项）

| 优先级 | 发现 | Direct-manipulation / physics 影响 |
|---|---|---|
| **P0** | 没有可靠的 drag session：`pointermove` 不检查是否已按下，`startY` 在所示代码中未使用，直接把 viewport `clientY` 写成 `top`，也没有 grab offset、active pointer、intent threshold、显式 pointer capture 或 `pointercancel`。 | 鼠标悬停移动就可能改位置；按住时 sheet 顶边会跳到指针位置；离开边界后可能丢失追踪；内部滚动和点击也没有手势仲裁。 |
| **P0** | `.sheet { transition: all 300ms; }` 会让连续 `top` 更新被反复插值；同时 hot path 使用布局属性 `top`。 | 代码结构已经违背 1:1：sheet 会追赶指针而不是贴住指针。`top` 还引入逐帧布局风险，但是否实际掉帧仍需 timeline 证明。 |
| **P0** | settle 不可正确中断：`animating` 只拦截 `pointerdown`，却不拦截 `pointermove`/`pointerup`；WAAPI 使用 `fill: "forwards"`，但没有把最终值提交为单一状态并清理 animation。 | settle 期间仍可能写入底层 `top` 或启动另一段动画；完成后 presentation value 与 inline/logical value 存在双重所有权。下一次拖动是否被旧 filled effect 覆盖属于高风险运行态问题。 |
| **P1** | 释放只按当前 `offsetTop` 选最近点，未采样速度、未做 velocity handoff；settle 固定为 `480ms ease-in`。 | 快速 flick 和慢速拖放没有物理区别；`ease-in` 在用户最关注的起始阶段最慢。对全天重复使用的操作界面，这会显得迟钝、沉重。投射选点是否应改变现有语义仍需产品授权。 |
| **P1** | pointer-down 反馈缩放整个 sheet 到 `0.96`，且所示实现没有 Reduced Motion 分支。 | 大表面缩小会扰动内容稳定性并与 calm utility 冲突；300ms transition 还会让按压反馈迟到。明确的 Reduced Motion 要求在当前证据中没有实现或验证。 |

## 4. 八个具体设计动作

1. **建立明确的 pointer-down 合同**  
   只从 drag handle 或专用 header 区开始拖动，不劫持 sheet 的可滚动内容。`pointerdown` 时记录 `pointerId`、设置 pointer capture，并在约 `8–12 CSS px` 的起始阈值后进入 drag；这个范围只是初始值，需真机调校。即时反馈改为 handle 颜色/粗细或极轻阴影，约 `80–120ms ease-out`，不要缩放整张 sheet。

2. **实现真正的 1:1 tracking**  
   按下时取当前 presentation Y，并保存 `grabOffset = pointerY - presentationY`；拖动值始终为 `pointerY - grabOffset`。dragging 状态禁用 transition，每帧用最新 pointer sample 更新单一 `translateY(...)`；不要直接把 `clientY` 当 `top`。translation 与 handle press feedback 分层，避免两个行为争夺同一个 `transform`。

3. **按 presentation value 中断**  
   移除 `animating` 输入锁。用户在 settle 中重新按下时，应立即停止当前 animator，从屏幕上此刻的 Y 开始，不得跳回上一个逻辑 snap；单一 motion controller 同时持有当前 `position`、`velocity` 和目标。若仍使用 WAAPI，必须持有 animation 引用、提交当前/最终样式后取消 effect，并用 cancellation-safe cleanup，而不是永久依赖 `fill: forwards`。

4. **测量并交接释放速度**  
   保留最近约 `80–120ms` 的单调时间戳和 CSS-pixel 位置样本，计算 `releaseVelocity`，单位明确为 `CSS px/s`；使用多个样本而不是最后一个事件。对异常值做有记录的 clamp，例如初始实验范围 `[-2400, 2400] px/s`，并把该速度传入 settle spring，而不是从零速度重新启动。

5. **将 projected endpoint 与 target selection 分开**  
   若产品明确允许 momentum-based snapping，可先实验：  
   `projectedY = clamp(currentY + clamp(v, -2400, 2400) * 0.12s, fullY, collapsedY)`，再选择离 `projectedY` 最近的 snap，并在决策中加入约 `12px` 的起始 hysteresis。默认限制一次释放最多跨一个相邻状态，除非验证证明跨两档不会造成误操作。若产品仍要求“按释放位置最近点”，继续用 `nearestSnapPoint(currentY)`，但 settle 仍应继承速度；不能把投射选点偷偷当成视觉 polish。

6. **用短促、无装饰的 settle physics**  
   用可读取位置和速度的 spring，而不是固定 `480ms`。calm utility 的初始候选可用 damping ratio `0.95–1.0`、response `0.25–0.32s`；默认无 bounce，只有真实产品 motion language 与设备测试都支持时才加入极轻 overshoot。距离较短时应更快稳定，而不是每次等待同一时长。

7. **边界内 1:1，边界外 soft resistance**  
   在 `fullY…collapsedY` 范围内完全跟手；超出后应用渐进阻力，例如  
   `resisted = bound + (overshoot * dimension * 0.55) / (dimension + 0.55 * abs(overshoot))`。  
   `pointercancel`、`lostpointercapture`、窗口失焦和第二指针都要有确定恢复规则；Reduced Motion 下直接 clamp，不做 rubber-band。

8. **为 Reduced Motion 设计等价反馈**  
   直接拖动仍保持 1:1，因为这是用户控制的因果关系；但取消惯性 projection、弹跳、elastic overshoot 和额外空间旅行。释放后可即时提交，或只做约 `80–120ms` 的极短 transform 收束。键盘/程序化切换不要滑过整屏：直接切换几何状态，并用 handle 色彩、snap label、焦点稳定及恰当的 `aria-expanded`/状态语义确认 `collapsed / half / full`。

## 5. 已验证与未验证

**从所给代码可以确认：**

- `pointermove` 没有 dragging、`buttons` 或 active-pointer gate；
- `startY` 在所示流程中没有参与位置计算；
- 没有显式 grab offset、pointer capture、hysteresis、velocity history、soft boundary、`pointercancel` 或 Reduced Motion 分支；
- drag 和 settle 都修改/动画 `top`；
- CSS 使用 `transition: all 300ms` 和整张 sheet 的 `scale(0.96)`；
- settle 是 `480ms ease-in`、`fill: forwards`；
- target 来自释放时的 `nearestSnapPoint(sheet.offsetTop)`；
- `animating` 只在 `pointerdown` 被检查。

**不能从静态证据确认：**

- 实际是否卡顿、掉帧、延迟多少或是否达到 1:1；
- 外部 CSS 是否覆盖 transition，或另有 `prefers-reduced-motion` 实现；
- `.sheet` 的 containing block、computed `top`、snap point 几何和 `nearestSnapPoint` 细节；
- filled WAAPI effect 在目标浏览器中对下一次拖动造成的具体可见结果；
- 内部内容是否可滚动、是否已有 `touch-action`、焦点与键盘等价路径；
- responsive、方向切换、安全区、60/120Hz、mouse/trackpad/touch 手感；
- Chrome、Firefox、Safari 之间的 Pointer Events 与 WAAPI 实际表现。

## 6. 实现批准前的最小浏览器/设备验证

1. 在主 Chromium 浏览器加入临时 trace：逐帧记录 pointer-derived Y、presentation Y、`velocity px/s`、projected Y、目标 snap 和状态提交时间。
2. 覆盖 hover、tap、慢拖、快速 flick、反向拖、拖出 sheet、释放在两个 snap 中点附近；确认无按下时绝不移动，grab 起点和拖动过程没有跳变或人为 easing。
3. 在 settle 的约 25%/50%/75% 位置重新抓取；录屏逐帧检查从当前 presentation value 接管，且没有逻辑目标回跳或残留 filled animation。
4. 验证 full/collapsed 两端的阻力、`pointercancel`、capture loss、多指输入，以及 drag handle 与内部内容滚动不会互相抢手势；同时检查桌面和窄 viewport 的三档几何。
5. 用 DevTools Performance 在接近真实内容量下录制拖动与 settle：drag hot path 不应出现由位置更新触发的持续 Layout，每帧采用最新输入，且无相关 long task；再在一个受支持的非 Chromium 浏览器做行为 smoke。
6. 模拟 `prefers-reduced-motion: reduce`，再在至少一台真实触摸设备复测；该高频核心手势若面向高刷设备，至少补一台 60Hz 与一台 120Hz 设备。记录设备、浏览器、刷新率、视频/trace artifact；通过前仍保持 **unverified**。

