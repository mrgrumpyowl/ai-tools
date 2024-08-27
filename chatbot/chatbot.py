#!/usr/bin/env python3

import argparse
import fnmatch
import json
import os
import sys
import threading
import tiktoken
import time
import subprocess

from datetime import datetime

from openai import OpenAI
from anthropic import Anthropic

from prompt_toolkit import prompt
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import HTML

from rich import print
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.rule import Rule

from model_config import get_model_list, get_model_config

console = Console(highlight=False)
current_chat_file = None

def ensure_chat_history_dir():
    """Ensures that the chat history directory exists."""
    home_dir = os.path.expanduser("~")
    chat_history_base_dir = os.path.join(home_dir, '.chatbot', 'chat-history')
    os.makedirs(chat_history_base_dir, exist_ok=True)
    return chat_history_base_dir

def get_todays_chat_dir(base_dir):
    """Returns today's chat directory, creating it if necessary."""
    today = datetime.now().strftime("%Y-%m-%d")
    todays_chat_dir = os.path.join(base_dir, today)
    os.makedirs(todays_chat_dir, exist_ok=True)
    return todays_chat_dir

def save_chat(chat_data, chat_dir):
    global current_chat_file
    """Saves current chat data to the session file."""
    if not current_chat_file:
        time_stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{time_stamp}.json"
        current_chat_file = os.path.join(chat_dir, filename)

    with open(current_chat_file, 'w', encoding='utf-8') as f:
        json.dump(chat_data, f, ensure_ascii=False, indent=4)

def load_chat(file_path):
    """Loads chat data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def select_chat_file(chat_dir):
    """Provides a UI to select an old chat file from available files."""
    files = []
    for subdir, dirs, files_in_dir in os.walk(chat_dir):
        for file in files_in_dir:
            if file.endswith('.json'):
                full_path = os.path.join(subdir, file)
                files.append(full_path)
    files = sorted(files, reverse=True)[:20]

    if not files:
        print("No previous chats available.")
        return None

    console.print(f"[bold cyan]\nHere are the most recent chats (up to 20) sorted by most recent first:[/]")
    for idx, file in enumerate(files):
        display_name = os.path.splitext(os.path.basename(file))[0]
        print(f"{idx + 1}) {display_name}")

    print("\nSelect a file to resume (number), or press Enter for the most recent chat: ")
    user_input = input().strip()
    if user_input == "":
        # Default to the first file if user just presses enter
        return files[0]

    try:
        choice = int(user_input) - 1
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

    if 0 <= choice < len(files):
        return files[choice]
    else:
        print("Invalid choice. Please select a valid file number.")
        return None

def main_menu():
    """Show the main menu to the user and handle the choice."""
    first_menu = ("\n1) Start New Chat\n2) Resume Recent Chat")
    console.print(f"[bold blue]{first_menu}[/]")
    choice = input(f"\nChoose (1-2): ")
    return choice.strip()

def get_user_input() -> str:
    """Display the prompt to the user for multiline input.
    The user can press Esc followed by Enter to submit their input."""
    text = HTML('<u><b><style fg="ansiblue">User:</style></b></u>')
    user_input = prompt(print_formatted_text(text), multiline=True)
    return user_input

def detect_file_analysis_request(content: str) -> tuple[bool, str, bool]:
    if content.startswith("Upload:"):
        path = content[len("Upload: "):].strip()
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            return True, path, True  # Indicates a directory
        return True, path, False  # Indicates a file
    return False, "", False

def should_ignore(file_path):
    ignore_patterns = [
        '*/.terraform/*', '.terraform',
        '*/.terragrunt-cache/*', '.terragrunt-cache',
        '*.tfstate', '*.tfstate*',
        '*/.tfsec/*', '.tfsec',
        '.vmc-makefile', '*/.centralized-makefile',
        'Pipfile', '*/Pipfile', 'Pipfile.lock', '*/Pipfile.lock',
        '.test-plans', '*/.test-plans', '.cache', '*/.cache',
        '*.pyc', '*/*.pyc', '*.pyo', '*/*.pyo', '*.zip', '*/*.zip',
        '__pycache__', '*/__pycache__', '.tox', '*/.tox',
        '*.egg-info', '*/*.egg-info', '.coverage', '*/.coverage',
        '.pytest_cache', '*/.pytest_cache', 'nosetests.xml', '*/nosetests.xml',
        'coverage.xml', '*/coverage.xml', 'htmlcov/', '*/htmlcov/',
        'report.xml', '*/report.xml', 'build/*', '*/build/*', 'dist/*',
        '*/dist/*', 'test-generated*.yml', '*/test-generated*.yml',
        '.DS_Store', '._.DS_Store', '.librarian', '.idea', '.vscode',
        '.history', '*swp', '.envrc', '.direnv', '.editorconfig',
        '.external_modules', 'modules/*', '.terraform.lock.hcl', '*.png',
        '*.jpg', '*.jpeg', '*.bmp', '.test-data', '*.plan', '*plan.out',
        '*plan.summary', '*/.git/hooks', '*/.git/info', '*/.git/logs',
        '*/.git/objects', '*/.git/refs', '*/.gitignore', '*/.git-credentials',
        '*/manifest.json', '.checkov.yaml', '*/saml/*'
    ]
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def is_binary(file_path):
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)  # Read the first 1024 bytes
            return b'\x00' in chunk  # Look for a NULL byte
    except Exception:
        return True  # If there's an error reading the file, treat it as binary

def get_directory_tree_structure(dir_path: str) -> str:
    """Returns the output of `tree -d` command on the specified directory path"""
    command = ["tree", "-d", dir_path]
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute `tree -d` on {dir_path}: {e}")
        return ""

def generate_markdown_from_directory(root_dir) -> tuple[str, int]:
    markdown_output = ""
    token_count = 0

    tree_structure = get_directory_tree_structure(root_dir)
    markdown_output += (f"# Directory Analysis for {root_dir}\n\n"
                        f"## Directory Structure as shown by the output of the `tree -d` command\n\n"
                        f"```\n{tree_structure}\n```\n\n")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if not should_ignore(os.path.join(dirpath, d))]
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            relative_file_path = os.path.relpath(file_path, start=root_dir)
            if not should_ignore(file_path) and not is_binary(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    # Determine the appropriate enclosure based on the file extension
                    enclosure = "```"
                    if filename.endswith('.md'):
                        enclosure = '"""'

                    markdown_output += f"## {relative_file_path}\n\n{enclosure}\n{content}\n{enclosure}\n\n"
                    token_count = estimate_token_count(markdown_output)
                    if token_count > 100000:
                        markdown_output = f"DIRECTORY TOO BIG."
                    else:
                        markdown_output = markdown_output
    return markdown_output, token_count

