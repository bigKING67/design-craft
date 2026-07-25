## 1. Evidence level, platform, design read

- **Evidence level:** L0 static/prose review only. Evidence is limited to the prompt and static implementation description.
- **Resolved platform:** `adaptive` — one field-operations product shipping through iOS and Android stores.
- **Style authority:** `DESIGN.md` allows shared semantic color roles/content hierarchy, but explicitly permits platform-native navigation, controls, icons, materials, and motion.
- **Design read:** Reading this as a cross-platform native task-completion flow for field operators and managers, with a calm operational tone, optimized for fast one-handed completion, interruption recovery, and tablet review.

## 2. Platform-conformance verdict

- **iOS:** **Not release-conformant.** The fixed phone canvas, custom top bar/back handling, disabled Dynamic Type, undersized controls, non-semantic colors, non-native controls/icons, unchanged tab layout on iPad, and unguarded spring motion all conflict with iOS/iPadOS expectations.
- **Android:** **Not release-conformant.** Consuming Android Back, bypassing predictive Back, using Cupertino controls/web icons, fixed type, `40x40` targets, static bottom tabs on expanded widths, hard-coded colors, and no Remove animations path break core Android/Material expectations.

## 3. Prioritized findings — max five blockers

1. **Blocked navigation contract**
   - Evidence: custom top bar/JS back replaces native navigation; empty `BackHandler` consumes Android Back.
   - Impact: iOS users lose expected stack/edge-swipe behavior; Android users lose system/predictive Back and may feel trapped.
   - Severity: **P0 iOS + Android.**

2. **Blocked accessibility scaling and input targets**
   - Evidence: fixed `fontSize: 14`, font scaling disabled, all primary actions `40x40`.
   - Impact: fails Dynamic Type/font scaling, one-handed touch reliability, VoiceOver/TalkBack readability, and likely external keyboard/focus ergonomics.
   - Severity: **P0.**

3. **Blocked adaptive layout**
   - Evidence: screen forced to `width: 390` and centered on tablets; bottom tab bar unchanged on phone, iPad, Android tablet.
   - Impact: tablet split-screen/multi-window manager workflow is treated as a letterboxed phone UI, not an adaptive review surface.
   - Severity: **P0.**

4. **Blocked platform-native control/theming system**
   - Evidence: raw `#777777`/`#FFFFFF`; same Cupertino switch and one web icon set on both platforms.
   - Impact: weak light/dark/high-contrast behavior, non-native affordances, and degraded trust on both platforms.
   - Severity: **P1, release-blocking given stated positioning.**

5. **Blocked motion preference compliance**
   - Evidence: 500ms spring with overshoot for task completion and no Reduced Motion/Remove animations alternative.
   - Impact: completion feedback may feel playful/unstable for field work and violates required motion accessibility settings.
   - Severity: **P1, release-blocking for accessibility.**

## 4. Concrete design moves — max eight

1. **Restore native navigation ownership**
   - iOS: native navigation stack, system title behavior, left-edge back.
   - Android: Material top app bar where needed, system Back and predictive Back; remove empty Back consumption.

2. **Replace fixed canvas with size/window-class layouts**
   - Compact phone: single-column, thumb-reachable task flow.
   - iPad/tablet/multi-window: split panes, sidebars/rails, or master-detail review structure.
   - Respect safe areas, cutouts, IME, hinge/fold posture, and split-screen widths.

3. **Adopt platform-native controls and iconography**
   - iOS: native switch, SF Symbols, iOS sheets/menus/alerts where appropriate.
   - Android: Material switch/buttons/chips/dialogs/sheets, Material Symbols.

4. **Fix touch and keyboard affordances**
   - iOS minimum: **44x44pt** effective target.
   - Android minimum: **48x48dp** effective target with spacing.
   - Add visible focus, logical traversal, disabled/loading states, and external keyboard order.

5. **Enable platform text scaling**
   - Use Dynamic Type text styles on iOS and scalable `sp`/Material type roles on Android.
   - Design for accessibility sizes without clipping, hidden actions, or lost hierarchy.

