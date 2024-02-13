from textwrap import dedent
from typing import Optional

from crewai import Task

from crew_assembler.agents import AgentBox
from crew_assembler.tools import Registry


class TaskBox:
    def __init__(self, user_input: Optional[str], agentbox: AgentBox):
        self.toolbox = Registry()
        self.user_input = user_input
        self.agentbox = agentbox
        self.tasks = {}

    def register_task(self, config: dict):
        description = (
            config["description"].format(self.user_input)
            if "{}" in config["description"]
            else config["description"]
        )
        expected = (
            config["expected_output"].format(self.user_input)
            if "{}" in config["expected_output"]
            else config["expected_output"]
        )
        agent = self.agentbox.agents[config["agent_id"]]

        task = Task(
            description=dedent(description),
            expected_output=dedent(expected),
            context=[self.tasks[tname] for tname in config.get("context", [])],
            agent=agent,
            tools=[getattr(self.toolbox, e) for e in config.get("tool_ids", [])],
        )

        self.tasks[config["id"]] = task

        return task
