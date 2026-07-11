Now I have all the design-craft references loaded. Let me compose the full critique.

---

# Design-Craft Critique — Field Operations Adaptive Task App

**Mode**: `critique` (read-only, no edits, no simulator/emulator/runtime claims).

---

## 1. Evidence Level, Resolved Platform, and Design Read

| Field | Value |
|---|---|
| **Evidence level** | `L0 static` — prose description only. No source tree, build output, screenshot, accessibility tree, rotation/split-screen/foldable, simulator, emulator, or hardware evidence. |
| **Resolved platform** | `adaptive` |
| **Platform source** | `product_context` (PRODUCT.md explicit) |
| **Confidence** | `0.9` — PRODUCT.md is explicit, but no source tree or build artifact confirms React Native or any native target. |
| **Design read** | _Reading this as: field operations task surface for operators completing tasks one-handed on a phone, and managers reviewing on tablet split-screen, with calm trustworthy operational tone, optimized for task-completion continuity across interruptions._ |
| **Style authority** | `DESIGN.md` — shared semantic color roles and content hierarchy; explicitly permits platform-native navigation, controls, icons, materials, and motion. |
| **Product context path** | PRODUCT.md (described in prompt; no file read in workspace) |
| **candidate_skills** | `design-craft`, `ios-quality`, `android-quality`, `adaptive-quality`, `motion-quality`, `interaction-physics`, `design-system-contract` |
| **selected_skills** | All of the above — all were read and applied. |

---

## 2. Platform-Conformance Verdicts

### iOS: **BLOCKED**

Fluent iPhone user trust would fail at five distinct touchpoints:

1. **No navigation stack / no left-edge swipe gesture** — replaced by a JavaScript top bar and custom back button. iOS users navigate via `UINavigationController` push/pop and the system left-edge interactive pop gesture. A custom bar + JS back button is a web pattern, not a native iOS pattern.

2. **Fixed `width: 390` centered on tablets** — no size-class adaptation. iPad Split View, slide-over, and full-screen rotation require `regular`/`compact` size-class-driven layout restructuring. A centered phone canvas on iPad is a web-in-WebView anti-pattern.

3. **`40×40pt` touch targets** — below `44×44pt` minimum. This is a hard HIG rule and VoiceOver hit-test boundary.

4. **`fontSize: 14` with font scaling disabled** — blocks Dynamic Type at every level, including accessibility sizes (up to 310% or ~53pt). This is a release-blocking accessibility violation.

5. **500ms spring with overshoot, no Reduce Motion path** — the task-complete transition must offer a cross-fade or reduced-travel alternative when Reduce Motion is enabled.

**iOS conformance: FAIL** — five blocking violations across navigation, adaptivity, touch targets, typography scaling, and motion accessibility.

### Android: **BLOCKED**

Fluent Android user trust would fail at six distinct touchpoints:

1. **Empty `BackHandler` consuming Android Back** — hijacks system/predictive Back navigation. Android users expect Back to pop the navigation stack or exit. Consuming it silently breaks the entire Back contract.

2. **Custom JS top bar instead of Top App Bar** — no Material Top App Bar, no predictive Back integration, no platform-consistent elevation/scrolling behavior.

3. **`40×40dp` touch targets** — below `48×48dp` minimum with at least `8dp` separation. TalkBack and D-pad navigation depend on this spacing.

4. **`fontSize: 14` with font scaling disabled** — blocks system font scaling at every level. Android font scale can reach 200% (or higher with some OEMs); fixed `sp`-less values are a release-blocking accessibility violation.

5. **Cupertino-shaped switch** — iOS control on Android. Android users expect a Material Switch. This is an immediate platform-trust failure.

6. **500ms spring with overshoot, no Remove animations path** — the system "Remove animations" setting requires a cross-fade or immediate state change.

**Android conformance: FAIL** — six blocking violations across Back navigation, app bar, touch targets, typography scaling, control style, and motion accessibility.

---

## 3. Prioritized Findings

### 🔴 BLOCKING — Accessibility

| # | Finding | iOS | Android | Principle at risk |
|---|---|---|---|---|
| A1 | `fontSize: 14` fixed, font scaling disabled | Blocks Dynamic Type (all sizes including accessibility) | Blocks system font scaling (all multipliers) | Flexibility, Platform trust |
| A2 | 500ms spring with overshoot, no reduced-motion alternative | Blocks Reduce Motion | Blocks Remove animations | Flexibility, Safety |
| A3 | `40×40` pressables below platform minimums | Below `44×44pt` min | Below `48×48dp` min | Familiarity, Platform trust |
| A4 | Custom JS top bar — VoiceOver/TalkBack labels, traits, and focus order unverified | High probability of broken rotor, heading navigation, and custom-action discovery | High probability of broken traversal, live-region, and action discovery | Familiarity, Accessibility |

