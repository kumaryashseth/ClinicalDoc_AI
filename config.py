import os
from dotenv import load_dotenv

load_dotenv()



LLM_PROVIDER = "groq"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "llama-3.3-70b-versatile"
)


EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)


TEMPERATURE = float(
    os.getenv("TEMPERATURE", 0)
)

MAX_TOKENS = int(
    os.getenv("MAX_TOKENS", 1024)
)



CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200


TOP_K = 5

MULTI_QUERY_COUNT = 4

RRF_K = 60


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploaded_files"
)

VECTOR_DB_PATH = os.path.join(
    BASE_DIR,
    "vector_store",
    "faiss_index"
)

LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

CACHE_DIR = os.path.join(
    BASE_DIR,
    "cache"
)