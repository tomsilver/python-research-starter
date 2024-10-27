# Python Research Code Example

![workflow](https://github.com/tomsilver/python-research-starter/actions/workflows/ci.yml/badge.svg)

This repository illustrates a nice way to structure Python research code. It is not intended for direct use.

## Philosophy

Many research projects involve developing **approaches** that perform well on some **benchmarks** with respect to some **metrics**. See [this blog post](https://lis.csail.mit.edu/whats-your-problem-an-oft-missing-section-in-ai-papers/) for an elaboration. This code is organized accordingly:

1. A [base benchmark](src/python_research_starter/benchmarks/base_benchmark.py) class defines the interface for all benchmarks.
2. A [base approach](src/python_research_starter/approaches/base_approach.py) class defines the interface for all approaches.
3. An [experiment script](experiments/run_single_experiment.py) evaluates approaches on benchmarks while recording metrics of interest.

## Example Use

We use [hydra](https://hydra.cc/) for experiments. The [conf](experiments/conf/) directory defines configurations. To run a single approach on a single benchmark with a single random seed:

```
python experiments/run_single_experiment.py seed=42 approach=random benchmark=maze_small
```

To run multiple approaches on multiple benchmarks with multiple random seeds:

```
python experiments/run_single_experiment.py -m seed=1,2,3 approach=random,search benchmark=maze_small,maze_large
```

Hydra also works well with clusters. For example, see [here](https://hydra.cc/docs/plugins/submitit_launcher/).

## Getting Started

This repository is based on [python-starter](https://github.com/tomsilver/python-starter), which is a general starter repository (not limited to research project code). We suggest starting with that codebase and then working your way up to the structure exemplified here.
