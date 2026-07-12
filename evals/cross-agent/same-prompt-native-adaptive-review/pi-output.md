## 1. Evidence level, platform, design read

- **Evidence level:** L0 static/prose-only review with product context supplied. No source tree, build, screenshot, accessibility tree, rotation, split-screen, foldable, simulator, emulator, or hardware run was performed.
- **Resolved platform:** `adaptive` from supplied `PRODUCT.md` platform. Confidence: high for intent, unverified for actual repo targets.
- **Design read:** Reading this as a native adaptive field-operations task flow for one-handed operators and tablet-review managers, with a calm trustworthy operational tone, optimized for fast completion, verification, and interruption recovery.

## 2. Platform-conformance verdict

- **iOS / iPadOS verdict: Block release.** The concept violates core native trust requirements: fixed phone canvas on iPad, custom navigation/back behavior, undersized targets, disabled Dynamic Type, non-semantic colors, non-native icon/control grammar, and missing Reduce Motion alternative.
- **Android verdict: Block release.** The concept violates Material/Android behavior: Android Back and predictive Back are consumed, touch targets are below `48dp`, font scaling is disabled, iOS-shaped controls ship on Android, tablet navigation does not adapt, and Remove animations is not honored.

## 3. Prioritized blocking findings

1. **Accessibility release requirements are directly broken.**  
   Evidence: `40x40` pressables, fixed `fontSize: 14`, font scaling disabled, no Reduced Motion/Remove animations path.  
   Impact: fails VoiceOver/TalkBack operability, Dynamic Type/font scaling, motor accessibility, and motion-sensitivity requirements.

2. **Navigation breaks native platform trust and Android system behavior.**  
   Evidence: custom top bar/JS back replaces iOS navigation stack and Android system/predictive Back; empty `BackHandler` consumes Android Back.  
   Impact: users cannot rely on learned back gestures, predictive Back previews, native hierarchy, or recovery expectations.

3. **Adaptive layout is a phone mock inside tablet space.**  
   Evidence: one React Native screen forced to `width: 390` and centered on tablets; bottom tab bar unchanged on phone, iPad, and Android tablet.  
   Impact: manager split-screen/multi-window review is underserved; tablet affordances, size classes, rails/sidebars/panes, and resize resilience are absent.

4. **Design-system and theming contract is bypassed.**  
   Evidence: raw `#777777` and `#FFFFFF` used in both appearances despite shared semantic color roles; same web icon set and Cupertino-shaped switch on both platforms.  
   Impact: weak dark/high-contrast behavior, possible contrast failure, and platform-inappropriate controls reduce trust.

5. **Completion motion is too expressive and not accessibility-aware.**  
   Evidence: `500ms` spring with overshoot and no Reduced Motion/Remove animations alternative.  
   Impact: excessive for a high-frequency operational task, potentially vestibular, and mismatched to calm trustworthy positioning.

## 4. Concrete design moves

1. **Replace fixed `390` layout with window-size adaptation.**  
   Compact phone: single task stack. Medium/expanded: task list + detail/review pane, or review sidebar. Support iPad Split View, Android multi-window, orientation, IME, and fold posture.

2. **Restore native navigation ownership.**  
   iOS: native stack/large-or-inline titles, preserved left-edge back gesture.  
   Android: system Back/predictive Back integration; only intercept for explicit unsaved-work confirmation, never with an empty consumer.

3. **Raise and clarify action targets.**  
   iOS minimum `44x44pt`; Android minimum `48x48dp` with spacing. Use labeled primary actions where ambiguity exists, not icon-only `40x40` buttons for critical task completion.

4. **Use scalable type roles.**  
   Map content hierarchy to platform text roles; enable Dynamic Type/font scaling; verify 200% text, wrapping, truncation, and reachable actions.

5. **Use platform-native controls and iconography.**  
   iOS: native switch, SF Symbols, system materials.  
   Android: Material switch, Material Symbols, tonal elevation, Android top app bars/navigation patterns.

6. **Map shared semantic tokens to platform implementations.**  
   Keep roles such as `surface`, `text.secondary`, `action.primary`, `status.success`; resolve them to iOS system colors/materials and Android Material ColorScheme/Dynamic Color-compatible values. Remove raw `#777777`/`#FFFFFF` from components.

