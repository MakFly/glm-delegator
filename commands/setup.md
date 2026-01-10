---
name: setup
description: Configure claude-delegator with Codex MCP server
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
timeout: 60000
---

# Setup

Configure Codex (GPT) as an AI collaborator via native MCP. Supports three roles: Worker (execution), Oracle (advisory), and Momus (plan validation).

## Step 1: Check Codex CLI

```bash
which codex 2>/dev/null && codex --version 2>&1 | head -1 || echo "CODEX_MISSING"
```

### If Missing

Tell user:
```
Codex CLI not found.

Install with: npm install -g @openai/codex
Then authenticate: codex login

After installation, re-run /claude-delegator:setup
```

**STOP here if Codex is not installed.**

## Step 2: Read Current Settings

```bash
cat ~/.claude/settings.json 2>/dev/null || echo "{}"
```

## Step 3: Configure MCP Server

Merge into `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "codex": {
      "type": "stdio",
      "command": "codex",
      "args": ["-m", "gpt-5.2-codex", "mcp-server"]
    }
  }
}
```

Note: Use `gpt-5.2-codex` explicitly for the latest model.

**CRITICAL**:
- Merge with existing settings, don't overwrite
- Preserve any existing `mcpServers` entries

## Step 4: Install Orchestration Rules

```bash
mkdir -p ~/.claude/rules/delegator && cp ${CLAUDE_PLUGIN_ROOT}/rules/*.md ~/.claude/rules/delegator/
```

## Step 5: Verify Installation

Run these checks and report results:

```bash
# Check 1: Codex CLI version
codex --version 2>&1 | head -1

# Check 2: MCP server configured
cat ~/.claude/settings.json | jq -r '.mcpServers.codex.args | join(" ")' 2>/dev/null

# Check 3: Rules installed (count files)
ls ~/.claude/rules/delegator/*.md 2>/dev/null | wc -l

# Check 4: Auth status (check if logged in)
codex auth status 2>&1 | head -1 || echo "Run 'codex login' to authenticate"
```

## Step 6: Report Status

Display actual values from the checks above:

```
claude-delegator Status
───────────────────────────────────────────────────
Codex CLI:     ✓ [version from check 1]
Model:         ✓ gpt-5.2-codex (or ✗ if not configured)
MCP Config:    ✓ ~/.claude/settings.json (or ✗ if missing)
Rules:         ✓ [N] files in ~/.claude/rules/delegator/
Auth:          [status from check 4]
───────────────────────────────────────────────────
```

If any check fails, report the specific issue and how to fix it.

## Step 7: Final Instructions

```
Setup complete!

Next steps:
1. Restart Claude Code to load MCP server
2. Authenticate: Run `codex login` in terminal (if not already done)

Three roles available:

┌─────────┬────────────────────────────────────────────────────┐
│ Worker  │ "Add a section to the README"                      │
│         │ "Fix the failing test"                             │
│         │ "Implement feature X"                              │
│         │ → Executes tasks directly, modifies files          │
├─────────┼────────────────────────────────────────────────────┤
│ Oracle  │ "What are the tradeoffs of X vs Y?"                │
│         │ "Review this architecture"                         │
│         │ "Is this secure?"                                  │
│         │ → Strategic advice, analysis, recommendations      │
├─────────┼────────────────────────────────────────────────────┤
│ Momus   │ "Review this plan"                                 │
│         │ "Validate my approach"                             │
│         │ → Plan critique before implementation              │
└─────────┴────────────────────────────────────────────────────┘

Role is auto-detected based on your request.
Explicit override: "Ask GPT..." (Oracle) or "Have GPT implement..." (Worker)
```
