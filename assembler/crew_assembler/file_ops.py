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
