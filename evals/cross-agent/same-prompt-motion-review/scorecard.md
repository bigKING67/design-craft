# Scorecard

This file defines the grading rubric for future Codex, Cursor, Claude, Pi, or
generic-agent runs. It is not itself an agent output.

| Criterion | Weight | Pass evidence | Deduction trigger |
|---|---:|---|---|
| Style authority and product context | 15 | Checks product context, component role, and existing motion policy before tuning motion. | Applies flashy default animation without product need. |
| Reference selection | 15 | Routes to motion quality, motion vocabulary, design-system contract, and validation references as needed. | Ignores motion-specific guidance or loads unrelated references. |
| Anti-generic redesign | 15 | Questions whether motion should exist and avoids decorative generic redesign. | Treats more animation as automatically better. |
| Evidence level labeling | 15 | Labels whether timing/performance claims are static, browser-observed, or unverified. | Claims smoothness or runtime performance without browser evidence. |
| Verified/unverified boundary | 15 | Separates inspected CSS/behavior from unverified hover, focus, reduced-motion, and interruption states. | Claims interaction states without testing them. |
| Concrete design moves | 15 | Recommends transform/opacity, scoped transitions, reduced-motion path, and interruptible state transitions. | Gives vague "make it smoother" advice or suggests `transition-all`. |
| Scope control and unrelated changes | 10 | Keeps recommendations scoped to motion behavior and UI validation. | Suggests unrelated layout or data changes to solve animation issues. |
