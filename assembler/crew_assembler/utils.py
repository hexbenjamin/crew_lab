import contextlib
import os
from pathlib import Path

import click
import tomlkit


def load_config(config_name):
    config_dir = make_subdir("configs")
    os.makedirs(config_dir, exist_ok=True)

    config_path = config_dir / f"{config_name}.toml"

    if not config_path.exists():
        click.echo(f"Configuration file '{config_name}' not found.")
        return

    toml_data = dict(tomlkit.parse(config_path.read_text()))

    return toml_data, str(config_path)


def make_subdir(dir_name: str):
    return Path(__file__).resolve().parent / dir_name


def select_llm(provider: str, model: str, base_url: str = None, api_key: str = None):
    if not api_key:
        with contextlib.suppress(KeyError):
            api_key = os.environ["OPENAI_API_KEY"] if provider == "openai" else None
            api_key = (
                os.environ["HUGGINGFACEHUB_API_TOKEN"] if provider == "hf" else None
            )
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
            api_key=api_key or os.environ["OPENAI_API_KEY"] or "sk-...",
            base_url=base_url or "http://api.openai.com/v1",
        )

    return llm
