"""Hefesto CLI - Template-driven Agent Skill generator for 7 AI CLIs."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

__version__ = "2.2.0"

app = typer.Typer(
    name="hefesto",
    help="Template-driven Agent Skill generator for 7 AI CLIs.",
    no_args_is_help=True,
)
console = Console()

# ── CLI Configuration ────────────────────────────────────────────────────────

CLI_CONFIG: dict[str, dict] = {
    "claude": {
        "name": "Claude Code",
        "folder": ".claude",
        "skills_dir": "skills",
        "commands_dir": "commands",
        "var_syntax": "$ARGUMENTS",
    },
    "gemini": {
        "name": "Gemini CLI",
        "folder": ".gemini",
        "skills_dir": "skills",
        "commands_dir": "commands",
        "var_syntax": "{{args}}",
    },
    "codex": {
        "name": "Codex CLI",
        "folder": ".codex",
        "skills_dir": "skills",
        "commands_dir": "prompts",
        "var_syntax": "$ARGUMENTS",
    },
    "cursor": {
        "name": "Cursor",
        "folder": ".cursor",
        "skills_dir": "skills",
        "commands_dir": "commands",
        "var_syntax": "$ARGUMENTS",
    },
    "opencode": {
        "name": "OpenCode",
        "folder": ".opencode",
        "skills_dir": "skills",
        "commands_dir": "command",
        "var_syntax": "$ARGUMENTS",
    },
    "qwen": {
        "name": "Qwen",
        "folder": ".qwen",
        "skills_dir": "skills",
        "commands_dir": "commands",
        "var_syntax": "{{args}}",
    },
    "copilot": {
        "name": "GitHub Copilot",
        "folder": ".github",
        "skills_dir": "skills",
        "commands_dir": "agents",  # Copilot uses .github/agents/ and .github/prompts/
        "var_syntax": "$ARGUMENTS",
    },
}


# ── Utility Functions ────────────────────────────────────────────────────────


def get_templates_dir() -> Path:
    """Resolve templates directory (works installed or from source)."""
    # Try relative to source first (development)
    src_templates = Path(__file__).parent.parent.parent / "templates_hefesto"
    if src_templates.exists():
        return src_templates

    # Try installed location (wheel shared-data)
    import sys

    if sys.prefix:
        wheel_templates = Path(sys.prefix) / "share" / "hefesto_cli" / "templates"
        if wheel_templates.exists():
            return wheel_templates

    # Fallback: try package resources
    try:
        import importlib.resources as pkg_resources

        pkg_path = Path(str(pkg_resources.files("hefesto_cli")))
        pkg_templates = pkg_path / "templates"
        if pkg_templates.exists():
            return pkg_templates
    except (ImportError, AttributeError):
        pass

    raise FileNotFoundError(
        "Could not find templates directory. Ensure hefesto-cli is properly installed."
    )


def get_project_root(target_dir: Path | None = None) -> Path:
    """Find project root (looks for .git or uses current dir)."""
    current = target_dir or Path.cwd()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return target_dir or Path.cwd()


def detect_clis(project_root: Path) -> dict[str, Path]:
    """Detect installed AI CLIs by checking directories and PATH."""
    detected = {}

    for cli_id, config in CLI_CONFIG.items():
        cli_folder = project_root / config["folder"]

        # Special handling for Copilot
        if cli_id == "copilot":
            # Check for Copilot signals
            if (project_root / ".github" / "copilot-instructions.md").exists() or (
                project_root / ".github" / "agents"
            ).exists():
                detected[cli_id] = cli_folder
        elif cli_folder.exists():
            detected[cli_id] = cli_folder

    return detected


def get_hefesto_dir(project_root: Path) -> Path:
    """Get .hefesto directory path."""
    return project_root / ".hefesto"


def is_hefesto_installed(project_root: Path) -> bool:
    """Check if Hefesto is installed in the project."""
    hefesto_dir = get_hefesto_dir(project_root)
    version_file = hefesto_dir / "version"
    return version_file.exists()


def get_hefesto_version(project_root: Path) -> str | None:
    """Get installed Hefesto version."""
    version_file = get_hefesto_dir(project_root) / "version"
    if version_file.exists():
        return version_file.read_text().strip()
    return None


# ── Commands ─────────────────────────────────────────────────────────────────


@app.command()
def init(
    target_dir: Path | None = typer.Argument(
        None, help="Target directory (defaults to current directory)"
    ),
    ai_cli: str | None = typer.Option(
        None, "--ai", help="Specific AI CLI to install to (claude, gemini, etc.)"
    ),
):
    """
    Bootstrap Hefesto: detect CLIs, create directories, install commands.

    This complements the bash/PowerShell installer scripts.
    """
    project_root = get_project_root(target_dir)

    console.print(
        Panel(
            f"[bold cyan]Hefesto Skill Generator v{__version__}[/]",
            title="Bootstrap",
            border_style="cyan",
        )
    )

    # Check if already installed
    if is_hefesto_installed(project_root):
        installed_version = get_hefesto_version(project_root)
        console.print(
            f"\n[yellow]![/] Hefesto v{installed_version} is already installed."
        )
        console.print("\n[dim]Use `hefesto check` to verify installation.[/]")
        return

    # Detect CLIs
    console.print("\n[bold]Detecting AI CLIs...[/]")
    detected_clis = detect_clis(project_root)

    if not detected_clis:
        console.print("[yellow]![/] No AI CLIs detected.")
        console.print("\n[dim]Creating .claude/ as default...[/]")
        detected_clis = {"claude": project_root / ".claude"}

    # Display detected CLIs
    table = Table(title="Detected CLIs", show_header=True, header_style="bold cyan")
    table.add_column("CLI", style="cyan")
    table.add_column("Path", style="dim")
    table.add_column("Status", justify="center")

    for cli_id, cli_path in detected_clis.items():
        cli_name = CLI_CONFIG[cli_id]["name"]
        status = "[green]+[/]" if cli_path.exists() else "[yellow]new[/]"
        table.add_row(cli_name, str(cli_path.relative_to(project_root)), status)

    console.print(table)

    # Filter if specific CLI requested
    if ai_cli:
        if ai_cli not in detected_clis:
            console.print(f"\n[red]-[/] CLI '{ai_cli}' not detected.")
            raise typer.Exit(1)
        detected_clis = {ai_cli: detected_clis[ai_cli]}

    # Create .hefesto directory
    console.print("\n[bold]Creating .hefesto directory...[/]")
    hefesto_dir = get_hefesto_dir(project_root)
    templates_target = hefesto_dir / "templates"
    templates_target.mkdir(parents=True, exist_ok=True)

    # Copy templates
    templates_src = get_templates_dir()
    templates_to_copy = [
        "skill-template.md",
        "quality-checklist.md",
        "cli-compatibility.md",
        "agent-template.md",
    ]

    for template_file in templates_to_copy:
        src = templates_src / template_file
        if src.exists():
            shutil.copy(src, templates_target / template_file)
            console.print(f"  [green]+[/] {template_file}")

    # Write version
    (hefesto_dir / "version").write_text(__version__)
    console.print(f"  [green]+[/] version ({__version__})")

    # Create skills directories and install commands
    console.print("\n[bold]Installing commands and creating skills directories...[/]")

    for cli_id, cli_path in detected_clis.items():
        cli_name = CLI_CONFIG[cli_id]["name"]
        skills_dir = cli_path / CLI_CONFIG[cli_id]["skills_dir"]
        commands_dir = cli_path / CLI_CONFIG[cli_id]["commands_dir"]

        # Create skills directory
        skills_dir.mkdir(parents=True, exist_ok=True)

        # Create commands directory
        commands_dir.mkdir(parents=True, exist_ok=True)

        # Install slash commands
        commands_src = templates_src / "commands"
        if commands_src.exists():
            for cmd_file in commands_src.glob("hefesto.*.md"):
                shutil.copy(cmd_file, commands_dir / cmd_file.name)

        console.print(f"  [green]+[/] {cli_name}")

    # Success summary
    console.print(
        Panel(
            f"[green]+[/] Hefesto v{__version__} installed successfully!\n\n"
            f"[bold]Installed:[/]\n"
            f"  - .hefesto/templates/ (4 templates)\n"
            f"  - Commands in {len(detected_clis)} CLI(s)\n\n"
            f"[bold]Next steps:[/]\n"
            f"  1. [cyan]hefesto check[/] - Verify installation\n"
            f"  2. [cyan]hefesto list[/] - List installed skills\n"
            f'  3. [cyan]/hefesto.create "description"[/] - Create your first skill',
            title="Installation Complete",
            border_style="green",
        )
    )


@app.command()
def check(
    target_dir: Path | None = typer.Argument(
        None, help="Target directory (defaults to current directory)"
    ),
):
    """
    Show Hefesto installation status and detected CLIs.
    """
    project_root = get_project_root(target_dir)

    console.print(
        Panel(
            "[bold cyan]Hefesto Status[/]",
            title="Check",
            border_style="cyan",
        )
    )

    # Check installation
    hefesto_dir = get_hefesto_dir(project_root)

    if not is_hefesto_installed(project_root):
        console.print("\n[red]-[/] Hefesto is not installed in this project.")
        console.print("\n[dim]Run: hefesto init[/]")
        raise typer.Exit(1)

    installed_version = get_hefesto_version(project_root)
    console.print(f"\n[green]+[/] Hefesto v{installed_version} installed")

    # Check templates
    console.print("\n[bold]Templates:[/]")
    templates_dir = hefesto_dir / "templates"
    required_templates = [
        "skill-template.md",
        "quality-checklist.md",
        "cli-compatibility.md",
    ]

    for template in required_templates:
        template_path = templates_dir / template
        if template_path.exists():
            console.print(f"  [green]+[/] {template}")
        else:
            console.print(f"  [red]-[/] {template} [dim](missing)[/]")

    # Detect CLIs
    console.print("\n[bold]Detected CLIs:[/]")
    detected_clis = detect_clis(project_root)

    if not detected_clis:
        console.print("  [yellow]![/] No AI CLIs detected")
    else:
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("CLI", style="cyan")
        table.add_column("Skills Dir", style="dim")
        table.add_column("Commands", justify="center")
        table.add_column("Skills", justify="center")

        for cli_id, cli_path in detected_clis.items():
            cli_name = CLI_CONFIG[cli_id]["name"]
            skills_dir = cli_path / CLI_CONFIG[cli_id]["skills_dir"]
            commands_dir = cli_path / CLI_CONFIG[cli_id]["commands_dir"]

            # Count commands
            cmd_count = 0
            if commands_dir.exists():
                cmd_files = list(commands_dir.glob("hefesto.*.md"))
                cmd_count = len(cmd_files)

            # Count skills
            skill_count = 0
            if skills_dir.exists():
                skill_count = len(
                    [
                        d
                        for d in skills_dir.iterdir()
                        if d.is_dir() and (d / "SKILL.md").exists()
                    ]
                )

            skills_path = (
                str(skills_dir.relative_to(project_root))
                if skills_dir.exists()
                else "[dim]missing[/]"
            )
            table.add_row(
                cli_name,
                skills_path,
                f"[cyan]{cmd_count}[/]/7" if cmd_count > 0 else "[dim]0[/]/7",
                f"[green]{skill_count}[/]" if skill_count > 0 else "[dim]0[/]",
            )

        console.print(table)

    # Show next steps
    console.print(
        f"\n[bold]Next steps:[/]\n"
        f'  - [cyan]/hefesto.create "description"[/] - Create a skill\n'
        f"  - [cyan]/hefesto.list[/] - List all skills\n"
        f"  - [cyan]/hefesto.validate skill-name[/] - Validate a skill"
    )


@app.command(name="list")
def list_skills(
    target_dir: Path | None = typer.Argument(
        None, help="Target directory (defaults to current directory)"
    ),
):
    """
    List all installed skills across detected CLIs.
    """
    project_root = get_project_root(target_dir)

    console.print(
        Panel(
            "[bold cyan]Installed Skills[/]",
            title="List",
            border_style="cyan",
        )
    )

    detected_clis = detect_clis(project_root)

    if not detected_clis:
        console.print("\n[yellow]![/] No AI CLIs detected.")
        console.print("\n[dim]Run: hefesto init[/]")
        raise typer.Exit(1)

    # Collect all skills
    all_skills = {}  # skill_name -> [cli_ids]

    for cli_id, cli_path in detected_clis.items():
        skills_dir = cli_path / CLI_CONFIG[cli_id]["skills_dir"]
        if not skills_dir.exists():
            continue

        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skill_name = skill_dir.name
                if skill_name not in all_skills:
                    all_skills[skill_name] = []
                all_skills[skill_name].append(cli_id)

    if not all_skills:
        console.print("\n[dim]No skills installed yet.[/]")
        console.print("\n[dim]Create your first skill:[/]")
        console.print('  [cyan]/hefesto.create "description"[/]')
        return

    # Display skills tree
    tree = Tree("[bold cyan]Skills[/]")

    for skill_name in sorted(all_skills.keys()):
        cli_ids = all_skills[skill_name]
        cli_names = [CLI_CONFIG[cli_id]["name"] for cli_id in cli_ids]

        skill_node = tree.add(f"[green]{skill_name}[/]")
        skill_node.add(f"[dim]Installed in: {', '.join(cli_names)}[/]")

    console.print("\n")
    console.print(tree)
    console.print(f"\n[bold]Total:[/] {len(all_skills)} skill(s)")


@app.command()
def version():
    """
    Show Hefesto CLI version.
    """
    console.print(f"[bold cyan]Hefesto CLI[/] v{__version__}")
    console.print(f"[dim]Template-driven Agent Skill generator[/]")


def main():
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()
