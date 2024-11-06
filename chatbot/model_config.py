MODEL_CONFIG = {
    "o1-preview": {
        "friendly_name": "OpenAI o1 Preview",
        "max_tokens": 32768,  
        "temperature": 1.0,
        "provider": "openai",
        "supports_system_message": False,
        "supports_streaming": False,
        "training_cutoff": "October 2023"
    },
    "chatgpt-4o-latest": {
        "friendly_name": "GPT-4o (tracking latest)",
        "max_tokens": 16384,
        "temperature": 1.05,
        "provider": "openai",
        "supports_system_message": True,
        "supports_streaming": True,
        "training_cutoff": "October 2023"
    },
    "gpt-4o-2024-08-06": {
        "friendly_name": "GPT-4o (2024/8/6 snapshot)",
        "max_tokens": 16384,
        "temperature": 1.05,
        "provider": "openai",
        "supports_system_message": True,
        "supports_streaming": True,
        "training_cutoff": "October 2023"
    },
    "gpt-4o-mini": {
        "friendly_name": "GPT-4o-mini",
        "max_tokens": 16384,
        "temperature": 1.05,
        "provider": "openai",
        "supports_system_message": True,
        "supports_streaming": True,
        "training_cutoff": "October 2023"
    },
    "gpt-4-turbo": {
        "friendly_name": "GPT-4-Turbo",
        "max_tokens": 4096,
        "temperature": 1.05,
        "provider": "openai",
        "supports_system_message": True,
        "supports_streaming": True,
        "training_cutoff": "December 2023"
    },
    "claude-3-5-haiku-20241022": {
        "friendly_name": "Claude 3.5 Haiku",
        "max_tokens": 8192,
        "temperature": 0.5,
        "provider": "anthropic",
        "supports_system_message": False,
        "supports_streaming": True,
        "training_cutoff": "July 2024"
    },
    "claude-3-5-sonnet-20241022": {
        "friendly_name": "Claude 3.5 Sonnet v2",
        "max_tokens": 8192,
        "temperature": 0.5,
        "provider": "anthropic",
        "supports_system_message": False,
        "supports_streaming": True,
        "training_cutoff": "April 2024"
    },
    "claude-3-opus-20240229": {
        "friendly_name": "Claude 3 Opus",
        "max_tokens": 4096,
        "temperature": 0.5,
        "provider": "anthropic",
        "supports_system_message": False,
        "supports_streaming": True,
        "training_cutoff": "August 2023"
    },
}

def get_model_list():
    return list(MODEL_CONFIG.keys())

def get_model_config(model_name):
    return MODEL_CONFIG.get(model_name)
