# Pi observed output

- Agent: Pi CLI
- Version: `pi 0.80.3`
- Date: 2026-07-10
- Command summary: `pi --no-session --no-tools --skill <repo>/skills/design-craft -p @prompt.md`
- Skill path observed: `/Users/gaoqian/Documents/sixseven/codeproject/design-craft/skills/design-craft`
- Evidence boundary: read-only prompt/source review; runtime behavior remains unverified.
- Benchmark contract: output includes concrete design move recommendations.

## Output

## Benchmark Response

### 1. Evidence Level, Resolved Platform, and Design Read

- **Evidence level**: Static implementation evidence only. The prompt provides a description of a React Native screen’s behavior, styling, and component choices. **No source tree, build artifact, screenshot, simulator/emulator, or real-device evidence was provided.** All design decisions are inferred from the static description.
- **Resolved platform**: `adaptive` (iOS and Android, shipping through both stores). The product is explicitly described as targeting both platforms with a single codebase.
- **Design read**: `PRODUCT.md` and `DESIGN.md` are referenced but not actually read. The prompt summarizes key points: shared semantic color roles, content hierarchy, platform-native navigation/controls/icons/materials/motion allowance. The actual design files are not available for review.

### 2. Platform-Conformance Verdict

- **iOS**: **Non-conformant**. The custom top bar and JavaScript back button replace the system navigation stack, breaking swipe-to-go-back and the platform-native back gesture. The `BackHandler` override is unnecessary on iOS and may interfere with other gestures. Fixed `fontSize: 14` and disabled font scaling violates Dynamic Type. A Cupertino-shaped switch on both platforms is technically a custom control that may not match iOS HIG exactly (and is wrong for Android). Hardcoded `#777777` and `#FFFFFF` bypass semantic color roles, risking dark mode and accessibility contrast issues. The 500ms spring with overshoot has no Reduced Motion alternative, violating iOS accessibility requirements.
- **Android**: **Non-conformant**. The custom top bar and JS back button ignore the system/predictive Back gesture, and the empty `BackHandler` consumer **blocks the Android system Back gesture entirely**, which is a severe navigation violation. Cupertino switch is non-native on Android and breaks Material Design expectations. The same web icon set ships on both platforms, ignoring Android’s Material iconography. Fixed font scaling rules out Android’s font scaling accessibility. The 500ms spring with overshoot conflicts with Android’s Remove animations requirement. The bottom tab bar unchanged across devices ignores Android tablet split-screen and multi-window conventions.

### 3. Prioritized Findings

**Accessibility (Critical)**
1. `fontSize: 14` with font scaling disabled breaks both Dynamic Type (iOS) and font scaling (Android). Screen readers may not read the content correctly if text does not scale.
2. Reduced Motion/Remove animations is ignored: the 500ms spring transition has no alternative, violating WCAG 2.2 and platform guidelines.
3. No mention of accessibility labels, roles, or states for VoiceOver/TalkBack. The 40×40 pressables may be too small for touch targets (44×44 minimum recommended).
4. External keyboard traversal is mentioned as a requirement but not evidenced in the static code.

**Navigation (High)**
5. Custom top bar and JavaScript back button replace system navigation stack on iOS, breaking swipe-to-go-back and system back gesture.
6. Empty `BackHandler` on Android **consumes and swallows the system Back gesture**, making the app unresponsive to Android’s back navigation. This is a platform-conformance blocker.
7. No mention of deep linking, state restoration, or interruption recovery, which is a core product requirement.

**Control & Interaction (High)**
8. All primary actions use `40×40` pressables, which is below the 44×44 touch target minimum on both platforms.
9. Cupertino-shaped switch on Android is a non-native control that violates user expectations.
10. A single web icon set on both platforms ignores platform-native iconography (SF Symbols vs. Material Symbols).

**Theming & Appearance (Medium)**
11. Raw `#777777` and `#FFFFFF` are used in both appearances instead of semantic color roles from `DESIGN.md`. This breaks dark mode, accessibility contrast, and platform-adaptive appearance.
12. No evidence of dynamic color support for iOS 13+ or Material You theming.

**Motion (Medium)**
13. 500ms spring with overshoot may be too slow and bouncy for a task-completion transition. It has no Reduced Motion alternative, and the duration may not align with platform motion guidelines.

**Adaptivity (Medium)**
14. Screen forced to `width: 390` and centered on tablets breaks iPad and Android tablet split-screen/multi-window usage. The task manager reviewing in tablet split-screen is a core user scenario.
15. Bottom tab bar unchanged across phone, iPad, and Android tablet ignores platform conventions (iPad uses a sidebar or top-level navigation, Android tablets may use a navigation rail).

### 4. Concrete Design Moves and Intentional Parity Matrix

**Design Moves**

