# Security Policy

## Supported versions

Frame is pre-1.0. Security fixes are made against the latest released `0.x` version; there is no long-term support branch yet.

| Version | Supported |
|---|---|
| 0.1.x | ✅ |
| < 0.1 | ❌ |

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Instead, use GitHub's private vulnerability reporting (Security tab → "Report a vulnerability") on the repository, or email the maintainers listed in `pyproject.toml`. Include:

- A description of the issue and its potential impact
- Steps to reproduce (a minimal `frame` snippet is ideal)
- The frame and discord.py versions you tested against

We'll acknowledge reports within a few days and aim to ship a fix or mitigation before any public disclosure. Frame is a thin layer over discord.py — if a report turns out to be a discord.py or Discord API issue rather than a frame-specific one, we'll help route it to the right place.

## Scope

In scope: frame's own code (embed/color/markdown validation, Components V2 tree validation and conversion, attachment handling). Out of scope: vulnerabilities in discord.py itself, or in bots built using frame (report those to the bot's own maintainers).
