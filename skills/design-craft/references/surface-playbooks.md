# Surface playbooks

Use this to avoid applying the wrong aesthetic to the wrong surface.

## Contents

- [Choose the surface mode](#choose-the-surface-mode)
- [Landing or brand page](#landing-or-brand-page)
- [Dashboard or admin app](#dashboard-or-admin-app)
- [Persistent agent workspace](#persistent-agent-workspace)
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

## Persistent agent workspace

Primary job: delegate work, understand its progress, and retain control.

An AI marketing page or ordinary chat input alone does not trigger this
playbook.

Use for product surfaces where delegated work outlives a single response,
users supervise computer actions, or routines run later. Apply only supported
capabilities; this reference does not require adding agents, scheduling,
computer control, or a new execution architecture.

### Start from the user's responsibility

Identify what users return to manage: a project, task, workspace, conversation,
or durable agent role. Preserve established product authority and navigation
unless the task authorizes a change supported by user needs. A bot roster is
useful only when durable roles are the user's organizing concept; it does not
replace the product's session or workspace source of truth.

Reuse [product-design-principles.md](product-design-principles.md) for agency
and feedback, and [motion-quality.md](motion-quality.md) for motion behavior.
Apply the following decisions to the affected flow, not every product screen.

### Truthful progress

- Map user-facing status to actual execution events. Distinguish active work,
  waiting for input, waiting for authorization, a blocking condition, failure,
  cancellation, and completion where those states exist. Use product-native
  names; a new backend state enum is not required.
- A spinner is not evidence of activity. If observation is disconnected or
  stale, communicate that uncertainty rather than declaring the task running,
  failed, or complete without evidence. Separate the last observed action from
  the current connection state.
- Show a compact status and the next action needed from the user, if any.
  Offer current-action detail and expandable execution records when useful.
  Report observed actions and outcomes, not fabricated internal reasoning or
  invented percentage progress.
- Make essential detail reachable by keyboard and touch, not only hover.
  Motion may reinforce a state but cannot be its only indicator; reduced
  motion must preserve the same information.

### Observe, take control, return control

- When computer control exists, distinguish a status summary, an inspection
  preview, and interactive control as needed. Opening a preview must not
  silently transfer ownership or grant execution permission.
- Identify the affected environment and current controller. Make takeover and
  return explicit, and reflect acknowledged runtime transitions. Do not show
  control as transferred merely because the user clicked a button; pending,
  rejected, and interrupted transfers need honest feedback.
- Prevent the interface from implying simultaneous independent control when
  the runtime cannot support it. If ownership enforcement is missing, report
  that implementation gap; a visual label cannot prove safe handoff.
- Keep task scope and existing authorization boundaries visible where users
  decide. Returning control does not grant permission for a new operation.

### Results that fit the task

- Choose prose, a table, a review card, a visualization, or a document from the
  user's next decision. Avoid converting every response into a card.
- Separate a proposed action or draft from approval, execution, and confirmed
  outcome. A successful tool invocation alone does not prove the user's goal
  succeeded; show partial results and failures where they affect the decision.
- Let users reopen durable outputs and connect them to their producing task
  or run. Avoid making a long transcript the only way to find a deliverable.
- Preserve action context across retries: show which attempt a result belongs
  to and avoid presenting an earlier failure as the current result. Retrying
  must respect existing authorization and duplicate-effect constraints.

### Recurring work, when supported

Expose responsibility, schedule or event trigger, relevant timezone, next
scheduled run when applicable, latest result, pause state, and exceptions that
need attention. Distinguish pausing future runs from stopping a current run.
Do not infer shared memory, tool permissions, or autonomous coordination from
the presence of several agent identities.

### Acceptance in the affected product

Choose checks for the changed capabilities; use the existing
[validation-contract.md](validation-contract.md) evidence levels. For example:

- An authorization wait stops looking like active execution and exposes the
  relevant decision; a disconnected observer does not falsely mark completion.
- A control transfer shows its pending and acknowledged states; returning
  control restores the supported workflow without implying broader permission.
- A user can distinguish a draft from an executed result and reopen the output
  after leaving the conversation; a retry retains attempt-specific outcomes.
- Essential status is understandable with reduced motion and accessible without
  hover; a paused routine clearly explains what happens to an in-flight run.

Source review or a mockup can establish intended behavior, not prove live
execution, ownership enforcement, or usability. Mark unobserved behavior as
unverified rather than treating a checklist as runtime evidence.

### Design case source and limits

Informed by xAI's [Designing Grok Bot for a world of persistent agents](https://x.ai/news/designing-grok-bot)
(September 3, 2026; reviewed September 5, 2026), particularly its treatment of
persistent responsibility, layered supervision, and task-shaped information.
The operational checks above are Design Craft's own application of those
ideas. The article is a vendor design account, not independent usability or
runtime validation. It supplies no authority to copy brand assets, prescribe
bot counts or avatar styles, or replace local architecture and permissions.

## Data visualization

Primary job: reveal a comparison, trend, composition, distribution, or anomaly.

- Keep the requested deliverable honest: a chart request stays a chart request;
  analysis alone does not imply a complete report. Use the report mode only
  when the user asks for a structured narrative deliverable.
- Pick the chart from the analytical question and data shape, not decoration,
  a gallery category, or the chart library's most convenient example.
- Count charts by independent conclusions, not available columns or template
  slots. Remove repeated views that make the same point.
- Prefer the simplest familiar encoding that preserves magnitude, order, and
  uncertainty. For ambiguous or high-consequence choices, compare two or three
  candidates on encoding truth, label density, reading time, and interaction
  need; do not force this ceremony for an obvious simple choice.
- Preserve project `DESIGN.md`, existing component/library choices, and runtime
  constraints as authority over external chart galleries.
- Keep tables as supporting evidence when charts can carry the story.
- Use accessible color ramps and direct labels where possible; color must not
  be the only cue for series, state, direction, or selection.
- Verify tooltip overflow, legend wrapping, and small viewport readability.
- For report composition and encoding-integrity checks, also read
  `references/report-quality.md`.

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
