from collections import defaultdict


def reciprocal_rank_fusion(
    dense_results,
    sparse_results,
    k=60
):
    """
    Fuse multiple ranked lists using Reciprocal Rank Fusion (RRF).
    """

    rrf_scores = defaultdict(float)
    document_map = {}

    retrieval_lists = [
        dense_results,
        sparse_results
    ]

    for result_list in retrieval_lists:

        for rank, document in enumerate(result_list):

            document_id = (
                document.metadata["source"],
                document.metadata["page"],
                document.page_content
            )

            document_map[document_id] = document

            rrf_scores[document_id] += 1 / (k + rank + 1)

    ranked_documents = sorted(
        rrf_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    fused_documents = [
        document_map[doc_id]
        for doc_id, _ in ranked_documents
    ]

    return fused_documents