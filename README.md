# Lawrean Kompa

Lawrean Kompa is a browser-based prototype for comparing two versions of a commercial offer PDF and identifying substantive changes between them.

The prototype is designed for text-based commercial offer PDFs and focuses on reliable comparison of item descriptions, quantities, unit prices, totals, delivery dates, and arithmetic discrepancies.

## Public Demo

**Frontend:**
https://frontend-ten-gamma-54.vercel.app

**Backend API:**
https://lawrean-kompa.vercel.app

**Source Code:**
https://github.com/lawrencepromada/lawrean-kompa

## Core Workflow

1. Upload the original commercial offer PDF.
2. Upload the revised commercial offer PDF.
3. Extract structured information from both documents.
4. Match corresponding line items even when rows have been renamed or reordered.
5. Detect substantive commercial changes.
6. Recalculate totals deterministically.
7. Identify discrepancies between stated and calculated totals.
8. Flag uncertain or unresolvable matches instead of making unsupported conclusions.
9. Show source evidence from both documents for detected changes.

## Architecture

```text
Browser
   ↓
React + Vite frontend
   ↓
FastAPI backend
   ↓
PyMuPDF PDF extraction
   ↓
Structured document parsing
   ↓
Semantic item matching
   ↓
Deterministic comparison and calculation
   ↓
Results with source evidence
```

The frontend and backend are deployed as separate Vercel projects.

## Important Design Decision

Semantic reasoning is used only where interpretation is required, mainly for determining whether differently named line items may represent the same commercial item.

Arithmetic and commercial calculations are handled deterministically in Python.

The system does not allow a language model or embedding model to silently calculate or replace financial values.

## Source Evidence

Every reported substantive change references the relevant source location in the original and revised documents where applicable.

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
* FastEmbed
* NumPy
* pytest

### Semantic Matching

The prototype uses:

`sentence-transformers/all-MiniLM-L6-v2`

through **FastEmbed** for local embedding generation.

The same model is used to calculate semantic similarity between line-item descriptions. Matching thresholds classify results as confirmed, uncertain, or unresolved.

The deployment version uses FastEmbed/ONNX rather than the larger PyTorch-based Sentence Transformers runtime. This keeps the deployment substantially lighter while retaining the required semantic matching workflow.

## Project Structure

```text
lawrean_kompa/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── pdf_extractor.py
│   │   ├── parser.py
│   │   ├── matcher.py
│   │   ├── matcher_fast.py
│   │   └── comparator.py
│   ├── tests/
│   │   ├── test_models.py
│   │   ├── test_pdf_extractor.py
│   │   ├── test_parser.py
│   │   ├── test_matcher.py
│   │   ├── test_comparator.py
│   │   ├── test_calculator.py
│   │   └── test_evaluation.py
│   ├── calculator.py
│   ├── measure_timing.py
│   ├── requirements.txt
│   └── requirements-local.txt
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
├── README.md
├── DELIVERY_NOTES.md
├── Dockerfile
└── .vercelignore
```

## Running Locally

### Backend

Open Command Prompt:

```cmd
cd /d D:\Lawrean\lawrean_kompa\backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

### Frontend

Open a second Command Prompt window:

```cmd
cd /d D:\Lawrean\lawrean_kompa\frontend
npm run dev
```

The frontend normally runs at:

```text
http://localhost:5173
```

The frontend uses the `VITE_API_URL` environment variable when deployed. If the variable is not set, it falls back to the local FastAPI address.

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

The backend includes unit tests and a reproducible evaluation test set.

Run the complete test suite:

```cmd
cd /d D:\Lawrean\lawrean_kompa\backend
.venv\Scripts\activate
pytest -q
```

Final result:

```text
12 passed


## Evaluation Scenarios

The reproducible evaluation set contains four scenarios.

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

Result:

* Expected substantive changes: detected
* Changes reported: 8
* Arithmetic discrepancy: detected
* Source evidence: provided

### 2. Ambiguous Match

Tests a renamed item where semantic similarity is not high enough for a confident match.

Result:

* Match is marked **Needs review**
* No unsupported commercial change is inferred from the uncertain match

### 3. Formatting Only

Tests visual and formatting changes without changing commercial meaning.

Result:

* 0 substantive changes
* 5 confirmed matches

### 4. Unresolvable Match

Tests two items where the system cannot safely determine whether they correspond.

Result:

* The system displays **Needs clarification**
* It does not incorrectly report the original item as removed and the revised item as added

## Final Evaluation Result

```text
Expected-change scenarios: 3
Detected-change scenarios: 3
False-change scenarios: 0
Missed-change scenarios: 0
Source references valid: 10/10
Source-reference accuracy: 100.0%
```

The evaluation was run against the reproducible sample-data scenarios rather than hard-coded answers in the application.

## Deterministic Calculation

For each line item, the system calculates:

```text
quantity × unit price = calculated line total
```

It compares the calculated value with the stated line total.

For the offer:

```text
sum of calculated line totals = calculated grand total
```

The calculated grand total is then compared with the stated grand total.

The system reports discrepancies rather than silently replacing the source value.

For example, in the normal revision scenario:

```text
Revised stated total:     USD 6,390
Revised calculated total: USD 6,490
Difference:               USD 100
```

The source-stated value remains visible while the calculated value is shown separately.

## Measured Processing Time

A three-run timing test was performed using the normal revision scenario.

```text
Run 1: 21.997s client total | 7.742s API processing
Run 2:  0.141s client total | 0.134s API processing
Run 3:  0.126s client total | 0.119s API processing
```

The first run includes cold-start and semantic-model loading overhead.

Warm API processing in runs 2 and 3 was approximately:

```text
0.119s - 0.134s
```

The timing test measures client/API processing rather than a separately instrumented user-visible result-rendering duration.

## AI Tools and Models

The prototype does not use a paid external reasoning API.

Semantic matching uses:

```text
FastEmbed
sentence-transformers/all-MiniLM-L6-v2
```

The embedding model is used only for semantic similarity between line-item descriptions.

Financial calculations, totals, discrepancy detection, and change classification are performed by deterministic application code.

## Estimated Variable Cost

The current workflow does not use a paid external AI API.

There is no paid:

* LLM API
* OCR API
* speech recognition API
* speech generation API
* external reasoning API

Estimated third-party/API variable cost per document pair:

```text
$0.00
```

This excludes hosting and local/cloud computing infrastructure costs.

## Deployment

The final prototype is deployed as two Vercel projects:

```text
React/Vite frontend
        ↓
https://frontend-ten-gamma-54.vercel.app
        ↓
FastAPI backend
        ↓
https://lawrean-kompa.vercel.app
```

The backend uses FastEmbed for semantic matching to avoid the large deployment footprint associated with the PyTorch-based Sentence Transformers runtime.

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
