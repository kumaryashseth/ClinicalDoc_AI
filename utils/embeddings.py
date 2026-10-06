from langchain_huggingface import HuggingFaceEmbeddings

from config import EMBEDDING_MODEL

from utils.logger import get_logger

logger = get_logger(__name__)


_embedding_model = None


def get_embedding_model():
    """
    Returns a singleton local embedding model.
    """

    global _embedding_model

    if _embedding_model is not None:
        return _embedding_model

    try:

        _embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        logger.info(
            f"Local embedding model initialized: {EMBEDDING_MODEL}"
        )

        return _embedding_model

    except Exception as e:

        logger.exception(
            "Failed to initialize embedding model."
        )

        raise RuntimeError(
            "Embedding model initialization failed."
        ) from e