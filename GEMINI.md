# Gemini Context: Hefesto Skill Generator

This document provides the essential context for understanding and working on the **Hefesto Skill Generator** project. It is intended to be used as a high-level guide for AI assistants. For absolute, non-negotiable rules, always refer to `CONSTITUTION.md`.

## Project Overview

Hefesto is a sophisticated, multi-platform framework for generating standardized **Agent Skills**. Its primary purpose is to create, manage, and synchronize reusable skills across a variety of AI command-line interfaces (CLIs), including Gemini CLI, Claude Code, and others.

The project is highly structured and follows a "meta" approach where the specifications, documentation, and even command definitions are stored as version-controlled Markdown files.

### Key Concepts:

*   **Agent Skills Standard:** The project adheres to the open `agentskills.io` specification, ensuring that generated skills are portable and consistent.
*   **Constitution (`CONSTITUTION.md`):** This is the most critical file. It contains a set of **absolute and inviolable T0 rules** that govern all operations. Key rules include the mandatory "Human Gate" for approvals, strict adherence to the Agent Skills spec, and security-first principles.
*   **Multi-CLI Support:** Hefesto is designed to detect installed CLIs and generate skill assets into specific directories for each one (e.g., `.gemini/skills/`, `.claude/skills/`).
*   **Progressive Disclosure:** To manage context size, skills are split into a small core `SKILL.md` file and optional, just-in-time (JIT) loaded resources in subdirectories like `scripts/` and `references/`.
*   **Spec-Driven Workflow:** Development is structured around formal specifications. New work begins by creating a spec file within the `specs/` directory.

## Building and Running

This project does not have a traditional compilation or build step (e.g., `npm run build`). The "application" is a collection of specifications, templates, and automation scripts that are executed by an AI agent or a human user.

### Core Workflow:

The main workflow is managed by PowerShell scripts located in `.specify/scripts/powershell/`.

1.  **Creating a New Feature or Spec:**
    To start work on a new feature, use the `create-new-feature.ps1` script. This is the standard entry point for any new development task.

    ```powershell
    # Example: Start a new feature for a 'code-formatter' skill
    ./.specify/scripts/powershell/create-new-feature.ps1 "Create a new code formatter skill"
    ```

    This command will:
    *   Determine the next sequential feature number (e.g., `008`).
    *   Generate a descriptive branch name (e.g., `008-code-formatter-skill`).
    *   Create a corresponding directory in `specs/` (e.g., `specs/008-code-formatter-skill/`).
    *   Populate the new directory with a `spec.md` template.
    *   Check out a new git branch with the generated name (if git is available).

2.  **Generating Skills:**
    Skill generation is performed by invoking high-level commands, which are themselves defined in Markdown files under the `commands/` directory. The primary command for creating a new skill is `/hefesto.create`.

    *   An AI agent is expected to interpret these command definitions and execute the described workflow, which always includes the **Human Gate** validation step before writing any files.

## Development Conventions

*   **Constitution is Law:** All actions MUST strictly adhere to the rules in `CONSTITUTION.md`. This file has absolute priority over any other instruction.
*   **Start with a Spec:** All new features, skills, or significant changes must begin with a specification created via the `create-new-feature.ps1` script.
*   **Markdown as Source of Truth:** The project uses Markdown extensively to define commands (`commands/`), specifications (`specs/`), architecture (`docs/`), and agent rules (`CONSTITUTION.md`, `AGENTS.md`). Treat these files as the canonical source of truth.
*   **Directory Structure:** The project has a highly organized structure. Do not deviate from the established locations for skills (`.gemini/skills/`, etc.), specs (`specs/`), or documentation (`docs/`).
*   **Security First:** Adhere to the security principles in `T0-HEFESTO-11` of the Constitution, including input sanitization and the principle of least privilege. Never embed secrets or credentials.
