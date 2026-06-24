# Live task log

This file records real task evidence for the `frontend-craft` workflow. It is
not a substitute for validation output; every entry must state what actually
ran and what remains unverified.

## 2026-06-24 - DataHub marketing industry-news route migration smoke

- Target:
  `/Users/gaoqian/Documents/sixseven/workman/groland/datahub/src/app/marketing/industry-news`
- Purpose: verify that the workflow can route a real DataHub frontend surface
  while preserving DataHub `DESIGN.md` authority over generic taste guidance.
- Expected authority:
  `/Users/gaoqian/Documents/sixseven/workman/groland/datahub/DESIGN.md`
- Route command:

  ```bash
  bash scripts/frontend_craft_route.sh \
    --target /Users/gaoqian/Documents/sixseven/workman/groland/datahub/src/app/marketing/industry-news \
    --surface dashboard \
    --intent visual-refine \
    --scope page
  ```

- Evidence status at 2026-06-24 route-policy migration:
  - `frontend_tier`: `L2`
  - `candidate_skills`: `frontend-craft`, `minimalist-ui`,
    `redesign-existing-projects`
  - `preflight_status`: `pass`
  - `preflight_code`: `OK`
  - `style_authority_path`:
    `/Users/gaoqian/Documents/sixseven/workman/groland/datahub/DESIGN.md`
  - `browser_validation_required`: `true`
  - `directory_governance_required`: `true`
  - `performance_review_required`: `true`
- Browser validation: not claimed by this log entry.
