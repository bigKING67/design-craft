# Pi adapter

Use the canonical Agent Skill at `skills/design-craft/`.

Pi installations may load skills from project or user skill directories. This
adapter keeps `design-craft` portable while avoiding a Pi-only fork.

## User-level install

```bash
bash scripts/design_craft_init_agent.sh \
  --agent pi \
  --target "$HOME" \
  --scope user
```

This installs to:

```text
$HOME/.pi/agent/skills/design-craft
```

## Project-level install

```bash
bash scripts/design_craft_init_agent.sh \
  --agent pi \
  --target /path/to/project \
  --scope project
```

This installs to:

```text
/path/to/project/.pi/skills/design-craft
```

## Package note

If distributing as a Pi package, package metadata should point to the canonical
`skills/design-craft/` folder and should not duplicate the references. Keep
agent-specific instructions in this adapter.

## Pi-specific expectations

- Keep capability claims truthful to the current Pi runtime and tool namespace.
- If browser or screenshot tools are unavailable, report that validation was not
  performed instead of claiming it.
- Use project rules and `DESIGN.md` above generic references.
