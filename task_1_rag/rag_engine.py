"""
Task 1: AI Document Assistant - Retrieval-Augmented Generation (RAG) Engine
Author: Keshav Jindal
"""

import io
import re
import math
from typing import List, Dict, Any, Tuple, Optional
import pypdf

class DocumentChunk:
    def __init__(self, text: str, doc_name: str, page_number: int, chunk_id: int):
        self.text = text.strip()
        self.doc_name = doc_name
        self.page_number = page_number
        self.chunk_id = chunk_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "document": self.doc_name,
            "page": self.page_number,
            "text": self.text,
        }

class RecursiveCharacterChunker:
    """
    Splits text recursively by paragraphs, sentences, words, and characters
    to maintain semantic cohesion while respecting token boundaries.
    """
    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 120):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", ". ", "? ", "! ", " ", ""]

    def split_text(self, text: str) -> List[str]:
        if not text:
            return []
        return self._split(text, self.separators)

    def _split(self, text: str, separators: List[str]) -> List[str]:
        final_chunks = []
        if not separators:
            # Base case: slice directly
            for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
                chunk = text[i:i + self.chunk_size].strip()
                if chunk:
                    final_chunks.append(chunk)
            return final_chunks

        sep = separators[0]
        remaining_seps = separators[1:]

        splits = text.split(sep) if sep else list(text)
        current_chunk = []
        current_length = 0

        for part in splits:
            part_len = len(part) + (len(sep) if current_chunk else 0)
            if current_length + part_len <= self.chunk_size:
                current_chunk.append(part)
                current_length += part_len
            else:
                if current_chunk:
                    joined = sep.join(current_chunk).strip()
                    if len(joined) > self.chunk_size:
                        # Recurse further on oversized chunk
                        final_chunks.extend(self._split(joined, remaining_seps))
                    elif joined:
                        final_chunks.append(joined)
                    
                    # Compute overlap
                    overlap_parts = []
                    overlap_len = 0
                    for rev_part in reversed(current_chunk):
                        if overlap_len + len(rev_part) <= self.chunk_overlap:
                            overlap_parts.insert(0, rev_part)
                            overlap_len += len(rev_part)
                        else:
                            break
                    current_chunk = overlap_parts + [part]
                    current_length = sum(len(p) for p in current_chunk) + len(sep) * (len(current_chunk) - 1)
                else:
                    # Single part is larger than chunk_size
                    final_chunks.extend(self._split(part, remaining_seps))

        if current_chunk:
            joined = sep.join(current_chunk).strip()
            if joined:
                if len(joined) > self.chunk_size and remaining_seps:
                    final_chunks.extend(self._split(joined, remaining_seps))
                else:
                    final_chunks.append(joined)

        return [c for c in final_chunks if len(c.strip()) >= 20]

class TFIDFVectorStore:
    """
    Lightweight, deterministic, zero-dependency in-memory vector store
    utilizing sublinear TF-IDF and Cosine Similarity.
    Allows offline instant testing and zero-cold-start performance.
    """
    def __init__(self):
        self.chunks: List[DocumentChunk] = []
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.vectors: List[Dict[int, float]] = []

    def _tokenize(self, text: str) -> List[str]:
        return [w.lower() for w in re.findall(r'\b[a-zA-Z0-9_-]{2,}\b', text)]

    def index_chunks(self, chunks: List[DocumentChunk]):
        self.chunks = chunks
        self.vocabulary = {}
        self.idf = {}
        self.vectors = []

        if not chunks:
            return

        doc_count = len(chunks)
        df: Dict[str, int] = {}
        tokenized_docs = [self._tokenize(c.text) for c in chunks]

        # Build vocabulary & document frequency
        for tokens in tokenized_docs:
            unique_tokens = set(tokens)
            for t in unique_tokens:
                df[t] = df.get(t, 0) + 1

        vocab_idx = 0
        for token, count in df.items():
            self.vocabulary[token] = vocab_idx
            # Smoothed IDF: ln(1 + (N / df))
            self.idf[token] = math.log(1.0 + (doc_count / count))
            vocab_idx += 1

        # Compute TF-IDF vectors
        for tokens in tokenized_docs:
            vec = {}
            tf: Dict[str, int] = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            
            norm_sq = 0.0
            for t, count in tf.items():
                if t in self.vocabulary:
                    v_idx = self.vocabulary[t]
                    # Sublinear TF: 1 + log(tf)
                    val = (1.0 + math.log(count)) * self.idf[t]
                    vec[v_idx] = val
                    norm_sq += val * val
            
            # Normalize vector
            norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
            norm_vec = {k: v / norm for k, v in vec.items()}
            self.vectors.append(norm_vec)

    def search(self, query: str, top_k: int = 4) -> List[Tuple[DocumentChunk, float]]:
        if not self.chunks or not self.vectors:
            return []

        q_tokens = self._tokenize(query)
        q_tf: Dict[str, int] = {}
        for t in q_tokens:
            q_tf[t] = q_tf.get(t, 0) + 1

        q_vec = {}
        q_norm_sq = 0.0
        for t, count in q_tf.items():
            if t in self.vocabulary:
                v_idx = self.vocabulary[t]
                val = (1.0 + math.log(count)) * self.idf[t]
                q_vec[v_idx] = val
                q_norm_sq += val * val

        q_norm = math.sqrt(q_norm_sq) if q_norm_sq > 0 else 1.0
        norm_q_vec = {k: v / q_norm for k, v in q_vec.items()}

        scores = []
        for i, doc_vec in enumerate(self.vectors):
            # Dot product of normalized vectors = Cosine Similarity
            dot = sum(norm_q_vec[k] * doc_vec[k] for k in norm_q_vec if k in doc_vec)
            scores.append((self.chunks[i], dot))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

