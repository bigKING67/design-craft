## 1. Evidence level, platform, design read

- **Evidence level:** L0 static/contextual critique from prompt + static implementation description only.
- **Resolved platform:** `adaptive` from provided `PRODUCT.md` platform statement; confidence high for intent, not verified from repo targets.
- **Design read:** Reading this as a field task completion surface for one-handed operators and tablet/multi-window managers, with a calm trustworthy native operations feel, optimized for fast completion, verification, and interruption recovery.
- **Mode:** read-only design-craft native adaptive critique. No files edited; no source tree, build, simulator, emulator, screenshot, accessibility tree, or hardware validation was performed.

## 2. Platform-conformance verdict

- **iOS / iPadOS: Fail for release.** The forced 390pt phone canvas, custom top bar/back button, disabled Dynamic Type, sub-44pt actions, non-semantic colors, shared web icons, non-native controls, unchanged phone tab bar on iPad, and unreduced overshooting spring all conflict with iOS trust, accessibility, and iPad adaptation.
- **Android: Fail for release.** Consuming system Back is a blocker, especially for predictive Back. The shared Cupertino switch/web icons, 40x40 actions below 48dp, fixed non-scaling text, raw colors, unchanged bottom tabs on tablet, and no Remove Animations path violate Android native, accessibility, and adaptive expectations.

## 3. Prioritized blocking findings

1. **Navigation breaks platform trust and recovery.**  
   Evidence: custom top bar/JS back replaces iOS navigation stack and Android system/predictive Back; empty `BackHandler` consumes Android Back.  
   Impact: users lose learned escape paths, managers/operators may be trapped or confused during interruption recovery.

2. **Accessibility release requirements are directly contradicted.**  
   Evidence: `40x40` primary pressables, fixed `fontSize: 14`, font scaling disabled.  
   Impact: misses iOS 44pt and Android 48dp target floors, blocks Dynamic Type/font scaling, and risks unreachable actions for VoiceOver/TalkBack and motor accessibility.

3. **Adaptive layout is phone-only, not tablet/multi-window capable.**  
   Evidence: screen forced to `width: 390` and centered on tablets; bottom tab bar unchanged across phone, iPad, and Android tablet.  
   Impact: manager review in split-screen/multi-window gets wasted space, weak hierarchy, and non-native navigation density.

4. **Design system and platform theming are bypassed.**  
   Evidence: raw `#777777`/`#FFFFFF` in both appearances; same Cupertino switch and web icon set on both platforms.  
   Impact: weak dark/high-contrast parity, poor semantic state expression, and obvious ported UI rather than operationally native UI.

5. **Motion is not accessible or operationally calm.**  
   Evidence: task-complete transition is a 500ms overshooting spring with no Reduced Motion/Remove Animations alternative.  
   Impact: completion feedback may feel playful/unstable, can trigger vestibular discomfort, and violates required motion settings.

## 4. Concrete design moves

1. **Remove fixed `390` width.** Use window/size classes: compact phone = single task flow; iPad/tablet/multi-window = split list/detail or review pane; foldables = hinge-aware panes.
2. **Restore native navigation contracts.** iOS: real stack/sheet behavior with edge-swipe back. Android: system Back + predictive Back integration; never consume Back with an empty handler.
3. **Adapt navigation by size/platform.** Phones may use bottom tabs for top-level destinations; iPad can use sidebar/tab sidebar; Android medium/expanded can use navigation rail or drawer.
4. **Use native controls and iconography.** iOS: native switches, SF Symbols, system materials. Android: Material switches, Material Symbols, tonal elevation/Dynamic Color where appropriate.
5. **Fix touch and keyboard access.** Primary actions at least 44pt iOS / 48dp Android, visible focus, logical external keyboard traversal, and accessible labels/traits/state descriptions.
6. **Re-enable text scaling.** Use platform text roles and scalable units; test large accessibility sizes without clipped task text or hidden actions.
7. **Replace raw colors with semantic roles.** Map `DESIGN.md` shared roles to platform system colors/material color roles with light/dark/high-contrast parity.
8. **Make completion feedback calm and setting-aware.** Use platform-native completion transition; Reduce Motion/Remove Animations should cross-fade or update immediately while preserving clear success state and saved progress.

## 5. Intentional parity matrix

| Area | Shared across platforms | Must adapt per platform |
|---|---|---|
| Product flow | Task complete, verify, resume after interruption | Navigation presentation and system back behavior |
| Content hierarchy | Task title, status, required fields, evidence, completion state | iOS large/inline titles vs Android top app bars |
| State model | Draft/saving/saved/error/completed semantics | Announcements, snackbars/toasts, haptics timing |
| Accessibility outcome | Screen reader usable, scalable text, keyboard traversal, reduced motion | VoiceOver traits/actions vs TalkBack roles/state descriptions |
| Tokens | Semantic roles: background, text, critical, success, disabled | System colors/material roles, dynamic color, materials/elevation |
| Controls | Same intent and labels | Native switch/button/picker/dialog/sheet implementations |
| Navigation destinations | Same information architecture | Bottom tabs vs sidebar/rail/drawer by size class |
| Motion intent | Calm continuity and completion confidence | iOS stack/sheet motion vs Android Material transitions; settings-specific alternatives |

## 6. Verified vs unverified claims

**Verified from provided static description only:**
- Fixed `width: 390`.
- Custom top bar/JS back and empty Android `BackHandler`.
- `40x40` primary pressables.
- Fixed `fontSize: 14` and disabled font scaling.
- Raw `#777777`/`#FFFFFF`.
- Shared Cupertino switch and web icon set.
- Same bottom tab bar across phone/tablet.
- 500ms overshooting spring without reduced-motion alternative.

**Unverified and not claimed:**
- Actual source structure, React Native navigation library, token files, or build settings.
- Real VoiceOver/TalkBack traversal, labels, announcements, or focus order.
- Actual contrast ratios in rendered light/dark/high-contrast appearances.
- Rotation, iPad Split View, Android multi-window, foldable posture, keyboard/IME insets.
- Runtime smoothness, frame rate, gesture feel, haptics, persistence, or interruption recovery.
- iOS Simulator, Android Emulator, or real-device behavior.

## 7. Minimal validation plan

1. **Source/static audit:** inspect `PRODUCT.md`, `DESIGN.md`, screen styles, navigation setup, `BackHandler`, pressable hit slop, text scaling props, color/token usage, control/icon imports, and motion settings branches.
2. **Build checks:** run project type-check/lint/tests; iOS compile via `xcodebuild`; Android compile/tests via Gradle.
3. **iOS runtime:** iPhone + iPad Simulator checks for Dynamic Type, Reduce Motion, VoiceOver, rotation, Split View, safe areas, keyboard traversal, and native back/edge gestures. **iOS Simulator: unverified locally.**
4. **Android runtime:** Emulator checks across phone/tablet/foldable or multi-window profiles, font scale, Remove Animations, TalkBack, predictive Back, insets, and hardware keyboard traversal. **Android Emulator: unverified locally.**
5. **Real devices before release:** representative iPhone/iPad and Android phone/tablet for gesture feel, haptics, OEM Back behavior, performance, interruption/resume, and one-handed ergonomics. **Real-device evidence: missing for both platforms.**
