from textwrap import dedent

import click

from crew_assembler.assembler import Assembler
from crew_assembler.utils import load_config

TEMPLATE_TEMPLATE = dedent(
    """⬡ ⬡ ⬡
    crew config '{crew_id}' loaded.
    
    + + +
    NAME: '{crew_name}'
    DESC: '{crew_description}'
    - - -
    
    running CREW ASSEMBLER with {crew_model}...
    """
)


@click.command()
@click.option(
    "--config-name",
    "-c",
    prompt="⬡ |  config name",
    help="Configuration file to construct the crew from.",
    type=str,
)
@click.option(
    "--user-input",
    "-i",
    prompt="⬡ |  user input",
    help="Input text for the crew, as applicable.",
    type=str,
    prompt_required=False,
    default="",
)
def run(config_name: str, user_input: str):
    """Crew Assembler CLI."""

    click.echo("\nwelcome to CREW ASSEMBLER, by hex benjamin!\n+ + + ⬡ + + +\n")

    config_data = load_config(config_name)
    crew_data = config_data["crew"]

    click.echo(
        TEMPLATE_TEMPLATE.format(
            crew_id=crew_data["id"].upper(),
            crew_name=crew_data["name"],
            crew_description=crew_data["description"],
            crew_model=crew_data["model"],
        )
    )

    if crew_data["process"] not in ["sequential", "hierarchical"]:
        raise ValueError(
            "invalid process type. only 'sequential' and 'hierarchical' are supported."
        )

    crew = Assembler(
        config_data=config_data,
        user_input=user_input or None,
    )
    crew.build_crew(config_data["agent"].unwrap(), config_data["task"].unwrap())
    result = crew.run()

    click.echo("\n+ + + ⬡ + + +\nRUN RESULTS :\n+ + + ⬡ + + +\n")
    click.echo(result + "\n\n")


if __name__ == "__main__":
    run()
