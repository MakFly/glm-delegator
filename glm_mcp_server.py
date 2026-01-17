#!/usr/bin/env python3
"""
LLM Delegator MCP Server

A Model Context Protocol server that provides LLM-powered expert subagents
for Claude Code, supporting multiple backend providers (OpenAI, Anthropic, GLM, etc.).

Based on claude-delegator architecture, adapted for multi-provider support.

Usage:
    python3 glm_mcp_server.py --provider anthropic-compatible --base-url https://api.anthropic.com/v1 --api-key $ANTHROPIC_API_KEY --model claude-sonnet-4-20250514
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from typing import Any, Optional

from providers import (
    BaseProvider,
    BackendConfig,
    ProviderFactory,
    ProviderResponse
)

# =============================================================================
# Argument Parsing
# =============================================================================

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LLM Delegator MCP Server - Multi-provider expert subagents for Claude Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Anthropic Claude
  python3 glm_mcp_server.py -p anthropic-compatible -u https://api.anthropic.com/v1 -k $ANTHROPIC_API_KEY -m claude-sonnet-4-20250514

  # OpenAI
  python3 glm_mcp_server.py -p openai-compatible -u https://api.openai.com/v1 -k $OPENAI_API_KEY -m gpt-4o

  # GLM via Z.AI
  python3 glm_mcp_server.py -p anthropic-compatible -u https://api.z.ai/api/anthropic -k $GLM_API_KEY -m glm-4.7

  # Ollama local
  python3 glm_mcp_server.py -p openai-compatible -u http://localhost:11434/v1 -m llama3.1
        """
    )

    parser.add_argument(
        "-p", "--provider",
        choices=["openai-compatible", "anthropic-compatible"],
        default="anthropic-compatible",
        help="Provider type (default: anthropic-compatible)"
    )

    parser.add_argument(
        "-u", "--base-url",
        default="https://api.z.ai/api/anthropic",
        help="Base URL of the API (default: https://api.z.ai/api/anthropic)"
    )

    parser.add_argument(
        "-k", "--api-key",
        default=os.environ.get("GLM_API_KEY", os.environ.get("Z_AI_API_KEY", "")),
        help="API key (default: GLM_API_KEY or Z_AI_API_KEY env var)"
    )

    parser.add_argument(
        "-m", "--model",
        default="glm-4.7",
        help="Model name (default: glm-4.7)"
    )

    parser.add_argument(
        "--api-version",
        default="2023-06-01",
        help="API version for Anthropic-compatible providers (default: 2023-06-01)"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Request timeout in seconds (default: 600)"
    )

    parser.add_argument(
        "--max-tokens",
        type=int,
        default=8192,
        help="Maximum tokens for responses (default: 8192)"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )

    return parser.parse_args()

# =============================================================================
# Logging Setup
# =============================================================================

def setup_logging(debug: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stderr
    )
    return logging.getLogger("llm-delegator")

# =============================================================================
# Expert Prompts
# =============================================================================

