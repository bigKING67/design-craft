## 1. 证据级别、平台解析与设计读取

- **证据级别：`L0 static / prompt-attested`**。只有题面和静态实现描述；没有源码树可供独立核对，也没有 build、截图、accessibility tree 或任何原生运行态证据。
- **Resolved platform：`adaptive`，产品意图置信度高**。依据是题面明确给出的 `PRODUCT.md platform: adaptive`、React Native 形态及 iOS/Android 双商店交付；实际 target、依赖和构建配置未核验。
- **Authority：**只读取到题面概述的 `PRODUCT.md` / `DESIGN.md` 合同，未读取真实文件。该合同允许并要求使用平台原生导航、控件、图标、材料与动效，而不是像素级统一。
- **Route / skill：**人工解析为 `critique + adaptive`，实际使用 `design-craft`，并完成 iOS、Android 两个独立只读平台复核。路由脚本因只读沙箱无法创建临时文件而未产生 JSON，因此不声称有 planner receipt。
- **Design read：**Reading this as: 面向单手现场作业人员和大屏审核经理的任务执行/复核界面，气质应安静、可信、平台原生，首要优化快速完成、明确反馈与中断后准确恢复。
- **一句话诊断：**当前概念把 parity 实现成了“同一 390 宽手机界面跨平台复制”，而不是“共享任务语义、按平台和窗口能力有意适配”。

## 2. 分平台符合性结论

| 平台 | Verdict | 决定性原因 |
|---|---|---|
| **iOS / iPadOS** | **不符合，阻断 release** | Dynamic Type 被关闭、有效主操作目标未达到 `44x44pt` 的证据要求、原生导航栈被替换、iPad 没有窗口级结构适配、Reduced Motion 分支缺失。 |
| **Android** | **不符合，阻断 release** | 空 `BackHandler` 消费 system/predictive Back、font scaling 被关闭、`40x40` 小于 `48x48dp` 基线、Android 仍使用 Cupertino/Web 控件语言、Remove animations 分支缺失。 |

以上是**所描述实现与发布合同相冲突**的静态结论，不代表已在任一运行时观察到实际手势、裁切、卡顿、数据丢失或读屏行为。

## 3. 五项阻断性 finding

1. **P0｜Accessibility 与主操作目标**
   - 固定 `fontSize: 14` 且禁用 scaling，直接违反 Dynamic Type / Android font scaling 的明确发布要求；统一字号也无法保持内容层级。
   - `40x40` pressable 低于 iOS `44pt`、Android `48dp` 基线。题面没有外围有效触控区或 accessibility frame 的补偿证据，不能视为合格。
   - VoiceOver/TalkBack label、role、value、reading order、状态播报和键盘焦点尚未验证；不能把这些未验证项说成“已缺失”。

2. **P0｜Navigation、Back 与恢复边界**
   - iOS 自定义 top bar/JS back 替代原生 stack，使系统边缘返回、导航状态、焦点恢复和 scene restoration 都失去可信默认值。
   - Android 的空 `BackHandler` 明确劫持 system Back，并阻断 predictive Back 合同；顶部返回、系统返回和导航栈可能形成三套决策。
   - 题面没有持久化草稿、process-death restore 或幂等完成证据；这**不证明已经丢数据**，但“中断不丢进度”仍是未通过的 release gate。

3. **P0｜Motion accessibility**
   - `500ms` overshoot spring 没有 Reduced Motion / Remove animations 替代路径，这是直接的发布阻断项。
   - 长弹簧和 overshoot 还与“calm、operational”定位不符；但眩晕感、帧率和可中断性没有运行时证据，不能宣称已经观察到这些问题。
   - 业务完成、持久化或导航绝不能等待动画结束回调。

