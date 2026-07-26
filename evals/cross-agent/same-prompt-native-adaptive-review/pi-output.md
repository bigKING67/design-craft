## 1. Evidence level, resolved platform, design read

- **Evidence level:** static contextual review only — prompt + implementation description. No source tree, build output, screenshots, accessibility tree, simulator/emulator, or device evidence.
- **Resolved platform:** `adaptive` from provided `PRODUCT.md` context; confidence is contextual, not file-verified.
- **Style authority:** provided `DESIGN.md` allows shared semantic color/content hierarchy while permitting native navigation, controls, icons, materials, and motion.
- **Design read:** Reading this as a cross-platform field task completion app for one-handed operators and tablet managers, with a calm operational-native feel, optimized for fast completion, verification, and interruption-safe progress.

## 2. Platform-conformance verdict

### iOS / iPadOS verdict: **Failing release conformance**
The concept reads as a centered phone canvas with custom chrome, not an iOS/iPadOS-native task surface. Static evidence conflicts with iOS expectations for navigation stack behavior, left-edge back, Dynamic Type, 44pt targets, semantic colors/materials, SF Symbols/native controls, Reduce Motion, and iPad size-class adaptation.

### Android verdict: **Failing release conformance**
The concept violates Android-native expectations more severely because Android Back is explicitly consumed. Static evidence conflicts with system/predictive Back, Material controls, 48dp targets, `sp` font scaling, semantic Material color roles, adaptive navigation for tablet widths, Remove animations, and Android multi-window/foldable readiness.

## 3. Prioritized blocking findings

1. **[Blocker: navigation + interruption safety] Custom back replaces OS navigation.**  
   Evidence: custom top bar/JS back button replaces iOS stack and Android system/predictive Back; empty `BackHandler` consumes Android Back.  
   Impact: breaks native trust, expected escape behavior, predictive Back previews, keyboard/system traversal assumptions, and may increase progress-loss risk during interruptions.

2. **[Blocker: accessibility] Text and targets fail platform minimums.**  
   Evidence: fixed `fontSize: 14`, font scaling disabled, all primary actions `40x40`.  
   Impact: fails Dynamic Type/font scaling requirements; misses iOS 44pt and Android 48dp target floors for primary actions, especially for one-handed field use.

3. **[Blocker: adaptivity] Tablet and multi-window are treated as centered phone.**  
   Evidence: one screen forced to `width: 390` and centered on tablets; bottom tab unchanged on phone, iPad, and Android tablet.  
   Impact: manager review in tablet split-screen/multi-window is not structurally supported; content does not adapt to iPad size classes, Android window size classes, fold posture, or expanded input modes.

4. **[Blocker: platform controls + theming] Shared visual look overrides native semantics.**  
   Evidence: same Cupertino-shaped switch and web icon set on both platforms; raw `#777777` and `#FFFFFF` in both appearances.  
   Impact: Android looks like an iOS/web port; iOS misses system color/material behavior; dark/high-contrast parity and token governance are suspect.

5. **[Blocker: motion accessibility] Completion transition ignores motion settings.**  
   Evidence: 500ms overshooting spring with no Reduced Motion/Remove animations alternative.  
   Impact: violates release accessibility requirements and risks making task completion feel playful or unstable instead of calm and operational.

## 4. Concrete design moves

1. **Restore native navigation ownership.**  
   Use iOS navigation stack with native back/edge gesture; use Android Navigation/system Back with predictive Back support. Remove the empty Android `BackHandler` except for explicit, tested unsaved-change confirmation.

2. **Make task progress interruption-safe.**  
   Persist draft/progress state independently of screen lifetime; on return, restore the same task, step, scroll/focus context, and completion status. Use native confirmation only when leaving would discard unsaved work.

3. **Replace fixed phone canvas with window-class layouts.**  
   Compact: single-column task flow. Medium/expanded: split task details, evidence, and verification pane. iPad Split View and Android multi-window must reflow rather than center `390`.

4. **Adapt navigation by form factor.**  
   Phone: bottom tabs only for true top-level destinations. iPad: sidebar or split navigation where appropriate. Android tablet: navigation rail/drawer where Material guidance fits. Do not keep the identical tab bar everywhere.

