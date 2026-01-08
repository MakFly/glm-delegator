# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code plugin that provides external AI models (GPT via Codex, Gemini) as native MCP tool providers. The plugin enables liberal delegation to models that excel at specific tasks.

## Development Commands

```bash
# Install Gemini MCP server dependencies
cd servers/gemini-mcp && bun install

# Run Gemini MCP server (for testing)
cd servers/gemini-mcp && bun run src/index.ts

# No build step - Bun runs TypeScript directly
```

## Architecture

### Plugin Structure

This is a Claude Code plugin with:
- **MCP servers** (`servers/`) - Wrap external CLIs as MCP tool providers
- **Rules** (`rules/`) - Orchestration logic installed to `~/.claude/rules/delegator/`
- **Prompts** (`prompts/`) - Role-specific system prompts auto-injected into delegations
- **Commands** (`commands/`) - `/setup` and `/configure` slash commands

### MCP Integration

**Codex (GPT)**: Uses native `codex mcp-server` - no wrapper needed.

**Gemini**: Requires our wrapper at `servers/gemini-mcp/src/index.ts` because Gemini CLI lacks native MCP support. The wrapper:
- Spawns `gemini` CLI as child process via `Bun.spawn()`
- Auto-injects role prompts from `prompts/` based on `role` parameter
- Tracks active processes for cleanup on shutdown
- Uses `didTimeout` flag for accurate timeout detection

### Role Prompts

When `role` parameter is passed to `mcp__gemini__gemini`, the corresponding prompt from `prompts/` is prepended:
- `oracle` - Strategic advisor (architecture, security)
- `librarian` - Research specialist (docs, best practices)
- `frontend-engineer` - UI/UX code generation
- `explore` - Codebase navigation

### Rules Installation

The `/setup` command copies `rules/*.md` to `~/.claude/rules/delegator/`. These rules teach Claude when and how to delegate:
- `orchestration.md` - Phase 0 delegation check, response synthesis
- `triggers.md` - Explicit and semantic trigger patterns
- `model-selection.md` - GPT vs Gemini decision matrix
- `delegation-format.md` - Mandatory 7-section prompt structure

## Key Design Decisions

1. **MCP over subagents** - External models as tool providers, not wrapped in Claude subagents
2. **Liberal delegation** - Autonomously delegate when task matches model strengths
3. **7-section format** - Structured prompts ensure external models have full context
4. **Response synthesis** - Never show raw external output; always interpret and evaluate
5. **Role injection** - System prompts shape external model behavior per task type

## Provider Configuration

`config/providers.json` defines available providers with their CLI commands, MCP configs, roles, and strengths. The `defaults` section maps task types to preferred providers.

## Testing the MCP Server

The Gemini MCP server has no automated tests. Manual testing:
1. Ensure `gemini` CLI is installed and authenticated
2. Run `bun run servers/gemini-mcp/src/index.ts`
3. Send MCP tool calls via stdio
