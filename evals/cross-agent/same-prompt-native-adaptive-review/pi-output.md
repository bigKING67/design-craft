Now I have the full design-craft reference surface loaded. Let me deliver the critique.

---

# Design Craft Critique — Field Operations Task App (Adaptive)

**Mode:** `critique` (read-only, no edits)

**Design Read:** *Reading this as: mobile field-operations task app for field operators (primary) and shift managers (secondary), with a calm, operationally trustworthy vibe, optimized for one-handed task completion under interruption on a phone and task review in tablet split-screen.*

---

## 1. Evidence Level, Resolved Platform, and Authority

| Field | Value |
|---|---|
| **Evidence level** | L0 static — prompt and prose description only |
| **Evidence sources** | Explicit `PRODUCT.md` (platform: `adaptive`), explicit shared `DESIGN.md` (semantic color roles, allows platform-native navigation/controls/icons/materials/motion), plus 9 static implementation claims |
| **Resolved platform** | `adaptive` (React Native) |
| **Platform source** | `product_context` — explicit PRODUCT.md |
| **Platform confidence** | 0.85 — the static claims describe React Native patterns (BackHandler, `width: 390`, pressables), but no `package.json`, `tsconfig`, or build target was inspected |
| **Style authority** | Shared `DESIGN.md` with semantic color roles — explicitly permits platform-native divergence |
| **Style authority mode** | **Intentionally ignored.** The DESIGN.md explicitly allows platform-native controls, icons, materials, and motion, but the implementation forces identical pixels, a single web icon set, Cupertino controls on Android, and a custom JS navigation stack on both platforms |
| **Missing evidence** | No source tree, no iOS Simulator, no Android Emulator, no real device, no screenshots, no accessibility tree, no rotation, no split-screen, no foldable posture, no TalkBack/VoiceOver traversal, no Dynamic Type/font-scaling verification, no Reduced Motion verification |

---

## 2. Platform-Conformance Verdict

### iOS — **FAIL**

The implementation fails the native trust test from `ios-quality.md` on six independent criteria:

1. **Custom top bar replaces UINavigationController.** A fluent iPhone user expects the system navigation stack with large/inline titles, the left-edge swipe-back gesture, and the native back chevron. A JavaScript back button is a web-in-a-shell pattern.

2. **`40x40` pressables** violate the `44x44pt` minimum touch target. This is a hard requirement under iOS HIG, not a suggestion.

3. **Fixed `fontSize: 14` with font scaling disabled** directly breaks Dynamic Type. iOS quality requires text to scale through accessibility sizes without clipping or losing actions.

4. **Cupertino-shaped switch is the only valid control here** — it is correct on iOS. But the bottom tab bar should use the native `UITabBar` appearance, not a look-alike.

5. **`width: 390` forced on tablet** breaks iPad size-class adaptation. iPad and Split View must restructure navigation and content, not center a phone canvas.

6. **No Reduced Motion alternative** for the 500ms spring with overshoot. iOS quality requires cross-fades or reduced travel when Reduce Motion is enabled.

**Verdict:** An iPhone user would recognize this as a web app wearing an iOS skin. Platform trust is broken.

### Android — **FAIL**

The implementation fails the native trust test from `android-quality.md` on seven independent criteria:

1. **Custom top bar + empty `BackHandler` consuming Android Back** replaces the Material top app bar and **traps system/predictive Back**. Android quality explicitly requires: *"Preserve system and predictive Back; do not trap or hijack the gesture."* An empty `BackHandler` that consumes the event is the canonical anti-pattern.

2. **`40x40` pressables** violate the `48x48dp` minimum touch target with `8dp` separation.

3. **Fixed `fontSize: 14` with font scaling disabled** breaks Android font scaling (`sp` units). Android quality requires: *"Verify system font scaling without clipped text or unreachable actions."*

4. **Cupertino-shaped switch on Android** is an iOS control shipped to the wrong platform. Android users expect Material switches, toggles, or checkboxes. This is an iOS-web port smell.

5. **One web icon set** replaces Material Symbols. Android quality requires: *"Prefer Material buttons, switches, chips, snackbars, bottom sheets, dialogs, pickers, navigation, and Material Symbols over Cupertino/web replacements."*

6. **Bottom tab bar unchanged on tablet** violates window size-class adaptation. Android quality requires: *"Compact widths use a navigation bar... medium/expanded widths use a navigation rail or drawer."*

