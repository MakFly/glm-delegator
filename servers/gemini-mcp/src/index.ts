import { pathToFileURL } from "url";
import { resolve } from "path";
import { startServer } from "./server.js";

export async function runCli(
  argv: string[] = process.argv,
  moduleUrl: string = import.meta.url
) {
  const entry = argv[1] ? pathToFileURL(resolve(argv[1])).href : "";
  if (moduleUrl === entry) {
    await startServer();
  }
}

void runCli();
