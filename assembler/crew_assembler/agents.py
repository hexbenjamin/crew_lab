from textwrap import dedent

from crewai import Agent
from dotenv import find_dotenv, load_dotenv

from crew_assembler.tools import Registry

load_dotenv(find_dotenv())


class AgentBox:
    def __init__(self, llm):
        self.toolbox = Registry()
        self.agents = {}
        self.llm = llm

    def register_agent(self, config: dict):
        tools = (
            [getattr(self.toolbox, e) for e in config["tool_ids"]]
            if config["tool_ids"]
            else None
        )

        agent = Agent(
            role=dedent(config["role"]),
            backstory=dedent(config["backstory"]),
            goal=dedent(config["goal"]),
            allow_delegation=config["delegation"],
            verbose=config["verbose"],
            tools=tools,
            llm=self.llm,
        )

        self.agents.update({config["id"]: agent})

        return agent
