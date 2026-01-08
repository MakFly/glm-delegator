import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "node",
    include: ["test/**/*.test.ts"],
  },
  coverage: {
    provider: "v8",
    all: true,
    include: ["src/**/*.ts"],
    reporter: ["text", "lcov"],
    thresholds: {
      lines: 100,
      statements: 100,
      functions: 100,
      branches: 100,
    },
  },
});
