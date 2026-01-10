---
name: configure
description: Uninstall claude-delegator (remove MCP config and rules)
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
timeout: 30000
---

# Configure

Uninstall claude-delegator from Claude Code.

## Confirm Removal

**Question**: "Remove Codex MCP configuration and plugin rules?"
**Options**:
- "Yes, uninstall"
- "No, cancel"

If cancelled, stop here.

## Remove MCP Configuration

Read `~/.claude/settings.json`, delete `mcpServers.codex` entry, write back.

## Remove Installed Rules

```bash
rm -rf ~/.claude/rules/delegator/
```

## Confirm Completion

```
✓ Removed 'codex' from MCP servers
✓ Removed rules from ~/.claude/rules/delegator/

To reinstall: /claude-delegator:setup
```
