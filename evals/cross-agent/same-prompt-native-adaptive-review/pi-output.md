## 1. Evidence level, resolved platform, design read

- **Evidence level:** static/prose-only implementation evidence. No source tree, build, screenshot, accessibility tree, rotation, split-screen, foldable, simulator/emulator, or hardware run was performed.
- **Resolved platform:** `adaptive` from prompt-supplied `PRODUCT.md` context. High confidence for this benchmark, but not independently repo-verified.
- **Design read:** Reading this as an adaptive native field-task completion/review screen for one-handed operators and tablet managers, with a calm trustworthy operational feel, optimized for fast task completion, verification, and interruption recovery.

## 2. Platform-conformance verdict

- **iOS / iPadOS verdict: release-blocking non-conformance.**  
  The fixed phone canvas, custom navigation/back behavior, disabled Dynamic Type, undersized targets, raw colors, non-semantic theming, and non-reduced motion violate core iOS/iPadOS expectations for native trust, accessibility, and iPad adaptation.

- **Android verdict: release-blocking non-conformance.**  
  Consuming Android Back, bypassing predictive Back, using Cupertino/web controls, fixed pixel typography, undersized `40x40` controls, unchanged phone tabs on tablets, and missing Remove animations support conflict with Material/Android platform behavior.

## 3. Prioritized findings — max five blockers

1. **Accessibility blocker: text scaling and target sizes fail release requirements.**  
   Evidence: fixed `fontSize: 14`, font scaling disabled, all primary actions `40x40`.  
   Impact: fails Dynamic Type / Android font scaling, risks clipped or unreadable task content, and misses iOS `44pt` / Android `48dp` touch targets.

2. **Navigation blocker: platform Back behavior is replaced or trapped.**  
   Evidence: custom top bar, JavaScript back button, empty `BackHandler` consuming Android Back.  
   Impact: breaks iOS navigation stack/edge-swipe trust and Android system/predictive Back; high risk of users losing flow or being unable to exit predictably.

3. **Adaptivity blocker: phone canvas is forced onto tablets.**  
   Evidence: screen forced to `width: 390` and centered on tablets; same bottom tab bar on phone, iPad, and Android tablet.  
   Impact: fails manager review use case in split-screen/multi-window; wastes tablet space and prevents native multi-pane verification workflows.

4. **Design-system/platform blocker: visual language is hard-coded and non-native.**  
   Evidence: raw `#777777` / `#FFFFFF` in both appearances, same Cupertino switch and one web icon set on both platforms.  
   Impact: weak light/dark/high-contrast parity, poor native affordance recognition, and accidental iOS/web port feel on Android.

5. **Motion blocker: completion transition ignores motion accessibility.**  
   Evidence: `500ms` spring with overshoot and no Reduced Motion / Remove animations path.  
   Impact: too expressive for a high-frequency operational confirmation and fails required motion accessibility settings.

## 4. Concrete design moves — max eight

1. **Replace the fixed `390` canvas with window-size-class adaptation.**  
   Compact phone: focused single-column task flow.  
   iPad/tablet/multi-window: task detail + verification pane, or list/detail split where useful.

2. **Restore native navigation contracts.**  
   iOS: native stack behavior with system back affordance and left-edge gesture.  
   Android: real back stack + predictive Back; remove empty `BackHandler` consumption except for explicit unsaved-progress interception.

3. **Use platform-native navigation patterns per width.**  
   Phone: bottom tabs only if these are true top-level destinations.  
   iPadOS: sidebar/split view where manager review benefits from context.  
   Android expanded: navigation rail or drawer when appropriate.

4. **Rebuild primary actions around accessible touch targets.**  
   Minimum `44x44pt` on iOS, `48x48dp` on Android, with adequate spacing and clear labels/state.

5. **Enable scalable typography.**  
   Use iOS Dynamic Type text roles and Android `sp`/font-scale-aware roles; allow font scaling and test large accessibility sizes for clipping and action reachability.