### 🔴 BLOCKING — Navigation

| # | Finding | iOS | Android | Principle at risk |
|---|---|---|---|---|
| N1 | Custom JS top bar replaces navigation stack | No push/pop, no large/inline titles, no interactive pop gesture | No Top App Bar, no predictive Back, no elevation | Familiarity, Platform trust |
| N2 | Empty `BackHandler` consumes Android Back | N/A (iOS has no system Back button) | Breaks system/predictive Back contract entirely | Agency, Platform trust |
| N3 | Bottom tab bar unchanged on tablets | iPad expects sidebar or tab-bar adaptation per size class | Tablet expects Navigation Rail or drawer at expanded widths | Flexibility |

### 🔴 BLOCKING — Controls

| # | Finding | iOS | Android | Principle at risk |
|---|---|---|---|---|
| C1 | Cupertino switch on Android | N/A (correct on iOS) | Wrong control; should be Material Switch | Familiarity, Platform trust |
| C2 | Single web icon set on both platforms | Should use SF Symbols | Should use Material Symbols | Familiarity, Craft |
| C3 | `40×40` pressables (cross-referenced) | Below 44pt min | Below 48dp min | Familiarity |

### 🟡 HIGH — Theming

| # | Finding | Impact | Principle at risk |
|---|---|---|---|
| T1 | Raw `#777777` and `#FFFFFF` values bypass semantic token roles | DESIGN.md specifies shared semantic color roles; raw values break dark-mode parity, high-contrast, and platform color-system mapping | Craft, Design-system contract |
| T2 | Both appearances use same raw values | Light/dark theme parity impossible without semantic tokens | Craft |

### 🟡 HIGH — Motion

| # | Finding | Impact | Principle at risk |
|---|---|---|---|
| M1 | 500ms spring with overshoot exceeds reasonable UI duration | Most UI animations should stay under 300ms; 500ms on a high-frequency action (task completion) will feel slow | Craft, Simplicity |
| M2 | No Reduced Motion / Remove animations alternative | Blocks accessibility contract on both platforms | Flexibility, Safety |

### 🔴 BLOCKING — Adaptivity

| # | Finding | iOS | Android | Principle at risk |
|---|---|---|---|---|
| AD1 | `width: 390` centered on tablets | No size-class or Split View adaptation | No window-size-class or multi-window adaptation | Flexibility |
| AD2 | Bottom tab bar identical on phone/iPad/Android tablet | iPad needs structural adaptation | Android tablet needs Navigation Rail or drawer | Flexibility |
| AD3 | Same controls shipped on both platforms (switch, icons) | Cupertino switch OK; SF Symbols missing | Cupertino switch wrong; Material Symbols missing | Familiarity, Platform trust |

---

## 4. Design Moves and Intentional Parity Matrix

### Concrete Design Moves (in priority order)

**Move 1 — Restore native navigation per platform**
- **iOS**: Replace custom top bar with native `UINavigationController` stack. Use large title at root, inline title on detail. Restore left-edge interactive pop gesture. Remove JS back button.
- **Android**: Replace custom top bar with Material 3 `TopAppBar`. Remove empty `BackHandler`; let the system Back gesture and predictive Back work normally. Use `NavHost` / navigation component for stack management.
- **Shared concern**: Content hierarchy (titles, back-label semantics) stays shared; the container is platform-native.

**Move 2 — Drive layout from size classes, not fixed pixel width**
- Remove `width: 390` hard constraint.
- **Phone (compact width)**: single-column stack.
- **iPad Split View / Android multi-window**: use `HStack` or equivalent column/supplementary layout driven by horizontal size class.
- **Tablet full-screen**: restructure into primary/detail split or list/detail navigation.
- **Shared concern**: task content, field definitions, and data model remain identical.

**Move 3 — Adopt platform scaling primitives for typography**
- **iOS**: Use `DynamicType` text styles (`.body`, `.headline`, `.caption`, etc.) via system fonts. Never set `allowFontScaling: false` on production text.
- **Android**: Use `sp` units and Material type roles. Never fix font size in raw `dp` or disable scaling.
- **Shared concern**: content hierarchy (what is heading vs. body vs. label) stays shared; the scaling mechanism is platform-native.

**Move 4 — Restore minimum touch targets**
- **iOS**: minimum `44×44pt`.
- **Android**: minimum `48×48dp` with `8dp` separation.
- **Shared concern**: action priority, layout structure, and interaction semantics stay shared.

**Move 5 — Use platform-native controls and icon sets**
- **iOS**: SF Symbols for icons, native `UISwitch` (or `.switch` toggle style), native segmented controls, native context menus.
- **Android**: Material Symbols for icons, `MaterialSwitch`, Material chips, Material bottom sheets, Material dialogs.
- **Shared concern**: the *control purpose* (toggle, select, confirm) is shared; the *rendering* is platform-native.

