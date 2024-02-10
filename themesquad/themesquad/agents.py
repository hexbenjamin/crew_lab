from textwrap import dedent

from crewai import Agent
from langchain_community.llms.ollama import Ollama

# from langchain_openai import ChatOpenAI

from themesquad.tools import youtube_transcript_retriever


class Agents:
    def __init__(self):
        self.llm = Ollama(
            model="openhermes:7b-mistral-v2.5-q6_K",
            base_url="https://6805-73-16-154-145.ngrok-free.app",
        )

    def build_agent(
        self,
        role="Agent",
        backstory="",
        goal="",
        tools=None,
        allow_delegation=True,
        verbose=False,
    ):
        if tools is None:
            tools = []
        return Agent(
            role=role,
            backstory=dedent(backstory),
            goal=dedent(goal),
            tools=tools,
            allow_delegation=allow_delegation,
            verbose=verbose,
            llm=self.llm,
        )

    def yt_summarizer(self):
        return self.build_agent(
            role="YouTube Summarizer",
            backstory="""
                You are an expert note-taker, and you have been asked to take notes on a YouTube video. 
                Retrieve the video's transcript, then summarize it as a Markdown-formatted note.
                """,
            goal=dedent("Summarize the video's transcript as a Markdown note."),
            tools=[youtube_transcript_retriever],
            allow_delegation=False,
            verbose=True,
        )
