# Comparative skill evals

These cases compare a no-skill baseline, the current focused Emil Kowalski upstream,
and `design-craft` under the same host, model, reasoning profile, and prompt.
They complement cross-host portability tests; they do not replace browser or
native implementation evidence.

Use Pi for the initial ablation because it can explicitly disable all discovered
skills and load only the named variant. Preserve raw outputs and run manifests,
then grade anonymized outputs against the case scorecard.

Active cases:

- `emil-motion-ablation`: concise gesture-sheet critique and interaction physics.
- `emil-motion-planning-ablation`: codebase recon, vetted prioritization, and
  self-contained implementation plans using the current `improve-animations`
  upstream alongside Apple and review guidance.

Run the following workflow for each active case:

```bash
python3 scripts/design_craft_comparative_run.py \
  --case-dir evals/comparative/emil-motion-ablation \
  --model <pi-model> --thinking high

python3 scripts/design_craft_comparative_blind.py \
  --case-dir evals/comparative/emil-motion-ablation \
  --seed <release-specific-seed>

python3 scripts/design_craft_comparative_judge.py \
  --case-dir evals/comparative/emil-motion-ablation \
  --host <codex|cursor|claude> \
  --model <judge-model> \
  --reasoning-profile <profile>

python3 scripts/design_craft_comparative_record.py \
  --case-dir evals/comparative/emil-motion-ablation

make comparative-observed-check
```

The Pi runner copies every selected skill into a repo-external isolated
workspace, fingerprints the source worktree before and after each run, and
publishes no repository evidence unless all three variants succeed. Outputs may
not reveal a skill/source brand. The independent judge receives only the blind
packet in an empty repo-external workspace; its raw output, canonical judgment,
host metadata, and worktree fingerprints are bound by `run.judge.json`.

Certified comparison requires `design-craft` to score above both alternatives
in every active case. If it does not, fix the Skill or narrow the claim; do not
edit the judgment headline or hand-author judge metadata.
