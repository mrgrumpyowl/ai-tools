MODEL_CONFIG = {
    "gpt-4o-2024-08-06": {"friendly_name": "GPT-4o (2024/8/6 snapshot)", "max_tokens": 16384, "temperature": 1.05, "provider": "openai"},
    "chatgpt-4o-latest": {"friendly_name": "GPT-4o (tracking latest)", "max_tokens": 16384, "temperature": 1.05, "provider": "openai"},
    "gpt-4o-mini": {"friendly_name": "GPT-4o-mini", "max_tokens": 16384, "temperature": 1.05, "provider": "openai"},
    "gpt-4-turbo": {"friendly_name": "GPT-4-Turbo", "max_tokens": 4096, "temperature": 1.05, "provider": "openai"},
    "claude-3-5-sonnet-20240620": {"friendly_name": "Claude 3.5 Sonnet", "max_tokens": 8192, "temperature": 0.5, "provider": "anthropic"},
    "claude-3-opus-20240229": {"friendly_name": "Claude 3 Opus", "max_tokens": 4096, "temperature": 0.5, "provider": "anthropic"},
}

def get_model_list():
    return list(MODEL_CONFIG.keys())

def get_model_config(model_name):
    return MODEL_CONFIG.get(model_name)
