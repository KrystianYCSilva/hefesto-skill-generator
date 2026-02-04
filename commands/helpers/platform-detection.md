---
description: "Cross-platform command abstraction for filesystem and CLI operations on Windows, macOS, and Linux"
category: "helper"
type: "abstraction"
used_by: ["all commands"]
platforms: ["windows", "macos", "linux"]
version: "1.0.0"
---

# Cross-Platform Command Abstraction

**Purpose**: Provide platform-agnostic commands for filesystem and CLI operations  
**Used by**: All `/hefesto.*` commands

---

## Platform Detection

### Detect Current Platform

```markdown
FUNCTION detect_platform():
  IF $Env:OS == "Windows_NT":
    RETURN "windows"
  
  uname_result = Execute("uname -s")
  
  IF uname_result == "Darwin":
    RETURN "macos"
  ELIF uname_result == "Linux":
    RETURN "linux"
  ELSE:
    RETURN "unknown"
```

### Platform-Specific Shell

| Platform | Primary Shell | Fallback |
|----------|--------------|----------|
| Windows | PowerShell 5.1+ | cmd.exe |
| macOS | Zsh (default since Catalina) | Bash |
| Linux | Bash | sh |

---

## Command Abstractions

### 1. Check if Command Exists in PATH

**Purpose**: Detect CLI installation via PATH

| Platform | Command |
|----------|---------|
| Windows | `where.exe {command} 2>$null` |
| Unix/macOS | `command -v {command} > /dev/null 2>&1` |

**Usage**:
```markdown
FUNCTION command_exists(command_name):
  IF platform == "windows":
    result = Execute("where.exe " + command_name + " 2>$null")
    RETURN result.exit_code == 0
  ELSE:
    result = Execute("command -v " + command_name + " > /dev/null 2>&1")
    RETURN result.exit_code == 0
```

**Example**:
```bash
# Windows (PowerShell)
where.exe claude 2>$null
if ($?) { Write-Output "FOUND" }

# Unix/macOS (Bash/Zsh)
if command -v claude > /dev/null 2>&1; then
  echo "FOUND"
fi
```

---

### 2. Get Command Path

**Purpose**: Get full path to CLI executable

| Platform | Command |
|----------|---------|
| Windows | `(Get-Command {command}).Source` |
| Unix/macOS | `which {command}` |

**Usage**:
```markdown
FUNCTION get_command_path(command_name):
  IF platform == "windows":
    result = Execute("(Get-Command " + command_name + ").Source 2>$null")
  ELSE:
    result = Execute("which " + command_name + " 2>/dev/null")
  
  RETURN result.stdout.trim()
```

**Example**:
```bash
# Windows (PowerShell)
(Get-Command claude).Source
# Output: C:\Users\user\AppData\Local\Programs\Claude\claude.exe

# Unix/macOS (Bash/Zsh)
which claude
# Output: /usr/local/bin/claude
```

---

### 3. Create Directory (with Parents)

**Purpose**: Create nested directories idempotently

| Platform | Command |
|----------|---------|
| Windows | `New-Item -ItemType Directory -Force -Path {path}` |
| Unix/macOS | `mkdir -p {path}` |

**Usage**:
```markdown
FUNCTION create_directory(path):
  IF platform == "windows":
    Execute("New-Item -ItemType Directory -Force -Path '" + path + "' | Out-Null")
  ELSE:
    Execute("mkdir -p '" + path + "'")
```

**Example**:
```bash
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path ".claude\skills" | Out-Null

# Unix/macOS (Bash/Zsh)
mkdir -p .claude/skills
```

**Notes**:
- Both commands are idempotent (no error if directory exists)
- `-Force` (Windows) and `-p` (Unix) create parent directories automatically

---

### 4. Check if File Exists

**Purpose**: Verify file presence

| Platform | Command |
|----------|---------|
| Windows | `Test-Path {path}` |
| Unix/macOS | `[ -f {path} ]` |

**Usage**:
```markdown
FUNCTION file_exists(path):
  IF platform == "windows":
    result = Execute("Test-Path '" + path + "'")
    RETURN result.stdout.trim() == "True"
  ELSE:
    result = Execute("[ -f '" + path + "' ]")
    RETURN result.exit_code == 0
```

**Example**:
```bash
# Windows (PowerShell)
if (Test-Path "CONSTITUTION.md") {
  Write-Output "EXISTS"
}

# Unix/macOS (Bash/Zsh)
if [ -f "CONSTITUTION.md" ]; then
  echo "EXISTS"
fi
```

