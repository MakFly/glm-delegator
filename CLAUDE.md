# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code plugin that provides GPT (via Codex CLI) as a native MCP tool for AI collaboration. Three roles: Worker (execution), Oracle (advisory), and Momus (plan validation).

## Development Commands

```bash
# Test plugin installation
/claude-delegator:setup

# Uninstall
/claude-delegator:configure
```

No build step, no dependencies. Uses Codex CLI's native MCP server.

## Architecture

### Sisyphus Model

Claude acts as orchestrator (Sisyphus) - delegates work to specialists, verifies results.

```
User Request → Claude Code → [Auto-detect role]
                                    ↓
              ┌─────────────────────┼─────────────────────┐
              ↓                     ↓                     ↓
           Worker               Oracle                 Momus
        (execution)           (advisory)          (plan review)
              ↓                     ↓                     ↓
     [sandbox: write]      [sandbox: read]       [sandbox: read]
              ↓                     ↓                     ↓
        [Verify]              [Synthesize]          [Report]
              ↓                     ↓                     ↓
         Report to user ←──────────┴──────────────────────┘
```

### Three-Role Model

| Role | Purpose | Sandbox | Trigger |
|------|---------|---------|---------|
| **Worker** | Execute tasks, modify files | `workspace-write` | Action verbs: add, fix, implement |
| **Oracle** | Strategic advice, analysis | `read-only` | Questions, tradeoffs, architecture |
| **Momus** | Plan validation, critique | `read-only` | "Review this plan" |

### Component Relationships

| Component | Location | Purpose |
|-----------|----------|---------|
| Rules | `rules/*.md` | Teaches when/how to delegate |
| Prompts | `prompts/*.md` | Shapes GPT behavior per role |
| Commands | `commands/*.md` | `/setup`, `/configure` |
| Config | `config/providers.json` | Provider configuration |

> Role prompts adapted from [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode)

## Key Design Decisions

1. **Native MCP only** - Codex has `codex mcp-server`, no wrapper needed
2. **Three distinct roles** - Worker executes, Oracle advises, Momus critiques
3. **Auto-detection** - Role determined by task type (action verbs vs questions)
4. **Verify then report** - Claude verifies Worker output before reporting
5. **Retry with codex-reply** - Up to 3 attempts before escalating failures

## When to Use Each Role

### Worker (Execution)
- "Add a section to the README"
- "Fix the failing test in auth.ts"
- "Implement the user export feature"
- "Update the config for production"

### Oracle (Advisory)
- "What are the tradeoffs of Redis vs in-memory?"
- "Review this architecture for scalability"
- "Is this authentication flow secure?"
- After 2+ failed fix attempts

### Momus (Plan Validation)
- "Review this migration plan"
- "Validate my approach before I start"
- "Is this implementation plan complete?"

## Plugin Structure

```
claude-delegator/
├── commands/
│   ├── setup.md       # /claude-delegator:setup
│   └── configure.md   # /claude-delegator:configure
├── rules/
│   ├── orchestration.md
│   ├── triggers.md
│   ├── model-selection.md
│   └── delegation-format.md
├── prompts/
│   ├── worker.md      # Executor prompt
│   ├── oracle.md      # Strategic advisor prompt
│   └── momus.md       # Plan reviewer prompt
└── config/
    └── providers.json
```
