# from youtube_transcript_api import YouTubeTranscriptApi
import json
import os
from textwrap import dedent

from dotenv import find_dotenv, load_dotenv
from langchain.tools import tool
from pathvalidate import sanitize_filename
from pytube import YouTube
from rich.pretty import pprint

from crew_assembler.utils import make_subdir

load_dotenv(find_dotenv())


"""
# Take 1! the "youtube auto caption" method. see [this](https://www.youtube.com/watch?v=23H8IdaS3tk) to learn how that went.

@tool("Fetch a YouTube link's transcript")
def youtube_transcript_retriever(video_url: str) -> str:
    '''
    Retrieve the transcript of a YouTube video.

    Parameters:
        - video_url: The URL of the YouTube video.

    Returns:
        - str, The transcript of the video.
    '''

    # Extract video id from URL
    video_id = video_url.split("watch?v=")[1]

    if "&" in video_id:
        video_id = video_id.split("&")[0]

    # Get the transcript of the video
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

    # Convert the transcript into a single string
    transcript = " ".join([i["text"] for i in transcript_list])

    return dedent(transcript)
"""


@tool("Fetch a YouTube link's transcript")
def youtube_transcript_retriever(video_url: str) -> str:
    """
    Retrieve the transcript of a YouTube video.

    Parameters:
        - video_url: The URL of the YouTube video.

    Returns:
        - str, The transcript of the video.
    """

    audio_path = make_subdir("tmp")

    yt = YouTube(video_url)

    video = yt.streams.filter(only_audio=True).first()
    video.download(output_path=audio_path, filename="youtube.mp3")

    transcript_path = os.path.join(
        audio_path, sanitize_filename(f"{yt.title.replace(' ', '_')}.txt")
    )

    args = [
        "insanely-fast-whisper",
        "--file-name",
        f"{audio_path}/youtube.mp3",
        "--device-id",
        "0",
        "--transcript-path",
        transcript_path,
    ]

    # if hf_token := os.environ.get("HUGGINGFACEHUB_API_TOKEN"):
    #     args.extend(["--hf_token", hf_token])

    os.system(" ".join(args))

    with open(transcript_path, "r") as f:
        transcript = f.read()

    transcript = json.loads(transcript)["text"]

    print(
        out_text := f"{yt.title.upper()}, by {yt.author.upper()}\n- - - - - -\n\n{transcript}\n"
    )

    os.remove(os.path.join(audio_path, "youtube.mp3"))
    # os.remove(transcript_path)

    return f'The transcript of "{yt.title.upper()}", by {yt.author.upper()}, has been saved to a file at {transcript_path}.'
