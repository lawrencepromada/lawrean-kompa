# Lawrean Kompa — Delivery Notes

## Submission Overview

Lawrean Kompa is a working browser-based prototype for comparing two versions of a commercial offer PDF and identifying substantive commercial changes.

The final prototype is deployed publicly and can process new uploaded PDF pairs through the deployed application.

## Public Links

**Public frontend:**
https://frontend-ten-gamma-54.vercel.app

**Public backend:**
https://lawrean-kompa.vercel.app

**GitHub repository:**
https://github.com/lawrencepromada/lawrean-kompa

## Implemented Requirements

The prototype supports:

* Original and revised PDF upload
* Text extraction from PDFs
* Structured commercial-item parsing
* Semantic matching of renamed or reordered items
* Quantity comparison
* Unit-price comparison
* Line-total comparison
* Delivery-date comparison
* Added/removed-item handling
* Uncertain-match warnings
* Unresolvable-match clarification
* Deterministic arithmetic validation
* Grand-total discrepancy detection
* Source evidence for reported changes
* Formatting-only detection
* Reproducible evaluation scenarios

The application processes uploaded documents rather than returning hard-coded demonstration results.

## Architecture

```text
Browser
  ↓
React + Vite
  ↓
FastAPI
  ↓
PyMuPDF extraction
  ↓
Structured parser
  ↓
FastEmbed semantic matching
  ↓
Deterministic comparison/calculation
  ↓
Comparison results + source evidence
```

The frontend and backend are deployed separately on Vercel.

## Semantic Matching

The semantic matching implementation uses:

```text
FastEmbed
sentence-transformers/all-MiniLM-L6-v2
```

FastEmbed was used for the deployment implementation to avoid the very large bundle size encountered when attempting to deploy the PyTorch-based Sentence Transformers runtime.

Semantic similarity is used for line-item correspondence only.

The application does not use semantic embeddings to perform financial calculations.

## Deterministic Financial Validation

Financial calculations are performed directly in Python.

For each line item:

```text
quantity × unit price = calculated line total
```

The calculated line totals are summed to produce the calculated grand total.

The system compares calculated values against the values stated in the source documents and reports discrepancies without silently changing the source values.

## Evaluation Dataset

Four reproducible scenarios were created.

### Normal Revision

Tests multiple substantive changes including:

* Renamed item
* Reordered rows
* Quantity change
* Unit-price change
* Removed item
* Delivery-date change
* Incorrect stated grand total
* Arithmetic discrepancy

Actual result:

```text
8 changes detected
```

### Ambiguous Match

Tests a renamed item where semantic similarity is insufficient for a confident correspondence.

Actual result:

```text
1 uncertain match
```

The UI displays this as **Needs review**.

### Formatting Only

Tests changes that affect presentation without changing commercial meaning.

Actual result:

```text
0 substantive changes
5 confirmed matches
```

### Unresolvable Match

Tests two unrelated descriptions where the system cannot safely determine correspondence.

Actual result:

```text
1 clarification required
```

The system does not make an unsupported removed/added conclusion.

## Final Evaluation Accuracy

The evaluation command produced:

```text
Expected-change scenarios: 3
Detected-change scenarios: 3
False-change scenarios: 0
Missed-change scenarios: 0
Source references valid: 10/10
Source-reference accuracy: 100.0%
```

## Automated Tests

The complete backend test suite produced:

```text
12 passed
```

The tests cover the models, extraction, parsing, arithmetic calculations, semantic matching, comparison logic, source evidence, and evaluation scenarios.

## Output-Checking Example

The normal revision scenario provides a concrete output check.

The revised document states:

```text
Grand total: USD 6,390
```

The application independently calculates:

```text
Calculated grand total: USD 6,490
```

The application therefore reports a grand-total arithmetic discrepancy of:

```text
USD 100
```

The original source value is not overwritten.

This demonstrates that the application does not simply trust the stated total and does not use semantic reasoning to perform the arithmetic.

## Source Evidence Validation

Reported substantive changes include source references containing:

* Page number
* Extracted source text
* Bounding-box coordinates when available

Final evaluation:

```text
Source references valid: 10/10
Source-reference accuracy: 100.0%
```

This allows a reviewer to trace reported changes back to the relevant source documents.

## Processing Time

A three-run timing test was performed using the normal revision scenario:

```text
Run 1: 21.997s client total | 7.742s API processing
Run 2:  0.141s client total | 0.134s API processing
Run 3:  0.126s client total | 0.119s API processing
```

The first run includes cold-start and semantic-model loading overhead.

Warm API processing in runs 2 and 3 was:

```text
0.119s - 0.134s
```

The test measures client/API processing and does not separately instrument the time from upload completion to final browser rendering.

## Cost

The current workflow does not use a paid external AI API.

There is no paid external:

* LLM
* OCR service
* speech service
* reasoning API

Semantic matching runs using FastEmbed and the local embedding model.

Estimated third-party/API variable cost per document pair:

```text
$0.00
```

This does not include hosting or computing infrastructure costs.

## Deployment Verification

The public deployment was tested using the actual sample PDFs through the browser.

Verified scenarios:

```text
Normal revision       ✓
Ambiguous match       ✓
Formatting only       ✓
Unresolvable match    ✓
```

The public frontend successfully communicated with the deployed FastAPI backend.

The normal revision produced the expected eight substantive changes and arithmetic discrepancy.

The ambiguous scenario produced a needs-review warning.

The formatting-only scenario produced zero substantive changes.

The unresolvable scenario produced a needs-clarification result without an unsupported removal/addition conclusion.

## Input Constraints

Current prototype limits:

* PDF only
* Text-based PDFs
* Maximum 3 pages per document
* Maximum 10 MB per PDF
* One currency per document pair
* Maximum 10 line items

OCR and scanned/handwritten documents are outside the prototype scope.

## Known Limitations

The prototype does not provide:

* User accounts
* Payments
* Permanent document storage
* OCR
* Handwriting recognition
* Voice input
* Video processing
* Currency conversion
* Production authentication
* Production-grade cloud infrastructure

These features were intentionally excluded from the take-home prototype scope.

## Development and Design Principle

The prototype separates interpretation from calculation:

```text
Semantic matching
        ↓
Used only where item correspondence requires interpretation

Deterministic Python calculations
        ↓
Used for quantities, prices, line totals and grand totals

Source evidence
        ↓
Used to make reported changes traceable
```

This separation reduces the risk of an AI/semantic component silently changing financial values.

## Submission Artifacts

The final repository contains:

* Backend application
* Frontend application
* Automated tests
* Evaluation dataset
* Sample PDFs
* Requirements files
* README
* Delivery notes
* Deployment configuration

## Ownership

Lawrean Kompa and its source code were developed as part of the product-builder assignment.

The project and its source code remain the property of Lawrence Pro Mada.

## Final Status

The prototype is complete and publicly deployed.

The GitHub repository is synchronized with the final committed source.

The public browser application has been tested against all four evaluation scenarios.
