# Chapter 19: Reinforcement Learning

This repository contains the current GridWorld reinforcement-learning example from Chapter 19, “Reinforcement Learning for Decision Making in Complex Environments.” The agent learns with tabular Q-learning and the environment is rendered with Pygame.

## Contents

```text
.
├── gridworld/
│   ├── agent.py                # Q-learning agent and Q-table
│   ├── gridworld_env.py        # 8x8 Pygame environment
│   ├── qlearning.py            # Training loop and learning plot
│   └── q-learning-history.png  # Generated learning-history plot
├── .github/                    # GitHub workflows, templates, and policies
├── .python-version             # Project Python version
├── requirements.txt            # Frozen project environment
├── LICENSE
└── README.md
```

## Requirements

- Python 3.13 or a compatible recent Python version
- A desktop session for the Pygame window
- CPU is supported; GPU/CUDA is not required

The checked-in requirements are a freeze of the working CPU environment. For a fresh virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
```

To confirm that PyTorch is using the CPU build:

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

The final line should print `False` in the CPU setup.

## Start Here: Q-learning

The main entry point is `gridworld/qlearning.py`. It runs the complete project example: the agent interacts with the GridWorld, learns a policy with tabular Q-learning, renders the environment in Pygame, and saves a learning-history plot.

Run it from the `gridworld` directory because the training script imports its neighboring modules directly:

```bash
cd gridworld
python qlearning.py
```

The environment is an 8x8 grid. One gold cell and seven trap cells are chosen once when the environment starts, remain fixed across training episodes, and are regenerated on the next process start. Seven traps make the search challenging while the environment's reachability check guarantees that the gold remains accessible. The learning chart is written to `gridworld/q-learning-history.png`.

`gridworld/gridworld_env.py` contains the environment implementation used by Q-learning. It is not the primary program to run; launch `qlearning.py` first to see the complete learning example. The environment file can be run separately only when you want to inspect random movement without training.

## Development checks

```bash
python -m compileall -q gridworld
python -m pip check
```

Headless environments can validate imports and rendering with:

```bash
cd gridworld
SDL_VIDEODRIVER=dummy python -c "from gridworld_env import GridWorldEnv; env = GridWorldEnv(); frame = env.render('rgb_array'); assert frame is not None; env.close()"
```

## Contributing

Bug reports, documentation improvements, and small educational enhancements are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request.

## Community and security

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security policy](SECURITY.md)
- [Support](SUPPORT.md)
- [Governance](GOVERNANCE.md)

## License

This project is distributed under the [MIT License](LICENSE).
