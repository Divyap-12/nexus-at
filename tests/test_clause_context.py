from app.pipeline import _split_sentences


def test_but_splits_clauses():
    result = _split_sentences(
        "My father does not have trouble walking, "
        "but he plans to use a wheelchair."
    )

    assert result == [
        "My father does not have trouble walking,",
        "he plans to use a wheelchair",
    ]


def test_but_split_preserves_historical_and_current_clauses():
    result = _split_sentences(
        "My father used to struggle to walk, "
        "but now he has trouble walking."
    )

    assert result == [
        "My father used to struggle to walk,",
        "now he has trouble walking",
    ]


def test_and_keeps_related_facts_in_same_clause():
    result = _split_sentences(
        "My father has trouble walking and uses a walking stick."
    )

    assert result == [
        "My father has trouble walking and uses a walking stick"
    ]
