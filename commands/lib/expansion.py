"""
Hefesto Skill Generator - Expansion Module

JIT resource management for iterative skill expansion (FR-015 to FR-019).
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from .preview import PreviewObject, ResourceInfo
from .timeout import input_with_timeout, TimeoutError
from .colors import bold, cyan, yellow, gray, warning, success


def prompt_for_resources(preview: PreviewObject) -> List[ResourceInfo]:
    """
    Prompt user to add JIT resources iteratively (FR-015, FR-016).

    Args:
        preview: Current PreviewObject to expand

    Returns:
        List of ResourceInfo objects to add

    Raises:
        TimeoutError: If user doesn't respond within timeout
    """
    resources = []

    print(f"\n{bold(cyan('=' * 60))}")
    print(f"{bold('Expand Skill: Add Optional Resources')}")
    print(f"{cyan('=' * 60)}\n")

    print("Available resource types:")
    print("  [scripts]    - Executable scripts")
    print("  [references] - Detailed documentation")
    print("  [assets]     - Static files (configs, templates, etc.)")
    print("  [done]       - Finish adding resources\n")

    while True:
        resource_type = (
            input_with_timeout(
                f"{bold('Resource type [scripts/references/assets/done]:')} ",
                timeout_seconds=300,
            )
            .strip()
            .lower()
        )

        if resource_type == "done":
            break

        if resource_type not in ["scripts", "references", "assets"]:
            print(
                warning(
                    f"Invalid resource type '{resource_type}'. Choose: scripts, references, assets, done"
                )
            )
            continue

        # Collect resource details (FR-017)
        resource = _collect_resource_details(resource_type)

        if resource:
            resources.append(resource)
            print(success(f"Added {resource_type} resource: {resource.filename}"))

            # Ask if user wants to add more of the same type (FR-019)
            more = (
                input_with_timeout(
                    f"\n{bold(f'Add another {resource_type} resource? [y/N]:')} ",
                    timeout_seconds=300,
                )
                .strip()
                .lower()
            )

            if more not in ["y", "yes"]:
                print(
                    gray(
                        f"Finished adding {resource_type}. Choose another type or 'done'.\n"
                    )
                )

    if resources:
        print(f"\n{success(f'Added {len(resources)} resource(s) to skill.')}")
    else:
        print(f"\n{gray('No resources added.')}")

    return resources


def _collect_resource_details(resource_type: str) -> Optional[ResourceInfo]:
    """
    Collect filename and content for a specific resource type (FR-017).

    Args:
        resource_type: Type of resource ('scripts', 'references', 'assets')

    Returns:
        ResourceInfo object or None if cancelled
    """
    print(f"\n{gray(f'--- Adding {resource_type} resource ---')}")

    # Get filename
    filename = input_with_timeout(f"{bold('Filename:')} ", timeout_seconds=300).strip()

    if not filename:
        print(warning("Filename cannot be empty. Skipping."))
        return None

    # For scripts and references, get content inline
    if resource_type in ["scripts", "references"]:
        print(f"{gray('Enter content (type END on a new line to finish):')}")

        content_lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            content_lines.append(line)

        content = "\n".join(content_lines)

        if not content.strip():
            print(warning("Content cannot be empty. Skipping."))
            return None

        size = len(content.encode("utf-8"))

        return ResourceInfo(
            resource_type=resource_type,
            filename=filename,
            content=content,
            path=None,
            size=size,
        )

    # For assets, get file path
    elif resource_type == "assets":
        file_path_str = input_with_timeout(
            f"{bold('File path:')} ", timeout_seconds=300
        ).strip()

        file_path = Path(file_path_str)

        if not file_path.exists():
            print(warning(f"File not found: {file_path}. Skipping."))
            return None

        if not file_path.is_file():
            print(warning(f"Path is not a file: {file_path}. Skipping."))
            return None

        size = file_path.stat().st_size

        return ResourceInfo(
            resource_type=resource_type,
            filename=filename,
            content=None,
            path=file_path,
            size=size,
        )

    return None


def update_preview_with_resources(
    preview: PreviewObject, resources: List[ResourceInfo]
) -> PreviewObject:
    """
    Update preview with added resources (FR-018).

    Args:
        preview: Original PreviewObject
        resources: Resources to add

    Returns:
        Updated PreviewObject
    """
    # Add resources to preview
    preview.resources.extend(resources)

    # Update file_paths and file_sizes for each CLI
    for cli in preview.target_clis:
        for resource in resources:
            # Construct resource path
            resource_path = Path(
                f".{cli}/skills/{preview.skill_name}/{resource.resource_type}/{resource.filename}"
            )

            # Add to file_paths
            if cli not in preview.file_paths:
                preview.file_paths[cli] = []

            preview.file_paths[cli].append(resource_path)

            # Add to file_sizes
            preview.file_sizes[str(resource_path)] = resource.size

    return preview
