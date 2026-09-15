import re

from app.models import DeliveryDate, LineItem, Offer, SourceLocation


MONEY_PATTERN = r"(?:[$€£]|USD|EUR|GBP)?\s*[\d,]+(?:\.\d{1,2})?"


def parse_number(value: str) -> float:
    value = value.replace(",", "").strip()

    value = re.sub(r"^(USD|EUR|GBP)\s*", "", value, flags=re.IGNORECASE)

    if value.startswith(("$", "€", "£")):
        value = value[1:].strip()

    return float(value)


def detect_currency(text: str) -> str | None:
    if "$" in text or "USD" in text.upper():
        return "USD"

    if "€" in text or "EUR" in text.upper():
        return "EUR"

    if "£" in text or "GBP" in text.upper():
        return "GBP"

    return None


def parse_delivery_date(
    locations: list[SourceLocation],
) -> DeliveryDate | None:
    pattern = re.compile(
        r"\b\d{1,2}\s+"
        r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
        r"\s+\d{4}\b",
        re.IGNORECASE,
    )

    for location in locations:
        match = pattern.search(location.text)

        if match:
            return DeliveryDate(
                value=match.group(0),
                source=location,
            )

    return None


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

    delivery_date = parse_delivery_date(locations)

    grand_total = None
    grand_total_source = None

    total_pattern = re.compile(
        rf"(?:grand\s+total|total\s+amount|total)"
        rf"\s*[:\-]?\s*"
        rf"(?:USD|EUR|GBP|\$|€|£)?\s*"
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
        delivery_date=delivery_date,
    )