# README Generator

This repository contains a Python script designed to automate the process of generating a `README.md` file for a project by collecting and processing all text files within a given directory structure and using OpenAI's API to compose a comprehensive README.

## Features

- **Text File Detection:** Identifies and filters text files within a directory to ensure only relevant content is processed.
- **Content Aggregation:** Gathers and concatenates the content of all identified text files.
- **OpenAI Integration:** Utilizes OpenAI's API to generate a README.md file based on the aggregated content.
- **Customizability:** Easy to modify for different output formats or to integrate with other APIs or tools.

## Requirements

- Python 3.6+
- `openai` Python package
- An API key from OpenAI

## Setup

1. Ensure you have Python 3.6 or higher installed on your system.
2. Install the required Python package using pip:

```bash
pip install openai
```

3. Obtain an API key from [OpenAI](https://openai.com/) and configure it as per the `openai` package's documentation.

## Usage

1. Clone this repository to your local machine.
2. Run the script:

```bash
python3 readmemaker.py
```

3. The script will prompt you for the local root directory of the repository that you want to create a README for. 
4. The script will recursively process all text files in the directory you provide, and its subdirectories, sending the combined content to OpenAI's API, which returns a generated README. This README will be saved as `README.md` in the same directory that you provided. Note that it will overwrite any existing `README.md` file that already exists in that directory.

## Customization

You can modify the script to change the way files are processed or the criteria for what constitutes a text file. You can also adjust the prompt sent to OpenAI's API to better suit your project's needs or to generate different types of documentation.

## Contributing

Contributions are welcome! If you have suggestions for improvements or encounter any issues, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.


This README.md template provides a basic structure for documenting the Python script's functionality, setup, usage, and customization options, along with sections for contributing and licensing. Adjust the content as necessary to fit the specific details and requirements of your project.
