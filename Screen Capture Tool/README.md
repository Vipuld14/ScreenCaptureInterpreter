# Screen Capture Tool

Capture an image of a screen and get a clear, AI-generated explanation of what's on it.

This program is a thin capture client: it grabs the screen and hands the image to Claude. The reading, classifying, and explaining is delegated to the **Claude Agent SDK** — we don't build the processing logic ourselves. See `REQUIREMENTS.md` for the full plan.

This repo is currently at **Milestone 1 — Foundation**: a working dev environment that can talk to the model through the Agent SDK.

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install the Claude Code runtime (the Agent SDK drives it under the hood). Requires Node.js:

   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

4. Authenticate. This project uses your **Claude subscription** (Pro/Max/Team/Enterprise) — no API key:

   ```bash
   claude        # then complete the login prompt in your browser
   ```

   The SDK reuses those saved credentials. Subscription usage draws from your normal plan limits.

   > Do **not** set `ANTHROPIC_API_KEY` for this route — if it's set, the SDK bills pay-as-you-go through the API instead of your subscription. (The `.env` / API-key path remains available as an alternative; `.env` is gitignored and must never be committed.)

## Run the connectivity test

```bash
python hello_agent.py
```

If everything is set up correctly, you'll see a short greeting printed back from the model. That confirms the SDK, the runtime, your subscription login, and your account are all live — Foundation is done.

> `hello_claude.py` is a legacy connectivity test that uses the raw Anthropic SDK with an API key. It's kept for reference; `hello_agent.py` is the canonical Milestone 1 test for the current (Agent SDK) stack.
