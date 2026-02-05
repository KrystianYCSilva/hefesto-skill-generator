# /hefesto.create - Phase Handlers (P0-P6)

> **Component:** Phase execution handlers for `/hefesto.create`
> **Memory System:** CoALA circular buffer + sliding windows
> **Version:** 1.0.0
> **Integration:** hefesto.create-coala-memory.md

---

## Handler Pattern

Each phase follows this pattern:

```
handle_phase_N(memory: CoALAMemory) → Result<PhaseOutcome, Error>
  
  1. Retrieve state from prior phase
  2. Perform phase-specific logic
  3. Validate invariants
  4. Push state to memory (CHECKPOINT-N)
  5. Return outcome (continue|error|human_gate_required)
```

---

## PHASE 0: Pre-Execution Validation

**Input**: Command invocation  
**Output**: Validated execution context  
**Checkpoint**: CHECKPOINT-0

```markdown
handle_phase_0_preexecution(args: CommandArgs) → Result<(), Error>
  
  1. VALIDATE CONSTITUTION.MD
     ├─ File exists: C:/.../CONSTITUTION.md
     ├─ Is valid YAML
     ├─ Contains all 11 T0 rules (T0-HEFESTO-01 .. T0-HEFESTO-11)
     └─ ABORT if invalid
         ERROR E-CREATE-000: "CONSTITUTION.md invalid"
  
  2. VALIDATE MEMORY.MD
     ├─ File exists
     ├─ Is valid YAML
     ├─ Contains skills_created, cli_detected sections
     └─ ABORT if not found
         ERROR E-CREATE-000: "Run /hefesto.init first"
  
  3. LOAD CONTEXT
     ├─ Load CONSTITUTION.md → standards
     ├─ Load .context/standards/architectural-rules.md → T0 rules
     ├─ Load .context/_meta/key-decisions.md → ADRs
     ├─ Load MEMORY.md → cli_detected, skills_created
     └─ Store in memory.window_input[meta_context]
  
  4. PUSH CHECKPOINT-0
     memory.push_state(PHASE-0, {
       context_loaded: true,
       constitution_valid: true,
       memory_valid: true,
       t0_rules_count: 11,
       detected_clis: [claude, gemini, ...],
       loaded_at: now(),
       execution_start: true
     })
     
  RETURN Ok(())
  
  PERFORMANCE TARGET: < 500ms
```

**Error Cases**:
- E-CREATE-000: CONSTITUTION/MEMORY invalid
- FileNotFoundError: Missing .context/ files

---

## PHASE 1: Argument Parsing & Wizard Mode

**Input**: Command arguments  
**Output**: Parsed description + target CLIs  
**Checkpoint**: CHECKPOINT-1

```markdown
handle_phase_1_parsing(memory: CoALAMemory, user_input: String) 
  → Result<ParsedInput, Error>
  
  1. PARSE ARGUMENTS
     ├─ Extract positional[0] → description (optional)
     ├─ Extract --target <cli> flag (optional)
     ├─ Extract --template <name> flag (optional, default: "base")
     ├─ Validate no unknown flags
     └─ Store in window_input
  
  2. CHECK WIZARD MODE NEEDED
     IF description IS null OR description.trim().empty():
       CALL trigger_wizard_mode(memory)
       RETURN parsed_input
  
  3. VALIDATE INPUT (if not wizard)
     ├─ Check length(description) ≤ 2000 chars
     │  └─ ERROR E-CREATE-001: "Description > 2000 chars"
     ├─ Check NOT empty
     │  └─ ERROR E-CREATE-007: "Empty description"
     ├─ Check no injection patterns
     │  ├─ Pattern: "'; DROP TABLE"
     │  ├─ Pattern: "${" (shell injection)
     │  └─ Pattern: "`" (backtick injection)
     └─ ERROR E-CREATE-????  (T0-HEFESTO-11 violation)
  
  4. VALIDATE --target FLAG (if provided)
     ├─ Retrieve detected_clis from PHASE-0
     ├─ FOR EACH cli IN --target list:
     │  └─ Check cli IN detected_clis
     │     └─ ERROR E-CREATE-004: "CLI not detected: {cli}"
     └─ Store target_cli
  
  5. PUSH CHECKPOINT-1
     memory.push_state(PHASE-1, {
       description: description,
       target_cli: target_cli,
       template_name: template_name,
       raw_input_hash: hash(user_input),
       input_valid: true,
       input_errors: [],
       parsed_at: now(),
       wizard_mode_used: false
     })
  
  RETURN Ok(ParsedInput {
    description,
    target_cli,
    template_name
  })
  
  PERFORMANCE TARGET: < 100ms
