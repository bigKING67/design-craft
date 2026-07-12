## 1. 证据等级、平台与设计判断

- **使用技能**：`design-craft`，模式为 `critique`，只读评审。
- **证据等级**：仅有用户提供的 **prompt-attested static description**。低于源码扫描，更不构成构建、可访问性树或运行态证据。
- **Resolved platform**：`adaptive`。
  - 来源：提示中明确给出的 `PRODUCT.md platform: adaptive`，并声明同时发布 iOS、Android。
  - 置信度：对本次评审路由为 `1.0`；这不是对实际仓库平台配置的独立验证。
- **Style authority**：`DESIGN.md` 要求共享语义角色和内容层级，同时允许平台原生导航、控件、图标、材质和动效；当前“相同像素/相同控件”策略与该授权方向冲突。
- **Design read**：Reading this as: an adaptive field-operations task surface for one-handed operators and split-screen managers, with a calm, trustworthy native feel, optimized for fast completion, verification, and interruption-safe recovery.
- **一句话诊断**：当前概念是“居中的固定手机画布 + 跨平台外观复用”，不是平台正确的 adaptive 产品；按现有静态描述应阻断发布批准。

## 2. 分平台一致性结论

| 平台 | 静态一致性结论 | 决定性原因 |
|---|---|---|
| **iOS / iPadOS** | **BLOCK：不符合平台与发布要求** | 绕过原生 navigation stack 和边缘返回；`40x40` 小于 `44x44pt`；禁用 Dynamic Type；iPad/Split View 仍是固定 `390` 手机画布；无 Reduce Motion 路径。 |
| **Android** | **BLOCK：不符合平台与发布要求** | `BackHandler` 吞掉系统/预测性 Back；`40x40` 小于 `48x48dp`；禁用字体缩放；使用 Cupertino 控件；平板不切换 rail/drawer/two-pane；无 Remove animations 路径。 |

这些是基于所述实现属性得出的**静态设计结论**，不是对设备上实际故障的观察报告。

## 3. 优先问题

### P0 阻断项，最多五项

| 优先级 | 类别 | 静态证据与影响 | 最低接受条件 |
|---|---|---|---|
| **P0-1** | Navigation | 自定义顶栏和 JS back 替代 iOS stack；空 `BackHandler` 消费 Android Back。会破坏 iOS 边缘返回、Android predictive Back、系统一致性及可预期的退出路径。 | 恢复平台导航栈；iOS 保留交互式边缘返回，Android Back 交给导航状态和系统预测性返回；仅在真实业务拦截时注册可观察的 handler。 |
| **P0-2** | Accessibility | 主操作命中区为 `40x40`；所有文本固定 `14` 且禁用缩放。直接违反 `44pt`、`48dp`、Dynamic Type/font scaling 发布要求。 | iOS 有效触控区至少 `44x44pt`；Android 至少 `48x48dp`；启用缩放，并在约 `200%`/accessibility sizes 下保持操作可达、内容不截断。 |
| **P0-3** | Adaptivity | 整屏固定 `width: 390` 且居中；手机、iPad、Android tablet 使用相同底部导航。无法支持经理的 Split View/multi-window 审核任务。 | 按可用窗口宽度、size class、posture 和输入模式重排；compact 单栏，medium/expanded 使用适当的双栏、sidebar、rail 或 drawer。 |
| **P0-4** | Controls + theming | Android 使用 Cupertino switch；两端共用 web icon set；明暗外观都直接使用 `#777777`、`#FFFFFF`。Android 原生可信度明确失败，且绕过语义主题合同。 | 共享 action/token 语义，但分别映射平台控件、图标、颜色和材质。实际对比度是否失败尚不能从当前描述确定，必须根据具体前景/背景组合验证。 |
| **P0-5** | Motion | 完成任务使用 `500ms` overshooting spring，且没有 Reduce Motion/Remove animations 替代。对高频、严肃操作反馈过于拖沓，并违反明确的可访问性要求。 | 默认改为短促、无过冲、非阻塞反馈；iOS Reduce Motion 和 Android Remove animations 下使用轻微淡变或即时状态切换。 |

### 发布关键但尚未证明为缺陷的未知项

- VoiceOver/TalkBack 的 label、role、value、状态播报、遍历顺序和自定义 action 均未验证。
- safe area、status/navigation/IME inset、横竖屏、折叠屏 hinge、外接键盘和 D-pad focus 均无证据。
- “中断后不丢进度”只有产品要求，没有 draft persistence、后台恢复、process death、离线或幂等完成证据。

## 4. 八个具体设计动作

1. **恢复平台导航合同**  
   使用 native-stack-backed navigation；自定义 header 只负责品牌表现，不接管平台返回语义。删除吞 Back 的空 handler，并验证 iOS edge swipe 与 Android predictive Back。

2. **从固定设备宽度改成窗口驱动布局**  
   移除 `width: 390`。根据 `useWindowDimensions`/平台 window size class 计算结构，而不是设备名称：phone 为单任务流，tablet/expanded 为任务内容与验证信息的双栏结构。

3. **按形态调整导航容器**  
   compact phone 可保留 3–5 个顶级目的地的 tab/navigation bar；iPad 根据层级使用 sidebar、split view 或平台适配 tab；Android medium/expanded 使用 navigation rail、drawer 或 two-pane。不是简单放大或居中手机 UI。

4. **修复触控目标与单手可达性**  
   图标视觉尺寸可保持约 `20–24`，但 press surface 扩展到 iOS `44pt`、Android `48dp`；操作间保持足够间距。手机主操作放在安全、拇指可达区域，平板则贴近其所影响的 detail pane。

