# from youtube_transcript_api import YouTubeTranscriptApi
import os
import subprocess
from textwrap import dedent

from langchain.tools import tool
from pathvalidate import sanitize_filename
from pytube import YouTube
from rich.pretty import pprint

from crew_assembler.utils import make_subdir

# @tool("Fetch a YouTube link's transcript")
# def youtube_transcript_retriever(video_url: str) -> str:
#     """
#     Retrieve the transcript of a YouTube video.

#     Parameters:
#         - video_url: The URL of the YouTube video.

#     Returns:
#         - str, The transcript of the video.
#     """

#     # Extract video id from URL
#     video_id = video_url.split("watch?v=")[1]

#     if "&" in video_id:
#         video_id = video_id.split("&")[0]

#     # Get the transcript of the video
#     transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

#     # Convert the transcript into a single string
#     transcript = " ".join([i["text"] for i in transcript_list])

#     return dedent(transcript)


class CommandFailed(Exception):
    pass


def run_command(cmd: str):
    print(cmd)
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True
    )
    if result.returncode != 0:
        raise CommandFailed(
            f"Command '{cmd}' failed with exit code {result.returncode}: {result.stderr}"
        )
    return result.stdout


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

    video_title = yt.title
    transcript_path = os.path.join(
        audio_path, sanitize_filename(f"{video_title.replace(' ', '_')}.txt")
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

    run_command(" ".join(args))
    print(f"{video_title.upper()}\n- - - - - -\n\n")
    with open(transcript_path, "r") as f:
        transcript = f.read()
        pprint(transcript)

    os.remove(audio_path)
    os.remove(transcript_path)


if __name__ == "__main__":
    youtube_transcript_retriever("https://www.youtube.com/watch?v=TZ8wp32PJTU")
