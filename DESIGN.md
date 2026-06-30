# Project Design Authority

This file is the style authority for the `design-craft` repository itself. It
exists so local route smoke tests have a concrete `DESIGN.md` baseline. It does
not override the `DESIGN.md`, scoped `AGENTS.md`, runtime behavior, or product
rules of any target project that uses the skill.

## Typography System

- Voice: precise, tool-like, and evidence-first. Prefer short operational
  headings over marketing language.
- Default copy hierarchy: title, one-line purpose, then command or evidence
  blocks. Avoid decorative prose inside maintenance docs.
- Code, command names, paths, schema names, and logs stay monospace and exact.
- Keep line length readable in Markdown. Dense command references should use
  fenced code blocks rather than inline wrapping.

## Color Palette

- The repository does not ship a product UI. Documentation examples should stay
  neutral and avoid inventing a branded visual system.
- When this repo needs UI examples, use the bundled Geist seed as the comparison
  baseline: quiet neutrals, restrained blue accents, strong contrast, and clear
  state colors.
- Do not introduce ornamental gradients, fake glassmorphism, or unrelated
  accent palettes into docs, screenshots, or generated examples.

## Motion Language

- Motion is documentation-only unless a real interactive surface is added.
- Any future demo UI should use motion only to explain state, sequence, or
  spatial origin. Avoid looping decorative animation.
- Default timing bands follow `skills/design-craft/references/motion-quality.md`:
  instant or near-instant for hot paths, short transform/opacity transitions for
  popovers, and reduced-motion support for all non-essential movement.

## Component Grammar

- Treat `skills/design-craft/` as the installable product; keep it lean and
  reference-driven.
- Treat `scripts/` as deterministic CLI helpers with explicit inputs and
  observable output. Prefer wrappers over hidden side effects.
- Treat `evals/` as evidence, not decoration. Evidence files must state what ran,
  what did not run, and which claims remain unverified.
- Treat `upstreams/` as pristine provenance. Do not edit upstream submodules to
  patch local workflow behavior.
- Any future visual page or docs UI should prioritize readable command cards,
  compact evidence tables, and explicit validation status over generic marketing
  sections.

## Route Smoke Policy

- `DESIGN.md` makes repository-root route smoke valid for maintenance checks.
- Route planner output is still only a plan. Do not claim a skill, subagent,
  browser validation, or screenshot artifact was actually used unless that step
  ran and produced evidence.
- For real client/product work, the target project's own design authority
  outranks this repository-level authority.
