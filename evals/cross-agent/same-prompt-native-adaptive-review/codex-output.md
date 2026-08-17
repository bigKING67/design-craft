## 1. 证据、平台与设计解读

- **评审模式**：`critique`，只读；未修改任何文件，未执行构建或原生运行。
- **证据等级**：**L0 static**。只有产品上下文和静态实现描述；没有截图，因此不能升级为要求“截图 + 上下文”的 L1。
- **Resolved platform**：`adaptive`。依据是提示所述 `PRODUCT.md` 明确声明 `adaptive`、React Native 实现，以及同时通过 iOS/Android 商店交付；该结论在提示范围内为高置信度，但未由真实仓库确认。
- **设计权威**：以提示所述 `PRODUCT.md` 和 `DESIGN.md` 为准；共享语义角色与内容层级，不要求两端像素一致，并明确允许平台原生分化。
- **Design read**：Reading this as: 一个供现场操作员单手完成、再由管理者在平板多窗复核的任务表面，气质冷静、可信、系统原生，优化目标是快速完成且中断后可恢复。
- **实际 Skill**：`design-craft`；主代理串行完成，未启用子代理。标准 route planner 已尝试，但只读沙箱阻止其创建 here-doc 临时文件，因此没有伪造 route 输出或 tier。

## 2. 分平台合规结论

| 平台 | 结论 | 静态判定 |
|---|---|---|
| **iOS / iPadOS** | **BLOCKED — 静态不符合平台合同** | 自定义导航替代 native stack、40pt 目标、禁用 Dynamic Type、固定手机画布、非平台图标/硬编码主题及缺失 Reduce Motion，均阻止通过发布级设计验收。 |
| **Android** | **BLOCKED — 静态不符合平台合同** | 主动吞掉系统/预测性 Back、40dp 目标、禁用字体缩放、Cupertino 控件、固定手机画布、非自适应导航及缺失 Remove animations，均阻止通过发布级设计验收。 |

这不是 App Store/Play 审核结果，也不是运行态判定；它是基于所给静态事实的 conformance gate。

## 3. 五项阻断发现

1. **B1 — P0｜可访问性与操作目标**
   - 所有主操作只有 `40x40`，低于 iOS `44x44pt` 和 Android `48x48dp` 的有效目标下限；没有更大 `hitSlop` 的证据。
   - `fontSize: 14` 固定且禁用缩放，直接违背 Dynamic Type/font scaling 发布要求。
   - VoiceOver、TalkBack、外接键盘遍历、焦点状态及放大后的重排均未验证，因此可访问性发布门禁不能通过。

2. **B2 — P0｜导航、Back 与任务安全**
   - 自定义顶栏和 JavaScript Back 替代 iOS navigation stack；Android `BackHandler` 又无条件消费系统 Back。
   - iOS 左缘返回、Android predictive Back、系统转场和一致的返回层级因此被破坏。
   - 尚不能断言已经丢失任务进度，但当前导航实现显著放大“返回、切后台或被打断时丢失草稿”的风险。

3. **B3 — P1｜平板、多窗口与结构适配**
   - 将屏幕固定为 `width: 390` 并在平板居中，是“把手机画布放进大屏”，不是 adaptive layout。
   - 不变的底部 tab 未响应 iPad Split View、Android multi-window、可用宽度、输入模式或折叠姿态。
   - 这直接削弱管理者同时浏览任务列表、任务详情和核验信息的核心场景；窄分屏是否裁切仍需运行态确认。

4. **B4 — P1｜控件、图标与主题系统**
   - 两端共用 Cupertino 形状 switch 和 web 图标集，属于视觉复用替代平台行为；Android 的 native trust 尤其明显失败。
   - `#777777`、`#FFFFFF` 绕过 `DESIGN.md` 的语义色角色，并在两种 appearance 中复用。
   - 已确认的是 token authority 被绕过；具体颜色配对、对比度数值和高对比模式表现仍未验证。

5. **B5 — P0｜完成动效与减弱动画**
   - `500ms`、带 overshoot 的完成动效不符合“冷静、快速、操作型”定位，并缺少 iOS Reduce Motion / Android Remove animations 分支。
   - 缺少替代路径本身即违反明确发布要求；是否掉帧、能否中断、是否阻塞下一操作则没有运行证据。

## 4. 八个具体设计动作

1. **取消固定画布（B3）**：按实际 window width、size class、posture 和输入模式组织布局；compact 为任务优先单栏，expanded 为列表/详情或详情/核验双栏，窗口变化不得重置草稿。
2. **恢复系统导航（B2）**：接入平台认可的 stack/navigation host，删除吞掉 Back 的空 `BackHandler`；定义“返回层级、未保存内容、取消与退出”规则。
3. **让导航 chrome 真正适配（B3）**：iPhone/compact 可保留 tab + stack；iPad regular width 按任务结构采用 sidebar/split；Android compact 用 NavigationBar，medium/expanded 评估 NavigationRail 或 Drawer。
4. **建立平台目标与输入合同（B1）**：iOS 有效区域至少 `44pt`，Android 至少 `48dp` 且避免相邻目标重叠；同时定义 pressed、disabled、loading、keyboard/D-pad focus、label、role、value 和 state。
5. **改为语义排版（B1）**：启用字体缩放；iOS 映射 Dynamic Type text styles，Android 映射 Material type roles/`sp`；允许换行和纵向增长，放大后不能隐藏主操作。
6. **共享角色、分平台解析（B4）**：保留共同的 `surface/text/action/status` token 名称；iOS 映射 system colors/materials、native switch、SF Symbols，Android 映射 Material color roles/elevation、Material switch、Material Symbols。
7. **把完成反馈改为因果动效（B5）**：状态立即提交，默认采用短促、无弹跳或平台原生反馈；Reduce Motion 下去除位移和 overshoot，Remove animations 下使用即时状态或极短淡变。
8. **建立中断安全状态机（B2/B3）**：关键输入自动持久化，明确显示 `Saving / Saved / Retry`；覆盖后台恢复、进程终止、旋转、多窗 resize 和离线失败，并恢复到原任务、原选择及合理焦点。

