from pathlib import Path

from app.calculator import calculate_offer
from app.parser import parse_offer
from app.pdf_extractor import extract_pages


def test_calculate_original_offer():
    pdf_path = (
        Path(__file__).resolve().parents[2]
        / "sample-data"
        / "original.pdf"
    )

    locations = extract_pages(str(pdf_path))
    offer = parse_offer("original.pdf", locations)

    result = calculate_offer(offer)

    assert result.calculated_grand_total == 5840
    assert result.stated_grand_total == 5840
    assert result.grand_total_discrepancy == 0

    assert result.lines[0].calculated_total == 4000
    assert result.lines[1].calculated_total == 600
    assert result.lines[2].calculated_total == 500
    assert result.lines[3].calculated_total == 540
    assert result.lines[4].calculated_total == 200