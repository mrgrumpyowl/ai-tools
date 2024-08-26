#!/usr/bin/env python3

import fnmatch
import os
import sys
import threading
import tiktoken
import time
import datetime
import subprocess

from anthropic import Anthropic

from prompt_toolkit import prompt
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import HTML

from rich import print
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.rule import Rule

console = Console(highlight=False)

def get_user_input() -> str:
    # Display the prompt to the user for multiline input.
    # The user can press Esc followed by Enter to submit their input.
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
    # Returns the output of `tree -d` command on the specified directory path
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
    # Returns the number of tokens as an int.
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

def main():
    try:
        client = Anthropic()

        now = datetime.datetime.now()
        local_date = now.strftime("%a %d %b %Y")  # e.g., "Fri 16 Feb 2024"
        local_time = now.strftime("%H:%M:%S %Z")  # e.g., "22:41:47 GMT+0000"

        system_prompt = (f"Specifically, your model is \"Claude 3 Opus\". Your knowledge base was last updated "
                         f"in August 2023. Today is {local_date}. Local time is {local_time}. You write in British "
                         f"English and you are not too quick to apologise.")
        
        messages = []

        welcome = (
"""
You're now chatting with Anthropic's Claude 3 Opus.
The user prompt handles multiline input, so Enter gives a newline.
To submit your prompt to Claude hit Esc -> Enter.
To exit gracefully simply submit the word: "exit", or hit Ctrl+C.

You can pass individual utf-8 encoded files to Claude by entering "Upload: ~/path/to/file_name"
You can pass entire directories (recursively) to Claude by entering "Upload: ~/path/to/directory"
"""
        )

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

            stream = client.messages.create(
                model="claude-3-opus-20240229",
                messages=messages,
                system=system_prompt,
                max_tokens=4096,
                temperature=0.5,
                stream=True
            )  
            console.print("\n[yellow underline]Claude 3 Opus:[/]")
            complete_message = ""
            with Live(Markdown(complete_message),
                refresh_per_second=10,
                console=console,
                transient=False,
            ) as live:
                for chunk in stream:
                    if chunk.type == "content_block_start":
                        continue
                    elif chunk.type == "content_block_delta":
                        if chunk.delta.text:
                            complete_message += chunk.delta.text
                            live.update(Markdown(complete_message))
                    elif chunk.type == "message_stop":
                        break

            append_message(messages, "assistant", complete_message)

            print(f"\n")
            print(Rule(), "")
                
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    main()
