# What you just watched

An agent chooses among the tools its host offers. The host executes the calls and
returns their results. Those tools can make spreadsheets, work with a calendar,
change code or delegate to another agent.

Try an ordinary request, look at the result, then ask for a useful change. Add
context when it matters. You do not need a formal working-brief document.

MCP provides a common connection between a host and a server. The server exposes
capabilities. Credentials, host policy and server checks determine what happens.
Connecting does not grant every permission or make human approval automatic.

Multiple agents can divide a task. In our cafe example, two specialists run in
separate contexts at the same time, then a coordinator combines their output.
Compare with one agent: extra agents can add perspectives, time and cost.

Guardrails can restrict tools or reject arguments. Our refund tool enforces its
limit in code. A separate human control approves or rejects the pending action.
The model cannot approve its own refund.

A coding harness supplies the surrounding tools, context, permissions and
execution environment. Read the [harness comparison](harnesses.md), then try the
[starter](../data/harness-starter.zip) in a product you already have.
