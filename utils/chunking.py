"""Text and code chunking with overlap."""
from typing import List, Dict
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP, CODE_CHUNK_SIZE, CODE_CHUNK_OVERLAP
from config.logging_config import get_logger

logger = get_logger("chunking")

class Chunker:
    """Chunk text and code with configurable overlap."""

    @staticmethod
    def chunk_text(text: str, chunk_size: int = None, chunk_overlap: int = None) -> List[str]:
        """Chunk text with overlap."""
        chunk_size = chunk_size or CHUNK_SIZE
        chunk_overlap = chunk_overlap or CHUNK_OVERLAP

        if not text:
            return []

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]

            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('. ')
                if last_period > chunk_size * 0.5:
                    end = start + last_period + 2
                    chunk = text[start:end]

            chunks.append(chunk.strip())
            start = end - chunk_overlap

        return chunks

    @staticmethod
    def chunk_code(code: str, chunk_size: int = None, chunk_overlap: int = None) -> List[str]:
        """Chunk code with overlap, respecting function boundaries."""
        chunk_size = chunk_size or CODE_CHUNK_SIZE
        chunk_overlap = chunk_overlap or CODE_CHUNK_OVERLAP

        if not code:
            return []

        # Try to split by functions/classes first
        import re

        # Python function/class boundaries
        pattern = r'(?:^\s*def\s+|^\s*class\s+|^\s*#\s*---)'
        matches = list(re.finditer(pattern, code, re.MULTILINE))

        if len(matches) > 1:
            chunks = []
            for i, match in enumerate(matches):
                start = match.start()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(code)
                chunk = code[start:end].strip()
                if chunk:
                    chunks.append(chunk)
            return chunks

        # Fallback to line-based chunking
        lines = code.split('\n')
        chunks = []
        current_chunk = []
        current_size = 0

        for line in lines:
            line_size = len(line) + 1
            if current_size + line_size > chunk_size and current_chunk:
                chunks.append('\n'.join(current_chunk))
                # Keep overlap lines
                overlap_lines = current_chunk[-chunk_overlap:] if len(current_chunk) > chunk_overlap else current_chunk
                current_chunk = overlap_lines + [line]
                current_size = sum(len(l) + 1 for l in current_chunk)
            else:
                current_chunk.append(line)
                current_size += line_size

        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        return chunks

    @staticmethod
    def chunk_document(text: str, file_type: str = "text") -> List[Dict]:
        """Chunk a document using Parent-Child chunking to preserve code/context structure."""
        if file_type in ["py", "sql", "yaml", "yml", "json"]:
            parent_chunks = Chunker.chunk_code(text, chunk_size=2000, chunk_overlap=200)
            chunk_type = "code"
        else:
            parent_chunks = Chunker.chunk_text(text, chunk_size=1500, chunk_overlap=150)
            chunk_type = "text"

        child_chunks = []
        global_child_index = 0

        for p_idx, p_text in enumerate(parent_chunks):
            # Split the parent chunk into smaller child chunks for vector matching
            if chunk_type == "code":
                c_texts = Chunker.chunk_code(p_text, chunk_size=450, chunk_overlap=50)
            else:
                c_texts = Chunker.chunk_text(p_text, chunk_size=350, chunk_overlap=40)

            # If sub-chunking returns nothing, fallback to parent text
            if not c_texts:
                c_texts = [p_text]

            for c_text in c_texts:
                child_chunks.append({
                    "text": c_text,
                    "parent_text": p_text,
                    "parent_index": p_idx,
                    "type": chunk_type,
                    "index": global_child_index
                })
                global_child_index += 1

        return child_chunks


def chunk_text(text: str, **kwargs) -> List[str]:
    """Convenience function for text chunking."""
    return Chunker.chunk_text(text, **kwargs)

def chunk_code(code: str, **kwargs) -> List[str]:
    """Convenience function for code chunking."""
    return Chunker.chunk_code(code, **kwargs)

def chunk_document(text: str, file_type: str = "text", **kwargs) -> List[Dict]:
    """Convenience function for document chunking."""
    return Chunker.chunk_document(text, file_type, **kwargs)


