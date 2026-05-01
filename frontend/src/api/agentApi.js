const API_URL = import.meta.env.VITE_API_URL;

export async function runAgent(inputText) {
  const response = await fetch(`${API_URL}/agent/run`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      input_text: inputText,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to generate travel plan");
  }

  return response.json();
}