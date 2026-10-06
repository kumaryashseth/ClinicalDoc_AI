from pathlib import Path

from langchain_community.vectorstores import FAISS

from config import VECTOR_DB_PATH
from utils.embeddings import get_embedding_model

from utils.logger import get_logger

logger = get_logger(__name__)

class FAISSVectorStore:
    """
    Wrapper class for FAISS Vector Store.
    """

    def __init__(self):

        self.embedding_model = get_embedding_model()

        self.vector_store = None

    def create(self, chunks):
        """
        Create a new FAISS index.
        """

        logger.info("Creating FAISS index...")

        self.vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=self.embedding_model
        )

        logger.info(
            f"Indexed {len(chunks)} chunks successfully."
        )

        return self.vector_store

    def save(self):
        """
        Save FAISS index to disk.
        """

        if self.vector_store is None:
            raise ValueError(
                "Vector store is not initialized."
            )

        Path(VECTOR_DB_PATH).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.vector_store.save_local(
            VECTOR_DB_PATH
        )

        logger.info(
            "FAISS index saved successfully."
        )

    def load(self):
        """
        Load an existing FAISS index.
        """

        index_path = Path(VECTOR_DB_PATH)

        if not index_path.exists():

            logger.warning(
                "No existing FAISS index found."
            )

            return None

        self.vector_store = FAISS.load_local(
            VECTOR_DB_PATH,
            self.embedding_model,
            allow_dangerous_deserialization=True
        )

        logger.info(
            "FAISS index loaded successfully."
        )

        return self.vector_store

    def similarity_search(
        self,
        query,
        k=5
    ):
        """
        Perform similarity search.
        """

        if self.vector_store is None:

            raise ValueError(
                "Vector store is not initialized."
            )

        return self.vector_store.similarity_search(
            query=query,
            k=k
        )