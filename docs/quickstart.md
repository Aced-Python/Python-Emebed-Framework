# Quick start

```python
import frame

embed = frame.embed("Welcome!", "Thanks for joining.", color="blurple")
await channel.send(embed=embed)
```

For Components V2:

```python
view = frame.ui.container(
    frame.ui.text("# Welcome"),
    frame.ui.separator(),
    frame.ui.action_row(
        frame.ui.button("Support", custom_id="support", style="primary"),
        frame.ui.button("Docs", url="https://example.com/docs"),
    ),
)
await interaction.response.send_message(view=view)
```
