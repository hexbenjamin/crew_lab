from typing import Literal
from crew_assembler.agents import AgentBox
from crew_assembler.tasks import TaskBox
from crew_assembler.utils import select_llm
from crewai import Crew, Process


class Assembler:
    def __init__(
        self,
        config_path: str,
        user_input: str,
        model: str,
        process: Literal["sequential", "hierarchical"] = "sequential",
    ):
        self.config_path: str = config_path
        self.user_input: str = user_input

        self.process = process

        self.provider, self.model = model.split("/", maxsplit=1)

        if not self.provider or not self.model:
            raise ValueError("Model should be in the format <provider>/<model>.")
        if self.provider not in ["ollama", "openai", "hf"]:
            raise ValueError("Provider should be only 'ollama', 'openai', or 'hf'.")

        self.llm = select_llm(provider=self.provider, model=self.model)

        self.agentbox: AgentBox = AgentBox(llm=self.llm)
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
            verbose=2,
            process=self.process,
            manager_llm=self.llm if self.process == "hierarchical" else None,
        )

    def run(self):
        return self.crew.kickoff()
