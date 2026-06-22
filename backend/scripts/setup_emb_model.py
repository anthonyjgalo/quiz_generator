from core.constants import EMB_MODEL_NAME, EMB_MODEL_SAVE_DIR
from sentence_transformers import SentenceTransformer


def download_model():
    EMB_MODEL_SAVE_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading model to {EMB_MODEL_SAVE_DIR} folder...")
    model = SentenceTransformer(EMB_MODEL_NAME)
    model.save(str(EMB_MODEL_SAVE_DIR))
    print("Embedding Model Ready.")


if __name__ == "__main__":
    download_model()
