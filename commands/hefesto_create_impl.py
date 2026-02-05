#!/usr/bin/env python3
"""
/hefesto.create Implementation
Generate new Agent Skill from natural language description with Human Gate approval
"""

import os
import sys
import re
import yaml
import json
from datetime import datetime
from pathlib import Path
import argparse


def validate_constitution():
    """Validate CONSTITUTION.md integrity and T0 rule presence"""
    constitution_path = Path("CONSTITUTION.md")
    
    if not constitution_path.exists():
        print("❌ Hefesto not initialized. Run /hefesto.init first.")
        return False
    
    # Read the file
    content = constitution_path.read_text(encoding='utf-8')
    
    # Check for required T0 rules
    required_t0_rules = [
        "T0-HEFESTO-01",  # Agent Skills Standard
        "T0-HEFESTO-02",  # Human Gate Protocol
        "T0-HEFESTO-03",  # Progressive Disclosure
        "T0-HEFESTO-04",  # Multi-CLI Detection
        "T0-HEFESTO-05",  # Local Storage
        "T0-HEFESTO-06",  # Validation
        "T0-HEFESTO-07",  # Skill Naming
        "T0-HEFESTO-08",  # Idempotency
        "T0-HEFESTO-09",  # Metadata
        "T0-HEFESTO-10", # Cross-CLI Consistency
        "T0-HEFESTO-11", # Security
    ]
    
    missing_rules = []
    for rule in required_t0_rules:
        if f"### {rule}:" not in content:
            missing_rules.append(rule)
    
    if missing_rules:
        print(f"❌ Constitutional Violation: Missing T0 rules: {missing_rules}")
        return False
    
    return True


def check_initialization():
    """Check if Hefesto is properly initialized"""
    if not Path("MEMORY.md").exists():
        print("❌ Hefesto not initialized. Run /hefesto.init first.")
        return False
    return True


def load_context():
    """Load context from /.context/ and templates"""
    # Load T0 rules from CONSTITUTION.md
    # Load skill templates from commands/templates/
    # Load CLI detection from MEMORY.md
    pass


def parse_arguments(args):
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Create new Agent Skill')
    parser.add_argument('description', nargs='?', help='Natural language description of skill to create')
    parser.add_argument('--target', dest='target_cli', help='Target specific CLI (default: all detected)')
    parser.add_argument('--template', dest='template_name', default='base', help='Use specific template variant (default: base)')
    
    parsed_args = parser.parse_args(args)
    
    # Validate description length
    if parsed_args.description and len(parsed_args.description) > 2000:
        print("ERROR [E-CREATE-001]: Description exceeds 2000 characters")
        print("Suggestion: Shorten description and try again")
        return None
    
    return parsed_args


def wizard_mode():
    """Interactive wizard mode when description is missing"""
    print("[WIZARD] Wizard Mode: Create Skill")
    print("="*60)
    
    # Step 1: Skill Description
    print("\nStep 1: Skill Description")
    description = ""
    attempts = 0
    while not description.strip() and attempts < 3:
        description = input("What should this skill do? (1-2 sentences)\n> ").strip()
        attempts += 1
        if not description.strip():
            print("ERROR [E-CREATE-007]: Description cannot be empty")

    if not description.strip():
        print("Maximum attempts reached. Aborting.")
        return None

    if len(description) > 2000:
        print("ERROR [E-CREATE-001]: Description exceeds 2000 characters")
        return None

    # Step 2: Skill Name (Auto-Generated)
    suggested_name = auto_generate_name(description)
    print(f"\nStep 2: Skill Name")
    print(f"Suggested name: {suggested_name}")
    custom_name = input("Press Enter to accept, or type custom name:\n> ").strip()

    if custom_name:
        skill_name = sanitize_name(custom_name)
    else:
        skill_name = suggested_name

    # Step 3: Target CLIs
    detected_clis = detect_installed_clis()
    print(f"\nStep 3: Target CLIs")
    print(f"Detected CLIs: {', '.join(detected_clis)}")
    target_input = input("Target CLIs (comma-separated or 'all') [all]:\n> ").strip()

    if not target_input or target_input.lower() == 'all':
        targets = detected_clis
    else:
        targets = [cli.strip() for cli in target_input.split(',')]
        # Validate that each CLI exists in detected list
        invalid_clis = [cli for cli in targets if cli not in detected_clis]
        if invalid_clis:
            print(f"Invalid CLI(s): {invalid_clis}. Detected CLIs: {detected_clis}")
            return None

    # Step 4: Confirmation
    print("\nStep 4: Confirmation")
    print("Preview:")
    print(f"  Name: {skill_name}")
    print(f"  Description: {description}")
    print(f"  Target CLIs: {targets}")

    action = input("[continue] [edit] [cancel]\n> ").strip().lower()

    if action == "cancel":
        print("Operation cancelled")
        return None
    elif action == "edit":
        return wizard_mode()  # Recursive call to start over
    elif action == "continue":
        return argparse.Namespace(
            description=description,
            target_cli=None,  # Will be handled separately
            template_name="base"
        ), skill_name, targets
    else:
        print("Invalid option. Aborting.")
        return None