---

### 5. Check if Directory Exists

**Purpose**: Verify directory presence

| Platform | Command |
|----------|---------|
| Windows | `Test-Path -PathType Container {path}` |
| Unix/macOS | `[ -d {path} ]` |

**Usage**:
```markdown
FUNCTION directory_exists(path):
  IF platform == "windows":
    result = Execute("Test-Path -PathType Container '" + path + "'")
    RETURN result.stdout.trim() == "True"
  ELSE:
    result = Execute("[ -d '" + path + "' ]")
    RETURN result.exit_code == 0
```

**Example**:
```bash
# Windows (PowerShell)
if (Test-Path -PathType Container ".claude") {
  Write-Output "EXISTS"
}

# Unix/macOS (Bash/Zsh)
if [ -d ".claude" ]; then
  echo "EXISTS"
fi
```

---

### 6. Get Current Timestamp (ISO 8601)

**Purpose**: Generate timestamps for state persistence

| Platform | Command |
|----------|---------|
| Windows | `Get-Date -Format "o"` |
| Unix/macOS | `date -u +"%Y-%m-%dT%H:%M:%SZ"` |

**Usage**:
```markdown
FUNCTION get_timestamp():
  IF platform == "windows":
    result = Execute("Get-Date -Format 'o'")
  ELSE:
    result = Execute("date -u +'%Y-%m-%dT%H:%M:%SZ'")
  
  RETURN result.stdout.trim()
```

**Example**:
```bash
# Windows (PowerShell)
Get-Date -Format "o"
# Output: 2026-02-04T14:30:00.1234567-08:00

# Unix/macOS (Bash/Zsh)
date -u +"%Y-%m-%dT%H:%M:%SZ"
# Output: 2026-02-04T22:30:00Z
```

**Note**: Windows output includes timezone offset; normalize to UTC if needed

---

### 7. Copy File

**Purpose**: Copy CONSTITUTION.md or other files

| Platform | Command |
|----------|---------|
| Windows | `Copy-Item -Path {source} -Destination {dest} -Force` |
| Unix/macOS | `cp {source} {dest}` |

**Usage**:
```markdown
FUNCTION copy_file(source, destination):
  IF platform == "windows":
    Execute("Copy-Item -Path '" + source + "' -Destination '" + destination + "' -Force")
  ELSE:
    Execute("cp '" + source + "' '" + destination + "'")
```

**Example**:
```bash
# Windows (PowerShell)
Copy-Item -Path "templates\CONSTITUTION.md.bundle" -Destination "CONSTITUTION.md" -Force

# Unix/macOS (Bash/Zsh)
cp templates/CONSTITUTION.md.bundle CONSTITUTION.md
```

---

### 8. Get File Modification Time

**Purpose**: Cache invalidation for CONSTITUTION validation

| Platform | Command |
|----------|---------|
| Windows | `(Get-Item {path}).LastWriteTime.Ticks` |
| Unix/macOS | `stat -c %Y {path}` (Linux) / `stat -f %m {path}` (macOS) |

**Usage**:
```markdown
FUNCTION get_file_mtime(path):
  IF platform == "windows":
    result = Execute("(Get-Item '" + path + "').LastWriteTime.Ticks")
  ELIF platform == "macos":
    result = Execute("stat -f %m '" + path + "'")
  ELIF platform == "linux":
    result = Execute("stat -c %Y '" + path + "'")
  
  RETURN result.stdout.trim()
```

**Example**:
```bash
# Windows (PowerShell)
(Get-Item "CONSTITUTION.md").LastWriteTime.Ticks
# Output: 638437266000000000

# macOS (Bash/Zsh)
stat -f %m CONSTITUTION.md
# Output: 1738696200

# Linux (Bash)
stat -c %Y CONSTITUTION.md
# Output: 1738696200
```

---

### 9. Get Home Directory

**Purpose**: Locate user-specific config directories

| Platform | Variable |
|----------|----------|
| Windows | `$Env:USERPROFILE` |
| Unix/macOS | `$HOME` |

**Usage**:
```markdown
FUNCTION get_home_directory():
  IF platform == "windows":
    RETURN $Env:USERPROFILE
  ELSE:
    RETURN $HOME
```

**Example**:
```bash
# Windows (PowerShell)
$Env:USERPROFILE
# Output: C:\Users\username

# Unix/macOS (Bash/Zsh)
echo $HOME
# Output: /home/username
```

