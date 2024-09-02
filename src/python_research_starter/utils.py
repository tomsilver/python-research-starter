"""Utility functions."""

from python_research_starter.benchmarks.base_benchmark import Benchmark
from python_research_starter.structs import Action, Task


def plan_is_valid(plan: list[Action], task: Task, benchmark: Benchmark) -> bool:
    """Checks if the plan solves the task."""
    state = task.init
    for action in plan:
        state = benchmark.get_next_state(state, action)
    return benchmark.check_goal(state, task.goal)
