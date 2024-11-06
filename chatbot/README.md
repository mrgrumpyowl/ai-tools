# CLI Chat Interface for LLMs made by OpenAI and Anthropic

This project provides a simple CLI chat interface to interact with Anthropic's and OpenAI's state of the art large language models. It utilizes the `openai` Python package to communicate with the OpenAI API and the `anthropic` Python package to communicate with the Anthropic API. Chatbot provides a user-friendly command-line interface for submitting prompts and receiving responses, with support for multiline inputs, file analysis, and chat history management.  

This project proudly offers the user a "Bring Your Own Key" (BYOK) means of LLM access with personal autonomy and privacy baked in. Chatbot runs locally and stores your chat history under your user's home directory. All LLM calls are made with your own API key(s) which Chatbot assumes are exported as local environment variables.  


## Features

- **Multiple Model Support**
  - OpenAI o1 Preview
  - GPT-4o (tracking latest)
  - GPT-4o (2024/8/6 snapshot)
  - GPT-4o-mini
  - GPT-4-Turbo
  - Claude 3.5 Haiku
  - Claude 3.5 Sonnet v2
  - Claude 3 Opus

- **Advanced Capabilities**
  - Multiline input support for detailed prompts.
  - Real-time response loading indicator.
  - Graceful exit options.
  - Enhanced output formatting with `rich` and `prompt_toolkit` libraries.
  - Supports uploading individual files by entering "Upload: ~/path/to/file_name"
  - Supports uploading an entire directory and its contents recursively by entering "Upload: ~/path/to/directory"
  - Note that the upload features are designed primarily for code repository analysis so supports only utf-8 encoded files.
  - Stores chat history in `~/.chatbot/chat-history/` and can resume a previous conversation if the user desires.
  - Optional web search integration via Perplexity API

## Prerequisites

Before you start, ensure you have installed the following:

- Python 3.10 or higher
- `anthropic` Python package
- `openai` Python package
- `prompt_toolkit` Python package
- `rich` Python package
- `tiktoken` Python package
- `tree` command-line utility

Web search requires `PERPLEXITY_API_KEY` environment variable (optional)  

## Installation

### Manual
<!-- markdownlint-disable MD029-->
1. Clone this repository to your local machine.

```bash
# Clone the repository
git clone https://github.com/mrgrumpyowl/ai-tools.git
cd ai-tools

# Ensure the script executable
chmod +x ./chatbot/chatbot.py
```

2. Install the required Python packages by running:

```bash
# Install dependencies
pip3 install -r chatbot/requirements.txt
```

3.1. Set up your OpenAI API key by following the instructions [here](https://openai.com/api/).
3.2. Once you have your OpenAI API key, export your OpenAI key as an environment variable in `.zshrc` or `.bashrc` like this:
<!-- markdownlint-enable MD029-->

```bash
export OPENAI_API_KEY='sk-yourkeyhere'
```

4.1. Set up your Anthropic by following the instructions [here](https://anthropic.com/api/).
4.2. Once you have your Anthropic, export your OpenAI key as an environment variable in `.zshrc` or `.bashrc` like this:
<!-- markdownlint-enable MD029-->

```bash
export ANTHROPIC_API_KEY='sk-ant-api-yourkeyhere'
```

## Usage

### Basic Usage

```bash
./chatbot.py
```

### Command Line Options

```bash
chatbot [-h] [-m [MODEL]] [-ws]

options:
  -h, --help            show this help message and exit
  -m [MODEL], --model-select [MODEL]
                        Select the AI model to use. Options:
                          - Specify a model name directly
                          - Use without a value to show the model selection menu
                          - Omit to use the default model (chatgpt-4o-latest)
  -ws, --web-search     Enable web search functionality for answering queries.
```

### Model Selection

By default, chatbot will attempt to use the latest version of the ChatGPT-4o model.  
However, you can use the `-m` or `--model-select` argument to choose a different model.  


### File Analysis

```bash
# In the chat interface:
Upload: ~/path/to/file.py    # Analyse single file
Upload: ~/path/to/directory  # Analyse entire directory
```

### Adding to PATH

Nb. If you like the script and want to put it in the way of your PATH so that you can run it from wherever, just add a symbolic link pointing `/usr/local/bin`.

For example (on MacOS):

```bash
sudo ln -s /Users/username/mrgrumpyowl/ai-tools/chatbot/chatbot.py /usr/local/bin/chatbot
```

### Pip install

Latest:

```bash
pip3 install git+https://gitlab.com/williamhillplc/technical-services/public-cloud/python-packages/tf-plan-summary.git@master --upgrade
```

Specific Version:

```bash
pip3 install git+https://gitlab.com/williamhillplc/technical-services/public-cloud/python-packages/tf-plan-summary.git@1.0.0 --upgrade
```

Whatever the code currently looks like while you're developing it (and assuming you're cd'd into this directory):

```bash
pip3 uninstall tf-plan-summary
pip3 install ./ --upgrade
```

>NOTE: You need to uninstall first if you already have it installed or pip will use the cached files from the last time you installed it.

## Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
