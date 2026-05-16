import os
from functools import lru_cache
from typing import cast

import chromadb
import numpy as np
from chonkie import EmbeddingsRefinery, SemanticChunker
from chromadb.api.types import Embeddings, Metadatas
from core.constants import (
    DOC_VEC_DB_PATH,
    EMB_MODEL_NAME,
    EMB_MODEL_SAVE_DIR,
    VEC_DB_COLLECTION,
)
from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def get_chunker():
    if not os.path.exists(EMB_MODEL_SAVE_DIR):
        os.makedirs(EMB_MODEL_SAVE_DIR, exist_ok=True)
        print(f"📦 Downloading embedding model to {EMB_MODEL_SAVE_DIR} folder...")
        print("    This could take a while....")
        model = SentenceTransformer(EMB_MODEL_NAME)
        model.save(EMB_MODEL_SAVE_DIR)
        print("✅  Model ready.")

    return SemanticChunker(
        embedding_model=EMB_MODEL_SAVE_DIR,
        threshold=0.5,
        chunk_size=512,
        min_sentences_per_chunk=1,
    )


@lru_cache(maxsize=1)
def get_collection():
    client = chromadb.PersistentClient(DOC_VEC_DB_PATH)
    return client.get_or_create_collection(name=VEC_DB_COLLECTION)


@lru_cache(maxsize=1)
def get_embedding_refinery():
    return EmbeddingsRefinery(embedding_model=EMB_MODEL_SAVE_DIR)


def save_document_content(doc_id: int, content: str):
    chunker = get_chunker()
    chunks = chunker.chunk(content)

    valid_chunks = [chunk for chunk in chunks if chunk is not None]

    emb_refinery = get_embedding_refinery()

    chnks_with_emb = emb_refinery(valid_chunks)

    ids = [f"doc_{doc_id}_chunk_{i}" for i in range(len(chnks_with_emb))]
    docs = [chunk.text for chunk in chnks_with_emb]

    emb_list = [
        (
            chunk.embedding.tolist()
            if isinstance(chunk.embedding, np.ndarray)
            else chunk.embedding
        )
        for chunk in chnks_with_emb
    ]

    emb_ids = cast(Embeddings, emb_list)

    metadatas_list = [
        {"doc_id": doc_id, "start_idx": chunk.start_index, "end_idx": chunk.end_index}
        for chunk in chunks
    ]

    metadatas = cast(Metadatas, metadatas_list)

    collection = get_collection()

    collection.add(ids=ids, documents=docs, embeddings=emb_ids, metadatas=metadatas)


def get_document_context(doc_id: int, query_text: str, question_qty: int):
    chunker = get_chunker()
    query_embeddings = chunker.embedding_model.embed(query_text)
    n_res = question_qty * 3

    collection = get_collection()

    results = collection.query(
        query_embeddings=query_embeddings,
        n_results=n_res,
        where={"doc_id": doc_id},
    )

    return results.get("documents", [[]])


def delete_document_content(doc_id: int):
    collection = get_collection()
    collection.delete(where={"doc_id": doc_id})