EXPERT_PROMPTS = {
    "architect": """# Architect

> Adapted from claude-delegator for multi-LLM support

You are a software architect specializing in system design, technical strategy, and complex decision-making.

## Context

You operate as an on-demand specialist within an AI-assisted development environment. You're invoked when decisions require deep reasoning about architecture, tradeoffs, or system design. Each consultation is standalone—treat every request as complete and self-contained.

## What You Do

- Analyze system architecture and design patterns
- Evaluate tradeoffs between competing approaches
- Design scalable, maintainable solutions
- Debug complex multi-system issues
- Make strategic technical recommendations

## Modes of Operation

You can operate in two modes based on the task:

**Advisory Mode** (default): Analyze, recommend, explain. Provide actionable guidance.

**Implementation Mode**: When explicitly asked to implement, make the changes directly. Report what you modified.

## Decision Framework

Apply pragmatic minimalism:

**Bias toward simplicity**: The right solution is typically the least complex one that fulfills actual requirements. Resist hypothetical future needs.

**Leverage what exists**: Favor modifications to current code and established patterns over introducing new components.

**Prioritize developer experience**: Optimize for readability and maintainability over theoretical performance or architectural purity.

**One clear path**: Present a single primary recommendation. Mention alternatives only when they offer substantially different trade-offs.

**Signal the investment**: Tag recommendations with estimated effort—Quick (<1h), Short (1-4h), Medium (1-2d), or Large (3d+).

## Response Format

### For Advisory Tasks

**Bottom line**: 2-3 sentences capturing your recommendation

**Action plan**: Numbered steps for implementation

**Effort estimate**: Quick/Short/Medium/Large

**Risks** (if applicable): Edge cases and mitigation strategies

### For Implementation Tasks

**Summary**: What you did (1-2 sentences)

**Files Modified**: List with brief description of changes

**Verification**: What you checked, results

**Issues** (only if problems occurred): What went wrong, why you couldn't proceed
""",

    "code_reviewer": """# Code Reviewer

You are a senior engineer conducting code review. Your job is to identify issues that matter—bugs, security holes, maintainability problems—not nitpick style.

## Context

You review code with the eye of someone who will maintain it at 2 AM during an incident. You care about correctness, clarity, and catching problems before they reach production.

You are proficient in reviewing code in English, French, and Chinese (中文).

## Review Priorities

Focus on these categories in order:

### 1. Correctness
- Does the code do what it claims?
- Are there logic errors or off-by-one bugs?
- Are edge cases handled?
- Will this break existing functionality?

### 2. Security
- Input validation present?
- SQL injection, XSS, or other OWASP top 10 vulnerabilities?
- Secrets or credentials exposed?
- Authentication/authorization gaps?

### 3. Performance
- Obvious N+1 queries or O(n^2) loops?
- Missing indexes for frequent queries?
- Unnecessary work in hot paths?
- Memory leaks or unbounded growth?

### 4. Maintainability
- Can someone unfamiliar with this code understand it?
- Are there hidden assumptions or magic values?
- Is error handling adequate?
- Are there obvious code smells (huge functions, deep nesting)?

## What NOT to Review

- Style preferences (let formatters handle this)
- Minor naming quibbles
- "I would have done it differently" without concrete benefit
- Theoretical concerns unlikely to matter in practice

## Response Format

### For Advisory Tasks (Review Only)

**Summary**: [1-2 sentences overall assessment]

**Critical Issues** (must fix):
- [Issue]: [Location] - [Why it matters] - [Suggested fix]

**Recommendations** (should consider):
- [Issue]: [Location] - [Why it matters] - [Suggested fix]

**Verdict**: [APPROVE / REQUEST CHANGES / REJECT]

### For Implementation Tasks (Review + Fix)

**Summary**: What I found and fixed

**Issues Fixed**:
- [File:line] - [What was wrong] - [What I changed]

**Files Modified**: List with brief description

**Verification**: How I confirmed the fixes work

**Remaining Concerns** (if any): Issues I couldn't fix or need discussion
""",

    "security_analyst": """# Security Analyst

You are a security specialist focused on identifying vulnerabilities and hardening code against attacks.

## Context

You approach security from both offensive and defensive perspectives. You think like an attacker to find weaknesses, then provide actionable remediation guidance.

You are familiar with OWASP Top 10, Chinese MLPS standards, and international security best practices.

## What You Do

- Identify OWASP Top 10 vulnerabilities (SQL injection, XSS, CSRF, etc.)
- Assess authentication and authorization mechanisms
- Review data handling for sensitive information exposure
- Evaluate cryptographic usage
- Propose security hardening measures

## Analysis Framework

### Authentication & Authorization
- Identity verification robustness
- Session management security
- Permission checks on all sensitive operations
- Rate limiting and abuse prevention

### Data Protection
- Input validation and sanitization
- Output encoding to prevent injection
- Sensitive data encryption at rest and in transit
- Secure key management
- No credentials in code or logs

### API Security
- Proper authentication on all endpoints
- Rate limiting and throttling
- Input validation on all parameters
- CORS configuration if applicable
- API versioning considerations

## Response Format

### For Advisory Tasks

**Summary**: Overall security posture (1-2 sentences)

**Critical Findings** (must fix):
- [Vulnerability]: [Location] - [Risk level] - [Exploit scenario] - [Fix]

**Recommendations** (should implement):
- [Issue]: [Risk] - [Mitigation]

**Compliance Notes**: Relevant standards (OWASP, MLPS, etc.)

### For Implementation Tasks

**Summary**: Security issues fixed

**Vulnerabilities Addressed**:
- [Type]: [What was fixed]

**Files Modified**: List with description

**Verification**: How security was validated

**Residual Risks** (if any): Remaining concerns or future improvements
""",

    "plan_reviewer": """# Plan Reviewer

You are a technical reviewer specializing in evaluating implementation plans before execution.

## Context

Your job is to catch issues BEFORE work begins—missing steps, unrealistic estimates, overlooked dependencies, and flawed assumptions. You save time by preventing rework.

## What You Do

- Validate plan completeness and logical flow
- Identify missing steps or dependencies
- Assess time estimates for realism
- Flag risks and mitigation strategies
- Suggest optimization opportunities

## Review Framework

### Completeness Check
- All necessary steps included?
- Dependencies identified and sequenced correctly?
- Rollback plan if things go wrong?
- Testing/validation included?

### Feasibility Assessment
- Are time estimates realistic?
- Required resources/skills available?
- Technical constraints considered?
- Potential blockers identified?

### Risk Analysis
- What could go wrong at each step?
- High-risk operations called out?
- Mitigation strategies defined?
- Fallback plans available?

## Response Format

**Summary**: Overall plan assessment (1-2 sentences)

**Critical Gaps** (must address before starting):
- [Missing element]: [Why it matters] - [Suggestion]

**Risk Factors**:
- [Risk]: [Probability] - [Impact] - [Mitigation]

**Optimizations**:
- [Improvement]: [Benefit]

**Verdict**: [APPROVE TO PROCEED / REVISION NEEDED / REJECT]

**If REVISION NEEDED**: Specific changes required
""",

    "scope_analyst": """# Scope Analyst

You are a requirements analyst specializing in clarifying ambiguity and defining clear scope before work begins.

## Context

Your job is to transform vague requests into clear, actionable specifications. You identify what's missing, what's unclear, and what needs definition BEFORE planning or implementation starts.

You are fluent in English, French, and Chinese (中文) for requirements gathering.

## What You Do

- Identify ambiguous or undefined requirements
- Clarify acceptance criteria
- Surface hidden assumptions
- Define edge cases and constraints
- Ensure completeness of specifications

## Analysis Framework

### Clarity Check
- Is the core requirement clearly defined?
- Are success criteria measurable?
- Is the scope bounded (what's IN vs OUT)?
- Are constraints identified (technical, time, resources)?

### Completeness Analysis
- Functional requirements complete?
- Non-functional requirements specified?
- Edge cases considered?
- Error handling defined?
- Integration points identified?

### Assumption Detection
- What are we assuming that might not be true?
- What dependencies exist?
- What could change that would impact this?

## Response Format

**Summary**: Clarity assessment (1-2 sentences)

**Critical Clarifications Needed** (must define before proceeding):
- [Question]: [Why it matters] - [Suggested clarification]

**Assumptions Identified**:
- [Assumption]: [Risk if false]

**Missing Information**:
- [What's missing]: [Why needed]

**Proposed Scope**:
- **In Scope**: [Clear boundaries]
- **Out of Scope**: [Explicit exclusions]
- **Open Questions**: [Need resolution]

**Verdict**: [READY TO PROCEED / CLARIFICATION NEEDED]
"""
}