```

**Wizard Mode Handler**:

```markdown
trigger_wizard_mode(memory: CoALAMemory) → Result<ParsedInput, Error>
  
  DISPLAY: "🧙 Wizard Mode: Create Skill"
  
  STEP 1: GET DESCRIPTION
    LOOP (max 3 attempts):
      PROMPT: "What should this skill do? (1-2 sentences, max 2000 chars)"
      INPUT: user_description
      
      IF empty OR length > 2000:
        DISPLAY: "❌ Invalid (too long or empty)"
        CONTINUE
      
      description = user_description
      BREAK
    
    IF max attempts reached:
      ERROR E-CREATE-007: "Could not get description"
  
  STEP 2: CONFIRM SKILL NAME
    skill_name = auto_generate_name(description)
    skill_name = sanitize_name(skill_name)  // T0-HEFESTO-07
    
    DISPLAY: "Suggested name: {skill_name}"
    PROMPT: "Press Enter to accept, or type custom name:"
    INPUT: custom_name OR [Enter]
    
    IF custom_name provided:
      skill_name = sanitize_name(custom_name)
  
  STEP 3: SELECT TARGET CLIs
    detected_clis = memory.get_state(PHASE-0).detected_clis
    
    DISPLAY: "Detected CLIs: {detected_clis.join(', ')}"
    PROMPT: "Target CLIs (comma-separated or 'all') [all]:"
    INPUT: target_selection
    
    IF target_selection.lower() == "all":
      target_cli = detected_clis
    ELSE:
      target_cli = target_selection.split(',').map(str::trim)
      // Validate each CLI
  
  STEP 4: PREVIEW & CONFIRM
    DISPLAY: |-
      ───────────────────────────────────
      Name: {skill_name}
      Description: {description}
      Target CLIs: {target_cli}
      ───────────────────────────────────
    
    PROMPT: "[continue] [edit] [cancel]"
    INPUT: action
    
    CASE action:
      "continue" → RETURN Ok(...)
      "edit"     → GOTO STEP 1
      "cancel"   → ERROR E-CREATE-????: "Cancelled"
  
  RETURN Ok(ParsedInput {...})
  
  TIMEOUT: 300 seconds of inactivity → ERROR
