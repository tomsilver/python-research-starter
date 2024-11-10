"""Script for running experiments with hydra."""

import logging
import time

import hydra
import numpy as np
import pandas as pd
from omegaconf import DictConfig

from limb_repo.approaches.base_approach import Approach
from limb_repo.benchmarks.base_benchmark import Benchmark
from limb_repo.structs import Task
from limb_repo.utils import get_plan_cost, plan_is_valid


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
    test_tasks = benchmark.generate_tasks(cfg.num_test_tasks, "test", rng)
    test_task_metrics: list[dict[str, float]] = []
    for i, task in enumerate(test_tasks):
        metrics = _run_single_task_evaluation(
            task, approach, benchmark, rng, timeout=cfg.planning_timeout
        )
        metrics["task_id"] = i
        test_task_metrics.append(metrics)

    # Aggregate and save results.
    df = pd.DataFrame(test_task_metrics)
    print(df)


def _run_single_task_evaluation(
    task: Task,
    approach: Approach,
    benchmark: Benchmark,
    rng: np.random.Generator,
    timeout: float,
) -> dict[str, float]:
    start_time = time.perf_counter()
    plan = approach.generate_plan(task, "test", timeout, rng)
    duration = time.perf_counter() - start_time
    metrics: dict[str, float] = {}
    metrics["success"] = plan_is_valid(plan, task, benchmark)
    metrics["cost"] = get_plan_cost(plan, task, benchmark)
    metrics["duration"] = duration
    return metrics


if __name__ == "__main__":
    _main()  # pylint: disable=no-value-for-parameter
