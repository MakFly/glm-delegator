# Model Orchestration

You have access to GPT via MCP tools. Use it strategically based on these guidelines.

## Available Tools

| Tool | Provider | Use For |
|------|----------|---------|
| `mcp__codex__codex` | GPT | Start new delegation (Worker, Oracle, or Momus) |
| `mcp__codex__codex-reply` | GPT | Continue conversation (retry failures, follow-up) |

---

## Three-Role Model

| Role | Purpose | Sandbox | Approval | Response Handling |
|------|---------|---------|----------|-------------------|
| **Worker** | Execute implementation tasks | `workspace-write` | `on-failure` | Verify then report |
| **Oracle** | Strategic advice, architecture | `read-only` | `on-request` | Synthesize |
| **Momus** | Plan validation, critique | `read-only` | `on-request` | Synthesize |

---

## Phase 0: Role Detection (EVERY message)

Before processing a request, determine the appropriate role:

```
1. Check explicit triggers ("ask GPT" → Oracle, "have GPT implement" → Worker)
2. Check for plan review ("review this plan" → Momus)
3. Check for questions/analysis (question words → Oracle)
4. Check for action verbs (add, fix, implement → Worker)
5. Ambiguous → Default to Worker
```

See `rules/triggers.md` for complete trigger definitions.

---

## Worker Flow (Execution)

When delegating to Worker:

### Step 1: Notify User

**Always** inform user before delegating:
```
Delegating to Worker: [brief task summary]
```

### Step 2: Execute Delegation

```typescript
mcp__codex__codex({
  prompt: "[Worker delegation format - see delegation-format.md]",
  sandbox: "workspace-write",
  "approval-policy": "on-failure",
  cwd: "[current working directory]",
  "developer-instructions": "[contents of prompts/worker.md]"
})
```

### Step 3: Verify Results

After Worker completes:

1. **Read reported files** - Confirm changes match Worker's report
2. **Run verification** - If project has tests/build/lint, run them
3. **Check for issues** - Look for obvious problems in changed code

### Step 4: Report to User

**On success** (expandable format):
```
**Worker completed**: [1-2 sentence summary]

<details>
<summary>Details</summary>

**Files modified**:
- [file list from Worker]

**Verification**:
- [what was checked, results]
</details>
```

**On failure** → Proceed to retry flow

### Step 5: Retry Flow (On Verification Failure)

```
Attempt 1: Worker completes → Verification fails
    ↓
Attempt 2: codex-reply with error context → Verification fails
    ↓
Attempt 3: codex-reply with error context → Verification fails
    ↓
Escalate: Report to user with full context
```

Use `mcp__codex__codex-reply` with the conversation ID:

```typescript
mcp__codex__codex-reply({
  conversationId: "[from previous response]",
  prompt: "Verification failed: [specific error]. Please fix and verify again."
})
```

After 3 failed attempts, escalate to user:
```
Worker attempted this task 3 times but verification continues to fail.

**Last error**: [error details]
**Files modified**: [list]
**Attempts made**: [summary of each attempt]

How would you like to proceed?
```

---

## Oracle Flow (Advisory)

When delegating to Oracle:

### Step 1: Notify User
```
Consulting Oracle: [topic]
```

### Step 2: Execute Delegation

```typescript
mcp__codex__codex({
  prompt: "[Oracle delegation format - see delegation-format.md]",
  "developer-instructions": "[contents of prompts/oracle.md]"
})
```

### Step 3: Synthesize Response

**ALWAYS synthesize** - Never show raw output directly:

1. Extract key recommendations and insights
2. Apply your judgment - external models can be wrong
3. Disagree when warranted - explain why
4. Connect to user's specific situation

```
**Oracle's analysis**:
[summary of key points]

**Key recommendations**:
- [recommendation 1]
- [recommendation 2]

**My assessment**: [your evaluation, any disagreements, how this applies]
```

---

## Momus Flow (Plan Validation)

When delegating to Momus:

### Step 1: Notify User
```
Validating plan with Momus...
```

### Step 2: Execute Delegation

```typescript
mcp__codex__codex({
  prompt: "[Momus delegation format - see delegation-format.md]",
  "developer-instructions": "[contents of prompts/momus.md]"
})
```

### Step 3: Report Verdict

```
**Plan review**: [OKAY / REJECT]

[Momus's justification]

[If REJECT: Top issues to address]
```

---

## Cost Awareness

External model calls cost money. Use strategically:

- **Don't spam** - One well-structured delegation beats five vague ones
- **Worker for action** - Don't ask Oracle when you need implementation
- **Use codex-reply** - Continue conversations instead of starting fresh
- **Avoid redundant calls** - If you have the answer, don't delegate

---

## Anti-Patterns

| Don't Do This | Do This Instead |
|---------------|-----------------|
| Delegate without notifying user | Always show "Delegating to [Role]: [task]" |
| Skip verification after Worker | Always verify changed files |
| Show raw Worker output | Summarize with expandable details |
| Retry indefinitely | Max 3 attempts, then escalate |
| Mix roles in one delegation | One role per delegation |
| Delegate trivial tasks | Handle directly |
