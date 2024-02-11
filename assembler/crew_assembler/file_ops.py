import click
import tomlkit


import os


def load_config(config_name):
    config_dir = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__),
        ),
        "configs",
    )

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    config_path = os.path.join(config_dir, f"{config_name}.toml")

    if not os.path.exists(config_path):
        click.echo(f"Configuration file '{config_name}' not found.")
        return

    with open(config_path, "r") as file:
        toml_data = dict(tomlkit.parse(file.read()))

    return toml_data, config_path
