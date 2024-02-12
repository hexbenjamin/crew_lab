import contextlib
import os
from textwrap import dedent

from crewai import Agent
from dotenv import load_dotenv
from langchain.agents import load_tools
from crew_assembler.utils import select_llm

from crew_assembler.tools import Registry


load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env"))


class AgentBox:
    def __init__(self, llm):
        self.toolbox = Registry()
        self.agents = {}
        self.llm = llm

    def register_agent(self, config: dict):
        # tools = None
        # with contextlib.suppress(KeyError):
        tools = (
            [getattr(self.toolbox, e) for e in config["tool_ids"]]
            if config["tool_ids"] != []
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
