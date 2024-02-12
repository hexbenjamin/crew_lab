from dataclasses import dataclass

from langchain.agents import load_tools
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun

from .memory import embed_text, similarity_search
from .web import unstructured_html
from .youtube import youtube_transcript_retriever


@dataclass
class Registry:
    (_human,) = load_tools(["human"])
    _ddg_search = DuckDuckGoSearchRun()
    html = unstructured_html
    memory_write = embed_text
    memory_read = similarity_search
    yt_transcript = youtube_transcript_retriever


__all__ = ["Registry"]
