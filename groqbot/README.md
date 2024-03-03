# CLI Chat Interface for Mixtral-8x7b

This project provides a simple CLI chat interface to interact with Mistral's Mixtral-8x7b model. It utilizes the `groq` Python package to communicate with the Groq API and provides a user-friendly command-line interface for submitting prompts and receiving responses.

This is essentially a clone of the original 'chatbot' in this repository. It makes use of Groq's clone of the OpenAI API Python SDK to provide a Mixtral model variant of the chatbot at very little effort to me, the developer. 

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
- `groq` Python package
- `prompt_toolkit` Python package
- `rich` Python package
- `tiktoken` Python package

## Installation

1. Clone this repository to your local machine.
2. Install the required Python packages by running:

```bash
pip3 install groq prompt_toolkit rich tiktoken
```

3. Set up your Groq API key by following the instructions [here](https://console.groq.com/docs/quickstart).
4. Once you have your Groq API key, export your Groq key as an environment variable in `.zshrc` or `.bashrc` like this:

```
export GROQ_API_KEY='gsk-yourkeyhere'
```

## Usage

To start the chat interface, navigate to the directory containing the script and make it executable:

```bash
chmod +x groqbot.py
```

Then you can just run it with: 

```
./groqbot.py
```

Follow the on-screen instructions for submitting prompts to GPT-4.

Nb. If you like the script and want to put it in the way of your PATH so that you can run it from wherever, just add a symbolic link pointing `/usr/local/bin`.

For example (on MacOS): 

```bash
sudo ln -s /Users/username/mrgrumpyowl/ai-tools/groqbot/groqbot.py /usr/local/bin/groqbot
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