```

---

## PHASE 2: Skill Generation

**Input**: Parsed description + template name  
**Output**: Generated SKILL.md + metadata.yaml  
**Checkpoint**: CHECKPOINT-2

```markdown
handle_phase_2_generation(memory: CoALAMemory) 
  → Result<GeneratedSkill, Error>
  
  1. RETRIEVE PARSED INPUT
     parsed = memory.get_state(PHASE-1)
     description = parsed.description
     template_name = parsed.template_name
     target_cli = parsed.target_cli
  
  2. LOAD TEMPLATE
     template_path = "./commands/templates/{template_name}/SKILL.md.template"
     
     TRY:
       template_content = read_file(template_path)
       template_metadata = yaml_frontmatter(template_content)
     CATCH FileNotFoundError:
       ERROR E-CREATE-008: "Template not found: {template_name}"
  
  3. GENERATE SKILL NAME
     // Check if wizard already provided name
     IF parsed.custom_name provided:
       skill_name = parsed.custom_name
     ELSE:
       skill_name = infer_name_from_description(description)
     
     // Sanitize per T0-HEFESTO-07
     skill_name = sanitize_skill_name(skill_name)
     
     // Validate format
     IF NOT valid_skill_name(skill_name):
       ERROR E-CREATE-002: "Invalid skill name generated"
  
  4. INFER SKILL METADATA
     category = infer_category(description)
       CASES:
         "test" OR "jest" OR "pytest" → "testing"
         "lint" OR "format" → "development"
         "deploy" OR "lambda" → "devops"
         "review" OR "pr" → "review"
         DEFAULT: "development"
     
     tags = infer_tags(description)
       // Extract keywords: regex, email, validation, etc.
  
  5. RENDER TEMPLATE
     context = {
       name: skill_name,
       description: description,
       category: category,
       tags: tags,
       created: now(),
       version: "1.0.0",
       license: "MIT",
       author: infer_author_from_git() OR "Developer",
       cli: target_cli  // For CLI-specific variations
     }
     
     skill_content = template.render(context)
     
     // Validate content not empty
     IF skill_content.length == 0:
       ERROR E-CREATE-008: "Template rendering failed"
  
  6. GENERATE METADATA.YAML
     metadata = {
       name: skill_name,
       version: "1.0.0",
       description: description,
       created: now(),
       author: context.author,
       category: category,
       tags: tags,
       license: "MIT",
       template_version: template_metadata.version,
       template_used: template_name
     }
  
  7. PUSH CHECKPOINT-2
     memory.push_state(PHASE-2, {
       skill_name: skill_name,
       skill_content: skill_content,
       metadata: metadata,
       template_used: template_name,
       category_inferred: category,
       tags_inferred: tags,
       generated_at: now()
     })
  
  RETURN Ok(GeneratedSkill {
    skill_name,
    skill_content,
    metadata
  })
  
  PERFORMANCE TARGET: < 5s
```

**Helper Functions**:

```markdown
sanitize_skill_name(name: String) → String
  // T0-HEFESTO-07 compliance
  
  name = name.lower()
  name = name.replace(r"[^a-z0-9\-]", "-")  // Only a-z, 0-9, -
  name = name.replace(r"\-{2,}", "-")  // No consecutive hyphens
  name = name.trim_matches('-')  // No leading/trailing hyphens
  
  IF name.length > 64:
    name = name[0..64]
  
  RETURN name

infer_category(desc: String) → String
  // Extract keywords and map to categories
  
  desc_lower = desc.lower()
  
  IF contains(desc_lower, ["test", "pytest", "jest", "mocha"]):
    RETURN "testing"
  
  ELSE IF contains(desc_lower, ["deploy", "docker", "k8s", "lambda"]):
    RETURN "devops"
  
  ELSE IF contains(desc_lower, ["lint", "format", "prettier"]):
    RETURN "development"
  
  ELSE IF contains(desc_lower, ["review", "pr", "merge"]):
    RETURN "review"
  
  ELSE IF contains(desc_lower, ["doc", "readme", "guide"]):
    RETURN "documentation"
  
  ELSE:
    RETURN "development"
