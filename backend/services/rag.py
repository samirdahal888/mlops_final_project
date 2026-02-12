from dataclasses import dataclass
from pathlib import Path

from backend.config import AppConfig
from backend.services.embedding import EmbeddingService
from backend.services.llm import LLMService
from backend.services.vector_store import SearchResult, VectorStoreService
from backend.utils.chunking import split_text_into_chunks
from backend.utils.document_parser import exract_text_from_pdf


@dataclass
class IndexResult:
    filename: str
    chunks_stored: int
    message: str


@dataclass
class ChatResult:
    answer: str
    sources: list[str]


class RAGOrchestrator:
    """Coordinates the full RAG pipeline: indexing and retrieval-augmented chat."""

    def __init__(
        self,
        config: AppConfig,
        embedding_service: EmbeddingService,
        vector_store: VectorStoreService,
        llm_service: LLMService,
    ):
        self._config = config
        self._embedding = embedding_service
        self._vector_store = vector_store
        self._llm = llm_service

    def index_document(self, file_path: Path, filename: str) -> IndexResult:
        """Parse, chunk, embed, and store a document."""
        text = exract_text_from_pdf(file_path)

        chunks = split_text_into_chunks(
            text=text,
            # source=filename,
            # config=self._config.chunking,
        )

        if not chunks:
            return IndexResult(
                filename=filename,
                chunks_stored=0,
                message="No content found in document.",
            )

        chunk_texts = [chunk.content for chunk in chunks]
        embeddings = self._embedding.embed_batch(chunk_texts)

        count = self._vector_store.store_embeddings(
            embeddings=embeddings,
            texts=chunk_texts,
            source=filename,
        )

        return IndexResult(
            filename=filename,
            chunks_stored=count,
            message=f"Successfully indexed {count} chunks from '{filename}'.",
        )

    def chat(self, question: str, top_k: int = 5) -> ChatResult:
        """Retrieve relevant context and generate an answer."""
        query_embedding = self._embedding.embed(question)

        search_results = self._vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        if not search_results:
            return ChatResult(
                answer="No relevant documents found. Please upload documents first.",
                sources=[],
            )

        context_chunks = [result.content for result in search_results]
        sources = _extract_unique_sources(search_results)

        answer = self._llm.generate_answer(
            question=question,
            context_chunks=context_chunks,
        )

        return ChatResult(answer=answer, sources=sources)


def _extract_unique_sources(results: list[SearchResult]) -> list[str]:
    seen = set()
    sources = []
    for result in results:
        if result.source not in seen:
            seen.add(result.source)
            sources.append(result.source)
    return sources