def read_file_contents(file_path: str) -> tuple[str, str, int]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_name = os.path.basename(file_path)
            file_contents = file.read()
            if not file_contents:
                return file_name, False, 0
            token_count = estimate_token_count(file_contents)
            if token_count > 64000:
                return file_name, f"FILE TOO BIG.", token_count
            return file_name, file_contents, token_count
    except Exception as e:
        print(f"\nError reading file: {e}")
        return "", f'I attempted to upload a file but it failed. For your next response reply ONLY: "No file was uploaded."', 0

def estimate_token_count(content: str) -> int:
    """Returns the number of tokens as an int."""
    encoding = tiktoken.encoding_for_model("gpt-4")
    num_tokens = len(encoding.encode(content))
    return num_tokens

def should_exit(content: str) -> bool:
    return content.lower() == "exit"

def append_message(messages: list, role: str, content: str):
    messages.append({"role": role, "content": content})

def spinner():
    spinner_chars = "|/-\\"
    while not spinner_stop:
        for char in spinner_chars:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\b")

def select_model():
    models = get_model_list()
    console.print(f"[bold blue]\nAvailable models:[/]")
    for idx, model in enumerate(models, 1):
        friendly_name = get_model_config(model)["friendly_name"]
        console.print(f"[bold blue]{idx}) {friendly_name}[/]")
    
    while True:
        try:
            choice = int(input("\nSelect a model (enter the number): "))
            if 1 <= choice <= len(models):
                return models[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(f"Universal Chatbot - Chat with various AI models "
            f"\nUse your own OpenAI and/or Anthropic API key to chat with their latest LLMs."),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-m", "--model-select",
        nargs='?',
        const='show_menu',
        metavar="MODEL",
        help="Select the AI model to use. Options:\n"
             "  - Specify a model name directly\n"
             "  - Use without a value to show the model selection menu\n"
             "  - Omit to use the default model (gpt-4o-2024-08-06)\n"
             "Available models:\n" +
             "\n".join(f"  - {model}" for model in get_model_list())
    )
    
    return parser.parse_args()

