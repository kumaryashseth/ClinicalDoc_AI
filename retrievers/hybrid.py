
from config import MULTI_QUERY_COUNT, RRF_K
from retrievers.multi_query import MultiQueryGenerator
from retrievers.rrf import reciprocal_rank_fusion

from utils.logger import get_logger

logger = get_logger(__name__)

class HybridRetriever:
    """
    Hybrid Retriever that combines:

    1. Multi Query Generation
    2. Dense Retrieval (FAISS)
    3. Sparse Retrieval (BM25)
    4. Reciprocal Rank Fusion (RRF)
    """

    def __init__(
        self,
        vector_store,
        bm25_retriever,
    ):
        self.vector_store = vector_store
        self.bm25_retriever = bm25_retriever
        self.multi_query_generator = MultiQueryGenerator()

    def _dense_search(self, query, top_k):
        return self.vector_store.similarity_search(
            query=query,
            k=top_k
        )

    def _sparse_search(self, query, top_k):
        return self.bm25_retriever.retrieve(
            query=query,
            top_k=top_k
        )

    def retrieve(
        self,
        query,
        top_k=5,
        use_multi_query=True
    ):
        """
        Complete Hybrid Retrieval Pipeline.
        """

        logger.info(f"User Query: {query}")

        if use_multi_query:

            queries = self.multi_query_generator.generate(query)

            if len(queries) > MULTI_QUERY_COUNT:
                queries = queries[:MULTI_QUERY_COUNT]

        else:

            queries = [query]

        logger.info(f"Generated Queries: {queries}")

        all_dense_results = []
        all_sparse_results = []

        for search_query in queries:

            dense_results = self._dense_search(
                search_query,
                top_k
            )

            sparse_results = self._sparse_search(
                search_query,
                top_k
            )

            all_dense_results.extend(dense_results)
            all_sparse_results.extend(sparse_results)

        fused_documents = reciprocal_rank_fusion(
            dense_results=all_dense_results,
            sparse_results=all_sparse_results,
            k=RRF_K
        )

        logger.info(
            f"Retrieved {len(fused_documents)} fused documents."
        )

        return fused_documents[:top_k]