4. **P1｜Adaptivity 只是居中手机画布**
   - 强制 `width: 390` 并在平板居中，无法服务 manager 的高密度审核；在窄 Split View / multi-window 中还有溢出风险，但实际溢出尚未观察。
   - phone、iPad、Android tablet 永久使用同一 bottom tabs，说明没有按 available width、window class、posture 或 input mode 重组导航和内容。
   - Bottom tabs 在 compact window 中可以保留；阻断点是**没有窗口驱动的替代结构**，而不是“平板绝不能出现 tabs”。

5. **P1｜平台控件、图标与主题被错误统一**
   - Cupertino switch 在 Android 上不符合 Material 交互语言；在 iOS 上“长得像 Cupertino”也不能证明它具有原生 switch 的语义、手势和辅助功能。
   - 同一 Web icon set 无法提供 SF Symbols / Material Symbols 各自的视觉度量、平台含义和 accessibility mapping。
   - `#777777`、`#FFFFFF` 绕过 `DESIGN.md` 的 semantic roles，并使 light/dark 映射不可治理。若二者恰好作为普通正文/白底组合，对比度约为 `4.48:1`；但题面没有证明它们相邻使用，因此这里只能判定为风险，不能泛化宣称所有实例均对比度失败。

## 4. 八个具体 design moves

1. **恢复平台导航所有权：**iOS 使用 native-stack 或等价系统集成；Android 使用支持 system/predictive Back 的导航路径。删除 blanket/空 Back handler，仅在真实 modal 或未保存状态决策中有条件拦截。
2. **建立可恢复任务状态机：**每个有业务意义的步骤原子 checkpoint；草稿、同步状态和完成幂等 key 持久化到组件内存之外，并呈现“已保存 / 待同步 / 同步失败”。
3. **扩大有效目标：**iOS 主操作至少 `44x44pt`，Android 至少 `48x48dp`，同时保留足够间距；不得仅凭不可见 `hitSlop` 推定读屏焦点框也合格。
4. **恢复可扩展字体和完整输入合同：**按 heading/label/body/status 等语义角色使用系统字体尺度；允许 Dynamic Type/font scaling，并在大字号下 reflow；补齐 screen-reader role/state、逻辑 traversal、可见键盘焦点及 Enter/Space 激活。
5. **以 window capability 驱动布局：**移除固定 `390`；compact 为单栏任务执行，expanded 为任务列表/上下文 + 详情/验证双栏，连续响应旋转、Split View、multi-window、IME 和 fold posture。
6. **自适应导航容器而不改变 IA：**compact 可用 bottom tabs；iPad regular width 使用 sidebar/split；Android medium/expanded 使用 navigation rail/drawer，并按实际窗口宽度折叠，而不是按设备名称分支。
7. **建立平台 adapter seam：**共享业务组件 API，但 iOS 映射原生 switch、SF Symbols、system materials；Android 映射 Material 3 switch、Material Symbols、color/elevation roles。
8. **拆分状态反馈与装饰动效：**完成状态先提交、保存并播报；正常模式使用短、无夸张 overshoot 的平台过渡，Reduced Motion / Remove animations 下使用即时切换或短 cross-fade。

### Intentional parity matrix

| 维度 | 保持共享 | iOS / iPadOS 必须适配 | Android 必须适配 |
|---|---|---|---|
| 任务语义 | 步骤、校验、草稿、完成状态、离线/同步规则、analytics semantics | scene/app lifecycle 与 restoration 接入 | Activity/process recreation、saved state 与恢复接入 |
| IA | 相同目的地、内容优先级、返回决策 | native stack、边缘返回、compact tabs、regular sidebar/split | system/predictive Back、compact bottom nav、expanded rail/drawer |
| 布局 | 手机执行、平板复核的内容层级 | compact/regular size class、Split View/Stage Manager | compact/medium/expanded window class、multi-window/fold posture |
| 控件/图标 | 共享 semantic props、业务状态和 label | UIKit/native behavior、SF Symbols、iOS materials | Material 3 behavior、Material Symbols、elevation/tonal surfaces |
| Accessibility | 相同任务顺序、名称、状态结果和恢复承诺 | VoiceOver、Dynamic Type、Reduce Motion、`44pt`、键盘焦点 | TalkBack、font scale、Remove animations、`48dp`、键盘/D-pad |
| Theme | 相同 semantic role 名称与状态矩阵 | 映射 iOS dynamic/system colors | 映射 Material color roles；dynamic color 仅在产品授权时启用 |
| Motion | 状态因果、业务提交时机和 reduced-motion outcome | iOS 原生过渡与 Reduce Motion | Android predictive transition、Material motion 与 Remove animations |