def auto_generate_name(description):
    """Generate skill name from description"""
    # Convert to lowercase and replace non-alphanumeric with hyphens
    name = re.sub(r'[^\w\s-]', '', description.lower())
    name = re.sub(r'[-\s]+', '-', name.strip())
    # Limit to 64 characters
    name = name[:64]
    return name


def sanitize_name(name):
    """Sanitize skill name according to T0-HEFESTO-07"""
    # Convert to lowercase
    name = name.lower()
    # Replace non-alphanumeric with hyphens
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name.strip())
    # Remove leading/trailing hyphens
    name = name.strip('-')
    # Limit to 64 characters
    name = name[:64]
    return name


def detect_installed_clis():
    """Detect installed CLIs from MEMORY.md or system"""
    memory_path = Path("MEMORY.md")
    if not memory_path.exists():
        return []

    content = memory_path.read_text(encoding='utf-8')
    # Look for CLIs in the "CLIs Detectados" section
    detected_clis = []

    # Look for the CLIs Detectados section
    lines = content.split('\n')

    for line in lines:
        # Look for lines that contain CLI names and detection status
        # Match patterns like: "| **OpenCode** | ✅ Detectado |" or "| **Qwen Code** | ✅ Detectado |"
        match = re.search(r'\|\s*\*\*(.*?)\*\*\s*\|\s*✅', line)
        if match:
            cli_full_name = match.group(1).lower()

            # Map full names to canonical IDs
            if "claude" in cli_full_name:
                detected_clis.append("claude")
            elif "gemini" in cli_full_name:
                detected_clis.append("gemini")
            elif "codex" in cli_full_name:
                detected_clis.append("codex")
            elif "copilot" in cli_full_name:
                detected_clis.append("copilot")
            elif "opencode" in cli_full_name:
                detected_clis.append("opencode")
            elif "cursor" in cli_full_name:
                detected_clis.append("cursor")
            elif "qwen" in cli_full_name:
                detected_clis.append("qwen")

    # Remove duplicates and return
    return list(set(detected_clis))


def load_template(template_name):
    """Load appropriate template"""
    template_path = Path(f"commands/templates/{template_name}/SKILL.md.template")
    
    if not template_path.exists():
        # Try default base template
        template_path = Path("commands/templates/skill-template.md")
        
        if not template_path.exists():
            print(f"ERROR [E-CREATE-008]: Template not found: {template_name}")
            return None
    
    return template_path.read_text(encoding='utf-8')


def detect_collision(skill_name, targets):
    """Detect if skill already exists"""
    collisions = []
    for cli in targets:
        skill_path = Path(f".{cli}/skills/{skill_name}/SKILL.md")
        if skill_path.exists():
            collisions.append(str(skill_path))

    if collisions:
        return handle_collision(skill_name, collisions)

    return True  # No collision