5. **Use platform-native controls and iconography.**  
   iOS: native switch, SF Symbols, iOS list/sheet/menu conventions. Android: Material switch/buttons/chips/dialogs, Material Symbols, Material top app bar/FAB only where semantically appropriate.

6. **Repair accessibility primitives.**  
   Enable font scaling; map text to semantic type roles; ensure no clipping at large accessibility sizes; raise primary targets to at least 44pt iOS / 48dp Android with adequate spacing; verify external keyboard focus order.

7. **Move colors to semantic roles.**  
   Replace raw `#777777`/`#FFFFFF` with shared semantic tokens that resolve to iOS system colors/materials and Android Material color roles, including dark and high-contrast behavior.

8. **Create platform-aware completion motion.**  
   Default: short, calm native transition with no overshoot for operational confirmation. Reduced Motion/Remove animations: immediate state change or brief cross-fade, preserving completion feedback without spring travel.

## 5. Intentional parity matrix

| Area | Stays shared | Must adapt per platform |
|---|---|---|
| Product flow | Task states, completion rules, verification model, draft recovery | Native navigation stack/back behavior |
| Content | Labels, hierarchy, required fields, error meaning | Typography roles and scaling primitives |
| Tokens | Semantic roles: surface, text, danger, success, focus | iOS system colors/materials vs Android Material roles/elevation |
| Controls | Business meaning of toggles/actions | Native switch, picker, sheet, dialog, menu, icon set |
| Navigation | Destination model and analytics names | iOS tab/sidebar patterns; Android bar/rail/drawer + predictive Back |
| Motion | Feedback intent: complete, save, error, restore | iOS/Android motion idioms; Reduce Motion vs Remove animations |
| Accessibility | Required outcomes for VO/TalkBack, scaling, keyboard | Traits/roles/state descriptions/custom actions per OS |
| Adaptivity | Same task can complete/review everywhere | Phone, tablet, split-screen, multi-window, fold posture layouts |

## 6. Verified versus unverified claims

### Verified from provided static evidence
- `platform` is described as adaptive.
- The implementation uses forced `width: 390` centered on tablets.
- Custom top bar/JS back replaces native stack/system Back.
- Empty Android `BackHandler` consumes Back.
- Primary actions are `40x40`.
- Text is fixed `14` with scaling disabled.
- Raw `#777777` and `#FFFFFF` are used.
- Same Cupertino switch and web icon set ship cross-platform.
- Bottom tab bar is unchanged across phone/tablet.
- Completion transition is 500ms overshooting spring with no motion alternative.

### Unverified and not claimed
- Actual visual appearance, density, contrast ratios, clipping, or overflow.
- VoiceOver/TalkBack labels, traits, traversal, announcements, or state descriptions.
- Real iPad Split View, Android multi-window, rotation, foldable, or keyboard behavior.
- Gesture feel, frame rate, haptics, battery/thermal behavior, or perceived smoothness.
- Whether other screens/components compensate for these issues.
- Any simulator, emulator, or real-device result.

## 7. Minimal validation plan

1. **Source/static checks**
   - Inspect navigation setup, BackHandler usage, tab/sidebar/rail branching, token usage, font-scaling props, target sizing, and motion preference handling.
   - Add/verify tests for draft persistence across background/foreground, route pop, process restore where feasible.

2. **Build checks**
   - iOS: run project iOS type/lint plus `xcodebuild` compile/test if available.
   - Android: run JS/TS checks plus Gradle assemble/test if available.
   - These would prove build/static integration only, not runtime UX quality.

3. **iOS runtime checks — missing evidence**
   - **iOS Simulator: unverified locally.**
   - Needed: iPhone compact + iPad regular + iPad Split View; Dynamic Type accessibility sizes; Reduce Motion; VoiceOver; external keyboard; light/dark/high contrast where supported.
   - **Real iOS/iPadOS device evidence: missing**, required before final claims on gestures, haptics, and one-handed field feel.

4. **Android runtime checks — missing evidence**
   - **Android Emulator: unverified locally.**
   - Needed: phone + tablet + multi-window/foldable profile where applicable; font scale; Remove animations; TalkBack; hardware keyboard/D-pad; gesture navigation with predictive Back.
   - **Real Android device evidence: missing**, required before final claims on OEM Back behavior, gestures, haptics, and sustained performance.
