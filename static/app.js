const analyzeButton = document.getElementById("analyzeButton");
const results = document.getElementById("results");
const errorBox = document.getElementById("error");

analyzeButton.addEventListener("click", analyzeCase);

async function analyzeCase() {
    const caseId = document.getElementById("caseId").value.trim();
    const narrative = document.getElementById("narrative").value.trim();

    errorBox.classList.add("hidden");
    results.classList.add("hidden");

    if (!caseId || !narrative) {
        showError("Please enter both a case ID and a narrative.");
        return;
    }

    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analyzing...";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                case_id: caseId,
                narrative: narrative
            })
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const data = await response.json();

        displayResults(data);

    } catch (error) {
        showError("Unable to analyze the case. Make sure the API is running.");
        console.error(error);
    } finally {
        analyzeButton.disabled = false;
        analyzeButton.textContent = "Analyze Case";
    }
}

function displayResults(data) {
    results.classList.remove("hidden");

    const summary = data.summary || "INCONCLUSIVE";

    document.getElementById("summaryStatus").textContent = summary;

    const claims = data.claims || [];
    const evidence = data.case?.evidence || [];
    const relationships = data.relationships || [];

    document.getElementById("claimCount").textContent =
        `${claims.length} claim${claims.length === 1 ? "" : "s"}`;

    document.getElementById("evidenceCount").textContent =
        `${evidence.length} item${evidence.length === 1 ? "" : "s"}`;

    renderClaims(claims, evidence);
    renderEvidence(evidence);
    renderRelationships(relationships);
    renderExplanation(data.explanation || []);
}

function renderClaims(claims, evidence) {
    const container = document.getElementById("claims");

    if (!claims.length) {
        container.innerHTML = "<p>No claims identified.</p>";
        return;
    }

    const evidenceById = new Map(
        evidence.map(item => [item.evidence_id, item])
    );

    container.innerHTML = claims.map(claim => {
        const linkedEvidence = (claim.evidence_ids || [])
            .map(id => evidenceById.get(id))
            .filter(Boolean);

        return `
            <div class="claim">
                <div class="claim-text">
                    ${escapeHtml(claim.claim)}
                </div>

                <div class="meta">
                    <span class="badge">
                        Status: ${escapeHtml(claim.status)}
                    </span>

                    <span class="badge">
                        Domain: ${escapeHtml(claim.functional_domain)}
                    </span>

                    <span class="badge">
                        Confidence: ${escapeHtml(String(claim.confidence))}
                    </span>
                </div>

                <div class="claim-trace">
                    <div class="trace-title">
                        Evidence for this claim
                    </div>

                    ${
                        linkedEvidence.length
                            ? linkedEvidence.map(item => `
                                <div class="trace-item">
                                    <div class="trace-header">
                                        <strong>
                                            ${escapeHtml(item.evidence_id)}
                                        </strong>

                                        <span class="badge">
                                            ${escapeHtml(item.evidence_type)}
                                        </span>
                                    </div>

                                    <div class="trace-text">
                                        "${escapeHtml(item.text_span)}"
                                    </div>

                                    <div class="trace-source">
                                        Source: ${escapeHtml(item.source_text)}
                                    </div>

                                    <div class="meta">
                                        <span class="badge">
                                            ${escapeHtml(item.temporal_status)}
                                        </span>

                                        <span class="badge">
                                            ${escapeHtml(item.functional_domain)}
                                        </span>

                                        <span class="badge">
                                            Confidence:
                                            ${escapeHtml(String(item.confidence))}
                                        </span>
                                    </div>
                                </div>
                            `).join("")
                            : "<p class=\"trace-empty\">No linked evidence.</p>"
                    }
                </div>
            </div>
        `;
    }).join("");
}

function renderEvidence(evidence) {
    const container = document.getElementById("evidence");

    if (!evidence.length) {
        container.innerHTML = "<p>No evidence identified.</p>";
        return;
    }

    container.innerHTML = evidence.map(item => `
        <div class="evidence-item">
            <div class="evidence-header">
                <strong>${escapeHtml(item.evidence_id)}</strong>
            </div>

            <div class="evidence-text">
                "${escapeHtml(item.text_span)}"
            </div>

            <div class="evidence-source">
                Source: ${escapeHtml(item.source_text)}
            </div>

            <div class="meta">
                <span class="badge">
                    ${escapeHtml(item.evidence_type)}
                </span>

                <span class="badge">
                    ${escapeHtml(item.temporal_status)}
                </span>

                <span class="badge">
                    ${escapeHtml(item.functional_domain)}
                </span>

                <span class="badge">
                    Confidence: ${escapeHtml(String(item.confidence))}
                </span>
            </div>
        </div>
    `).join("");
}

function renderRelationships(relationships) {
    const container = document.getElementById("relationships");

    if (!container) {
        return;
    }

    if (!relationships.length) {
        container.innerHTML = "<p>No evidence relationships identified.</p>";
        return;
    }

    container.innerHTML = relationships.map(item => `
        <div class="relationship-item">
            <div class="relationship-node">
                ${escapeHtml(item.source_evidence_id)}
            </div>

            <div class="relationship-arrow">
                ${escapeHtml(item.relationship)}
            </div>

            <div class="relationship-node">
                ${escapeHtml(item.target_evidence_id)}
            </div>
        </div>
    `).join("");
}

function showError(message) {
    errorBox.textContent = message;
    errorBox.classList.remove("hidden");
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderExplanation(explanation) {
    const container = document.getElementById("explanation");

    if (!container) {
        return;
    }

    if (!explanation.length) {
        container.innerHTML = "<p>No explanation available.</p>";
        return;
    }

    container.innerHTML = explanation.map((item, index) => `
        <div class="explanation-item">
            <span class="explanation-number">${index + 1}</span>
            <span class="explanation-text">
                ${escapeHtml(item)}
            </span>
        </div>
    `).join("");
}

