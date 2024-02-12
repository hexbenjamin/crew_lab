import click

from crew_assembler.assembler import Assembler
from crew_assembler.utils import load_config


def make_specs(config_data: dict):
    agent_specs = config_data["agent"].unwrap()
    task_specs = config_data["task"].unwrap()

    return agent_specs, task_specs


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

    click.echo("\nwelcome to CREW ASSEMBLER, by hex benjamin!\n")
    click.echo("+ + + ⬡ + + +\n")

    config_data, config_path = load_config(config_name)

    crew_data = config_data["crew"]
    click.echo("+ + +")
    click.echo(f"Crew config '{crew_data['id']}' loaded.")
    click.echo("⬡ ⬡ ⬡")
    click.echo(f"NAME: '{crew_data['name']}'")
    click.echo(f"DESC: '{crew_data['description']}'")
    click.echo("- - -\n")

    click.echo(f"running CREW ASSEMBLER with {crew_data['model']}...\n")

    if crew_data["process"] not in ["sequential", "hierarchical"]:
        raise ValueError(
            "invalid process type. only 'sequential' and 'hierarchical' are supported."
        )

    crew = Assembler(
        config_path=config_path,
        user_input=user_input or None,
        model=crew_data["model"],
        process=crew_data["process"],
    )
    crew.build_crew(*make_specs(config_data))
    result = crew.run()

    print("\n+ + + ⬡ + + +")
    print("RUN RESULTS :")
    print("+ + + ⬡ + + +\n")
    print(result + "\n\n")


if __name__ == "__main__":
    import logging

    logging.basicConfig(filename="log_0-10-0.txt", level=logging.DEBUG)

    run()

    logging.shutdown()
