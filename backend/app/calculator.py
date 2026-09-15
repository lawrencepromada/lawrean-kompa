from dataclasses import dataclass

from app.models import LineItem, Offer


@dataclass
class LineCalculation:
    description: str
    quantity: float | None
    unit_price: float | None
    stated_total: float | None
    calculated_total: float | None
    discrepancy: float | None


@dataclass
class OfferCalculation:
    lines: list[LineCalculation]
    calculated_grand_total: float
    stated_grand_total: float | None
    grand_total_discrepancy: float | None


def calculate_line(item: LineItem) -> LineCalculation:
    calculated_total = None

    if item.quantity is not None and item.unit_price is not None:
        calculated_total = round(
            item.quantity * item.unit_price,
            2,
        )

    discrepancy = None

    if calculated_total is not None and item.stated_total is not None:
        discrepancy = round(
            item.stated_total - calculated_total,
            2,
        )

    return LineCalculation(
        description=item.description,
        quantity=item.quantity,
        unit_price=item.unit_price,
        stated_total=item.stated_total,
        calculated_total=calculated_total,
        discrepancy=discrepancy,
    )


def calculate_offer(offer: Offer) -> OfferCalculation:
    lines = [
        calculate_line(item)
        for item in offer.line_items
    ]

    calculated_grand_total = round(
        sum(
            line.calculated_total
            for line in lines
            if line.calculated_total is not None
        ),
        2,
    )

    grand_total_discrepancy = None

    if offer.stated_grand_total is not None:
        grand_total_discrepancy = round(
            offer.stated_grand_total - calculated_grand_total,
            2,
        )

    return OfferCalculation(
        lines=lines,
        calculated_grand_total=calculated_grand_total,
        stated_grand_total=offer.stated_grand_total,
        grand_total_discrepancy=grand_total_discrepancy,
    )