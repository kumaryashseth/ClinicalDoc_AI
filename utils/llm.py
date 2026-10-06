from langchain_groq import ChatGroq

from config import (
    GROQ_API_KEY,
    LLM_MODEL,
    TEMPERATURE,
    MAX_TOKENS
)

from utils.logger import get_logger

logger = get_logger(__name__)


_llm = None


def get_llm():
    """
    Returns a singleton Groq LLM instance.
    """

    global _llm

    if _llm is not None:
        return _llm

    try:

        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not set."
            )

        _llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=LLM_MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        logger.info(
            f"Groq LLM initialized: {LLM_MODEL}"
        )

        return _llm

    except Exception as e:

        logger.exception(
            "Failed to initialize Groq LLM."
        )

        raise RuntimeError(
            "Groq LLM initialization failed."
        ) from e