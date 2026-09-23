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

    document.getElementById("relationshipCount").textContent =
        `${relationships.length} relationship${relationships.length === 1 ? "" : "s"}`;

    renderClaims(claims);
    renderEvidence(evidence);
    renderRelationships(relationships);
}

function renderClaims(claims) {
    const container = document.getElementById("claims");

    if (!claims.length) {
        container.innerHTML = "<p>No claims identified.</p>";
        return;
    }

    container.innerHTML = claims.map(claim => `
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
        </div>
    `).join("");
}

function renderEvidence(evidence) {
    const container = document.getElementById("evidence");

    if (!evidence.length) {
        container.innerHTML = "<p>No evidence identified.</p>";
        return;
    }

    container.innerHTML = evidence.map(item => `
        <div class="evidence-item">
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
            </div>
        </div>
    `).join("");
}

function renderRelationships(relationships) {
    const container = document.getElementById("relationships");

    if (!relationships.length) {
        container.innerHTML =
            "<p>No evidence relationships identified.</p>";
        return;
    }

    container.innerHTML = relationships.map(item => `
        <div class="relationship">
            <span class="evidence-node">
                ${escapeHtml(item.source_evidence_id)}
            </span>

            <span class="relationship-arrow">
                ?
            </span>

            <span class="relationship-type">
                ${escapeHtml(item.relationship)}
            </span>

            <span class="relationship-arrow">
                ?
            </span>

            <span class="evidence-node">
                ${escapeHtml(item.target_evidence_id)}
            </span>
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
