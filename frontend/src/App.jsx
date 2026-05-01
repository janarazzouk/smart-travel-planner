import { useState } from "react";
import { runAgent } from "./api/agentApi";
import TripInputBox from "./components/TripInputBox";
import MissingInfoBox from "./components/MissingInfoBox";
import TravelPlan from "./components/TravelPlan";
import "./index.css";

function hasBudget(text) {
  return /\$?\d+\s*(usd|dollars|\$)?/i.test(text);
}

function hasTripDays(text) {
  return /(\d+)\s*(days?|weeks?)/i.test(text);
}

export default function App() {
  const [inputText, setInputText] = useState("");
  const [budget, setBudget] = useState("");
  const [tripDays, setTripDays] = useState("");
  const [showMissingBox, setShowMissingBox] = useState(false);
  const [plan, setPlan] = useState("");
  const [loading, setLoading] = useState(false);
  const [missingBudget, setMissingBudget] = useState(false);
  const [missingTripDays, setMissingTripDays] = useState(false);

  async function submitToAgent(finalText) {
    setLoading(true);
    setPlan("");

    try {
      const result = await runAgent(finalText);
      setPlan(result.output_text);
      setShowMissingBox(false);
    } catch (error) {
      setPlan("Something went wrong while generating the travel plan.");
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit() {
    const budgetMissing = !hasBudget(inputText);
    const daysMissing = !hasTripDays(inputText);

    setMissingBudget(budgetMissing);
    setMissingTripDays(daysMissing);

    if (budgetMissing || daysMissing) {
      setShowMissingBox(true);
      return;
    }

    submitToAgent(inputText);
  }

  function handleContinue() {
    let finalText = inputText;

    if (missingBudget && budget) {
      finalText += ` My budget is $${budget}.`;
    }

    if (missingTripDays && tripDays) {
      finalText += ` My trip duration is ${tripDays} days.`;
    }

    submitToAgent(finalText);
  }

  return (
    <main className="page">
      <TripInputBox
        inputText={inputText}
        setInputText={setInputText}
        onSubmit={handleSubmit}
        loading={loading}
      />

      {showMissingBox && (
        <MissingInfoBox
            budget={budget}
            setBudget={setBudget}
            tripDays={tripDays}
            setTripDays={setTripDays}
            missingBudget={missingBudget}
            missingTripDays={missingTripDays}
            onContinue={handleContinue}
            loading={loading}
        />
      )}

      <TravelPlan plan={plan} />
    </main>
  );
}