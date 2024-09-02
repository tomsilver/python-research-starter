"""Tests for search_approach.py."""

import numpy as np

from python_research_starter.approaches.search_approach import SearchApproach
from python_research_starter.benchmarks.maze_benchmark import MazeBenchmark
from python_research_starter.utils import plan_is_valid


def test_search_approach():
    """Tests for SearchApproach()."""
    benchmark = MazeBenchmark()
    approach = SearchApproach(
        benchmark.get_actions(),
        benchmark.get_next_state,
        benchmark.get_cost,
        benchmark.check_goal,
    )
    assert approach.get_name() == "search"
    rng = np.random.default_rng(123)
    task = benchmark.generate_tasks(1, "train", rng)[0]
    plan = approach.generate_plan(task, "test", 1.0, rng)
    assert plan_is_valid(plan, task, benchmark)