**Move 6 — Fix motion contract**
- Reduce task-complete transition to ≤300ms. Drop overshoot entirely for this operational surface — a trust/calm tone calls for critically damped or near-critically-damped motion (`damping: 1.0`, `response: 0.3–0.4s`).
- Read `UIAccessibility.isReduceMotionEnabled` on iOS; gate spring transition behind `!isReduceMotionEnabled`. Fallback: cross-fade or instant state change.
- Read `Settings.Global.ANIMATOR_DURATION_SCALE` or `accessibilityManager` on Android; gate spring transition behind remove-animations check. Fallback: cross-fade.
- **Shared concern**: the *semantic feedback* (task completed) is shared; the *motion delivery* adapts to platform accessibility settings.

### Intentional Parity Matrix

| Concern | Shared | iOS-specific | Android-specific |
|---|---|---|---|
| **Domain model** | Task, status, fields, assignment, completion state | — | — |
| **Content hierarchy** | Title → status → fields → actions | — | — |
| **Semantic color roles** | `surface`, `text.primary`, `text.secondary`, `accent`, `success`, `danger` | Mapped to iOS system colors + materials | Mapped to Material color roles + tonal elevation |
| **Task completion semantics** | Same event, same analytics, same offline queue | — | — |
| **Navigation model** | — | `UINavigationController` push/pop, tab bar, sheets | `NavHost`, system Back, predictive Back, bottom nav |
| **Back behavior** | — | Left-edge swipe + back button in nav bar | System Back gesture + predictive Back |
| **Layout adaptation** | — | Size classes (`UITraitCollection`) | Window size classes (`WindowSizeClass`) |
| **Touch targets** | — | `≥44×44pt` | `≥48×48dp` + `8dp` gap |
| **Typography scaling** | — | Dynamic Type text styles | `sp` + Material type scale |
| **Controls** | — | Native switches, SF Symbols, context menus | Material switches, Material Symbols, chips |
| **Tab bar / nav rail** | — | `UITabBar` → sidebar on iPad | `NavigationBar` → `NavigationRail` on tablet |
| **Icons** | — | SF Symbols | Material Symbols |
| **Motion language** | Feedback semantics, timing constraint (≤300ms) | Reduce Motion → cross-fade; spring only when allowed | Remove animations → cross-fade; spring only when allowed |
| **Accessibility labels** | Shared label content, traits semantics | VoiceOver-specific rotor, actions | TalkBack-specific actions, live regions |
| **Offline/error recovery** | Shared retry queue, error model | Platform-specific error UI | Platform-specific error UI |

---

## 5. Verified versus Unverified Claims

### Verified (from static description)
- ✅ `width: 390` hard-coded and centered on tablets — stated explicitly.
- ✅ Custom JS top bar and JS back button replace native navigation — stated explicitly.
- ✅ Empty `BackHandler` consumes Android Back — stated explicitly.
- ✅ `40×40` pressables — stated explicitly; below both platform minimums.
- ✅ `fontSize: 14` with font scaling disabled — stated explicitly.
- ✅ Raw `#777777` and `#FFFFFF` values — stated explicitly.
- ✅ Cupertino-shaped switch on both platforms — stated explicitly.
- ✅ Single web icon set on both platforms — stated explicitly.
- ✅ Bottom tab bar unchanged on all devices — stated explicitly.
- ✅ 500ms spring with overshoot, no Reduced Motion alternative — stated explicitly.

### Unverified (no source/runtime evidence)
- ❌ Actual framework (React Native assumed, not confirmed by source tree or `package.json`).
- ❌ Whether SF Symbols or Material Symbols are available in the project's icon set (the description says "web icon set" — we can infer they are not, but we haven't confirmed).
- ❌ VoiceOver/TalkBack label content, traits, focus order, or custom actions — no accessibility tree inspection was performed.
- ❌ Whether keyboard/D-pad traversal works on iPad or Android with external keyboard — no runtime test.
- ❌ Dynamic Type / font scaling behavior at accessibility sizes (200%+) — no runtime test.
- ❌ Whether the 500ms spring visually clips, overflows, or causes layout thrashing — no runtime observation.
- ❌ Rotation behavior, Split View, multi-window, foldable posture — no runtime evidence.
- ❌ Offline/error/loading/empty state behavior — not described, not verified.
- ❌ Haptics implementation — not described, not verified.
- ❌ Actual color contrast ratios for `#777777` on any background — not measured.
- ❌ Build succeeds on either platform — no `xcodebuild` or Gradle output.
- ❌ Whether the app is actually React Native, SwiftUI, Compose, Flutter, or a WebView — no source tree available.

