import contextlib
import os
from textwrap import dedent

from crewai import Agent
from dotenv import load_dotenv
from langchain.agents import load_tools

from crew_assembler.tools import Registry


load_dotenv(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env"))


def select_llm(provider: str, model: str, base_url: str = None, api_key: str = None):
    if not api_key:
        with contextlib.suppress(KeyError):
            api_key = os.environ["OPENAI_API_KEY"] if provider == "openai" else None
            api_key = (
                os.environ["HUGGINGFACEHUB_API_TOKEN"] if provider == "hf" else None
            )
    if provider == "hf":
        from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

        endpoint_url = f"https://api-inference.huggingface.co/models/{model}"
        llm = HuggingFaceEndpoint(
            endpoint_url=endpoint_url,
            huggingfacehub_api_token=api_key or "hf_...",
            task="text-generation",
        )

    elif provider == "ollama":
        from langchain_community.llms.ollama import Ollama

        llm = Ollama(
            model=model or "openhermes:7b-mistral-v2.5-q6_K",
            base_url=base_url or "http://localhost:11434",
        )

    elif provider == "openai":
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model=model or "gpt-3.5-turbo",
            api_key=api_key or os.environ["OPENAI_API_KEY"] or "sk-...",
            base_url=base_url or "http://api.openai.com/v1",
        )

    return llm


class AgentBox:
    def __init__(self, model: str):
        self.toolbox = Registry()
        self.agents = {}

        self.provider, self.model = model.split("/", maxsplit=1)

        if not self.provider or not self.model:
            raise ValueError("Model should be in the format <provider>/<model>.")
        if self.provider not in ["ollama", "openai", "hf"]:
            raise ValueError("Provider should be only 'ollama', 'openai', or 'hf'.")

        self.llm = select_llm(provider=self.provider, model=self.model)

    def register_agent(self, config: dict):
        tools = (
            [getattr(self.toolbox, e) for e in config["tool_ids"]]
            if config["tool_ids"] != ""
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
