## 1. Evidence level, resolved platform, design read

- **Evidence level:** L0 static/prose-only review. Evidence is limited to the prompt, `PRODUCT.md`/`DESIGN.md` descriptions, and static implementation notes.  
- **Resolved platform:** `adaptive` native mobile, likely React Native, shipping to **iOS/iPadOS and Android**. Confidence: high from stated store targets and React Native screen evidence.  
- **Design read:** Reading this as a field-operations task-completion surface for one-handed operators and tablet-review managers, with a calm, trustworthy, operationally native feel, optimized for fast completion, verification, and interruption resilience.

## 2. Platform-conformance verdict

### iOS / iPadOS: **Not conformant — release-blocking**
The concept violates core iOS expectations: fixed phone canvas on iPad, custom navigation replacing the native stack and edge-back behavior, undersized targets below 44pt, Dynamic Type disabled, hard-coded colors, weak semantic theming, unchanged phone tab pattern on iPad, and no Reduce Motion alternative.

### Android: **Not conformant — release-blocking**
The concept violates Android expectations: Android Back is consumed by an empty `BackHandler`, predictive/system Back is broken, touch targets are below 48dp, font scaling is disabled, Cupertino controls and web icons are shipped unchanged, Material color/type/navigation patterns are not respected, tablet/multi-window adaptation is missing, and Remove animations is unsupported.

## 3. Prioritized findings

### Blocking findings

1. **Adaptive layout is functionally wrong**
   - Evidence: one screen forced to `width: 390` and centered on tablets; tab bar unchanged across phone/iPad/Android tablet.
   - Impact: manager review in tablet split-screen or multi-window becomes a letterboxed phone app, wasting space and reducing review speed.
   - Blocks: adaptive platform quality, iPadOS, Android tablets, multi-window, split-screen.

2. **Navigation breaks native trust and interruption recovery**
   - Evidence: custom top bar and JavaScript back button replace iOS navigation stack and Android system/predictive Back; empty `BackHandler` consumes Android Back.
   - Impact: users lose platform-learned recovery paths; Android users cannot trust Back; iOS users lose edge-swipe hierarchy behavior.
   - Blocks: iOS conformance, Android conformance, task interruption resilience.

3. **Accessibility release requirements are directly violated**
   - Evidence: `40x40` pressables; fixed `fontSize: 14`; font scaling disabled.
   - Impact: fails minimum target sizes, Dynamic Type/font scaling, likely long-label resilience, and one-handed operator ergonomics.
   - Blocks: VoiceOver/TalkBack readiness, Dynamic Type, Android font scaling, external-keyboard confidence.

4. **Design-system and platform theming are bypassed**
   - Evidence: raw `#777777` and `#FFFFFF`; same Cupertino switch and web icon set on both platforms.
   - Impact: light/dark/high-contrast behavior is fragile; platform-native affordances are lost; Android reads as an iOS/web port.
   - Blocks: trustworthy native positioning and `DESIGN.md` semantic-role contract.

5. **Motion is inappropriate and inaccessible**
   - Evidence: task-complete transition is a 500ms overshooting spring with no Reduce Motion/Remove animations alternative.
   - Impact: too expressive for frequent operational completion, may delay perceived confirmation, and fails vestibular/system-motion requirements.
   - Blocks: Reduced Motion / Remove animations release requirement.

## 4. Concrete design moves

1. **Replace fixed `390` layout with adaptive structure**
   - Compact phone: single-column task flow.
   - Medium/expanded/tablet: split task detail + verification pane, rail/sidebar where appropriate.
   - Drive by window size classes, split-screen width, orientation, and fold posture—not device names.

2. **Restore platform-native navigation**
   - iOS: native stack behavior, edge-swipe Back, large/inline titles where appropriate.
   - Android: system Back and predictive Back; never consume Back with an empty handler.
   - If a dirty task exists, autosave first; ask only when data loss is real.

3. **Adapt navigation surfaces by platform and size**
   - iPhone: native tab bar only for true top-level sections.
   - iPad: sidebar/split view where review context benefits from parallel panes.
   - Android phone: Material navigation bar.
   - Android tablet/foldable: navigation rail or drawer as appropriate.

4. **Increase hit targets and separate visual size from touch area**
   - iOS minimum: 44x44pt.
   - Android minimum: 48x48dp with comfortable spacing.
   - Primary completion action should be thumb-reachable on phone and contextually placed near verification content on tablet.

5. **Enable text scaling**
   - Use iOS Dynamic Type-compatible text styles and Android `sp`/Material type roles.
   - Remove font-scaling disablement.
   - Validate at large accessibility sizes, long task names, localized strings, and dense manager-review content.

