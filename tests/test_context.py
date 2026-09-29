from app.extraction.context import (
    ContextType,
    detect_context,
    detect_temporal_context,
)


def test_negated_context():
    assert (
        detect_context("My father does not have trouble walking.")
        == ContextType.NEGATED
    )


def test_uncertain_context():
    assert (
        detect_context("My father might have trouble walking.")
        == ContextType.UNCERTAIN
    )


def test_historical_context():
    assert (
        detect_context("My father used to struggle to walk.")
        == ContextType.HISTORICAL
    )


def test_planned_context():
    assert (
        detect_context("My father plans to use a walking stick.")
        == ContextType.PLANNED
    )


def test_historical_negated_context_keeps_negation_polarity():
    assert (
        detect_context(
            "My father previously did not have trouble walking."
        )
        == ContextType.NEGATED
    )


def test_historical_negated_context_keeps_historical_temporal_status():
    assert (
        detect_temporal_context(
            "My father previously did not have trouble walking."
        )
        == ContextType.HISTORICAL
    )


def test_uncertain_negated_context_keeps_negation_polarity():
    assert (
        detect_context(
            "My father might not have trouble walking."
        )
        == ContextType.NEGATED
    )


def test_uncertain_negated_context_keeps_current_temporal_status():
    assert (
        detect_temporal_context(
            "My father might not have trouble walking."
        )
        == ContextType.CURRENT
    )


def test_current_context():
    assert (
        detect_context("My father struggles to walk.")
        == ContextType.CURRENT
    )


def test_current_temporal_context():
    assert (
        detect_temporal_context("My father struggles to walk.")
        == ContextType.CURRENT
    )
