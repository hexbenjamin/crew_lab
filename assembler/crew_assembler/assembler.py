from crew_assembler.agents import AgentBox
from crew_assembler.tasks import TaskBox
from crewai import Crew, Process


class Assembler:
    def __init__(
        self,
        config_path: str,
        user_input: str,
        model: str,
    ):
        self.config_path: str = config_path
        self.user_input: str = user_input
        self.model_str = model

        self.agentbox: AgentBox = AgentBox(model=self.model_str)
        self.taskbox: TaskBox = TaskBox(self.user_input, self.agentbox)
        self.agents = []
        self.tasks = []
        self.crew: Crew = None

    def build_crew(self, agent_specs: dict, task_specs: dict):
        self.agents.extend(
            self.agentbox.register_agent(a_spec) for a_spec in agent_specs
        )

        self.tasks.extend(self.taskbox.register_task(t_spec) for t_spec in task_specs)

        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            process=Process.sequential,
        )

    def run(self):
        return self.crew.kickoff()
