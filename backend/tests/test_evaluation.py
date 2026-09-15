import json
from pathlib import Path

from app.comparator import compare_offers
from app.parser import parse_offer
from app.pdf_extractor import extract_pages


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DATA = ROOT / "sample-data"


def load_offer(filename: str):
    pdf_path = SAMPLE_DATA / filename
    locations = extract_pages(str(pdf_path))
    return parse_offer(filename, locations)


def load_expected_results():
    path = SAMPLE_DATA / "expected-results.json"

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_evaluation_set():
    expected_results = load_expected_results()

    for scenario_name, scenario in expected_results.items():
        original = load_offer(scenario["original"])
        revised = load_offer(scenario["revised"])

        result = compare_offers(original, revised)
        expected = scenario["expected"]

        uncertain_matches = sum(
            match.status == "uncertain"
            for match in result.matches
        )

        reported_removed_items = sum(
            change.change_type == "item_removed"
            for change in result.changes
        )

        reported_added_items = sum(
            change.change_type == "item_added"
            for change in result.changes
        )

        needs_clarification = any(
            change.change_type == "needs_clarification"
            for change in result.changes
        )

        arithmetic_discrepancy = any(
            change.change_type == "arithmetic_discrepancy"
            for change in result.changes
        )

        if "substantive_changes" in expected:
            assert (
                len(result.changes) > 0
            ) == expected["substantive_changes"], (
                f"{scenario_name}: unexpected substantive-change result"
            )

        if "change_count" in expected:
            assert (
                len(result.changes)
                == expected["change_count"]
            ), (
                f"{scenario_name}: unexpected change count"
            )

        if "uncertain_matches" in expected:
            assert (
                uncertain_matches
                == expected["uncertain_matches"]
            ), (
                f"{scenario_name}: unexpected uncertain-match count"
            )

        if "removed_items" in expected:
            assert (
                reported_removed_items
                == expected["removed_items"]
            ), (
                f"{scenario_name}: unexpected reported removed-item count"
            )

        if "added_items" in expected:
            assert (
                reported_added_items
                == expected["added_items"]
            ), (
                f"{scenario_name}: unexpected reported added-item count"
            )

        if "needs_clarification" in expected:
            assert (
                needs_clarification
                == expected["needs_clarification"]
            ), (
                f"{scenario_name}: unexpected clarification result"
            )

        if "original_calculated_total" in expected:
            assert (
                result.original_calculated_total
                == expected["original_calculated_total"]
            ), (
                f"{scenario_name}: unexpected original calculated total"
            )

        if "revised_calculated_total" in expected:
            assert (
                result.revised_calculated_total
                == expected["revised_calculated_total"]
            ), (
                f"{scenario_name}: unexpected revised calculated total"
            )

        if "original_stated_total" in expected:
            assert (
                result.original_stated_total
                == expected["original_stated_total"]
            ), (
                f"{scenario_name}: unexpected original stated total"
            )

        if "revised_stated_total" in expected:
            assert (
                result.revised_stated_total
                == expected["revised_stated_total"]
            ), (
                f"{scenario_name}: unexpected revised stated total"
            )

        if "arithmetic_discrepancy" in expected:
            assert (
                arithmetic_discrepancy
                == expected["arithmetic_discrepancy"]
            ), (
                f"{scenario_name}: unexpected arithmetic discrepancy"
            )


def test_all_substantive_changes_have_source_evidence():
    expected_results = load_expected_results()

    for scenario_name, scenario in expected_results.items():
        original = load_offer(scenario["original"])
        revised = load_offer(scenario["revised"])

        result = compare_offers(original, revised)

        for change in result.changes:
            if change.change_type == "item_added":
                assert change.revised_source is not None, (
                    f"{scenario_name}: added item has no revised source"
                )

            elif change.change_type == "item_removed":
                assert change.original_source is not None, (
                    f"{scenario_name}: removed item has no original source"
                )

            elif change.change_type == "arithmetic_discrepancy":
                assert (
                    change.original_source is not None
                    or change.revised_source is not None
                ), (
                    f"{scenario_name}: arithmetic discrepancy has no source"
                )

            elif change.change_type == "needs_clarification":
                assert change.original_source is not None, (
                    f"{scenario_name}: clarification has no original source"
                )

                assert change.revised_source is not None, (
                    f"{scenario_name}: clarification has no revised source"
                )

            else:
                assert change.original_source is not None, (
                    f"{scenario_name}: change has no original source"
                )

                assert change.revised_source is not None, (
                    f"{scenario_name}: change has no revised source"
                )


def test_evaluation_accuracy_report():
    expected_results = load_expected_results()

    total_expected_changes = 0
    total_detected_changes = 0
    false_changes = 0
    missed_changes = 0

    total_changes_requiring_evidence = 0
    changes_with_valid_evidence = 0

    for scenario_name, scenario in expected_results.items():
        original = load_offer(scenario["original"])
        revised = load_offer(scenario["revised"])

        result = compare_offers(original, revised)

        expected = scenario["expected"]

        expected_substantive = expected.get(
            "substantive_changes",
            False,
        )

        detected_substantive = len(result.changes) > 0

        if expected_substantive:
            total_expected_changes += 1

        if detected_substantive:
            total_detected_changes += 1

        if detected_substantive and not expected_substantive:
            false_changes += 1

        if expected_substantive and not detected_substantive:
            missed_changes += 1

        for change in result.changes:
            total_changes_requiring_evidence += 1

            if change.change_type == "item_added":
                evidence_valid = (
                    change.revised_source is not None
                )

            elif change.change_type == "item_removed":
                evidence_valid = (
                    change.original_source is not None
                )

            elif change.change_type == "arithmetic_discrepancy":
                evidence_valid = (
                    change.original_source is not None
                    or change.revised_source is not None
                )

            elif change.change_type == "needs_clarification":
                evidence_valid = (
                    change.original_source is not None
                    and change.revised_source is not None
                )

            else:
                evidence_valid = (
                    change.original_source is not None
                    and change.revised_source is not None
                )

            if evidence_valid:
                changes_with_valid_evidence += 1

        print(
            f"\n[{scenario_name}]"
            f"\n  Expected substantive changes: "
            f"{expected_substantive}"
            f"\n  Detected substantive changes: "
            f"{detected_substantive}"
            f"\n  Changes reported: "
            f"{len(result.changes)}"
        )

    source_reference_accuracy = (
        (
            changes_with_valid_evidence
            / total_changes_requiring_evidence
        )
        * 100
        if total_changes_requiring_evidence
        else 100
    )

    print("\n=== Evaluation Accuracy ===")

    print(
        f"Expected-change scenarios: "
        f"{total_expected_changes}"
    )

    print(
        f"Detected-change scenarios: "
        f"{total_detected_changes}"
    )

    print(
        f"False-change scenarios: "
        f"{false_changes}"
    )

    print(
        f"Missed-change scenarios: "
        f"{missed_changes}"
    )

    print(
        f"Source references valid: "
        f"{changes_with_valid_evidence}/"
        f"{total_changes_requiring_evidence}"
    )

    print(
        f"Source-reference accuracy: "
        f"{source_reference_accuracy:.1f}%"
    )

    assert false_changes == 0
    assert missed_changes == 0
    assert (
        changes_with_valid_evidence
        == total_changes_requiring_evidence
    )