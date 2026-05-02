def build_feature_extraction_prompt(input_text: str) -> str:
    return f"""
Extract travel planning features from this user request.

User request:
{input_text}

Rules:
- budget_usd: extract the total budget in USD if mentioned.
- trip_days: extract trip duration in days. If user says 2 weeks, use 14.
- All score features must be integers from 0 to 5.
- 0 means not requested / not important.
- 2 or 3 = neutral or somewhat important.
- 5 means very important.
- tourism_density:
  - 0 or 1 = wants quiet / not touristy / hidden gems
  - 3 = neutral
  - 5 = wants popular / famous / touristy
- avg_temp_summer_c is only an estimated preference from the text.
  Example: warm = 28, hot = 32, mild = 22, cold = 10.
Do not invent budget or days if missing.
"""


def build_final_answer_prompt(state: dict) -> str:
    return f"""
You are a smart travel planning assistant.

User request:
{state.get("input_text")}

Extracted user info:
- Budget USD: {state.get("budget_usd")}
- Trip days: {state.get("trip_days")}
- ML features: {state.get("features")}

ML predicted travel style:
{state.get("predicted_style")}

Candidate destinations from RAG:
{state.get("destinations")}

Selected destination:
None. You must choose the best destination from the candidates.

Live weather results for candidate destinations:
{state.get("weather_results")}

Errors:
{state.get("errors")}

Write a helpful final travel plan.
Do not just list tool outputs.

Important decision rule:
If the live weather conflicts with the user's preference, explain the conflict and prefer another candidate destination if it is a better match.

Explain:
1. the recommended destination
2. why it matches the user
3. weather situation
4. budget fit
5. other possible options if available

Format the answer as clean plain text.
Do not use Markdown.
Do not use **, #, or bullet symbols.
Keep it clear and not too long.
"""