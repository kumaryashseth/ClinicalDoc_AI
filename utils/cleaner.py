import re
from utils.logger import get_logger

logger = get_logger(__name__)


def clean_text(text: str) -> str:
    """
    Clean raw text extracted from PDF.
    """

    if not text:
        return ""

    # Remove extra spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize multiple newlines
    text = re.sub(r"\n+", "\n", text)

    # Remove non-printable characters
    text = re.sub(r"[^\x20-\x7E\n]", "", text)

    return text.strip()


def clean_documents(documents):
    """
    Clean page content of all LangChain documents.
    """

    cleaned_documents = []

    for document in documents:

        document.page_content = clean_text(
            document.page_content
        )

        cleaned_documents.append(document)

    logger.info(
        f"Cleaned {len(cleaned_documents)} documents."
    )

    return cleaned_documents