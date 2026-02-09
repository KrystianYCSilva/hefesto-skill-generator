#!/usr/bin/env bash
# Hefesto Skill Generator - Installer
# Compatible with bash 3.2+ (macOS), bash 4+/5+ (Linux), Git Bash (Windows)
# Zero dependencies. Idempotent.

set -euo pipefail

HEFESTO_VERSION="2.2.0"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PAYLOAD_DIR="${SCRIPT_DIR}/payload"

# Colors (disable if not a terminal)
if [ -t 1 ]; then
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  RED='\033[0;31m'
  BLUE='\033[0;34m'
  BOLD='\033[1m'
  NC='\033[0m'
else
  GREEN='' YELLOW='' RED='' BLUE='' BOLD='' NC=''
fi

# ─── Helpers ─────────────────────────────────────────────────────────────────

log_info()  { printf "${GREEN}[install]${NC} %s\n" "$1"; }
log_warn()  { printf "${YELLOW}[warn]${NC} %s\n" "$1"; }
log_error() { printf "${RED}[error]${NC} %s\n" "$1"; }
log_step()  { printf "${BLUE}[step]${NC} %s\n" "$1"; }

# ─── Find Project Root ──────────────────────────────────────────────────────

find_project_root() {
  local dir="$PWD"
  while [ "$dir" != "/" ]; do
    if [ -d "$dir/.git" ]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  # Fallback to current directory
  echo "$PWD"
}

PROJECT_ROOT="$(find_project_root)"

# ─── CLI Detection ───────────────────────────────────────────────────────────

# Arrays for detected CLIs (bash 3.2 compatible - indexed arrays)
DETECTED_CLI_IDS=()
DETECTED_CLI_NAMES=()
DETECTED_CLI_METHODS=()

detect_cli() {
  local cli_id="$1"
  local cli_name="$2"
  local cli_cmd="$3"
  local cli_dir="$4"

  # Check PATH
  if command -v "$cli_cmd" >/dev/null 2>&1; then
    DETECTED_CLI_IDS+=("$cli_id")
    DETECTED_CLI_NAMES+=("$cli_name")
    DETECTED_CLI_METHODS+=("PATH")
    return 0
  fi

  # Check directory
  if [ -d "$PROJECT_ROOT/$cli_dir" ]; then
    DETECTED_CLI_IDS+=("$cli_id")
    DETECTED_CLI_NAMES+=("$cli_name")
    DETECTED_CLI_METHODS+=("directory")
    return 0
  fi

  return 1
}

detect_copilot() {
  # Special detection for Copilot - check multiple signals
  if command -v github-copilot >/dev/null 2>&1; then
    DETECTED_CLI_IDS+=("copilot")
    DETECTED_CLI_NAMES+=("GitHub Copilot")
    DETECTED_CLI_METHODS+=("PATH")
    return 0
  fi

  if [ -f "$PROJECT_ROOT/.github/copilot-instructions.md" ]; then
    DETECTED_CLI_IDS+=("copilot")
    DETECTED_CLI_NAMES+=("GitHub Copilot")
    DETECTED_CLI_METHODS+=("copilot-instructions")
    return 0
  fi

  if [ -d "$PROJECT_ROOT/.github/agents" ]; then
    DETECTED_CLI_IDS+=("copilot")
    DETECTED_CLI_NAMES+=("GitHub Copilot")
    DETECTED_CLI_METHODS+=("agents-dir")
    return 0
  fi

  return 1
}

detect_all_clis() {
  log_step "Detecting installed AI CLIs..."

  detect_cli "claude"   "Claude Code" "claude"   ".claude"   || true
  detect_cli "gemini"   "Gemini CLI"  "gemini"   ".gemini"   || true
  detect_cli "codex"    "OpenAI Codex" "codex"   ".codex"    || true
  detect_copilot || true
  detect_cli "opencode" "OpenCode"    "opencode" ".opencode" || true
  detect_cli "cursor"   "Cursor"      "cursor"   ".cursor"   || true
  detect_cli "qwen"     "Qwen Code"   "qwen"     ".qwen"     || true

  local count=${#DETECTED_CLI_IDS[@]}

  if [ "$count" -eq 0 ]; then
    log_warn "No AI CLIs detected. Creating .claude/ as default."
    DETECTED_CLI_IDS+=("claude")
    DETECTED_CLI_NAMES+=("Claude Code")
    DETECTED_CLI_METHODS+=("default")
  fi

  log_info "Detected ${#DETECTED_CLI_IDS[@]} CLI(s):"
  local i=0
  while [ "$i" -lt "${#DETECTED_CLI_IDS[@]}" ]; do
    printf "  ${GREEN}+${NC} %s (via %s)\n" "${DETECTED_CLI_NAMES[$i]}" "${DETECTED_CLI_METHODS[$i]}"
    i=$((i + 1))
  done
}

# ─── Directory Mapping ───────────────────────────────────────────────────────

get_skills_dir() {
  local cli_id="$1"
  case "$cli_id" in
    claude)   echo ".claude/skills" ;;
    gemini)   echo ".gemini/skills" ;;
    codex)    echo ".codex/skills" ;;
    copilot)  echo ".github/skills" ;;
    opencode) echo ".opencode/skills" ;;
    cursor)   echo ".cursor/skills" ;;
    qwen)     echo ".qwen/skills" ;;
  esac
}

