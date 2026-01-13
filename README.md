# GLM Delegator

> GLM-4.7 expert subagents for Claude Code — A fork of [claude-delegator](https://github.com/jarrodwatts/claude-delegator) adapted for Z.AI's GLM models

GLM expert subagents for Claude Code. Five specialists that can analyze AND implement—architecture, security, code review, and more.

[![License](https://img.shields.io/github/license/MakFly/glm-delegator?v=2)](LICENSE)
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## What is GLM Delegator?

Claude gains a team of GLM-4.7 specialists via MCP. Each expert has a distinct specialty and can advise OR implement.

| What You Get | Why It Matters |
|--------------|----------------|
| **5 domain experts** | Right specialist for each problem type |
| **Dual mode** | Experts can analyze (read-only) or implement (write) |
| **Auto-routing** | Claude detects when to delegate based on your request |
| **Synthesized responses** | Claude interprets GLM output, never raw passthrough |
| **Multilingual** | Code Review supports EN/FR/CN (中文) |

### The Experts

| Expert | What They Do | Example Triggers |
|--------|--------------|------------------|
| **Architect** | System design, tradeoffs, complex debugging | "How should I structure this?" / "What are the tradeoffs?" |
| **Plan Reviewer** | Validate plans before you start | "Review this migration plan" / "Is this approach sound?" |
| **Scope Analyst** | Catch ambiguities early | "What am I missing?" / "Clarify the scope" |
| **Code Reviewer** | Find bugs, improve quality (EN/FR/CN) | "Review this PR" / "What's wrong with this?" |
| **Security Analyst** | Vulnerabilities, threat modeling | "Is this secure?" / "Harden this endpoint" |

## Differences from claude-delegator

| Feature | claude-delegator | glm-delegator |
|---------|------------------|---------------|
| Backend | Codex GPT-5.2 | GLM-4.7 (Z.AI) |
| API | OpenAI Codex CLI | Custom MCP server with Z.AI Anthropic-compatible API |
| Code Review | English only | **EN/FR/CN multilingual** |
| Security | OWASP | OWASP + Chinese MLPS standards |
| License | MIT | MIT |

## Install

### Prerequisites

- **Python 3.8+** for the MCP server
- **Z.AI API Key** - Get one from [Z.AI Platform](https://platform.z.ai/)
- **httpx** library - `pip install -r requirements.txt`

### Step 1: Install Dependencies

```bash
cd glm-delegator
pip install -r requirements.txt
```

### Step 2: Configure API Key

Set your Z.AI API key as an environment variable:

```bash
export GLM_API_KEY="your_z_ai_api_key_here"
# Or use Z_AI_API_KEY (also supported)
export Z_AI_API_KEY="your_z_ai_api_key_here"
```

For persistent configuration, add to your `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export GLM_API_KEY="your_z_ai_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### Step 3: Register MCP Server

Add to `~/.claude.json` (or `~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "glm-delegator": {
      "command": "python3",
      "args": ["/path/to/glm-delegator/glm_mcp_server.py"],
      "env": {
        "GLM_API_KEY": "your_z_ai_api_key_here"
      }
    }
  }
}
```

### Step 4: Restart Claude Code

Restart Claude Code to load the MCP server.

### Alternative: Using the setup command

Inside Claude Code, run:

```
/glm-delegator:setup
```

This will guide you through the installation process.

## Usage

Once installed, delegation happens automatically. Claude Code will detect when to delegate based on your request.

### Explicit Delegation

You can also explicitly request GLM expert help:

```
"Ask GLM to review this authentication flow"
"Use GLM architect to design this API"
"Have GLM security analyst review this code"
```

### Manual Tool Call

You can call the MCP tools directly:

```typescript
// Advisory mode (analysis only)
mcp__glm-delegator__glm_architect({
  task: "Analyze tradeoffs between Redis and in-memory caching",
  mode: "advisory",
  context: "Building a session store for a Node.js app"
})

// Implementation mode (make changes)
mcp__glm-delegator__glm_code_reviewer({
  task: "Fix the SQL injection vulnerability in user.ts",
  mode: "implementation",
  files: ["src/routes/user.ts"]
})
```

## How It Works

```
You: "Is this authentication flow secure?"
                    ↓
Claude: [Detects security question → selects Security Analyst]
                    ↓
        ┌─────────────────────────────┐
        │  mcp__glm-delegator__glm_   │
        │  security_analyst           │
        │  → Security Analyst prompt  │
        │  → GLM-4.7 analyzes your    │
        │    code via Z.AI API        │
        └─────────────────────────────┘
                    ↓
Claude: "Based on the analysis, I found 3 issues..."
        [Synthesizes response, applies judgment]
```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GLM_API_KEY` | Yes* | - | Your Z.AI API key |
| `Z_AI_API_KEY` | Yes* | - | Alternative to GLM_API_KEY |
| `GLM_BASE_URL` | No | `https://api.z.ai/api/anthropic` | Z.AI API endpoint |
| `GLM_MODEL` | No | `glm-4.7` | GLM model to use |

*Either `GLM_API_KEY` or `Z_AI_API_KEY` is required.

### Operating Modes

Every expert supports two modes based on the task:

| Mode | Use When |
|------|----------|
| **Advisory** | Analysis, recommendations, reviews |
| **Implementation** | Making changes, fixing issues |

Claude automatically selects the mode based on your request.

## Customizing Expert Prompts

Expert prompts are embedded in `glm_mcp_server.py` (EXPERT_PROMPTS dictionary). Each follows the same structure:
- Role definition and context
- Advisory vs Implementation modes
- Response format guidelines
- When to invoke / when NOT to invoke

Edit the `EXPERT_PROMPTS` dictionary in `glm_mcp_server.py` to customize expert behavior for your workflow.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MCP server not found | Restart Claude Code after configuration |
| GLM authentication failed | Verify your API key is correct and active |
| Tool not appearing | Check `~/.claude.json` has glm-delegator entry |
| Expert not triggered | Try explicit: "Ask GLM to review this architecture" |
| Python not found | Ensure Python 3.8+ is in your PATH |

### Debug Mode

To see MCP server logs, check stderr output or run manually:

```bash
python3 glm_mcp_server.py 2>&1
```

## Development

```bash
git clone https://github.com/MakFly/glm-delegator
cd glm-delegator

# Install dependencies
pip install -r requirements.txt

# Test locally
python3 glm_mcp_server.py
```

## Architecture

### Components

| Component | Purpose |
|-----------|---------|
| `glm_mcp_server.py` | MCP server implementation with GLM API integration |
| `prompts/*.md` | Expert personality definitions (for reference) |
| `rules/*.md` | Delegation rules and triggers (for reference) |
| `.claude-plugin/plugin.json` | Plugin metadata |

### API Flow

```
Claude Code → MCP Request → glm_mcp_server.py
                                ↓
                        Z.AI API (Anthropic-compatible)
                                ↓
                            GLM-4.7
                                ↓
                        Response → Claude Code
```

## Acknowledgments

- Based on [claude-delegator](https://github.com/jarrodwatts/claude-delegator) by [Jarrod Watts](https://github.com/jarrodwatts)
- Expert prompts adapted from [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) by [@code-yeongyu](https://github.com/code-yeongyu)
- Uses Z.AI's [Anthropic-compatible API](https://docs.z.ai/devpack/mcp)

## License

MIT — see [LICENSE](LICENSE)
