## 1) Evidence level, platform, design read

- **Evidence level:** static prompt-only review. No source tree, build, screenshot, accessibility tree, rotation, split-screen, foldable, simulator/emulator, or hardware evidence.
- **Resolved platform:** `adaptive` — one React Native product shipping to iOS and Android.
- **Design read:** Reading this as a field task completion surface for one-handed operators and tablet-review managers, with a calm operational-native feel, optimized for fast completion, verification, interruption recovery, and accessibility.

## 2) Platform-conformance verdict

- **iOS verdict: Block.** The screen behaves like a centered fixed phone canvas with custom navigation, fixed type, non-semantic colors, undersized targets, and cross-platform controls that bypass expected iOS/iPadOS behavior.
- **Android verdict: Block.** The empty `BackHandler` consuming Android Back, iOS-shaped controls, unchanged phone tab bar on tablets, fixed type, and missing Remove animations alternative are release-blocking for Android-native trust.

## 3) Prioritized findings

### F1 — Accessibility release requirements are directly violated
**Evidence:** fixed `fontSize: 14`, font scaling disabled, `40x40` primary pressables, no Reduced Motion/Remove animations path.  
**Impact:** Dynamic Type/font scaling, touch access, motor accessibility, and vestibular accessibility fail core release requirements.  
**Blocking because:** iOS needs scalable Dynamic Type and ~`44x44pt` targets; Android needs scalable `sp`/fontScale support and ~`48x48dp` targets.

### F2 — Navigation breaks native trust and recovery
**Evidence:** custom top bar and JS back button replace native navigation; Android Back is consumed by an empty `BackHandler`.  
**Impact:** iOS users lose stack behavior/edge-back expectations; Android users lose system and predictive Back; interrupted operators may be trapped or lose predictable recovery.  
**Blocking because:** Back behavior is platform-owned, not decorative chrome.

### F3 — Adaptive layout is phone-only
**Evidence:** one screen forced to `width: 390` and centered on tablets; bottom tab bar unchanged on phone, iPad, and Android tablet.  
**Impact:** managers in iPad Split View, Android multi-window, tablets, or foldables get wasted space and poor task-review ergonomics.  
**Blocking because:** `adaptive` means structural adaptation, not pixel-identical phone UI.

### F4 — Controls and iconography are accidental parity
**Evidence:** same Cupertino-shaped switch and one web icon set ship on both platforms.  
**Impact:** Android feels like an iOS/web port; iOS may miss SF Symbols/system traits; both risk incorrect semantics and accessibility roles.  
**Blocking because:** shared components must preserve platform contracts, not just shared visuals.

### F5 — Theming and motion ignore system settings
**Evidence:** raw `#777777` and `#FFFFFF` used in both appearances; 500ms overshooting spring has no reduced-motion alternative.  
**Impact:** contrast/dark-mode/high-contrast parity is unproven and likely brittle; completion feedback may feel playful or vestibular rather than calm and operational.  
**Blocking because:** `DESIGN.md` requires semantic color roles and allows native materials/motion.

## 4) Concrete design moves

1. **Replace the fixed `390` canvas with adaptive size classes.**  
   Phone: single task flow. Tablet/split-screen: two-pane task + verification/review, or list/detail where appropriate.

2. **Restore native navigation ownership.**  
   iOS: React Navigation/native stack with iOS back affordance and edge gesture.  
   Android: no empty Back consumption; support system Back and predictive Back with explicit unsaved-progress handling.

3. **Rebuild the action system around platform target sizes.**  
   Minimum effective target: iOS `44x44pt`, Android `48x48dp`; add spacing/hitSlop only if semantics and visual affordance remain clear.

4. **Enable text scaling and use semantic text roles.**  
   iOS: Dynamic Type-style roles. Android: Material type roles / scalable `sp` equivalent. Verify 200%/accessibility sizes without clipping or unreachable actions.