5. **采用语义排版而非统一 `14`**  
   定义 heading、body、label、metadata、button 等共享内容角色；iOS 映射 Dynamic Type text styles，Android 映射 Material typography/可缩放 `sp` 语义。开启字体缩放，并允许文本换行、容器增长和操作区重排。

6. **恢复语义主题与平台映射**  
   将 `#777777`、`#FFFFFF` 替换为 `surface.*`、`text.primary`、`text.secondary`、`border.*`、`state.*` 等角色。iOS 映射动态 system colors/materials；Android 映射 Material 3 color roles，并提供明确的静态 fallback。覆盖 light、dark、increased contrast/high contrast。

7. **平台化控件和图标**  
   共享业务 props 和 accessibility contract，但 iOS 使用原生 switch、SF Symbols、系统 sheet/alert/picker；Android 使用 Material switch、Material Symbols、bottom sheet/dialog/picker。不要用外观相似的共享壳牺牲系统行为。

8. **把完成反馈和进度恢复设计成同一个可靠状态机**  
   每次关键编辑增量保存 draft；完成操作幂等并呈现 pending/synced/error 状态；支持后台、进程终止和离线恢复。完成时提供可访问性 announcement，默认动效约 `150–250ms`、无过冲，并提供 reduced/no-motion 分支。

## 5. Intentional parity matrix

像素一致不是目标；应保持**任务结果一致、平台行为正确**。

| 合同 | 保持共享 | iOS / iPadOS 适配 | Android 适配 |
|---|---|---|---|
| 任务模型 | 字段、验证规则、完成语义、draft/offline 状态机 | 相同业务结果 | 相同业务结果 |
| 内容层级 | 任务、步骤、证据、验证、状态的优先关系 | 使用 iOS 排版和容器表达 | 使用 Material 排版和容器表达 |
| Navigation | IA、route identity、deep-link 语义 | Navigation stack、edge back、sidebar/split view | Navigation component、predictive Back、bar/rail/drawer |
| Adaptivity | compact/medium/expanded 的内容优先级 | size classes、iPad Split View、键盘输入 | window size classes、multi-window、fold posture |
| Controls/icons | action 名称、状态、analytics 语义 | 原生控件、SF Symbols、iOS sheets/alerts | Material 控件、Material Symbols、bottom sheets/dialogs |
| Color/type | `surface`、`text`、`state` 等 token 名称和内容角色 | system colors/materials、Dynamic Type | Material roles/tonal elevation、font scaling |
| Motion/feedback | “操作已接收/已完成/失败”的因果含义 | iOS transition、克制 haptic、Reduce Motion | Material motion、snackbar/haptic、Remove animations |
| Accessibility | label 意图、遍历逻辑、状态结果、键盘可达目标 | VoiceOver、Switch Control、external keyboard | TalkBack、Switch Access、D-pad/external keyboard |

## 6. 已确认与未验证

### 已确认——仅指输入材料明确陈述

- 产品目标平台为 `adaptive`，并具有 phone operator 与 tablet manager 两类使用姿态。
- `DESIGN.md` 允许平台原生分化，而不是要求像素一致。
- 提示明确描述了固定 `390` 宽度、被替换的导航、吞 Back 的 handler、`40x40` pressables、禁用字体缩放、literal colors、共享 Cupertino 控件/web icons、固定 tab bar 和无降级的 `500ms` spring。
- 本次没有修改任何文件，也没有生成截图或运行构建。

### 未验证

- 没有读取真实 `PRODUCT.md`、`DESIGN.md`、React Native 源码或 native project 配置。
- 未确认 `40x40` 是否另有 `hitSlop`；若只是视觉尺寸，源码必须证明有效命中区达到平台下限。
- 未确认具体颜色配对，因此不能断言某个对比度数值已经失败。
- 未验证 safe areas、IME、rotation、split-screen、multi-window、foldable 或实际布局溢出。
- 未验证 VoiceOver/TalkBack tree、keyboard focus、announcement、localization 和状态恢复。
- 未验证编译、启动、predictive Back、edge gesture、帧率、动画流畅度、haptic、OEM 差异或性能。
- **iOS Simulator：unverified locally；本次没有运行。**
- **Android Emulator：unverified locally；本次没有运行。**
- **Real-device evidence：unverified；没有 iPhone、iPad、Android phone/tablet/foldable 证据。**

## 7. 最小源码、构建与运行态验证计划

1. **源码扫描**  
   检查 `package.json`、navigation 配置、`ios/`、`android/` 和相关 screen/component；定向搜索：  
   `rg -n 'width:\s*390|BackHandler|allowFontScaling|fontSize:\s*14|#777777|#FFFFFF|Switch|spring|500|tabBar' <source-roots>`  
   同时确认 platform branching、window dimensions、safe-area/inset、accessibility settings 和 draft persistence。

2. **静态与构建验证**  
   运行仓库实际存在的 typecheck、lint 和相关单测，不臆造脚本名称；随后使用真实 workspace/scheme 执行 `xcodebuild ... build/test`，Android 执行项目对应的 Gradle `assembleDebug`、`lint`、unit tests。

3. **iOS Simulator 最小矩阵**  
   iPhone compact + iPad expanded/Split View；light/dark、最大 Dynamic Type、VoiceOver、Reduce Motion、外接键盘；验证 edge back、旋转、后台/恢复和进程重启后的 draft。

4. **Android Emulator 最小矩阵**  
   gesture-navigation phone + tablet/可调整或 foldable profile；multi-window、约 `200%` font scale、TalkBack、Remove animations、keyboard/D-pad；验证 predictive Back、IME、旋转和 process-death restore。

5. **真实设备发布门禁**  
   至少一台 iPhone 和一台采用手势导航的 Android 手机；经理平板流程应再覆盖 iPad 或 Android tablet。真实设备用于最终确认手势协调、haptic、OEM 差异、触控可达性和持续性能。