# Security Policy

## Supported versions

This is an educational code repository. Security fixes are applied to the default branch when a reproducible issue is confirmed. There is no separate long-term support branch.

## Reporting a vulnerability

Please do not disclose an exploitable vulnerability in a public issue. Use GitHub's private vulnerability reporting feature when it is enabled for this repository. If that feature is unavailable, contact the repository maintainers privately through the contact method shown on the repository's GitHub page.

Include:

- a short description of the issue;
- affected file, component, or dependency;
- reproduction steps or a minimal proof of concept;
- potential impact;
- a suggested mitigation, if known.

Do not include passwords, access tokens, private keys, or other secrets in a report.

You can expect an acknowledgement when the report is received and a follow-up after triage. Please allow time for investigation before public disclosure.

## Dependency concerns

For dependency vulnerabilities, include the package name, installed version, affected version range, and the command or workflow that exposes the problem. Run `python -m pip check` after dependency changes.
