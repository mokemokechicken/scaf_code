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
    out_file: str,
    ref_files: list[str] = None,
    options: dict[str, str] = None,
) -> bool:
    """Scaffold code.

    Args:
        spec_texts: Specification texts.
        out_file: Output file.
        ref_files: Reference files.
        options: Options.
            model_name: Model name (default: gpt-4-1106-preview).
            system_prompt: System prompt (default: DEFAULT_SYSTEM_PROMPT).

    Returns:
        True if successful, False otherwise.
    """
    logger.debug("Starting scaf_code")
    ref_texts: dict[str, str] = load_files(ref_files)  # file_name -> file_text
    inputs = create_inputs(spec_texts, ref_texts)
    if not inputs:
        logger.error("No input")
        return False

    options = options or {}
    model_name = options.get("model_name", "gpt-4-1106-preview")
    system_prompt = options.get("system_prompt", DEFAULT_SYSTEM_PROMPT)

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

    logger.debug("Writing output to %s", out_file)
    output_to_file(out_file, content)

    return True


def create_inputs(
    spec_texts: list[str] | None, ref_texts: dict[str, str]
) -> list[dict]:
    """create messages for chat.completions.create

    :param spec_texts:
    :param ref_texts:
    :return: list of messages: {"role": "user", "content": "..."}
    """
    inputs = []
    for spec_text in spec_texts or []:
        inputs.append(
            {"role": "user", "content": f"==== Instruction ====\n\n{spec_text}"}
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


def load_files(files: list[str] | None) -> dict[str, str]:
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


def output_to_file(file: str, content: str) -> None:
    """Output to file.

    Args:
        file: File.
        content: Content.
    """
    file_path = Path(file)
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file, "wt") as f:
            f.write(content)
    except Exception as e:
        logger.error("Failed to write to file %s: %s", file, e)
        print("==== Output ====")
        print(content)
        print("==== Output ====")
        raise e
