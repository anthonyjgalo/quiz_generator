import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# RAG
DOC_VEC_DB_PATH = os.path.join(BASE_DIR, "data", "doc_vec_db")
VEC_DB_COLLECTION = "documents"

# Utils
ALLOWED_EXTENSIONS = {"txt", "pdf", "docx"}
MAX_SIZE = 10 * 1024 * 1024

# Embedding Model
EMB_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMB_MODEL_SAVE_DIR = os.path.join(BASE_DIR, ".emb_model")
