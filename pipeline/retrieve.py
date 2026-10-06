from retrievers.multi_query import generate_multi_queries
from retrievers.rrf import reciprocal_rank_fusion


def retrieve_documents(
    query,
    hybrid_retriever,
    top_k=5
):
    """
    Complete retrieval pipeline.
    """

    queries = generate_multi_queries(query)

    all_dense_results = []
    all_sparse_results = []

    for q in queries:

        dense_results, sparse_results = hybrid_retriever.retrieve(
            query=q,
            top_k_dense=top_k,
            top_k_sparse=top_k
        )

        all_dense_results.extend(dense_results)
        all_sparse_results.extend(sparse_results)

    fused_documents = reciprocal_rank_fusion(
        all_dense_results,
        all_sparse_results
    )

    return fused_documents[:top_k]