# AI Development Toolkit

Welcome to the AI Development Toolkit repository. This toolkit is designed to facilitate the development, interaction, and deployment of AI models, with a particular focus on GPT-4, through Python interfaces and automation scripts. It includes a simple yet highly usable CLI Chat Interface for OpenAI's GPT-4 and a basic README Generator script to streamline project documentation processes. Additionally, a CLI Chat Interface is offered for Mistral's Mixtral-8x7b.

## Features

- **CLI Chat Interface for OpenAI's GPT-4**: A user-friendly Python-based command-line interface for interacting with OpenAI's GPT-4 model. It supports multiline input, file upload, recursive directory upload, and enhanced output formatting.
- **CLI Chat Interface for Mistral's Mixtral-8x7b**: A user-friendly Python-based command-line interface for interacting with Mistral's Mixtral-8x7b model. It supports multiline input, file upload, recursive directory upload, and enhanced output formatting.
- **README Generator**: A Python script that automates the generation of `README.md` files for projects by processing text files within a directory and leveraging OpenAI's API for content creation.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- `openai`, `prompt_toolkit`, `rich`, and `tiktoken` Python packages for the GPT-4 Chat Interface
- `groq`, `prompt_toolkit`, `rich`, and `tiktoken` Python packages for the Mixtral-8x7b Chat Interface
- `openai` Python package for the README Generator
- Git for version control

### Installation

1. Clone this repository to your local machine.
2. Install the required Python packages for the respective tools you intend to use:

```bash
pip3 install -r chatbot_requirements.txt
pip3 install -r groqbot_requirements.txt
pip3 install -r readmemaker_requirements.txt
```

3. Configure your OpenAI API key as per the instructions [here](https://openai.com/api/).

### Usage

#### CLI Chat Interface for GPT-4

Navigate to the directory containing `chatbot.py` and run:

```bash
python3 chatbot.py
```

Follow the on-screen instructions to interact with GPT-4.

#### CLI Chat Interface for Mixtral-8x7b

Navigate to the directory containing `groqbot.py` and run:

```bash
python3 groqbot.py
```

Follow the on-screen instructions to interact with Mixtral-8x7b.

#### README Generator

Navigate to the directory containing `readmemaker.py` and run:

```bash
python3 readmemaker.py
```

The script will process text files in the directory and subdirectories, generating a `README.md` file.

## Contributing

Contributions to improve the toolkit or add new features are welcome. Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