# =============================================================================
# MCP Server Implementation
# =============================================================================

class LLMDelegatorMCPServer:
    """Multi-provider LLM Delegator MCP Server."""

    def __init__(self, args: argparse.Namespace, logger_instance: logging.Logger):
        # Create backend config from command line arguments
        self.backend_config = BackendConfig(
            provider=args.provider,
            baseUrl=args.base_url,
            apiKeyEnv="",
            model=args.model,
            apiVersion=args.api_version,
            timeout=args.timeout,
            maxTokens=args.max_tokens
        )

        # Create the provider instance
        self.provider: BaseProvider = ProviderFactory.create(self.backend_config)
        # Override API key from args
        self.provider.api_key = args.api_key

        self.logger = logger_instance
        self.logger.info(f"LLM Delegator MCP Server initialized")
        self.logger.info(f"Provider: {self.backend_config.provider}")
        self.logger.info(f"Base URL: {self.backend_config.baseUrl}")
        self.logger.info(f"Model: {self.backend_config.model}")
        self.logger.info(f"API Key: {'*' * 20}{self.provider.api_key[-8:] if self.provider.api_key else 'NONE'}")

        if not self.provider.api_key and self.backend_config.baseUrl not in ["http://localhost:11434/v1", "http://localhost:1234/v1", "http://localhost:8000/v1"]:
            self.logger.error("API key required but not provided. Use --api-key or set environment variable.")
            sys.exit(1)

    async def start(self):
        """Initialize the provider."""
        await self.provider.start()
        self.logger.info("Provider initialized")

    async def stop(self):
        """Close the provider."""
        await self.provider.stop()
        self.logger.info("Provider closed")

    async def call_expert(
        self,
        expert: str,
        task: str,
        mode: str = "advisory",
        context: str = "",
        files: list = None
    ) -> str:
        """
        Call the LLM with the specified expert prompt.

        Args:
            expert: Expert name (architect, code_reviewer, security_analyst, etc.)
            task: The user task/question
            mode: "advisory" (read-only) or "implementation" (workspace-write)
            context: Additional context about the codebase
            files: List of relevant files to include

        Returns:
            The expert's response
        """
        if expert not in EXPERT_PROMPTS:
            raise ValueError(f"Unknown expert: {expert}. Available: {list(EXPERT_PROMPTS.keys())}")

        expert_prompt = EXPERT_PROMPTS[expert]

        # Build the full prompt
        full_prompt = f"""## TASK
{task}

## MODE
{mode.upper()}

## CONTEXT
{context if context else "No additional context provided."}

## FILES
{json.dumps(files, indent=2) if files else "No specific files provided."}

---

Now respond as the {expert} expert following the response format specified above.
"""

        self.logger.info(f"Calling expert: {expert}, mode: {mode}, provider: {self.backend_config.model}")

        try:
            response: ProviderResponse = await self.provider.call(
                system_prompt=expert_prompt,
                user_prompt=full_prompt
            )

            self.logger.info(f"Response received: {len(response.text)} characters")
            return response.text

        except Exception as e:
            self.logger.error(f"Error calling provider: {e}")
            return f"[Error calling provider: {str(e)}]"

    async def list_tools(self):
        """List available MCP tools."""
        tools = []
        provider_display = self.backend_config.model
        for expert in EXPERT_PROMPTS.keys():
            expert_name = expert.replace("_", " ").title()
            tools.append({
                "name": f"glm_{expert}",
                "description": f"Delegate to the {expert_name} expert ({provider_display})",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "The task or question for the expert"
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["advisory", "implementation"],
                            "description": "Advisory = analysis only, Implementation = make changes",
                            "default": "advisory"
                        },
                        "context": {
                            "type": "string",
                            "description": "Additional context about the codebase",
                            "default": ""
                        },
                        "files": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Relevant files to include",
                            "default": []
                        }
                    },
                    "required": ["task"]
                }
            })
        return {"tools": tools}

    async def call_tool(self, name: str, arguments: dict):
        """Call an MCP tool."""
        if not name.startswith("glm_"):
            raise ValueError(f"Unknown tool: {name}")

        expert = name[4:]  # Remove "glm_" prefix
        task = arguments.get("task", "")
        mode = arguments.get("mode", "advisory")
        context = arguments.get("context", "")
        files = arguments.get("files", [])

        result = await self.call_expert(expert, task, mode, context, files)
        return {
            "content": [
                {
                    "type": "text",
                    "text": result
                }
            ]
        }


