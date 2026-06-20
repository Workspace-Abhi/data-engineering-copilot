"""GitHub Repository Sync pipeline for AST parsing and index ingestion."""
import ast
from typing import Dict, List, Optional
from config.logging_config import get_logger
from services.rag_service import get_rag_service

logger = get_logger("github_repo_sync")

class GitHubRepoSyncPipeline:
    """Synchronizes code repos by parsing python syntax trees (AST) and indexing declarations."""

    def __init__(self, repo_name: str):
        self.repo_name = repo_name
        self.rag_service = get_rag_service()

    def parse_python_ast(self, code: str) -> List[Dict]:
        """Extract functions and classes definitions using python AST module."""
        try:
            tree = ast.parse(code)
            declarations = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    declarations.append({
                        "type": "class",
                        "name": node.name,
                        "line": node.lineno
                    })
                elif isinstance(node, ast.FunctionDef):
                    declarations.append({
                        "type": "function",
                        "name": node.name,
                        "line": node.lineno
                    })
            return declarations
        except Exception as e:
            logger.error(f"AST parsing failed: {e}")
            return []

    def handle_webhook_push(self, payload: Dict) -> Dict:
        """Simulate processing a git push webhook with changed file AST index updates."""
        logger.info(f"Processing GitHub push webhook for repository {self.repo_name}...")
        
        # Simulated changed file content
        changed_file = "utils/helpers.py"
        sample_code = """
class DataFormatter:
    def format_output(self, data):
        return str(data).upper()

def calculate_checksum(val):
    return hash(val)
"""
        declarations = self.parse_python_ast(sample_code)
        
        # Prepare text representation for indexing
        indexed_text = f"Repository: {self.repo_name}\nFile: {changed_file}\n"
        for decl in declarations:
            indexed_text += f"- Declared {decl['type']} '{decl['name']}' at line {decl['line']}\n"
            
        doc_id = f"github_{self.repo_name}_helper_ast"
        self.rag_service.add_documents(
            documents=[indexed_text],
            metadatas=[{"source": changed_file, "repo": self.repo_name, "type": "github_ast"}],
            ids=[doc_id]
        )
        
        return {
            "success": True,
            "repo": self.repo_name,
            "file_processed": changed_file,
            "declarations_found": len(declarations)
        }


def get_github_sync(repo_name: str) -> GitHubRepoSyncPipeline:
    """Get GitHub Sync instance."""
    return GitHubRepoSyncPipeline(repo_name)
