# Testing strategy

Frame tests should not require a live Discord connection.

### Unit tests

Colors, markdown, validation, serialization helpers and attachment descriptors are deterministic and can run without importing the Discord client.

### Integration tests

When the development environment has the supported `discord.py` installed, test that Frame objects are instances of native Discord classes, that `to_components()` produces the expected payload, and that callbacks dispatch correctly.

### Snapshot tests

A future snapshot helper should snapshot deterministic `to_dict()` output rather than the repr of internal Python objects. This gives Frame Studio and CI a stable contract without inventing a second Discord payload encoder.
