from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationCase:
    case_id: str
    narrative: str
    expected_evidence_count: int
    expected_claims: tuple[str, ...]
    expected_temporal_statuses: tuple[str, ...]
    expected_evidence_types: tuple[str, ...]


EVALUATION_CASES = (
    EvaluationCase(
        case_id="EV001",
        narrative="My father struggles to walk.",
        expected_evidence_count=1,
        expected_claims=(
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("CURRENT",),
        expected_evidence_types=("DIRECT",),
    ),

    EvaluationCase(
        case_id="EV002",
        narrative="My father used to struggle to walk.",
        expected_evidence_count=1,
        expected_claims=(
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("HISTORICAL",),
        expected_evidence_types=("DIRECT",),
    ),

    EvaluationCase(
        case_id="EV003",
        narrative="My father may have difficulty walking.",
        expected_evidence_count=1,
        expected_claims=(
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("CURRENT",),
        expected_evidence_types=("INFERRED",),
    ),

    EvaluationCase(
        case_id="EV004",
        narrative="My father does not struggle to walk.",
        expected_evidence_count=1,
        expected_claims=(
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("CURRENT",),
        expected_evidence_types=("CONTRADICTED",),
    ),

    EvaluationCase(
        case_id="EV005",
        narrative="My father is planning to use a wheelchair.",
        expected_evidence_count=1,
        expected_claims=(
            "Person uses a mobility aid.",
        ),
        expected_temporal_statuses=("PLANNED",),
        expected_evidence_types=("DIRECT",),
    ),

    EvaluationCase(
        case_id="EV006",
        narrative="My father struggles to walk. He uses a walking stick.",
        expected_evidence_count=2,
        expected_claims=(
            "Person reports difficulty walking.",
            "Person uses a mobility aid.",
        ),
        expected_temporal_statuses=("CURRENT", "CURRENT"),
        expected_evidence_types=("DIRECT", "DIRECT"),
    ),

    EvaluationCase(
        case_id="EV007",
        narrative="My father used to struggle to walk. He does not struggle to walk.",
        expected_evidence_count=2,
        expected_claims=(
            "Person reports difficulty walking.",
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("HISTORICAL", "CURRENT"),
        expected_evidence_types=("DIRECT", "CONTRADICTED"),
    ),

    EvaluationCase(
        case_id="EV008",
        narrative="My father struggles to walk. He may have difficulty walking.",
        expected_evidence_count=2,
        expected_claims=(
            "Person reports difficulty walking.",
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("CURRENT", "CURRENT"),
        expected_evidence_types=("DIRECT", "INFERRED"),
    ),

    EvaluationCase(
        case_id="EV009",
        narrative="My father struggles to walk. He cannot walk long distances.",
        expected_evidence_count=2,
        expected_claims=(
            "Person reports difficulty walking.",
            "Person has limited walking distance.",
        ),
        expected_temporal_statuses=("CURRENT", "CURRENT"),
        expected_evidence_types=("DIRECT", "DIRECT"),
    ),

    EvaluationCase(
        case_id="EV010",
        narrative="My father enjoys reading newspapers every morning.",
        expected_evidence_count=0,
        expected_claims=(),
        expected_temporal_statuses=(),
        expected_evidence_types=(),
    ),

    EvaluationCase(
        case_id="EV011",
        narrative="Walking has become difficult for my father.",
        expected_evidence_count=1,
        expected_claims=(
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("CURRENT",),
        expected_evidence_types=("DIRECT",),
    ),

    EvaluationCase(
        case_id="EV012",
        narrative="My father cannot walk far without help.",
        expected_evidence_count=1,
        expected_claims=(
            "Person has limited walking distance.",
        ),
        expected_temporal_statuses=("CURRENT",),
        expected_evidence_types=("DIRECT",),
    ),

    EvaluationCase(
        case_id="EV013",
        narrative="My father might have trouble walking.",
        expected_evidence_count=1,
        expected_claims=(
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("CURRENT",),
        expected_evidence_types=("INFERRED",),
    ),

    EvaluationCase(
        case_id="EV014",
        narrative="My father previously struggled to walk.",
        expected_evidence_count=1,
        expected_claims=(
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("HISTORICAL",),
        expected_evidence_types=("DIRECT",),
    ),

    EvaluationCase(
        case_id="EV015",
        narrative="My father plans to use a walking stick.",
        expected_evidence_count=1,
        expected_claims=(
            "Person uses a mobility aid.",
        ),
        expected_temporal_statuses=("PLANNED",),
        expected_evidence_types=("DIRECT",),
    ),

    EvaluationCase(
        case_id="EV016",
        narrative="My father struggles to walk and uses a wheelchair.",
        expected_evidence_count=2,
        expected_claims=(
            "Person reports difficulty walking.",
            "Person uses a mobility aid.",
        ),
        expected_temporal_statuses=("CURRENT", "CURRENT"),
        expected_evidence_types=("DIRECT", "DIRECT"),
    ),

    EvaluationCase(
        case_id="EV017",
        narrative="My father does not use a wheelchair.",
        expected_evidence_count=1,
        expected_claims=(
            "Person uses a mobility aid.",
        ),
        expected_temporal_statuses=("CURRENT",),
        expected_evidence_types=("CONTRADICTED",),
    ),

    EvaluationCase(
        case_id="EV018",
        narrative="My father used to struggle to walk, but now he does not struggle to walk.",
        expected_evidence_count=2,
        expected_claims=(
            "Person reports difficulty walking.",
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("HISTORICAL", "CURRENT"),
        expected_evidence_types=("DIRECT", "CONTRADICTED"),
    ),

    EvaluationCase(
        case_id="EV019",
        narrative="My father enjoys reading books.",
        expected_evidence_count=0,
        expected_claims=(),
        expected_temporal_statuses=(),
        expected_evidence_types=(),
    ),

    EvaluationCase(
        case_id="EV020",
        narrative="My father struggles to walk. He may have difficulty walking. He uses a walking stick.",
        expected_evidence_count=3,
        expected_claims=(
            "Person reports difficulty walking.",
            "Person reports difficulty walking.",
            "Person uses a mobility aid.",
        ),
        expected_temporal_statuses=("CURRENT", "CURRENT", "CURRENT"),
        expected_evidence_types=("DIRECT", "INFERRED", "DIRECT"),
    ),

    EvaluationCase(
        case_id="EV021",
        narrative="My father has trouble walking.",
        expected_evidence_count=1,
        expected_claims=(
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("CURRENT",),
        expected_evidence_types=("DIRECT",),
    ),

    EvaluationCase(
        case_id="EV022",
        narrative="Walking is difficult for my father.",
        expected_evidence_count=1,
        expected_claims=(
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("CURRENT",),
        expected_evidence_types=("DIRECT",),
    ),

    EvaluationCase(
        case_id="EV023",
        narrative="My father finds it hard to walk.",
        expected_evidence_count=1,
        expected_claims=(
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("CURRENT",),
        expected_evidence_types=("DIRECT",),
    ),

    EvaluationCase(
        case_id="EV024",
        narrative="My father does not have trouble walking anymore.",
        expected_evidence_count=1,
        expected_claims=(
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("CURRENT",),
        expected_evidence_types=("CONTRADICTED",),
    ),

    EvaluationCase(
        case_id="EV025",
        narrative="My father might have trouble walking.",
        expected_evidence_count=1,
        expected_claims=(
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("CURRENT",),
        expected_evidence_types=("INFERRED",),
    ),

    EvaluationCase(
        case_id="EV026",
        narrative="My father struggled to walk last year.",
        expected_evidence_count=1,
        expected_claims=(
            "Person reports difficulty walking.",
        ),
        expected_temporal_statuses=("HISTORICAL",),
        expected_evidence_types=("DIRECT",),
    ),

)
