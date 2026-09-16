import numpy as np
from functools import lru_cache

from fastembed import TextEmbedding

from app.models import LineItem, MatchResult


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CONFIRMED_THRESHOLD = 0.70
UNCERTAIN_THRESHOLD = 0.45


@lru_cache(maxsize=1)
def get_model():
    return TextEmbedding(MODEL_NAME)


def normalize_description(description: str) -> str:
    return " ".join(
        description.lower()
        .strip()
        .split()
    )


def cosine_similarity(a, b) -> float:
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def match_items(
    original_items: list[LineItem],
    revised_items: list[LineItem],
) -> list[MatchResult]:

    if not original_items:
        return [
            MatchResult(
                original_index=None,
                revised_index=index,
                status="added",
                confidence=0.0,
                reason="No corresponding original item was found.",
            )
            for index in range(len(revised_items))
        ]

    if not revised_items:
        return [
            MatchResult(
                original_index=index,
                revised_index=None,
                status="removed",
                confidence=0.0,
                reason="No corresponding revised item was found.",
            )
            for index in range(len(original_items))
        ]

    model = get_model()

    original_descriptions = [
        normalize_description(item.description)
        for item in original_items
    ]

    revised_descriptions = [
        normalize_description(item.description)
        for item in revised_items
    ]

    original_embeddings = list(
        model.embed(original_descriptions)
    )

    revised_embeddings = list(
        model.embed(revised_descriptions)
    )

    results: list[MatchResult] = []
    unused_revised = set(range(len(revised_items)))

    for original_index, original_embedding in enumerate(
        original_embeddings
    ):
        candidates = [
            (
                revised_index,
                cosine_similarity(
                    original_embedding,
                    revised_embeddings[revised_index],
                ),
            )
            for revised_index in unused_revised
        ]

        if not candidates:
            results.append(
                MatchResult(
                    original_index=original_index,
                    revised_index=None,
                    status="removed",
                    confidence=0.0,
                    reason="No corresponding revised item was found.",
                )
            )
            continue

        candidates.sort(
            key=lambda candidate: candidate[1],
            reverse=True,
        )

        revised_index, score = candidates[0]
        score = round(score, 3)

        if score >= CONFIRMED_THRESHOLD:
            status = "confirmed"
            reason = "Descriptions are semantically similar."

        elif score >= UNCERTAIN_THRESHOLD:
            status = "uncertain"
            reason = (
                "Descriptions may refer to the same "
                "commercial item, but the match is uncertain."
            )

        else:
            status = "removed"
            reason = (
                "No sufficiently similar revised item "
                "was found."
            )

        results.append(
            MatchResult(
                original_index=original_index,
                revised_index=(
                    revised_index
                    if status != "removed"
                    else None
                ),
                status=status,
                confidence=score,
                reason=reason,
            )
        )

        if status != "removed":
            unused_revised.remove(revised_index)

    for revised_index in sorted(unused_revised):
        results.append(
            MatchResult(
                original_index=None,
                revised_index=revised_index,
                status="added",
                confidence=0.0,
                reason="No corresponding original item was found.",
            )
        )

    return results