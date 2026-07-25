## 1. Evidence level, platform, design read

- **Evidence level:** L0 static/prose implementation evidence only. No source tree, screenshot, accessibility tree, rotation, split-screen, foldable, simulator/emulator, or hardware run.
- **Resolved platform:** `adaptive`, explicit from supplied `PRODUCT.md` context. Confidence: high for intended platform, low for actual runtime quality.
- **Design read:** Reading this as a native field-task completion surface for one-handed operators and tablet-review managers, with a calm operational tone, optimized for fast completion, verification, interruption recovery, and platform trust.

## 2. Platform-conformance verdict

- **iOS / iPadOS verdict: Block release.** The fixed phone canvas, custom navigation/back behavior, disabled Dynamic Type, undersized targets, non-semantic colors, and non-adaptive tab layout fail core iOS/iPadOS expectations.
- **Android verdict: Block release.** Consuming Android Back, bypassing predictive Back, using Cupertino/web controls, fixed type, undersized 40dp targets, raw colors, and unchanged phone tabs on tablets fail Android native trust and accessibility requirements.

## 3. Prioritized findings — max five blockers

1. **Adaptive structure is not adaptive.**
   - Evidence: screen forced to `width: 390` and centered on tablets; bottom tab bar unchanged on phone, iPad, and Android tablet.
   - Impact: manager review in split-screen/multi-window becomes a letterboxed phone UI instead of a tablet work surface; content hierarchy and input mode do not adapt.

2. **Navigation breaks both platform contracts.**
   - Evidence: custom top bar and JS back button replace iOS navigation stack and Android system/predictive Back; empty `BackHandler` consumes Android Back.
   - Impact: users lose learned escape/recovery behavior; Android users may be trapped; iOS loses stack affordances and edge-back expectations.

3. **Accessibility release requirements are directly contradicted.**
   - Evidence: all primary actions are `40x40`; text fixed at `fontSize: 14` with scaling disabled.
   - Impact: misses iOS 44pt and Android 48dp target floors; Dynamic Type/font scaling cannot work; one-handed field use and assistive traversal become fragile.

4. **Visual system and controls are accidental parity, not adaptive parity.**
   - Evidence: raw `#777777` and `#FFFFFF` in both appearances; same Cupertino switch and web icon set on both platforms.
   - Impact: violates `DESIGN.md` semantic color roles; likely weak dark/high-contrast behavior; Android reads as an iOS/web port and iOS loses native symbol/control semantics.

5. **Completion motion is too expressive and not accessibility-safe.**
   - Evidence: task-complete transition is a 500ms spring with overshoot and no Reduced Motion/Remove animations alternative.
   - Impact: a high-value operational confirmation becomes delayed/flashy; vestibular/accessibility settings are ignored; “calm and trustworthy” is undermined.

## 4. Concrete design moves — max eight

1. **Replace fixed `390` layout with window-size adaptation.**
   - Compact: one-column task flow.
   - Medium/expanded: split task detail + verification/review pane.
   - Support iPad Split View, Android multi-window, orientation, IME, safe areas, and fold posture.

2. **Restore native navigation ownership.**
   - iOS: native stack/navigation controller behavior, platform title treatment, preserved edge-back where applicable.
   - Android: remove empty `BackHandler`; integrate system Back and predictive Back; only intercept with explicit unsaved-progress confirmation.

3. **Adapt navigation chrome by platform and width.**
   - Phone: bottom tabs only if they represent true top-level destinations.
   - iPad: consider sidebar/tab sidebar or split navigation.
   - Android tablet: navigation rail or drawer where destination count and hierarchy justify it.

4. **Rebuild touch and keyboard interaction contract.**
   - iOS targets at least 44x44pt; Android targets at least 48x48dp with adequate spacing.
   - Add visible focus, logical external-keyboard traversal, accessibility labels/roles/state values, and custom actions where needed.

5. **Enable platform text scaling.**
   - Use Dynamic Type/text styles on iOS and scalable `sp`/Material type roles on Android.
   - Validate large accessibility sizes without clipping, hidden actions, or broken task progress.