7. **No Remove animations alternative** for the 500ms spring with overshoot. Android quality requires: *"Honor the Remove animations setting with a cross-fade or immediate state change."*

**Verdict:** An Android user would recognize this as an iOS app poorly ported. The Back gesture trap alone makes the app feel broken.

---

## 3. Prioritized Findings

### A. Accessibility — **CRITICAL (3 findings)**

| # | Finding | Platform | Severity | Reference |
|---|---|---|---|---|
| A1 | Font scaling disabled (`fontSize: 14`, `allowFontScaling: false`) | iOS + Android | **Block** — release requirement violated | `ios-quality.md` Dynamic Type, `android-quality.md` font scaling, `PRODUCT.md` accessibility |
| A2 | No Reduced Motion / Remove animations alternative for 500ms spring with overshoot | iOS + Android | **Block** — release requirement violated | `motion-quality.md` accessibility, `ios-quality.md` Reduce Motion, `android-quality.md` Remove animations |
| A3 | `40x40` pressables below both `44pt` and `48dp` minimums | iOS + Android | **Block** — touch target violation | `ios-quality.md` controls, `android-quality.md` controls |

### B. Navigation — **CRITICAL (3 findings)**

| # | Finding | Platform | Severity | Reference |
|---|---|---|---|---|
| B1 | Empty `BackHandler` consumes Android Back — system navigation trapped | Android | **Block** — platform contract broken | `android-quality.md`: "do not trap or hijack the gesture" |
| B2 | Custom JS top bar replaces UINavigationController navigation stack + left-edge back gesture | iOS | **Block** — platform contract broken | `ios-quality.md`: "Preserve the left-edge back gesture. Use a navigation stack for hierarchy" |
| B3 | Bottom tab bar unchanged on phone, iPad, and Android tablet | iOS + Android | **Block** — adaptivity failure | `adaptive-quality.md`: "Phone-to-tablet adaptation restructures navigation and content into appropriate columns, panes, rails, drawers, sidebars, or popovers" |

### C. Controls — **HIGH (2 findings)**

| # | Finding | Platform | Severity | Reference |
|---|---|---|---|---|
| C1 | Cupertino-shaped switch shipped on Android | Android | **High** — platform mismatch | `android-quality.md`: "Prefer Material buttons, switches, chips... over Cupertino/web replacements" |
| C2 | One web icon set on both platforms | iOS + Android | **High** — platform mismatch | `ios-quality.md`: SF Symbols; `android-quality.md`: Material Symbols |

### D. Theming — **HIGH (1 finding)**

| # | Finding | Platform | Severity | Reference |
|---|---|---|---|---|
| D1 | Raw `#777777` and `#FFFFFF` in both appearances, no semantic token mapping | iOS + Android | **High** — design-system contract violated | `design-system-contract.md`: "Components should consume semantic tokens, not branch on theme-specific literal colors" |

### E. Motion — **MEDIUM (1 finding)**

| # | Finding | Platform | Severity | Reference |
|---|---|---|---|---|
| E1 | 500ms spring with overshoot for task-complete transition | iOS + Android | **Medium** — out of spec | `motion-quality.md`: "Most UI animations should stay under 300ms. Keep bounce subtle (0.1-0.3)" |

### F. Adaptivity — **CRITICAL (1 finding)**

| # | Finding | Platform | Severity | Reference |
|---|---|---|---|---|
| F1 | `width: 390` forced and centered on tablets | iOS + Android | **Block** — adaptivity failure | `adaptive-quality.md`: "Drive layout from size/window classes... never stretch a phone canvas" |

---

## 4. Concrete Design Moves and Intentional Parity Matrix

### What stays shared

| Layer | Shared element | Rationale |
|---|---|---|
| Product | Task domain model, business rules, offline/error recovery logic | `adaptive-quality.md`: "Share product intent and domain model" |
| Semantic tokens | Color role names (`--color-text-primary`, `--color-surface`, etc.) | `design-system-contract.md`: "Shared semantic roles preserve platform-correct iOS/Android behavior rather than force identical pixels" |
| Content | Task hierarchy, field labels, error copy, empty-state messaging | `adaptive-quality.md`: "Share content hierarchy and core task flow" |
| Accessibility outcomes | Both platforms meet WCAG 2.1 AA contrast, screen reader parity, font scaling to 200% | `adaptive-quality.md`: "Share accessibility outcomes" |

### What must adapt per platform