```

---

## PHASE 3: Validation

**Input**: Generated skill + metadata  
**Output**: Validation report  
**Checkpoint**: CHECKPOINT-3

```markdown
handle_phase_3_validation(memory: CoALAMemory) 
  → Result<ValidationResult, Error>
  
  1. RETRIEVE GENERATED SKILL
     skill = memory.get_state(PHASE-2)
     skill_name = skill.skill_name
     skill_content = skill.skill_content
     metadata = skill.metadata
  
  2. VALIDATE AGAINST T0 RULES
     errors = Vec::new()
     
     // T0-HEFESTO-01: Agent Skills Spec
     ├─ Check frontmatter exists
     ├─ Check `name` field exists
     ├─ Check `description` field exists
     └─ ABORT if missing (E-CREATE-005)
     
     // T0-HEFESTO-07: Nomenclature
     ├─ Check skill_name.matches(/^[a-z0-9]+(-[a-z0-9]+)*$/)
     ├─ Check length(skill_name) ≤ 64
     └─ ERROR if invalid (E-CREATE-002)
     
     // T0-HEFESTO-03: Progressive Disclosure
     ├─ Count lines in skill_content
     ├─ Check lines < 500
     └─ ERROR if > 500 (E-CREATE-005)
     
     // T0-HEFESTO-11: Security
     ├─ Scan for secrets:
     │  ├─ Pattern: /aws_access_key/i
     │  ├─ Pattern: /api[_-]?key/i
     │  ├─ Pattern: /password/i
     │  ├─ Pattern: /token/i
     │  └─ Pattern: /secret/i
     └─ ERROR if found (E-CREATE-005)
  
  3. CHECK METADATA VALIDITY
     ├─ description NOT empty
     ├─ length(description) ≤ 1024 chars
     ├─ author field present
     ├─ license field present
     └─ ERROR if invalid
  
  4. DECIDE OUTCOME
     validation_passed = errors.is_empty()
     
     IF NOT validation_passed:
       // Do NOT proceed to Human Gate
       
       DISPLAY: "❌ Validation Failed:"
       FOR error IN errors:
         DISPLAY: "  - {error.code}: {error.message}"
         DISPLAY: "    Fix: {error.remediation}"
       
       memory.push_state(PHASE-3, {
         validation_passed: false,
         validation_errors: errors,
         validation_timestamp: now()
       })
       
       ERROR E-CREATE-005: "Template validation failed"
  
  5. PUSH CHECKPOINT-3 (SUCCESS)
     memory.push_state(PHASE-3, {
       validation_passed: true,
       validation_errors: [],
       checked_rules: [
         "T0-HEFESTO-01: ✓ Agent Skills spec",
         "T0-HEFESTO-07: ✓ Name format",
         "T0-HEFESTO-03: ✓ Line count",
         "T0-HEFESTO-11: ✓ No secrets"
       ],
       validation_timestamp: now()
     })
  
  RETURN Ok(ValidationResult {
    passed: true,
    errors: []
  })
  
  PERFORMANCE TARGET: < 500ms
