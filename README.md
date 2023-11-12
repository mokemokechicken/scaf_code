# About

scaf_code is a tool for generating code from reference and specification files by Large Language Models.

# Usage

## Install

```bash
pip install scaf_code
```

## Run

```bash
export OPENAI_API_KEY=<your_openai_api_key>
scaf_code --ref <ref_file> <ref_file> --spec-file <spec_file> --out <output_path>
```

The `--ref` option now supports image inputs. The tool determines whether a file is an image based on its extension.

Supported image formats are `.jpg`, `.png`, `.gif`, and `.webp`.

## Example

```bash
scaf_code --out tests/test_scaffold_code.py --ref scaf_code/cli.py scaf_code/scaffold_code.py  --spec "write pytest to scaf_code.scaffold_code.py"
```

To include an image as a reference, simply pass the image file with the appropriate extension:

```bash
scaf_code --out tests/test_image_processing.py --ref image_processing_algorithm.jpg --spec "write a function to process an image according to the algorithm specified in the reference image"
```