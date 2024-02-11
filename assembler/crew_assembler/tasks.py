from textwrap import dedent
from typing import Optional

from crew_assembler.agents import AgentBox
from crew_assembler.tools import Registry
from crewai import Task


class TaskBox:
    def __init__(self, user_input: Optional[str], agentbox: AgentBox):
        self.toolbox = Registry()
        self.user_input = user_input
        self.agentbox = agentbox
        self.tasks = {}
        # self.__tip_section = ""

    def register_task(self, config: dict):
        tools = (
            [getattr(self.toolbox, e) for e in config["tool_ids"]]
            if config["tool_ids"] != ""
            else []
        )

        description = config["description"]
        if "{}" in description:
            description = description.format(self.user_input)

        expected = config["expected_output"]
        if "{}" in expected:
            expected = expected.format(self.user_input)

        task = Task(
            description=dedent(description),
            expected_output=dedent(expected) or None,
            context=dedent(config["context"]) or None,
            agent=self.agentbox.agents[config["agent"]],
            tools=tools,
        )

        self.tasks[config["id"]] = task

        return task
