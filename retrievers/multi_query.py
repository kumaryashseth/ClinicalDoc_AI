
from langchain_core.output_parsers import StrOutputParser

from config import MULTI_QUERY_COUNT
from utils.llm import get_llm
from utils.prompts import get_multi_query_prompt

from utils.logger import get_logger

logger = get_logger(__name__)

class MultiQueryGenerator:
    """
    Generate multiple search queries from a single user query.
    """

    def __init__(self):
        self.llm = get_llm()
        self.prompt = get_multi_query_prompt()

    def generate(self, query: str):
        """
        Generate multiple semantically different search queries.
        """

        chain = (
            self.prompt
            | self.llm
            | StrOutputParser()
        )

        response = chain.invoke(
            {
                "question": query,
                "count": MULTI_QUERY_COUNT
            }
        )

        queries = [
            q.strip()
            for q in response.split("\n")
            if q.strip()
        ]

        # Remove duplicate queries while preserving order
        unique_queries = list(dict.fromkeys(queries))

        # Fallback if LLM returns nothing
        if not unique_queries:
            unique_queries = [query]

        logger.info(
            f"Generated {len(unique_queries)} search queries."
        )

        return unique_queries