from app.config import get_settings
from app.rag.embedder import load_embedding_model
from app.rag.ingestion import ingest_destinations


def main() -> None:
    settings = get_settings()

    csv_path = "data/knowledge/cleaned_dataset.csv"

    print("Loading embedding model...")
    embedder = load_embedding_model(settings.embedding_model)

    print("Starting RAG ingestion...")
    result = ingest_destinations(
        csv_path=csv_path,
        chroma_path=settings.chroma_path,
        collection_name=settings.chroma_collection_name,
        embedder=embedder,
    )

    print("Ingestion result:")
    print(result)


if __name__ == "__main__":
    main()