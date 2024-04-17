# CHANGELOG

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Dates in this file are in format of YYYY-MM-DD (2019-12-13 means 13th of December 2019).

## [[1.3.0]](https://github.com/mrgrumpyowl/ai-dev-tools/releases/tag/1.3.0) - 2024-04-15

### Added
* chatbot: Added new functionality to store chat history in `~/.chatbot/chat-history/` and to resume a previous conversation from chat history if the user desires. [@mrgrumpyowl](https://github.com/mrgrumpyowl)

### Changed
* chatbot: Updated the gpt-4 model to `gpt-4-turbo` so as to track the latest gpt-4 model available from OpenAI. `got-4-turbo` currently points to gpt-4-turbo-2024-04-09. Training data up to Dec 2023. [@mrgrumpyowl](https://github.com/mrgrumpyowl)

## [[1.2.0]](https://github.com/mrgrumpyowl/ai-dev-tools/releases/tag/1.2.0) - 2024-03-10

### Added
* claude: Added a clone of the chatbot that leverages the Anthropic API to offer a chat interface to their excellent new Claude 3 Opus model. [@mrgrumpyowl](https://github.com/mrgrumpyowl)

## [[1.1.1]](https://github.com/mrgrumpyowl/ai-dev-tools/releases/tag/1.1.1) - 2024-03-04

### Changed
* README hotfix - mention tree dependency. [@mrgrumpyowl](https://github.com/mrgrumpyowl)

## [[1.1.0]](https://github.com/mrgrumpyowl/ai-dev-tools/releases/tag/1.1.0) - 2024-03-03

### Added
* chatbot: Added new functionality to upload an entire directory and its contents recursively. This is designed primarily for code repository analysis so supports only utf-8 encoded files. [@mrgrumpyowl](https://github.com/mrgrumpyowl)
* groqbot: Added a clone of the chatbot that leverages the Groq API to offer a chat interface to Mistral's Mixtral-8x7b model. [@mrgrumpyowl](https://github.com/mrgrumpyowl)
* ALL: requirements.txt files. READMEs updated where appropriate. [@mrgrumpyowl](https://github.com/mrgrumpyowl)

## [[1.0.0]](https://github.com/mrgrumpyowl/ai-dev-tools/releases/tag/1.0.0) - 2024-02-20

### Added
* First fully working GPT-4 chatbot and readmemaker products. Leverages the OpenAI API to offer simple proof of concept AI tools for the CLI. [@mrgrumpyowl](https://github.com/mrgrumpyowl)

## [[0.9.0]](https://github.com/mrgrumpyowl/ai-dev-tools/releases/tag/0.9.0) - 2024-02-17

### Added
* Alpha code testing: system prompt and current date/time awareness to the chatbot. Temperature set to 1.05. max_tokens set to maximum permitted. [@mrgrumpyowl](https://github.com/mrgrumpyowl)

## [[0.8.0]](https://github.com/mrgrumpyowl/ai-dev-tools/releases/tag/0.8.0) - 2024-02-15

### Added
* Alpha code testing: chatbot and readmemaker products. [@mrgrumpyowl](https://github.com/mrgrumpyowl)

