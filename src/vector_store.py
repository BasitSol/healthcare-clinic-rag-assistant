"""Build and load the FAISS vector store."""

from __future__ import annotations

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import settings
from .document_loader import load_pdf_documents


def get_embeddings() -> HuggingFaceEmbeddings:
    """Create the local embedding model."""
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        encode_kwargs={"normalize_embeddings": True},
    )


def split_documents(documents: list[Document]) -> list[Document]:
    """Split PDF pages into smaller chunks for retrieval."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = index

    return chunks


def build_vector_store(force_rebuild: bool = False) -> FAISS:
    """Build or load a FAISS vector store from PDF documents."""
    index_dir = settings.vectorstore_dir
    index_file = index_dir / "index.faiss"

    if index_file.exists() and not force_rebuild:
        return load_vector_store()

    documents = load_pdf_documents(settings.docs_dir)
    chunks = split_documents(documents)

    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    index_dir.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(index_dir))
    return vector_store


def load_vector_store() -> FAISS:
    """Load the local FAISS vector store. Build it if it does not exist."""
    index_dir = settings.vectorstore_dir
    index_file = index_dir / "index.faiss"

    if not index_file.exists():
        return build_vector_store(force_rebuild=True)

    embeddings = get_embeddings()
    return FAISS.load_local(
        str(index_dir),
        embeddings,
        allow_dangerous_deserialization=True,
    )
