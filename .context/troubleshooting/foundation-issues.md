---
description: "Comprehensive troubleshooting guide for common Hefesto Foundation Infrastructure issues"
category: "documentation"
type: "troubleshooting"
audience: "users"
last_updated: "2026-02-04"
version: "1.0.0"
---

# Troubleshooting: Hefesto Foundation Issues

**Audience**: Users experiencing issues with Hefesto Foundation Infrastructure  
**Last Updated**: 2026-02-04

---

## Quick Diagnostics

Run these commands to diagnose issues:

```bash
# 1. Check if Hefesto initialized
/hefesto.list

# 2. Check CLI detection
/hefesto.detect

# 3. Check filesystem consistency
/hefesto.list --check-sync

# 4. Get help
/hefesto.help
```

---

## Common Issues

### Issue 1: "Hefesto not initialized"

**Symptoms**:
- Error when running `/hefesto.list` or `/hefesto.detect`
- No MEMORY.md file in project root

**Cause**: Hefesto hasn't been initialized in this project

**Solution**:
```bash
# Run initialization
/hefesto.init

# Verify
/hefesto.list
```

**Prevention**: Always run `/hefesto.init` first in new projects

---

### Issue 2: "No CLIs detected"

**Symptoms**:
- `/hefesto.init` reports 0 CLIs found
- Prompted for manual specification

**Cause**: No AI CLIs installed or not in PATH

**Diagnosis**:
```bash
# Check if CLI installed (Unix/macOS)
which claude
which gemini
which opencode

# Windows
where.exe claude
```

**Solution**:
```bash
# Option 1: Install an AI CLI
# (Follow CLI-specific installation instructions)

# Option 2: Add CLI to PATH
export PATH=$PATH:/path/to/cli  # Unix/macOS
# Or edit system PATH on Windows

# Option 3: Use manual specification
# When prompted during /hefesto.init, select CLI number
```

**Prevention**: Install at least one AI CLI before running Hefesto

---

### Issue 3: Permission Denied Errors

**Symptoms**:
- `❌ Permission denied: .{cli}/skills/`
- Cannot create directories
- Partial bootstrap success

**Cause**: Insufficient permissions to create directories

**Diagnosis**:
```bash
# Check directory permissions
ls -la .
ls -la .claude/ 2>/dev/null

# Check if directory writable
touch .test && rm .test
```

**Solution**:
```bash
# Option 1: Fix permissions
chmod +w .  # Current directory
chmod +w .claude/  # Specific CLI directory

# Option 2: Manually create directories
mkdir -p .claude/skills
mkdir -p .gemini/skills
chmod +w .claude/skills .gemini/skills

# Option 3: Run with appropriate privileges (use carefully)
sudo /hefesto.init  # Unix/macOS only
```

**Prevention**: Ensure write permissions before running Hefesto

---

### Issue 4: Corrupted MEMORY.md

**Symptoms**:
- `⚠️ State Recovery: MEMORY.md corrupted`
- Backup file created: `MEMORY.md.backup.{timestamp}`
- State rebuilt from filesystem

**Cause**: Manual editing or filesystem corruption

**What Hefesto Does**:
1. Automatically backs up corrupted file
2. Creates fresh MEMORY.md
3. Rescans filesystem to rebuild state
4. Continues operation

**Manual Intervention** (if needed):
```bash
# Review backup
cat MEMORY.md.backup.2026-02-04T16-00-00Z

# If recovery failed, restore backup and fix manually
mv MEMORY.md.backup.2026-02-04T16-00-00Z MEMORY.md
# Edit MEMORY.md to fix syntax errors

# Or delete and re-initialize
rm MEMORY.md
/hefesto.init
```

**Prevention**: Never manually edit MEMORY.md

---

### Issue 5: Missing CONSTITUTION.md

**Symptoms**:
- `⚠️ Governance Recovery: CONSTITUTION.md missing`
- File auto-restored from bundle

