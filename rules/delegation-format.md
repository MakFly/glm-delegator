# Delegation Prompt Templates

When delegating to external models, use these structured templates.

## The 7-Section Format (MANDATORY)

Every delegation prompt MUST include these sections:

```
1. TASK: [One sentence - atomic, specific goal]

2. EXPECTED OUTCOME: [What success looks like]

3. CONTEXT:
   - Current approach: [what's been tried]
   - Relevant code: [paths or snippets]
   - Background: [why this is needed]

4. CONSTRAINTS:
   - Technical: [versions, dependencies]
   - Patterns: [existing conventions to follow]
   - Limitations: [what cannot change]

5. MUST DO:
   - [Requirement 1]
   - [Requirement 2]
   - [Be exhaustive]

6. MUST NOT DO:
   - [Forbidden action 1]
   - [Forbidden action 2]
   - [Anticipate rogue behavior]

7. OUTPUT FORMAT:
   - [How to structure response]
   - [What sections to include]
```

---

## Oracle (GPT) Template

For architecture, debugging, code review, security analysis.

```markdown
TASK: [Analyze/Review/Debug] [specific thing] to [achieve outcome].

EXPECTED OUTCOME: Clear recommendation with rationale, concerns identified, actionable next steps.

CONTEXT:
- Current approach: We're using [pattern/architecture] because [reason].
- Relevant code:
  ```[language]
  [code snippet or file:line reference]
  ```
- Problem: [What's not working or what decision needs to be made]
- Prior attempts: [What's been tried, if applicable]

CONSTRAINTS:
- Must work with [framework/library] version [X]
- Must maintain backward compatibility with [existing feature]
- Cannot change [protected component/API]
- Performance budget: [if applicable]

MUST DO:
- Analyze step by step, showing reasoning
- Consider edge cases and failure modes
- Identify potential issues before they become problems
- Provide concrete, implementable recommendations
- Cite specific code locations when relevant

MUST NOT DO:
- Make assumptions about code you haven't seen
- Suggest solutions that violate stated constraints
- Provide vague or generic advice
- Ignore error handling or edge cases

OUTPUT FORMAT:
1. Summary (2-3 sentences)
2. Analysis (step-by-step reasoning)
3. Concerns (if any)
4. Recommendation (specific, actionable)
5. Implementation notes (if code changes needed)
```

---

## Momus (GPT) Template

For plan review, validation, and critique before implementation.

```markdown
TASK: Review [plan/approach/design] for [project/feature] before implementation.

EXPECTED OUTCOME: Honest critique identifying gaps, risks, and improvements.

CONTEXT:
- Plan summary: [What's being proposed]
- Goals: [What this is trying to achieve]
- Constraints: [Technical/business limitations]
- Timeline: [If relevant]

CONSTRAINTS:
- Must work within [existing architecture]
- Cannot break [protected functionality]
- Budget/time constraints: [if applicable]

MUST DO:
- Identify gaps, missing edge cases, and overlooked requirements
- Point out risks and potential failure modes
- Suggest concrete improvements
- Be direct and honest, even if critical
- Prioritize feedback by importance

MUST NOT DO:
- Rubber-stamp plans without real analysis
- Provide vague or non-actionable feedback
- Ignore obvious problems to be polite
- Add unnecessary complexity

OUTPUT FORMAT:
1. Overall assessment (go/no-go/needs work)
2. Critical issues (must fix before proceeding)
3. Risks identified (with mitigation suggestions)
4. Improvements (nice-to-have enhancements)
5. Questions (clarifications needed)
```

---

## Worker (GPT) Template

For implementation tasks - executing code changes directly.

```markdown
TASK: [Action verb] [specific thing] in [location].

EXPECTED OUTCOME: [Thing] is [done/added/fixed/updated] and verified working.

WORKING DIRECTORY: [absolute path to cwd]

FILES TO MODIFY: [specific files if known, otherwise "discover as needed"]

CONTEXT:
- Purpose: [Why this change is needed]
- Existing patterns: [Relevant conventions in this codebase]
- Related files: [Files to reference for patterns/context]

REQUIREMENTS:
- [Specific requirement 1]
- [Specific requirement 2]

VERIFICATION:
- [How to verify: run tests, build, lint, etc.]
- [Expected outcome of verification]

CONSTRAINTS:
- Only modify files related to this task
- Follow existing code patterns in the project
- Report all files you modify
- Do not refactor unrelated code
```

### Worker Template Example

```markdown
TASK: Add installation section to README.md.

EXPECTED OUTCOME: README has clear installation instructions with npm and yarn commands.

WORKING DIRECTORY: /Users/dev/my-project

FILES TO MODIFY: README.md

CONTEXT:
- Purpose: Users need to know how to install the package
- Existing patterns: README uses ## headers, has Overview section already
- Related files: package.json (for package name)

REQUIREMENTS:
- Include npm install command
- Include yarn add command
- Place after Overview section

VERIFICATION:
- Confirm markdown renders correctly
- Verify package name matches package.json

CONSTRAINTS:
- Only modify README.md
- Match existing markdown style
- Report the file modification
```

---

## Quick Reference

| Role | Model | Template Focus |
|------|-------|----------------|
| Worker | GPT | Execute task, modify files, verify results |
| Oracle | GPT | Deep analysis, tradeoffs, recommendations |
| Momus | GPT | Plan review, critique, validation |

---

## Anti-Patterns

### Don't Do This

```
"Can you help me with this code?"
```

### Do This Instead

```
TASK: Review this authentication middleware for security vulnerabilities.

EXPECTED OUTCOME: List of vulnerabilities with severity ratings and fixes.

CONTEXT:
- Current code:
  [code snippet]
- This handles: JWT validation for API routes
- Deployed to: Production, ~10k requests/day

...
```

The structured format ensures:
- External model has full context
- No ambiguity in what's expected
- Consistent, actionable responses
- Easier to verify the output meets requirements
