# Python Chat Interface for GPT-4

This project provides a simple CLI chat interface to interact with OpenAI's GPT-4 model. It utilizes the `openai` Python package to communicate with the GPT-4 API and provides a user-friendly command-line interface for submitting prompts and receiving responses.

## Features

- Multiline input support for detailed prompts.
- Real-time response loading indicator.
- Graceful exit options.
- Enhanced output formatting with `rich` and `prompt_toolkit` libraries.
- Supports uploading whole (utf-8 encoded) files by entering "Upload: ~/path/to/file_name"

## Prerequisites

Before you start, ensure you have installed the following:
- Python 3.6 or higher
- `openai` Python package
- `prompt_toolkit` Python package
- `rich` Python package
- `tiktoken` Python package

## Installation

1. Clone this repository to your local machine.
2. Install the required Python packages by running:

```bash
pip install openai prompt_toolkit rich tiktoken
```

3. Set up your OpenAI API key by following the instructions [here](https://openai.com/api/).
4. Once you have your OpenAI API key, export your OpenAI key as an environment variable in `.zshrc` or `.bashrc` like this:

```
export OPENAI_API_KEY='sk-yourkeyhere'
```

## Usage

To start the chat interface, navigate to the directory containing the script and make it executable:

```bash
chmod +x chatbot.py
```

Then you can just run it with: 

```
./chatbot.py
```

Follow the on-screen instructions for submitting prompts to GPT-4.

Nb. If you like the script and want to put it in the way of your PATH so that you can run it from wherever, just add a symbolic link pointing `/usr/local/bin`.

For example: 

```bash
sudo ln -s /Users/gfalkingham/gitnet/gfalkingham_wh/ai/chatbot/chatbot.py /usr/local/bin/chatbot
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