```

---

## PHASE 4: Human Gate & Collision

**Input**: Validated skill  
**Output**: Human approval + collision resolution  
**Checkpoint**: CHECKPOINT-4

**Timeout**: 120 seconds for response

```markdown
handle_phase_4_human_gate(memory: CoALAMemory) 
  → Result<HumanGateDecision, Error>
  
  1. RETRIEVE SKILL STATE
     skill = memory.get_state(PHASE-2)
     validation = memory.get_state(PHASE-3)
     target_clis = memory.get_state(PHASE-1).target_cli
  
  2. CHECK FOR COLLISION
     collision_detected = false
     
     FOR cli IN target_clis:
       skill_path = ".{cli}/skills/{skill_name}/"
       IF file_exists(skill_path):
         collision_detected = true
         existing_metadata = load_metadata(skill_path)
         BREAK
  
  3. DISPLAY SKILL PREVIEW
     DISPLAY: "═══════════════════════════════════════════════════"
     DISPLAY: "✅ Skill Generated: {skill_name}"
     DISPLAY: "═══════════════════════════════════════════════════"
     DISPLAY: ""
     DISPLAY: "Preview:"
     DISPLAY: "-----------------------------------------"
     
     // Show frontmatter
     DISPLAY: "name: {skill_name}"
     DISPLAY: "description: {metadata.description}"
     DISPLAY: "version: {metadata.version}"
     DISPLAY: "created: {metadata.created}"
     DISPLAY: "target_clis: {target_clis.join(', ')}"
     
     DISPLAY: "-----------------------------------------"
     
     // Show first 20 lines of content
     lines = skill_content.split('\n')[0..20]
     FOR line IN lines:
       DISPLAY: line
     
     DISPLAY: "..."
     DISPLAY: "-----------------------------------------"
     DISPLAY: ""
     DISPLAY: "Validation: PASS ✅"
     DISPLAY: ""
     
     // Show files to be created
     DISPLAY: "Files to create:"
     FOR cli IN target_clis:
       DISPLAY: "  - .{cli}/skills/{skill_name}/SKILL.md"
       DISPLAY: "  - .{cli}/skills/{skill_name}/metadata.yaml"
     
     DISPLAY: "═══════════════════════════════════════════════════"
  
  4. COLLISION PATH (if detected)
     IF collision_detected:
       CALL handle_collision_gate(memory, existing_metadata)
       // This function prompts user and returns action
  
  5. PROMPT FOR APPROVAL
     IF NOT collision_detected:
       PROMPT: "Actions: [approve] [expand] [edit] [reject]"
     
     INPUT: action (with 120s timeout)
     
     CASE action:
       "approve":
         memory.push_state(PHASE-4, {
           collision_detected: false,
           human_gate_response: "approve",
           human_gate_timestamp: now()
         })
         RETURN Ok(HumanGateDecision::Approve)
       
       "expand":
         DISPLAY: "[Full skill content...]"
         PROMPT: "Actions: [approve] [reject]"
         INPUT: action2
         IF action2 == "approve":
           RETURN Ok(HumanGateDecision::Approve)
         ELSE:
           RETURN Err(E-CREATE-????: "User rejected")
       
       "edit":
         // Advanced mode: allow manual edits
         PROMPT: "Edit skill (careful!):"
         INPUT: edited_content
         // Re-validate edited content
         CALL handle_phase_3_validation(memory)
         IF validation passes:
           // Continue with edited version
           RETURN Ok(HumanGateDecision::Approve)
       
       "reject":
         memory.push_state(PHASE-4, {
           human_gate_response: "reject"
         })
         DISPLAY: "Operation cancelled. No changes made."
         RETURN Err(E-CREATE-????: "User rejected")
       
       timeout (after 120s):
         DISPLAY: "Timeout: No response for 120 seconds"
         CLEANUP: Discard in-memory state
         RETURN Err(E-CREATE-????: "Human Gate timeout")
  
  RETURN Ok(...)
  
  TIMEOUT: 120 seconds
```

**Collision Handler**:

```markdown
handle_collision_gate(memory: CoALAMemory, existing: Metadata) 
  → Result<CollisionAction, Error>
  
  DISPLAY: ""
  DISPLAY: "⚠️  Skill already exists: {skill_name}"
  DISPLAY: ""
  DISPLAY: "Existing location(s):"
  
  FOR each_cli IN target_clis:
    skill_path = ".{each_cli}/skills/{skill_name}/"
    IF file_exists(skill_path):
      DISPLAY: "  - {skill_path}"
  
  DISPLAY: ""
  DISPLAY: "Created: {existing.created}"
  DISPLAY: "Last modified: {file_mtime}"
  DISPLAY: ""
  
  PROMPT: "Actions: [overwrite] [rename] [cancel]"
  INPUT: action
  
  CASE action:
    "overwrite":
      // Create backup
      backup_timestamp = now().format("YYYY-MM-DDTHH-MM-SS")
      backup_name = "{skill_name}-{backup_timestamp}"
      backup_path = ".hefesto/backups/{backup_name}.tar.gz"
      
      TRY:
        FOR each_cli IN target_clis:
          skill_dir = ".{each_cli}/skills/{skill_name}/"
          tar_czf(backup_path, skill_dir)
      CATCH error:
        ERROR: "Failed to create backup"
      
      DISPLAY: "Backup created: {backup_path}"
      
      // Continue with overwrite
      memory.push_state(PHASE-4, {
        collision_detected: true,
        action_chosen: "overwrite",
        backup_path: backup_path,
        human_gate_response: "approve"
      })
      
      RETURN Ok(CollisionAction::Overwrite)
    
    "rename":
      PROMPT: "New skill name:"
      INPUT: new_name
      
      new_name = sanitize_skill_name(new_name)
      
      // Check collision with new name
      collision_again = false
      FOR cli IN target_clis:
        IF file_exists(".{cli}/skills/{new_name}/"):
          collision_again = true
          BREAK
      
      IF collision_again:
        DISPLAY: "⚠️  New name also exists. Try again."
        RETURN handle_collision_gate(...)  // Recursion
      
      memory.push_state(PHASE-4, {
        collision_detected: true,
        action_chosen: "rename",
        new_skill_name: new_name,
        human_gate_response: "approve"
      })
      
      // Update memory for next phases
      skill = memory.get_state(PHASE-2)
      skill.skill_name = new_name
      // Proceed with new name
      
      RETURN Ok(CollisionAction::Rename(new_name))
    
    "cancel":
      DISPLAY: "Operation cancelled."
      
      memory.push_state(PHASE-4, {
        collision_detected: true,
        action_chosen: "cancel",
        human_gate_response: "reject"
      })
      
      RETURN Err(E-CREATE-????: "User cancelled on collision")
