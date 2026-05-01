export default function TripInputBox({ inputText, setInputText, onSubmit, loading }) {
  return (
    <div className="card">
      <h2>Smart Travel Planner</h2>

      <textarea
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Example: I want somewhere warm, not too touristy, and I like hiking."
        rows={6}
      />

      <button onClick={onSubmit} disabled={loading}>
        {loading ? "Generating..." : "Generate Travel Plan"}
      </button>
    </div>
  );
}