| Layer | iOS | Android |
|---|---|---|
| **Navigation** | `UINavigationController` with stack push/pop, large/inline titles, left-edge swipe-back gesture | Material 3 top app bar with `NavigationBar` (phone) / `NavigationRail` (tablet), system predictive Back, no BackHandler trap |
| **Back behavior** | Left-edge gesture + native back chevron | System Back gesture + predictive Back animation; do not register an empty `BackHandler` |
| **Touch targets** | `44x44pt` minimum | `48x48dp` minimum with `8dp` separation |
| **Typography scaling** | Dynamic Type text styles (`body`, `callout`, `title1`, etc.) via `maximumFontSize` / `adjustsFontForContentSizeCategory` | Material type roles in `sp` units; no `allowFontScaling: false` |
| **Controls** | `UISwitch` (system toggle), `UISegmentedControl`, `UIPickerView`, context menus, SF Symbols | `MaterialSwitch`, `Chip`, Material pickers/dialogs, Material Symbols |
| **Icons** | SF Symbols (weight/scale variants, Dynamic Type-aware) | Material Symbols (weight/fill/optical-size variants) |
| **Color mapping** | Semantic token → iOS system colors + materials (`systemBackground`, `label`, `tintColor`) | Semantic token → Material 3 color roles (`surface`, `onSurface`, `primary`) |
| **Tablet structure** | `UISplitViewController` with sidebar + detail, size-class-driven | `ListDetailPaneScaffold` or navigation rail + detail, window-size-class-driven |
| **Task-complete motion** | `UIFeedbackGenerator` haptic + cross-fade or `UIView.animate` with Reduce Motion gate | Haptic confirmation + cross-fade or `AnimatedVisibility` with Remove animations gate |
| **Insets** | `safeAreaInsets` (notch, Dynamic Island, home indicator, keyboard) | `WindowInsets` (status bar, navigation bar, cutout, hinge, IME) |

### Motion parity table

| State | Shared intent | iOS behavior | Android behavior |
|---|---|---|---|
| Task complete (default) | Confirm completion with spatial clarity | `UINotificationFeedbackGenerator.success` + `UIView.animate` opacity/scale fade (≤ 300ms, no overshoot) | Haptic confirmation + `AnimatedVisibility` fade-through (≤ 300ms, no overshoot) |
| Task complete (Reduced Motion / Remove animations) | Confirm without positional movement | Cross-fade ≤ 200ms | Cross-fade or immediate state change |
| Navigation push | Spatial right→left push | Native `UINavigationController` push (interruptible, edge-swipe to pop) | Material shared-axis X transition or native fragment transition |
| Navigation pop / Back | Spatial left→right pop | Native swipe-back gesture (interactive, interruptible) | Predictive Back gesture (interactive, interruptible) |

---

## 5. Verified vs. Unverified Claims

| Claim | Status | Notes |
|---|---|---|
| `PRODUCT.md platform: adaptive` | **Accepted** (explicit prompt) | No PRODUCT.md file was inspected in the repo; accepted as the benchmark premise |
| `DESIGN.md` allows platform-native divergence | **Accepted** (explicit prompt) | No DESIGN.md file was inspected; accepted as the premise |
| `width: 390` forced on tablets | **Unverified** — no source, no runtime | Static claim only |
| Custom JS back button + empty BackHandler | **Unverified** — no source, no runtime | Static claim only |
| `40x40` pressables | **Unverified** — no source, no runtime | Static claim only |
| `fontSize: 14` with scaling disabled | **Unverified** — no source, no runtime | Static claim only |
| Raw `#777777` / `#FFFFFF` | **Unverified** — no source, no runtime | Static claim only |
| Cupertino switch on Android | **Unverified** — no source, no runtime | Static claim only |
| Web icon set on both platforms | **Unverified** — no source, no runtime | Static claim only |
| Bottom tab bar unchanged on tablet | **Unverified** — no source, no runtime | Static claim only |
| 500ms spring with overshoot, no Reduced Motion | **Unverified** — no source, no runtime | Static claim only |
| VoiceOver/TalkBack labels and traversal | **Not tested** | Release requirement in PRODUCT.md, zero evidence |
| Dynamic Type to 200% | **Not tested** | Release requirement, explicitly contradicted by fixed `fontSize` claim |
| External keyboard traversal | **Not tested** | Release requirement, zero evidence |
| Orientation, split-screen, multi-window | **Not tested** | iPad Split View and Android multi-window untested |
| Foldable posture | **Not tested** | Not tested |
| Offline/error/interruption recovery | **Not tested** | Purpose states "without losing progress when interrupted" — untested |