6. **Move colors into semantic tokens**
   - Replace raw `#777777`/`#FFFFFF` with `DESIGN.md` roles.
   - Verify light, dark, and high-contrast mappings; use system/dynamic color where platform-appropriate.

7. **Create an accessibility-safe completion feedback pattern**
   - Default: restrained, platform-consistent completion transition.
   - Reduced Motion / Remove animations: immediate state change or short cross-fade, no overshoot.
   - Completion feedback should reinforce trust, not celebration.

8. **Design interruption resilience explicitly**
   - Autosave task progress, resumable state, clear pending/synced/error states, and non-destructive recovery after app switch, lock, network loss, or split-screen resize.

## 5. Intentional parity matrix

| Area | Shared across platforms | Must adapt per platform |
|---|---|---|
| Product model | Task state, completion rules, verification data | Native persistence hooks and interruption handling |
| Content hierarchy | Task title, status, required fields, completion CTA | iOS title/nav stack vs Android top app bar/back model |
| Navigation | Same destinations and analytics meaning | iOS stack/tabs/sheets; Android predictive Back, nav bar/rail/drawer |
| Controls | Same semantic actions and enabled/disabled logic | Native switches, buttons, pickers, dialogs, sheets |
| Typography | Same hierarchy roles | Dynamic Type on iOS; Material type/`sp` on Android |
| Color | Shared semantic roles from `DESIGN.md` | iOS system materials/tint; Android Material color roles/dynamic color |
| Icons | Same concepts | SF Symbols on iOS; Material Symbols on Android |
| Motion | Same task-state meaning | iOS-native transitions vs Material motion; platform motion settings |
| Adaptivity | Same operator/manager jobs | iPad size classes/Split View; Android window classes/multi-window/foldables |
| Accessibility | Same release outcomes | VoiceOver traits/actions vs TalkBack roles/state descriptions |

## 6. Verified vs unverified claims

**Verified within supplied static evidence**
- Fixed `width: 390` tablet behavior is present.
- Custom top bar/JS back replaces native navigation.
- Android Back is consumed by an empty `BackHandler`.
- Primary actions are `40x40`.
- Font size is fixed at `14` with scaling disabled.
- Raw `#777777` and `#FFFFFF` are used.
- Cupertino-shaped switch and one web icon set ship on both platforms.
- Bottom tab bar does not adapt for tablet.
- Completion transition uses a 500ms overshooting spring without motion-preference alternative.

**Unverified**
- Actual rendered contrast ratios.
- VoiceOver/TalkBack labels, roles, traversal, announcements, and custom actions.
- External keyboard traversal.
- Rotation, split-screen, multi-window, foldable behavior.
- Safe-area, IME, cutout, and hinge handling.
- Runtime animation feel, frame pacing, interruption behavior, and haptics.
- Autosave/resume behavior after interruptions.
- Real iOS/Android build status or store-readiness.

## 7. Minimal validation plan

1. **Source audit**
   - Inspect React Native screen, navigation setup, `BackHandler`, theme tokens, typography utilities, switch/icon imports, tab layout, motion code, and accessibility props.

2. **Build/static checks**
   - Run project type-check/lint/tests if available.
   - iOS: run `xcodebuild` or project iOS build command.
   - Android: run Gradle build/test command.

3. **iOS runtime validation**
   - iOS Simulator: **unverified locally / not performed.**
   - Needed: iPhone compact width, iPad, Split View, rotation, Dynamic Type accessibility sizes, VoiceOver, Reduce Motion, keyboard traversal.

4. **Android runtime validation**
   - Android Emulator: **unverified locally / not performed.**
   - Needed: phone, tablet, multi-window, foldable if supported, font scale, TalkBack, Remove animations, predictive Back, keyboard/D-pad traversal.

5. **Real-device evidence**
   - Real iOS device: **missing.**
   - Real Android device: **missing.**
   - Needed before final claims on gesture feel, predictive Back confidence, haptics, performance, OEM behavior, and one-handed field usability.

**Skill used:** design-craft critique mode. No files edited; no simulator, emulator, browser, build, screenshot, or real-device validation was claimed.
