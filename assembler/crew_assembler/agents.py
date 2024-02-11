from textwrap import dedent

from crew_assembler.tools import Registry
from crewai import Agent
from langchain_community.llms.ollama import Ollama
from langchain_openai import ChatOpenAI

# from langchain_openai import ChatOpenAI


class AgentBox:
    def __init__(self, model: str, base_url: str = None):
        self.toolbox = Registry()
        self.agents = {}

        self.provider, self.model = model.split("/")
        if not self.provider or not self.model:
            raise ValueError("Model should be in the format <provider>/<model>.")
        if self.provider not in ["ollama", "openai"]:
            raise ValueError("Provider should be either 'ollama' or 'openai'.")

        if self.provider == "ollama":
            self.llm = Ollama(
                model=model or "openhermes:7b-mistral-v2.5-q6_K",
                base_url=base_url or "http://localhost:11434",
            )
        elif self.provider == "openai":
            self.llm = ChatOpenAI(
                model=model or "gpt-3.5-turbo",
                base_url=base_url or "http://api.openai.com/v1",
            )

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
