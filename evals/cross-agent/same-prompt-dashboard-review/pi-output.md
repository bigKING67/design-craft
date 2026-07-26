## 1. Evidence level and score band

**Evidence level:** `L0 prose-static` — product context and described structure only.  
No screenshot, DOM, tokens, responsive behavior, interaction states, focus path, loading, or error handling were verified.

**Score band:** **58–68 / 100 product UI taste band**, assuming the described structure is accurate.  
Reason: the concept has the ingredients of an operations dashboard, but the current hierarchy sounds optimized for presenting metrics rather than deciding what needs action in the next hour.

---

## 2. Design read

**Reading this as:** a restrained enterprise **revenue operations command surface** for internal ecommerce operators, dense but calm, optimized for **finding the account or campaign requiring attention now and understanding the next action**.

The dashboard should not optimize for “show all business health at a glance.” It should optimize for:

- exception detection,
- triage by impact and urgency,
- confidence in why something is flagged,
- fast handoff into the account/campaign work object.

---

## 3. Top hierarchy / product-fit issues

### 1. Blocking: KPI card soup hides operational priority
Twelve equal KPI cards create symmetry, not judgment. If every metric has the same weight, the operator must perform the prioritization mentally.

### 2. Blocking: decorative chart consumes attention without answering a decision question
An area chart is only useful if it explains a current exception, trend break, pacing risk, or forecast miss. As described, it sounds like visual atmosphere rather than operational evidence.

### 3. Blocking: dense table is likely the real work surface, but it appears visually secondary
For this user, the account/campaign table is probably the decision queue. If it sits below generic summary modules, the dashboard delays the primary job.

### 4. Blocking: right-rail tips do not match the operator’s next-hour workflow
Generic tips are weak in an enterprise console unless they are entity-specific, evidence-backed, and tied to an owner or action. Otherwise they compete with real signals.

### 5. Blocking: no stated state model for trust and recovery
For revenue operations, loading, stale data, partial data, metric errors, permissions, long labels, and empty exception states are not edge polish; they determine whether the operator can trust the surface.

---

## 4. Concrete design moves

1. **Dashboard card soup → decision surface**  
   Replace the 12-card top grid with a lead operational summary: “Top revenue risk now,” “Accounts needing action,” or “Campaigns breaching threshold.” Keep only supporting metrics in a compact strip.

2. **Flat KPI grid → priority hierarchy**  
   Split metrics into tiers:  
   - lead risk / opportunity,  
   - supporting business context,  
   - diagnostics.  
   Every metric should include comparison context: period, threshold, target, owner, or delta.

3. **Promote the table into an exception queue**  
   Move the account/campaign table closer to the top and order columns by task:  
   identity → severity/status → revenue impact → reason flagged → owner/SLA → next action.  
   Keep numeric columns aligned and scanning-friendly.

4. **Turn the chart into diagnostic evidence**  
   Replace the decorative area chart with a chart that answers one named question, such as:  
   “Which campaigns are pacing below target this hour?” or “Where did spend/revenue diverge?”  
   If it cannot answer a triage question, demote or remove it.

5. **Replace generic tips with an action rail**  
   The right rail should become contextual: selected account/campaign summary, reason codes, recommended action, owner, and recent change log. Generic advice should not occupy persistent dashboard real estate.

6. **Use restrained enterprise visual grammar**  
   Prefer compact typography, subtle dividers, semantic status color, token-backed surfaces, and minimal elevation. Reserve color for severity, variance, freshness, and action state — not decoration.

7. **Design resilient states as first-class modules**  
   Define what renders for loading, stale data, partial data, metric failure, empty exception queue, permission-limited rows, long account names, and zero-result filters.

8. **Keep controls close to affected data**  
   Filters, sort, saved views, time window, channel/account scope, and severity thresholds should live with the queue/table they affect, not as detached global chrome.

---

## 5. Verified versus unverified claims

**Verified from prompt only:**

- Surface is an internal ecommerce revenue operations dashboard.
- Primary user is deciding which account or campaign needs attention in the next hour.
- Current concept has 12 equal KPI cards, decorative area chart, dense account table, and generic right-rail tips.
- Style authority is restrained enterprise console, dense but calm, token-backed color only.

**Not verified:**

- Actual visual hierarchy, spacing, contrast, typography, or token usage.
- Whether the KPI cards are truly equal in rendered weight.
- Whether the chart is actually decorative in implementation.
- Table column order, row density, sorting, filtering, keyboard behavior, or row actions.
- Responsive behavior, hover/focus states, loading/error/empty states.
- Data freshness, metric definitions, source-of-truth, or alert thresholds.
- Browser rendering, screenshots, DOM, accessibility tree, or performance.

---

## 6. Minimal validation plan before implementation

1. **Decision-path review**  
   With product/operator stakeholders, define the top 3 “needs attention now” cases and the exact ranking logic: severity, revenue impact, SLA, trend break, or spend anomaly.

2. **Metric source-of-truth audit**  
   Confirm each KPI’s definition, time window, freshness, owner, and threshold. Separate true source absence from mapping/filter/date issues.

3. **Low-fidelity hierarchy test**  
   Prototype lead summary + exception queue + diagnostic chart + contextual action rail. Test whether an operator can identify the top action in under 3 seconds.

4. **Table usability pass**  
   Validate realistic account/campaign names, long values, zero-result filters, 100+ rows, sorting, selection, and next-action affordances.

5. **State coverage checklist**  
   Verify loading, stale, partial, error, empty, permission-limited, and long-content states before visual polish.

6. **Design-system check**  
   Confirm token roles for surface, text, border, severity, warning, success, focus, and disabled states. No one-off marketing gradients or arbitrary colors.

7. **Accessibility/browser validation later**  
   Before shipping, run actual browser checks for keyboard order, focus visibility, contrast, responsive overflow, tooltip/legend behavior, and table navigation. None of that was performed for this read-only critique.
