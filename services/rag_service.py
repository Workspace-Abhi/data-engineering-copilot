"""ChromaDB vector search and context augmentation service."""
import os
from typing import List, Dict, Optional, Tuple
import chromadb
from chromadb.config import Settings
import streamlit as st
from config.settings import CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME, CHROMA_SEARCH_K
from config.logging_config import get_logger
from services.llm_service import get_llm_service

import pickle
from pathlib import Path
import math

logger = get_logger("rag_service")

class InMemoryCollection:
    """Fallback in-memory vector store mimicking ChromaDB's Collection interface."""

    def __init__(self, persist_dir: str):
        self.persist_path = Path(persist_dir) / "fallback_vector_store.pkl"
        self.data = {
            "ids": [],
            "embeddings": [],
            "documents": [],
            "metadatas": []
        }
        self._load()

    def _load(self):
        if self.persist_path.exists():
            try:
                with open(self.persist_path, "rb") as f:
                    self.data = pickle.load(f)
                logger.info(f"Loaded fallback vector database from {self.persist_path}")
            except Exception as e:
                logger.error(f"Failed to load fallback vector database: {e}")

    def _save(self):
        try:
            with open(self.persist_path, "wb") as f:
                pickle.dump(self.data, f)
        except Exception as e:
            logger.error(f"Failed to save fallback vector database: {e}")

    def add(self, embeddings, documents, metadatas, ids):
        for emb, doc, meta, doc_id in zip(embeddings, documents, metadatas, ids):
            if doc_id in self.data["ids"]:
                idx = self.data["ids"].index(doc_id)
                self.data["embeddings"][idx] = emb
                self.data["documents"][idx] = doc
                self.data["metadatas"][idx] = meta
            else:
                self.data["ids"].append(doc_id)
                self.data["embeddings"].append(emb)
                self.data["documents"].append(doc)
                self.data["metadatas"].append(meta)
        self._save()

    def query(self, query_embeddings, n_results, where=None, include=None):
        query_emb = query_embeddings[0]

        def dot_product(v1, v2):
            return sum(x * y for x, y in zip(v1, v2))

        def magnitude(v):
            return math.sqrt(sum(x * x for x in v))

        def cosine_similarity(v1, v2):
            mag1 = magnitude(v1)
            mag2 = magnitude(v2)
            if not mag1 or not mag2:
                return 0.0
            return dot_product(v1, v2) / (mag1 * mag2)

        results = []
        for idx, (emb, doc, meta, doc_id) in enumerate(zip(
            self.data["embeddings"], self.data["documents"], self.data["metadatas"], self.data["ids"]
        )):
            if where:
                match = True
                for k, v in where.items():
                    if meta.get(k) != v:
                        match = False
                        break
                if not match:
                    continue

            sim = cosine_similarity(query_emb, emb)
            dist = 1.0 - sim  # Cosine distance
            results.append((dist, doc, meta, doc_id))

        results.sort(key=lambda x: x[0])
        results = results[:n_results]

        ret = {
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]],
            "ids": [[]]
        }
        for dist, doc, meta, doc_id in results:
            ret["documents"][0].append(doc)
            ret["metadatas"][0].append(meta)
            ret["distances"][0].append(dist)
            ret["ids"][0].append(doc_id)
        return ret

    def delete(self, ids):
        for doc_id in ids:
            if doc_id in self.data["ids"]:
                idx = self.data["ids"].index(doc_id)
                self.data["ids"].pop(idx)
                self.data["embeddings"].pop(idx)
                self.data["documents"].pop(idx)
                self.data["metadatas"].pop(idx)
        self._save()

    def get(self):
        return {
            "ids": self.data["ids"],
            "documents": self.data["documents"],
            "metadatas": self.data["metadatas"]
        }

    def count(self):
        return len(self.data["ids"])


