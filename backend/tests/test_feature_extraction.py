import asyncio

from app.agent.feature_extraction import extract_features_with_gemini


async def main():
    text = (
        "I have 2 weeks off in July and around $1500. "
        "I want somewhere warm, not too touristy, and I like hiking. "
        "I don't care about luxury hotels."
    )

    result = await extract_features_with_gemini(text)

    print("\nExtracted result:")
    print(result)

    print("\nML features:")
    for key, value in result["ml_features"].items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())