6. **Map shared semantic colors to platform theme roles.**  
   Keep shared roles such as `surface`, `textSecondary`, `actionPrimary`, `success`, `warning`; resolve them to iOS system colors/materials and Material color roles with dark/high-contrast parity.

7. **Swap look-alike controls/icons for native ones.**  
   iOS: native switch, SF Symbols, iOS list/sheet/action patterns.  
   Android: Material Switch, Material Symbols, Material dialogs/sheets/snackbars.

8. **Create a motion accessibility policy.**  
   Default completion: short, calm, platform-consistent confirmation.  
   Reduced Motion / Remove animations: cross-fade or immediate state change; no overshoot.

## 5. Intentional parity matrix

| Area | Shared across platforms | iOS / iPadOS adapts | Android adapts |
|---|---|---|---|
| Product job | Complete, preserve, verify task | Same outcome | Same outcome |
| Content hierarchy | Task status, required fields, evidence, completion CTA | iOS typography/list grammar | Material typography/list grammar |
| Navigation semantics | Same destinations and task state | Native stack, edge Back, iPad sidebar/split | System/predictive Back, nav bar/rail/drawer by width |
| Layout | Same priority order | Size classes, Split View-friendly panes | Window size classes, multi-window/fold posture |
| Controls | Same business meaning | iOS controls, SF Symbols | Material controls, Material Symbols |
| Accessibility outcomes | VO/TalkBack labels, scaling, keyboard traversal, reduced motion | Dynamic Type, VoiceOver traits/actions | Font scale, TalkBack roles/state descriptions |
| Theming | Shared semantic token names | System colors/materials/tint | Material color roles, tonal elevation, Dynamic Color if chosen |
| Motion | Same causal feedback intent | iOS-native transitions, Reduce Motion path | Material motion/predictive Back alignment, Remove animations path |

## 6. Verified versus unverified claims

**Verified from prompt/static description only:**

- Prompt states `PRODUCT.md` platform is `adaptive`.
- Prompt states `DESIGN.md` permits platform-native navigation, controls, icons, materials, and motion.
- Static description reports forced `width: 390`, custom top bar/back button, empty Android `BackHandler`, `40x40` pressables, fixed/scaling-disabled text, raw colors, shared Cupertino switch/web icons, unchanged bottom tabs, and non-reduced `500ms` overshooting spring.

**Unverified and not claimed:**

- Actual source locations or component ownership.
- Actual rendered appearance, contrast, clipping, safe-area behavior, or visual density.
- VoiceOver/TalkBack traversal, labels, roles, state announcements, or keyboard focus order.
- iPad Split View, Android multi-window, rotation, foldable posture, IME/inset behavior.
- Gesture feel, predictive Back animation, haptics, frame rate, or performance.
- iOS Simulator, Android Emulator, or real-device validation.

## 7. Minimal validation plan

1. **Source/static audit**
   - Inspect `PRODUCT.md`, `DESIGN.md`, navigation setup, `BackHandler` usage, layout width constraints, typography props, `allowFontScaling`, color/token usage, platform branches, icon/control imports, and motion settings.

2. **Build/static gates**
   - Run project type-check/lint/tests if available.
   - iOS: run `xcodebuild` compile/test where configured.
   - Android: run Gradle compile/test/assemble where configured.

3. **iOS runtime plan**
   - **iOS Simulator: unverified locally.**
   - Validate iPhone compact, iPad, iPad Split View, rotation, Dynamic Type accessibility sizes, VoiceOver, Reduce Motion, external keyboard traversal, safe areas, and interruption/resume.

4. **Android runtime plan**
   - **Android Emulator: unverified locally.**
   - Validate phone, tablet, multi-window, foldable posture if supported, font scale, TalkBack, Remove animations, predictive Back, hardware keyboard/D-pad, edge-to-edge insets, and interruption/resume.

5. **Real-device plan**
   - **Real-device evidence: missing.**
   - Required before final release claims for gesture Back behavior, haptics, OEM Android differences, sustained performance, and one-handed field usability.
