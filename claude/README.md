# CLI Chat Interface for Claude 3 Opus

This project provides a simple CLI chat interface to interact with Anthropic's Claude 3 Opus model. It utilizes the `anthropic` Python package to communicate with the Claude 3 Opus via the API and provides a user-friendly command-line interface for submitting prompts and receiving responses.

## Features

- Multiline input support for detailed prompts.
- Real-time response loading indicator.
- Graceful exit options.
- Enhanced output formatting with `rich` and `prompt_toolkit` libraries.
- Supports uploading individual files by entering "Upload: ~/path/to/file_name"
- Supports uploading an entire directory and its contents recursively by entering "Upload: ~/path/to/directory"
- Note that the upload features are designed primarily for code repository analysis so supports only utf-8 encoded files.

## Prerequisites

Before you start, ensure you have installed the following:
- Python 3.10 or higher
- `anthropic` Python package
- `prompt_toolkit` Python package
- `rich` Python package
- `tiktoken` Python package
- `tree` command-line utility

## Installation

1. Clone this repository to your local machine.
2. Install the required Python packages by running:

```bash
pip3 install anthropic prompt_toolkit rich tiktoken
```

3. Set up your Anthropic by following the instructions [here](https://anthropic.com/api/).
4. Once you have your Anthropic, export your OpenAI key as an environment variable in `.zshrc` or `.bashrc` like this:

```
export ANTHROPIC_API_KEY='sk-ant-api-yourkeyhere'
```

## Usage

To start the chat interface, navigate to the directory containing the script and make it executable:

```bash
chmod +x claude.py
```

Then you can just run it with: 

```
./claude.py
```

Follow the on-screen instructions for submitting prompts to Claude 3 Opus.

Nb. If you like the script and want to put it in the way of your PATH so that you can run it from wherever, just add a symbolic link pointing `/usr/local/bin`.

For example (on MacOS): 

```bash
sudo ln -s /Users/username/mrgrumpyowl/ai-tools/chatbot/claude.py /usr/local/bin/claude
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
