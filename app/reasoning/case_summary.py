from enum import Enum


class CaseSummaryStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    CONFLICTING = "CONFLICTING"
    HISTORICAL = "HISTORICAL"
    UNCERTAIN = "UNCERTAIN"
    MIXED = "MIXED"
    INCONCLUSIVE = "INCONCLUSIVE"


def determine_case_summary(claims) -> CaseSummaryStatus:
    if not claims:
        return CaseSummaryStatus.INCONCLUSIVE

    statuses = {claim.status.value for claim in claims}

    if "CONFLICTING" in statuses:
        return CaseSummaryStatus.CONFLICTING

    if statuses == {"HISTORICAL"}:
        return CaseSummaryStatus.HISTORICAL

    if statuses == {"UNCERTAIN"}:
        return CaseSummaryStatus.UNCERTAIN

    if "MIXED" in statuses:
        return CaseSummaryStatus.MIXED

    if "SUPPORTED" in statuses and "UNCERTAIN" in statuses:
        return CaseSummaryStatus.MIXED

    if len(statuses) > 1:
        return CaseSummaryStatus.MIXED

    if statuses == {"SUPPORTED"}:
        return CaseSummaryStatus.SUPPORTED

    return CaseSummaryStatus.INCONCLUSIVE
