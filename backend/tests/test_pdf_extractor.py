from pathlib import Path

from app.pdf_extractor import extract_pages


def test_extract_pages_from_pdf():
    pdf_path = Path(__file__).resolve().parents[2] / "sample-data" / "original.pdf"

    locations = extract_pages(str(pdf_path))

    assert locations
    assert all(location.page >= 1 for location in locations)