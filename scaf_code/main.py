"""Main entry point for scaf_code.

scaf_code is a tool for generating code from reference and specification files by Large Language Models.

About:
    This module is the main entry point for scaf_code. It contains the main function
    and the command line interface.

example:
    scaf_code --ref ref_code_file --ref ref_base_spec_file --spec spec_text --out out_file_path
"""
from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

from scaf_code.scaffold_code import scaffold_code


def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="scaf_code is a tool for generating code from reference and specification files by Large Language Models."
    )
    parser.add_argument(
        "--ref",
        dest="ref",
        type=Path,
        nargs="*",
        required=False,
        help="Reference files.",
    )
    parser.add_argument(
        "--spec",
        dest="spec",
        type=str,
        nargs="*",
        help="Specification Text.",
    )
    parser.add_argument(
        "--out",
        dest="out",
        type=Path,
        required=True,
        help="Output file.",
    )
    parser.add_argument(
        "--log-level",
        dest="log_level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level.",
    )
    # --model-name
    parser.add_argument(
        "--model-name",
        dest="model_name",
        type=str,
        default="gpt-4-1106-preview",
        help="Model name.",
    )
    # --system-prompt
    parser.add_argument(
        "--system-prompt",
        dest="system_prompt",
        type=Path,
        default="",
        help="System prompt.",
    )

    return parser.parse_args(args)


def main(args: list[str]) -> bool:
    """Main entry point for scaf_code.

    required:
        OPENAI_API_KEY environment variable must be set.

    Args:
        args: Command line arguments.
    """
    args = parse_args(args)
    logging.basicConfig(level=args.log_level)
    logging.debug("Starting scaf_code")
    logging.debug("Arguments: %s", args)

    # check if OPENAI_API_KEY environment variable is set
    if "OPENAI_API_KEY" not in os.environ:
        logging.error("OPENAI_API_KEY environment variable must be set")
        raise EnvironmentError("OPENAI_API_KEY environment variable must be set")

    # check if ref or spec are set
    if not args.ref and not args.spec:
        print("Please specify either --ref or --spec")
        return False

    system_prompt = None
    if args.system_prompt:
        system_prompt = args.system_prompt.read_text()

    # Compare this snippet from scaf_code/scaffold_code.py:
    options = {"model_name": args.model_name, "system_prompt": system_prompt}
    scaffold_code(args.spec, args.out, args.ref, options)

    return True


if __name__ == "__main__":
    import sys

    sys.exit(0 if main(sys.argv[1:]) else 1)
