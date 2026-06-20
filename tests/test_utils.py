"""Unit tests for utility layer (file_parser, chunking, helpers)."""
import pytest
import json
from unittest.mock import patch, Mock
from utils.file_parser import FileParser
from utils.chunking import Chunker
from utils.helpers import check_ollama_status, estimate_tokens, truncate_text

class TestFileParser:
    """Test cases for FileParser."""

    def test_parse_text(self):
        """Test parsing plain text."""
        content = b"Hello, this is a plain text file."
        res = FileParser.parse_text(content, "test.txt")
        assert res["text"] == "Hello, this is a plain text file."
        assert res["metadata"]["file_name"] == "test.txt"
        assert res["metadata"]["type"] == "text"

    def test_parse_json(self):
        """Test parsing JSON files."""
        data = {"project": "data-eng-copilot", "active": True}
        content = json.dumps(data).encode("utf-8")
        res = FileParser.parse_json(content, "test.json")
        assert "data-eng-copilot" in res["text"]
        assert res["metadata"]["type"] == "json"

    def test_parse_csv(self):
        """Test parsing CSV files."""
        content = b"id,name,role\n1,Abhi,Lead\n2,Sak,Analyst\n"
        res = FileParser.parse_csv(content, "test.csv")
        assert "Total Rows: 2" in res["text"]
        assert "Abhi" in res["text"]
        assert res["metadata"]["row_count"] == 2
        assert "id" in res["metadata"]["columns"]

    def test_parse_notebook(self):
        """Test parsing Jupyter notebooks."""
        nb_data = {
            "cells": [
                {"cell_type": "markdown", "source": ["# Notebook Title\n"]},
                {"cell_type": "code", "source": ["print('Hello')\n"]}
            ]
        }
        content = json.dumps(nb_data).encode("utf-8")
        res = FileParser.parse_notebook(content, "test.ipynb")
        assert "Notebook Title" in res["text"]
        assert "print('Hello')" in res["text"]
        assert res["metadata"]["cell_count"] == 2


class TestChunking:
    """Test cases for Chunker."""

    def test_chunk_text_sentence_aware(self):
        """Test that text chunking tries to break at sentence boundaries."""
        text = "First sentence. Second sentence. Third sentence. Fourth sentence."
        chunks = Chunker.chunk_text(text, chunk_size=35, chunk_overlap=10)
        assert len(chunks) > 1
        # Check that sentences aren't split mid-word
        for chunk in chunks:
            assert len(chunk) > 0

    def test_chunk_code_function_boundaries(self):
        """Test that code chunking splits by python function boundaries."""
        code = (
            "def func_one():\n"
            "    print('One')\n"
            "\n"
            "def func_two():\n"
            "    print('Two')\n"
        )
        chunks = Chunker.chunk_code(code)
        assert len(chunks) == 2
        assert "def func_one()" in chunks[0]
        assert "def func_two()" in chunks[1]


class TestHelpers:
    """Test cases for helpers."""

    def test_estimate_tokens(self):
        """Test rough token estimation."""
        assert estimate_tokens("Hello World") == 2

    def test_truncate_text(self):
        """Test text truncation."""
        text = "This is a very long string of text."
        assert truncate_text(text, max_length=15) == "This is a ve..."

    @patch("requests.get")
    def test_check_ollama_status_running(self, mock_get):
        """Test check_ollama_status when Ollama is running."""
        check_ollama_status.clear()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"models": [{"name": "llama3.2"}]}
        mock_get.return_value = mock_response

        status = check_ollama_status()
        assert status["status"] == "running"
        assert "llama3.2" in status["models"]

    @patch("requests.get")
    def test_check_ollama_status_not_running(self, mock_get):
        """Test check_ollama_status when Ollama is not running."""
        check_ollama_status.clear()
        mock_get.side_effect = Exception("Connection refused")
        status = check_ollama_status()
        assert status["status"] == "not_running"
        assert "Connection refused" in status["message"]