5. **Split shared task logic from platform controls.**  
   Share task state, validation, autosave/progress recovery, labels, and analytics. Render native switches, pickers, dialogs, sheets, menus, icons, and navigation per platform.

6. **Move all colors to semantic tokens with platform appearance mapping.**  
   Replace raw `#777777`/`#FFFFFF` with roles such as `text.secondary`, `surface.primary`, `border.subtle`, `action.primary`; map to iOS system colors/materials and Android Material roles.

7. **Make completion motion calm and settings-aware.**  
   Default: shorter, non-bouncy confirmation transition.  
   iOS Reduce Motion / Android Remove animations: cross-fade or immediate state change with persistent completion status.

8. **Adapt top-level navigation by width and platform.**  
   Phone: bottom tabs only if they represent 3–5 top-level destinations.  
   iPad: sidebar/tab sidebar or split view.  
   Android tablet: navigation rail/drawer where appropriate; preserve content continuity in multi-window/fold postures.

## Intentional parity matrix

| Area | Shared | iOS adaptation | Android adaptation |
| --- | --- | --- | --- |
| Task flow | Same completion/review states, progress preservation | Native stack/sheets, iPad split structure | System Back/predictive Back, Material navigation |
| Content hierarchy | Same labels, task status, verification priority | Dynamic Type, SF Symbols where used | Material type, Material Symbols where used |
| Controls | Same domain meaning and validation | Native switch/picker/action sheets | Material switch/chips/dialogs/sheets |
| Theming | Semantic roles and light/dark intent | System colors/materials/tint | Material color roles/tonal elevation |
| Motion | Same causal feedback meaning | Reduce Motion alternative, restrained native transitions | Remove animations alternative, Material motion patterns |
| Accessibility | Equivalent outcomes and traversal goals | VoiceOver traits/actions/announcements | TalkBack roles/state descriptions/predictive Back expectations |
| Adaptive layout | Same task data and review model | iPhone compact, iPad size classes/Split View | Phone/tablet/fold/multi-window size classes |

## 5) Verified vs unverified claims

**Verified from supplied static evidence only:**
- `PRODUCT.md` platform is described as `adaptive`.
- One React Native screen is fixed to `width: 390`.
- Custom top bar/back button replace platform navigation.
- Android Back is consumed by an empty `BackHandler`.
- Primary actions are `40x40`.
- Text uses fixed `14` with scaling disabled.
- Raw `#777777`/`#FFFFFF` are used.
- Same Cupertino switch, web icons, bottom tabs, and 500ms overshooting completion spring ship cross-platform.
- No Reduced Motion/Remove animations alternative is described.

**Unverified:**
- Actual source implementation, inherited hitSlop, labels, roles, focus order, safe-area/inset handling, state persistence, offline/error recovery, dark/high-contrast rendering, orientation behavior, split-screen behavior, foldable behavior, runtime performance, screenshots, simulator/emulator behavior, and real-device gesture feel.

## 6) Minimal validation plan

**Source/static checks**
- Inspect React Native navigation setup, `BackHandler` usage, platform branches, font scaling props, color token usage, switch/icon implementations, tab adaptation, and completion animation settings.
- Add/check tests or static guards for no empty Back consumption, no disabled font scaling on release-critical text, and no raw color literals outside token definitions.

**Build checks**
- Run TypeScript/lint and platform builds if available.
- iOS: `xcodebuild` compile/test path.
- Android: Gradle assemble/test path.

**Runtime checks — required but not performed here**
- **Missing iOS Simulator evidence:** iPhone + iPad/Split View, VoiceOver, Dynamic Type accessibility sizes, Reduce Motion, external keyboard, rotation/interruption recovery.
- **Missing Android Emulator evidence:** phone + tablet/foldable or multi-window, TalkBack, 200% font scale, Remove animations, predictive Back, keyboard/D-pad, rotation/interruption recovery.
- **Missing real-device evidence:** iPhone/iPad and representative Android hardware for touch targets, system Back gestures, haptics if any, animation feel, OEM differences, and sustained field-use performance.
