from typing import cast

import chromadb
import numpy as np
from chonkie import SemanticChunker
from chromadb.api.types import Embeddings, Metadatas, Where

DOC_VEC_DB_PATH = "../data/doc_vec_db"
COLLECTION_NAME = "global_knowledge_base"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

client = chromadb.PersistentClient(DOC_VEC_DB_PATH)
chunker = SemanticChunker(
    embedding_model=EMBEDDING_MODEL,
    threshold=0.5,
    chunk_size=512,
    min_sentences_per_chunk=1,
)

collection = client.get_or_create_collection(name=COLLECTION_NAME)


def process_document_content(doc_id: int, content: str):
    chunks = chunker.chunk(content)

    valid_chunks = [chunk for chunk in chunks if chunk is not None]

    ids = [f"doc_{doc_id}_chunk_{i}" for i in range(len(valid_chunks))]
    doc_ids = [chunk.text for chunk in valid_chunks]

    emb_list = [
        (
            chunk.embedding.tolist()
            if isinstance(chunk.embedding, np.ndarray)
            else chunk.embedding
        )
        for chunk in valid_chunks
    ]

    emb_ids = cast(Embeddings, emb_list)

    metadatas_list = [
        {"doc_id": doc_id, "start_idx": chunk.start_index, "end_idx": chunk.end_index}
        for chunk in chunks
    ]

    metadatas = cast(Metadatas, metadatas_list)

    collection.add(ids=ids, documents=doc_ids, embeddings=emb_ids, metadatas=metadatas)


def get_document_context(doc_ids: list[int], query_text: str, question_num: int):
    query_embeddings = chunker.embedding_model.embed(query_text)
    n_res = question_num * 3

    filter_dict = {"doc_id": {"$in": doc_ids}}

    results = collection.query(
        query_embeddings=query_embeddings,
        n_results=n_res,
        where=cast(Where, filter_dict),
    )

    return results


def delete_document_content(doc_id: int):
    collection.delete(where={"doc_id": doc_id})
