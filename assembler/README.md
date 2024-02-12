# crew-assembler !

experiments with a CLI-based, TOML-loading [CrewAI](https://github.com/joaomdmoura/crewAI/) runner.

run your poetry install on *this* `pyproject.toml`, then use `assembler -c <config_name>` to run a crew!

1. `assembler -c remix_selector` should be a pretty straightforward run

2. make sure to use `poetry install --extras "web"` to use the yt_summarizer example, and pass in a link: `assembler -c yt_summarizer -i <YouTube link>`. 🫡
