from app.extraction.recurrence import is_recurrence


def test_again_marks_recurrence():
    assert is_recurrence("now he struggles again")


def test_normal_current_clause_is_not_recurrence():
    assert not is_recurrence("now he struggles to walk")


def test_again_is_case_insensitive():
    assert is_recurrence("He struggles AGAIN")
