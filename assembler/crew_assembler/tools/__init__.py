from dataclasses import dataclass
from .youtube_transcript import youtube_transcript_retriever


@dataclass
class Registry:
    yt_transcript = youtube_transcript_retriever


__all__ = ["Registry", "youtube_transcript_retriever"]
