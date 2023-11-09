import unittest
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from scaf_code.scaffold_code import (
    scaffold_code,
    create_inputs,
    load_files,
    DEFAULT_SYSTEM_PROMPT,
)

# Constants for testing
SPEC_TEXTS = ["Generate a function to add two numbers."]
SPEC_FILES = ["spec_file1.txt", "spec_file2.txt"]
REF_FILES = ["ref_code.py", "ref_spec.txt"]
OPTIONS = {"model_name": "gpt-4-1106-preview"}

# Mocked content for spec and ref files
MOCKED_SPEC_FILE_CONTENT = {
    "spec_file1.txt": "Specification for file 1",
    "spec_file2.txt": "Specification for file 2",
}
MOCKED_REF_FILE_CONTENT = {
    "ref_code.py": "Reference code in Python",
    "ref_spec.txt": "Reference specification text",
}

# Mocked response from OpenAI API
MOCKED_OPENAI_RESPONSE = {
    "choices": [
        {
            "message": {"content": "def add(a, b):\n    return a + b\n"},
            "finish_reason": "stop",
        }
    ],
    "usage": {"prompt_tokens": 100, "completion_tokens": 10, "total_tokens": 110},
}


@pytest.fixture
def mock_openai_client():
    with patch("scaf_code.scaffold_code.OpenAI") as mock:
        mock.return_value.chat.completions.create.return_value = MagicMock(
            **MOCKED_OPENAI_RESPONSE
        )
        yield mock.return_value


@pytest.fixture
def mock_file_io():
    with patch("builtins.open", new_callable=unittest.mock.mock_open) as mock_file:
        mock_file().read.side_effect = lambda: MOCKED_SPEC_FILE_CONTENT.get(
            Path(mock_file.call_args[0][0]).name, ""
        )
        yield mock_file


@pytest.fixture
def mock_path_exists():
    with patch("pathlib.Path.exists") as mock_exists:
        mock_exists.return_value = True
        yield mock_exists


def test_scaffold_code_with_spec_texts(
    mock_openai_client, mock_file_io, mock_path_exists
):
    result = scaffold_code(SPEC_TEXTS, None, None, OPTIONS)
    assert result == "def add(a, b):\n    return a + b\n"
    mock_openai_client.chat.completions.create.assert_called_once()


# ... (other tests remain unchanged, just add the mock_path_exists fixture to them)


def test_load_files(mock_file_io, mock_path_exists):
    texts = load_files(SPEC_FILES)
    assert texts == MOCKED_SPEC_FILE_CONTENT
