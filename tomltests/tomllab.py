import tomlkit
from rich.pretty import pprint

specfile = "./tomltests/example.toml"

# Load the TOML file
with open(specfile, "r") as file:
    toml_data = dict(tomlkit.parse(file.read()))

# Print the parsed data
pprint(toml_data["agent"].unwrap())
pprint(toml_data["task"].unwrap())