class RAGService:
    """Retrieval-Augmented Generation service."""

    def __init__(self, persist_dir: str = None, collection_name: str = None):
        self.persist_dir = persist_dir or CHROMA_PERSIST_DIR
        self.collection_name = collection_name or CHROMA_COLLECTION_NAME
        self.client = None
        self.collection = None
        self._init_chroma()
        
        # Preseed database with expert data engineering documentation if empty
        try:
            import sys
            is_testing = "pytest" in sys.modules or "unittest" in sys.modules
            if not is_testing and self.count() == 0:
                self.preseed_database()
        except Exception as e:
            logger.error(f"Failed to check or preseed database: {e}")

    def _init_chroma(self):
        """Initialize ChromaDB client, falling back to InMemoryCollection on failure."""
        try:
            os.makedirs(self.persist_dir, exist_ok=True)
            self.client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            self.is_fallback = False
            logger.info(f"ChromaDB initialized: {self.collection_name}")
        except Exception as e:
            logger.warning(f"ChromaDB initialization failed: {e}. Falling back to InMemoryCollection.")
            self.collection = InMemoryCollection(self.persist_dir)
            self.is_fallback = True

    def preseed_database(self):
        """Preseed the vector store with high-fidelity expert data engineering documentation."""
        preseed_dir = Path(__file__).parent.parent / "knowledge_base" / "preseeded_kb"
        if not preseed_dir.exists():
            logger.warning(f"Preseed directory {preseed_dir} does not exist. Skipping pre-population.")
            return

        logger.info("Preseeding knowledge database with expert markdown blueprints...")
        documents = []
        metadatas = []
        ids = []

        for filepath in preseed_dir.glob("*.md"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                file_name = filepath.name
                meta = {
                    "file_name": file_name,
                    "type": "md",
                    "length": len(content)
                }

                from utils.chunking import chunk_document
                chunks = chunk_document(content, "md")

                import uuid
                for chunk in chunks:
                    doc_id = f"preseeded_{filepath.stem}_{uuid.uuid4().hex[:8]}_{chunk['index']}"
                    documents.append(chunk["text"])
                    metadatas.append({
                        **meta,
                        "chunk_index": chunk["index"],
                        "chunk_type": chunk["type"],
                        "parent_text": chunk.get("parent_text", ""),
                        "parent_index": chunk.get("parent_index", 0),
                        "source": file_name
                    })
                    ids.append(doc_id)
            except Exception as e:
                logger.error(f"Failed to read preseeded file {filepath.name}: {e}")

        if documents:
            try:
                self.add_documents(documents, metadatas, ids)
                logger.info(f"Successfully indexed {len(documents)} preseeded expert document chunks.")
            except Exception as e:
                logger.error(f"Failed to index preseeded document chunks: {e}")

    def add_documents(
        self, 
        documents: List[str], 
        metadatas: List[Dict] = None,
        ids: List[str] = None
    ):
        """Add documents to vector store."""
        if not documents:
            return

        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]

        if metadatas is None:
            metadatas = [{} for _ in documents]

        try:
            # Generate embeddings via Ollama
            llm_service = get_llm_service()
            embeddings = llm_service.embed(documents)

            self.collection.add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(documents)} documents to ChromaDB")
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise

    def search(
        self, 
        query: str, 
        k: int = None,
        filter_dict: Dict = None
    ) -> List[Dict]:
        """Search relevant documents using a hybrid vector + BM25 ranking and Parent retrieval."""
        k = k or CHROMA_SEARCH_K

        try:
            # 1. Semantic Vector Search
            llm_service = get_llm_service()
            query_embedding = llm_service.embed_single(query)

            db_count = self.count()
            if not isinstance(db_count, int):
                db_count = 0

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(k * 2, db_count) if db_count > 0 else k,
                where=filter_dict,
                include=["documents", "metadatas", "distances"]
            )

            vector_docs = []
            if results and results.get("documents") and results["documents"][0]:
                for i in range(len(results["documents"][0])):
                    meta = results["metadatas"][0][i] if results["metadatas"] else {}
                    vector_docs.append({
                        "id": results["ids"][0][i] if results["ids"] else f"v_{i}",
                        "content": results["documents"][0][i],
                        "metadata": meta,
                        "distance": results["distances"][0][i] if results["distances"] else 0.5
                    })

            # 2. Keyword TF-IDF Search over all candidates
            all_docs_raw = self.collection.get()
            all_docs = []
            if all_docs_raw and all_docs_raw.get("ids"):
                for i in range(len(all_docs_raw["ids"])):
                    meta = all_docs_raw["metadatas"][i] if all_docs_raw["metadatas"] else {}
                    all_docs.append({
                        "id": all_docs_raw["ids"][i],
                        "content": all_docs_raw["documents"][i] if all_docs_raw["documents"] else "",
                        "metadata": meta
                    })

            keyword_docs = self._keyword_search(query, all_docs, k=k * 2)

            # 3. Combine search scores via Reciprocal Rank Fusion (RRF)
            merged_docs = self._reciprocal_rank_fusion(vector_docs, keyword_docs, k=k)

            # 4. Resolve Content to Parent Chunk (Parent Retrieval)
            for doc in merged_docs:
                parent_text = doc["metadata"].get("parent_text", "")
                if parent_text:
                    doc["child_text"] = doc["content"]
                    doc["content"] = parent_text

            return merged_docs
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def _keyword_search(self, query: str, documents: List[Dict], k: int) -> List[Dict]:
        """Simple TF-IDF ranking in Python for reliable keyword query hits."""
        import re
        from collections import Counter
        import math

        def tokenize(text):
            return re.findall(r'\w+', text.lower())

        query_tokens = tokenize(query)
        if not query_tokens or not documents:
            return []

        N = len(documents)
        doc_tokens_list = [tokenize(doc["content"]) for doc in documents]

        # Calculate Document Frequency
        df = Counter()
        for tokens in doc_tokens_list:
            for token in set(tokens):
                df[token] += 1

        scores = []
        for i, doc in enumerate(documents):
            tokens = doc_tokens_list[i]
            tf = Counter(tokens)
            doc_len = len(tokens)
            if doc_len == 0:
                continue

            score = 0.0
            for token in query_tokens:
                if token in tf:
                    # Smoothing IDF computation
                    idf = math.log((N - df[token] + 0.5) / (df[token] + 0.5) + 1.0)
                    idf = max(0.0001, idf)
                    tf_val = tf[token] / doc_len
                    score += tf_val * idf
            if score > 0:
                scores.append((score, doc))

        scores.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scores[:k]]

    def _reciprocal_rank_fusion(self, vector_results: List[Dict], keyword_results: List[Dict], k: int) -> List[Dict]:
        """Rank fusion combining vector and keyword hits."""
        rrf_scores = {}
        doc_lookup = {}

        def get_doc_key(doc):
            return doc.get("id") or doc.get("content")

        for rank, doc in enumerate(vector_results):
            key = get_doc_key(doc)
            doc_lookup[key] = doc
            rrf_scores[key] = rrf_scores.get(key, 0.0) + (1.0 / (60.0 + rank + 1.0))

        for rank, doc in enumerate(keyword_results):
            key = get_doc_key(doc)
            doc_lookup[key] = doc
            rrf_scores[key] = rrf_scores.get(key, 0.0) + (1.0 / (60.0 + rank + 1.0))

        sorted_keys = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
        return [doc_lookup[key] for key in sorted_keys[:k]]

    def get_context(self, query: str, k: int = None) -> str:
        """Get augmented context for a query."""
        try:
            import streamlit as st
            if not st.session_state.get("enable_rag", True):
                return ""
        except Exception:
            pass

        results = self.search(query, k=k)
        if not results:
            return ""

        context_parts = []
        for i, result in enumerate(results):
            source = result["metadata"].get("source", "Unknown")
            context_parts.append(f"[Document {i+1} from {source}]\n{result['content']}")

        return "\n\n".join(context_parts)

    def delete_document(self, doc_id: str):
        """Delete a document by ID."""
        try:
            self.collection.delete(ids=[doc_id])
            logger.info(f"Deleted document: {doc_id}")
        except Exception as e:
            logger.error(f"Failed to delete document: {e}")

    def get_all_documents(self) -> List[Dict]:
        """Get all indexed documents."""
        try:
            results = self.collection.get()
            documents = []
            for i in range(len(results["ids"])):
                documents.append({
                    "id": results["ids"][i],
                    "content": results["documents"][i] if results["documents"] else "",
                    "metadata": results["metadatas"][i] if results["metadatas"] else {}
                })
            return documents
        except Exception as e:
            logger.error(f"Failed to get documents: {e}")
            return []

    def count(self) -> int:
        """Get document count."""
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"Failed to count documents: {e}")
            return 0


@st.cache_resource
def get_rag_service() -> RAGService:
    """Get cached RAG service instance."""
    return RAGService()
