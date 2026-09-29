from app.extraction.clauses import split_clauses


def test_period_splits_sentences():
    result = split_clauses(
        "My father struggles to walk. He uses a wheelchair."
    )

    assert result == [
        "My father struggles to walk",
        "He uses a wheelchair",
    ]


def test_but_splits_contrasting_clauses():
    result = split_clauses(
        "My father struggles to walk, but he uses a wheelchair."
    )

    assert result == [
        "My father struggles to walk,",
        "he uses a wheelchair",
    ]


def test_and_does_not_split_related_facts():
    result = split_clauses(
        "My father struggles to walk and uses a walking stick."
    )

    assert result == [
        "My father struggles to walk and uses a walking stick",
    ]


def test_historical_and_current_clauses_are_separate():
    result = split_clauses(
        "My father used to struggle to walk, but now he walks normally."
    )

    assert result == [
        "My father used to struggle to walk,",
        "now he walks normally",
    ]


def test_multiple_but_clauses_are_separated():
    result = split_clauses(
        "My father struggles to walk, but he uses a wheelchair, "
        "but he remains independent."
    )

    assert result == [
        "My father struggles to walk,",
        "he uses a wheelchair,",
        "he remains independent",
    ]
