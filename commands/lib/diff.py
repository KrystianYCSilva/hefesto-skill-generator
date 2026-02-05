"""
Hefesto Skill Generator - Markdown Diff Module

Section-by-section markdown diffing for merge conflicts (FR-024).
"""

import difflib
import re
from typing import List, Tuple, Dict

from .timeout import input_with_timeout
from .colors import bold, cyan, yellow, green, red, gray, warning


def extract_sections(markdown_content: str) -> List[Tuple[str, str]]:
    """
    Split markdown into sections: frontmatter + each heading block.

    Args:
        markdown_content: Full markdown content

    Returns:
        List of (section_name, content) tuples
    """
    sections = []

    # Extract frontmatter (between first two ---)
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n", markdown_content, re.DOTALL)
    if frontmatter_match:
        sections.append(("frontmatter", frontmatter_match.group(0)))
        remaining = markdown_content[frontmatter_match.end() :]
    else:
        remaining = markdown_content

    # Split by headings (# or ##)
    heading_pattern = r"^(#{1,6})\s+(.+)$"
    current_section = None
    current_content = []

    for line in remaining.split("\n"):
        match = re.match(heading_pattern, line)
        if match:
            # Save previous section
            if current_section:
                sections.append((current_section, "\n".join(current_content)))

            # Start new section
            current_section = match.group(2).strip()
            current_content = [line]
        else:
            if current_section:
                current_content.append(line)
            else:
                # Content before any heading
                if line.strip():
                    if not current_content:
                        current_section = "_preamble"
                        current_content = [line]
                    else:
                        current_content.append(line)

    # Save last section
    if current_section and current_content:
        sections.append((current_section, "\n".join(current_content)))

    return sections


def display_section_diff(section_name: str, existing: str, new: str) -> None:
    """
    Display unified diff for one section.

    Args:
        section_name: Name of section being diffed
        existing: Existing section content
        new: New section content
    """
    print(f"\n{cyan('=' * 60)}")
    print(f"{bold(f'Section: {section_name}')}")
    print(f"{cyan('=' * 60)}\n")

    if not existing and new:
        print(green("[NEW SECTION]"))
        print(gray("Content:"))
        print(new[:200] + "..." if len(new) > 200 else new)
    elif existing and not new:
        print(red("[SECTION DELETED IN NEW VERSION]"))
        print(gray("Original content:"))
        print(existing[:200] + "..." if len(existing) > 200 else existing)
    else:
        # Show unified diff
        existing_lines = existing.splitlines(keepends=True)
        new_lines = new.splitlines(keepends=True)

        diff = difflib.unified_diff(
            existing_lines, new_lines, fromfile="existing", tofile="new", lineterm=""
        )

        diff_lines = list(diff)

        if len(diff_lines) <= 2:
            # No real changes (just header lines)
            print(gray("No changes in this section"))
            return

        # Display diff with colors
        for line in diff_lines[2:]:  # Skip header lines
            if line.startswith("+"):
                print(green(line))
            elif line.startswith("-"):
                print(red(line))
            elif line.startswith("@@"):
                print(cyan(line))
            else:
                print(gray(line))


def prompt_section_choice(section_name: str, existing: str, new: str) -> str:
    """
    Prompt user to keep existing or use new for a section.

    Args:
        section_name: Name of section
        existing: Existing section content
        new: New section content

    Returns:
        'existing' or 'new'
    """
    # Display diff
    display_section_diff(section_name, existing, new)

    # Prompt for choice
    while True:
        print(f"\n{bold('Keep [existing] or use [new]?')} ", end="")
        choice = input_with_timeout("", timeout_seconds=300).strip().lower()

        if choice in ["existing", "e", "keep"]:
            return "existing"
        elif choice in ["new", "n", "use"]:
            return "new"
        else:
            print(
                warning(f"Invalid choice '{choice}'. Please choose 'existing' or 'new'")
            )


def merge_sections(existing_skill: str, new_skill: str) -> str:
    """
    Guide user through section-by-section merge (FR-024).

    Args:
        existing_skill: Existing SKILL.md content
        new_skill: New SKILL.md content to merge

    Returns:
        Merged skill content
    """
    print(f"\n{bold(cyan('=' * 60))}")
    print(f"{bold('Merge Mode: Section-by-Section Approval')}")
    print(f"{cyan('=' * 60)}\n")

    print(gray("You'll be shown each changed section."))
    print(gray("Choose to keep existing or use new content for each.\n"))

    # Extract sections
    existing_sections = dict(extract_sections(existing_skill))
    new_sections = dict(extract_sections(new_skill))

    merged_sections = {}
    all_section_names = sorted(set(existing_sections.keys()) | set(new_sections.keys()))

    # Process each section
    for section_name in all_section_names:
        existing = existing_sections.get(section_name, "")
        new = new_sections.get(section_name, "")

        if existing == new:
            # No change - keep existing
            merged_sections[section_name] = existing
            print(f"{green('✓')} Section '{section_name}': No changes")
            continue

        # Prompt for choice
        choice = prompt_section_choice(section_name, existing, new)

        if choice == "existing":
            merged_sections[section_name] = existing
            print(green(f"✓ Keeping existing content for '{section_name}'"))
        else:
            merged_sections[section_name] = new
            print(green(f"✓ Using new content for '{section_name}'"))

    # Reconstruct merged markdown
    return reconstruct_markdown(merged_sections, all_section_names)


def reconstruct_markdown(sections: Dict[str, str], section_order: List[str]) -> str:
    """
    Rebuild markdown from section dictionary.

    Args:
        sections: Dict mapping section name to content
        section_order: Order of sections to maintain

    Returns:
        Complete markdown string
    """
    parts = []

    # Frontmatter always first
    if "frontmatter" in sections:
        parts.append(sections["frontmatter"])

    # Preamble (content before any heading)
    if "_preamble" in sections:
        parts.append(sections["_preamble"])

    # Other sections in order
    for section_name in section_order:
        if section_name not in ["frontmatter", "_preamble"]:
            content = sections.get(section_name, "")
            if content:
                parts.append(content)

    # Join with double newline for section separation
    return "\n\n".join(parts)
