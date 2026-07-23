# Surface playbooks

Use this to avoid applying the wrong aesthetic to the wrong surface.

## Contents

- [Choose the surface mode](#choose-the-surface-mode)
- [Landing or brand page](#landing-or-brand-page)
- [Dashboard or admin app](#dashboard-or-admin-app)
- [Data visualization](#data-visualization)
- [Static or special report](#static-or-special-report)
- [Mobile flow](#mobile-flow)
- [Native phone or tablet app](#native-phone-or-tablet-app)
- [Forms and settings](#forms-and-settings)
- [Existing redesign](#existing-redesign)

## Choose the surface mode

Choose the mode from the current surface, not the product's category or brand:

- `Persuade`: the visitor must understand, decide, and act. Landing, campaign,
  pricing, and marketing surfaces belong here.
- `Operate`: the user must complete or monitor a task. Apps, dashboards,
  editors, admin, settings, and tools belong here.
- `Read`: the reader must understand structured information. Documentation,
  articles, guides, help, changelogs, and evidence-heavy reports belong here.
- `Experience`: the work itself is the destination. Portfolios, galleries, and
  showcases belong here; the interface should recede behind the artifact.

A developer tool's landing page is still `Persuade`; a fashion brand's guide
is still `Read`. Persist the choice only for the surface being designed.

## Landing or brand page

Primary job: persuade, explain, convert, or establish taste.

- Strong design read is mandatory.
- Visual hierarchy can be expressive.
- Use proof, contrast, rhythm, and memorable sections.
- Avoid generic hero + three cards + testimonial grid.
- Browser verification should cover desktop and mobile.

## Dashboard or admin app

Primary job: monitor, compare, operate, decide.

- Information architecture beats visual drama.
- Density should be purposeful, not sparse by default.
- Tables need scanning, sorting/filtering, empty/loading/error states.
- Charts need correct scales, labels, legends, tooltips, and responsive behavior.
- Motion should be quiet and state-oriented.

## Data visualization

Primary job: reveal a comparison, trend, composition, distribution, or anomaly.

- Pick the chart from the analytical question, not decoration.
- Keep tables as supporting evidence when charts can carry the story.
- Use accessible color ramps and direct labels where possible.
- Verify tooltip overflow, legend wrapping, and small viewport readability.

## Static or special report

Primary job: guide reading and decision-making.

- Use formal report grammar: clear cover, executive summary, section hierarchy,
  chart-first evidence, quiet navigation, footnote-sized caveats.
- For dashboard exports, business-review pages, and evidence-heavy report
  surfaces, also read `references/report-quality.md`.
- Avoid dashboard hero treatments, heavy rounded cards, decorative section
  banners, and giant tables as the main narrative.
- Every chart should answer a question; every table should justify its weight.
- Caveats belong in footnotes or hover/title when they are secondary.

## Mobile flow

Primary job: complete one task under interruption.

- Resolve whether the surface is mobile web, iOS, Android, or adaptive before
  choosing controls. `surface=mobile` alone is not a native signal.
- Mobile web touch targets should normally be at least 44 CSS px. Native iOS
  uses at least `44pt`; Android uses at least `48dp`.
- Prefer simple flows, visible progress, and forgiving errors.
- Avoid hover-only behavior.
- Test long labels and keyboard viewport behavior.
- For iOS, Android, or adaptive targets, read the matching platform reference
  and verify system navigation, insets, text scaling, screen reader order, and
  runtime gesture behavior.

## Native phone or tablet app

Primary job: complete the product task while preserving platform trust.

- Read `product-context.md` and resolve the platform before implementation.
- iOS reads `ios-quality.md`; Android reads `android-quality.md`; adaptive reads
  both plus `adaptive-quality.md`.
- Translate brand through system tint/color roles, typography, content, and
  motion rather than replacing navigation and controls.
- Restructure for tablets, split-screen, multi-window, orientation, or fold
  posture; never stretch a phone canvas.
- Treat simulator/emulator breadth and real-device truth as separate evidence.

## Forms and settings

Primary job: configure or submit accurately.

- Group related fields.
- Labels must be explicit.
- Help text should be local and concise.
- Error messages should say what happened and how to recover.
- Destructive actions need separation and confirmation.

## Existing redesign

Primary job: improve without breaking learned behavior.

- Audit before changing.
- Preserve brand assets, information architecture, and successful interactions
  unless the user asked for a full overhaul.
- Change one visual language at a time.
- Verify affected routes in browser.
