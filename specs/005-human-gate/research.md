# Research: Human Gate + Wizard Mode

**Feature**: 005-human-gate  
**Date**: 2026-02-05  
**Status**: Complete  
**Dependencies**: **ZERO external libraries** - Pure Python 3.13 stdlib only

---

## Executive Summary

All six research areas resolved with stdlib-only solutions. No external dependencies required. All solutions cross-platform compatible (Windows PowerShell, macOS/Linux Bash).

**Key Decisions**:
1. `input()` + `signal.alarm()` / `threading.Timer()` for wizard with timeout
2. ANSI escape codes with auto-detection for preview formatting
3. `pathlib` + `tarfile` + exception handling for atomic backups
4. Regex-based markdown parsing for section diffs (simpler than markdown-it)
5. `subprocess.run()` + `$EDITOR` for editor integration
6. Custom validation functions + allowlist approach for security

---

## 1. Interactive Terminal Input

### Decision: **stdlib `input()` + `signal.alarm()` (Unix) / `threading.Timer()` (Windows)**

### Rationale

- **FR-010**: Wizard collects inputs step-by-step
- **FR-012**: Support `back` command
- **FR-005**: 5-minute timeout
- **Zero dependencies**: `input()` + `signal`/`threading` are stdlib
- **Cross-platform**: signal.alarm() on Unix, threading.Timer() fallback on Windows

### Alternatives Considered

- **prompt_toolkit**: Rich features but heavy dependency
- **inquirer**: CLI forms library but another dependency  
- **Verdict**: Stdlib sufficient for simple step-by-step prompts

---

## 2. Preview Formatting

### Decision: **ANSI escape codes with auto-detection fallback**

### Rationale

- **FR-003**: Formatted preview with file paths, contents, sizes
- **Assumption #1**: ANSI colors supported (fallback to plain text)
- **Zero dependencies**: Raw ANSI escape codes
- **Cross-platform**: Windows 10+ and all Unix terminals support ANSI

### Alternatives Considered

- **colorama**: Popular ANSI library, but adds dependency
- **rich**: Beautiful formatting, but heavy and complex
- **Verdict**: Raw ANSI codes sufficient for simple formatting

---

## 3. Collision Detection & Atomic Backups

### Decision: **`pathlib` + `tarfile` + exception handling for rollback**

### Rationale

- **FR-023**: Create backup at `.hefesto/backups/{skill-name}-{timestamp}.tar.gz`
- **FR-006**: Atomic persistence (all files succeed or all fail)
- **Edge Case #4**: Atomic rollback if multi-CLI write fails
- **Zero dependencies**: `pathlib` + `tarfile` are stdlib

### Alternatives Considered

- **tempfile + rename**: Atomic single-file writes, but doesn't handle multi-file/multi-dir
- **Transaction libraries**: Overkill for filesystem operations
- **Verdict**: Manual exception handling + backup/restore sufficient

---

## 4. Section-by-Section Diff

### Decision: **Regex-based markdown parsing (stdlib only)**

### Rationale

- **FR-024 (Clarified)**: Section-by-section approval (Option C)
- **Agent Skills structure**: Predictable (frontmatter + markdown sections)
- **Zero dependencies**: `re` module for regex
- **Simple**: No need for full AST parsing

### Alternatives Considered

- **markdown-it-py**: Full markdown parser, but adds dependency
- **commonmark**: Spec-compliant parser, but unnecessary
- **Verdict**: Simple regex sufficient for Agent Skills' predictable structure

---

## 5. Editor Integration

### Decision: **`subprocess.run()` + `$EDITOR` with platform fallbacks**

### Rationale

- **FR-027**: Open skill content in user's default editor
- **Assumption #2**: $EDITOR set or system default available
- **Zero dependencies**: `subprocess` + `tempfile` are stdlib
- **Cross-platform**: Works on Windows (notepad), Linux/macOS (vim/nano)

### Alternatives Considered

- **click.edit()**: Handles editor detection, but requires Click framework
- **editor package**: Wraps subprocess, adds no value
- **Verdict**: Stdlib subprocess sufficient

---

## 6. Input Sanitization

### Decision: **Custom validation functions + allowlist approach**

### Rationale

- **T0-HEFESTO-11**: Validate against injection patterns
- **FR-031**: Sanitize shell, prompt, SQL injection
- **ADR-002**: "Prompt Injection Attacks on Agentic Coding Assistants"
- **Zero dependencies**: Pure Python regex + `shlex.quote()`
- **Allowlist > Blocklist**: Define what's allowed (safer)

### Alternatives Considered

- **bleach**: HTML sanitization, wrong domain
- **pyparsing**: Grammar validation, overkill
- **Verdict**: Custom validation sufficient and safer (no dependencies)

---

## Testing Strategy

### Unit Tests (pytest)

- `test_wizard.py`: Wizard step navigation, back command, timeout
- `test_preview.py`: ANSI detection, truncation logic, formatting
- `test_collision.py`: Backup creation, atomic writes, rollback
- `test_sanitizer.py`: Injection detection, name sanitization, allowlist validation

### Integration Tests

- Full wizard flow end-to-end (name → description → approve)
- Human Gate with all 4 options ([approve], [expand], [edit], [reject])
- Multi-CLI atomic write + rollback
- Collision detection + merge section-by-section

### Cross-Platform Tests

- Windows: PowerShell + notepad.exe editor
- Linux: Bash + vim editor
- Timeout behavior on both platforms (signal.alarm vs threading.Timer)

### Security Tests

- Fuzz inputs with injection patterns (100+ test cases)
- Path traversal attempts (../, ..\\)
- Shell injection attempts (`;`, `|`, `&&`)
- Prompt injection attempts (ignore instructions, show prompt)

---

## Summary & Recommendations

**External Dependencies**: **ZERO**  
**Stdlib-Only**: All 6 research areas resolved with Python 3.13 standard library

**Implementation Priority**:
1. Input sanitization (security first)
2. Preview formatting (user visibility)
3. Atomic backups (data safety)
4. Wizard input (user experience)
5. Section diff (merge functionality)
6. Editor integration (advanced feature)

**Next Phase**: Data model design (entities, state machines, contracts)

---

**Research Status**: ✅ COMPLETE  
**Next Gate**: Human Gate approval before Phase 1 (data model + contracts)
