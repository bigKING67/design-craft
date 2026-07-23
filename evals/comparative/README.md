# Comparative skill evals

`scorecard.json` is the machine authority for criterion IDs and weights.
`scorecard.md` is deterministically generated from the machine-authoritative
`scorecard.json`; the validator rejects any drift. It is hashed into
run provenance, but validators never parse Markdown tables as score data.

These cases compare a no-skill baseline, one focused upstream variant, and
`design-craft` under the same host, model, reasoning profile, and prompt. They
complement cross-host portability tests; they do not replace browser or native
implementation evidence.

Use Pi for the initial ablation because it can explicitly disable all discovered
skills and load only the named variant. Preserve raw outputs and run manifests,
then grade anonymized outputs against the case scorecard.

Active cases:

- `emil-motion-ablation`: concise gesture-sheet critique and interaction physics.
- `emil-motion-planning-ablation`: codebase recon, vetted prioritization, and
  self-contained implementation plans using the current `improve-animations`
  upstream alongside Apple and review guidance.
- `taste-visual-critique-ablation`: product hierarchy, anti-generic judgment,
  typography/surface craft, product fit, and concrete redesign moves.
- `impeccable-production-ablation`: audit sequencing, hostile-data hardening,
  responsive/accessibility quality, detector reconciliation, and measured
  performance planning.

Active case directories are definition truth only until a complete new run is
recorded. The 2026-07-12 result tranche is preserved byte-for-byte under
`history/v0.4.0/`; it cannot satisfy a current-source release gate.

Run the following workflow for each active case:

```bash
python3 scripts/design_craft_comparative_run.py \
  --case-dir evals/comparative/<case-id> \
  --model <pi-model> --thinking high

python3 scripts/design_craft_comparative_blind.py \
  --case-dir evals/comparative/<case-id> \
  --seed <release-specific-seed>

python3 scripts/design_craft_comparative_judge.py \
  --case-dir evals/comparative/<case-id> \
  --host <codex|cursor|claude> \
  --model <judge-model> \
  --reasoning-profile <profile>

python3 scripts/design_craft_comparative_record.py \
  --case-dir evals/comparative/<case-id>

make comparative-observed-check
```

The Pi runner copies every selected skill into a repo-external isolated
workspace, fingerprints the source worktree before and after each run, and
publishes no repository evidence unless all three variants succeed. Outputs may
not reveal a skill/source brand. The independent judge receives only the blind
packet in an empty repo-external workspace; its raw output, canonical judgment,
host metadata, and worktree fingerprints are bound by `run.judge.json`.

Each `variants.json` declares its focused upstream with
`focused_variant`. Certified comparison requires `design-craft` to score above
both the no-skill baseline and that focused upstream in every active case. If
it does not, fix the Skill or narrow the claim; do not edit the judgment
headline or hand-author judge metadata.

Validate archived internal hashes separately with:

```bash
python3 scripts/design_craft_comparative_validate.py \
  --history-root evals/comparative/history
```
