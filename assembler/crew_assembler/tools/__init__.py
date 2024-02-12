from dataclasses import dataclass

from langchain.agents import load_tools

from .youtube_transcript import youtube_transcript_retriever


@dataclass
class Registry:
    _human = load_tools(["human"])
    yt_transcript = youtube_transcript_retriever


__all__ = ["Registry", "youtube_transcript_retriever"]
