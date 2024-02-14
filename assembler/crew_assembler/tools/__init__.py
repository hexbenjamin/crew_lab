from dataclasses import dataclass

from langchain.agents import load_tools
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun

# from .memory import MemoryTools
from .web import WebTools
from .youtube import YouTubeTools


@dataclass
class Registry:
    (_human,) = load_tools(["human"])
    _ddg_search = DuckDuckGoSearchRun()
    docusaurus = WebTools.get_docusaurus_docs
    html = WebTools.get_html
    # memory_write = MemoryTools.embed_text
    # memory_read = MemoryTools.similarity_search
    yt_transcript = YouTubeTools.transcript_retriever


__all__ = ["Registry"]