### Intentional parity matrix

像素一致不是目标；**任务结果和可访问性结果一致，平台行为主动分化**。

| 关注项 | 保持共享 | iOS / iPadOS 适配 | Android 适配 |
|---|---|---|---|
| 任务与恢复 | 领域模型、步骤、校验、autosave、错误和 analytics 语义 | scene/background 生命周期与系统恢复路径 | activity/process-death、saved state 与多窗口生命周期 |
| 信息层级 | 主任务、状态、证据、完成动作的优先级 | compact stack；regular-width split/sidebar | compact 单栏；medium/expanded list-detail |
| Back | 返回意图、草稿保存和 discard 规则 | native stack、左缘返回、系统转场 | system Back、predictive Back、不可被空 handler 吞掉 |
| 控件与图标 | action/state/label 语义 | iOS controls、SF Symbols、最小 `44pt` | Material controls/Symbols、最小 `48dp` |
| 排版与辅助技术 | 内容角色、阅读顺序、完成公告 | Dynamic Type、VoiceOver、iPad keyboard focus | `sp`/font scale、TalkBack、keyboard/D-pad focus |
| 颜色与材质 | 同一语义 token 名称和状态含义 | semantic system colors/materials/tint | Material color roles、tonal elevation；Dynamic Color 可按品牌决定 |
| Motion | 因果事件、可中断原则、减弱动画结果 | 平台 push/sheet/haptic；Reduce Motion | Material transition/feedback；Remove animations |

## 5. Verified 与 unverified

**静态已确认——仅相对提示文本，不是现场取证：**

- `adaptive` 产品意图，以及 B1–B5 所引用的固定宽度、Back、尺寸、字号、颜色、控件、tab 和动效事实。
- 这些事实与提示所述产品/设计 authority 及两端平台合同存在明确冲突。
- 因而可以给出“静态 conformance blocked”，但不能宣称观察到了裁切、丢数据、对比度失败、卡顿或手势异常。

**未验证：**

- 真实 source tree、依赖版本、native project、补偿性 `hitSlop`、隐藏的平台分支及状态持久化实现。
- safe area、IME/insets、旋转、iPad Split View、Android multi-window、foldable posture 和动态 resize。
- VoiceOver/TalkBack 语义树、阅读顺序、公告、外接键盘/D-pad traversal 和最大文字缩放表现。
- 明暗/高对比模式的实际颜色配对及对比度；500ms 动效的帧率、可中断性和触觉反馈。
- 后台、进程终止、网络中断和系统 Back 后是否真正恢复进度。
- 任何 simulator、emulator、真实硬件、截图或商店发布就绪结论。

## 6. 最小 source / build / runtime 验证计划

1. **Source**：取得真实仓库后核对 `PRODUCT.md`、`DESIGN.md`、导航与状态 ownership；定向搜索  
   `rg -n 'width.?390|BackHandler|allowFontScaling|fontSize.?14|#777777|#FFFFFF|Switch|spring|reduceMotion|accessibility(Label|Role|State)' <app-src>`。
2. **Static/build gates**：先运行项目既有 typecheck、lint、unit/integration tests；随后用真实 workspace/scheme 执行 `xcodebuild ... -destination 'generic/platform=iOS Simulator' build`，Android 执行 `./gradlew lintDebug testDebugUnitTest assembleDebug`。
3. **iOS Simulator**：至少覆盖 iPhone 与 iPad、compact/regular width、旋转/Split View、最大 Dynamic Type、light/dark、Reduce Motion、VoiceOver 基础遍历和外接键盘；记录 exact commit、OS/profile、截图/视频和失败日志。
4. **Android Emulator**：至少覆盖 phone、tablet 及 foldable profile，测试 gesture navigation/predictive Back、multi-window、font scale、TalkBack、Remove animations、IME 和 keyboard/D-pad。
5. **真实设备**：代表性 iPhone+iPad、Android phone+tablet/foldable；验证单手可达性、边缘/预测性 Back、触觉、OEM 差异、启动/交互性能，以及 background → resume、process kill → restore、offline → retry。
6. **发布门禁**：B1–B5 全部关闭，并以两端运行证据证明完成任务、窗口重排和辅助技术路径不会丢失内容或关键操作，再将结论从 `blocked/static` 升级。

**当前明确缺失：**

- Source inspection / iOS build / Android build：**unverified**。
- **iOS Simulator: unverified locally**。
- **Android Emulator: unverified locally**。
- **iPhone/iPad real-device evidence: missing**。
- **Android phone/tablet/foldable real-device evidence: missing**。
- 文件改动：**none**。

Memory: `user:global + project:design-craft`，4 hits；仅用于校准静态、模拟器与真机证据边界；候选 0，写入 0。

