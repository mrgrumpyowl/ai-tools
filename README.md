# AI Development Toolkit

Welcome to the AI Development Toolkit repository. This toolkit is designed to facilitate the development, interaction, and deployment of AI models, through Python interface and automation scripts. It includes a fast, simple yet highly usable CLI Chat Interface for OpenAI's GPT-4o, Anthropic's Claude 3.5 Sonnet, and Mistral's Mixtral-8x7b. Plus a basic README Generator script to streamline project documentation processes. 

## Features

- **CLI Chat Interface for OpenAI's GPT-4o**: A user-friendly Python-based command-line interface for interacting with OpenAI's GPT-4o model. It supports multiline input, file upload, recursive directory upload, and enhanced output formatting.
- **CLI Chat Interface for Anthropic's Claude 3.5 Sonnet**: A user-friendly Python-based command-line interface for interacting with Anthropic's Claude 3.5 Sonnet model. It supports multiline input, file upload, recursive directory upload, and enhanced output formatting.
- **CLI Chat Interface for Mistral's Mixtral-8x7b**: A user-friendly Python-based command-line interface for interacting with Mistral's Mixtral-8x7b model. It supports multiline input, file upload, recursive directory upload, and enhanced output formatting.
- **README Generator**: A Python script that automates the generation of `README.md` files for projects by processing text files within a directory and leveraging OpenAI's API for content creation.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- `openai`, `prompt_toolkit`, `rich`, and `tiktoken` Python packages for the GPT-4o Chat Interface
- `anthropic`, `prompt_toolkit`, `rich`, and `tiktoken` Python packages for the Claude 3.5 Sonnet Chat Interface
- `groq`, `prompt_toolkit`, `rich`, and `tiktoken` Python packages for the Mixtral-8x7b Chat Interface
- `openai` Python package for the README Generator

## Installation and Usage (Manual)

1. Clone this repository to your local machine.
2. Install the required Python packages for the respective tools you intend to use:

```bash
pip3 install -r chatbot_requirements.txt
pip3 install -r claude_requirements.txt
pip3 install -r groqbot_requirements.txt
pip3 install -r readmemaker_requirements.txt
```

3. Create/configure your vendor API key(s):
   - OpenAI API key as per the instructions [here](https://openai.com/api/).  
   - Anthropic API key as per the instructions [here](https://docs.anthropic.com/en/api/getting-started).  
   - Groq's API key as per the instructions [here](https://console.groq.com/docs/quickstart).  

4. Export your API key(s) as an environment variable. 

- `chatbot.py` leverages the OpenAI API so to use `chatbot` you would have to add the following to your `.bashrc` or `.zshrc` file:
```export OPENAI_API_KEY="your-unique-key-here"```
- `claude.py` leverages the Anthropic API so to use `claude` you would have to add the following to your `.bashrc` or `.zshrc` file:
```export ANTHROPIC_API_KEY="your-unique-key-here"```
- `groqbot.py` leverages the Groq API so to use `groqbat` you would have to add the following to your `.bashrc` or `.zshrc` file:
```export GROQ_API_KEY="your-unique-key-here"```

### Usage

#### CLI Chat Interface for GPT-4o

Navigate to the directory containing `chatbot.py` and run:

```bash
python3 chatbot.py
```

Follow the on-screen instructions to interact with GPT-4o.

#### CLI Chat Interface for Claude 3.5 Sonnet

Navigate to the directory containing `claude.py` and run:

```bash
python3 claude.py
```

Follow the on-screen instructions to interact with Claude 3.5 Sonnet.

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

## Installation and Usage (pip)

You can install each project by navigating into its directory and running:

```bash
pip install .
```

Alternatively, you can run the `install_all` script:

```bash
python3 install_all.py
```

Either way, once done, each of the scripts can be invoked by name.

For more detailed instructions on installing specific versions of the individual scripts, please refer to the `README.md` files in the subdirectories.
