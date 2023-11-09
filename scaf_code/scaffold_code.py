from __future__ import annotations

from logging import getLogger
from pathlib import Path

from openai import OpenAI

logger = getLogger(__name__)


DEFAULT_SYSTEM_PROMPT = """
- You are a software developer. You are given a set of reference files and specification files. Your task is to generate code that satisfies the specification.
- Output the complete program code. Your output will be saved as a file. Therefore, never add any extra comments or code fences.
- Never omit it. If the maximum number of tokens is exceeded, the rest of the sequence will be called, so do not worry about it and write them in order from the beginning without omission.
""".strip()


def scaffold_code(
    spec_texts: list[str],
    spec_files: list[str | Path] = None,
    ref_files: list[str | Path] = None,
    options: dict[str, str] = None,
) -> str | None:
    """Scaffold code.

    Args:
        spec_texts: Specification texts.
        spec_files: Specification files.
        ref_files: Reference files.
        options: Options.
            model_name: Model name (default: gpt-4-1106-preview).
            system_prompt: System prompt (default: DEFAULT_SYSTEM_PROMPT).

    Returns: Scaffolded code.
    """
    logger.debug("Starting scaf_code")
    logger.debug("spec_texts: %s", spec_texts)
    logger.debug("spec_files: %s", spec_files)
    logger.debug("ref_files: %s", ref_files)
    logger.debug("options: %s", options)

    #
    spec_texts_from_files: dict[str, str] = load_files(spec_files)
    ref_texts: dict[str, str] = load_files(ref_files)  # file_name -> file_text
    inputs = create_inputs(spec_texts, ref_texts, spec_texts_from_files)
    if not inputs:
        logger.error("No input")
        return None

    options = options or {}
    model_name = options.get("model_name", "gpt-4-1106-preview")
    system_prompt = options.get("system_prompt") or DEFAULT_SYSTEM_PROMPT

    client = OpenAI()
    content = ""
    while True:
        response = client.chat.completions.create(
            model=model_name,
            temperature=0.0,
            messages=[
                {"role": "system", "content": system_prompt},
                *inputs,
            ],
        )
        res0 = response.choices[0]
        content += res0.message.content
        finish_reason = res0.finish_reason

        # output response.usage
        logger.info("response.usage: %s", response.usage)

        if finish_reason == "stop":
            break
        elif finish_reason == "length":
            inputs.append({"role": "assistant", "content": res0.message.content})
            logger.info("Continuing conversation")
        else:
            logger.error("Unexpected finish reason: %s", finish_reason)
            raise RuntimeError(f"Unexpected finish reason: {finish_reason}")

    return content


def create_inputs(
    spec_texts: list[str] | None,
    ref_texts: dict[str, str],
    spec_texts_from_files: dict[str, str],
) -> list[dict]:
    """create messages for chat.completions.create

    :param spec_texts:
    :param ref_texts: file_name -> file_text
    :param spec_texts_from_files: file_name -> file_text
    :return: list of messages: {"role": "user", "content": "..."}
    """
    inputs = []
    for spec_text in spec_texts or []:
        inputs.append(
            {"role": "user", "content": f"==== Instruction ====\n\n{spec_text}"}
        )
    for file, text in spec_texts_from_files.items():
        filename = Path(file).name
        inputs.append(
            {"role": "user", "content": f"==== Instruction: {filename} ====\n\n{text}"}
        )

    for ref_file, ref_text in ref_texts.items():
        filename = Path(ref_file).name
        inputs.append(
            {
                "role": "user",
                "content": f"==== Reference: {filename} ====\n\n{ref_text}",
            }
        )

    return inputs


def load_files(files: list[str | Path] | None) -> dict[str, str]:
    """Load files.

    Args:
        files: Files.

    Returns:
        File texts.
    """
    texts: dict[str, str] = {}
    for file in files or []:
        file_path = Path(file)
        if not file_path.exists():
            logger.error("File %s does not exist", file)
            raise FileNotFoundError(f"File {file} does not exist")
        with open(file, "rt") as f:
            texts[file] = f.read()
    return texts
