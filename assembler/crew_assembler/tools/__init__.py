from .youtube_transcript import youtube_transcript_retriever

registry = {
    "yt_transcript": youtube_transcript_retriever,
}

__all__ = ["registry", "youtube_transcript_retriever"]