---

## 6. Minimal Source/Build/Runtime Validation Plan

### Phase 1 — Source Tree Audit (can be done now with access)

| Check | Tool | Expected |
|---|---|---|
| Confirm framework and native targets | Read `package.json`, `ios/`, `android/` directories | React Native / Expo / Flutter / KMP confirmed |
| Find `width: 390` constraint | `grep -r "width.*390" --include="*.tsx" --include="*.swift" --include="*.kt"` | Locate and document |
| Find font-scaling disable | `grep -r "allowFontScaling.*false\|fontScale\|adjustsFontForContentSizeCategory.*false"` | Locate and document |
| Find raw color values | `grep -r "#777777\|#FFFFFF" --include="*.tsx" --include="*.swift" --include="*.kt"` | Map all hard-coded colors |
| Find BackHandler | `grep -r "BackHandler\|onBackPress\|handleBack"` | Confirm empty consumer |
| Find motion configuration | `grep -r "spring\|Animated.spring\|useNativeDriver\|ReducedMotion\|UIAccessibility"` | Map all animation configs |
| Confirm DESIGN.md token definitions | Read DESIGN.md | Verify semantic token names exist |
| Confirm PRODUCT.md | Read PRODUCT.md | Confirm exact user/accessibility requirements |

### Phase 2 — Build Validation (requires toolchain)

| Check | iOS | Android |
|---|---|---|
| Type-check / compile | `npx react-native run-ios --simulator` or `xcodebuild` | `npx react-native run-android` or `./gradlew assembleDebug` |
| Lint | `npx eslint .` or project lint command | Same |
| Test suite | `npm test` or `npx jest` | Same |

### Phase 3 — Runtime Validation (reported as unverified until executed)

| Evidence | iOS required? | Android required? | Tool |
|---|---|---|---|
| iPhone (compact width) screenshot | ✅ Required | — | `xcrun simctl` + Simulator (e.g., iPhone 15, iOS 17+) |
| Android phone (compact width) screenshot | — | ✅ Required | `adb` + Emulator (e.g., Pixel 8, API 34+) |
| iPad (regular width, full-screen) screenshot | ✅ Required | — | Simulator |
| iPad Split View (1/3 + 2/3) screenshot | ✅ Required | — | Simulator + drag split |
| Android tablet (expanded width) screenshot | — | ✅ Required | Emulator (e.g., Pixel Tablet) |
| Android multi-window screenshot | — | ✅ Required | Emulator + multi-window toggle |
| Dynamic Type — accessibility Large (AX1) | ✅ Required | — | Simulator Settings → Accessibility → Display & Text Size → Larger Text |
| Dynamic Type — accessibility max (AX5) | ✅ Required | — | Simulator |
| Android font scaling 200% | — | ✅ Required | Emulator Settings → Display → Font size |
| Reduce Motion enabled | ✅ Required | — | Simulator Settings → Accessibility → Motion → Reduce Motion |
| Remove animations enabled | — | ✅ Required | Emulator Settings → Accessibility → Remove animations |
| VoiceOver audit | ✅ Required | — | Simulator + Accessibility Inspector |
| TalkBack audit | — | ✅ Required | Emulator + TalkBack |
| Keyboard traversal (iPad + external keyboard) | ✅ Required | — | Simulator + "Connect Hardware Keyboard" |
| Keyboard/D-pad (Android tablet) | — | ✅ Required | Emulator |
| Rotation (portrait ↔ landscape, phone + tablet) | ✅ Required | ✅ Required | Simulator + Emulator |
| Real-device gesture feel | Recommended | Recommended | Physical iPhone + Pixel or similar |
| Real-device haptics | Recommended | Recommended | Physical hardware |
| Foldable posture (if target includes foldables) | — | Recommended | Emulator with foldable AVD |

### Explicitly Missing Evidence (as of this critique)

- **`iOS Simulator: unverified locally`** — no Simulator or `xcrun simctl` session was run.
- **`Android Emulator: unverified locally`** — no Emulator or `adb` session was run.
- **Real-device validation: unverified** — no physical iPhone or Android device was tested.
- **Accessibility tree: unverified** — no VoiceOver/TalkBack output was captured.
- **Motion reduced-motion path: unverified** — no runtime observation with accessibility settings enabled.
- **Split View / multi-window: unverified** — no tablet adaptation evidence exists.

---

**Verdict**: This concept is a **web-shaped cross-platform shell masquerading as native**, not an adaptive product. The eight blocking findings collectively violate the platform trust test on both iOS and Android. The shared semantic contract (DESIGN.md) is correct in intent but is undermined by raw color values, disabled platform scaling, and a Cupertino control on Android. The parity matrix above provides the concrete path from "one stretched phone layout" to "one product family with platform-correct experiences."
