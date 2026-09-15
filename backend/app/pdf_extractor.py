import pymupdf

from app.models import SourceLocation


def extract_pages(pdf_path: str) -> list[SourceLocation]:
    document = pymupdf.open(pdf_path)
    locations: list[SourceLocation] = []

    try:
        for page_number, page in enumerate(document, start=1):
            blocks = page.get_text("blocks")

            for block in blocks:
                x0, y0, x1, y1, text = block[:5]

                text = text.strip()

                if not text:
                    continue

                locations.append(
                    SourceLocation(
                        page=page_number,
                        text=text,
                        x0=x0,
                        y0=y0,
                        x1=x1,
                        y1=y1,
                    )
                )
    finally:
        document.close()

    return locations