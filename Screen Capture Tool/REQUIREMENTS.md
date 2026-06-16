# Screen Capture Tool — Requirements

_Last updated: 2026-06-16_

## Core purpose
Take an image of a screen and return a clear explanation of what's on it. The MVP is exactly that, run manually on a single screenshot. Anything fancier goes on a "later" list.

**Key design intent:** this program does *not* implement the understanding/processing logic itself. Its job is to capture the screen and hand it to Claude; Claude does the reading, classifying, reasoning, and response generation. We delegate the "brain" to the Claude Agent SDK rather than hand-building an agent loop.

## Authorization
Teaching project; user has authorization to access the content. Caveat noted: "authorized to access" is not the same as "authorized to extract/reproduce elsewhere" — keep in mind, not a blocker.

## Stack
- Python throughout
- `mss` + `Pillow` for screen capture (grab pixels, save the frame to disk)
- **Claude Agent SDK** (`claude-agent-sdk`) as the processing brain — it reads the captured image, decides what's on it, routes to a suitable explanation approach, and generates the response. We do not write the understanding/agentic logic ourselves.
- Auth: the Agent SDK runs on a **paid Claude subscription** (Pro/Max/Team/Enterprise) via OAuth, or on a Claude Platform API key. (Billing note below.)
- FastAPI + a basic web page later, only if a real UI is wanted
- Explicitly avoiding for v1: Electron, queues, databases, microservices, premature abstractions

### Billing note (as of 2026-06-16)
Anthropic paused the planned separate monthly Agent SDK credit. For now, Agent SDK usage draws from your subscription's normal usage limits (same pool as interactive Claude/Cowork/Claude Code). A free plan won't work — a paid plan is required for the subscription route; otherwise use an API key with pay-as-you-go. This billing model is being reworked, so re-check before relying on the economics.

## The five layers
1. **Understanding** — the heart, and the biggest unknown. Can the agent reliably read & explain content from a screenshot? Validate first. This lives inside the Agent SDK; our job is to feed it the image and a good prompt.
2. **Capture** — grab pixels (`mss`), full screen or region, on a hotkey or interval; save the frame to a file the agent can read.
3. **Agentic** — classify what's on screen into whatever type it is (code, legal doc, spreadsheet, diagram, UI, chart, prose, etc.), route to an explanation approach suited to that type, judge whether it has enough to explain or needs more captures, and accumulate understanding across a multi-screen document.
   - **This is the agent's job, not ours.** We do not build the loop; we configure the agent and craft the prompt/instructions so it performs open-ended typing and routing on its own.
   - **Content typing is OPEN-ENDED**: the agent decides the content type on the fly each time; no hardcoded category list.
   - **Fallback**: if open-ended typing produces too many errors / low-quality explanations, constrain the agent toward a predefined set of content types with tuned per-type instructions.
4. **State/context** — feed prior captures/explanations back to the agent so explanations build on each other instead of treating each screenshot as isolated.
5. **Output** — terminal first; UI only once the core works.

## Milestones (riskiest slice first)
1. **Foundation** — repo, virtualenv, Agent SDK installed, auth working, a "hello Claude" agent call returns text.
2. **Core value end-to-end** — manual screenshot saved to disk → handed to the agent → printed explanation. Do not move on until this feels good.
3. **Real capture** — hotkey-triggered region/full-screen capture feeding step 2 automatically.
4. **Agentic routing** — prompt/configure the agent for open-ended content typing, then have it explain with an approach suited to that type. (Configuration + prompt work, not loop-building.)
5. **Multi-capture context** — dedupe near-identical frames, stitch, maintain running context across screens by feeding history back to the agent.
6. **UI + polish** — only what you'll actually use.

## Solo-build traps to watch
- No accountability — set visible milestones.
- The agent does the heavy lifting; resist re-implementing its reasoning yourself.
- Steps 4 & 5 are tempting to over-engineer; lean on the agent and good prompts first.
- Tempting to build a slick UI before the core understanding is solid; don't.
