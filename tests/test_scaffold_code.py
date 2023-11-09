import pytest
from unittest.mock import patch, MagicMock, mock_open
from scaf_code.scaffold_code import (
    scaffold_code,
    load_files,
    create_inputs,
    DEFAULT_SYSTEM_PROMPT,
)
from openai import OpenAI
from pathlib import Path

# Mock data for testing
mock_spec_text = "Generate a function to add two numbers."
mock_spec_file_content = "Specification for adding two numbers."
mock_ref_file_content = "Reference implementation of math operations."
mock_output_code = "def add(a, b):\n    return a + b"

# Mock OpenAI response
mock_openai_response = {
    "choices": [{"message": {"content": mock_output_code}, "finish_reason": "stop"}],
    "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
}


@pytest.fixture
def mock_openai_client():
    with patch.object(OpenAI, "create_chat_completion") as mock_chat:
        mock_chat.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(content=mock_output_code), finish_reason="stop"
                )
            ]
        )
        yield mock_chat


def test_scaffold_code_with_spec_text(mock_openai_client):
    # Test scaffold_code function with specification text
    with patch("builtins.open", mock_open(mock_ref_file_content)):
        generated_code = scaffold_code(
            [mock_spec_text], options={"model_name": "test-model"}
        )
        assert generated_code == mock_output_code


def test_scaffold_code_with_spec_file(mock_openai_client):
    # Test scaffold_code function with specification file
    with patch("builtins.open", mock_open(read_data=mock_spec_file_content)):
        generated_code = scaffold_code(
            [], spec_files=["spec_file.txt"], options={"model_name": "test-model"}
        )
        assert generated_code == mock_output_code


def test_scaffold_code_with_ref_file(mock_openai_client):
    # Test scaffold_code function with reference file
    with patch("builtins.open", mock_open(read_data=mock_ref_file_content)):
        generated_code = scaffold_code(
            [mock_spec_text],
            ref_files=["ref_file.txt"],
            options={"model_name": "test-model"},
        )
        assert generated_code == mock_output_code


def test_load_files():
    # Test load_files function
    with patch("builtins.open", mock_open(read_data=mock_ref_file_content)):
        files_content = load_files(["ref_file.txt"])
        assert files_content == {"ref_file.txt": mock_ref_file_content}


def test_create_inputs():
    # Test create_inputs function
    inputs = create_inputs(
        [mock_spec_text],
        {"ref_file.txt": mock_ref_file_content},
        {"spec_file.txt": mock_spec_file_content},
    )
    expected_inputs = [
        {"role": "user", "content": f"==== Instruction ====\n\n{mock_spec_text}"},
        {
            "role": "user",
            "content": f"==== Instruction: spec_file.txt ====\n\n{mock_spec_file_content}",
        },
        {
            "role": "user",
            "content": f"==== Reference: ref_file.txt ====\n\n{mock_ref_file_content}",
        },
    ]
    assert inputs == expected_inputs


def test_scaffold_code_without_spec_or_ref(mock_openai_client):
    # Test scaffold_code function without specification or reference
    with pytest.raises(ValueError):
        scaffold_code([], options={"model_name": "test-model"})
