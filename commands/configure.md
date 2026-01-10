---
description: Add, customize, or remove model providers
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
arguments:
  - name: action
    type: string
    description: "Action: add, remove, list, test"
  - name: provider
    type: string
    description: "Provider: codex, gemini, custom"
---

# Configure

Manage model providers for claude-delegator.

## Parse Arguments

Get `action` and `provider` from arguments:
- `action`: add | remove | list | test
- `provider`: codex | gemini | custom

If no arguments provided, ask:

**Question**: "What would you like to do?"
**Options**:
- "List configured providers"
- "Add a provider"
- "Remove a provider"
- "Test a provider"

## Action: list

Read `~/.claude/settings.json` and list configured MCP servers:

```bash
cat ~/.claude/settings.json | jq '.mcpServers // {}' 2>/dev/null
```

Display:
```
Configured Providers:
─────────────────────
• codex     - GPT via Codex CLI
• gemini    - Gemini via MCP wrapper
```

Also check rules installation:
```bash
ls ~/.claude/rules/delegator/ 2>/dev/null
```

## Action: add

### add codex

Check if codex is installed:
```bash
which codex && codex --version
```

If not installed, offer to install:
```bash
npm install -g @openai/codex
codex login
```

Add to `~/.claude/settings.json`:
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

### add gemini

Check if gemini is installed:
```bash
which gemini && gemini --version
```

If not installed, offer to install:
```bash
npm install -g @google/gemini-cli
```

Detect package manager:
```bash
which bun 2>/dev/null && echo "PKG_MANAGER=bun" || \
which npm 2>/dev/null && echo "PKG_MANAGER=npm" || \
which yarn 2>/dev/null && echo "PKG_MANAGER=yarn" || \
echo "PKG_MANAGER=NONE"
```

Install MCP server dependencies (use detected package manager):
```bash
# If bun
cd ${CLAUDE_PLUGIN_ROOT}/servers/gemini-mcp && bun install

# If npm
cd ${CLAUDE_PLUGIN_ROOT}/servers/gemini-mcp && npm install

# If yarn
cd ${CLAUDE_PLUGIN_ROOT}/servers/gemini-mcp && yarn install
```

Add to `~/.claude/settings.json`:

**If bun:**
```json
{
  "mcpServers": {
    "gemini": {
      "type": "stdio",
      "command": "bun",
      "args": ["run", "${CLAUDE_PLUGIN_ROOT}/servers/gemini-mcp/src/index.ts"]
    }
  }
}
```

**If npm or yarn:**
```json
{
  "mcpServers": {
    "gemini": {
      "type": "stdio",
      "command": "npx",
      "args": ["tsx", "${CLAUDE_PLUGIN_ROOT}/servers/gemini-mcp/src/index.ts"]
    }
  }
}
```

### add custom

Interactive setup for custom CLI tools:

**Question 1**: "What is the CLI command name?"
(e.g., "mistral", "llama", etc.)

**Question 2**: "What arguments should be passed?"
(e.g., "--model", "chat", etc.)

**Question 3**: "What should this provider be called in MCP?"
(e.g., "my-local-llm")

Generate config and add to settings.

## Action: remove

**Question**: "Which provider would you like to remove?"
**Options**: List currently configured providers

Remove from `~/.claude/settings.json`:
- Read current settings
- Delete the specified mcpServers entry
- Write back

Confirm removal:
```
✓ Removed 'gemini' from MCP servers

Note: The CLI tool itself is not uninstalled.
To reinstall: /claude-delegator:configure add gemini
```

## Action: test

**Question**: "Which provider would you like to test?"
**Options**: List currently configured providers + "All"

### Test codex
Make a simple call:
```
mcp__codex__codex({ prompt: "Say 'Codex working!' and nothing else" })
```

### Test gemini
Make a simple call:
```
mcp__gemini__gemini({ prompt: "Say 'Gemini working!' and nothing else" })
```

Report results:
```
Provider Tests:
───────────────
• codex   ✓ Working (responded in 1.2s)
• gemini  ✓ Working (responded in 0.8s)
```

Or if failed:
```
• codex   ✗ Failed: Authentication required
          Run: codex login
```

## Error Handling

### Provider not found
```
Error: Provider 'xyz' is not configured.

Available providers: codex, gemini

To add a provider: /claude-delegator:configure add <provider>
```

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
