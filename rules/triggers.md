# Delegation Triggers

This file defines when and how to delegate to Codex (GPT) across three roles: Worker, Oracle, and Momus.

## Role Auto-Detection

Automatically route to the appropriate role based on task type:

| Signal | Role | Examples |
|--------|------|----------|
| Action verb + target | **Worker** | "add tests", "fix the bug", "update README", "implement feature", "create config" |
| Question word or analysis | **Oracle** | "what are the tradeoffs", "how should I", "is this secure", "review this architecture" |
| "plan" + review/validate | **Momus** | "review this plan", "validate the approach", "check this plan" |

**Default on ambiguity**: Worker (bias toward action)

Examples:
- "Improve the README" → Worker (action implied)
- "How should I improve the README?" → Oracle (question)
- "Review my plan to improve the README" → Momus (plan review)

---

## Explicit Triggers (Highest Priority)

User intent is explicit. Always honor direct requests.

| Phrase Pattern | Role | Action |
|----------------|------|--------|
| "ask GPT", "consult GPT", "GPT's opinion" | Oracle | Advisory mode |
| "have GPT implement", "GPT should fix" | Worker | Execution mode |
| "review this plan with GPT" | Momus | Plan validation |
| "oracle" | Oracle | Explicit oracle role |
| "get a second opinion" | Oracle | Advisory mode |

---

## Worker Triggers (→ Execution)

Worker is invoked for implementation tasks with clear action verbs.

### Action Patterns

| Pattern | Examples |
|---------|----------|
| "add [thing]" | "Add a section to README", "Add tests for X" |
| "fix [thing]" | "Fix the bug in auth", "Fix the failing test" |
| "update [thing]" | "Update the config", "Update dependencies" |
| "implement [thing]" | "Implement feature X", "Implement the API endpoint" |
| "create [thing]" | "Create a new component", "Create the migration" |
| "delete/remove [thing]" | "Delete the unused code", "Remove deprecated API" |
| "refactor [thing]" | "Refactor the auth module" |

### Worker Sandbox

Worker executes with:
- `sandbox: workspace-write` - Can modify files in workspace
- `approval-policy: on-failure` - Only prompts on errors
- `cwd: [current directory]` - Operates in current working directory

---

## Oracle Triggers (→ Advisory)

Oracle is invoked for strategic advice, analysis, and complex decisions.

### Architecture & Design

| Intent Pattern | Example |
|----------------|---------|
| "review this architecture" | "Review this database schema" |
| "is this design sound" | "Is this API design sound?" |
| "what are the tradeoffs" | "Tradeoffs of this caching approach" |
| "should I use [A] or [B]" | "Should I use microservices or monolith?" |
| "how should I structure" | "How should I structure this service?" |

### Security

| Intent Pattern | Example |
|----------------|---------|
| "security implications of" | "Security implications of this auth flow" |
| "is this secure" | "Is this token handling secure?" |
| "vulnerability in" | "Any vulnerabilities in this code?" |
| "threat model" | "Threat model for this API" |

### Code Review (Advisory)

| Intent Pattern | Example |
|----------------|---------|
| "code review [code]" | "Code review this function" |
| "review for edge cases" | "Review for edge cases in this logic" |
| "what am I missing" | "What am I missing in this implementation?" |

### Debugging Escalation

| Condition | Action |
|-----------|--------|
| 2+ failed fix attempts | Suggest oracle escalation |
| "why is this failing" (after attempts) | Oracle with full failure context |
| "I've tried everything" | Oracle with documented attempts |

---

## Momus Triggers (→ Plan Validation)

Momus is invoked to validate work plans before execution.

| Intent Pattern | Example |
|----------------|---------|
| "review this plan" | "Review this migration plan" |
| "validate the approach" | "Validate my approach before I start" |
| "check this plan for gaps" | "Check this implementation plan" |
| "is this plan complete" | "Is this refactoring plan complete?" |

---

## Trigger Priority

1. **Explicit user request** - Always honor direct role requests ("ask GPT", "have GPT implement")
2. **Plan validation** - "plan" + review/validate → Momus
3. **Question/analysis** - Question words, "review", "analyze" → Oracle
4. **Action verbs** - add, fix, implement, update, create → Worker
5. **Ambiguous** - Default to Worker (bias toward action)

---

## When NOT to Delegate

| Situation | Reason |
|-----------|--------|
| Simple syntax questions | Claude knows the answer |
| Direct file operations (no reasoning needed) | No external insight needed |
| Trivial bug fixes (obvious solution) | Don't waste delegation |
| User just wants info/explanation | Answer directly |
| First attempt at any fix | Try yourself first (except Worker tasks) |

---

## Context-Dependent Triggers

```
IF 2+ fix attempts failed
AND error persists
THEN suggest oracle escalation

IF user is frustrated
AND problem is complex
THEN offer oracle consultation

IF architectural decision
AND long-term impact
THEN recommend oracle review

IF task involves code changes
AND action verb present
THEN route to Worker
```

---

## Role Reference

| Role | Prompt File | Purpose |
|------|-------------|---------|
| Worker | `prompts/worker.md` | Execute implementation tasks |
| Oracle | `prompts/oracle.md` | Strategic advice, architecture, security |
| Momus | `prompts/momus.md` | Plan validation and critique |