class RAGEngine:
    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 120):
        self.chunker = RecursiveCharacterChunker(chunk_size, chunk_overlap)
        self.vector_store = TFIDFVectorStore()
        self.indexed_files: List[str] = []
        self.total_pages = 0

    def load_pdf(self, file_bytes: bytes, filename: str) -> List[DocumentChunk]:
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        if reader.is_encrypted:
            raise ValueError(f"File '{filename}' is password-protected or encrypted.")
        
        doc_chunks = []
        page_count = len(reader.pages)
        self.total_pages += page_count

        extracted_any = False
        for page_idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                extracted_any = True
                chunks = self.chunker.split_text(page_text)
                for c_idx, chunk_text in enumerate(chunks):
                    chunk = DocumentChunk(
                        text=chunk_text,
                        doc_name=filename,
                        page_number=page_idx + 1,
                        chunk_id=len(doc_chunks) + 1
                    )
                    doc_chunks.append(chunk)

        if not extracted_any:
            raise ValueError(f"No readable text could be extracted from '{filename}'. It may be a scanned image-only PDF.")

        return doc_chunks

    def ingest_documents(self, uploaded_files: List[Tuple[str, bytes]]) -> Dict[str, Any]:
        all_chunks = []
        self.indexed_files = []
        self.total_pages = 0
        errors = []

        for filename, file_bytes in uploaded_files:
            try:
                chunks = self.load_pdf(file_bytes, filename)
                all_chunks.extend(chunks)
                self.indexed_files.append(filename)
            except Exception as e:
                errors.append(f"{filename}: {str(e)}")

        self.vector_store.index_chunks(all_chunks)

        return {
            "indexed_files": self.indexed_files,
            "total_chunks": len(all_chunks),
            "total_pages": self.total_pages,
            "errors": errors
        }

    def query(self, query_text: str, top_k: int = 4, api_key: Optional[str] = None) -> Dict[str, Any]:
        results = self.vector_store.search(query_text, top_k=top_k)
        
        citations = []
        context_parts = []
        for chunk, score in results:
            citations.append({
                "document": chunk.doc_name,
                "page": chunk.page_number,
                "chunk_id": chunk.chunk_id,
                "similarity_score": round(score, 4),
                "text": chunk.text
            })
            context_parts.append(f"[Source: {chunk.doc_name} | Page {chunk.page_number}]\n{chunk.text}")

        context_str = "\n\n---\n\n".join(context_parts)

        # Grounded synthesis
        system_prompt = (
            "You are a strict, helpful AI Document Assistant. "
            "Answer the user's question using ONLY the provided document context below. "
            "Do NOT hallucinate or extrapolate beyond what is explicitly stated in the context. "
            "If the answer cannot be found in the context, explicitly state: "
            "'Based on the provided document(s), this information is not mentioned.' "
            "Always cite the document name and page number for facts you state."
        )

        prompt = f"{system_prompt}\n\nCONTEXT:\n{context_str}\n\nUSER QUESTION: {query_text}\n\nGROUNDED ANSWER:"

        answer = self._generate_llm_response(prompt, api_key, context_parts, query_text)

        return {
            "query": query_text,
            "answer": answer,
            "citations": citations,
            "context_used": context_str
        }

    def _generate_llm_response(self, prompt: str, api_key: Optional[str], context_parts: List[str], query: str) -> str:
        # Check if Google Gemini API is available
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                pass

        # Fallback local deterministic extractive synthesis
        if not context_parts:
            return "Based on the provided document(s), this information is not mentioned."

        # Extractive answer fallback when API key is not supplied
        relevant_sentences = []
        q_words = set(re.findall(r'\b\w{3,}\b', query.lower()))
        for part in context_parts:
            lines = part.split("\n")
            header = lines[0] if lines else ""
            body = " ".join(lines[1:])
            sentences = re.split(r'(?<=[.!?])\s+', body)
            for s in sentences:
                s_words = set(re.findall(r'\b\w{3,}\b', s.lower()))
                overlap = len(q_words.intersection(s_words))
                if overlap >= 2:
                    relevant_sentences.append(f"• {s.strip()} ({header})")

        if relevant_sentences:
            return "Based on the retrieved passages:\n\n" + "\n".join(relevant_sentences[:4])
        else:
            top_excerpt = context_parts[0]
            return f"Relevant excerpt found in document:\n\n\"{top_excerpt}\""