- **Navigation design move**: Replace the custom top bar and JS back button with the platform-native navigation stack. On iOS, use `UINavigationController`-style navigation (React Navigation’s native stack). On Android, respect the system Back gesture. Remove the empty `BackHandler` that blocks Android Back.
- **Typography design move**: Remove fixed `fontSize: 14` and font scaling disable. Use `Dynamic Type` on iOS (through `allowFontScaling` and `Text` component props) and respect Android’s font scaling. Use relative sizes (e.g., `title`, `body`, `callout`) from the semantic type scale.
- **Motion design move**: Provide a reduced-motion alternative for the task-complete transition. On iOS, check `UIAccessibility.isReduceMotionEnabled` and use a cross-fade or shorter duration. On Android, check `remove animations` setting. Use `LayoutAnimation` or `Animated` with a duration that respects the system setting.
- **Color design move**: Replace raw `#777777` and `#FFFFFF` with semantic color roles from `DESIGN.md`. On iOS, use `UIUserInterfaceStyle` for dark mode. On Android, use `Theme.Material3` dynamic colors. Provide a `PlatformColor` or custom theme tokens that adapt per platform.
- **Control design move**: Increase touch targets to at least 44×44. Use platform-native switches: `Switch` on iOS (Cupertino) and `Switch` on Android (Material). Replace the web icon set with platform-native icons: `SF Symbols` on iOS, `Material Symbols` on Android.
- **Adaptivity design move**: Remove fixed width `390` and center on tablets. Use `useWindowDimensions` and `SafeAreaView` to support split-screen and multi-window on iPad and Android tablets. Consider a two-column layout for tablet managers. Adapt the bottom tab bar: on iPad, use a sidebar or top-level navigation; on Android tablets, use a navigation rail.

**Intentional Parity Matrix**

| Layer | Shared | Adapts per Platform |
|---|---|---|
| Content hierarchy | Task data model, fields, completion state | – |
| Semantic color roles | Light/dark token definitions (e.g., `primary`, `surface`, `error`) | Platform-native color resolution (e.g., `PlatformColor`, `DynamicColorIOS`) |
| Navigation structure | Screen order, flow logic | Navigation controller (iOS native stack, Android system Back) |
| Controls | Task completion action logic | Switch style (Cupertino vs. Material), iconography (SF Symbols vs. Material Symbols) |
| Motion | Task completion state transition | Animation duration and curve (respect Reduced Motion/Remove animations) |
| Typography | Semantic type scale (e.g., `body`, `caption`) | Font scaling behavior (Dynamic Type vs. font scaling) |
| Layout | Content importance and order | Responsive layout for tablet split-screen/multi-window; bottom bar vs. sidebar/rail |

### 5. Verified versus Unverified Claims

- **Verified**: The static implementation description contains the specific anti-patterns listed (custom top bar, fixed width, raw colors, disabled font scaling, etc.). The prompt’s description is self-consistent and can be evaluated against known platform guidelines.
- **Unverified**: All runtime behavior, actual accessibility tree, screen reader announcements, rotation/split-screen behavior, real-device performance, haptic feedback, and visual appearance are **unverified**. The `PRODUCT.md` and `DESIGN.md` contents are not actually read; only the prompt’s summary is available. No build, simulator, or real-device testing was performed. The claim that “one React Native screen is forced to width: 390” is taken as true for the purpose of this benchmark, but it is not independently verified against a source file.

### 6. Minimal Source/Build/Runtime Validation Plan

To move from static description to evidence-based validation, the following minimal steps are required:

1. **Source validation**: Inspect the actual React Native code for the screen, navigation setup, and theming. Confirm the static claims (fixed width, font size, raw colors, custom back button, etc.).
2. **iOS Simulator (missing evidence)**:
   - Run on iPhone and iPad simulators.
   - Test Dynamic Type by changing text size in Settings → Accessibility → Display & Text Size.
   - Test VoiceOver: verify accessibility labels, focus order, and custom actions.
   - Test Reduced Motion: enable in Settings → Accessibility → Motion and observe the task-complete transition.
   - Test iPad split-screen: drag the app into split-screen and verify layout adapts.
   - Test rotation and external keyboard navigation.
3. **Android Emulator (missing evidence)**:
   - Run on phone and tablet emulators.
   - Test TalkBack accessibility.
   - Test font scaling under Settings → Accessibility → Font size.
   - Test Remove animations under Settings → Accessibility → Remove animations.
   - Test system Back gesture: swipe from edge and observe behavior.
   - Test multi-window: put the app in split-screen and verify layout.
4. **Real-device validation (missing evidence)**:
   - One-handed usage on a phone (target: single-handed field operator).
   - Haptic feedback on task completion.
   - Dark mode appearance on both platforms.
   - External keyboard navigation on iPad.

The benchmark response is based solely on static implementation evidence. All platform-conformance, accessibility, and adaptivity findings are **unverified** and require the above validation steps to be confirmed.
