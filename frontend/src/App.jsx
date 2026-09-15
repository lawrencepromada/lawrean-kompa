import { useState } from "react";

function App() {
  const [originalFile, setOriginalFile] = useState(null);
  const [revisedFile, setRevisedFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function compareOffers() {
    if (!originalFile || !revisedFile) {
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    const formData = new FormData();
    formData.append("original", originalFile);
    formData.append("revised", revisedFile);

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"}/compare`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Comparison failed."
        );
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function money(value) {
    if (value === null || value === undefined) {
      return "—";
    }

    const currency = result?.currency || "";
    const amount = Number(value).toLocaleString();

    return currency + " " + amount;
  }

  function matchLabel(status) {
    if (status === "confirmed") {
      return "Confirmed";
    }

    if (status === "uncertain") {
      return "Needs review";
    }

    if (status === "removed") {
      return "Removed";
    }

    if (status === "added") {
      return "Added";
    }

    return status;
  }

  const clarificationChanges =
    result?.changes.filter(
      (change) =>
        change.change_type === "needs_clarification"
    ) || [];

  const clarificationCount =
    clarificationChanges.length;

  const hasClarification =
    clarificationCount > 0;

  return (
    <main className="app">
      {!result && (
        <>
          <section className="hero">
            <p className="eyebrow">LAWREAN KOMPA</p>

            <h1>
              Compare commercial offers without the
              guesswork.
            </h1>

            <p className="subtitle">
              Upload an original offer and its revision.
              Lawrean Kompa identifies commercial changes
              and shows where each change came from.
            </p>
          </section>

          <section className="upload-panel">
            <div className="file-card">
              <h2>Original offer</h2>

              <p>
                The earlier version of the commercial
                offer.
              </p>

              <label className="upload-button">
                Choose PDF

                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={(event) => {
                    setOriginalFile(
                      event.target.files[0] || null
                    );
                  }}
                />
              </label>

              {originalFile && (
                <p className="file-name">
                  {originalFile.name}
                </p>
              )}
            </div>

            <div className="file-card">
              <h2>Revised offer</h2>

              <p>
                The newer version you want to compare.
              </p>

              <label className="upload-button">
                Choose PDF

                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={(event) => {
                    setRevisedFile(
                      event.target.files[0] || null
                    );
                  }}
                />
              </label>

              {revisedFile && (
                <p className="file-name">
                  {revisedFile.name}
                </p>
              )}
            </div>
          </section>

          <button
            className="compare-button"
            disabled={
              !originalFile ||
              !revisedFile ||
              loading
            }
            onClick={compareOffers}
          >
            {loading ? "Comparing..." : "Compare offers"}
          </button>

          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

          <p className="limits">
            PDF only · Maximum 3 pages · Maximum 10
            line items
          </p>
        </>
      )}

      {result && (
        <section className="results">
          <div className="results-header">
            <div>
              <p className="eyebrow">LAWREAN KOMPA</p>

              <h1>Comparison results</h1>

              <p className="subtitle">
                {result.changes.length} changes detected.
                {hasClarification &&
                  ` ${clarificationCount} requires clarification.`}
              </p>
            </div>

            <button
              className="secondary-button"
              onClick={() => setResult(null)}
            >
              Compare another pair
            </button>
          </div>

          <section className="summary-grid">
            <div className="summary-card">
              <span>Changes</span>
              <strong>
                {result.changes.length}
              </strong>
            </div>

            <div className="summary-card">
              <span>Confirmed matches</span>
              <strong>
                {
                  result.matches.filter(
                    (match) =>
                      match.status === "confirmed"
                  ).length
                }
              </strong>
            </div>

            <div className="summary-card">
              <span>Warnings</span>
              <strong>
                {
                  result.changes.filter(
                    (change) =>
                      change.severity === "warning"
                  ).length
                }
              </strong>
            </div>

            <div className="summary-card">
              <span>Currency</span>
              <strong>
                {result.currency || "—"}
              </strong>
            </div>
          </section>

          {hasClarification && (
            <section className="results-card">
              <h2>Needs clarification</h2>

              <p>
                Lawrean Kompa could not confidently
                determine one or more item correspondences.
                No unsupported removal or addition
                conclusion was made.
              </p>
            </section>
          )}

          <section className="results-card">
            <h2>Total check</h2>

            <div className="totals-grid">
              <div>
                <span>Original stated</span>
                <strong>
                  {money(
                    result.original_stated_total
                  )}
                </strong>
              </div>

              <div>
                <span>Original calculated</span>
                <strong>
                  {money(
                    result.original_calculated_total
                  )}
                </strong>
              </div>

              <div>
                <span>Revised stated</span>
                <strong>
                  {money(
                    result.revised_stated_total
                  )}
                </strong>
              </div>

              <div>
                <span>Revised calculated</span>
                <strong>
                  {money(
                    result.revised_calculated_total
                  )}
                </strong>
              </div>
            </div>
          </section>

          <section className="changes-section">
            <h2>Detected changes</h2>

            {result.changes.map((change, index) => (
              <article
                className="change-card"
                key={index}
              >
                <div className="change-header">
                  <span className="change-type">
                    {change.change_type}
                  </span>

                  <span
                    className={
                      "severity " + change.severity
                    }
                  >
                    {change.severity}
                  </span>
                </div>

                <h3>{change.description}</h3>

                {change.change_type ===
                "arithmetic_discrepancy" ? (
                  <div className="values">
                    <div>
                      <span>Stated total</span>
                      <strong>
                        {money(change.original_value)}
                      </strong>
                    </div>

                    <div>
                      <span>Calculated total</span>
                      <strong>
                        {money(change.revised_value)}
                      </strong>
                    </div>
                  </div>
                ) : (
                  <div className="values">
                    <div>
                      <span>Original</span>
                      <strong>
                        {change.original_value || "—"}
                      </strong>
                    </div>

                    <div>
                      <span>Revised</span>
                      <strong>
                        {change.revised_value || "—"}
                      </strong>
                    </div>
                  </div>
                )}

                {(change.original_source ||
                  change.revised_source) && (
                  <details>
                    <summary>
                      View source evidence
                    </summary>

                    <div className="sources">
                      {change.original_source && (
                        <div className="source">
                          <strong>
                            Original · Page{" "}
                            {
                              change.original_source
                                .page
                            }
                          </strong>

                          <p>
                            {
                              change.original_source
                                .text
                            }
                          </p>
                        </div>
                      )}

                      {change.revised_source && (
                        <div className="source">
                          <strong>
                            Revised · Page{" "}
                            {
                              change.revised_source
                                .page
                            }
                          </strong>

                          <p>
                            {
                              change.revised_source
                                .text
                            }
                          </p>
                        </div>
                      )}
                    </div>
                  </details>
                )}
              </article>
            ))}
          </section>

          <section className="matches-section">
            <h2>Item matching</h2>

            {hasClarification &&
              clarificationChanges.map(
                (change, index) => {
                  const clarificationMatch =
                    result.matches.find(
                      (match) =>
                        match.status === "removed" &&
                        match.original_index !== null
                    );

                  const confidence =
                    clarificationMatch
                      ? Math.round(
                          clarificationMatch.confidence *
                            100
                        )
                      : null;

                  return (
                    <div
                      className="match-row"
                      key={"clarification-" + index}
                    >
                      <span>
                        Needs clarification
                      </span>

                      <p>
                        <strong>
                          {change.original_value}
                        </strong>

                        {" ↕ "}

                        <strong>
                          {change.revised_value}
                        </strong>

                        <br />

                        The system could not safely
                        determine whether these items
                        correspond.
                      </p>

                      {confidence !== null && (
                        <strong>
                          {confidence}%
                        </strong>
                      )}
                    </div>
                  );
                }
              )}

            {result.matches
              .filter(
                (match) =>
                  !(
                    hasClarification &&
                    (
                      match.status === "removed" ||
                      match.status === "added"
                    )
                  )
              )
              .map((match, index) => (
                <div
                  className="match-row"
                  key={"match-" + index}
                >
                  <span>
                    {matchLabel(match.status)}
                  </span>

                  <p>{match.reason}</p>

                  {match.status === "confirmed" ||
                  match.status === "uncertain" ? (
                    <strong>
                      {Math.round(
                        match.confidence * 100
                      )}
                      %
                    </strong>
                  ) : (
                    <strong>—</strong>
                  )}
                </div>
              ))}

            {result.matches.length === 0 && (
              <p>No item matches were found.</p>
            )}
          </section>
        </section>
      )}
    </main>
  );
}

export default App;