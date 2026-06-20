"""Code Execution Engine for running SQL in SQLite and Python in sandbox."""
import sys
import io
import sqlite3
from typing import Dict, Any, Optional
from config.logging_config import get_logger

logger = get_logger("code_execution_engine")

class CodeExecutionEngine:
    """Safely executes SQL and Python snippets."""

    @staticmethod
    def execute_sql(sql: str) -> Dict[str, Any]:
        """Execute a SQL query against an in-memory SQLite database."""
        conn = None
        try:
            conn = sqlite3.connect(":memory:")
            cursor = conn.cursor()
            
            # Execute multiple statements if separated by semicolon
            statements = [s.strip() for s in sql.split(";") if s.strip()]
            results = []
            columns = []
            
            for statement in statements:
                cursor.execute(statement)
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
                    results.extend(rows)
            
            conn.commit()
            return {
                "success": True,
                "columns": columns,
                "rows": results,
                "row_count": len(results)
            }
        except Exception as e:
            logger.error(f"SQL Execution failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            if conn:
                conn.close()

    @staticmethod
    def execute_python(code: str) -> Dict[str, Any]:
        """Safely execute Python code using redirected stdout/stderr and restricted globals."""
        # Capture stdout
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        # Restricted environment
        exec_globals = {
            "__builtins__": {
                "print": print,
                "range": range,
                "len": len,
                "int": int,
                "float": float,
                "str": str,
                "list": list,
                "dict": dict,
                "set": set,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "bool": bool,
                "enumerate": enumerate,
                "zip": zip,
                "Exception": Exception,
                "TypeError": TypeError,
                "ValueError": ValueError,
            },
            "math": __import__("math"),
            "json": __import__("json"),
        }
        exec_locals = {}

        try:
            # Execute in sandbox
            exec(code, exec_globals, exec_locals)
            sys.stdout = old_stdout
            output = redirected_output.getvalue()
            return {
                "success": True,
                "output": output,
                "variables": {k: str(v) for k, v in exec_locals.items() if not k.startswith("__")}
            }
        except Exception as e:
            sys.stdout = old_stdout
            logger.error(f"Python execution sandbox failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "output": redirected_output.getvalue()
            }
        finally:
            sys.stdout = old_stdout


def get_code_execution_engine() -> CodeExecutionEngine:
    """Get code execution engine instance."""
    return CodeExecutionEngine()
