from textwrap import dedent

from crewai import Crew, Process

from crew_assembler.agents import Agents
from crew_assembler.tasks import Tasks


class Assembler:
    def __init__(self, link):
        self.link: str = link
        self.agents: Agents = Agents()
        self.tasks: Tasks = Tasks()
        self.crew: Crew = None

    def build_crew(self):
        yt_summarizer = self.agents.yt_summarizer()
        summarize_task = self.tasks.summarize(yt_summarizer, self.link)

        self.crew = Crew(
            agents=[yt_summarizer],
            tasks=[summarize_task],
            verbose=2,
            process=Process.sequential,
        )

    def run(self):
        self.build_crew()
        return self.crew.kickoff()


def main():
    print("\n\nwelcome! to YouTube But Worse")
    print("+ + + ⬡ + + +\n")
    link = input(dedent("""enter YouTube link: """))

    crew = Assembler(link)
    result = crew.run()
    print("\n+ + + ⬡ + + +")
    print("RUN RESULTS :")
    print("+ + + ⬡ + + +\n")
    print(result + "\n\n")


if __name__ == "__main__":
    main()
