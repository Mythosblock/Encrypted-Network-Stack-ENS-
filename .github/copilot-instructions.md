# Copilot Instructions for Encrypted Network Stack (ENS)

## Project Overview
Secure Net Stack is a modular, secure, and extensible Python framework for
building encrypted network nodes and communication systems.

## Repository Layout
- `src/` — Core modules (`networking.py`, `encryption.py`, `node.py`)
- `tests/` — Unit tests (run with `python3 -m unittest discover -s tests`)
- `examples/` — Demo scripts
- `docs/` — Architecture and design documentation
- `environment/` — Shell scripts for setup, deploy, and testing
- `tools/` — External tool submodules

## Conventions
- Pin all dependencies in `requirements.txt` with minimum versions.
- All shell scripts must start with `#!/usr/bin/env bash` and `set -euo pipefail`.
- Never assume directories exist — create them before writing files.
- Keep modules modular and independently testable.
- Include unit tests in `tests/` for any new feature.
- Follow PEP 8 style for Python code.

## CI
- GitHub Actions workflow at `.github/workflows/ci.yml` runs linting and tests
  on every push and pull request to `main`.

## Security
- Use the `cryptography` library for all encryption operations.
- Keep `cryptography` pinned to a version without known vulnerabilities.
- Do not commit secrets, keys, or `.env` files.
