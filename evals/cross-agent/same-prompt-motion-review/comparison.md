# Motion benchmark comparison

Codex and Pi both labeled the Evidence as static, called runtime behavior
unverified, rejected `transition: all`, and proposed concrete design moves.

- **Codex** was stronger on pointer lifecycle, grab-offset preservation,
  presentation-value interruption, velocity continuity, projected endpoints,
  `fill: forwards` state drift, and acceptance tests.
- **Pi** found the main direct-manipulation issues and supplied a useful runtime
  plan, but its implementation suggestions were less precise about eliminating
  `top` animation and maintaining one presentation-state source.
- **Cursor** is unverified because no real Cursor run was collected.
- **Claude** is unverified because no real Claude run was collected.

The comparison demonstrates cross-host value without claiming identical output
or unobserved Cursor/Claude portability.
