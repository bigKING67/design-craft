## 1) Evidence level, platform, design read

- **Evidence level:** static contextual review only — product context + static implementation description. No source tree, build, screenshot, accessibility tree, simulator/emulator, split-screen, foldable, or hardware evidence.
- **Resolved platform:** `adaptive` from supplied `PRODUCT.md` context; high confidence.
- **Style authority:** `DESIGN.md` keeps shared semantic color roles/content hierarchy and explicitly allows platform-native navigation, controls, icons, materials, and motion.
- **Design read:** Reading this as a field task-completion app for one-handed operators and tablet managers, with a calm operational-native feel, optimized for fast completion, review, interruption recovery, and trust.

## 2) Platform-conformance verdict

- **iOS verdict:** **Not release-conformant.** The forced phone canvas, custom top bar/back behavior, disabled Dynamic Type, undersized targets, raw colors, non-semantic theming, shared web icons, and unchanged phone tab bar undermine iPhone/iPadOS native trust.
- **Android verdict:** **Not release-conformant, with a critical Back failure.** Consuming Android Back and replacing system/predictive Back is a platform blocker. Cupertino controls, web icons, fixed text, small targets, fixed phone width, and unchanged tablet navigation read as an iOS/web port rather than Material/adaptive Android.

## 3) Prioritized findings

1. **P0 — Navigation/back behavior breaks platform trust and task recovery.**  
   Evidence: custom top bar + JavaScript back button replace native stacks; empty `BackHandler` consumes Android Back.  
   Impact: Android users cannot rely on system/predictive Back; iOS users lose expected stack/edge-back behavior; interruptions and escape paths become risky.

2. **P0 — Accessibility release requirements are directly contradicted.**  
   Evidence: `40x40` pressables; fixed `fontSize: 14`; font scaling disabled.  
   Impact: below iOS `44x44pt` and Android `48x48dp` target floors; Dynamic Type/font scaling cannot work; one-handed touch, VoiceOver/TalkBack traversal, and external keyboard use are high-risk/unverified.

3. **P0 — Adaptivity is structurally absent.**  
   Evidence: screen forced to `width: 390` and centered on tablets; bottom tab bar unchanged across phone, iPad, and Android tablet.  
   Impact: manager tablet split-screen/multi-window use is treated as a boxed phone app, not an adaptive review surface.

4. **P0 — Native control/theming layer is accidental parity, not intentional parity.**  
   Evidence: raw `#777777`/`#FFFFFF`; same Cupertino-shaped switch and one web icon set on both platforms.  
   Impact: violates semantic roles and appearance parity; Android looks non-native, iOS lacks system-integrated color/material behavior; contrast/dark/high-contrast behavior is unverified.

5. **P1 release-blocking risk — Motion ignores accessibility and operational calm.**  
   Evidence: task-complete transition is a 500ms overshooting spring with no Reduced Motion/Remove animations alternative.  
   Impact: completion feedback may feel playful or vestibular; users requesting reduced motion get no compliant path.

## 4) Concrete design moves

1. **Restore platform navigation ownership.**  
   iOS: use native navigation stack, safe-area-aware title bars, and preserve left-edge back. Android: remove empty Back trap, wire system/predictive Back to route/task state, and confirm only for real unsaved-loss cases.

2. **Replace the fixed `390` shell with adaptive layout rules.**  
   Compact phone: one-handed task flow. iPad/tablet/multi-window: split task detail + verification/review pane, responsive to size class/window width, not device name.

3. **Use adaptive navigation components.**  
   Phone: bottom tabs only for true top-level destinations. iPad: sidebar/split view where appropriate. Android medium/expanded: navigation rail or drawer, not unchanged phone tabs.

4. **Create platform control adapters.**  
   Keep domain props shared, but render native switch/button/list/dialog/picker variants per platform; use SF Symbols on Apple and Material Symbols on Android where platform icons are expected.

5. **Fix touch and keyboard affordances.**  
   Minimum effective targets: iOS `44x44pt`, Android `48x48dp`; preserve visible focus, logical tab/D-pad order, and action proximity for one-handed completion.

6. **Restore scalable type.**  
   Use platform text roles and allow scaling; verify 200%/accessibility sizes with wrapping, no clipped labels, and primary actions still reachable.

7. **Move colors/materials to semantic tokens.**  
   Replace raw colors with shared role names mapped to iOS system colors/materials and Android Material color roles; validate light, dark, and high-contrast appearances.

8. **Make completion motion platform- and setting-aware.**  
   Default: short, non-overshooting, causal completion feedback. iOS Reduce Motion: cross-fade/reduced travel. Android Remove animations: immediate or fade-through state change.

## 5) Intentional parity matrix

| Area | Stays shared | Must adapt |
|---|---|---|
| Product flow | task steps, completion semantics, review status | navigation structure and back behavior |
| Content hierarchy | task title, required fields, verification priority | large titles/inline titles vs Material top app bars |
| Design tokens | semantic roles: surface, text, danger, success, focus | platform color/material/elevation mappings |
| Controls | domain API: toggle, confirm, complete, review | iOS controls/SF Symbols vs Material controls/icons |
| Accessibility | outcomes: screen reader, scaling, reduced motion, keyboard | VoiceOver traits/actions vs TalkBack roles/state descriptions |
| Adaptivity | same task state and progress continuity | iPad split/sidebar vs Android rail/drawer/fold posture |
| Motion | causal feedback and interruption safety | iOS Reduce Motion vs Android Remove animations patterns |
| Analytics/state | event names, draft persistence, recovery rules | platform lifecycle hooks and back-stack integration |

## 6) Verified vs unverified claims

**Verified from supplied static evidence:**
- Fixed `width: 390`.
- Custom top bar/JS back replacement.
- Empty Android `BackHandler` consuming Back.
- `40x40` pressables.
- Fixed `fontSize: 14` with scaling disabled.
- Raw `#777777`/`#FFFFFF`.
- Shared Cupertino switch and web icon set.
- Unchanged bottom tab bar across phone/tablet.
- 500ms overshooting spring with no reduced-motion alternative.

**Unverified and not claimed:**
- Actual rendered layout, safe-area handling, rotation, split-screen, foldable posture.
- VoiceOver/TalkBack labels, roles, order, announcements, or accessibility tree.
- Real contrast in all appearances.
- Keyboard/D-pad traversal.
- Build success, native module behavior, performance, gesture feel, haptics.
- iOS Simulator, Android Emulator, and real-device behavior.

## 7) Minimal validation plan

**Source/static:**
- Inspect `PRODUCT.md`, `DESIGN.md`, navigation setup, screen layout, token usage, text props, pressable sizing, icon/control adapters, motion settings, and task draft persistence.
- Search for fixed widths, `BackHandler`, `allowFontScaling={false}`, raw colors, hard-coded font sizes, and platform-agnostic icon/control imports.

**Build checks:**
- React Native type/lint/test commands from the actual repo scripts.
- iOS compile/test via `xcodebuild` if available.
- Android compile/test via Gradle if available.

**Runtime checks required before release:**
- **iOS Simulator: unverified locally** — test iPhone + iPad, portrait/landscape, Split View, Dynamic Type accessibility sizes, Reduce Motion, VoiceOver, external keyboard.
- **Android Emulator: unverified locally** — test phone + tablet/foldable profiles, multi-window, font scale, Remove animations, TalkBack, D-pad/keyboard, system/predictive Back.
- **Real devices: unverified** — required for final gesture feel, Back behavior, haptics, one-handed ergonomics, OEM differences, and sustained performance.
