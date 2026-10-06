
from retrievers.bm25_store import BM25Retriever
from retrievers.faiss_store import FAISSVectorStore
from utils.chunker import chunk_documents
from utils.cleaner import clean_documents
from utils.loader import load_pdf

from utils.logger import get_logger

logger = get_logger(__name__)

class IngestionPipeline:
    """
    End-to-End Document Ingestion Pipeline.
    """

    def __init__(self):

        self.vector_store = FAISSVectorStore()

        self.bm25_retriever = None

    def ingest(self, pdf_path):

        logger.info("Starting document ingestion...")

        # Step 1 : Load PDF
        documents = load_pdf(pdf_path)

        # Step 2 : Clean Text
        documents = clean_documents(documents)

        # Step 3 : Chunk Documents
        chunks = chunk_documents(documents)

        logger.info(f"Generated {len(chunks)} chunks.")

        # Step 4 : Create FAISS Index
        self.vector_store.create(chunks)

        # Step 5 : Save FAISS Index
        self.vector_store.save()

        # Step 6 : Create BM25 Index
        self.bm25_retriever = BM25Retriever(chunks)

        logger.info("Document ingestion completed successfully.")

        return self.vector_store, self.bm25_retriever