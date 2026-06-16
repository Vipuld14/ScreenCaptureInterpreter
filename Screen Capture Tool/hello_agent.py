"""Foundation connectivity test — Claude Agent SDK, subscription auth.

Confirms the Milestone 1 foundation on the new stack:
  1. the claude-agent-sdk package is installed,
  2. the Claude Code runtime (CLI) is installed and reachable,
  3. you're authenticated through your Claude subscription,
  4. a round-trip to the model returns text.

Auth model: this script uses your Claude SUBSCRIPTION (Pro/Max/Team/
Enterprise) via the Claude Code login — no API key. Usage draws from your
normal subscription limits.

Prerequisites (one-time):
  - Install the Claude Code CLI:   npm install -g @anthropic-ai/claude-code
  - Log in with your subscription:  claude   (then follow the login prompt)
    The SDK reuses those saved credentials.

IMPORTANT: do NOT set ANTHROPIC_API_KEY for the subscription route. If that
variable is set, the SDK routes through pay-as-you-go API billing instead of
your subscription. This script warns you if it detects one.

Run it:  python hello_agent.py
You should see a short greeting printed back from the model.
"""

import os
import sys

import anyio

PROMPT = "Say hello in one short sentence."


async def ask() -> str:
    """Send one prompt through the Agent SDK and collect any text returned."""
    from claude_agent_sdk import query, ClaudeAgentOptions

    # Keep it to a single, simple turn — no tools needed for a hello check.
    options = ClaudeAgentOptions(max_turns=1)

    parts: list[str] = []
    async for message in query(prompt=PROMPT, options=options):
        # AssistantMessage carries a list of content blocks; text blocks have
        # a `.text`. Use duck typing so this stays robust across SDK versions.
        content = getattr(message, "content", None)
        if not content:
            continue
        for block in content:
            text = getattr(block, "text", None)
            if text:
                parts.append(text)
    return "".join(parts).strip()


def main() -> int:
    if os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "Warning: ANTHROPIC_API_KEY is set. The SDK will use pay-as-you-go\n"
            "API billing, NOT your subscription. Unset it to use your plan:\n"
            "    unset ANTHROPIC_API_KEY\n",
            file=sys.stderr,
        )

    try:
        reply = anyio.run(ask)
    except ImportError:
        print(
            "claude-agent-sdk is not installed.\n"
            "Install dependencies first:  pip install -r requirements.txt",
            file=sys.stderr,
        )
        return 1
    except Exception as exc:  # noqa: BLE001 - surface a friendly hint
        # Most common causes: Claude Code CLI not installed, or not logged in.
        print(
            f"Could not complete the call: {type(exc).__name__}: {exc}\n\n"
            "Common fixes:\n"
            "  - Install the CLI:   npm install -g @anthropic-ai/claude-code\n"
            "  - Log in:            claude   (then complete the login prompt)\n"
            "  - Confirm you're on a paid plan (subscription auth needs one).",
            file=sys.stderr,
        )
        return 1

    if not reply:
        print("Connected, but no text was returned.", file=sys.stderr)
        return 1

    print(reply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