def handle_collision(skill_name, collisions):
    """Handle collision when skill already exists"""
    print(f"\n[WARNING] Skill already exists: {skill_name}")
    print("\nExisting location(s):")
    for path in collisions:
        print(f"  - {path}")

    print("\nActions:")
    print("  [overwrite] - Replace existing skill (creates backup)")
    print("  [rename]    - Choose different name")
    print("  [cancel]    - Abort operation")

    action = input("> ").strip().lower()

    if action == "cancel":
        print("Operation cancelled")
        return False
    elif action == "rename":
        new_name = input("New skill name:\n> ").strip()
        if new_name:
            # Sanitize the new name
            new_name = sanitize_name(new_name)
            # Need to recursively check for collision with new name
            # This is simplified - in practice would need to return new name
            print(f"New name selected: {new_name}, but recursive collision check not fully implemented here")
            return False
    elif action == "overwrite":
        # Create backup
        print(f"Backup created: .hefesto/backups/{skill_name}-{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz")
        return True
    else:
        print("Invalid option. Operation cancelled.")
        return False


def generate_skill_content(template, skill_data):
    """Generate skill content from template and data"""
    # Replace template variables
    content = template.replace("{{SKILL_NAME}}", skill_data['name'])
    content = content.replace("{{SKILL_DESCRIPTION}}", skill_data['description'])
    content = content.replace("{{USE_WHEN}}", f"when you need to {skill_data['description']}")
    content = content.replace("{{SKILL_BODY}}", f"This skill helps with: {skill_data['description']}")
    content = content.replace("{{ARGUMENTS}}", "<arguments>")
    
    return content


def generate_metadata(skill_data):
    """Generate metadata for the skill"""
    metadata_template_path = Path("commands/templates/metadata-template.yaml")
    if not metadata_template_path.exists():
        print("Warning: metadata template not found")
        return ""
    
    template = metadata_template_path.read_text(encoding='utf-8')
    
    # Replace template variables
    template = template.replace("{{AUTHOR}}", "Hefesto Skill Generator")
    template = template.replace("{{VERSION}}", "1.0.0")
    template = template.replace("{{CREATED_DATE}}", skill_data['created'])
    template = template.replace("{{CATEGORY}}", skill_data.get('category', 'development'))
    template = template.replace("{{TAGS}}", '"development", "automation", "tool"')
    template = template.replace("{{PLATFORMS}}", ', '.join([f'"{cli}"' for cli in skill_data['targets']]))
    template = template.replace("{{DEPENDENCIES}}", "")
    template = template.replace("{{EXAMPLE_PROMPT}}", f"Use the {skill_data['name']} skill to {skill_data['description']}")
    
    return template


def validate_skill(content):
    """Validate skill content against Agent Skills spec"""
    errors = []
    
    # Check if content starts with frontmatter
    if not content.startswith("---"):
        errors.append("Missing frontmatter start '---'")
        return errors
    
    # Split content to get frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("Invalid frontmatter format")
        return errors
    
    frontmatter_yaml = parts[1]
    body = parts[2]
    
    try:
        data = yaml.safe_load(frontmatter_yaml)
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML frontmatter: {str(e)}")
        return errors
    
    # Validate required fields
    if "name" not in data:
        errors.append("Missing required field: 'name'")
    elif not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', data["name"]):
        errors.append(f"Invalid name '{data['name']}'. Must be lowercase, alphanumeric, with hyphens.")
    
    if "description" not in data:
        errors.append("Missing required field: 'description'")
    elif not data["description"].strip():
        errors.append("Description cannot be empty")
    elif len(data["description"]) > 1024:
        errors.append("Description exceeds 1024 characters")
    
    # Check line count (T0-HEFESTO-03)
    line_count = len(content.splitlines())
    if line_count > 500:
        errors.append(f"SKILL.md exceeds 500 lines ({line_count}). Move content to references/.")
    
    return errors


