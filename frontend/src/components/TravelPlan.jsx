export default function TravelPlan({ plan }) {
  if (!plan) return null;

  return (
    <div className="card result">
      <h3>Your Travel Plan</h3>
      <p>{plan}</p>
    </div>
  );
}