```

---

## PHASE 5: Persistence

**Input**: Approved skill  
**Output**: Persisted files  
**Checkpoint**: CHECKPOINT-5

```markdown
handle_phase_5_persistence(memory: CoALAMemory) 
  → Result<PersistenceResult, Error>
  
  1. RETRIEVE ALL STATE
     skill = memory.get_state(PHASE-2)
     skill_name = skill.skill_name
     skill_content = skill.skill_content
     metadata = skill.metadata
     
     parsed = memory.get_state(PHASE-1)
     target_clis = parsed.target_cli
  
  2. CREATE DIRECTORIES
     created_dirs = Vec::new()
     
     FOR each_cli IN target_clis:
       skill_dir = ".{each_cli}/skills/{skill_name}/"
       
       TRY:
         create_directory_recursive(skill_dir)
         created_dirs.push(skill_dir)
       CATCH PermissionError:
         // ROLLBACK: Remove all created directories
         FOR dir IN created_dirs:
           remove_directory(dir)
         
         ERROR E-CREATE-006: "Write permission denied: {skill_dir}"
         ABORT
  
  3. WRITE SKILL FILES
     files_written = Vec::new()
     
     FOR each_cli IN target_clis:
       skill_path = ".{each_cli}/skills/{skill_name}/SKILL.md"
       metadata_path = ".{each_cli}/skills/{skill_name}/metadata.yaml"
       
       TRY:
         write_file(skill_path, skill_content)
         files_written.push(skill_path)
         
         write_file(metadata_path, to_yaml(metadata))
         files_written.push(metadata_path)
       CATCH error:
         // ROLLBACK: Remove all written files and directories
         FOR file IN files_written:
           remove_file(file)
         FOR dir IN created_dirs:
           remove_directory(dir)
         
         ERROR E-CREATE-006: "Write failed: {error}"
         ABORT
  
  4. UPDATE MEMORY.MD
     memory_data = read_memory_yaml()
     
     IF NOT memory_data.skills_created:
       memory_data.skills_created = Vec::new()
     
     memory_data.skills_created.append({
       name: skill_name,
       created: now(),
       clis: target_clis,
       status: "active",
       version: "1.0.0"
     })
     
     TRY:
       write_file("MEMORY.md", to_yaml(memory_data))
     CATCH error:
       // ROLLBACK: Remove created files
       FOR file IN files_written:
         remove_file(file)
       
       ERROR E-CREATE-006: "Failed to update MEMORY.md"
       ABORT
  
  5. PUSH CHECKPOINT-5
     memory.push_state(PHASE-5, {
       persistence_success: true,
       files_created: files_written,
       directories_created: created_dirs,
       memory_updated: true,
       persistence_timestamp: now()
     })
  
  RETURN Ok(PersistenceResult {
    success: true,
    skill_name,
    files_created: files_written
  })
  
  PERFORMANCE TARGET: < 1s
