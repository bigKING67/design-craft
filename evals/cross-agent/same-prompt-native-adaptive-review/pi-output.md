## 1. Evidence level, platform, design read

- **Evidence level:** `L0 static/prose` with supplied product context. No source tree, screenshot, accessibility tree, build, simulator/emulator, or device run was performed.
- **Resolved platform:** `adaptive` — one product family shipping to **iOS and Android**, including phone and tablet/multi-window use.
- **Design read:** Reading this as a field-operations task screen for one-handed operators and tablet-review managers, with a calm trustworthy native feel, optimized for fast completion, verification, interruption recovery, and accessibility.

## 2. Platform-conformance verdict

- **iOS verdict:** **Fail / release-blocking from static evidence.** The concept overrides iOS navigation behavior, blocks Dynamic Type, undersizes targets, uses non-semantic colors, ignores iPad adaptation, and lacks Reduce Motion support.
- **Android verdict:** **Fail / release-blocking from static evidence.** The concept consumes system Back/predictive Back, ports Cupertino/web controls, blocks font scaling, undersizes targets, keeps phone tabs on tablets, and lacks Remove Animations support.

## 3. Prioritized findings

| ID | Priority | Finding | Static proof | Runtime unknown | Required repair |
|---|---:|---|---|---|---|
| F1 | P0 | Adaptive layout is a centered phone canvas, not an adaptive product. | Forced `width: 390`; unchanged bottom tabs on phone/iPad/Android tablet. | Split-screen, rotation, foldable, keyboard/IME behavior unverified. | Use window size classes/posture/input mode; phone single-column, tablet split/master-detail or review panes; adapt tab bar to sidebar/rail where native. |
| F2 | P0 | Navigation breaks native trust and interruption recovery. | Custom top bar/JS back replaces iOS stack and Android system Back; empty `BackHandler` consumes Android Back. | Actual progress persistence and gesture behavior unverified. | Restore native stack semantics, iOS edge-swipe Back, Android system/predictive Back; autosave or confirm only when destructive. |
| F3 | P0 | Release accessibility requirements are not met. | `40x40` pressables; fixed `fontSize:14`; font scaling disabled. | VoiceOver/TalkBack labels, focus order, keyboard traversal, clipping unknown. | Minimum `44pt` iOS / `48dp` Android targets; enable font scaling; use platform text roles; verify large accessibility sizes and keyboard traversal. |
| F4 | P1 | Theming and controls are accidental cross-platform sameness. | Raw `#777777` / `#FFFFFF`; same Cupertino switch and one web icon set on both platforms. | Contrast, dark mode, high contrast, native semantics unverified. | Map `DESIGN.md` semantic roles to iOS/system and Material color roles; use native/platform controls and icon families. |
| F5 | P1 | Motion conflicts with calm operations and accessibility settings. | 500ms overshooting spring for completion; no Reduced Motion/Remove Animations alternative. | Perceived smoothness and interruption behavior unverified. | Replace with restrained platform motion; provide cross-fade/immediate completion under Reduce Motion/Remove Animations. |

## 4. Concrete design moves

1. **Navigation:** use native-stack navigation on iOS and Android-aware navigation with predictive Back support; remove the Back-consuming no-op.
2. **Adaptive layout:** replace fixed `390` width with responsive/window-class layout: compact phone task flow, expanded tablet review/detail panes.
3. **Tablet navigation:** keep bottom tabs only where native for compact widths; use iPad sidebar/tab adaptation and Android navigation rail/drawer for expanded widths.
4. **Touch and type:** set effective targets to `44pt` iOS / `48dp` Android; enable Dynamic Type/font scaling and design for long scaled labels.
5. **Native controls/icons:** iOS switch, sheets, context actions, SF Symbols; Android Material switch/buttons/snackbars/bottom sheets/Material Symbols.
6. **Semantic theming:** replace raw colors with shared semantic roles mapped to platform color systems, including dark and high-contrast appearances.
7. **Motion accessibility:** use platform-appropriate completion feedback; remove overshoot for operational confirmation; honor Reduce Motion/Remove Animations.
8. **Interruption resilience:** make task progress durable, show “saved”/sync/error state, and preserve state across app switch, Back, rotation, and multi-window.

### Intentional parity matrix

| Area | Shared | iOS adaptation | Android adaptation |
|---|---|---|---|
| Task model | Same task states, validation, autosave, audit trail | Native iOS hierarchy | Native Android hierarchy |
| Content | Same hierarchy and terminology | Large/inline titles as appropriate | Material top app bar patterns |
| Navigation | Same destinations and recovery rules | Navigation stack, edge-swipe Back, iPad sidebar where apt | System/predictive Back, nav bar/rail/drawer by width |
| Controls | Same intent and state | UIKit/SF-style controls and SF Symbols | Material controls and Material Symbols |
| Theme | Shared semantic token names | System colors/materials/tint | Material color roles/tonal elevation/Dynamic Color if chosen |
| Motion | Same state meaning | iOS-native restrained transitions; Reduce Motion | Material motion; Remove Animations |
| Accessibility | Same outcomes and acceptance criteria | VoiceOver, Dynamic Type, Switch Control/keyboard | TalkBack, font scaling, keyboard/D-pad |

## 5. Verified versus unverified claims

**Verified from prompt/static description only**
- Product platform is `adaptive`.
- `DESIGN.md` allows platform-native navigation, controls, icons, materials, and motion.
- Implementation description includes fixed width, custom back behavior, small targets, disabled font scaling, raw colors, shared Cupertino/web controls, unchanged tab bar, and non-reduced overshooting motion.

**Unverified**
- Actual source files, component boundaries, token implementation, state persistence, builds, screenshots, runtime behavior, accessibility tree, focus order, contrast measurements, rotation, split-screen, foldable posture, performance, haptics, and real gesture feel.

## 6. Minimal validation plan

**Source/static**
- Inspect `PRODUCT.md`, `DESIGN.md`, React Native navigation setup, `BackHandler`, target sizing, `allowFontScaling`, color tokens, platform branches, `useWindowDimensions`/window-class logic, accessibility props, and reduced-motion handling.

**Build/checks**
- Run project lint/type/test scripts if present.
- iOS: run `xcodebuild` or project iOS build command.
- Android: run Gradle build/tests, e.g. `./gradlew assembleDebug test` if applicable.

**Runtime**
- **iOS Simulator: unverified locally** — test iPhone and iPad, portrait/landscape, Split View, Dynamic Type, VoiceOver, Reduce Motion, external keyboard.
- **Android Emulator: unverified locally** — test phone, tablet, foldable/multi-window, font scaling, TalkBack, Remove Animations, hardware keyboard/D-pad, predictive Back.
- **Real device evidence: missing** — required before final claims about gestures, haptics, OEM behavior, sustained performance, and one-handed field use.
