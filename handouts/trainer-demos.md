# Five main demonstrations

Prepare course access once. Use the Explore route for Modules 1, 3, 4 and 5.
Module 2 includes Connected services within the Explore page. Each main demonstration ends with a visible
result, then learners try the nearby challenge. Technical details are optional.

## 1. An outing becomes an Excel file (5 minutes)

Open Tools that do useful things. Use the starting request. While it runs, explain
that the model chooses among a catalogue search, a quote function and a workbook
tool. Use the interactive browser comparison. Change the group size and update totals. The Excel download is optional.

Expected fixture values for eight people: pottery EUR 240, escape room EUR 200,
museum EUR 174. The agent may choose different valid options. Show one tool call
only if useful for explaining the mechanism. Stop when the file is usable.

Fallback: run the prepared workbook function in the Colab companion's runtime,
or open the labelled output produced by build/verify_exploration.py. Explain that
this is a direct tool call without a live model choosing it.

Optional trainer extension: ask a harness with a presentation tool for three
slides pitching the selected option. This is not a built-in browser lab feature.

## 2. A calendar appointment through MCP (5 minutes)

Open the Module 2 connection link. Choose Fitness, set Read & propose and press
Set connection. Run the starting request. Inspect the proposed time, approve it,
apply it and use Verify destination. Return through the site logo.

Explain host, client and server using what the class just saw. All diary data is
fictional. The MCP connection and saved appointment are real. Read-only access
and disconnection are optional variations, not four extra demos.

Rehearse the Thursday 10 September 2026 diary constraints. For a later course,
change the source fixture and prompt together. Review existing sandbox events
before rerunning because a prior appointment can change which slot is free.

Fallback: show the server tool list and a labelled prepared proposal from the
existing MCP notebook. Do not describe an offline example as a live connection.

## 3. Two specialists and a coordinator (5 minutes)

Open Agents working as a team. Run the starting cafe request with the two-agent
option. Show the creative and operations contributions, then the combined result.
Explain that the harness launches two separate tool-using agent loops concurrently
and makes a final synthesis call. The coordinator does not dynamically invent the
team. The interface exposes the actual contributions, time and reported tokens.

Ask the room what would change with an accessibility specialist. Let learners
try that variation and compare a solo run. Stop after the first combined menu.

Fallback: give two people the specialist roles using the five-item menu in the
runtime source, then have a third combine their suggestions. Label this as a human
simulation of the pattern, not a multi-agent model run.

## 4. An enforced limit and a human decision (5 minutes)

Open Guardrails and human decisions. Ask for EUR 80. The model may refuse directly
or call the tool and receive a rejection. Either is a valid live observation.
If it does not call the tool, use Try EUR 80 limit in the Colab companion to show
the deterministic boundary separately. This call makes no model request.

Request EUR 40. Show that the ledger remains empty while the proposal waits.
Reject it, ask again and approve the new proposal. The approval control records
the exact pending proposal once. There is no model approval tool and no money moves.

The EUR 50 limit is cumulative. Reset the fictional activity before repeating the
whole demonstration. Stop once the difference between rule and human choice is clear.

## 5. A calculator and a coding harness (7 minutes)

Run the calculator request in the mini harness. Open Tools used to show read,
edit and checks briefly, then try price 10 and quantity 2. Select the discount
requirement for learner practice. The mini harness evaluates a restricted arithmetic
expression, not arbitrary Python or shell commands.

For the product comparison, use [the harness sheet](harnesses.md) and the starter
ZIP. Prepare separate copies in the trainer's available Codex, Claude Code and/or
Antigravity CLI environments. Run the identical request in each available product,
show one permission or project-instruction control, and open the result. Allow
15–20 additional minutes for the comparison during Module 5.

If only one product is ready, demonstrate it live and discuss the others using
their official documentation. Do not improvise installations in participant time
or label documentation as a recorded product demonstration.

## Optional material

Use the old demo library only when it answers a question: prompt injection,
memory after a restart, a model judge or a role-specific evidence review. No
mandatory working brief, evidence worksheet, pilot proposal or multi-file export.

The larger selectable menu is in build/demo-menu.md. The demo launcher is notebooks/demos-exploration.ipynb. Student activities require no installed software.
