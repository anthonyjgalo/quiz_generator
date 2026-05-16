import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.constants import EMB_MODEL_NAME, EMB_MODEL_SAVE_DIR
from sentence_transformers import SentenceTransformer

os.makedirs(EMB_MODEL_SAVE_DIR, exist_ok=True)

print(f"Downloading model to {EMB_MODEL_SAVE_DIR} folder...")

model = SentenceTransformer(EMB_MODEL_NAME)

model.save(EMB_MODEL_SAVE_DIR)

print("Embedding Model Ready.")
