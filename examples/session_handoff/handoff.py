"""Fictional, in-memory policy example; not production authentication code."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Review:
    owner: str
    document: str
    revision: int
    open: bool = True


@dataclass(frozen=True)
class Request:
    actor: str
    document: str
    revision: int
    accepted: bool


def baseline_allows(review: Review, request: Request) -> bool:
    """Deliberately incomplete decision rule for the regression demonstration."""
    return (
        review.open
        and request.accepted
        and request.document == review.document
        and request.revision == review.revision
    )


def can_continue(review: Review, request: Request) -> bool:
    """Require evidence AND an authorized actor in this fictional model."""
    return bool(request.actor) and request.actor == review.owner and baseline_allows(review, request)