6. **Tokenize colors and appearance states.**
   - Replace raw `#777777`/`#FFFFFF` with shared semantic roles from `DESIGN.md`.
   - Provide light, dark, elevated/surface, disabled, focus, success, warning, and high-contrast-safe mappings per platform.

7. **Use native controls, icons, and feedback.**
   - iOS: native switch semantics, SF Symbols, iOS materials/tint where appropriate.
   - Android: Material 3 switch, Material Symbols, tonal elevation/Dynamic Color fallback where appropriate.
   - Share labels and state meaning, not identical pixels.

8. **Define a calm completion and recovery motion policy.**
   - Default completion: immediate status change plus restrained platform-native transition.
   - Reduced Motion/Remove animations: cross-fade or immediate state update.
   - Completion should not hide whether progress was saved; interruptions must resume without task loss.

## 5. Intentional parity matrix

| Area | Shared across platforms | iOS / iPadOS adapts | Android adapts |
|---|---|---|---|
| Product flow | task completion, verification, saved-progress semantics | stack/sheet/sidebar conventions | system Back, predictive Back, Material navigation |
| Content hierarchy | task state, required fields, completion status | large/inline titles, iPad panes | top app bar, nav bar/rail/drawer |
| Design tokens | semantic roles and state meanings | system colors/materials/SF Symbols mapping | Material color roles/tonal elevation/Material Symbols |
| Controls | labels, validation rules, enabled/disabled states | iOS-native switch/pickers/actions | Material switch/pickers/snackbars/dialogs |
| Accessibility | VO/TalkBack outcomes, scaling, keyboard traversal | Dynamic Type, VoiceOver traits/actions | font scaling, TalkBack roles/state descriptions |
| Motion | calm confirmation, reduced-motion outcome | Reduce Motion cross-fade/reduced travel | Remove animations immediate/cross-fade path |
| Tablet use | manager review must gain structure | iPad Split View/sidebar/panes | Android tablet multi-window/rail/fold posture |

## 6. Verified vs unverified claims

**Verified from supplied static description only:**
- Fixed 390-wide centered layout exists.
- Custom top bar/JS back replaces native navigation.
- Empty Android `BackHandler` consumes Back.
- Primary actions are 40x40.
- Text is fixed 14 with font scaling disabled.
- Raw colors are used.
- Same Cupertino switch and web icon set ship on both platforms.
- Bottom tabs do not adapt across phone/tablet.
- 500ms overshooting completion spring lacks reduced-motion alternative.

**Unverified and not claimed:**
- Actual rendered contrast ratios.
- VoiceOver/TalkBack traversal, labels, roles, or announcements.
- Real split-screen, rotation, foldable, keyboard, IME, safe-area behavior.
- Actual persistence under interruption.
- Runtime smoothness, frame rate, haptics, or perceived device feel.
- Any simulator, emulator, or real-device result.

## 7. Minimal validation plan

1. **Source/static checks**
   - Inspect React Native screen, navigation setup, BackHandler usage, style tokens, text scaling props, pressable dimensions, icon/control imports, and motion settings.
   - Run type-check/lint/build if project scripts exist.

2. **iOS runtime evidence — missing**
   - Build with Xcode/CI where available.
   - Test iPhone compact and iPad Split View in **iOS Simulator**.
   - Verify Dynamic Type, VoiceOver, Reduce Motion, dark/high-contrast appearance, keyboard traversal.
   - **iOS Simulator: unverified locally.**
   - Real iPhone/iPad still required before claiming gesture, haptic, interruption, or sustained-performance quality.

3. **Android runtime evidence — missing**
   - Build with Gradle/CI where available.
   - Test phone, tablet, multi-window/foldable profile in **Android Emulator**.
   - Verify TalkBack, font scaling, Remove animations, predictive Back, dark theme, keyboard/D-pad traversal.
   - **Android Emulator: unverified locally.**
   - Real Android hardware still required before claiming OEM Back behavior, gesture feel, haptics, or performance quality.

**Overall decision:** Block release until adaptive layout, native navigation/back, accessibility scaling/targets, semantic theming/native controls, and reduced-motion-safe completion are corrected and validated on both platforms.
