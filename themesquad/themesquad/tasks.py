from textwrap import dedent

from crewai import Task


class Tasks:
    def __tip_section(self):
        return "<helpful instruction>"

    def summarize(self, agent, link):
        return Task(
            description=dedent(
                f"""
                Use your tools to retrieve the transcript of the YouTube video link provided to you. Share this text with the requester. 
                Link: {link}
                """,
            ),
            agent=agent,
        )
