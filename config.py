import os
import yaml

def get_config(config_path="config.yml"):
    """Load configuration from YAML file and environment variables."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Load sensitive API keys from environment
    config["huggingfacehub_api_token"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    config["groq_api_key"] = os.getenv("GROQ_API_KEY")

    return config