**Cause**: CONSTITUTION.md deleted or missing from project

**What Hefesto Does**:
1. Automatically restores from bundled copy
2. Validates restored file
3. Continues operation

**Manual Intervention** (if customizations lost):
```bash
# Restore from version control
git restore CONSTITUTION.md

# Or manually restore specific version
git show HEAD:CONSTITUTION.md > CONSTITUTION.md
```

**Prevention**: Don't delete CONSTITUTION.md; keep in version control

---

### Issue 6: Constitutional Violations

**Symptoms**:
- `❌ Constitutional Violation: T0 rules missing or invalid`
- All operations blocked
- Missing T0 rules listed

**Cause**: CONSTITUTION.md manually modified or corrupted

**Solution**:
```bash
# Option 1: Restore from version control
git restore CONSTITUTION.md

# Option 2: Force restore from bundle
/hefesto.restore-constitution --force

# Option 3: Check diff and fix manually
git diff CONSTITUTION.md
# Fix any removed or modified T0 rules

# Verify fix worked
/hefesto.list
```

**Prevention**: Don't manually edit CONSTITUTION.md; treat as read-only

---

### Issue 7: CLI Detected but Not in PATH

**Symptoms**:
- `⚠️ Config found but not in PATH`
- Warning (non-blocking)
- Skills may not work

**Cause**: CLI config directory exists but executable not in PATH

**Diagnosis**:
```bash
# Check config exists
ls -la ~/.claude/  # or appropriate config dir

# Check PATH
echo $PATH | grep claude  # Should show nothing
which claude  # Should return nothing
```

**Solution**:
```bash
# Option 1: Reinstall CLI properly
# (Follow CLI installation instructions)

# Option 2: Add CLI to PATH
export PATH=$PATH:/path/to/cli/bin
# Add to ~/.bashrc or ~/.zshrc for persistence

# Verify
which claude  # Should now show path

# Update Hefesto
/hefesto.detect
```

**Prevention**: Install CLIs properly with PATH configuration

---

### Issue 8: Filesystem Inconsistencies

**Symptoms**:
- `⚠️ Filesystem inconsistencies detected`
- Orphaned or missing skills reported

**Cause**: Manual file operations or failed operations

**Diagnosis**:
```bash
# Run sync check
/hefesto.list --check-sync
```

**Solution**:
```bash
# For orphaned skills (in filesystem, not tracked):
# Option 1: Keep skill - manually add to MEMORY.md
# Option 2: Remove skill
rm -rf .claude/skills/orphaned-skill/

# For missing skills (tracked but not in filesystem):
# Option 1: Regenerate skill
/hefesto.create  # Future command

# Option 2: Remove from tracking
# Edit MEMORY.md and remove skill entry (careful!)

# Option 3: Wait for /hefesto.sync command (future)

# Verify fix
/hefesto.list --check-sync
```

**Prevention**: Use Hefesto commands instead of manual file operations

---

### Issue 9: Already Initialized

**Symptoms**:
- `ℹ️ Hefesto already initialized`
- `/hefesto.init` exits without doing anything

**Cause**: MEMORY.md already exists (expected behavior)

**Solution**:
```bash
# If you want to re-initialize
/hefesto.init --force

# Or just list current state
/hefesto.list
```

**Note**: This is not an error - idempotency working correctly

---

### Issue 10: Slow Performance

**Symptoms**:
- Bootstrap takes > 10 seconds
- Detection takes > 5 seconds
- Listing takes > 500ms

**Diagnosis**:
```bash
# Run with verbose timing (future enhancement)
/hefesto.init --verbose

# Check system resources
# Unix/macOS
time /hefesto.init
df -h .

# Windows
Measure-Command { /hefesto.init }
```

**Common Causes**:
- Slow filesystem (network drives)
- Many CLIs to check
- Large number of existing skills
- Disk I/O contention

