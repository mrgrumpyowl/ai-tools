#!/usr/bin/env python3

import os
import subprocess

project_dirs = ["chatbot", "claude", "groqbot", "readmemaker"]

def install_project(project_dir):
    subprocess.check_call(["pip3", "install", "."], cwd=project_dir)

root_dir = os.path.dirname(os.path.realpath(__file__))

for project in project_dirs:
    full_path = os.path.join(root_dir, project)
    install_project(full_path)
