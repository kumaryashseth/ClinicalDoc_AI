
from utils.llm import get_llm


from utils.prompts import (
    get_rag_prompt,
    get_summary_prompt
)

from utils.logger import get_logger

logger = get_logger(__name__)

class RAGGenerator:
    """
    Retrieval-Augmented Generation Pipeline.
    """

    def __init__(self, hybrid_retriever):

        self.hybrid_retriever = hybrid_retriever

        self.llm = get_llm()

        self.prompt = get_rag_prompt()

    def _build_context(self, documents):
        """
        Convert retrieved documents into a formatted context.
        """

        context = []

        for doc in documents:

            page = doc.metadata.get("page", "Unknown")

            source = doc.metadata.get(
                "document_name",
                "Unknown Document"
            )

            context.append(
                f"""
Source : {source}

Page : {page}

Content :
{doc.page_content}
"""
            )

        return "\n\n-------------------------\n\n".join(context)

    def _build_sources(self, documents):
        """
        Build source metadata.
        """

        sources = []

        seen = set()

        for doc in documents:

            source = (
                doc.metadata.get("document_name"),
                doc.metadata.get("page")
            )

            if source not in seen:

                seen.add(source)

                sources.append(
                    {
                        "document": source[0],
                        "page": source[1]
                    }
                )

        return sources

    def generate(
        self,
        query,
        top_k=5
    ):
        
    

        logger.info(
            f"Generating answer for query: {query}"
        )

        documents = self.hybrid_retriever.retrieve(
            query=query,
            top_k=top_k
        )

        if not documents:

            return {
                "answer": "No relevant information found in the uploaded document.",
                "sources": [],
                "documents": []
            }

        context = self._build_context(documents)

        chain = (
            self.prompt
            | self.llm
        )

        response = chain.invoke(
            {
                "context": context,
                "question": query
            }
        )

        logger.info("Answer generated successfully.")

        return {

            "answer": response.content,

            "sources": self._build_sources(
                documents
            ),

            "documents": documents

        }
    def generate_summary(self, top_k=20):

        logger.info("Generating document summary...")

        documents = self.hybrid_retriever.retrieve(
            query="Summarize the complete medical document including diagnosis, medications, history, lab findings and treatment.",
            top_k=top_k
        )

        if not documents:
            return "No document content available."

        context = self._build_context(documents)

        chain = (
            get_summary_prompt()
            | self.llm
        )

        response = chain.invoke(
            {
                "context": context
            }
        )

        logger.info("Summary generated successfully.")

        return response.content