from textwrap import dedent

from crewai import Crew, Process

from themesquad.agents import Agents
from themesquad.tasks import Tasks


class Themesquad:
    def __init__(self, link):
        self.link = link
        self.agents = Agents()
        self.tasks = Tasks()

    def build(self):
        yt_summarizer = self.agents.yt_summarizer()
        summarize_task = self.tasks.summarize(yt_summarizer, self.link)

        self.crew = Crew(
            agents=[yt_summarizer],
            tasks=[summarize_task],
            verbose=2,
            process=Process.sequential,
        )

    def run(self):
        self.build()
        return self.crew.kickoff()


def main():
    print("\n\nwelcome! to YouTube But Worse")
    print("+ + + ⬡ + + +\n")
    link = input(dedent("""enter YouTube link: """))

    crew = Themesquad(link)
    result = crew.run()
    print("\n+ + + ⬡ + + +")
    print("RUN RESULTS :")
    print("+ + + ⬡ + + +\n")
    print(result + "\n\n")


if __name__ == "__main__":
    main()
