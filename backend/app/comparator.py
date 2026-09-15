from app.calculator import calculate_offer
from app.models import Change, ComparisonResult, Offer
from app.matcher import match_items


def compare_offers(
    original: Offer,
    revised: Offer,
) -> ComparisonResult:
    matches = match_items(
        original.line_items,
        revised.line_items,
    )

    changes: list[Change] = []

    original_calculation = calculate_offer(original)
    revised_calculation = calculate_offer(revised)

    for match in matches:
        if match.status == "uncertain":
            original_source = None
            revised_source = None

            if match.original_index is not None:
                original_source = original.line_items[
                    match.original_index
                ].source

            if match.revised_index is not None:
                revised_source = revised.line_items[
                    match.revised_index
                ].source

            changes.append(
                Change(
                    change_type="uncertain_match",
                    description=match.reason,
                    original_value=(
                        original.line_items[
                            match.original_index
                        ].description
                        if match.original_index is not None
                        else None
                    ),
                    revised_value=(
                        revised.line_items[
                            match.revised_index
                        ].description
                        if match.revised_index is not None
                        else None
                    ),
                    original_source=original_source,
                    revised_source=revised_source,
                    severity="warning",
                )
            )
            continue

        if match.status == "removed":
            original_item = original.line_items[
                match.original_index
            ]

            possible_revised_items = [
                item
                for item in revised.line_items
                if item.description != original_item.description
            ]

            # If the number of items stayed the same, an unmatched
            # original item may actually correspond to a renamed/replaced
            # revised item. Do not claim removal without enough evidence.
            if (
                len(original.line_items)
                == len(revised.line_items)
                and possible_revised_items
            ):
                candidate_revised_item = possible_revised_items[0]

                changes.append(
                    Change(
                        change_type="needs_clarification",
                        description=(
                            "Could not confidently determine whether "
                            f"'{original_item.description}' corresponds "
                            f"to '{candidate_revised_item.description}'. "
                            "Clarification is required."
                        ),
                        original_value=original_item.description,
                        revised_value=candidate_revised_item.description,
                        original_source=original_item.source,
                        revised_source=candidate_revised_item.source,
                        severity="warning",
                    )
                )
            else:
                changes.append(
                    Change(
                        change_type="item_removed",
                        description=(
                            f"Item removed: "
                            f"{original_item.description}"
                        ),
                        original_value=original_item.description,
                        original_source=original_item.source,
                        severity="high",
                    )
                )

            continue

        if match.status == "added":
            revised_item = revised.line_items[
                match.revised_index
            ]

            if len(original.line_items) != len(revised.line_items):
                changes.append(
                    Change(
                        change_type="item_added",
                        description=(
                            f"Item added: "
                            f"{revised_item.description}"
                        ),
                        revised_value=revised_item.description,
                        revised_source=revised_item.source,
                        severity="high",
                    )
                )

            continue

        if match.status != "confirmed":
            continue

        original_item = original.line_items[
            match.original_index
        ]

        revised_item = revised.line_items[
            match.revised_index
        ]

        if original_item.description != revised_item.description:
            changes.append(
                Change(
                    change_type="description_changed",
                    description=(
                        f"Item renamed from "
                        f"'{original_item.description}' "
                        f"to '{revised_item.description}'."
                    ),
                    original_value=original_item.description,
                    revised_value=revised_item.description,
                    original_source=original_item.source,
                    revised_source=revised_item.source,
                    severity="info",
                )
            )

        if original_item.quantity != revised_item.quantity:
            changes.append(
                Change(
                    change_type="quantity_changed",
                    description=(
                        f"Quantity changed for "
                        f"'{revised_item.description}'."
                    ),
                    original_value=str(
                        original_item.quantity
                    ),
                    revised_value=str(
                        revised_item.quantity
                    ),
                    original_source=original_item.source,
                    revised_source=revised_item.source,
                    severity="high",
                )
            )

        if original_item.unit_price != revised_item.unit_price:
            changes.append(
                Change(
                    change_type="unit_price_changed",
                    description=(
                        f"Unit price changed for "
                        f"'{revised_item.description}'."
                    ),
                    original_value=str(
                        original_item.unit_price
                    ),
                    revised_value=str(
                        revised_item.unit_price
                    ),
                    original_source=original_item.source,
                    revised_source=revised_item.source,
                    severity="high",
                )
            )

        if original_item.stated_total != revised_item.stated_total:
            changes.append(
                Change(
                    change_type="line_total_changed",
                    description=(
                        f"Line total changed for "
                        f"'{revised_item.description}'."
                    ),
                    original_value=str(
                        original_item.stated_total
                    ),
                    revised_value=str(
                        revised_item.stated_total
                    ),
                    original_source=original_item.source,
                    revised_source=revised_item.source,
                    severity="high",
                )
            )

        original_line_calculation = (
            original_calculation.lines[
                match.original_index
            ]
        )

        if (
            original_line_calculation.discrepancy is not None
            and original_line_calculation.discrepancy != 0
        ):
            changes.append(
                Change(
                    change_type="line_arithmetic_discrepancy",
                    description=(
                        f"Original line total for "
                        f"'{original_item.description}' "
                        f"does not match quantity × unit price."
                    ),
                    original_value=str(
                        original_item.stated_total
                    ),
                    revised_value=str(
                        original_line_calculation.calculated_total
                    ),
                    original_source=original_item.source,
                    revised_source=revised_item.source,
                    severity="warning",
                )
            )

        revised_line_calculation = (
            revised_calculation.lines[
                match.revised_index
            ]
        )

        if (
            revised_line_calculation.discrepancy is not None
            and revised_line_calculation.discrepancy != 0
        ):
            changes.append(
                Change(
                    change_type="line_arithmetic_discrepancy",
                    description=(
                        f"Revised line total for "
                        f"'{revised_item.description}' "
                        f"does not match quantity × unit price."
                    ),
                    original_value=str(
                        original_item.stated_total
                    ),
                    revised_value=str(
                        revised_line_calculation.calculated_total
                    ),
                    original_source=original_item.source,
                    revised_source=revised_item.source,
                    severity="warning",
                )
            )

    if (
        original.delivery_date is not None
        and revised.delivery_date is not None
        and original.delivery_date.value
        != revised.delivery_date.value
    ):
        changes.append(
            Change(
                change_type="delivery_date_changed",
                description="Delivery date changed.",
                original_value=original.delivery_date.value,
                revised_value=revised.delivery_date.value,
                original_source=original.delivery_date.source,
                revised_source=revised.delivery_date.source,
                severity="high",
            )
        )

    if (
        original_calculation.grand_total_discrepancy is not None
        and original_calculation.grand_total_discrepancy != 0
    ):
        changes.append(
            Change(
                change_type="arithmetic_discrepancy",
                description=(
                    "Original offer contains a "
                    "grand-total discrepancy."
                ),
                original_value=str(
                    original.stated_grand_total
                ),
                revised_value=str(
                    original_calculation.calculated_grand_total
                ),
                original_source=original.grand_total_source,
                severity="warning",
            )
        )

    if (
        revised_calculation.grand_total_discrepancy is not None
        and revised_calculation.grand_total_discrepancy != 0
    ):
        changes.append(
            Change(
                change_type="arithmetic_discrepancy",
                description=(
                    "Revised offer contains a "
                    "grand-total discrepancy."
                ),
                original_value=str(
                    revised.stated_grand_total
                ),
                revised_value=str(
                    revised_calculation.calculated_grand_total
                ),
                revised_source=revised.grand_total_source,
                severity="warning",
            )
        )

    return ComparisonResult(
        currency=original.currency,
        matches=matches,
        changes=changes,
        original_calculated_total=(
            original_calculation.calculated_grand_total
        ),
        revised_calculated_total=(
            revised_calculation.calculated_grand_total
        ),
        original_stated_total=original.stated_grand_total,
        revised_stated_total=revised.stated_grand_total,
    )