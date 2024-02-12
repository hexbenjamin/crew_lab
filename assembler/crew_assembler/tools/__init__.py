from dataclasses import dataclass

from langchain.agents import load_tools
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun

from .html_tools import unstructured_html
from .youtube_transcript import youtube_transcript_retriever


@dataclass
class Registry:
    (_human,) = load_tools(["human"])
    _ddg_search = DuckDuckGoSearchRun()
    html = unstructured_html
    yt_transcript = youtube_transcript_retriever


__all__ = ["Registry"]