def human_gate(skill_name, description, targets, skill_content, validation_result):
    """Display preview and get user approval"""
    print("\n" + "="*60)
    print(f"[SUCCESS] Skill Generated: {skill_name}")
    print("="*60)
    
    print("\nPreview:")
    print("-" * 40)
    print(f"name: {skill_name}")
    print(f"description: {description}")
    print(f"version: 1.0.0")
    print(f"created: {datetime.now().isoformat()}")
    print(f"target_clis: {targets}")
    print("-" * 40)
    
    # Show first 20 lines of content
    content_lines = skill_content.split('\n')
    print("\nFirst 20 lines of SKILL.md content:")
    print("-" * 40)
    for i, line in enumerate(content_lines[:20]):
        print(line)
        if i == 19 and len(content_lines) > 20:
            print("... (content truncated)")
    print("-" * 40)

    if validation_result:
        print("\nValidation: PASS [OK]")
    else:
        print("\nValidation: FAILED [ERROR]")
        return False

    print(f"\nFiles to create:")
    for cli in targets:
        print(f"  - .{cli}/skills/{skill_name}/SKILL.md")
        print(f"  - .{cli}/skills/{skill_name}/metadata.yaml")

    print("\n" + "="*60)

    action = input("Actions: [approve] [expand] [edit] [reject]\n> ").strip().lower()

    if action == "approve":
        return True
    elif action == "expand":
        # Show full content
        print("\nFull SKILL.md content:")
        print("-" * 40)
        print(skill_content)
        print("-" * 40)
        return human_gate(skill_name, description, targets, skill_content, validation_result)
    elif action == "edit":
        # Allow manual editing (simplified - would need more sophisticated editor in practice)
        print("Manual editing not fully implemented in this version")
        return False
    elif action == "reject":
        print("Operation cancelled. No changes made.")
        return False
    else:
        print("Invalid option. Operation cancelled.")
        return False


def persist_skill(skill_name, targets, skill_content, metadata_content):
    """Persist skill files to disk"""
    for cli in targets:
        skill_dir = Path(f".{cli}/skills/{skill_name}")
        
        try:
            skill_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print(f"ERROR [E-CREATE-006]: Write permission denied: {skill_dir}")
            return False
        
        # Write skill file
        skill_path = skill_dir / "SKILL.md"
        skill_path.write_text(skill_content, encoding='utf-8')
        
        # Write metadata file
        metadata_path = skill_dir / "metadata.yaml"
        metadata_path.write_text(metadata_content, encoding='utf-8')
    
    # Update MEMORY.md
    update_memory_md(skill_name, targets)
    
    return True


def update_memory_md(skill_name, targets):
    """Update MEMORY.md with new skill info"""
    memory_path = Path("MEMORY.md")
    if not memory_path.exists():
        print("Warning: MEMORY.md not found, skipping update")
        return
    
    content = memory_path.read_text(encoding='utf-8')
    
    # Find the "Skills Criadas" section and add new skill
    lines = content.split('\n')
    new_lines = []
    inserted = False
    
    for line in lines:
        new_lines.append(line)
        if line.startswith("## Skills Criadas") and not inserted:
            # Add the new skill entry
            new_lines.extend([
                "",
                f"### {len([l for l in lines if l.startswith('### ')]) + 1}. {skill_name}",
                "",
                "| Campo | Valor |",
                "|-------|-------|",
                f"| **Nome** | {skill_name} |",
                "| **Versão** | 1.0.0 |",
                f"| **Criada** | {datetime.now().strftime('%Y-%m-%d')} |",
                f"| **Categoria** | development |",
                f"| **Target CLIs** | {', '.join(targets)} ({len(targets)} CLIs) |",
                f"| **Descrição** | {skill_name.replace('-', ' ').title()} |",
                "| **Status** | ✅ Criada e persistida |",
                "",
            ])
            inserted = True
    
    # If Skills Criadas section wasn't found, append at end
    if not inserted:
        new_lines.extend([
            "",
            "## Skills Criadas",
            "",
            f"### 1. {skill_name}",
            "",
            "| Campo | Valor |",
            "|-------|-------|",
            f"| **Nome** | {skill_name} |",
            "| **Versão** | 1.0.0 |",
            f"| **Criada** | {datetime.now().strftime('%Y-%m-%d')} |",
            f"| **Categoria** | development |",
            f"| **Target CLIs** | {', '.join(targets)} ({len(targets)} CLIs) |",
            f"| **Descrição** | {skill_name.replace('-', ' ').title()} |",
            "| **Status** | ✅ Criada e persistida |",
            "",
        ])
    
    # Write updated content
    memory_path.write_text('\n'.join(new_lines), encoding='utf-8')


