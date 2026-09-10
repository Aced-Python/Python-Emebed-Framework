"""Discord's documented embed limits, and validation against them.

Kept as one small module so the numbers are easy to audit/update if
Discord changes them, and so both :class:`~frame.embed.builder.Embed` and
tests import from a single source of truth.
"""

from __future__ import annotations

from ..exceptions import InvalidEmbedError

TITLE_LIMIT = 256
DESCRIPTION_LIMIT = 4096
FIELD_NAME_LIMIT = 256
FIELD_VALUE_LIMIT = 1024
FOOTER_TEXT_LIMIT = 2048
AUTHOR_NAME_LIMIT = 256
MAX_FIELDS = 25
# Combined length of title + description + every field name/value +
# footer text + author name, summed across ALL embeds in one message.
TOTAL_LIMIT = 6000


def check_length(value: str, limit: int, *, what: str) -> None:
    if len(value) > limit:
        raise InvalidEmbedError(
            f"Embed {what} exceeds Discord's {limit} character limit",
            current=len(value),
            maximum=limit,
        )


def check_field_count(count: int) -> None:
    if count > MAX_FIELDS:
        raise InvalidEmbedError(
            "Embed has too many fields",
            current=count,
            maximum=MAX_FIELDS,
        )


def total_length(
    *,
    title: str = "",
    description: str = "",
    footer: str = "",
    author: str = "",
    fields: list[tuple[str, str, bool]] | None = None,
) -> int:
    total = len(title) + len(description) + len(footer) + len(author)
    for name, value, _inline in fields or []:
        total += len(name) + len(value)
    return total


def check_total_length(**kwargs) -> None:
    total = total_length(**kwargs)
    if total > TOTAL_LIMIT:
        raise InvalidEmbedError(
            "Embed's combined content (title + description + fields + "
            "footer + author) exceeds Discord's total character limit",
            current=total,
            maximum=TOTAL_LIMIT,
        )