def main():
    args = parse_arguments()

    default_model = "gpt-4o-2024-08-06"

    if args.model_select:
        if args.model_select == 'show_menu':
            selected_model = select_model()
        elif args.model_select in get_model_list():
            selected_model = args.model_select
        else:
            print(f"Invalid model: {args.model_select}")
            selected_model = select_model()
    else:
        selected_model = default_model

    model_config = get_model_config(selected_model)
    friendly_name = model_config["friendly_name"]

    if model_config["provider"] == "openai":
        client = OpenAI()
    else:
        client = Anthropic()

    try:
        # Initialize and ensure chat history directories
        base_dir = ensure_chat_history_dir()
        todays_chat_dir = get_todays_chat_dir(base_dir)

        now = datetime.now()
        local_date = now.strftime("%a %d %b %Y")  # e.g., "Fri 16 Feb 2024"
        local_time = now.strftime("%H:%M:%S %Z")  # e.g., "22:41:47 GMT+0000"

        system_prompt = (f"Specifically, your model is \"{friendly_name}\". Your knowledge base was last updated "
                         f"in April 2024. Today is {local_date}. Local time is {local_time}. You write in British "
                         f"English and you are not too quick to apologise.")

        choice = main_menu()
        if choice == "2":
            all_chats_dir = os.path.join(base_dir)
            chat_file = select_chat_file(all_chats_dir)
            if chat_file:
                messages = load_chat(chat_file)
            else:
                print("No chat selected or file not found.")
                return
        else:
            messages = []
            if model_config["provider"] == "openai":
                messages.append({
                    "role": "system",
                    "content": (f"You are a helpful AI assistant. Today is {local_date}. Local time is {local_time}. "
                                f"You answer queries succinctly, avoiding preamble and summaries whenever possible. "
                                f"You answer queries at a high language level and with expert level knowledge. "
                                f"Avoid responses that comment on the limitations of your model. You provide full, "
                                f"detailed answers. You behave like a passionate expert who always takes a clear "
                                f"stance on any topic discussed. You are excellent at reasoning. When reasoning, take "
                                f"a deep breath and think step by step before you answer the question. You do not finish "
                                f"your answers with a question unless specifically prompted to do so.")
                })

        welcome = f"""
You're now chatting with {friendly_name}.
The user prompt handles multiline input, so Enter gives a newline.
To submit your prompt hit Esc -> Enter.
To exit gracefully simply submit the word: "exit", or hit Ctrl+C.

You can pass individual utf-8 encoded files by entering "Upload: ~/path/to/file_name"
You can pass entire directories (recursively) by entering "Upload: ~/path/to/directory"
"""

        console.print(f"[bold blue]{welcome}[/]")
        
        while True:
            content = get_user_input()

            if should_exit(content):
                break

            is_file_request, path, is_directory = detect_file_analysis_request(content)
            if is_file_request:
                if is_directory:
                    markdown_content, token_count = generate_markdown_from_directory(path)
                    if markdown_content == "DIRECTORY TOO BIG.":
                        print(f"\nThe directory is too large to upload because it is likely larger than 100,000 tokens.\n"
                              f"Estimated token count for this recursive directory analysis: {token_count}\n")
                    if markdown_content:
                        dir_analysis_request = (f"The following describes a directory stucture along with all its contents in "
                                            f"Markdown format. "
                                            f"Please carefully analyse the directory structure and the files contained within. Pay "
                                            f"attention to whether the directory stucture looks like a code repository. Then take a "
                                            f"deep breath and provide a brief summary of your analysis. End your response with an "
                                            f"assurance that you have memorised the contents of the repository and you are ready to "
                                            f"answer the user's questions.\n\n{markdown_content}")
                        append_message(messages, "user", dir_analysis_request)
                        print(f"\nEstimated token count for this recursive directory analysis: {token_count}\n")
                    else:
                        print_formatted_text(HTML("<ansired>Directory is empty or contains no readable files.</ansired>"))
                        continue
                else:
                    file_name, file_contents, token_count = read_file_contents(path)
                    if file_contents == "FILE TOO BIG.":
                        print(f"\nThe file: {file_name} is too large to upload because it is likely larger than 64,000 tokens.\n"
                              f"Estimated token count for this file: {token_count}\n")
                    elif file_contents:
                        file_analysis_request = (f"Please analyse the contents of the following file:\n"
                                            f"\n{file_name}\n"
                                            f"\n{file_contents}\n"
                                            f"\nEnd your response by asking the user what questions they have about the file.")
                        append_message(messages, "user", file_analysis_request)
                        print(f"\nEstimated token count for this file: {token_count}\n")
                    else:
                        print_formatted_text(HTML(f"\nThe file: {file_name} is empty.\n"))
                        print(f"Estimated token count for this file: {token_count}\n")
                        continue
            else:
                append_message(messages, "user", content)

            if model_config["provider"] == "openai":
                stream = client.chat.completions.create(
                    model=selected_model,
                    messages=messages,
                    max_tokens=model_config["max_tokens"],
                    temperature=model_config["temperature"],
                    stream=True,
                )
            else:
                stream = client.messages.create(
                    model=selected_model,
                    messages=messages,
                    system=system_prompt,
                    max_tokens=model_config["max_tokens"],
                    temperature=model_config["temperature"],
                    stream=True
                )

            console.print(f"\n[yellow underline]{friendly_name}:[/]")
            complete_message = ""
            with Live(Markdown(complete_message),
                refresh_per_second=10,
                console=console,
                transient=False,
            ) as live:
                if model_config["provider"] == "openai":
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            complete_message += chunk.choices[0].delta.content
                            live.update(Markdown(complete_message))
                else:
                    for chunk in stream:
                        if chunk.type == "content_block_delta":
                            if chunk.delta.text:
                                complete_message += chunk.delta.text
                                live.update(Markdown(complete_message))
                        elif chunk.type == "message_stop":
                            break

            append_message(messages, "assistant", complete_message)

            print(f"\n")
            print(Rule(), "")

            save_chat(messages, todays_chat_dir)
                
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    main()
