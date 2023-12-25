import os
from pathlib import Path
from unittest.mock import patch, mock_open
import argparse

import pytest

from scaf_code.cli import parse_args, _main, output_to_file


# Test cases for parse_args function
def test_parse_args_with_ref_and_spec():
    args = [
        "--ref",
        "ref_code_file",
        "ref_base_spec_file",
        "--spec",
        "spec_text",
        "--out",
        "out_file_path",
    ]
    parsed_args = parse_args(args)
    assert parsed_args.ref == [Path("ref_code_file"), Path("ref_base_spec_file")]
    assert parsed_args.spec == ["spec_text"]
    assert parsed_args.out == Path("out_file_path")


def test_parse_args_with_spec_file():
    args = ["--spec-file", "spec_file", "--out", "out_file_path"]
    parsed_args = parse_args(args)
    assert parsed_args.spec_file == [Path("spec_file")]
    assert parsed_args.out == Path("out_file_path")


def test_parse_args_with_log_level():
    args = ["--out", "out_file_path", "--log-level", "DEBUG"]
    parsed_args = parse_args(args)
    assert parsed_args.log_level == "DEBUG"


def test_parse_args_with_model_name():
    args = ["--out", "out_file_path", "--model-name", "custom-model"]
    parsed_args = parse_args(args)
    assert parsed_args.model_name == "custom-model"


def test_parse_args_with_system_prompt():
    args = ["--out", "out_file_path", "--system-prompt", "system_prompt_file"]
    parsed_args = parse_args(args)
    assert parsed_args.system_prompt == Path("system_prompt_file")


# Test cases for _main function
@patch("scaf_code.cli.parse_args")
@patch("scaf_code.cli.scaffold_code")
@patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
def test_main_success(mock_scaffold_code, mock_parse_args):
    mock_parse_args.return_value = argparse.Namespace(
        ref=[Path("ref_code_file"), Path("ref_base_spec_file")],
        spec=["spec_text"],
        spec_file=None,
        out=Path("out_file_path"),
        log_level="INFO",
        model_name="gpt-4-1106-preview",
        system_prompt=None,
        refine=False,
    )
    mock_scaffold_code.return_value = "generated code"
    with patch("builtins.open", mock_open()) as mock_file:
        assert _main([]) is True
        mock_file.assert_called_once_with(Path("out_file_path"), "wt")
        mock_file().write.assert_called_once_with("generated code")


@patch("scaf_code.cli.parse_args")
@patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
def test_main_no_ref_spec_spec_file(mock_parse_args):
    mock_parse_args.return_value = argparse.Namespace(
        ref=None,
        spec=None,
        spec_file=None,
        out=Path("out_file_path"),
        log_level="INFO",
        model_name="gpt-4-1106-preview",
        system_prompt=None,
        refine=False,
    )
    assert _main([]) is False


@patch("scaf_code.cli.parse_args")
@patch.dict(os.environ, {}, clear=True)
def test_main_missing_api_key(mock_parse_args):
    mock_parse_args.return_value = argparse.Namespace(
        ref=[Path("ref_code_file"), Path("ref_base_spec_file")],
        spec=["spec_text"],
        spec_file=None,
        out=Path("out_file_path"),
        log_level="INFO",
        model_name="gpt-4-1106-preview",
        system_prompt=None,
        refine=False,
    )
    with pytest.raises(EnvironmentError) as e:
        _main([])
    assert "OPENAI_API_KEY environment variable must be set" in str(e.value)


# Test cases for output_to_file function
def test_output_to_file_success():
    content = "test content"
    with patch("builtins.open", mock_open()) as mock_file:
        output_to_file("test_file.txt", content)
        mock_file.assert_called_once_with("test_file.txt", "wt")
        mock_file().write.assert_called_once_with(content)


def test_output_to_file_exception():
    content = "test content"
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = IOError
        with pytest.raises(IOError):
            output_to_file("test_file.txt", content)
