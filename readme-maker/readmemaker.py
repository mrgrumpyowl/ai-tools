#!/usr/bin/env python3

import os

from openai import OpenAI

def is_text_file(file_path):
    """
    Attempt to open and read a file in text mode to determine if it is a text file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.read(1024) # Read the first 1024 bytes
        return True
    except UnicodeDecodeError:
        return False

def crawl_files(directory):
    """
    Recursively crawl through all files in a directory and its sub-directories,
    skipping non-text files and the script itself.
    """
    file_contents = []
    script_path = os.path.abspath(__file__)
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path != script_path and is_text_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file_obj:
                        content = file_obj.read()
                        file_contents.append(content)
                except Exception as e:
                    print(f"Error reading {file}: {e}")
    return "\n\n---\n\n".join(file_contents)

def generate_readme(client, file_contents):
    """
    Send the contents to the OpenAI API to generate a README.md file.
    """
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {
                "role": "user",
                "content": (f"What follows is a set of file contents from a git repository. "
                            f"You must create a standard README.md file for the git repository "
                            f"based these file contents. Use the file contents to infer the nature "
                            f"and purpose of the git repository, along with any other details "
                            f"which are pertinent to the formation of an excellent standard README. "
                            f"Note that your response will be written directly to the README.md file, "
                            f"so do not preface the content of the README document in any way."
                            f"These are the file contents:\n\n{file_contents}"),
            }
        ],
    temperature=0.4,
    )
    return response.choices[0].message.content

def main():
    client = OpenAI()
    
    # Prompt the user for the directory to start the scan
    start_directory = input("Please enter the absolute path of the directory to start the file scan from: ")
    
    all_file_contents = crawl_files(start_directory)
    readme_content = generate_readme(client, all_file_contents)
    
    # Use the start_directory variable to define the path of README.md
    readme_path = os.path.join(start_directory, 'README.md')
    
    with open(readme_path, 'w', encoding='utf-8') as readme_file:
        readme_file.write(readme_content)
    print(f"README.md has been generated successfully in {start_directory}.")

if __name__ == "__main__":
    main()
