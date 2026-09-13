# Contributing

Thank you for helping improve this educational reinforcement-learning project.

## Before you start

- Read the [README](README.md) and confirm that the change fits Chapter 19 and the examples in this repository.
- Search existing issues and pull requests before opening a new one.
- Do not commit `.venv`, generated images, editor settings, credentials, or large unrelated files.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The project targets a CPU environment. Do not add CUDA or NVIDIA packages to the shared requirements file unless the project explicitly adopts a GPU profile.

## Making changes

- Keep changes focused and consistent with the existing educational style.
- Preserve the Gymnasium API (`reset()` returns `(observation, info)` and `step()` returns five values).
- Keep GridWorld layouts reproducible when a seed is supplied.
- Update the README or notebook notes when behavior or setup changes.
- Prefer small, readable functions over broad refactors.

## Checks

Run the relevant checks before opening a pull request:

```bash
python -m compileall -q cartpole gridworld
python -m pip check
```

For GridWorld rendering in a headless environment:

```bash
SDL_VIDEODRIVER=dummy python -c "import sys; sys.path.insert(0, 'gridworld'); from gridworld_env import GridWorldEnv; env = GridWorldEnv(); frame = env.render('rgb_array'); assert frame is not None; env.close()"
```

## Pull requests

A pull request should explain:

- what changed and why;
- which files or examples are affected;
- how the change was tested;
- whether the change affects rendered output, training behavior, or notebook cells.

Keep commits and pull requests small enough to review. Be open to feedback and update documentation when the implementation changes.
