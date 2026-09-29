from app.pipeline import analyze_case


def test_explanation_describes_temporal_distinction():
    result = analyze_case(
        "X001",
        "My father used to struggle to walk, but now he has trouble walking.",
    )

    assert result.explanation

    explanation = "\n".join(result.explanation)

    assert "TEMPORALLY_DISTINCT" in explanation
    assert "HISTORICAL" in explanation
    assert "CURRENT" in explanation


def test_explanation_describes_contradiction_with_context():
    result = analyze_case(
        "X002",
        "My father struggles to walk. "
        "He does not struggle to walk.",
    )

    explanation = "\n".join(result.explanation)

    assert "CONTRADICTS" in explanation
    assert "DIRECT" in explanation
    assert "CONTRADICTED" in explanation


def test_explanation_describes_supporting_evidence():
    result = analyze_case(
        "X003",
        "My father struggles to walk. "
        "He may have difficulty walking.",
    )

    explanation = "\n".join(result.explanation)

    assert "SUPPORTS" in explanation
    assert "DIRECT" in explanation
    assert "INFERRED" in explanation