```

---

## PHASE 6: Success & Cleanup

**Input**: Persisted skill  
**Output**: Success message + cleanup  
**Checkpoint**: CHECKPOINT-6

```markdown
handle_phase_6_success(memory: CoALAMemory) 
  → Result<(), Error>
  
  1. RETRIEVE SKILL INFO
     skill = memory.get_state(PHASE-2)
     persistence = memory.get_state(PHASE-5)
     
     skill_name = skill.skill_name
     files_created = persistence.files_created
  
  2. DISPLAY SUCCESS MESSAGE
     DISPLAY: ""
     DISPLAY: "✅ Skill created successfully!"
     DISPLAY: ""
     DISPLAY: "Name: {skill_name}"
     DISPLAY: "Location(s):"
     
     FOR file IN files_created:
       IF file.ends_with("SKILL.md"):
         DISPLAY: "  - {file}"
     
     DISPLAY: ""
     DISPLAY: "Next steps:"
     DISPLAY: "  - Validate: /hefesto.validate {skill_name}"
     DISPLAY: "  - View: /hefesto.show {skill_name}"
     DISPLAY: "  - Test: Use the skill with your AI CLI"
     DISPLAY: ""
  
  3. CLEANUP IN-MEMORY STATE
     memory.clear_non_checkpoint_state()
     // Keep checkpoints for debugging, clear temp data
  
  4. PUSH CHECKPOINT-6
     memory.push_state(PHASE-6, {
       final_state: "success",
       skill_created: skill_name,
       target_clis: persistence.directories_created,
       completed_at: now()
     })
  
  RETURN Ok(())
  
  PERFORMANCE TARGET: < 100ms
```

---

## Error Recovery Flow

```
IF error at phase N:
  
  1. Log error with phase context
  2. Retrieve CHECKPOINT-(N-1)
     last_valid = memory.rollback_to(N-1)
  
  3. Filesystem cleanup
     FOR file IN last_valid.files_created:
       remove_file(file)
     FOR dir IN last_valid.directories_created:
       remove_directory(dir)
  
  4. Display error message
     DISPLAY: ERROR [E-CREATE-XXX]: {message}
     DISPLAY: Suggestion: {remediation}
  
  5. Offer retry
     PROMPT: "Retry? [yes] [no]"
     IF yes:
       GOTO PHASE 1 (allow retry with new input)
```

---

## Implementation Checklist

- [ ] **Phase 0**: CONSTITUTION + MEMORY validation
- [ ] **Phase 1**: Argument parsing + Wizard mode
- [ ] **Phase 2**: Template loading + skill generation
- [ ] **Phase 3**: T0 rule validation + security checks
- [ ] **Phase 4**: Human Gate + collision handling
- [ ] **Phase 5**: Atomic file persistence + MEMORY update
- [ ] **Phase 6**: Success message + cleanup

---

## Testing Strategy

Each phase needs unit tests:

```
Phase 0: 2 tests
  ├─ Valid CONSTITUTION + MEMORY
  └─ Invalid/missing CONSTITUTION

Phase 1: 3 tests
  ├─ Basic parsing
  ├─ Wizard mode
  └─ Input validation (E-CREATE-001, E-CREATE-007)

Phase 2: 2 tests
  ├─ Template rendering
  └─ Name sanitization

Phase 3: 2 tests
  ├─ T0 rule validation
  └─ Secret detection

Phase 4: 3 tests
  ├─ Normal approval
  ├─ Collision + overwrite
  └─ Collision + rename

Phase 5: 2 tests
  ├─ Successful persistence
  └─ Permission error + rollback

Phase 6: 1 test
  └─ Success message

TOTAL: 15 unit tests
```

---

**Version:** 1.0.0  
**Status:** Ready for implementation  
**Integration:** hefesto.create-coala-memory.md
