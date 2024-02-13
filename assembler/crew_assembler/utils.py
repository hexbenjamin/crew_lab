import os
from pathlib import Path

import click
import tomlkit


def load_config(config_name):
    config_dir = make_subdir("configs")
    config_dir.mkdir(exist_ok=True)

    config_path = config_dir / f"{config_name}.toml"

    if not config_path.exists():
        click.echo(f"Configuration file '{config_name}' not found.")
        return

    return dict(tomlkit.parse(config_path.read_text()))


def make_subdir(dir_name: str):
    return Path(__file__).resolve().parent / dir_name


def select_llm(provider: str, model: str, base_url: str = None, api_key: str = None):
    env_vars = {
        "openai": "OPENAI_API_KEY",
        "hf": "HUGGINGFACEHUB_API_TOKEN",
    }
    api_key = api_key or os.getenv(env_vars.get(provider))

    if provider == "hf":
        from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

        endpoint_url = f"https://api-inference.huggingface.co/models/{model}"
        llm = HuggingFaceEndpoint(
            endpoint_url=endpoint_url,
            huggingfacehub_api_token=api_key or "hf_...",
            task="text-generation",
        )

    elif provider == "ollama":
        from langchain_community.llms.ollama import Ollama

        llm = Ollama(
            model=model or "openhermes:7b-mistral-v2.5-q6_K",
            base_url=base_url or "http://localhost:11434",
        )

    elif provider == "openai":
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model=model or "gpt-3.5-turbo",
            api_key=api_key or "sk-...",
            base_url=base_url or "http://api.openai.com/v1",
        )

    return llm