6. **Map shared semantic roles to platform-native color systems**
   - Keep `DESIGN.md` semantic roles shared.
   - Implement them through iOS dynamic/system colors and Android Material color roles.
   - Remove raw `#777777` / `#FFFFFF` except where explicitly tokenized and contrast-tested.

7. **Use platform-native controls and iconography**
   - iOS: native switch semantics and SF Symbols where appropriate.
   - Android: Material Switch, Material Symbols, Material buttons/sheets/dialogs/snackbars.
   - Share domain meaning, labels, and state; do not force identical control shapes.

8. **Redesign completion motion**
   - Default: short, calm confirmation under ~300ms, no overshoot for routine operations.
   - Reduced Motion / Remove animations: immediate state change or subtle fade.
   - Optional haptic feedback only at the causal completion moment and only respecting platform settings.

## Intentional parity matrix

| Area | Stays shared | Must adapt per platform |
| --- | --- | --- |
| Product flow | Task states, completion rules, verification model, autosave semantics | Native navigation stack, Back behavior, gestures |
| Content hierarchy | Task title, status, required fields, verification summary | Large title vs top app bar, pane/sidebar/rail presentation |
| Design tokens | Semantic roles: background, text, warning, success, action | iOS dynamic colors/materials; Android Material color roles/elevation |
| Accessibility outcomes | Screen-reader meaning, scalable text, keyboard traversal, reduced motion | VoiceOver traits/actions; TalkBack roles/state descriptions; platform focus order |
| Controls | Domain labels and enabled/disabled/error states | iOS controls/SF Symbols; Android Material controls/Symbols |
| Motion intent | Completion should confirm state without disrupting work | iOS Reduce Motion path; Android Remove animations path; platform-specific transition idioms |
| Tablet behavior | Manager can review more context efficiently | iPad split/sidebar patterns; Android rail/drawer/fold/multi-window handling |
| Analytics | Same task events and completion semantics | Platform-specific navigation/back/cancel event context |

## 5. Verified vs unverified claims

### Verified from provided static evidence only
- Screen is forced to `width: 390`.
- Tablet layout is centered instead of structurally adapted.
- Custom top bar and JS back button replace platform navigation.
- Android Back is consumed by an empty `BackHandler`.
- Primary actions use `40x40` pressables.
- Text uses fixed `fontSize: 14` with font scaling disabled.
- Raw `#777777` and `#FFFFFF` are used.
- Cupertino switch and web icon set are shared across platforms.
- Bottom tab bar is unchanged across phone/tablet platforms.
- Completion motion is a 500ms overshooting spring with no reduced-motion alternative.

### Unverified / not claimed
- No source tree was inspected.
- No build, lint, type-check, or unit test was run.
- No screenshot, accessibility tree, simulator, emulator, or hardware evidence exists.
- No VoiceOver/TalkBack traversal was observed.
- No Dynamic Type/font-scale runtime behavior was observed.
- No rotation, iPad Split View, Android multi-window, foldable, keyboard, IME, dark mode, high contrast, or offline/interruption behavior was observed.
- No performance, frame pacing, haptics, or gesture feel was validated.

## 6. Minimal validation plan

### Source/static validation
- Inspect `PRODUCT.md` and `DESIGN.md` to confirm adaptive platform and token authority.
- Inspect React Native screen/component code for:
  - fixed width/layout constraints
  - `BackHandler` usage
  - navigation implementation
  - `allowFontScaling={false}` or equivalent
  - hard-coded colors
  - touch target sizes
  - shared switch/icon imports
  - motion settings and reduced-motion branches
- Run closest project scripts from `package.json`: type-check, lint, unit tests if present.

### Build validation
- iOS: run the project’s normal iOS build path, e.g. Xcode/`xcodebuild` for the app scheme.
- Android: run Gradle compile/lint path, e.g. `./gradlew assembleDebug lint`, adjusted to the actual project.

### Runtime validation required before release claims
- **iOS Simulator: unverified locally.** Required checks: iPhone + iPad, portrait/landscape, Dynamic Type sizes, Reduce Motion, dark mode/high contrast where supported, VoiceOver traversal, external keyboard.
- **Android Emulator: unverified locally.** Required checks: phone + tablet/foldable profile, multi-window, font scale, Remove animations, TalkBack traversal, system/predictive Back, keyboard/D-pad where relevant.
- **Real-device evidence: missing.** Required before final claims for touch feel, native Back/edge gestures, haptics, performance, OEM Android behavior, and one-handed field-operation ergonomics.

Selected skill used: `design-craft` critique mode with native adaptive references.
