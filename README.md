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

## Example

```bash
scaf_code --out tests/test_scaffold_code.py --ref scaf_code/cli.py scaf_code/scaffold_code.py  --spec "write pytest to scaf_code.scaffold_code.py"
```