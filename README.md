# scaf_code

scaf_code is an innovative command-line tool designed to streamline the process of generating code. By leveraging the capabilities of Large Language Models, scaf_code can transform your reference and specification files into working code that meets your project's requirements.

## Features

- **Code Generation**: Generate code that adheres to your specifications using reference files.
- **Support for Images**: Include images as references for visual specifications.
- **Customizable**: Use command-line options to tailor the code generation process to your needs.
- **Easy to Install**: Get started quickly with a simple pip command.
- **Refinement**: Refine existing code by providing additional context or corrections.

## Installation

To install scaf_code, run the following command in your terminal:

```bash
pip install scaf_code
```

## Configuration

Before using scaf_code, you need to set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=<your_openai_api_key>
```

## Usage

To use scaf_code, you'll need to provide reference files, a specification, and an output path. Here's the basic syntax:

```bash
scaf_code --ref <ref_file>... --spec "<spec_text>" --out <output_path>
```

You can also specify a specification file instead of inline text:

```bash
scaf_code --ref <ref_file>... --spec-file <spec_file> --out <output_path>
```

To refine existing code, provide the file to be refined along with the reference files and specification:

```bash
scaf_code --refine <refine_file> --ref <ref_file>... --spec "<spec_text>"
```

The `--refine` option allows you to improve or modify existing code. When using this option, scaf_code will take the provided file and apply the changes specified in the specification text. This is particularly useful for optimizing code, fixing bugs, or adding new features.

When refining code, you can use the `--no-backup` option to prevent scaf_code from creating a backup of the original file. This is useful if you are confident in the changes being made and do not require a backup.

### Options

- `--ref`: One or more reference files. Images are supported with `.jpg`, `.png`, `.gif`, and `.webp` extensions.
- `--spec`: The specification text describing what code to generate.
- `--spec-file`: A file containing the specification text.
- `--out`: The path to the output file where the generated code will be saved.
- `--refine`: The file to be refined. This option is used to refine existing code.
- `--no-backup`: Do not create a backup of the original file when using the `--refine` option.

## Examples

### Generating Code from Text Specifications

To generate a Python test file based on existing code files and a text specification:

```bash
scaf_code --out tests/test_scaffold_code.py --ref scaf_code/cli.py scaf_code/scaffold_code.py --spec "write pytest to scaf_code.scaffold_code.py"
```

### Using Images as References

To generate code that processes an image according to an algorithm specified in a reference image:

```bash
scaf_code --out tests/test_image_processing.py --ref image_processing_algorithm.jpg --spec "write a function to process an image according to the algorithm specified in the reference image"
```

### Refining Existing Code

To refine an existing Python script with additional specifications:

```bash
scaf_code --refine existing_script.py --ref additional_context.py --spec "optimize the existing function for better performance"
```

To refine the script without creating a backup file:

```bash
scaf_code --refine existing_script.py --ref additional_context.py --spec "optimize the existing function for better performance" --no-backup
```

## Contributing

Contributions are welcome! If you have ideas for improvements or have found a bug, please open an issue or submit a pull request on our [GitHub repository](https://github.com/mokemokechicken/scaf_code).

## License

scaf_code is released under the [MIT License](https://mokemokechicken.mit-license.org/). 

## Support

If you need help or have any questions, please open an issue on the GitHub repository, and we'll do our best to assist you.

Happy coding!