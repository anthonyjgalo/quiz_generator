import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# RAG
DOC_VEC_DB_PATH = os.path.join(BASE_DIR, "data", "doc_vec_db")
VEC_DB_COLLECTION = "documents"
RESULTS_PER_QUESTION = 3

# Utils
ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}
MAX_SIZE = 10 * 1024 * 1024

# Embedding Model
EMB_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMB_MODEL_SAVE_DIR = os.path.join(BASE_DIR, ".emb_model")

# Quiz Generations
MAX_DIRECT_CHARS = 10_000
DEFAULT_USER_INSTRUCTIONS = "key concepts, main topics, and essential information"
QUESTION_FIXED_LIMITS = [
    ((0, 500), 3),
    ((501, 2_000), 5),
    ((2_001, 5_000), 10),
    ((5_001, 10_000), 15),
    ((10_001, 20_000), 20),
    ((20_001, 50_000), 30),
    ((50_0001, 100_000), 50),
]