get_commands_dir() {
  local cli_id="$1"
  case "$cli_id" in
    claude)   echo ".claude/commands" ;;
    gemini)   echo ".gemini/commands" ;;
    codex)    echo ".codex/prompts" ;;
    copilot)  echo ".github" ;;
    opencode) echo ".opencode/command" ;;
    cursor)   echo ".cursor/commands" ;;
    qwen)     echo ".qwen/commands" ;;
  esac
}

get_payload_commands_dir() {
  local cli_id="$1"
  case "$cli_id" in
    claude)   echo "commands/claude" ;;
    gemini)   echo "commands/gemini" ;;
    codex)    echo "commands/codex" ;;
    copilot)  echo "commands/github" ;;
    opencode) echo "commands/opencode" ;;
    cursor)   echo "commands/cursor" ;;
    qwen)     echo "commands/qwen" ;;
  esac
}

# ─── Install .hefesto/ ───────────────────────────────────────────────────────

install_hefesto_dir() {
  log_step "Installing .hefesto/ directory..."

  local hefesto_dir="$PROJECT_ROOT/.hefesto"
  mkdir -p "$hefesto_dir/templates"

  # Copy templates
  local templates_src="$PAYLOAD_DIR/hefesto/templates"
  if [ -d "$templates_src" ]; then
    local file
    for file in "$templates_src"/*.md; do
      [ -f "$file" ] || continue
      local basename="$(basename "$file")"
      local dest="$hefesto_dir/templates/$basename"
      if [ -f "$dest" ]; then
        if cmp -s "$file" "$dest"; then
          printf "  ${YELLOW}[skip]${NC} .hefesto/templates/%s (identical)\n" "$basename"
        else
          cp "$file" "$dest"
          printf "  ${BLUE}[update]${NC} .hefesto/templates/%s\n" "$basename"
        fi
      else
        cp "$file" "$dest"
        printf "  ${GREEN}[install]${NC} .hefesto/templates/%s\n" "$basename"
      fi
    done
  fi

  # Write version
  echo "$HEFESTO_VERSION" > "$hefesto_dir/version"
  log_info ".hefesto/version = $HEFESTO_VERSION"
}

# ─── Install Commands ────────────────────────────────────────────────────────

install_commands_for_cli() {
  local cli_id="$1"
  local target_dir="$PROJECT_ROOT/$(get_commands_dir "$cli_id")"
  local source_dir="$PAYLOAD_DIR/$(get_payload_commands_dir "$cli_id")"

  if [ ! -d "$source_dir" ]; then
    log_warn "No payload found for $cli_id, skipping commands"
    return 0
  fi

  # Copilot has nested structure (agents/ + prompts/)
  if [ "$cli_id" = "copilot" ]; then
    install_copilot_commands "$source_dir" "$target_dir"
    return 0
  fi

  mkdir -p "$target_dir"

  local file
  for file in "$source_dir"/hefesto.*; do
    [ -f "$file" ] || continue
    local basename="$(basename "$file")"
    local dest="$target_dir/$basename"

    if [ -f "$dest" ]; then
      if cmp -s "$file" "$dest"; then
        printf "  ${YELLOW}[skip]${NC} %s/%s (identical)\n" "$(get_commands_dir "$cli_id")" "$basename"
      else
        cp "$file" "$dest"
        printf "  ${BLUE}[update]${NC} %s/%s\n" "$(get_commands_dir "$cli_id")" "$basename"
      fi
    else
      cp "$file" "$dest"
      printf "  ${GREEN}[install]${NC} %s/%s\n" "$(get_commands_dir "$cli_id")" "$basename"
    fi
  done
}

install_copilot_commands() {
  local source_dir="$1"
  local target_base="$2"

  # Install agents
  if [ -d "$source_dir/agents" ]; then
    mkdir -p "$target_base/agents"
    local file
    for file in "$source_dir/agents"/hefesto.*; do
      [ -f "$file" ] || continue
      local basename="$(basename "$file")"
      local dest="$target_base/agents/$basename"
      if [ -f "$dest" ]; then
        if cmp -s "$file" "$dest"; then
          printf "  ${YELLOW}[skip]${NC} .github/agents/%s (identical)\n" "$basename"
        else
          cp "$file" "$dest"
          printf "  ${BLUE}[update]${NC} .github/agents/%s\n" "$basename"
        fi
      else
        cp "$file" "$dest"
        printf "  ${GREEN}[install]${NC} .github/agents/%s\n" "$basename"
      fi
    done
  fi

  # Install prompts
  if [ -d "$source_dir/prompts" ]; then
    mkdir -p "$target_base/prompts"
    local file
    for file in "$source_dir/prompts"/hefesto.*; do
      [ -f "$file" ] || continue
      local basename="$(basename "$file")"
      local dest="$target_base/prompts/$basename"
      if [ -f "$dest" ]; then
        if cmp -s "$file" "$dest"; then
          printf "  ${YELLOW}[skip]${NC} .github/prompts/%s (identical)\n" "$basename"
        else
          cp "$file" "$dest"
          printf "  ${BLUE}[update]${NC} .github/prompts/%s\n" "$basename"
        fi
      else
        cp "$file" "$dest"
        printf "  ${GREEN}[install]${NC} .github/prompts/%s\n" "$basename"
      fi
    done
  fi
}

# ─── Install Skills Directories ──────────────────────────────────────────────

install_skills_dirs() {
  log_step "Creating skills directories..."

  local i=0
  while [ "$i" -lt "${#DETECTED_CLI_IDS[@]}" ]; do
    local cli_id="${DETECTED_CLI_IDS[$i]}"
    local skills_dir="$PROJECT_ROOT/$(get_skills_dir "$cli_id")"

    if [ -d "$skills_dir" ]; then
      printf "  ${YELLOW}[exists]${NC} %s\n" "$(get_skills_dir "$cli_id")"
    else
      mkdir -p "$skills_dir"
      printf "  ${GREEN}[create]${NC} %s\n" "$(get_skills_dir "$cli_id")"
    fi
    i=$((i + 1))
  done
}

# ─── Install All Commands ────────────────────────────────────────────────────

install_all_commands() {
  log_step "Installing hefesto commands..."

  local i=0
  while [ "$i" -lt "${#DETECTED_CLI_IDS[@]}" ]; do
    local cli_id="${DETECTED_CLI_IDS[$i]}"
    install_commands_for_cli "$cli_id"
    i=$((i + 1))
  done
}

# ─── Report ──────────────────────────────────────────────────────────────────

print_report() {
  echo ""
  printf "${BOLD}════════════════════════════════════════════════${NC}\n"
  printf "${GREEN}${BOLD}  Hefesto v%s installed successfully!${NC}\n" "$HEFESTO_VERSION"
  printf "${BOLD}════════════════════════════════════════════════${NC}\n"
  echo ""
  printf "  Project: %s\n" "$PROJECT_ROOT"
  printf "  CLIs:    %d detected\n" "${#DETECTED_CLI_IDS[@]}"
  echo ""
  printf "${BOLD}  Installed:${NC}\n"
  printf "    .hefesto/          templates + version\n"

  local i=0
  while [ "$i" -lt "${#DETECTED_CLI_IDS[@]}" ]; do
    local cli_id="${DETECTED_CLI_IDS[$i]}"
    printf "    %-18s commands + skills/\n" "$(get_commands_dir "$cli_id")/"
    i=$((i + 1))
  done

  echo ""
  printf "${BOLD}  Next steps:${NC}\n"
  printf "    1. Run ${GREEN}/hefesto.list${NC} to verify installation\n"
  printf "    2. Run ${GREEN}/hefesto.create \"description\"${NC} to generate your first skill\n"
  printf "    3. Run ${GREEN}/hefesto.validate skill-name${NC} to validate a skill\n"
  echo ""
}

# ─── Main ────────────────────────────────────────────────────────────────────

main() {
  echo ""
  printf "${BOLD}Hefesto Skill Generator v%s - Installer${NC}\n" "$HEFESTO_VERSION"
  echo ""

  # Verify payload exists
  if [ ! -d "$PAYLOAD_DIR" ]; then
    log_error "Payload directory not found: $PAYLOAD_DIR"
    log_error "Please run this script from the installer/ directory."
    exit 1
  fi

  detect_all_clis
  echo ""

  install_hefesto_dir
  echo ""

  install_skills_dirs
  echo ""

  install_all_commands
  echo ""

  print_report
}

main "$@"
