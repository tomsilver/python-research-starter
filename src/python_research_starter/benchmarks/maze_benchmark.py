"""A 2D maze benchmark."""

from typing import ClassVar

import numpy as np

from python_research_starter.benchmarks.base_benchmark import Benchmark
from python_research_starter.structs import Action, Goal, State, Task


class MazeBenchmark(Benchmark):
    """A 2D maze benchmark."""

    _min_height: ClassVar[int] = 5
    _max_height: ClassVar[int] = 8
    _min_width: ClassVar[int] = 5
    _max_width: ClassVar[int] = 8

    _empty: ClassVar[int] = 0
    _obstacle: ClassVar[int] = 1
    _agent: ClassVar[int] = 2

    _up: ClassVar[int] = 0
    _down: ClassVar[int] = 1
    _left: ClassVar[int] = 2
    _right: ClassVar[int] = 3

    @classmethod
    def get_name(cls) -> str:
        return "maze"

    def get_actions(self) -> list[Action]:
        return [self._up, self._down, self._left, self._right]

    def generate_tasks(
        self, num_tasks: int, train_or_test: str, rng: np.random.Generator
    ) -> list[Task]:
        assert train_or_test in ("train", "test")  # does not actually matter
        # Generate mazes independently.
        return [self._generate_task(rng) for _ in range(num_tasks)]

    def _generate_task(self, rng: np.random.Generator) -> Task:
        # Generate an empty obstacle grid of random size.
        height = rng.integers(self._min_height, self._max_height + 1)
        width = rng.integers(self._min_width, self._max_width + 1)
        grid = np.full((height, width), self._empty, dtype=int)

        # Generate a random start position.
        start = (
            rng.integers(0, height, dtype=int),
            rng.integers(0, width, dtype=int),
        )
        grid[start] = self._agent

        # Do a random walk to get an end position.
        visited = {start}
        walk_grid = grid.copy()
        possible_actions = [self._up, self._down, self._left, self._right]
        while True:
            action = rng.choice(possible_actions)
            walk_grid = self.get_next_state(walk_grid, action)
            current = self._state_to_agent(walk_grid)
            visited.add(current)
            if start != current and rng.uniform() > 0.9:
                target = current
                break

        # Add random obstacles. Choose a quarter of the safe cells.
        all_positions = {(r, c) for r in range(height) for c in range(width)}
        obstacle_candidates = sorted(all_positions - visited)
        num_obstacles = int(len(obstacle_candidates) * 0.25)
        obstacles = rng.choice(obstacle_candidates, size=num_obstacles, replace=False)
        for r, c in obstacles:
            grid[r, c] = self._obstacle

        # Finish the task.
        task = Task(grid, f"Go to {target}")

        return task

    def get_next_state(self, state: State, action: Action) -> State:
        r, c = self._state_to_agent(state)
        dr, dc = {
            self._up: (-1, 0),
            self._down: (1, 0),
            self._left: (0, -1),
            self._right: (0, 1),
        }[action]
        nr, nc = r + dr, c + dc
        if (not (0 <= nr < state.shape[0] and 0 <= nc < state.shape[1])) or (
            state[nr, nc] == self._obstacle
        ):
            nr, nc = r, c
        next_state = state.copy()
        next_state[r, c] = self._empty
        next_state[nr, nc] = self._agent
        return next_state

    def get_cost(self, state: State, action: Action, next_state: State) -> float:
        return 1.0

    def check_goal(self, state: State, goal: Goal) -> bool:
        assert goal.startswith("Go to (") and goal.endswith(")")
        r, c = map(int, goal[len("Go to (") : -1].replace(" ", "").split(","))
        return state[r, c] == self._agent

    def _state_to_agent(self, state: State) -> tuple[int, int]:
        loc = np.argwhere(state == self._agent)[0]
        return (int(loc[0]), int(loc[1]))
