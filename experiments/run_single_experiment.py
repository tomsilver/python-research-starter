"""Script for running experiments with hydra."""

import logging

import hydra
import numpy as np
from omegaconf import DictConfig

from python_research_starter.approaches.base_approach import Approach
from python_research_starter.benchmarks.base_benchmark import Benchmark
from python_research_starter.structs import Task
from python_research_starter.utils import plan_is_valid


@hydra.main(version_base=None, config_name="config", config_path="conf/")
def _main(cfg: DictConfig) -> None:

    logging.info(
        f"Running seed={cfg.seed}, benchmark={cfg.benchmark}, approach={cfg.approach}"
    )

    # Initialize.
    benchmark = hydra.utils.instantiate(cfg.benchmark)
    assert isinstance(benchmark, Benchmark)
    approach = hydra.utils.instantiate(
        cfg.approach,
        benchmark.get_actions(),
        benchmark.get_next_state,
        benchmark.get_cost,
        benchmark.check_goal,
    )
    assert isinstance(approach, Approach)
    rng = np.random.default_rng(cfg.seed)

    # Train.
    train_tasks = benchmark.generate_tasks(cfg.num_train_tasks, "train", rng)
    approach.train(training_tasks=train_tasks)

    # Evaluate.
    test_tasks = benchmark.generate_tasks(cfg.num_eval_tasks, "test", rng)
    test_task_metrics: list[dict[str, float]] = []
    for task in test_tasks:
        metrics = _run_single_task_evaluation(
            task, approach, benchmark, rng, timeout=cfg.planning_timeout
        )
        test_task_metrics.append(metrics)

    # Aggregate and save results.
    import ipdb

    ipdb.set_trace()


def _run_single_task_evaluation(
    task: Task,
    approach: Approach,
    benchmark: Benchmark,
    rng: np.random.Generator,
    timeout: float,
) -> dict[str, float]:
    plan = approach.generate_plan(task, "test", timeout, rng)
    # TODO add more metrics
    metrics: dict[str, float] = {}
    metrics["success"] = plan_is_valid(plan, task, benchmark)
    return metrics


if __name__ == "__main__":
    _main()  # pylint: disable=no-value-for-parameter