**Solution**:
```bash
# Option 1: Use local filesystem (not network drive)
# Move project to local disk

# Option 2: Reduce CLI checks
# Install only needed CLIs

# Option 3: Check disk health
# Verify no disk errors or fragmentation
```

**Expected Performance**:
- Bootstrap: 2-4 seconds
- Detection: 1-2 seconds
- Listing: 40-70ms

---

## Platform-Specific Issues

### Windows Issues

**Issue**: PowerShell execution policy

**Error**: `Scripts disabled on this system`

**Solution**:
```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for current session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Or for current user
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

**Issue**: Path separators

**Symptoms**: Paths shown with forward slashes on Windows

**Note**: This is expected - Hefesto normalizes to forward slashes internally

---

### macOS Issues

**Issue**: CLI installed via Homebrew not detected

**Diagnosis**:
```bash
# Check Homebrew path
which brew

# Check if CLI in Homebrew
ls /opt/homebrew/bin/ | grep claude
ls /usr/local/bin/ | grep claude
```

**Solution**:
```bash
# Add Homebrew to PATH (if not already)
export PATH="/opt/homebrew/bin:$PATH"  # Apple Silicon
export PATH="/usr/local/bin:$PATH"     # Intel

# Add to ~/.zshrc for persistence
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc

# Verify
which claude

# Re-detect
/hefesto.detect
```

---

### Linux Issues

**Issue**: Snap or Flatpak CLI not detected

**Diagnosis**:
```bash
# Check snap binaries
ls /snap/bin/

# Check flatpak
flatpak list
```

**Solution**:
```bash
# Add snap to PATH
export PATH="/snap/bin:$PATH"

# Or create symlink
sudo ln -s /snap/bin/claude /usr/local/bin/claude

# Verify
which claude

# Re-detect
/hefesto.detect
```

---

## Advanced Troubleshooting

### Enable Debug Mode (Future)

```bash
# Export debug flag
export HEFESTO_DEBUG=1

# Run command
/hefesto.init

# Check logs
cat .hefesto/debug.log
```

### Check File Integrity

```bash
# Verify CONSTITUTION.md
cat CONSTITUTION.md | head -20

# Verify MEMORY.md
cat MEMORY.md

# Check for required sections
grep "T0-HEFESTO-" CONSTITUTION.md  # Should show 11 rules
grep "## Detected CLIs" MEMORY.md
```

### Manual State Reset

**Warning**: This deletes all Hefesto state

```bash
# Backup first
cp MEMORY.md MEMORY.md.manual-backup
cp CONSTITUTION.md CONSTITUTION.md.manual-backup

# Remove state
rm MEMORY.md

# Remove CLI directories (careful!)
rm -rf .claude/ .gemini/ .opencode/ .cursor/ .codex/ .github/ .qwen/

# Re-initialize
/hefesto.init
```

---

## Getting Help

### Information to Provide

When reporting issues, include:

1. Error message (full text)
2. Command that failed
3. Operating system and version
4. Hefesto version: Check `MEMORY.md` frontmatter
5. Installed CLIs: `which claude gemini opencode`
6. File permissions: `ls -la .`
7. Disk space: `df -h .`

### Diagnostic Report (Future)

```bash
# Generate diagnostic report
/hefesto.diagnose > hefesto-diagnostic.txt

# Share report when asking for help
```

---

## Prevention Best Practices

1. **Always initialize first**: Run `/hefesto.init` in new projects
2. **Don't edit state files**: Use commands, never manual edits
3. **Use version control**: Track MEMORY.md and CONSTITUTION.md
4. **Check permissions**: Ensure write access before running
5. **Install CLIs properly**: Add to PATH, verify with `which`
6. **Keep disk space**: Maintain at least 100MB free
7. **Read error messages**: They contain resolution steps
8. **Use --force carefully**: Only when you understand the impact

---

## References

- **Error Codes**: commands/helpers/error-codes.md
- **Commands**: commands/*.md
- **Help**: `/hefesto.help`
- **AGENTS.md**: Complete documentation
