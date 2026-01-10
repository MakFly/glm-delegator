# claude-delegator

![MCP Tools](https://img.shields.io/badge/Integration-MCP%20Tools-blue)
![Provider](https://img.shields.io/badge/Provider-Codex%20(GPT)-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

GPT as a native Claude Code tool via Codex CLI. Strategic advisor for architecture, debugging escalation, and code review.

---

## Install

Inside a Claude Code instance:

```
/plugin marketplace add jarrodwatts/claude-delegator
/plugin install claude-delegator
/claude-delegator:setup
```

Done! Claude now has access to GPT as the oracle advisor.

> **Note**: Requires Codex CLI. Setup will guide you through installation.

---

## What is claude-delegator?

Claude Code gains access to GPT via native MCP tool calls. Use it sparingly for complex decisions.

| Feature | What It Does |
|---------|-------------|
| **Native MCP Tool** | `mcp__codex__codex` appears as a regular tool |
| **Strategic Advisor** | Oracle role for architecture, security, debugging |
| **Plan Review** | Momus role validates work plans before execution |
| **Response Synthesis** | Claude interprets GPT output, never raw passthrough |

### When to Use GPT

| Use For | Example |
|---------|---------|
| Architecture decisions | "Review this database schema" |
| Debugging escalation | After 2+ failed fix attempts |
| Code review | "What am I missing in this auth flow?" |
| Security analysis | "Threat model for this API" |
| Tradeoff analysis | "Should I use microservices or monolith?" |

### When NOT to Use GPT

- Simple file operations
- First attempt at any fix
- Trivial decisions
- Research or documentation
- Frontend/UI generation

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Code                               │
│                                                                  │
│   User: "How should I structure this caching layer?"            │
│                                                                  │
│   Claude: [Detects architecture question]                        │
│           [Calls mcp__codex__codex with oracle role]            │
│                                                                  │
│           ┌──────────────────────────────────────┐              │
│           │  MCP Server: codex                   │              │
│           │  → codex mcp-server (native)         │              │
│           │  → Returns GPT analysis              │              │
│           └──────────────────────────────────────┘              │
│                                                                  │
│   Claude: "Based on GPT's analysis, I recommend..."             │
└─────────────────────────────────────────────────────────────────┘
```

### Plugin Structure

```
claude-delegator/
├── rules/                    # Installed to ~/.claude/rules/delegator/
│   ├── orchestration.md      # When to delegate
│   ├── triggers.md           # Explicit + semantic triggers
│   ├── model-selection.md    # Oracle decision guidelines
│   └── delegation-format.md  # Prompt structure
├── prompts/
│   ├── oracle.md             # Strategic advisor
│   └── momus.md              # Plan reviewer
├── commands/
│   ├── setup.md              # /claude-delegator:setup
│   └── configure.md          # /claude-delegator:configure
└── config/
    └── providers.json        # Provider configuration
```

---

## Configuration

### Available Tools

| Tool | Description |
|------|-------------|
| `mcp__codex__codex` | Start a conversation with GPT |
| `mcp__codex__codex-reply` | Continue an existing conversation |

### Role Prompts

| Role | Purpose |
|------|---------|
| `oracle` | Strategic advisor—architecture, security, complex debugging |
| `momus` | Plan reviewer—validates work plans before execution |

### Example Call

```typescript
mcp__codex__codex({
  prompt: "Review this caching architecture for race conditions",
  model: "gpt-5.2",
  "developer-instructions": "<oracle prompt>"
})
```

### Manual MCP Setup

If `/setup` doesn't work, manually add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "codex": {
      "type": "stdio",
      "command": "codex",
      "args": ["mcp-server"]
    }
  }
}
```

---

## Requirements

| Dependency | Installation |
|------------|--------------|
| Codex CLI | `npm install -g @openai/codex` |

### Authentication

```bash
codex login
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/claude-delegator:setup` | Configure MCP server, install rules |
| `/claude-delegator:configure` | Check status, test, or remove |

---

## Testing

To test the plugin locally during development, run Claude with a local plugin directory (see `commands/setup.md` for setup context):

```bash
claude --plugin-dir /path/to/claude-delegator
```

This loads the plugin directly from your working copy so you can iterate without reinstalling.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MCP server not found | Restart Claude Code after setup |
| Codex not authenticated | Run `codex login` |
| Tool not appearing | Check `~/.claude/settings.json` has codex entry |

---

## Acknowledgments

Role prompts (oracle, momus) adapted from [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) by [@code-yeongyu](https://github.com/code-yeongyu).

---

## License

MIT License - see [LICENSE](LICENSE) for details.
