# Delegation Triggers

This file defines when to delegate to GLM-4.7 experts via the GLM MCP server.

## IMPORTANT: Check These Triggers on EVERY Message

You MUST scan incoming messages for delegation triggers. This is NOT optional.

**Behavior:**
1. **PROACTIVE**: On every user message, check if semantic triggers match → delegate automatically
2. **REACTIVE**: If user explicitly mentions GLM → delegate immediately

When a trigger matches:
1. Identify the appropriate expert
2. Use the MCP tool `mcp__glm-delegator__glm_{expert}`
3. Pass the task, mode (advisory/implementation), context, and files

---

## Available Experts

| Expert | MCP Tool | Specialty | Use For |
|--------|----------|-----------|---------|
| **Architect** | `glm_architect` | System design, tradeoffs | Architecture decisions, complex debugging |
| **Plan Reviewer** | `glm_plan_reviewer` | Plan validation | Reviewing work plans before execution |
| **Scope Analyst** | `glm_scope_analyst` | Pre-planning analysis | Catching ambiguities before work starts |
| **Code Reviewer** | `glm_code_reviewer` | Code quality, bugs | Reviewing code changes, finding issues |
| **Security Analyst** | `glm_security_analyst` | Vulnerabilities, threats | Security audits, hardening |

## Explicit Triggers (Highest Priority)

User explicitly requests delegation:

| Phrase Pattern | Expert |
|----------------|--------|
| "ask GLM", "consult GLM" | Route based on context |
| "review this architecture" | Architect |
| "review this plan" | Plan Reviewer |
| "analyze the scope" | Scope Analyst |
| "review this code" | Code Reviewer |
| "security review", "is this secure" | Security Analyst |

## Semantic Triggers (Intent Matching)

### Architecture & Design (→ Architect)

| Intent Pattern | Example |
|----------------|---------|
| "how should I structure" | "How should I structure this service?" |
| "what are the tradeoffs" | "Tradeoffs of this caching approach" |
| "should I use [A] or [B]" | "Should I use microservices or monolith?" |
| System design questions | "Design a notification system" |
| After 2+ failed fix attempts | Escalation for fresh perspective |

### Plan Validation (→ Plan Reviewer)

| Intent Pattern | Example |
|----------------|---------|
| "review this plan" | "Review my migration plan" |
| "is this plan complete" | "Is this implementation plan complete?" |
| "validate before I start" | "Validate my approach before starting" |
| Before significant work | Pre-execution validation |

### Requirements Analysis (→ Scope Analyst)

| Intent Pattern | Example |
|----------------|---------|
| "what am I missing" | "What am I missing in these requirements?" |
| "clarify the scope" | "Help clarify the scope of this feature" |
| Vague or ambiguous requests | Before planning unclear work |
| "before we start" | Pre-planning consultation |

### Code Review (→ Code Reviewer)

| Intent Pattern | Example |
|----------------|---------|
| "review this code" | "Review this PR" |
| "find issues in" | "Find issues in this implementation" |
| "what's wrong with" | "What's wrong with this function?" |
| After implementing features | Self-review before merge |

### Security (→ Security Analyst)

| Intent Pattern | Example |
|----------------|---------|
| "security implications" | "Security implications of this auth flow" |
| "is this secure" | "Is this token handling secure?" |
| "vulnerabilities in" | "Any vulnerabilities in this code?" |
| "threat model" | "Threat model for this API" |
| "harden this" | "Harden this endpoint" |

## Trigger Priority

1. **Explicit user request** - Always honor direct requests
2. **Security concerns** - When handling sensitive data/auth
3. **Architecture decisions** - System design with long-term impact
4. **Failure escalation** - After 2+ failed attempts
5. **Don't delegate** - Default: handle directly

## When NOT to Delegate

| Situation | Reason |
|-----------|--------|
| Simple syntax questions | Answer directly |
| Direct file operations | No external insight needed |
| Trivial bug fixes | Obvious solution |
| Research/documentation | Use other tools |
| First attempt at any fix | Try yourself first |

## Advisory vs Implementation Mode

Any expert can operate in two modes:

| Mode | When to Use |
|------|-------------|
| **Advisory** | Analysis, recommendations, review verdicts |
| **Implementation** | Actually making changes, fixing issues |

Set the mode based on what the task requires.

**Examples:**

```
# Architect analyzing (advisory)
mcp__glm-delegator__glm_architect({
  task: "Analyze tradeoffs of Redis vs in-memory caching",
  mode: "advisory"
})

# Architect implementing (implementation)
mcp__glm-delegator__glm_architect({
  task: "Refactor the caching layer to use Redis",
  mode: "implementation"
})

# Security Analyst reviewing (advisory)
mcp__glm-delegator__glm_security_analyst({
  task: "Review this auth flow for vulnerabilities",
  mode: "advisory"
})

# Security Analyst hardening (implementation)
mcp__glm-delegator__glm_security_analyst({
  task: "Fix the SQL injection vulnerability in user.ts",
  mode: "implementation"
})
```
