---
description: Manage Codex provider configuration
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
arguments:
  - name: action
    type: string
    description: "Action: status, test, remove"
---

# Configure

Manage Codex (GPT) provider for claude-delegator.

## Parse Arguments

Get `action` from arguments:
- `action`: status | test | remove

If no arguments provided, ask:

**Question**: "What would you like to do?"
**Options**:
- "Check status"
- "Test Codex connection"
- "Remove Codex configuration"

## Action: status

Read `~/.claude/settings.json` and check Codex configuration:

```bash
cat ~/.claude/settings.json | jq '.mcpServers.codex // "NOT_CONFIGURED"' 2>/dev/null
```

Display:
```
Codex Status:
─────────────
• MCP Server:  [✓ Configured / ✗ Not configured]
• CLI:         [✓ Installed / ✗ Missing]
• Auth:        Run `codex login` to verify
```

Also check rules installation:
```bash
ls ~/.claude/rules/delegator/ 2>/dev/null
```

## Action: test

Make a simple call:
```
mcp__codex__codex({ prompt: "Say 'Codex working!' and nothing else" })
```

Report result:
```
Codex Test:
───────────
• Status:   ✓ Working (responded in X.Xs)
```

Or if failed:
```
• Status:   ✗ Failed: [error message]
• Fix:      Run `codex login` to authenticate
```

## Action: remove

Confirm first:

**Question**: "Remove Codex configuration and plugin rules?"
**Options**:
- "Yes, remove everything"
- "No, cancel"

If confirmed:

1. Remove from `~/.claude/settings.json`:
   - Read current settings
   - Delete `mcpServers.codex` entry
   - Write back

2. Remove installed rules:
   ```bash
   rm -rf ~/.claude/rules/delegator/
   ```

Confirm removal:
```
✓ Removed 'codex' from MCP servers
✓ Removed rules from ~/.claude/rules/delegator/

To reinstall: /claude-delegator:setup
```

## Error Handling

### CLI not installed
```
Error: Codex CLI not found.

Install with: npm install -g @openai/codex
Then run: codex login
```

### Auth failed
```
Error: Codex authentication failed.

Run: codex login
```