---

### 10. List Directory Contents

**Purpose**: Scan for skill directories

| Platform | Command |
|----------|---------|
| Windows | `Get-ChildItem -Directory -Path {path}` |
| Unix/macOS | `ls -d {path}/*/` |

**Usage**:
```markdown
FUNCTION list_directories(path):
  IF platform == "windows":
    result = Execute("Get-ChildItem -Directory -Path '" + path + "' | Select-Object -ExpandProperty Name")
  ELSE:
    result = Execute("ls -d '" + path + "'/*/ 2>/dev/null | xargs -n1 basename")
  
  RETURN result.stdout.split("\n")
```

**Example**:
```bash
# Windows (PowerShell)
Get-ChildItem -Directory -Path ".claude\skills" | Select-Object -ExpandProperty Name
# Output: code-review
#         api-docs

# Unix/macOS (Bash/Zsh)
ls -d .claude/skills/*/ 2>/dev/null | xargs -n1 basename
# Output: code-review
#         api-docs
```

---

## Path Normalization

### Path Separator

| Platform | Separator | Example |
|----------|-----------|---------|
| Windows | `\` (backslash) | `.claude\skills\` |
| Unix/macOS | `/` (forward slash) | `.claude/skills/` |

**Usage**:
```markdown
FUNCTION normalize_path(path):
  IF platform == "windows":
    RETURN path.replace("/", "\")
  ELSE:
    RETURN path.replace("\", "/")
```

### Relative vs. Absolute Paths

```markdown
FUNCTION get_absolute_path(relative_path):
  IF platform == "windows":
    result = Execute("(Resolve-Path '" + relative_path + "').Path")
  ELSE:
    result = Execute("cd '" + relative_path + "' && pwd")
  
  RETURN result.stdout.trim()
```

---

## Special Platform Considerations

### Windows

**PowerShell Execution Policy**:
```powershell
# May need to set execution policy
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Path Quoting**: Always use single quotes for paths with spaces
```powershell
New-Item -ItemType Directory -Force -Path 'C:\Program Files\My App'
```

**Case Sensitivity**: Filesystem is case-insensitive (C:\ = c:\)

---

### macOS

**Homebrew Paths**: Check `/opt/homebrew/bin` for Apple Silicon Macs
```bash
if [ -f "/opt/homebrew/bin/claude" ]; then
  export PATH="/opt/homebrew/bin:$PATH"
fi
```

**Application Bundles**: CLI tools often in `.app/Contents/MacOS/`
```bash
# Cursor example
/Applications/Cursor.app/Contents/MacOS/cursor
```

**Case Sensitivity**: Filesystem typically case-insensitive (default APFS)

---

### Linux

**Distribution Variations**:
- Debian/Ubuntu: CLIs in `/usr/bin` or `/usr/local/bin`
- Arch/Manjaro: CLIs in `/usr/bin`
- Fedora/RHEL: CLIs in `/usr/bin` or `/usr/local/bin`

**Snap/Flatpak**: Check `/snap/bin` or `/var/lib/flatpak/exports/bin`

**Case Sensitivity**: Filesystem is case-sensitive

---

## Error Handling

### Command Not Found

```markdown
FUNCTION safe_execute(command):
  TRY:
    result = Execute(command)
    RETURN result
  CATCH CommandNotFound:
    LOG("Command not found: " + command)
    RETURN {exit_code: 127, stdout: "", stderr: "Command not found"}
```

### Permission Denied

```markdown
FUNCTION safe_create_directory(path):
  TRY:
    create_directory(path)
    RETURN success
  CATCH PermissionError:
    LOG("Permission denied: " + path)
    RETURN error
```

---

## Testing

### Test Platform Detection

```bash
# Should output current platform
detect_platform()
# Expected: "windows", "macos", or "linux"
```

### Test Command Existence

```bash
# Should return true for existing command
command_exists("ls")  # Unix/macOS
command_exists("dir") # Windows

# Should return false for non-existent command
command_exists("nonexistent-cli-12345")
```

### Test Directory Creation

```bash
# Should create directory idempotently
create_directory(".test-hefesto/skills")
create_directory(".test-hefesto/skills")  # Second call should succeed
```

---

## References

- Research: Cross-Platform Compatibility (research.md #6)
- FR-007: Offline operation support
- SC-003: 95%+ success rate across platforms
- Assumptions: Windows, macOS, or Linux operating systems