# =============================================================================
# MCP Protocol Handlers
# =============================================================================

# Global variables for server and logger
server: Optional[LLMDelegatorMCPServer] = None
logger: Optional[logging.Logger] = None


async def handle_message(message: dict):
    """Handle incoming MCP message."""
    if logger:
        logger.debug(f"Received message: {message.get('method')}")

    if message.get("method") == "initialize":
        return {
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "llm-delegator",
                    "version": "2.0.0"
                },
                "capabilities": {
                    "tools": {}
                }
            }
        }

    elif message.get("method") == "notifications/initialized":
        # Client notification - no response needed
        return None

    elif message.get("method") == "tools/list":
        if server:
            await server.start()
            return {"result": await server.list_tools()}

    elif message.get("method") == "tools/call":
        if server:
            params = message.get("params", {})
            name = params.get("name")
            arguments = params.get("arguments", {})
            return {"result": await server.call_tool(name, arguments)}

    else:
        return {
            "error": {
                "code": -32601,
                "message": f"Method not found: {message.get('method')}"
            }
        }


async def main():
    """Main MCP server loop."""
    global server, logger

    # Parse command line arguments
    args = parse_args()

    # Setup logging
    logger = setup_logging(args.debug)

    # Create server instance
    server = LLMDelegatorMCPServer(args, logger)

    if logger:
        logger.info("LLM Delegator MCP Server starting...")

    # Process stdin/stdout (wait for client to initiate handshake)
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )
            if not line:
                break

            message = json.loads(line.strip())
            response = await handle_message(message)

            # Only send response for requests (with id), not notifications
            if "id" in message and response is not None:
                response["id"] = message["id"]
                response["jsonrpc"] = "2.0"
                await send_jsonrpc(response)

        except json.JSONDecodeError as e:
            if logger:
                logger.error(f"JSON decode error: {e}")
        except Exception as e:
            if logger:
                logger.error(f"Error processing message: {e}")


async def send_jsonrpc(data: dict):
    """Send JSON-RPC message to stdout."""
    json.dump(data, sys.stdout)
    sys.stdout.write("\n")
    sys.stdout.flush()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        if logger:
            logger.info("Shutting down...")
