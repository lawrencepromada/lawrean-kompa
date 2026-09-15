# Lawrean Kompa — Delivery Notes

## 1. Project Summary

Lawrean Kompa is a browser-based prototype for comparing two versions of a commercial offer PDF and identifying substantive changes.

The prototype extracts structured information from both documents, matches corresponding line items, detects commercial changes, independently recalculates totals, and provides source evidence for reported changes.

The current scope is text-based commercial offer PDFs with a maximum of 3 pages and 10 line items per document.

## 2. Test Inputs

The reproducible test set contains four scenarios:

* Normal revision
* Ambiguous match
* Formatting-only revision
* Unresolvable match

The sample documents and expected outcomes are stored in:

```
sample-data/
```

Expected outcomes are recorded before evaluation in:

```
sample-data/expected-results.json
```

## 3. Expected and Actual Results

### Normal Revision

Expected:

* Detect substantive changes.
* Detect renamed items.
* Detect quantity changes.
* Detect unit-price changes.
* Detect removed items.
* Detect delivery-date changes.
* Detect incorrect stated total.
* Recalculate totals independently.

Actual:

* 8 substantive changes detected.
* 4 confirmed item matches.
* 1 removed item.
* Delivery-date change detected.
* Revised stated total: USD 6,390.
* Revised calculated total: USD 6,490.
* Arithmetic discrepancy: USD 100.

### Ambiguous Match

Expected:

* Detect the substantive difference.
* Avoid treating an uncertain semantic match as confirmed.

Actual:

* 1 change reported.
* 4 confirmed matches.
* 1 match flagged for review.
* Similarity confidence: 47%.

### Formatting Only

Expected:

* Formatting changes should not be reported as substantive commercial changes.

Actual:

* 0 substantive changes reported.
* 5 confirmed matches.
* No arithmetic discrepancy.

### Unresolvable Match

Expected:

* Do not incorrectly conclude that an item was removed or added when correspondence cannot be established.
* Request clarification.

Actual:

* 1 clarification case reported.
* Confidence: approximately 20%.
* No unsupported removal or addition conclusion was made.

## 4. Evaluation Results

The evaluation suite contains three scenarios where substantive changes are expected and one formatting-only scenario where no substantive changes are expected.

Results:

* Expected-change scenarios: 3
* Detected-change scenarios: 3
* False-change scenarios: 0
* Missed-change scenarios: 0
* Detection rate: 100%
* False-change rate: 0%
* Missed-change rate: 0%

## 5. Source-Reference Validation

Every reported change requiring evidence was checked for valid source references.

Results:

* Changes requiring evidence: 10
* Changes with valid evidence: 10
* Invalid or missing evidence: 0
* Source-reference accuracy: 100%

Each source reference contains the document page and extracted source text. Bounding-box coordinates are also retained when available.

## 6. Automated Test Results

The complete backend test suite was executed with pytest.

Result:

```
12 passed
0 failed
```

Pass rate:

```
100%
```

Test execution time:

```
62.17 seconds
```

The evaluation test was also executed independently and completed successfully.

## 7. Processing-Time Measurements

A three-run timing test was performed using the normal revision scenario.

Results:

| Run | Client Total | API Processing |
| --- | -----------: | -------------: |
| 1   |     21.997 s |        7.742 s |
| 2   |      0.141 s |        0.134 s |
| 3   |      0.126 s |        0.119 s |

The first run includes cold-start and semantic-model loading overhead.

Warm API processing for runs 2 and 3 was:

```
0.119 - 0.134 seconds
```

The average client time across all three runs was:

```
7.421 seconds
```

A separate useful-result timer was not instrumented in the application, so no independent useful-result-time figure is claimed.

## 8. AI Tools and Models

The prototype uses the following semantic model:

```
sentence-transformers/all-MiniLM-L6-v2
```

The model runs locally through the sentence-transformers library.

No external OpenAI, Anthropic, Gemini, or other paid reasoning API is used in the current workflow.

Semantic matching is used for determining whether differently described line items may correspond.

Financial calculations are performed deterministically in Python.

## 9. Example of Output Checking

The evaluation process uses a reproducible test set with expected outcomes recorded before testing.

The application output is then compared against those expected outcomes.

For example, the normal revision scenario was expected to contain substantive changes, including quantity, price, delivery-date, removal, and arithmetic changes.

The actual application output detected these changes and independently calculated the revised total as USD 6,490 against the stated USD 6,390, producing the expected USD 100 discrepancy.

The evaluation also checks that reported changes contain valid source evidence.

## 10. Estimated Variable Cost

The current text-PDF workflow uses no paid external AI API.

Estimated third-party/API variable cost per document pair:

```
USD 0.00
```

The current workflow does not use:

* Paid reasoning APIs
* Paid OCR
* Speech recognition
* Speech generation
* Paid intermediaries

The USD 0.00 estimate refers to third-party/API variable charges only. Local computing and future hosting costs are separate.

## 11. Time Spent

Development time is being recorded separately from runtime processing measurements.

The prototype was developed iteratively, including:

* Architecture and scope definition
* Backend implementation
* PDF extraction and parsing
* Deterministic calculation
* Semantic matching
* Comparison logic
* Frontend implementation
* Test fixture creation
* Evaluation
* Timing measurements
* Documentation

Final development time will be recorded after the prototype, deployment, and submission materials are complete.

## 12. Known Limitations

The current prototype does not support:

* Scanned PDFs
* Handwritten documents
* OCR
* Voice input
* Video processing
* User accounts
* Payments
* Permanent document storage
* Production authentication
* Multi-currency conversion
* Production cloud infrastructure

The current parser is designed for the scoped commercial-offer format rather than arbitrary document layouts.

Semantic matching can identify uncertain correspondences, but genuinely unresolvable cases are deliberately surfaced for clarification instead of being forced into a conclusion.

## 13. Failure Handling

The system is designed to avoid silently converting uncertainty into a commercial change.

When item correspondence is uncertain, the application can flag the match for review.

When correspondence cannot be established safely, the application requests clarification rather than incorrectly classifying the item as removed or added.

Arithmetic discrepancies are reported alongside the source-stated values rather than replacing those values.

## 14. Current Status

The prototype currently has:

* Working browser interface
* Working FastAPI backend
* PDF extraction
* Structured parsing
* Semantic line-item matching
* Deterministic calculations
* Change detection
* Source evidence
* Ambiguity handling
* Reproducible test data
* Automated tests
* Evaluation measurements
* Processing-time measurements
* Documentation

Remaining submission work includes browser deployment, repository preparation, and the final demonstration video.

## 15. Submission Artifacts

The intended submission package contains:

* Working browser demo
* Source repository
* README
* Delivery/testing notes
* Sample input PDFs
* Expected-results file
* Automated tests
* Demonstration video

## 16. Ownership

Lawrean Kompa and its source code were developed as part of the product-builder assignment.


