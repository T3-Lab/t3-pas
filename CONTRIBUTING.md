# Contributing to PAS

Thanks for your interest in contributing! PAS started as a personal learning project — contributions are welcome from anyone curious about the same questions.

---

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run PAS:
   ```bash
   python -m src.pas
   ```

For full usage, see [README.md](README.md).

---

## Reporting Bugs & Suggesting Features

Please **open an Issue first** before submitting a PR — this keeps things transparent and avoids duplicate work.

When opening an Issue, include:
- What you expected to happen
- What actually happened
- Steps to reproduce (if applicable)

---

## Submitting a Pull Request

1. Fork the repository
2. Create a branch for your change
3. Submit a PR referencing the related Issue

PRs without a linked Issue may be closed without review.

---

## Hard Rule — Keep the Primitive

> **The agent's main logic must remain rule-based. No ML in planning, intent parsing, or decision-making.**

This is PAS's core principle, not a suggestion. Contributions that introduce ML into the agent's main logic will not be accepted regardless of quality.

Tools (under `tools.py`) are exempt — they can use ML or any approach appropriate for the task.

---

## Contribution Spirit

PAS is an exploration, not a production system. Experiments are welcome — as long as they come with an explanation of *why*. A good PR doesn't just change code, it documents the reasoning behind the change.

When in doubt, ask in an Issue first.