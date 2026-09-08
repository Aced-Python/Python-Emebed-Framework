# Migration from raw discord.py

### Before

```python
embed = discord.Embed(
    title="Welcome",
    description="Hello!",
    color=discord.Color.blurple(),
)
embed.set_thumbnail(url=avatar)
embed.add_field(name="Members", value="100", inline=True)
```

### After

```python
embed = frame.embed(
    "Welcome",
    "Hello!",
    color="blurple",
    thumbnail=avatar,
    fields=[("Members", "100", True)],
)
```

Both compile to a native `discord.Embed`. You can pass the result to existing `discord.py` APIs without rewriting your bot.
