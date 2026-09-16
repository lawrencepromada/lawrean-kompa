import re

from app.models import DeliveryDate, LineItem, Offer, SourceLocation


MONEY_PATTERN = r"(?:[$Γé¼┬ú]|USD|EUR|GBP)?\s*[\d,]+(?:\.\d{1,2})?"


DATE_PATTERN = re.compile(
    r"\b\d{1,2}\s+"
    r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+\d{4}\b",
    re.IGNORECASE,
)


def parse_number(value: str) -> float:
    value = value.replace(",", "").strip()

    value = re.sub(r"^(USD|EUR|GBP)\s*", "", value, flags=re.IGNORECASE)

    if value.startswith(("$", "Γé¼", "┬ú")):
        value = value[1:].strip()

    return float(value)


def detect_currency(text: str) -> str | None:
    if "$" in text or "USD" in text.upper():
        return "USD"

    if "Γé¼" in text or "EUR" in text.upper():
        return "EUR"

    if "┬ú" in text or "GBP" in text.upper():
        return "GBP"

    return None


def _make_date(
    match: re.Match[str],
    location: SourceLocation,
) -> DeliveryDate:
    return DeliveryDate(
        value=match.group(0),
        source=location,
    )


def parse_document_dates(
    locations: list[SourceLocation],
) -> tuple[
    DeliveryDate | None,
    DeliveryDate | None,
    DeliveryDate | None,
]:
    """
    Locate the document's general Date, Revision Date, and Delivery Date.

    Labels are handled separately so that a general "Date" does not
    accidentally match the "Date" portion of "Delivery Date".
    """

    document_date = None
    revision_date = None
    delivery_date = None

    for location in locations:
        text = location.text.strip()

        # Delivery Date must be checked before the general Date.
        delivery_label = re.search(
            r"\b(?:delivery\s+date|expected\s+delivery)\b",
            text,
            re.IGNORECASE,
        )

        if delivery_label:
            match = DATE_PATTERN.search(
                text,
                delivery_label.end(),
            )

            if match and delivery_date is None:
                delivery_date = _make_date(match, location)

            continue

        # Revision Date / Revised Date / Date Revised.
        revision_label = re.search(
            r"\b(?:revision\s+date|revised\s+date|date\s+revised)\b",
            text,
            re.IGNORECASE,
        )

        if revision_label:
            match = DATE_PATTERN.search(
                text,
                revision_label.end(),
            )

            if match and revision_date is None:
                revision_date = _make_date(match, location)

            continue

        # General document Date.
        # The negative lookahead prevents matching the "Date" inside
        # "Delivery Date" or "Revision Date".
        date_label = re.search(
            r"(?<!delivery\s)(?<!revision\s)(?<!revised\s)"
            r"\bdate\b",
            text,
            re.IGNORECASE,
        )

        if date_label:
            match = DATE_PATTERN.search(
                text,
                date_label.end(),
            )

            if match and document_date is None:
                document_date = _make_date(match, location)

    return document_date, revision_date, delivery_date


def parse_delivery_date(
    locations: list[SourceLocation],
) -> DeliveryDate | None:
    """
    Backwards-compatible wrapper used by existing code/tests.

    It now returns only an explicitly labelled delivery date instead
    of simply taking the first date in the document.
    """

    _, _, delivery_date = parse_document_dates(locations)

    return delivery_date


def parse_line_items(
    locations: list[SourceLocation],
) -> list[LineItem]:
    items: list[LineItem] = []

    for location in locations:
        text = location.text.strip()

        match = re.search(
            rf"(?P<description>.+?)\s+"
            rf"(?P<quantity>\d+(?:\.\d+)?)\s+"
            rf"(?P<unit_price>{MONEY_PATTERN})\s+"
            rf"(?P<total>{MONEY_PATTERN})$",
            text,
        )

        if not match:
            continue

        description = match.group("description").strip()

        if description.lower() in {
            "description",
            "item",
            "product",
            "subtotal",
            "total",
            "grand total",
        }:
            continue

        items.append(
            LineItem(
                description=description,
                quantity=float(match.group("quantity")),
                unit_price=parse_number(match.group("unit_price")),
                stated_total=parse_number(match.group("total")),
                source=location,
            )
        )

    return items


def parse_offer(
    filename: str,
    locations: list[SourceLocation],
) -> Offer:
    combined_text = "\n".join(location.text for location in locations)

    currency = detect_currency(combined_text)

    line_items = parse_line_items(locations)

    document_date, revision_date, delivery_date = parse_document_dates(
        locations
    )

    grand_total = None
    grand_total_source = None

    total_pattern = re.compile(
        rf"(?:grand\s+total|total\s+amount|total)"
        rf"\s*[:\-]?\s*"
        rf"(?:USD|EUR|GBP|\$|Γé¼|┬ú)?\s*"
        rf"(?P<amount>[\d,]+(?:\.\d{{1,2}})?)",
        re.IGNORECASE,
    )

    for location in locations:
        match = total_pattern.search(location.text)

        if match:
            grand_total = parse_number(match.group("amount"))
            grand_total_source = location

    return Offer(
        filename=filename,
        currency=currency,
        line_items=line_items,
        stated_grand_total=grand_total,
        grand_total_source=grand_total_source,
        date=document_date,
        revision_date=revision_date,
        delivery_date=delivery_date,
    )