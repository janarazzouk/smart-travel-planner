export default function MissingInfoBox({
  budget,
  setBudget,
  tripDays,
  setTripDays,
  missingBudget,
  missingTripDays,
  onContinue,
  loading,
}) {
  return (
    <div className="card warning">
      <h3>Missing trip details</h3>
      <p>Please add the missing info so we can generate a better plan.</p>

      {missingBudget && (
        <input
          type="number"
          placeholder="Budget in USD"
          value={budget}
          onChange={(e) => setBudget(e.target.value)}
        />
      )}

      {missingTripDays && (
        <input
          type="number"
          placeholder="Trip days"
          value={tripDays}
          onChange={(e) => setTripDays(e.target.value)}
        />
      )}

      <button onClick={onContinue} disabled={loading}>
        {loading ? "Generating..." : "Continue"}
      </button>
    </div>
  );
}