# Worked Example: First-Response Protocol Slip

Use this reference when a target agent in a Telegram group sends substantive content first, but fails to make the visible caller/ownership chain legible.

Current practical reading:
- the most important repair target is the **visible caller anchor**
- native quote-reply can still be discussed, but it is not the first pass/fail gate when the runtime only reliably preserves topic continuity

## Failure shape

Observed bad first response:
- free-floating plain-text analysis
- no native quote-reply to the triggering message
- no `[ACK]`
- no `@caller [reply-fallback]`

Observed bad closeout variant:
- the agent later produces a thoughtful final summary
- the agent knows who the caller is
- but the **final visible message** still drops `@caller [reply-fallback]`
- and no native quote-reply chain was restored

This is a **protocol slip**, not automatically proof that the target agent never loaded the skill.
A later correction can still show that the agent knows the protocol vocabulary but did not let it govern the first response.

## Diagnosis rule

When this happens, prefer this interpretation order:
1. the skill did not sufficiently govern the first response behavior
2. the agent defaulted to generic answer-first habits
3. only then consider whether the skill may not have been loaded or prioritized

Do **not** jump straight to "the skill was definitely not loaded" unless you have stronger evidence than message shape alone.

## Corrective response pattern

If the agent already sent content incorrectly, the next public message should repair the chain immediately:

```text
@caller_bot [reply-fallback]
原链路无法继续做原生引用回复。
[ACK] 收到，我接手。
任务: <one-line restatement>
下一步: <one-line next action>
```

After that, continue the substantive discussion in the corrected chain.

If the turn is ending and the chain was never restored to native quote-reply, the final visible closeout should still preserve the fallback anchor:

```text
@caller_bot [reply-fallback]
原链路仍未恢复为原生引用回复，这里继续沿用 fallback 链路。
[REPORT] <final summary>
```

## Skill hardening lesson

If this failure happens in a real deployment, harden the umbrella skill in this order:
1. add a **First-Response Hard Rule** near the top of the file
2. explicitly forbid a **free-floating plain-text answer first**
3. require **ACK before analysis**
4. add a one-screen **Incoming request quick path**
5. add **Wrong vs Right** examples
6. add a checklist item that blocks sending analysis before native quote-reply / reply-fallback is fixed

## Minimal acceptable first response

Preferred native quote-reply form:

```text
[ACK] 收到，我接手。
任务: <one line>
下一步: <one line>
```

Fallback form when native quote-reply is unavailable:

```text
@caller_bot [reply-fallback]
原链路无法继续做原生引用回复。
[ACK] 收到，我接手。
任务: <one line>
下一步: <one line>
```

## Why this matters

In Telegram public coordination, the first response does two jobs before any real analysis:
- preserves the visible native quote-reply task lineage
- makes ownership explicit for humans and other agents

If those two jobs are skipped, the group can still recover, but the protocol has already slipped.

The same standard applies at closeout:
- if fallback mode is still the active visible path, the final visible summary must preserve the caller anchor
- knowing the caller internally is not enough; the public message shape must still show it

Operational takeaway:
- if you can only reliably enforce one thing in constrained runtime conditions, enforce `@caller_bot [reply-fallback]`
- treat native quote-reply quality as a nice-to-have runtime improvement, not the main document-level blocker