---

## 6. Minimal Source/Build/Runtime Validation Plan

### Source scan (can run now, no toolchain)

```bash
# Platform inference and conservative native findings
python3 scripts/design_craft_platform_scan.py --target <repo> --platform adaptive --json

# Static UI smell signals
python3 scripts/design_craft_css_smell_scan.py --target <repo>
python3 scripts/design_craft_token_audit.py --target <repo>
python3 scripts/design_craft_focus_audit.py --target <repo>

# Normalized static review packet
python3 scripts/design_craft_static_review.py --target <repo> --json
```

### iOS build scan (requires Xcode toolchain)

```bash
# Verify the React Native iOS target compiles
xcodebuild -workspace ios/<Project>.xcworkspace -scheme <Scheme> \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro' \
  build 2>&1 | tail -30

# Check Dynamic Type text styles in source
grep -rn "fontSize\|allowFontScaling\|adjustsFontForContentSizeCategory" \
  --include="*.tsx" --include="*.ts" --include="*.swift"

# Check minimum touch targets
grep -rn "minWidth\|minHeight\|hitSlop\|44\|48" \
  --include="*.tsx" --include="*.ts"
```

### Android build scan (requires Android SDK/NDK)

```bash
# Verify the React Native Android target compiles
cd android && ./gradlew assembleDebug 2>&1 | tail -30

# Check for BackHandler trapping
grep -rn "BackHandler\|onBackPress\|addEventListener.*hardwareBackPress" \
  --include="*.tsx" --include="*.ts" --include="*.kt" --include="*.java"

# Check font scaling
grep -rn "allowFontScaling\|fontScale\|sp\|textScaleFactor" \
  --include="*.tsx" --include="*.ts"
```

### Runtime validation — explicitly missing

| Evidence | Status | Tool needed |
|---|---|---|
| **iOS Simulator (iPhone)** | ❌ Unverified locally | `simctl boot`, run on device, test: back gesture, Dynamic Type, Reduce Motion, VoiceOver, rotation |
| **iOS Simulator (iPad, Split View)** | ❌ Unverified locally | `simctl`, test: size-class adaptation, sidebar/detail, multi-window |
| **Android Emulator (phone)** | ❌ Unverified locally | `adb` + Emulator, test: Back gesture (predictive), font scaling, Remove animations, TalkBack, rotation |
| **Android Emulator (tablet, multi-window)** | ❌ Unverified locally | `adb` + Emulator with tablet AVD, test: navigation rail, multi-window resize |
| **Real iPhone hardware** | ❌ Unverified locally | Required for: gesture feel, haptics, notch/Dynamic Island behavior, thermal/battery |
| **Real Android hardware** | ❌ Unverified locally | Required for: OEM Back gesture differences, haptics, cutout/hinge behavior, thermal/battery |
| **Accessibility tree (VoiceOver)** | ❌ Unverified | `Accessibility Inspector` (macOS) or Simulator VoiceOver |
| **Accessibility tree (TalkBack)** | ❌ Unverified | Emulator TalkBack + `adb shell uiautomator dump` |
| **Contrast verification** | ❌ Unverified | Accessibility Inspector or `adb shell` contrast tool against raw `#777777` on `#FFFFFF` |
| **Font scaling to 200%** | ❌ Unverified | Simulator Dynamic Type largest + Emulator font scale max |

### If neither Simulator nor Emulator is available locally

Run the static checks above and report:

- **iOS Simulator: unverified locally**
- **Android Emulator: unverified locally**
- **iOS runtime verdict: deferred** — all platform-conformance claims are based on static evidence only
- **Android runtime verdict: deferred** — all platform-conformance claims are based on static evidence only

---

## Summary

This implementation is an **undifferentiated React Native port** that ignores the `DESIGN.md` explicit permission for platform-native divergence. It ships a phone canvas (`width: 390`) to tablets, replaces both platform navigation stacks with a custom JavaScript top bar, traps Android Back, ships iOS controls to Android, disables font scaling, uses sub-minimum touch targets, and has no Reduced Motion alternative — all against the `PRODUCT.md` accessibility requirements and both platform quality contracts.

The single highest-leverage fix is **restoring platform-native navigation**: remove the custom top bar and empty `BackHandler`, use React Navigation's native stack on iOS and a Material top app bar on Android, and let the system handle Back. Everything else — touch targets, controls, icons, typography, tablet adaptation, and motion — flows from that decision.
