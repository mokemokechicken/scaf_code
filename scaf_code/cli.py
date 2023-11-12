"""Main entry point for scaf_code.

scaf_code is a tool for generating code from reference and specification files by Large Language Models.

About:
    This module is the main entry point for scaf_code. It contains the main function
    and the command line interface.

Example:

ex1) specify reference and specification text
    scaf_code --ref ref_code_file ref_base_spec_file --spec spec_text --out out_file_path

ex2) specify reference and specification files
    scaf_code --ref ref_code_file ref_base_spec_file --spec-file spec_file --out out_file_path

ex3) refine code
    scaf_code --refine refine_file --spec spec_text --ref ref_code_file
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

import scaf_code
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
        "--spec-file",
        dest="spec_file",
        type=Path,
        nargs="*",
        help="Specification files.",
    )
    parser.add_argument(
        "--out",
        dest="out",
        type=Path,
        required=False,
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
        help="Model name.",
    )
    # --system-prompt
    parser.add_argument(
        "--system-prompt",
        dest="system_prompt",
        type=Path,
        help="path to system prompt file.",
    )
    # --refine
    parser.add_argument(
        "--refine",
        dest="refine",
        type=Path,
        help="Refine file.",
    )
    # --no-backup
    parser.add_argument(
        "--no-backup",
        dest="no_backup",
        action="store_true",
        help="Do not backup to .bak file when --refine is specified.",
    )
    # --version
    parser.add_argument(
        "--version",
        action="version",
        version=f"scaf_code {scaf_code.__version__}",
    )

    return parser.parse_args(args)


def _main(args: list[str]) -> bool:
    """Main entry point for scaf_code.

    required:
        OPENAI_API_KEY environment variable must be set.

    Args:
        args: Command line arguments.
    """
    args = parse_args(args)
    logging.basicConfig(level=args.log_level)
    logging.info(f"ref: {args.ref}")
    logging.info(f"spec: {args.spec}")
    logging.info(f"spec_file: {args.spec_file}")
    logging.info(f"out: {args.out}")
    logging.info(f"refine: {args.refine}")
    if args.model_name:
        logging.info(f"model_name: {args.model_name}")
    if args.system_prompt:
        logging.info(f"system_prompt: {args.system_prompt}")

    # check if OPENAI_API_KEY environment variable is set
    if "OPENAI_API_KEY" not in os.environ:
        logging.error("OPENAI_API_KEY environment variable must be set")
        raise EnvironmentError("OPENAI_API_KEY environment variable must be set")

    # check if ref or spec are set
    if not args.ref and not args.spec and not args.spec_file:
        print("Please specify either --ref or --spec or --spec-file")
        return False

    # check if out or refine are set
    if not args.out and not args.refine:
        print("Please specify either --out or --refine")
        return False

    # check if out and refine are set
    if args.out and args.refine:
        print("Please specify either --out or --refine")
        return False

    options = {}
    if args.model_name:
        options["model_name"] = args.model_name

    if args.system_prompt:
        logging.debug("Reading system prompt from %s", args.system_prompt)
        options["system_prompt"] = args.system_prompt.read_text()

    # Handle --refine option
    if args.refine:
        if args.ref:
            args.ref = [args.refine] + args.ref
        else:
            args.ref = [args.refine]
        args.out = args.refine
        options["refine_mode"] = True
        if args.no_backup:
            options["no_backup"] = True

    # Compare this snippet from scaf_code/scaffold_code.py:
    content = scaffold_code(args.spec, args.spec_file, args.ref, options)
    if not content:
        return False
    else:
        backup = options.get("refine_mode", False) and not options.get("no_backup", False)
        output_to_file(args.out, content, backup=backup)
        return True


def output_to_file(file: str | Path, content: str, backup: bool = False) -> None:
    """Output to file.

    Args:
        file: File.
        content: Content.
        backup: Backup.

    if backup is True, backup file to file.bak
    """
    file_path = Path(file)
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if backup and file_path.exists():
            # rename xxx.py to xxx.py.bak
            file_path.rename(file_path.with_suffix(file_path.suffix + ".bak"))
        with open(file, "wt") as f:
            f.write(content)
    except Exception as e:
        print("==== Output ====")
        print(content)
        print("==== Output ====")
        raise e


def main():
    sys.exit(0 if _main(sys.argv[1:]) else 1)


if __name__ == "__main__":
    main()
