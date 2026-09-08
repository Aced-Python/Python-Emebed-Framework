# Design tokens and themes

Themes are plain data so they can later be serialized for Frame Studio.

```python
theme = frame.Theme(
    color="#5865F2",
    footer="My Bot",
    thumbnail="https://example.com/logo.png",
)

frame.set_theme(theme)
```

For long-lived applications, prefer passing `theme=` explicitly at subsystem boundaries. `set_theme()` is context-local rather than process-global, which keeps concurrent interactions isolated.
