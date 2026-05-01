export default function TripInputBox({ inputText, setInputText, onSubmit, loading }) {
  return (
    <div className="card hero-card">
      <p className="eyebrow">AI Travel Assistant</p>
      <h2>Smart Travel Planner</h2>
      <p className="subtitle">
        Tell us your budget, dates, travel vibe, and activities. We’ll generate a personalized destination plan.
      </p>

      <textarea
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Example: I have 2 weeks in July and around $1500. I want somewhere warm, not too touristy, and I like hiking."
        rows={6}
      />

      <button onClick={onSubmit} disabled={loading}>
        {loading ? "Generating your plan..." : "Generate Travel Plan"}
      </button>
    </div>
  );
}