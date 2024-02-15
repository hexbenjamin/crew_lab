# from youtube_transcript_api import YouTubeTranscriptApi
import json
import os
from typing import Any, Tuple

from dotenv import find_dotenv, load_dotenv
from gradio_tools import GradioTool
from langchain.tools import tool
from pytube import YouTube

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


class YouTubeToolsIFW:
    @tool("Fetch a YouTube link's transcript")
    def transcript_retriever(video_url: str) -> str:
        """
        Retrieve the transcript of a YouTube video.

        Parameters:
            - video_url: The URL of the YouTube video.

        Returns:
            - str, The transcript of the video.
        """

        tmp_path = make_subdir("tmp")

        yt = YouTube(video_url)

        video = yt.streams.filter(only_audio=True).first()
        video.download(output_path=tmp_path, filename="youtube.mp3")

        transcript_path = os.path.join(tmp_path, "whisper.json")

        args = [
            "insanely-fast-whisper",
            "--file-name",
            f"{tmp_path}/youtube.mp3",
            "--device-id",
            "0",
            "--batch-size",
            "8",
            "--transcript-path",
            transcript_path,
        ]

        # if hf_token := os.environ.get("HUGGINGFACEHUB_API_TOKEN"):
        #     args.extend(["--hf_token", hf_token])

        os.system(" ".join(args))

        with open(transcript_path, "r") as f:
            transcript = json.loads(transcript)["text"]

        out_text = (
            f"{yt.title.upper()}, by {yt.author.upper()}\n- - - - - -\n\n{transcript}\n"
        )

        os.remove(os.path.join(tmp_path, "youtube.mp3"))
        # os.remove(transcript_path)

        return f'The transcript of "{yt.title.upper()}", by {yt.author.upper()}, has been saved to a file at {transcript_path}.\n\nCONTENT:\n{out_text}'

    @tool("Fetch a YouTube link's transcript")
    def gradio_retriever(video_url: str) -> str:
        """
        Retrieve the transcript of a YouTube video.

        Parameters:
            - video_url: The URL of the YouTube video.

        Returns:
            - str, The transcript of the video.
        """

        whisper = GradioTool(
            name="YouTube Whisper",
            description="Transcribe a YouTube video using OpenAI's Whisper.",
            src="SteveDigital/free-fast-youtube-url-video-to-text-using-openai-whisper",
        )

        print(whisper.run(video_url))


class YouTubeTools(GradioTool):
    def __init__(self):
        super().__init__(
            name="YouTube Whisper",
            description="Transcribe a YouTube video using OpenAI's Whisper model",
            src="hf-audio/whisper-large-v3",
        )

    def create_job(self, query: str):
        return self.client.submit(query, "transcribe", api_name="/predict_2")

    def postprocess(self, output: Tuple[Any] | Any) -> str:
        return str(output[1])
