# Coding agents and their harnesses

A harness is the application around the model. It manages context, provides
tools, executes calls and controls access. A coding harness can read a project,
edit it and run its commands. The course mini harness demonstrates that loop
using a restricted arithmetic language. It is not an implementation of a vendor product.

| Product | Company | What to explore |
| --- | --- | --- |
| Codex | OpenAI | Project tasks, changes, tools and permission controls |
| Claude Code | Anthropic | The agent loop, project context and specialised subagents |
| Antigravity CLI | Google | Terminal work, MCP connections and sandbox controls |

Documentation checked 8 September 2026. Features and account access can change.
Use the trainer's installed products for the comparison. Students install no proprietary software. The course code does
not provide a vendor subscription.

## The same task in each product

For the trainer demonstration, extract a fresh copy of [calculator-starter.zip](../data/harness-starter.zip)
into a separate folder for each product. Open that folder in the chosen harness.
The trainer handles installation and authentication before class.

> Read PROJECT-INSTRUCTIONS.txt. Repair the calculator so total(price, quantity)
> returns price multiplied by quantity. Keep the function name, use no dependencies
> and run the checks.

Then request one change:

> Apply a 10% discount when the subtotal is at least EUR 50. Extend the checks for
> just below, exactly at and above the threshold. Keep smaller orders unchanged.
> Run the checks again.

Watch where the product shows its work, how it handles permissions and how you
can correct it. Note the product version, model and settings. A single classroom
run illustrates the experience; it does not rank model quality.

Optional: ask for a simple local browser interface. Open it and try an order.

## Instructions, skills and connections

Project instructions supply persistent guidance. For example, Codex documents
AGENTS.md, while Claude Code uses CLAUDE.md. In this comparison, the explicit
request to read PROJECT-INSTRUCTIONS.txt avoids depending on automatic discovery.

A skill packages reusable instructions. An MCP connection provides access to a
server's capabilities. A subagent receives a focused task in another context.
The host controls which of these are available. A permission prompt and a sandbox
serve different purposes: one asks for a decision, the other restricts execution.

## Official references

- [Codex CLI: tasks, tools, delegation and MCP](https://learn.chatgpt.com/docs/codex/cli)
- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [MCP servers with Antigravity CLI](https://antigravity.google/docs/cli/features/)
- [Sandboxing in Antigravity CLI](https://antigravity.google/docs/cli/sandbox/)
- [MCP architecture](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture)
