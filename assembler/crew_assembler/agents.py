from textwrap import dedent

from crew_assembler.tools import Registry
from crewai import Agent
from langchain_community.llms.ollama import Ollama

# from langchain_openai import ChatOpenAI


class AgentBox:
    def __init__(self):
        self.llm = Ollama(
            model="openhermes:7b-mistral-v2.5-q6_K",
            base_url="https://6805-73-16-154-145.ngrok-free.app",
        )
        self.toolbox = Registry()
        self.agents = {}

    def register_agent(self, config: dict):
        tools = (
            [getattr(self.toolbox, e) for e in config["tool_ids"]]
            if config["tool_ids"] != ""
            else []
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
