---
name: uninstall
description: Uninstall glm-delegator (remove MCP config and rules)
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
timeout: 30000
---

# Uninstall

Remove glm-delegator from Claude Code.

## Confirm Removal

**Question**: "Remove GLM Delegator MCP configuration and plugin rules?"

**Options**:
- "Yes, uninstall"
- "No, cancel"

If cancelled, stop here.

## Remove MCP Configuration

Read `~/.claude.json` (or `~/.claude/settings.json`), delete `mcpServers.glm-delegator` entry, write back.

## Remove Installed Rules

```bash
rm -rf ~/.claude/rules/glm-delegator/
```

## Confirm Completion

```
✓ Removed 'glm-delegator' from MCP servers
✓ Removed rules from ~/.claude/rules/glm-delegator/

To reinstall: /glm-delegator:setup
```