## 5. 已验证与未验证

**在题面证据范围内成立：**
- 题面明确声明了 `adaptive` 产品目标及 accessibility release requirements。
- 评审将固定 `390`、自定义 Back、空 `BackHandler`、`40x40`、禁用 scaling、原始色值、共享 switch/icons/tabs、无 motion alternative 视为给定事实。
- 两个平台均可仅凭这些给定事实判定为“不满足所声明的静态发布合同”。

**未独立验证：**
- 上述属性是否存在于真实当前源码、是否有题面未提及的补偿路径，以及 `PRODUCT.md` / `DESIGN.md` 的真实内容与 revision。
- 实际 contrast 使用关系、safe area/IME、读屏节点与 traversal、键盘焦点、边缘/predictive Back、状态持久化、旋转、Split View、多窗口、foldable、性能、haptics 和 OEM 差异。
- 未运行 `xcodebuild`、Gradle、React Native tests，也未生成截图或 accessibility tree。
- **`iOS Simulator: unverified locally`**
- **`Android Emulator: unverified locally`**
- **`iOS real device: unverified`**；缺少 iPhone 与 iPad 证据。
- **`Android real device: unverified`**；缺少 Android phone 与 tablet/large-screen 证据。

## 6. 最小 source / build / runtime 验证计划

1. **Source audit：**取得真实 repo 后，检查 navigation/native-stack、全部 `BackHandler`、`allowFontScaling`、尺寸和 `hitSlop`、accessibility props、switch/icon imports、semantic token 映射、window-size 分支、motion setting listener、AppState/lifecycle、draft persistence、离线队列和完成幂等性。
2. **Targeted checks：**先发现并运行项目现有 typecheck、lint、unit/integration scripts；为 draft serialize/restore、schema migration、重复完成、返回决策和离线重放补最小测试。
3. **iOS build：**先用 `xcodebuild -list` 确认真实 project/workspace 与 scheme，再执行该 scheme 的 Simulator build/test 和至少一次 release-like build；没有 scheme 信息前不伪造具体命令。
4. **Android build：**先用 Gradle task/variant discovery 确认真正任务，再执行对应 compile/assemble、unit test 和 lint；不要假定题面一定使用默认 `app` variant。
5. **iOS runtime：**一台 compact iPhone Simulator + 一台 iPad Simulator；覆盖 full screen、窄/中 Split View、横竖屏、最大支持字号、VoiceOver、Reduce Motion、外接键盘、边缘返回、background/terminate/relaunch、离线/重连。
6. **Android runtime：**current-API gesture-navigation phone Emulator + expanded tablet/multi-window 配置；覆盖 predictive Back、连续 resize、旋转/IME、200% font scale、TalkBack、Remove animations、键盘/D-pad、Activity recreation、`force-stop` 后恢复；foldable 在支持范围内增加 posture 测试。
7. **Real-device release gate：**至少在代表性 iPhone、iPad、Android phone 和 Android tablet/large-screen 上复测单手触达、真实 screen reader、系统手势、锁屏/来电/后台回收、硬件键盘、弱网、haptics、OEM 行为和持续性能。
8. **通过条件：**任一窗口/字号下核心动作不裁切且可触达；Back 路径与平台一致；读屏和键盘顺序可预测；中断或进程终止后恢复到准确步骤；完成动作只提交一次且不依赖动画结束。

本轮未编辑任何文件，未执行构建，也未启动 Simulator、Emulator 或真实设备。