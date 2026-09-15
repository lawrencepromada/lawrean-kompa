import os
import tempfile
import time

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.comparator import compare_offers
from app.parser import parse_offer
from app.pdf_extractor import extract_pages


app = FastAPI(
    title="Lawrean Kompa",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


MAX_PAGES = 3
MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_LINE_ITEMS = 10


@app.get("/")
def health_check():
    return {
        "name": "Lawrean Kompa",
        "status": "running",
    }


@app.post("/compare")
async def compare(
    original: UploadFile = File(...),
    revised: UploadFile = File(...),
):
    start_time = time.perf_counter()

    original_path = None
    revised_path = None

    try:
        if (
            not original.filename
            or not original.filename.lower().endswith(".pdf")
        ):
            raise HTTPException(
                status_code=400,
                detail="Original document must be a PDF.",
            )

        if (
            not revised.filename
            or not revised.filename.lower().endswith(".pdf")
        ):
            raise HTTPException(
                status_code=400,
                detail="Revised document must be a PDF.",
            )

        original_data = await original.read()
        revised_data = await revised.read()

        if len(original_data) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="Original PDF is too large.",
            )

        if len(revised_data) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="Revised PDF is too large.",
            )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as original_file:
            original_file.write(original_data)
            original_path = original_file.name

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf",
        ) as revised_file:
            revised_file.write(revised_data)
            revised_path = revised_file.name

        original_locations = extract_pages(original_path)
        revised_locations = extract_pages(revised_path)

        original_page_count = max(
            (location.page for location in original_locations),
            default=0,
        )

        revised_page_count = max(
            (location.page for location in revised_locations),
            default=0,
        )

        if original_page_count > MAX_PAGES:
            raise HTTPException(
                status_code=400,
                detail="Original PDF exceeds the 3-page limit.",
            )

        if revised_page_count > MAX_PAGES:
            raise HTTPException(
                status_code=400,
                detail="Revised PDF exceeds the 3-page limit.",
            )

        original_offer = parse_offer(
            original.filename,
            original_locations,
        )

        revised_offer = parse_offer(
            revised.filename,
            revised_locations,
        )

        if original_offer.currency is None:
            raise HTTPException(
                status_code=400,
                detail="Original PDF currency could not be determined.",
            )

        if revised_offer.currency is None:
            raise HTTPException(
                status_code=400,
                detail="Revised PDF currency could not be determined.",
            )

        if original_offer.currency != revised_offer.currency:
            raise HTTPException(
                status_code=400,
                detail=(
                    "The original and revised PDFs must use "
                    "the same currency."
                ),
            )

        if len(original_offer.line_items) > MAX_LINE_ITEMS:
            raise HTTPException(
                status_code=400,
                detail="Original PDF contains more than 10 line items.",
            )

        if len(revised_offer.line_items) > MAX_LINE_ITEMS:
            raise HTTPException(
                status_code=400,
                detail="Revised PDF contains more than 10 line items.",
            )

        result = compare_offers(
            original_offer,
            revised_offer,
        )

        response = result.model_dump()

        response["processing_time_seconds"] = round(
            time.perf_counter() - start_time,
            3,
        )

        return response

    finally:
        if original_path and os.path.exists(original_path):
            os.remove(original_path)

        if revised_path and os.path.exists(revised_path):
            os.remove(revised_path)