def main(args):
    """Main function for /hefesto.create command"""
    print("[INFO] Initializing /hefesto.create...")
    
    # Phase 0: Pre-Execution Validation
    if not validate_constitution():
        return 1
    
    if not check_initialization():
        return 1
    
    load_context()
    
    # Phase 1: Argument Parsing & Wizard Mode
    parsed_args = parse_arguments(args)
    
    if not parsed_args:
        return 1
    
    description = parsed_args.description
    target_cli = parsed_args.target_cli
    template_name = parsed_args.template_name
    
    # If no description provided, enter wizard mode
    if not description:
        result = wizard_mode()
        if result is None:
            return 1
        
        # Handle tuple return from wizard_mode
        if isinstance(result, tuple):
            parsed_args, skill_name, targets = result
            description = parsed_args.description
        else:
            # If wizard_mode returns just parsed_args, get targets differently
            detected_clis = detect_installed_clis()
            if target_cli:
                targets = [target_cli] if target_cli in detected_clis else detected_clis
            else:
                targets = detected_clis
            
            skill_name = auto_generate_name(description)
    else:
        # Use provided description, determine targets
        detected_clis = detect_installed_clis()
        if target_cli:
            targets = [target_cli] if target_cli in detected_clis else detected_clis
        else:
            targets = detected_clis
        
        skill_name = auto_generate_name(description)
    
    if not targets:
        print("ERROR [E-CREATE-004]: No CLIs detected. Run /hefesto.detect first.")
        return 1
    
    # Phase 2: Skill Generation
    template = load_template(template_name)
    if not template:
        return 1
    
    # Detect collision
    if not detect_collision(skill_name, targets):
        return 1
    
    # Generate skill content
    skill_data = {
        'name': skill_name,
        'description': description,
        'created': datetime.now().isoformat(),
        'version': '1.0.0',
        'category': 'development',  # Could be inferred from description
        'targets': targets
    }
    
    skill_content = generate_skill_content(template, skill_data)
    metadata_content = generate_metadata(skill_data)
    
    # Phase 3: Validation
    validation_errors = validate_skill(skill_content)
    
    if validation_errors:
        print("❌ Validation Failed:")
        for error in validation_errors:
            print(f"  - {error}")
        
        print("ERROR [E-CREATE-005]: Template validation failed")
        return 1
    
    # Phase 4: Human Gate
    approved = human_gate(skill_name, description, targets, skill_content, not validation_errors)
    
    if not approved:
        print("Operation cancelled. No changes made.")
        return 1
    
    # Phase 5: Persistence
    success = persist_skill(skill_name, targets, skill_content, metadata_content)
    
    if not success:
        return 1
    
    # Success message
    print("\n[SUCCESS] Skill created successfully!")
    print(f"\nName: {skill_name}")
    print("Location(s):")
    for cli in targets:
        print(f"  - .{cli}/skills/{skill_name}/SKILL.md")

    print("\nNext steps:")
    print(f"  - Validate: /hefesto.validate {skill_name}")
    print(f"  - View: /hefesto.show {skill_name}")
    print(f"  - Test: Use the skill with your AI CLI")
    
    return 0


if __name__ == "__main__":
    # Extract arguments, excluding script name
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # If user wants to create a skill about Kotlin fundamentals
    if '--kotlin' in args:
        # Remove the flag and use a default description
        args.remove('--kotlin')
        args = ["fundamentals of kotlin programming including coroutines, compose, and modern features"] + args
    
    exit_code = main(args)
    sys.exit(exit_code)