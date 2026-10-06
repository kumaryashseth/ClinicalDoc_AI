import uuid

from langchain.text_splitter import RecursiveCharacterTextSplitter

from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(documents):
    """
    Split documents into chunks while preserving
    and enriching metadata.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ],
        add_start_index=True
    )

    chunks = text_splitter.split_documents(documents)

    for index, chunk in enumerate(chunks):

        chunk.metadata.update(
            {
                "chunk_id": str(uuid.uuid4()),
                "chunk_index": index,
                "chunk_size": len(chunk.page_content),
                "end_index": (
                    chunk.metadata.get("start_index", 0)
                    + len(chunk.page_content)
                )
            }
        )

    return chunks