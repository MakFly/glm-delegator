# Model Selection Guidelines

Codex (GPT) serves three roles: Worker (execution), Oracle (advisory), and Momus (plan validation). Each role has different sandbox settings and use cases.

## Role Overview

| Role | Purpose | Sandbox | Approval | When to Use |
|------|---------|---------|----------|-------------|
| **Worker** | Execute implementation tasks | `workspace-write` | `on-failure` | Action verbs: add, fix, implement, update |
| **Oracle** | Strategic advice, analysis | `read-only` | `on-request` | Questions, tradeoffs, architecture |
| **Momus** | Plan validation, critique | `read-only` | `on-request` | "Review this plan" |

---

## GPT (Codex) — Worker Role

**Tool:** `mcp__codex__codex`

### When to Use Worker

| Situation | Examples |
|-----------|----------|
| Implementation tasks | "Add tests for X", "Fix the bug in Y" |
| File modifications | "Update the README", "Create a config file" |
| Code changes | "Implement feature Z", "Refactor module W" |
| Build/test tasks | "Run and fix failing tests" |

### Worker Philosophy

Worker operates with **direct execution**:

> Execute the task, don't advise on it. Make changes, verify they work, report results.

Priorities:
1. Complete the requested task
2. Follow existing code patterns
3. Verify before reporting done
4. Stay within scope

### Worker Parameters

```typescript
mcp__codex__codex({
  prompt: "[Worker delegation format]",
  sandbox: "workspace-write",
  "approval-policy": "on-failure",
  cwd: "/path/to/project",
  "developer-instructions": "[prompts/worker.md content]"
})
```

### Worker Response Format

1. **Summary**: What was done (1-2 sentences)
2. **Files Modified**: List with brief descriptions
3. **Verification**: What was checked, results
4. **Issues**: Problems encountered (if any)

---

## GPT (Codex) — Oracle Role

**Tool:** `mcp__codex__codex`

### When to Consult Oracle

| Situation | Trigger |
|-----------|---------|
| Architecture decisions | System design, database schemas, API design |
| Complex debugging | After 2+ failed fix attempts |
| Code review | Multi-system thinking, edge case identification |
| Security analysis | Threat modeling, vulnerability assessment |
| Tradeoff analysis | When multiple valid approaches exist |
| Unfamiliar patterns | Domain-specific best practices |

### Oracle Philosophy

The oracle operates with **pragmatic minimalism**:

> Favor the least complex solution that fulfills actual requirements over theoretically optimal approaches.

Priorities:
1. Existing code patterns in the codebase
2. Developer experience
3. Maintainability over cleverness

### Oracle Parameters

```typescript
mcp__codex__codex({
  prompt: "[Oracle delegation format]",
  "approval-policy": "on-request",
  "developer-instructions": "[prompts/oracle.md content]"
})
```

### Oracle Response Format

**Essential** (always provided):
- Bottom line / recommendation
- Action plan
- Effort estimate: Quick / Short / Medium / Large

**Expanded** (when relevant):
- Reasoning
- Risk assessment

**Edge cases** (only if applicable):
- Escalation conditions
- Alternatives

---

## GPT (Codex) — Momus Role

**Tool:** `mcp__codex__codex`

### When to Use Momus

| Situation | Trigger |
|-----------|---------|
| Plan validation | Before executing a multi-step plan |
| Approach review | "Is this plan complete?" |
| Gap identification | "What am I missing in this plan?" |

### Momus Philosophy

Momus operates with **ruthless critique**:

> Find every gap, ambiguity, and missing context that would block implementation.

Focus:
1. Can this plan be executed as written?
2. Are all requirements clear?
3. Are verification criteria defined?
4. Is context complete?

### Momus Parameters

```typescript
mcp__codex__codex({
  prompt: "[Momus delegation format]",
  "approval-policy": "on-request",
  "developer-instructions": "[prompts/momus.md content]"
})
```

### Momus Response Format

- **Verdict**: OKAY / REJECT
- **Justification**: Why this verdict
- **Issues**: Critical gaps (if REJECT)
- **Summary**: Assessment of clarity, verifiability, completeness

---

## When NOT to Delegate

See `rules/triggers.md` for the complete list of when NOT to delegate.

General rule: Don't delegate trivial tasks. If Claude can do it directly with confidence, do it.

---

## Cost-Benefit Analysis

### Worth the Cost

- **Worker**: Substantial implementation tasks (not single-line fixes)
- **Oracle**: Architectural decisions, security concerns, after 2+ failures
- **Momus**: Complex plans before significant implementation

### Not Worth the Cost

- Questions Claude can answer directly
- Trivial code changes
- Style or formatting decisions
- Simple CRUD operations
- First attempt at any fix (for Oracle - try yourself first)

---

## Codex Parameters Reference

| Parameter | Values | Default | Notes |
|-----------|--------|---------|-------|
| `approval-policy` | `untrusted`, `on-failure`, `on-request`, `never` | `on-request` | Controls tool approval |
| `sandbox` | `read-only`, `workspace-write`, `danger-full-access` | `read-only` | File access level |
| `cwd` | path | current | Working directory |
| `developer-instructions` | string | - | System prompt injection |

Model selection is handled by your Codex CLI configuration, not passed per-call.
