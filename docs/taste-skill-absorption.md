# Leonxlnx/taste-skill absorption matrix

This document records the deliberate baseline-fusion boundary for
`https://github.com/Leonxlnx/taste-skill` at commit
`b17742737e796305d829b3ad39eda3add0d79060`.

## Contents

- [Inventory truth](#inventory-truth)
- [Status vocabulary](#status-vocabulary)
- [Entrypoint matrix](#entrypoint-matrix)
- [Auxiliary-file matrix](#auxiliary-file-matrix)
- [Rules deliberately not promoted](#rules-deliberately-not-promoted)
- [Current conclusion](#current-conclusion)

## Inventory truth

The reviewed upstream contains thirteen Skill entrypoints, one `llms.txt`, and
one Stitch-oriented `DESIGN.md`. It contains no reusable component library,
runtime package, test harness, or implementation script under `skills/`.

`design-craft` therefore absorbs durable judgment and workflow behavior. It
does not flatten every style preset, image-generation workflow, host-output
policy, or product-specific generator into the default baseline. Those remain
separate, explicitly selected Skills when their specialized surface is needed.

## Status vocabulary

- `absorbed`: the durable capability is represented in local instructions,
  references, scripts, templates, or validation.
- `partial`: a useful, generalizable subset is local; style- or host-specific
  behavior remains separate.
- `missing-high-value`: an important behavior is absent and must block an
  "absorption complete" claim.
- `intentionally-rejected`: promoting the rule into the baseline would reduce
  correctness, force a style/tool, or conflict with project authority.
- `provenance-only`: retained for history or compatibility, not active behavior.

## Entrypoint matrix

| Upstream entrypoint | Status | Local target or boundary | Decision |
| --- | --- | --- | --- |
| `taste-skill` | absorbed | `visual-judgment.md`, `foundational-visual-principles.md`, `product-ui-taste-review.md`, `design-move-library.md` | Brief inference, anti-slop judgment, hierarchy, product fit, responsive craft, and final preflight are baseline behavior. |
| `taste-skill-v1` | provenance-only | pristine upstream | The legacy v1 behavior is retained for traceability; the current fusion is the maintained baseline. |
| `redesign-skill` | absorbed | `product-ui-taste-review.md`, `design-move-library.md`, critique/polish passes | Scan, diagnose, preserve functionality, remove generic patterns, and apply concrete repair moves are local. |
| `minimalist-skill` | partial | `visual-judgment.md`, `design-system-contract.md` | Restraint, typography, low-noise surfaces, and meaningful elevation are useful; a fixed minimalist palette/font/icon prescription is not universal. |
| `brutalist-skill` | intentionally-rejected | separate style Skill | Industrial brutalism is a valid selected direction, not a safe default for every product surface. |
| `gpt-tasteskill` | partial | `visual-judgment.md`, motion references | Variance, typography width, composition, anti-repetition, and motion craft are useful. Simulated Python randomness, mandatory AIDA, GSAP, fixed fonts, and universal cinematic spacing are rejected. |
| `brandkit` | intentionally-rejected | separate `brandkit` Skill | Brand-board image generation is a specialized artifact workflow, not baseline UI implementation behavior. |
| `image-to-code-skill` | intentionally-rejected | separate `image-to-code` Skill | Image-first visual reconstruction is opt-in because ordinary product work should not be forced through generated reference images. |
| `imagegen-frontend-web` | intentionally-rejected | separate image-generation Skill | Section-by-section image generation is valuable only when the task explicitly needs visual references. |
| `imagegen-frontend-mobile` | intentionally-rejected | separate image-generation Skill | Mobile concept-image generation is not native implementation or general UI review. |
| `stitch-skill` | partial | `design-system-contract.md`, developer-product templates | Agent-readable `DESIGN.md`, semantic tokens, typography roles, and state contracts are local; Google Stitch-specific generation stays opt-in. |
| `soft-skill` | partial | `visual-judgment.md`, `product-ui-taste-review.md` | Premium specificity, rhythm, restrained surfaces, and anti-generic checks are local. Absolute font/icon/border bans and price/persona theater are rejected. |
| `output-skill` | intentionally-rejected | host delivery policy | Complete output is important, but overriding host truncation/context policy is not a design-engineering capability and must not live in this baseline. |

## Auxiliary-file matrix

| Upstream file | Status | Decision |
| --- | --- | --- |
| `skills/llms.txt` | provenance-only | Discovery metadata is not behavior. |
| `skills/stitch-skill/DESIGN.md` | partial | Its machine-readable design-system structure informed the local contract, while Stitch-specific style authority remains opt-in. |

## Rules deliberately not promoted

The baseline does not universally require or ban a named font, icon library,
layout archetype, color family, card shape, animation library, generated image,
or page-funnel formula. It also does not simulate tools that were not run.

Project `PRODUCT.md`, project `DESIGN.md`, real content, live runtime evidence,
accessibility, platform conventions, and measured performance always outrank a
generic aesthetic prescription. Style Skills can be selected alongside
`design-craft`; they do not silently redefine its default behavior.

## Current conclusion

`missing-high-value`: none for the reviewed snapshot.

The cumulative state is selective absorption: high-value design judgment and
redesign behavior are local, while specialized style, image-generation,
Stitch, brand-kit, and output-policy Skills remain deliberately independent.
The range after `06d6028b5c623016c59ce8536f578e5a1127b499` changes README
sponsorship and image assets only, so its latest-range status is
`provenance-only` rather than a statement that the upstream was never absorbed.
