# Architecture

## Design principles

### 1. Native outputs

The public builders compile directly to `discord.Embed`, `discord.File`, `discord.ui.*`, and `discord.ui.LayoutView` instances. There is no second networking layer and no hidden bot lifecycle.

### 2. Validation before HTTP

The library mirrors documented limits where practical. It should be easier to diagnose a broken payload locally than after Discord returns `400 Bad Request`.

### 3. Progressive disclosure

The function API is deliberately small. Advanced users can switch to `EmbedBuilder`, native discord.py subclasses, or raw component constructors without leaving Frame's mental model.

### 4. Deterministic serialization

`discord.py` owns canonical Discord payload behavior. Frame's `to_dict()` helpers expose a stable debugging boundary, but do not attempt to become a duplicate Discord protocol implementation.

### 5. Compatibility layer, not replacement runtime

Frame must remain embeddable in ordinary cogs, commands, listeners, persistent views, and interaction handlers.

## Package layout

```text
src/frame/
├── attachments/    local-file descriptors and upload conversion
├── colors/         immutable color normalization
├── embed/          ergonomic embed builder + Discord compilation
├── markdown/       small Discord-markdown composition helpers
├── ui/             Components V2 factories and callback conveniences
├── exceptions.py   user-facing error taxonomy
└── __init__.py     small public surface
```

## Components V2 strategy

Discord's current component reference exposes message layout and modal primitives separately. Frame's message API therefore mirrors the message-oriented V2 tree first: Container → TextDisplay / Section / Separator / MediaGallery / ActionRow / File, with Button and select primitives where Discord permits them. Modal-only components are intentionally kept out of `frame.ui.container()`.

The root object is a native `discord.ui.LayoutView`. This is important because `discord.py` handles the Components V2 message flag and view lifecycle. Frame should not duplicate that machinery. The library should also preserve the escape hatch to raw `discord.py` components.

## Themes

Themes are plain data objects, not global mutable configuration. `frame.set_theme()` stores the current default in a `contextvars.ContextVar`, so concurrent interactions do not share mutable theme state.

## Attachments

A local upload is represented as a lazy `Attachment` descriptor. The descriptor knows how to produce a `discord.File` and how to produce an `attachment://filename` URL. Frame never opens files at import time and never claims that a path is a remote URL.

## Future visual tooling

A future Frame Studio should consume the same deterministic object graph exposed through Frame's JSON/debug boundary. The Python package should not depend on the web application; Studio can be a separate product that imports/export serialized Frame trees.
