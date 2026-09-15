from pathlib import Path

from app.comparator import compare_offers
from app.parser import parse_offer
from app.pdf_extractor import extract_pages


def load_offer(filename: str):
    pdf_path = (
        Path(__file__).resolve().parents[2]
        / "sample-data"
        / filename
    )

    locations = extract_pages(str(pdf_path))

    return parse_offer(filename, locations)


def test_compare_original_and_revised():
    original = load_offer("original.pdf")
    revised = load_offer("revised.pdf")

    result = compare_offers(original, revised)

    change_types = {
        change.change_type
        for change in result.changes
    }

    assert "description_changed" in change_types
    assert "quantity_changed" in change_types
    assert "unit_price_changed" in change_types
    assert "item_removed" in change_types
    assert "delivery_date_changed" in change_types
    assert "arithmetic_discrepancy" in change_types

    assert result.original_calculated_total == 5840
    assert result.revised_calculated_total == 6490

    assert result.revised_stated_total == 6390


def test_formatting_only_changes_produce_no_substantive_changes():
    original = load_offer("original.pdf")
    formatting_only = load_offer("formatting-only.pdf")

    result = compare_offers(
        original,
        formatting_only,
    )

    assert result.changes == []

    assert result.original_calculated_total == 5840
    assert result.revised_calculated_total == 5840

    assert result.original_stated_total == 5840
    assert result.revised_stated_total == 5840