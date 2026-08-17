# Visual reference workflow

Use this contract when the task is reference-only, includes a supplied visual
reference, or needs a generated reference before implementation. A reference
is evidence for a bounded design mechanism, not permission to copy a brand or
override project authority.

## Contents

- [Authority and source classes](#authority-and-source-classes)
- [Reference Card](#reference-card)
- [Review procedure](#review-procedure)
- [Reference Pack](#reference-pack)
- [Pattern promotion](#pattern-promotion)
- [Peekpaper adapter](#peekpaper-adapter)
- [Evidence and artifact boundary](#evidence-and-artifact-boundary)
- [Operational cadence](#operational-cadence)
- [Completion](#completion)

## Authority and source classes

Resolve conflicts in this order:

1. User constraints and the target's live runtime behavior.
2. Scoped `PRODUCT.md`, `DESIGN.md`, tokens, components, and platform rules.
3. An approved Reference Pack for the current task.
4. Reviewed Reference Cards.
5. Mutable discovery sources such as Peekpaper.

Discovery sources are not code upstreams, product requirements, design-system
authorities, engineering proof, or training corpora. Keep source observations
separate from target-project decisions.

## Reference Card

Use `design-craft.visual-reference-card.v1`. Every card records:

- canonical discovery and origin URLs plus observation date and source digest;
- source surface, product archetype, possible reference roles, and target fit;
- desktop, mobile, origin-runtime, interaction, accessibility, and performance
  evidence with explicit observed, partial, unverified, or unavailable states;
- observations, transferable mechanisms, do-not-copy boundaries, and cases
  where the reference is unsuitable;
- reference-only rights, lifecycle, and any later project validation.

A screenshot may establish composition, hierarchy, type scale, color
relationships, and visible desktop/mobile differences. It cannot establish
hover, focus, loading, errors, accessibility, performance, DOM semantics, or
interaction physics.

## Review procedure

1. Classify the target surface as `Persuade`, `Operate`, `Read`, or
   `Experience` from its primary job, not its brand category.
2. Observe desktop and mobile separately. Record only visible facts.
3. Name the mechanism without brand nouns. Prefer causal language such as
   "proof follows the promise before detailed features" over visual labels
   such as "large hero".
4. Record what must not transfer: trademarks, copy, proprietary imagery,
   distinctive illustration, exact geometry, and unsupported interactions.
5. Record target modes where the mechanism is useful or blocked.
6. Audit the origin only when a claim depends on runtime behavior. Preserve
   inaccessible states as unavailable or unverified.
7. Set a review-after date. A stale card cannot enter a ready Reference Pack.

Review outcomes may be `reviewed`, `exemplar_only`, `rejected`, or
`unavailable`. Do not force a positive outcome to satisfy a sample count.

## Reference Pack

Use `design-craft.visual-reference-pack.v1` immediately before target design or
implementation. A ready Pack contains one to three cards total, including any
counter-reference. An incomplete diagnostic Pack may contain zero when no
selection is usable. Each selected card has exactly one role:

- `structure`: information order, grouping, or composition;
- `responsive`: reprioritization across viewport or platform constraints;
- `tone`: typography, color relationship, density, or visual rhythm;
- `interaction`: origin-audited behavior only;
- `counter_reference`: a concrete example of what the target must reject.

For every positive reference, copy reviewed mechanisms into `adapt`, explicit
boundaries into `reject`, and incomplete evidence into `unverified`. A positive
reference blocked for the target surface makes the Pack incomplete. At least
one positive reference is required.

## Pattern promotion

One work is an exemplar, not a pattern. Promotion requires:

1. at least three reviewed cards with different origin URLs supporting the
   same mechanism;
2. at least one origin live audit for a runtime-dependent claim;
3. at least one target project or prototype validation;
4. a comparative evaluation using the same target input and acceptance rules.

Only then may a hypothesis move through `proposed`, `project_validated`,
`comparative_validated`, and `absorbed`. Golden contract fixtures prove schema
and blocking behavior; they do not satisfy target or comparative evidence.
One artifact may satisfy only one promotion rung for a given hypothesis:
`target_validation_refs` and `comparative_eval_refs` must be disjoint. A first
target result cannot be counted again as the later comparative evaluation;
promotion requires a distinct result with its own pre-registered comparison.

## Peekpaper adapter

Peekpaper is a mutable discovery source. Prefer its official issue JSON over
HTML scraping and cite the canonical post HTML page. The portable adapter:

- permits only explicit issue dates at the official HTTPS issue endpoint;
- defaults to offline fixtures and requires `--allow-network` for live fetches;
- limits issue count, post count, response size, timeout, content type, and
  redirects;
- keeps public title, origin, description, capture availability, dimensions,
  and capture time while discarding internal selection fields and CDN keys;
- never downloads or redistributes screenshots;
- permanently enforces reference-only, no-training use.

If the source policy becomes stricter, stop online refreshes until the policy
is reviewed. Source availability never changes project authority.

## Evidence and artifact boundary

Keep screenshot PNGs repo-external. Checked-in manifests may record a portable
artifact reference, viewport, byte size, SHA-256, dimensions, target URL,
observation time, and availability. A local-only path is not remote or release
evidence.

Origin audit should cover desktop and mobile, page structure, one meaningful
reachable interaction, keyboard focus, visible semantics, and console errors.
Check Reduced Motion only when motion exists. Keep complete accessibility and
performance status unverified unless separately measured with the applicable
contract.

## Operational cadence

Use a bounded manual cycle rather than a crawler or archive import:

1. ingest no more than a small set of issues;
2. shortlist for product and surface diversity;
3. review a smaller set of cards;
4. live-audit only claims that need origin runtime evidence;
5. build a task-specific Pack;
6. validate on the target before considering promotion.

Do not batch the full archive. New source material can add candidates without
changing installed design rules.

## Completion

Reference work is complete only when:

- the card, catalog, or Pack passes its machine contract;
- authority, target fit, evidence limits, and rights are explicit;
- unavailable and stale evidence remains visible;
- no third-party screenshot or asset entered the repository or package;
- no candidate or proposed hypothesis is reported as an absorbed capability.
