from app.matcher import match_items
from app.models import LineItem, SourceLocation


def source():
    return SourceLocation(
        page=1,
        text="test",
    )


def item(description):
    return LineItem(
        description=description,
        quantity=1,
        unit_price=100,
        stated_total=100,
        source=source(),
    )


def test_matches_reordered_items():
    original = [
        item("Business laptops"),
        item("Network switches"),
        item("Wireless access points"),
    ]

    revised = [
        item("Wireless access points"),
        item("Professional laptops"),
        item("Network switches"),
    ]

    results = match_items(original, revised)

    assert len(results) == 3

    assert results[0].status == "confirmed"
    assert results[1].status == "confirmed"
    assert results[2].status == "confirmed"

    assert results[0].revised_index == 1
    assert results[1].revised_index == 2
    assert results[2].revised_index == 0


def test_detects_removed_and_added_items():
    original = [
        item("Business laptops"),
        item("Delivery and logistics"),
    ]

    revised = [
        item("Business laptops"),
        item("Maintenance services"),
    ]

    results = match_items(original, revised)

    removed = next(
        result
        for result in results
        if result.original_index == 1
    )

    added = next(
        result
        for result in results
        if result.revised_index == 1
    )

    assert removed.status == "removed"
    assert removed.revised_index is None

    assert added.status == "added"
    assert added.original_index is None