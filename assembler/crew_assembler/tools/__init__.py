from dataclasses import dataclass

from langchain.agents import load_tools
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun

from .youtube_transcript import youtube_transcript_retriever


@dataclass
class Registry:
    (_human,) = load_tools(["human"])
    _ddg_search = DuckDuckGoSearchRun()
    yt_transcript = youtube_transcript_retriever


__all__ = ["Registry"]
