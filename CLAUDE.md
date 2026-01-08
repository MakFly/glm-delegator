# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code plugin that provides external AI models (GPT via Codex, Gemini) as native MCP tool providers. Liberal delegation to models that excel at specific tasks.

## Development Commands

```bash
# Install dependencies (from repo root)
cd servers/gemini-mcp && bun install

# Run MCP server locally
bun run servers/gemini-mcp/src/index.ts

# Test plugin installation
/claude-delegator:setup
```

No build step - Bun runs TypeScript directly.

## Architecture

### Data Flow

```
User Request → Claude Code → [Phase 0: Delegation Check]
                                    ↓
                    [Match trigger?] → Yes → MCP tool call
                                              ↓
                    mcp__codex__codex (GPT) ──or── mcp__gemini__gemini
                                              ↓
                    [Role prompt injected] → External CLI spawned
                                              ↓
                    [Response] → Claude synthesizes (never raw passthrough)
```

### Component Relationships

| Component | Location | Installed To | Purpose |
|-----------|----------|--------------|---------|
| MCP Server | `servers/gemini-mcp/src/index.ts` | Runtime (stdio) | Wraps Gemini CLI as MCP |
| Rules | `rules/*.md` | `~/.claude/rules/delegator/` | Teaches when/how to delegate |
| Prompts | `prompts/*.md` | Read at runtime | Shapes external model behavior |
| Commands | `commands/*.md` | Plugin namespace | `/setup`, `/configure` |

### MCP Server Internals (`servers/gemini-mcp/src/index.ts`)

Key behaviors:
- `buildArgs()` (line 133): Constructs CLI args, injects role prompts
- `runGemini()` (line 162): Spawns process, handles timeout via `didTimeout` flag
- `activeProcesses` Set (line 160): Tracks processes for cleanup on SIGINT/SIGTERM
- Role injection (lines 143-148): Prepends prompt from `prompts/{role}.md`

The `-reply` tool does NOT inject roles - it continues existing conversations.

### Role → Provider Mapping

| Role | Provider | Trigger Patterns |
|------|----------|------------------|
| `oracle` | GPT (Codex) | Architecture, security, debugging failures |
| `librarian` | Gemini | Research, docs, "how do I use X" |
| `frontend-engineer` | Gemini | UI/UX code generation |
| `explore` | Gemini | Codebase navigation |

## Key Design Decisions

1. **MCP over subagents** - External models as tool providers, not wrapped agents
2. **7-section delegation format** - TASK, EXPECTED OUTCOME, CONTEXT, CONSTRAINTS, MUST DO, MUST NOT DO, OUTPUT FORMAT
3. **Response synthesis mandatory** - Never show raw external output
4. **Role injection** - System prompts shape model behavior per task type

## Adding a New Provider

1. Check if CLI has native MCP support (like `codex mcp-server`)
2. If not, create `servers/your-provider-mcp/src/index.ts` following gemini-mcp pattern
3. Add to `config/providers.json` with CLI, MCP config, roles, strengths
4. Add role prompts to `prompts/` if needed
5. Update `commands/setup.md` to check for the new CLI

## Code Style

- No `any` without justification
- No `@ts-ignore` or `@ts-expect-error`
- Prefer Bun APIs over Node.js equivalents
- Pin dependency versions exactly in production
