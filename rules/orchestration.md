# Model Orchestration

You have access to GLM-4.7 experts via MCP tools. Use them strategically based on these guidelines.

## Available Tools

| Tool | Provider | Use For |
|------|----------|---------|
| `mcp__glm-delegator__glm_{expert}` | GLM-4.7 (Z.AI) | Delegate to an expert |

> **Note:** Each delegation is independent—include full context in every call.

## Available Experts

| Expert | MCP Tool | Specialty |
|--------|----------|-----------|
| **Architect** | `glm_architect` | System design, tradeoffs, complex debugging |
| **Plan Reviewer** | `glm_plan_reviewer` | Plan validation before execution |
| **Scope Analyst** | `glm_scope_analyst` | Pre-planning, catching ambiguities |
| **Code Reviewer** | `glm_code_reviewer` | Code quality, bugs, security issues (EN/FR/CN) |
| **Security Analyst** | `glm_security_analyst` | Vulnerabilities, threat modeling |

---

## Stateless Design

**Each delegation is independent.** The expert has no memory of previous calls.

**Implications:**
- Include ALL relevant context in every delegation prompt
- For retries, include what was attempted and what failed
- Don't assume the expert remembers previous interactions

---

## PROACTIVE Delegation (Check on EVERY message)

Before handling any request, check if an expert would help:

| Signal | Expert |
|--------|--------|
| Architecture/design decision | Architect |
| 2+ failed fix attempts on same issue | Architect (fresh perspective) |
| "Review this plan", "validate approach" | Plan Reviewer |
| Vague/ambiguous requirements | Scope Analyst |
| "Review this code", "find issues" | Code Reviewer |
| Security concerns, "is this secure" | Security Analyst |

**If a signal matches → delegate to the appropriate expert.**

---

## REACTIVE Delegation (Explicit User Request)

When user explicitly requests GLM:

| User Says | Action |
|-----------|--------|
| "ask GLM", "consult GLM" | Identify task type → route to appropriate expert |
| "ask GLM to review the architecture" | Delegate to Architect |
| "have GLM review this code" | Delegate to Code Reviewer |
| "GLM security review" | Delegate to Security Analyst |

**Always honor explicit requests.**

---

## Delegation Flow (Step-by-Step)

When delegation is triggered:

### Step 1: Identify Expert
Match the task to the appropriate expert based on triggers.

### Step 2: Determine Mode
| Task Type | Mode |
|-----------|------|
| Analysis, review, recommendations | Advisory |
| Make changes, fix issues, implement | Implementation |

### Step 3: Notify User
Always inform the user before delegating:
```
Delegating to [Expert Name]: [brief task summary]
```

### Step 4: Call the Expert
```typescript
mcp__glm-delegator__glm_{expert}({
  task: "[clear description of what you need]",
  mode: "[advisory or implementation]",
  context: "[relevant context about the codebase]",
  files: ["[list of relevant files]"]
})
```

### Step 5: Handle Response
1. **Synthesize** - Never show raw output directly
2. **Extract insights** - Key recommendations, issues, changes
3. **Apply judgment** - Experts can be wrong; evaluate critically
4. **Verify implementation** - For implementation mode, confirm changes work

---

## Retry Flow (Implementation Mode)

When implementation fails verification, retry with a NEW call including error context:

```
Attempt 1 → Verify → [Fail]
     ↓
Attempt 2 (new call with: original task + what was tried + error details) → Verify → [Fail]
     ↓
Attempt 3 (new call with: full history of attempts) → Verify → [Fail]
     ↓
Escalate to user
```

---

## Example: Architecture Question

User: "What are the tradeoffs of Redis vs in-memory caching?"

**Step 1**: Signal matches "Architecture decision" → Architect

**Step 2**: Advisory mode (question, not implementation)

**Step 3**: "Delegating to Architect: Analyze caching tradeoffs"

**Step 4**:
```typescript
mcp__glm-delegator__glm_architect({
  task: "Analyze tradeoffs between Redis and in-memory caching for this use case",
  mode: "advisory",
  context: "[user's situation, full details]"
})
```

**Step 5**: Synthesize response, add your assessment.

---

## Example: Retry After Failed Implementation

First attempt failed with "TypeError: Cannot read property 'x' of undefined"

**Retry call:**
```typescript
mcp__glm-delegator__glm_code_reviewer({
  task: `Fix the input validation error in user registration.

PREVIOUS ATTEMPT:
- Added validation middleware to routes/auth.ts
- Error: TypeError: Cannot read property 'x' of undefined at line 45
- The middleware was added but req.body was undefined

Please fix this issue.`,
  mode: "implementation",
  context: "Express 4.x application with body parser in app.ts",
  files: ["routes/auth.ts", "app.ts"]
})
```

---

## Cost Awareness

- **Don't spam** - One well-structured delegation beats multiple vague ones
- **Include full context** - Saves retry costs from missing information
- **Reserve for high-value tasks** - Architecture, security, complex analysis

---

## Anti-Patterns

| Don't Do This | Do This Instead |
|---------------|-----------------|
| Delegate trivial questions | Answer directly |
| Show raw expert output | Synthesize and interpret |
| Skip user notification | ALWAYS notify before delegating |
| Retry without including error context | Include FULL history of what was tried |
| Assume expert remembers previous calls | Include all context in every call |
