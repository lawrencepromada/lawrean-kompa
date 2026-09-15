---
title: Lawrean Kompa API
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---

# Lawrean Kompa

Lawrean Kompa is a browser-based prototype for comparing two versions of a commercial offer PDF and identifying substantive changes between them.

The prototype is designed for text-based commercial offer PDFs and focuses on reliable comparison of item descriptions, quantities, unit prices, totals, delivery dates, and arithmetic discrepancies.

## Project Summary

Lawrean Kompa helps users review revised commercial offers without manually comparing every line item. It extracts structured data from both PDFs, matches corresponding items despite renaming or reordering, identifies substantive changes, and independently recalculates financial totals. When the system cannot confidently determine a correspondence, it flags the case for clarification rather than making an unsupported conclusion. Each reported change is backed by source evidence from the documents.


## Core Workflow

1. Upload the original commercial offer PDF.
2. Upload the revised commercial offer PDF.
3. Extract structured information from both documents.
4. Match corresponding line items even when rows have been renamed or reordered.
5. Detect substantive commercial changes.
6. Recalculate totals deterministically.
7. Identify discrepancies between stated and calculated totals.
8. Flag uncertain matches instead of making unsupported conclusions.
9. Show source evidence from both documents for detected changes.

## Architecture

Browser
→ React + Vite frontend
→ FastAPI backend
→ PyMuPDF PDF extraction
→ Structured document parsing
→ Semantic item matching
→ Deterministic comparison and calculation
→ Results displayed in the browser

## Important Design Decision

Semantic reasoning is used only where interpretation is required, mainly for determining whether differently named line items may represent the same item.

Arithmetic and commercial calculations are handled deterministically in Python.

The system does not allow a language model to silently calculate or replace financial values.

## Source Evidence

Every reported substantive change should reference the relevant source location in both the original and revised documents where applicable.

Source locations contain:

* Page number
* Extracted source text
* Bounding-box coordinates when available

This allows detected changes to be traced back to the source PDFs.

## Technology Stack

### Frontend

* React
* Vite
* JavaScript
* Plain CSS

### Backend

* Python
* FastAPI
* Pydantic
* PyMuPDF
* sentence-transformers
* pytest

### Semantic Matching Model

The prototype uses:

sentence-transformers/all-MiniLM-L6-v2

The model runs locally and is used for semantic similarity between line-item descriptions.

## Project Structure

```
lawrean_kompa/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── pdf_extractor.py
│   │   ├── parser.py
│   │   ├── matcher.py
│   │   └── comparator.py
│   ├── tests/
│   ├── calculator.py
│   ├── measure_timing.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
│
├── sample-data/
│   ├── original.pdf
│   ├── revised.pdf
│   ├── ambiguous-original.pdf
│   ├── ambiguous-revised.pdf
│   ├── formatting-only.pdf
│   ├── unresolvable-original.pdf
│   ├── unresolvable-revised.pdf
│   └── expected-results.json
│
└── README.md
```

## Running Locally

### Backend

Open Command Prompt and run:

```
cd /d D:\Lawrean\lawrean_kompa\backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

The backend runs at:

```
http://127.0.0.1:8000
```

### Frontend

Open a second Command Prompt window and run:

```
cd /d D:\Lawrean\lawrean_kompa\frontend
npm run dev
```

The frontend runs at:

```
http://localhost:5173
```

Open the frontend address in a browser.

## Input Constraints

The current prototype accepts:

* PDF files only
* Text-based PDFs
* Maximum 3 pages per document
* Maximum 10 MB per PDF
* One currency per document pair
* Maximum 10 line items

Handwritten or scanned documents are outside the current prototype scope because OCR is not included.

## Testing

The backend includes unit tests and an evaluation test set.

Run the complete test suite with:

```
cd /d D:\Lawrean\lawrean_kompa\backend
.venv\Scripts\activate
pytest -q
```

Current result:

```
12 passed
```

The evaluation scenarios are run with:

```
pytest -q -s tests\test_evaluation.py
```

Current evaluation result:

```
Expected-change scenarios: 3
Detected-change scenarios: 3
False-change scenarios: 0
Missed-change scenarios: 0
Source references valid: 10/10
Source-reference accuracy: 100.0%
```

## Evaluation Scenarios

The reproducible test set contains four scenarios.

### 1. Normal Revision

Tests:

* Renamed item
* Reordered rows
* Quantity change
* Unit-price change
* Removed item
* Delivery-date change
* Incorrect stated grand total
* Arithmetic discrepancy

Expected result:

Substantive changes are detected and source evidence is provided.

### 2. Ambiguous Match

Tests a renamed item where the semantic similarity is not high enough for a confident match.

Expected result:

The item is flagged for review instead of being treated as a confirmed match.

### 3. Formatting Only

Tests visual and formatting changes without changing commercial meaning.

Expected result:

No substantive commercial changes are reported.

### 4. Unresolvable Match

Tests two items where the system cannot safely determine whether they correspond.

Expected result:

The system asks for clarification instead of incorrectly reporting an item as removed or added.

## Deterministic Calculation

For each line item, the system calculates:

```
quantity × unit price = calculated line total
```

It compares the calculated value with the stated line total.

For the offer:

```
sum of calculated line totals = calculated grand total
```

The calculated grand total is then compared with the stated grand total.

The system reports discrepancies rather than silently replacing the source value.

## Measured Processing Time

A three-run timing test was performed using the normal revision scenario.

Results:

```
Run 1: 21.997s client total | 7.742s API processing
Run 2: 0.141s client total  | 0.134s API processing
Run 3: 0.126s client total  | 0.119s API processing
```

The first run includes cold-start and semantic-model loading overhead.

Warm API processing in runs 2 and 3 was approximately:

```
0.119s - 0.134s
```

## Estimated Variable Cost

The current text-PDF workflow does not use a paid external AI API.

Semantic matching uses the locally running:

```
sentence-transformers/all-MiniLM-L6-v2
```

No paid speech recognition, speech generation, OCR, or external reasoning API is used in the current workflow.

Estimated third-party/API variable cost per document pair:

```
$0.00
```

This excludes hosting and local computing/infrastructure costs.

## Limitations

The current prototype does not include:

* User accounts
* Payments
* Permanent document storage
* OCR for scanned documents
* Handwritten-document recognition
* Speech or voice input
* Video processing
* Multi-currency conversion
* Production authentication
* Production-grade cloud infrastructure

These are outside the current prototype scope.

## Development Approach

The prototype prioritizes correctness and traceability over visual complexity.

The comparison process separates:

1. Document extraction
2. Structured parsing
3. Semantic matching
4. Deterministic calculations
5. Change classification
6. Source-evidence presentation

This separation makes the system easier to test and reduces the risk of semantic reasoning affecting financial calculations.

## Ownership

Lawrean Kompa and its source code were developed as part of the product-builder assignment.

This project and its code remain the property of Lawrence Pro Mada.
