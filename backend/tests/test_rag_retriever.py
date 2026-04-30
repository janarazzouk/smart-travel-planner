from app.config import get_settings
from app.rag.embedder import load_embedding_model
from app.rag.retriever import retrieve_destinations_by_style


def main() -> None:
    settings = get_settings()

    print("Loading embedding model...")
    embedder = load_embedding_model(settings.embedding_model)

    travel_style = "Adventure"

    print(f"Retrieving destinations for: {travel_style}")

    results = retrieve_destinations_by_style(
        travel_style=travel_style,
        embedder=embedder,
        chroma_path=settings.chroma_path,
        collection_name=settings.chroma_collection_name,
        top_k=settings.rag_top_k,
    )

    print(f"Results found: {len(results)}")

    for item in results:
        print(item)


if __name__ == "__main__":
    main()