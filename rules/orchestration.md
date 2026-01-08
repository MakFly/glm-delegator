# Multi-Model Orchestration

You have access to external AI models via MCP tools. Use them when they genuinely add value.

## Available Tools

| Tool | Provider | Use For |
|------|----------|---------|
| `mcp__codex__codex` | GPT | Architecture, debugging, code review |
| `mcp__codex__codex-reply` | GPT | Continue GPT conversation |
| `mcp__gemini__gemini` | Gemini | Research, docs, frontend, multimodal |
| `mcp__gemini__gemini-reply` | Gemini | Continue Gemini conversation |

---

## When Delegation Actually Adds Value

Be honest about when external models help vs. when your native tools are better.

### Use External Models When:

| Scenario | Why It Helps |
|----------|--------------|
| **User explicitly requests** | "Ask GPT", "Get Gemini's opinion" - honor the request |
| **Fresh perspective after failures** | 2+ failed attempts - different model may see what you missed |
| **Multimodal analysis** | Gemini can analyze images/PDFs differently |
| **Second opinion on critical decisions** | High-stakes architecture, security - verification matters |
| **User trusts specific model** | Some users prefer GPT/Gemini for certain domains |

### Use Your Native Tools When:

| Scenario | Why Native is Better |
|----------|---------------------|
| **Library research** | You have context7, WebSearch, exa - better integration |
| **Codebase questions** | You have LSP, Grep, Glob - direct access |
| **Simple code review** | You can read and analyze code directly |
| **Documentation lookup** | WebFetch + WebSearch are faster |
| **Quick best practices** | You already know common patterns |

### The Honest Truth

External delegation adds:
- **Latency** (10-60+ seconds for a response)
- **Cost** (API calls aren't free)
- **Context loss** (external model doesn't see conversation history)

Only delegate when the benefit outweighs these costs.

---

## When to Delegate (Decision Tree)

```
User explicitly asks for external model?
  → YES: Delegate immediately
  → NO: Continue...

Is this a multimodal task (image/PDF analysis)?
  → YES: Consider Gemini
  → NO: Continue...

Have you failed 2+ times on the same issue?
  → YES: Suggest escalation to GPT (ask user first)
  → NO: Continue...

Is this a critical/high-stakes decision where verification matters?
  → YES: Consider parallel consultation
  → NO: Continue...

Can you answer this with your native tools?
  → YES: Don't delegate. Just answer.
  → NO: Consider delegation
```

---

## Response Handling

When external model returns a response:

1. **Synthesize** - Don't show raw output
2. **Evaluate** - External models can be wrong
3. **Disagree when warranted** - If you spot issues, say so
4. **Connect to context** - Apply their response to user's situation

```
GPT's analysis: [summary]

Key points:
- [insight 1]
- [insight 2]

My assessment: [your evaluation, where you agree/disagree]
```

---

## Delegation Prompt Structure

**Core rule**: Include enough context for the question to be answerable.

Simple questions get simple prompts. Complex questions need more structure.

See `delegation-format.md` for examples.

---

## Escalation Pattern

After 2+ consecutive failures:

1. Document what you tried
2. **Ask user**: "I've tried X and Y without success. Want me to get GPT's perspective?"
3. Wait for approval
4. Include failure history when delegating

---

## Cost Awareness

- **GPT is expensive** - Reserve for architecture, security, verified second opinions
- **Gemini is cheaper** - More reasonable for research tasks
- **Your native tools are free** - Prefer them when equally capable

---

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Delegate trivial questions | Answer directly |
| Auto-delegate library questions | Use context7/WebSearch first |
| Show raw external output | Synthesize and interpret |
| Auto-escalate without asking | Suggest, then wait for approval |
| Delegate what you can answer | Only delegate when it adds value |
