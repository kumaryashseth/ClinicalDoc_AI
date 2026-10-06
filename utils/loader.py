import uuid
from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader


from utils.logger import get_logger

logger = get_logger(__name__)

def load_pdf(pdf_path: str):
    """
    Load a PDF and enrich every page with useful metadata.

    Returns:
        List[Document]
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        logger.error(f"PDF not found: {pdf_path}")
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        logger.error("Uploaded file is not a PDF.")
        raise ValueError("Only PDF files are supported.")

    logger.info(f"Loading PDF: {pdf_path.name}")

    loader = PyMuPDFLoader(str(pdf_path))
    documents = loader.load()

    if not documents:
        logger.warning("No text found in PDF.")
        raise ValueError("No readable text found in the uploaded PDF.")

    for page_number, document in enumerate(documents):

        document.metadata.update(
            {
                "document_id": str(uuid.uuid4()),
                "document_name": pdf_path.name,
                "source": str(pdf_path),
                "page": page_number + 1,
            }
        )

    logger.info(
        f"Loaded {len(documents)} pages from {pdf_path.name}"
    )

    return documents