7. **Adapt navigation chrome by width.**  
   Phone: bottom tabs only if they represent true top-level destinations.  
   iPad: sidebar/tab sidebar where appropriate.  
   Android tablet: navigation rail or drawer where appropriate. Do not keep identical phone tabs everywhere.

8. **Redesign completion feedback for operations.**  
   Use immediate state change plus short confirmation. Default: crisp fade/settle under ~300ms, no overshoot. Reduced Motion/Remove animations: cross-fade or immediate state, with accessibility announcement and optional restrained platform haptic at the causal moment.

## 5. Intentional parity matrix

| Area | Shared across platforms | iOS / iPadOS adaptation | Android adaptation |
|---|---|---|---|
| Product flow | Task complete, verify, preserve progress | Native stack/sheets where appropriate | Material hierarchy, Back-aware flow |
| Content hierarchy | Same task fields, status, evidence, review order | iOS typography/material mapping | Material type/color/elevation mapping |
| Navigation | Same destinations and analytics semantics | Stack, tab/sidebar, edge-swipe Back | System/predictive Back, nav bar/rail/drawer |
| Controls | Same domain meaning and states | UIKit/iOS-native switches, pickers, SF Symbols | Material controls, dialogs, sheets, symbols |
| Accessibility outcomes | VO/TalkBack labels, scaling, keyboard traversal | VoiceOver traits/actions, Dynamic Type | TalkBack roles/state descriptions, font scale |
| Theming | Semantic token roles | System colors/materials, high contrast | Material ColorScheme/Dynamic Color fallback |
| Motion | Completion feedback and state clarity | Reduce Motion cross-fade/reduced travel | Remove animations immediate/cross-fade path |
| Adaptivity | Compact vs expanded information architecture | iPad size classes/Split View | Window size classes, multi-window/foldables |

## 6. Verified versus unverified claims

**Verified only from supplied static description, assuming it is accurate:**

- Forced `width: 390` centered tablet screen.
- Custom top bar and JavaScript back.
- Empty `BackHandler` consuming Android Back.
- `40x40` pressables.
- Fixed `fontSize: 14` with font scaling disabled.
- Raw `#777777` and `#FFFFFF`.
- Same Cupertino-shaped switch and web icon set on both platforms.
- Bottom tab bar unchanged across phone/tablet platforms.
- `500ms` overshooting spring without Reduced Motion/Remove animations alternative.

**Unverified:**

- Actual source paths, implementation details, navigation library, token files, or build configuration.
- Real iOS/iPadOS or Android rendering.
- VoiceOver, TalkBack, accessibility tree, focus order, labels, traits, state announcements.
- Dynamic Type/font-scale behavior, keyboard traversal, switch access, D-pad traversal.
- Contrast across all states/themes.
- Rotation, iPad Split View, Android multi-window, foldable posture, IME/insets.
- Gesture feel, predictive Back preview, haptics, frame rate, interruption recovery, autosave/draft persistence.
- Simulator, emulator, or real-device behavior.

## 7. Minimal validation plan

**Source/static validation**

1. Inspect `PRODUCT.md`, `DESIGN.md`, theme/token files, navigation setup, screen layout, shared components, icons, switches, pressables, typography, and motion utilities.
2. Search for fixed dimensions, `allowFontScaling={false}`, raw hex colors, `BackHandler`, custom back buttons, hard-coded tab bars, and spring configs.
3. Check component state matrix: pressed, disabled, loading, error, success, focus/keyboard, accessibility labels/roles/values.

**Build/static gates**

1. Run project type check and lint.
2. iOS: run the project’s Xcode build/test command where available.
3. Android: run Gradle assemble/lint/test where available.

**Runtime validation required before release**

- **iOS Simulator: unverified locally.** Validate iPhone compact and iPad/Split View, Dynamic Type accessibility sizes, Reduce Motion, VoiceOver traversal, keyboard traversal, safe areas, rotation, and interrupted task recovery.
- **Android Emulator: unverified locally.** Validate phone, tablet, multi-window/foldable profile, font scale, Remove animations, TalkBack traversal, predictive Back, gesture navigation, IME/insets, and interrupted task recovery.
- **Real-device evidence: missing.** Required before final claims for gesture feel, haptics, predictive Back behavior on hardware, OEM Android differences, sustained performance, and one-handed ergonomics.

Rules/skill used: `design-craft`, frontend rule, and native adaptive references for iOS, Android, accessibility, design-system, motion, and validation.
