# Message-Link Semantics

Use this reference when a Telegram-group coordination task depends on distinguishing a true message-level link from a same-topic post.

## Core distinction

### Native quote-reply / 原生引用回复
A native Telegram reply to one specific message.

Properties:
- preserves a message-level quote/reply chain
- should be described as `quote-reply` or `原生引用回复`
- is the preferred link form when the runtime actually supports it

### Topic-post / 同 topic 新发一条
A new message posted in the same Telegram topic/thread, but not attached as a native reply to one specific message.

Properties:
- stays in the same visible topic
- does **not** preserve a message-level reply handle
- should not be described as if it were a native quote-reply

### Reply-fallback / 引用回复降级补救
A same-topic topic-post used when native quote-reply is unavailable or unreliable.

Required shape:
- first line explicitly starts with `@caller_bot [reply-fallback]`
- acknowledges that native quote-reply could not be used
- then continues with `[ACK]`, ownership, task, and next step
- if the conversation remains on fallback through the end of the turn, the **final visible summary/report should also preserve `@caller_bot [reply-fallback]`** unless a real native quote-reply chain has been established

Practical priority:
- in deployments where quote-reply is not reliably preserved, keeping the visible `@caller_bot [reply-fallback]` contract matters more than forcing quote-reply language everywhere

## Hermes tool mapping

### `send_message` without an explicit message-level reply handle
Treat the result as a **topic-post**, not a native quote-reply.

Implication:
- if the protocol wanted native quote-reply but the tool path only produced a same-topic new post, describe it as `reply-fallback` rather than pretending the quote-reply chain exists
- do not treat the lack of native quote-reply as the main blocker if the caller anchor is still visible and stable

### Plain final assistant text sent into the current chat/topic
Also treat this as a surface message, not automatically as a native quote-reply, unless the platform/runtime explicitly preserves a message-level reply reference

Implication:
- if the visible end-of-turn message is just plain assistant text in the topic, and no message-level reply reference is preserved, evaluate it as a `topic-post`
- if fallback mode was active, that final topic-post should still preserve `@caller_bot [reply-fallback]`

## Language rules

Preferred wording:
- `native quote-reply` / `原生引用回复`
- `topic-post` / `同 topic 新发一条`
- `reply-fallback` / `引用回复降级补救`

Avoid vague wording:
- `reply this` when you really mean native quote-reply
- `reply failed` when the actual issue was "we only had a topic-post path"
- `same chain` when there is only same-topic continuity but no message-level quote chain

## Operational rule

If you cannot prove that a message was attached as a native Telegram reply to a specific prior message, do **not** describe it as a native quote-reply.

Instead:
1. call it a `topic-post`
2. if it is compensating for the missing quote-reply, mark it `reply-fallback`
3. if it is the final visible message on that fallback path, preserve `@caller_bot [reply-fallback]` there too
4. instruct the downstream agent using fallback language, not quote-reply language

Do not overstate the requirement:
- native quote-reply remains useful terminology
- but for deployments with limited reply-anchor support, the enforceable contract is the visible caller anchor, not perfect quote-reply fidelity

## Example

Bad description:
- "I replied to the target specialist in the thread" when the actual action was a new same-topic `send_message`

Correct description:
- "I made a same-topic topic-post to the target specialist via `send_message`; because no message-level reply handle was available, it should be treated as `reply-fallback`, not native quote-reply."

Bad closeout description:
- "The agent knew the caller and posted a final summary in the topic, so the fallback was good enough."

Correct closeout description:
- "The final visible message was still only a topic-post. Because fallback mode remained active, the closeout should have preserved `@caller_bot [reply-fallback]`; dropping that caller anchor was still a protocol failure."
