from pathlib import Path

from app.pdf_extractor import extract_pages
from app.parser import parse_offer


def test_parse_original_offer():
    pdf_path = Path(__file__).resolve().parents[2] / "sample-data" / "original.pdf"

    locations = extract_pages(str(pdf_path))
    offer = parse_offer("original.pdf", locations)

    assert offer.currency == "USD"
    assert len(offer.line_items) == 5
    assert offer.stated_grand_total == 5840
    assert offer.delivery_date is not None
    assert offer.delivery_date.value == "15 October 2026"

    first_item = offer.line_items[0]

    assert first_item.description == "Business laptops"
    assert first_item.quantity == 5
    assert first_item.unit_price == 800
    assert first_item.stated_total == 4000