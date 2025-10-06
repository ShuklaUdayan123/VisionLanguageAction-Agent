# VisionLanguageAction-Agent

A project that integrates **AI2-THOR** with a **language-to-action parser** using the **TinyLlama** model. This allows a virtual agent to interpret natural language commands and perform actions in a simulated household environment.

---

## Features

- Control a virtual agent in AI2-THOR environments.
- Parse natural language commands into structured JSON actions.
- Supports actions like:
  - `MoveAhead`
  - `RotateRight`
  - `PickupObject` (optional)
- Fully modular: separate files for language parsing and AI2-THOR interface.

---

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/ShuklaUdayan123/VisionLanguageAction-Agent.git
cd VisionLanguageAction-Agent
