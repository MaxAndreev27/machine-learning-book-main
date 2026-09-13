## Summary

<!-- What changed and why? -->

## Affected examples

- [ ] GridWorld
- [ ] CartPole
- [ ] Notebook
- [ ] Documentation
- [ ] Dependencies

## Validation

<!-- List the commands and checks you ran. -->

```text
python -m compileall -q cartpole gridworld
python -m pip check
```

## Checklist

- [ ] I kept the change focused and documented behavior changes.
- [ ] I did not commit `.venv`, secrets, generated outputs, or unrelated files.
- [ ] I preserved the Gymnasium `reset()` and `step()` API where applicable.
- [ ] I updated README or notebook notes when setup or behavior changed.
- [ ] I added or updated tests/checks when the change needs them.
