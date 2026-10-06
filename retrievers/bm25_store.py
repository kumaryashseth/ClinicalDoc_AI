from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(self, chunks):
        """
        Initialize BM25 Retriever.
        """

        self.documents = chunks

        self.tokenized_corpus = [
            doc.page_content.lower().split()
            for doc in chunks
        ]

        self.bm25 = BM25Okapi(self.tokenized_corpus)
import re

from rank_bm25 import BM25Okapi


from utils.logger import get_logger

logger = get_logger(__name__)

class BM25Retriever:
    """
    Sparse Retriever using BM25.
    """

    def __init__(self, documents):

        self.documents = documents

        self.tokenized_corpus = [
            self._tokenize(doc.page_content)
            for doc in documents
        ]

        self.bm25 = BM25Okapi(self.tokenized_corpus)

        logger.info(
            f"BM25 initialized with {len(documents)} chunks."
        )

    @staticmethod
    def _tokenize(text: str):
        """
        Normalize and tokenize text.
        """

        text = text.lower()

        tokens = re.findall(r"\b\w+\b", text)

        return tokens

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):
        """
        Retrieve top-k documents.
        """

        tokenized_query = self._tokenize(query)

        scores = self.bm25.get_scores(
            tokenized_query
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        logger.info(
            f"BM25 retrieved {len(ranked_indices)} chunks."
        )

        return [
            self.documents[i]
            for i in ranked_indices
        ]
    def retrieve(self, query, top_k=5):
        """
        Retrieve top-k relevant documents using BM25.
        """

        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:top_k]

        return [self.documents[i] for i in ranked_indices]