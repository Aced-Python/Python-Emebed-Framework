# Competitive analysis

Frame should not compete by reimplementing a Discord bot runtime.

| Tool | Primary value | Frame's position |
| --- | --- | --- |
| `discord.py` | General Discord API wrapper | Keep it underneath Frame; preserve native objects and existing bot architecture. |
| `discord-ui` | Older UI/interaction extension | Learn from the ergonomic direction, but avoid overriding core client behavior or owning the bot lifecycle. |
| `nextcord` / `disnake` / `py-cord` | Alternative Discord API wrappers | Do not fork the runtime. Frame deliberately standardizes on `discord.py` and focuses on authoring DX. |

A key opportunity is the gap between raw Discord primitives and a visual/design-system-oriented authoring workflow. Frame's differentiators are deliberately narrow: ergonomic native builders, pre-send validation, deterministic serialization, themes, and a future-compatible component tree for tooling.

The project should avoid a feature checklist race. Pagination, polls, and dashboards are better positioned as extension packages unless they become universally useful authoring primitives.
