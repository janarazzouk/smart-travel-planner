from app.config import get_settings
from app.rag.chunker import build_destination_documents
from app.rag.embedder import embed_texts, load_embedding_model
from app.rag.loader import load_destination_rows
from app.rag.store import (
    add_documents_to_collection,
    get_chroma_client,
    get_or_create_collection,
)


def main() -> None:
    settings = get_settings()

    csv_path = "data/knowledge/cleaned_dataset.csv"

    print("Loading rows...")
    rows = load_destination_rows(csv_path)
    print(f"Rows loaded: {len(rows)}")
    print(rows[:2])

    print("\nBuilding documents...")
    documents = build_destination_documents(rows)
    print(f"Documents built: {len(documents)}")
    print(documents[:2])

    print("\nLoading embedding model...")
    embedder = load_embedding_model(settings.embedding_model)
    print("Embedder loaded")

    print("\nEmbedding documents...")
    texts = [doc["text"] for doc in documents]
    embeddings = embed_texts(texts, embedder)
    print(f"Embeddings created: {len(embeddings)}")
    print(f"Embedding size: {len(embeddings[0])}")

    print("\nTesting Chroma store...")
    client = get_chroma_client(settings.chroma_path)
    collection = get_or_create_collection(
        client=client,
        collection_name=settings.chroma_collection_name,
    )

    add_documents_to_collection(
        collection=collection,
        documents=documents,
        embeddings=embeddings,
    )

    print(f"Documents in Chroma: {collection.count()}")
    print("\nRAG pipeline test passed")


if __name__ == "__main__":
    main()