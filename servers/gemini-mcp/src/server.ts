import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { spawn, ChildProcess } from "child_process";
import { readFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
export const DEFAULT_TIMEOUT = 10 * 60 * 1000; // 10 minutes
export const PROMPTS_DIR = join(__dirname, "../../prompts");

export const TOOLS = [
  {
    name: "gemini",
    description:
      "Run a Gemini session. Use for research, documentation, frontend code, multimodal analysis.",
    inputSchema: {
      type: "object" as const,
      properties: {
        prompt: {
          type: "string",
          description: "The task/question for Gemini",
        },
        model: {
          type: "string",
          description: "Model: gemini-2.5-pro, gemini-2.5-flash",
        },
        role: {
          type: "string",
          enum: ["oracle", "librarian", "frontend-engineer", "explore"],
          description: "Role prompt to auto-inject (optional)",
        },
        "approval-mode": {
          type: "string",
          enum: ["default", "auto_edit", "yolo"],
          description: "Approval mode for tool use",
        },
        sandbox: {
          type: "boolean",
          description: "Run in sandbox mode",
        },
        cwd: {
          type: "string",
          description: "Working directory",
        },
        timeout: {
          type: "number",
          description: "Timeout in ms (default: 600000)",
        },
      },
      required: ["prompt"],
    },
  },
  {
    name: "gemini-reply",
    description: "Continue an existing Gemini conversation",
    inputSchema: {
      type: "object" as const,
      properties: {
        sessionIndex: {
          type: "string",
          description: "Session index or 'latest'",
        },
        prompt: {
          type: "string",
          description: "Follow-up message",
        },
      },
      required: ["sessionIndex", "prompt"],
    },
  },
];

export function loadRolePrompt(
  role: string,
  promptsDir: string = PROMPTS_DIR
): string | null {
  const promptPath = join(promptsDir, `${role}.md`);
  if (existsSync(promptPath)) {
    return readFileSync(promptPath, "utf-8");
  }
  return null;
}

export function buildArgs(
  args: Record<string, unknown>,
  promptsDir: string = PROMPTS_DIR
): string[] {
  const cliArgs: string[] = [];

  if (args.model) cliArgs.push("-m", args.model as string);
  if (args["approval-mode"])
    cliArgs.push("--approval-mode", args["approval-mode"] as string);
  if (args.sandbox) cliArgs.push("--sandbox");
  if (args.cwd) cliArgs.push("--cwd", args.cwd as string);

  let prompt = args.prompt as string;
  if (args.role) {
    const rolePrompt = loadRolePrompt(args.role as string, promptsDir);
    if (rolePrompt) {
      prompt = `${rolePrompt}\n\n---\n\nTask:\n${prompt}`;
    }
  }

  cliArgs.push(prompt);
  return cliArgs;
}

export interface GeminiResult {
  output: string;
  exitCode: number;
  durationMs: number;
}

export type SpawnFn = typeof spawn;

export const activeProcesses = new Set<ChildProcess>();

export async function runGemini(
  args: string[],
  timeout: number,
  spawnFn: SpawnFn = spawn,
  processes: Set<ChildProcess> = activeProcesses
): Promise<GeminiResult> {
  const startTime = Date.now();
  let didTimeout = false;

  const proc = spawnFn("gemini", args, {
    stdio: ["ignore", "pipe", "pipe"],
  });

  processes.add(proc);

  const timeoutId = setTimeout(() => {
    didTimeout = true;
    proc.kill();
  }, timeout);

  const stdoutChunks: Buffer[] = [];
  const stderrChunks: Buffer[] = [];

  proc.stdout?.on("data", (chunk) => stdoutChunks.push(chunk));
  proc.stderr?.on("data", (chunk) => stderrChunks.push(chunk));

  try {
    const exitCode = await new Promise<number>((resolve, reject) => {
      proc.on("close", (code) => resolve(code ?? 0));
      proc.on("error", reject);
    });

    clearTimeout(timeoutId);
    processes.delete(proc);

    const stdout = Buffer.concat(stdoutChunks).toString();
    const stderr = Buffer.concat(stderrChunks).toString();
    const durationMs = Date.now() - startTime;

    if (didTimeout) {
      throw new Error(
        `Gemini timed out after ${timeout}ms` +
          (stdout ? `\nPartial output: ${stdout}` : "")
      );
    }

    if (exitCode !== 0) {
      throw new Error(
        `Gemini failed (exit code ${exitCode})` +
          (stderr ? `\nStderr: ${stderr}` : "") +
          (stdout ? `\nPartial output: ${stdout}` : "")
      );
    }

    return { output: stdout, exitCode, durationMs };
  } catch (error) {
    clearTimeout(timeoutId);
    processes.delete(proc);
    throw error;
  }
}

export function cleanup(processes: Set<ChildProcess> = activeProcesses) {
  for (const proc of processes) {
    try {
      proc.kill();
    } catch {
      // Process may have already exited
    }
  }
  processes.clear();
}

export function registerSignalHandlers(
  onCleanup: () => void = cleanup,
  processRef: NodeJS.Process = process
) {
  const handle = () => {
    onCleanup();
    processRef.exit(0);
  };

  processRef.on("SIGINT", handle);
  processRef.on("SIGTERM", handle);

  return () => {
    processRef.off("SIGINT", handle);
    processRef.off("SIGTERM", handle);
  };
}

export async function callToolHandler(
  request: {
    params: { name: string; arguments?: Record<string, unknown> | null };
  },
  runGeminiFn: (
    args: string[],
    timeout: number
  ) => Promise<GeminiResult> = runGemini
) {
  const { name, arguments: args } = request.params;

  if (!args) {
    return {
      content: [{ type: "text", text: "Error: No arguments provided" }],
      isError: true,
    };
  }

  try {
    if (name === "gemini") {
      const cliArgs = buildArgs(args as Record<string, unknown>);
      const timeout = (args.timeout as number | undefined) || DEFAULT_TIMEOUT;
      const result = await runGeminiFn(cliArgs, timeout);
      return { content: [{ type: "text", text: result.output }] };
    }

    if (name === "gemini-reply") {
      const result = await runGeminiFn(
        ["--resume", args.sessionIndex as string, args.prompt as string],
        DEFAULT_TIMEOUT
      );
      return { content: [{ type: "text", text: result.output }] };
    }

    return {
      content: [{ type: "text", text: `Unknown tool: ${name}` }],
      isError: true,
    };
  } catch (error) {
    return {
      content: [{ type: "text", text: `Error: ${(error as Error).message}` }],
      isError: true,
    };
  }
}

export function createServer(
  runGeminiFn: (
    args: string[],
    timeout: number
  ) => Promise<GeminiResult> = runGemini
) {
  const server = new Server(
    { name: "gemini-mcp-server", version: "1.0.0" },
    { capabilities: { tools: {} } }
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: TOOLS,
  }));

  server.setRequestHandler(CallToolRequestSchema, async (request) =>
    callToolHandler(request, runGeminiFn)
  );

  return server;
}

export async function startServer(
  createServerFn: () => Server = createServer,
  createTransport: () => StdioServerTransport =
    () => new StdioServerTransport(),
  registerSignals: () => void | (() => void) = registerSignalHandlers,
  log: (message: string) => void = console.error
) {
  const server = createServerFn();
  const transport = createTransport();
  registerSignals();
  await server.connect(transport);
  log("Gemini MCP server running on stdio");
}
