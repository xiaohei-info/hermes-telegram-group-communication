# Shared-topic final quote-reply runtime note

Use this reference when a Telegram group/topic coordination task asks whether Hermes can make the **final visible response** land as a native quote-reply to the triggering user message.

## What this session established

In some Hermes Telegram deployments, native quote-reply is not blocked by Telegram itself.

The relevant split is:
- the Telegram adapter `send()` path supports `reply_to_message_id`
- inbound Telegram events can capture `reply_to_message_id` / `reply_to_text`
- but the gateway's shared-topic reply-anchor policy may **not** automatically preserve a reply anchor for normal Telegram group/forum-topic final responses

## Important distinction

### Telegram DM topic special case
Some helpers preserve a reply anchor for Telegram **DM topics** because those lanes need both thread metadata and a reply anchor to render in the correct lane.

### Telegram shared topic / group thread case
For Telegram shared topics (forum/supergroup topic-style conversations), some gateway configurations prefer:
- topic continuity via `thread_id`
- not automatic message-level native quote-reply on the final response

So if the user says:
- "When I @ you in this topic, your final response should quote-reply my message"

that is a **runtime/gateway behavior request**, not something a protocol skill can enforce by wording alone.

## Why the skill still matters

The coordination skill should still enforce:
- visible caller anchoring via `@caller_bot [reply-fallback]` when native quote-reply is unavailable
- visible public ACK before or during long tool turns
- treating a plain final topic-post as fallback unless a real message-level quote-reply was actually established

But the skill cannot itself upgrade a topic-post into a native quote-reply if the gateway send path does not carry the reply anchor.

## Practical diagnosis rule

If a Telegram shared-topic final response failed to native-quote-reply the triggering message, ask in this order:
1. did the gateway/runtime preserve a message-level reply anchor for the final send?
2. or did it only preserve `thread_id`, producing topic continuity without a message-level reply link?
3. if only `thread_id` was preserved, treat the outcome as topic-post / fallback behavior, not as a skill-compliance win on quote-reply

## Implementation implication

If the product requirement is:
- final responses in Telegram shared topics should quote-reply the triggering user message

then the likely fix lives in the gateway policy / send wiring, not only in the protocol skill:
- choose a reply anchor for Telegram shared-topic inbound events
- carry that anchor into the normal final-response send path
- verify chunking behavior (`reply_to_mode`) after the change

## Remember

Protocol wording can require `@caller` fallback and visible ACK.
Native quote-reply in Telegram shared topics requires gateway/runtime support to preserve and use a real reply anchor.