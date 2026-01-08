# Delegation Triggers

When to delegate to external models.

## Explicit Triggers (Always Honor)

When users explicitly ask, delegate immediately:

| Phrase Pattern | Action |
|----------------|--------|
| "ask GPT", "consult GPT", "GPT's opinion" | `mcp__codex__codex` |
| "ask Gemini", "research with Gemini" | `mcp__gemini__gemini` |
| "get a second opinion" | `mcp__codex__codex` |
| "what does GPT/Gemini think" | Delegate to requested model |

---

## Conditional Triggers (Use Judgment)

These situations **may** warrant delegation. Evaluate first.

### After Failed Attempts

| Condition | Action |
|-----------|--------|
| 2+ failed fix attempts | **Suggest** GPT escalation (ask user first) |
| "I've tried everything" | Offer fresh perspective from external model |

### Verification for Critical Decisions

| Condition | Action |
|-----------|--------|
| Security-critical code | **Consider** GPT review as second opinion |
| Major architecture change | **Consider** parallel consultation |
| User seems uncertain about approach | **Offer** external validation |

---

## When NOT to Delegate

Prefer native tools for these scenarios:

| Scenario | Use Instead |
|----------|-------------|
| Library documentation | context7, WebSearch |
| Code search | LSP, Grep, Glob |
| Best practices lookup | WebSearch, your knowledge |
| Simple code review | Direct analysis |
| Documentation writing | Do it yourself |

---

## Role Selection (When Delegating)

| Role | Model | Use For |
|------|-------|---------|
| `oracle` | GPT | Architecture, security, debugging |
| `librarian` | Gemini | Research (when native tools insufficient) |
| `frontend-engineer` | Gemini | UI code generation |
| `explore` | Gemini | Codebase exploration (when you need parallel search) |

---

## The Decision

Before delegating, ask yourself:

1. Did the user explicitly ask for external model? → Delegate
2. Can I answer this with my native tools? → Don't delegate
3. Have I failed multiple times? → Suggest escalation
4. Is this high-stakes and verification matters? → Consider delegation
5. None of the above? → Don't delegate
