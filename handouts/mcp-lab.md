# Connected services with MCP

[Open the Colab lab](https://colab.research.google.com/github/FeikoWielsma/Using-AI-Agents/blob/main/notebooks/demo39-MCP_Connected_Services.ipynb).

This course service uses real MCP over HTTPS at `https://mcp.feikowielsma.nl/mcp`.
It provides fictional source records and a persistent task board and calendar.
It is not connected to a real employer, bank, customer system or Garmin account.

The notebook connects directly to Google Cloud Run at
`https://course-mcp-207474260976.europe-west4.run.app/mcp`. This removes the
instructor's home internet connection from the lab. The same credentials work.
The [access sheet](https://course-mcp-207474260976.europe-west4.run.app/access)
is also hosted there; `mcp.feikowielsma.nl/access` is its friendly address once
the DNS mapping and Google certificate are ready.

Your instructor supplies individual credentials for your sandbox. Add them in
Colab Secrets and enable Notebook access: `COURSE_MCP_TOKEN` for the connection,
`COURSE_MCP_REVIEW_TOKEN` for human review, and optionally `COURSE_MCP_READ_TOKEN`
for restricted access. Keep your existing `COURSE_API_KEY` for Qwen. Credentials
belong in Secrets, never in a prompt or shared document.

## The connection

The Colab interface is the host. Its MCP client discovers the server's tools and
their input schemas. Qwen can select a tool; the host makes the MCP call and
returns its result to Qwen. The server checks the credential and sandbox.
The model does not connect to arbitrary systems merely because a prompt names one.

Run six short demonstrations in the lab: discover tools, read records, propose a
change, approve and verify, restrict access, and disconnect. Each has a visible
result. Review is a separate host control: it is not an MCP tool the model can call.
This is how this course application enforces approval, not a universal MCP feature.

## Module 2 activity

Allow about ten minutes. Use the browser lab's Connected services activity, or the Colab controls above.

1. Connect with read-and-propose access and select Fitness. Ask for a free twenty-minute planning-review slot on Thursday 10 September 2026, after the fictional business trip.
2. Inspect the proposed time and title. Approve and apply it, or reject it and ask for a different slot.
3. Retrieve the calendar and locate the saved appointment. Disconnect when finished.

The diary and calendar are fictional. The task is scheduling a review; no Garmin connection or workout prescription is involved. An existing appointment can affect a repeated run.

If time permits, select Sales for an account follow-up or Programme for a dependency task. Save connection notes only if useful; no procedure or memory document is required.

If the service is unavailable, the trainer can show a prepared connection walkthrough, labelled as a recording or simulation. The other browser activities run independently.

Disconnecting closes this connection; it does not revoke a copied credential. Saved server records can survive browser and Colab restarts. The instructor controls credential revocation and course access.

For another MCP-capable application, use a remote Streamable HTTP connection and
the service URL above with an `Authorization: Bearer …` header, if that application
supports custom authenticated servers. Product subscriptions do not guarantee this
feature. Keep the separate review credential out of the agent's configuration;
use the Colab review controls for this service.
