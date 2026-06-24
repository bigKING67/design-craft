# Report quality

Use this for DataHub, dashboard exports, static reports, special reports, and
business-review pages where reading order and evidence quality matter more than
landing-page drama.

## Report grammar

Reports should feel like a clear analyst deliverable:

1. Cover or compact header: what period, market, channel, or entity is covered.
2. Executive summary: 3-5 decisive points, not a generic hero.
3. Evidence sections: one question per section.
4. Chart-first narrative: charts carry comparisons, trends, mix, and anomalies.
5. Supporting detail: tables, caveats, and methodology only where they earn
   their weight.
6. Appendix or disclosure: dense rows, definitions, and edge caveats.

Do not use generic SaaS landing patterns as the default: giant gradient hero,
decorative cards, testimonial rhythm, animated section banners, or oversized
marketing CTAs.

## Chart-first evidence

- Start from the analytical question: trend, rank, contribution, distribution,
  composition, correlation, or anomaly.
- Use one primary chart per question when possible.
- Prefer direct labels or restrained legends for top series.
- Keep table detail below the chart or behind expansion when the chart answers
  the main question.
- Make units, baseline, date range, and filters visible near the chart.
- Treat negative, zero, missing, and >100% share values explicitly.

## Tables

Use tables when the user must scan exact rows, compare many entities, audit
inputs, or export operational detail.

Avoid:

- Giant tables as the main story.
- Repeating the same metric in chart, card, and table without a different job.
- Unbounded table height inside report sections.
- Dense numeric columns without units, alignment, or sorting cues.

## Navigation and hierarchy

- Use quiet TOC or sticky section markers for long reports.
- Keep headings short and decision-oriented.
- Avoid over-carded layouts; sections can be separated by typography and space.
- Put caveats in footnote-sized copy, hover/title, or methodology blocks when
  secondary.
- Preserve print/export readability if reports are likely to be shared.

## DataHub and special-report defaults

- Business truth and project `DESIGN.md` outrank generic visual rules.
- Use formal-report density: compact header, readable charts, restrained cards.
- Net-change labels should be quiet; keep noisy contribution math in tooltip or
  details when it distracts from the main story.
- If share/contribution exceeds 100%, explain in hover/title or methodology
  rather than making it a headline unless it is the point.
- For channel/material/ROI reports, prioritize trend, contribution, top movers,
  and exceptions over decorative summaries.

## ECharts and responsive checks

- Ensure charts resize after container, tab, drawer, or route changes.
- Verify canvas/SVG does not overflow at narrow width.
- Check tooltip clipping, legend wrapping, axis label rotation, and empty data.
- For hidden tabs or accordions, trigger resize after reveal.
- Browser validation should inspect at least one desktop and one narrow viewport
  when chart layout changed.
