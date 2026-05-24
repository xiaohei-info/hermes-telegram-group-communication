---
name: telegram-group-agent-cluster-communicate-protocol
description: Use when multiple Hermes/OpenClaw/other agent bots need to talk, hand off work, coordinate ownership, or report through a shared Telegram group or topic without causing noisy misfires.
version: 1.5.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [telegram, group-chat, multi-agent, coordination, handoff, routing, protocol]
    related_skills: [hermes-agent, subagent-collaboration-workflow, writing-skills]
---

# Telegram Group Agent Cluster Communication Protocol

## Overview

Use this skill when two or more agent bots share a Telegram group or topic and need to coordinate in public.

This protocol is designed for the real failure modes that appear in multi-agent Telegram operations:
- the wrong bot wakes up because someone casually typed a handle
- the right bot never wakes up because nobody explicitly addressed it
- multiple bots answer the same task and create noise
- a conversation forks into several top-level messages and loses the timeline
- nobody knows who is supposed to report upstream

Core principle:
- **topic = workspace**
- **native quote-reply chain = task lineage**
- **@mention = explicit wake-up / routing signal**
- **a task graph may branch, but each branch should have one current owner**

Current operating focus:
- Telegram already gives durable visible message history, native quote-reply chains, topics, and explicit wake-ups
- this skill is about **current visible coordination behavior**, not a future shared-state/runtime design
- coordination quality comes from explicit wake-ups, native quote-reply discipline, clear ownership, and low-noise routing

In a multi-agent Telegram deployment, “Telegram bot-to-bot communication mode” should be understood operationally, not magically:
- one bot publicly talks in the Telegram group/topic
- another bot is woken up because it was **explicitly @mentioned** or the message **used native Telegram quote-reply to one of its prior messages**
- the collaboration then continues in the same visible thread so humans can audit the handoff

Do **not** assume passive omniscience. A bot seeing a group message is a delivery/routing event, not a given.

## Message-Link Terminology

In this skill, do **not** use bare `reply` as a vague word.

Use these terms instead:

- **Native quote-reply / 原生引用回复**
  - A native Telegram quote-reply to one specific message, preserving the message-level quote/reply chain.
  - This is the preferred form when the environment supports it.

- **Topic-post / 同 topic 新发一条**
  - A new message posted in the same Telegram topic/thread, but not attached as a native quote-reply to a specific message.

- **Reply-fallback / 引用回复降级补救**
  - When native quote-reply is unavailable or unreliable, make a same-topic topic-post and explicitly start with `@caller_bot [reply-fallback]`.

- **@mention wake-up / @mention 唤醒**
  - Used to route attention to a target agent.
  - This is not the same thing as a native quote-reply.

Hard meaning rule:
- In this skill, bare `reply` does **not** mean “any textual response.”
- Unless explicitly marked as `reply-fallback`, `reply` means a **native Telegram quote-reply** to one specific message.

Current tooling reality:
- current Hermes Telegram operations may not always expose a reliable message-level native quote-reply primitive
- when native quote-reply is unavailable, use `reply-fallback` instead of pretending a same-topic new post is a true quote-reply
- when using channel-level posting paths such as `send_message` without an explicit message-level reply handle, treat the result as a **topic-post**, not a native quote-reply

Practical priority in deployments where message-level native quote-reply may be unavailable from the runtime/tooling:
- **keep the visible caller anchor alive first**
- if `@caller_bot [reply-fallback]` is visible and stable, that already satisfies the current minimum coordination contract
- treat native quote-reply as a **best-effort enhancement**, not a hard requirement when the runtime/tool path does not reliably provide it

## First-Response Hard Rule

If you are explicitly asked to act in a Telegram group/topic, your **first protocol-valid response** should follow one of these two forms:

1. **Use a native Telegram quote-reply to the triggering message** and start with `[ACK]`
2. If native quote-reply is unavailable, send a same-topic topic-post whose first line is `@caller_bot [reply-fallback]`, then `[ACK]`

Hard rules:
- **Do not send a free-floating plain-text answer first.**
- **Do not give substantive analysis before ownership / message-link path is made explicit.**
- **ACK comes before analysis.** In public coordination, the first job is to make the native quote-reply chain or explicit fallback path legible.
- **A model-internal ACK does not count unless it becomes a visible Telegram message.** If the ACK only exists in an assistant/tool-call intermediate state, the protocol was not actually satisfied.
- **If you are on a reply-fallback path, the final visible response must still preserve the caller anchor** (for example `@caller_bot [reply-fallback]`) unless a real native quote-reply chain has already been established.
- If you skipped this and already sent content, immediately send a protocol-correct fallback message and continue there.

Operational priority:
- if you must choose between forcing quote-reply wording and keeping a clear visible caller anchor, choose the **visible caller anchor**
- in deployments where message-level reply anchors are not reliably preserved, `@caller_bot [reply-fallback]` is the reliable baseline

### Final visible response rule

If the conversation is currently running on a `reply-fallback` path, the **final visible Telegram response must still look like fallback**.

Minimum acceptable final-fallback shape:

```text
@caller_bot [reply-fallback]
<final summary / report / answer>
```

This rule exists because a common failure mode is:
- the agent internally understands who the caller is
- the agent may even produce an internal `[ACK]`
- but the only message that becomes publicly visible is a final plain-text summary with no caller anchor

That outcome is still a protocol failure.

Non-negotiable rule:
- **If the final visible message is a topic-post rather than a native quote-reply, it must preserve the caller anchor when fallback mode is in effect.**
- A polished final summary without `@caller_bot [reply-fallback]` does **not** satisfy the fallback contract.
- Do **not** over-correct by making native quote-reply itself the primary completion criterion when your runtime only guarantees topic continuity.

### Incoming request quick path

When a public Telegram message is asking **you** to act, do this in order:

1. **Use native Telegram quote-reply if it is naturally available and reliable** on the triggering message
2. If native quote-reply is not available, send a same-topic topic-post starting with `@caller_bot [reply-fallback]`
3. Start with **`[ACK]`**
4. If you expect a long tool/investigation turn, make that ACK a **real visible Telegram message first**; do not leave it as an internal assistant/tool-call intermediate
5. State only these three things before deeper analysis:
   - `owner: @self_bot` or equivalent ownership claim
   - `任务:` one-line restatement
   - `下一步:` immediate next action
6. If the turn later ends with a fallback topic-post rather than a native quote-reply, make sure the **final visible message again starts with `@caller_bot [reply-fallback]`**

One-line practical rule:
- **If in doubt, keep the `@caller_bot [reply-fallback]` chain alive. Do not block yourself on quote-reply.**

Compact form:

```text
[ACK] 收到，我接手。
任务: <one line>
下一步: <one line>
```

Wrong:

```text
我觉得今天最值得关注的是 SEC、宏观和 BTC 结构...
```

Right (native quote-reply preferred):

```text
[ACK] 收到，我接手。
任务: 给出今天最值得关注的 5 个点
下一步: 先列 5 点，再收敛 Top 3
```

Right (topic-post fallback when native quote-reply is unavailable):

```text
@caller_bot [reply-fallback]
原链路无法继续做原生引用回复。
[ACK] 收到，我接手。
任务: 给出今天最值得关注的 5 个点
下一步: 先列 5 点，再收敛 Top 3
```

Worked example for this exact failure mode:
- `references/first-response-protocol-slip-example.md`

For tool-level message-link semantics, including when a same-topic post from `send_message` should be treated as a `topic-post` rather than a native quote-reply:
- `references/message-link-semantics.md`

## When to Use

Use this skill when:
- an agent must ask another agent to investigate or act in a Telegram group
- several agents need to converge on what to report upstream
- a user wants a visible in-group coordination flow instead of hidden internal tooling
- ownership needs to move from one agent to another
- a topic/thread should remain readable as an auditable timeline

Do **not** use this skill as the primary guide for:
- one-agent DM conversations
- non-Telegram platforms
- background cron jobs that do not coordinate publicly in-group
- internal controller/subagent delegation that happens entirely off-platform

## Durable Platform Facts To Respect

These are the realities the protocol is built around:

1. **Do not assume every bot sees every group message.**
   Telegram delivery depends on platform behavior plus bot settings. In practice, the reliable triggers are:
   - a real `@botusername` mention
   - a native quote-reply to the bot’s message
   - an explicit `/command@botname` style command when supported

2. **Native quote-reply and mention are different signals.**
   - `native quote-reply` preserves message-level conversational lineage
   - `@mention` explicitly routes attention
   Good protocol uses them for different jobs instead of treating them as interchangeable.

3. **Topics/threads matter.**
   If the group uses topics, the visible discussion should stay in the correct topic. Splitting work across unrelated top-level messages makes coordination much harder to audit.

4. **Telegram does not give you “other bot fully understood and accepted the task” as a platform primitive.**
   You must define your own acknowledgement convention.

5. **Sending a message successfully is not the same as achieving coordination.**
   Coordination is only real after the target agent acknowledges ownership or answers in-thread.

## Protocol Vocabulary

Use these labels consistently when helpful:

- `[PING]` — waking another agent up
- `[ACK]` — acknowledging receipt / taking ownership
- `[HANDOFF]` — transferring ownership or a subtask
- `[DONE]` — task/result complete
- `[BLOCKED]` — cannot proceed; needs help / decision / fix
- `[REPORT]` — final summary intended for the human owner or upstream audience
- `[FYI]` — informative update that does **not** request action

You do not need to overuse the labels, but they help in crowded group flows.

## Operating Model

### 1) Start a new cross-agent conversation with an explicit wake-up

When you need another agent to act, **explicitly @mention that agent**.

Your first ping should normally include five things:
1. who you are
2. what you need
3. which protocol skill the target should load before acting
4. how the target should link its first response
5. what counts as success for the immediate next step

### Skill-loading reminder rule

When you are asking another agent to coordinate in a Telegram group/topic, **proactively tell that agent to load `telegram-group-agent-cluster-communicate-protocol` before replying**.

Do not assume the other agent will remember:
- to `@mention` the next owner
- to preserve `reply-fallback` caller anchors
- to start with `[ACK]`
- to nominate an upstream reporter

If protocol fidelity matters, the wake-up message should name the skill explicitly.

Recommended shape:

```text
@target_bot 我是 <self_bot> / <profile_name>。
请先加载 `telegram-group-agent-cluster-communicate-protocol` skill，再继续处理这条协作消息。
我需要你帮我 <one concrete ask>。
请优先使用 Telegram 原生引用回复（quote-reply）直接回复本条消息；如果当前环境无法执行原生引用回复，再在同一 topic 新发一条，并以 @<self_bot> [reply-fallback] 开头。
先回一句“收到”，然后给出 <expected next artifact>。
```

Why this works:
- the target knows it is being addressed
- the target is reminded to load the shared protocol before acting
- the human can audit the coordination
- the native quote-reply path or explicit fallback path is made explicit immediately

### 2) Continue an existing task with native quote-reply-first discipline

If the conversation is already underway, **prefer using a native Telegram quote-reply on the most relevant existing message when that path is naturally available and reliable** instead of starting a new topic-post.

Default rule:
- **same task, same chain -> prefer native quote-reply**
- **if native quote-reply is unavailable -> use same topic + `@caller_bot [reply-fallback]`**
- **new task, new owner, or new branch of work -> native quote-reply + @mention target if action is required**

Why:
- native quote-reply preserves lineage
- humans can read the chain from top to bottom
- less risk of parallel confusion

### 3) Use `native quote-reply + @target` for handoffs

When transferring work from one agent to another, the safest public shape is:
- use native quote-reply on the current task chain when possible
- @mention the new target agent
- summarize the handoff in 2-5 lines

Recommended template:

```text
[HANDOFF] @target_bot
当前 owner: @current_owner_bot
需要你做: <one concrete ask>
已知结论: <1-2 lines>
阻塞/边界: <if any>
请优先使用原生引用回复本条确认是否接手；如果当前环境无法执行原生引用回复，再在同一 topic 中以 @current_owner_bot [reply-fallback] 开头继续。
```

### 4) A task graph may branch, but each branch needs one current owner

This rule does **not** mean only one agent may participate in the whole job.
It means:
- one large task can split into **multiple parallel branches**
- different branches may have **different owners**
- but any **single external branch / formal subtask chain** should have one current owner at a time

Important nuance:
- visible branch ownership is about who is responsible in the chat
- the current owner may still do private/local execution work behind the scenes
- do not turn every internal helper step into a public branch unless another agent truly needs to act

Why this matters:
- it still allows parallel work
- it avoids duplicate execution inside the same visible branch
- it keeps the public thread readable
- it makes it clear who is responsible for follow-up, status, and completion of that branch

Good shape:
- parent task: coordinated by one initiator or your routing specialist
- branch A owner: <implementation-specialist> bot
- branch B owner: <interface-specialist> bot
- branch C owner: <validation-specialist> bot

Bad shape:
- the same visible branch is simultaneously "owned" by three bots with no clear boundary
- every small internal step is announced publicly even though nobody else needs to act

Recommended branch-level ACK format:

```text
[ACK] 我收到并接手这个分支。
owner: @self_bot
branch: <one-line branch name>
任务: <one-line restatement>
下一步: <immediate next action>
```

Rules:
- one formal branch should have **one current owner**
- a parent task may contain **many child branches**
- if a new agent takes over a branch, it should be a visible handoff, not a silent collision
- when creating a new child branch, say clearly whether it is:
  - a parallel child branch
  - a review gate
  - a verification gate
  - an escalation branch
- do not turn every small local step into a new public branch

### 5) Route by profile capability, not by random availability

When an agent wants help from other agents, it should choose them based on **capability boundary**, not on who happens to be active in the chat.

Default routing sources:
1. the target profile’s `SOUL.md`
2. the target profile’s known role boundary and output contract
3. the shared routing reference in `references/profile-capability-routing.md`

Examples:
- architecture / migration / cross-service boundary -> ask your architecture specialist
- API / service behavior / backend logic -> ask your backend specialist
- UI / browser behavior / interaction flow -> ask your frontend or interface specialist
- ETL / ELT / warehouse / backfill / data quality -> ask your data specialist
- independent technical quality gate -> ask your reviewer
- validation evidence / regression / user-path verification -> ask your QA or validation specialist
- scope / acceptance / product framing / sign-off boundary -> ask your PM or product owner
- if you do not know the right split, or the work naturally becomes a graph -> ask your routing/orchestration specialist

Preferred behavior:
- choose the **smallest sufficient specialist set**
- ask one specialist first when the boundary is clear
- expand only when crossing another real responsibility boundary

### 6) Collaboration may expand, but keep it bounded

A bot may proactively ask other bots for help.
A child collaborator may in turn ask another specialist for help.
This is allowed — but it must stay controlled.

Important correction:
- do **not** treat this protocol as saying there must always be a tiny fixed number of agents or a tiny fixed depth
- complexity varies by task
- what matters is whether the expansion is **explicitly justified and convergent**

Preferred control model:
- start with a small specialist set
- expand only when:
  - whether a new capability boundary is being crossed
  - whether the expected value of the new child is clear
  - whether the parent branch still has a clear owner and stop condition

Good default behavior:
- start with a **small initial specialist set**
- increase it only when the branch owner can explain:
  - why another agent is needed
  - what output is expected
  - how the result will merge back into the parent branch
- if the branch is already sprawling, prefer re-planning or orchestrator routing over continued sideways expansion

### 7) Anti-loop rules

To prevent infinite expansion or ping-pong loops:

1. **Every new agent request must answer “why this agent?” in one line.**
   If you cannot name the capability gap, do not wake another bot.

2. **Every new branch must define a stop condition.**
   Good examples:
   - "give me 1-3 report candidates"
   - "verify whether this regression reproduces"
   - "review this implementation and return pass/blocked"

3. **Every child branch should be made visible in-thread with a clear owner, goal, expected output, and stop condition.**

4. **Do not bounce the same undecided question back and forth between peer roles.**
   Example bad loop:
   - an implementation specialist asks an architecture specialist
   - the architecture specialist asks the implementation specialist back
   - the implementation specialist asks the architecture specialist again
   without a clearer question or narrower boundary

5. **Escalate, don’t recurse, when the boundary is disputed.**
   If two specialists disagree on who owns it, either:
   - route to your orchestration specialist, or
   - explicitly ask your PM / architecture specialist / reviewer for a boundary decision,
   instead of continuing to expand sideways.

6. **The parent branch owner remains responsible for convergence.**
   Asking another agent for help does not erase ownership of the parent branch unless a visible handoff happens.

7. **Use no-progress as a stopping signal, not as a reason to blindly spawn more agents.**
   If the branch has no real progress, re-plan or escalate.

### 8) Decide the upstream reporter explicitly

If multiple agents discuss what to tell the human, do **not** assume “whoever talks last reports.”

Before final reporting, someone should explicitly say one of:
- `我建议由 @X 统一汇报。`
- `如果你不发，我来替你汇报。`
- `这次我来汇报，你补充。`

Good rule:
- **the agent with the cleanest final wording usually reports**
- **the agent with operational context stays available for follow-up questions**

## Message Types And Recommended Behavior

### `[PING]`
Use when waking an agent up for action.
- must include `@target_bot`
- should state who you are
- should state whether native quote-reply or reply-fallback is expected

### `[ACK]`
Use when accepting responsibility.
- in public Telegram coordination, the **first substantive response** should normally begin with `[ACK]`
- claim ownership explicitly
- restate the task in one line
- say the next action

### `[HANDOFF]`
Use when moving work.
- prefer native quote-reply in the same chain
- if native quote-reply is unavailable, use a same-topic topic-post with explicit `@target_bot [reply-fallback]` or `@current_owner_bot [reply-fallback]` as appropriate
- include `@target_bot`
- include enough context that the target does not need to rediscover the entire situation

### `[DONE]`
Use when the requested immediate task is complete.
- say what was produced
- say whether more action is needed
- if relevant, nominate who should report upstream

### `[BLOCKED]`
Use when you cannot continue.
- say what is blocking you
- say whether you need a user decision, another agent, or a technical fix
- do not just go silent

### `[REPORT]`
Use when presenting the final message that should go to the human owner.
- keep it concise
- separate “what happened” from “what action is suggested”
- if it is a candidate draft, say so
- if the discussion is still on a `reply-fallback` path, preserve the caller anchor in the final visible report instead of dropping into an unanchored plain-text summary

## Avoiding Accidental Wake-Ups

This matters a lot in busy group threads.

### Never casually type a real bot handle unless you want that agent’s attention

Bad:
- “我们可以让 @some_bot 之后再看看”
- “参考 @other_bot 的命名”

Safer alternatives:
- wrap it in backticks: `` `@some_bot` ``
- replace `@` with the full-width version: `＠some_bot`
- write the profile name without the live handle: `market-analysis profile bot`

### Do not list many live bot handles in one normal sentence

If you mention three or four real bot usernames in the open, you may wake several agents unintentionally.

Only mention the bot(s) that need to act now.

### Distinguish action requests from references

If a message is **for action**, use a real mention.
If a message is **just documentation or discussion**, de-activate the handle.

## Preferred Fallback Path When Native Quote-Reply Fails

Sometimes native quote-reply is unavailable, awkward, or the original message is gone.

Fallback rule:
1. start a fresh message in the **same topic/thread if possible**
2. `@mention` the target agent
3. include a compact context recap
4. explicitly say that this is a native-quote-reply fallback

Recommended template:

```text
@target_bot [reply-fallback]
原链路无法继续做原生引用回复，这里补一条同 topic 新消息。
上下文: <2-3 line summary>
需要你现在做: <one concrete ask>
请在这条下面继续。
```

Final-summary variant when the fallback chain remains the active visible path:

```text
@caller_bot [reply-fallback]
原链路仍未恢复为原生引用回复，这里继续沿用 fallback 链路。
[REPORT] <final summary>
```

## Silence Rules

Good collaboration is not maximal chatter.

### If you are not the owner

Default behavior:
- add signal, not noise
- do not restate what is already obvious
- do not start doing the owner’s work unless asked
- do not race to produce a second full answer unless the owner is stalled or the user explicitly wants multiple views

### If you are the owner

Default behavior:
- acknowledge quickly
- give short progress updates only when they reduce uncertainty
- when blocked, say so explicitly instead of disappearing
- once the work is done, propose who should report upstream

## Failure Modes And How To Diagnose Them

When debugging Telegram coordination slips, prioritize the **visible public contract** over incidental inbound-shape details.

Diagnostic priority order:
1. did the final visible message preserve the caller anchor (`@caller_bot [reply-fallback]`) when fallback was in use?
2. was there a visible public `[ACK]` / ownership claim, rather than only an internal assistant/tool-call ACK?
3. only after those checks, inspect whether target wake-up details (such as the exact target `@mention`) were preserved verbatim in the agent-visible inbound text
4. native quote-reply quality can be checked afterward as a secondary runtime detail, not the first pass/fail gate

Reason:
- for protocol quality, a missing final caller anchor or missing quote-reply shape is a more important failure than whether the target wake-up handle survived unchanged in the inbound text
- do **not** let analysis get stuck on the wrong question if the user is complaining about the final visible response shape

If an agent does not answer, do **not** jump straight to “it ignored me.” Check the likely failure classes:

1. **No real wake-up happened**
   - no actual `@mention`
   - mention text did not become a real Telegram mention entity
   - no native quote-reply to the target’s message

2. **Bot visibility/delivery constraints**
   - Telegram delivery mode / privacy behavior
   - bot can’t see ordinary chatter and needs a true direct trigger

3. **Hermes-side routing limits**
   - `allowed_chats` / `require_mention`
   - user allowlists such as `TELEGRAM_ALLOWED_USERS`
   - wrong topic/thread

4. **Bot identity/config problems**
   - invalid or stale token
   - bot not actually running
   - wrong bot username assumed by the sender

5. **Conversation-structure problems**
   - native quote-reply chain broke
   - new top-level message lost the lineage
   - several bots were mentioned and nobody knew who owned the task
   - the final visible response lost the caller anchor (`@caller_bot [reply-fallback]`) even though the agent knew who the caller was
   - a protocol-correct ACK existed only internally before tool calls, but no visible public ACK / fallback anchor was ever sent

Diagnostic priority:
- when evaluating whether the protocol held, prioritize the **visible public contract**:
  - did the final visible message preserve `@caller_bot [reply-fallback]` when fallback was in use?
  - did the group still have a legible caller/owner chain?
- native quote-reply is a secondary quality-improvement check here, not the first pass/fail gate
- do **not** over-focus on whether the target wake-up `@mention` survived verbatim in the agent-visible inbound text; that may matter for delivery, but it does not excuse losing the caller anchor in the final visible response

### If the target bot stays silent

Use this order:
1. confirm you used a real `@target_bot` or a native quote-reply to its message
2. confirm you are in the intended topic/thread
3. check whether the bot is configured/running
4. if needed, retry with a shorter direct wake-up
5. if still silent, treat it as a delivery/config problem, not a social one

## Optional Local Bot Roster

If your deployment maintains a verified roster of profile keys, bot usernames, and topic capabilities, keep it in:
- `references/live-bot-roster.md`

Operational rule:
- re-verify target bot usernames and topic capability flags against your local Telegram runtime before relying on them
- if your deployment does not maintain a central roster, remove that reference and route by your human-maintained capability docs instead

## Quick Templates

### Ask another agent to contribute

```text
@target_bot 我是 @self_bot。
请先加载 `telegram-group-agent-cluster-communicate-protocol` skill，再继续处理这条协作消息。
我需要你帮我 <one concrete ask>。
请优先使用 Telegram 原生引用回复本条；如果当前环境无法执行原生引用回复，再在同一 topic 中以 @self_bot [reply-fallback] 开头。
先回“收到”，再给出 <expected next artifact>。
```

### Claim ownership

```text
[ACK] 收到，我接手。
owner: @self_bot
任务: <one line>
下一步: <one line>
```

### Claim ownership when native quote-reply is unavailable

```text
@caller_bot [reply-fallback]
原链路无法继续做原生引用回复。
[ACK] 收到，我接手。
任务: <one line>
下一步: <one line>
```

### Nominate the reporter

```text
我同意当前排序/结论。
我建议这次由 @target_bot 统一给用户汇报；我留在这里补充追问。
```

### Report fallback when native quote-reply chain breaks

```text
@target_bot [reply-fallback]
原链路无法继续做原生引用回复。
上下文: <2-3 lines>
请在这条下继续，并先回“收到”。
```

## Common Pitfalls

1. **把 `@mention` 当普通文字引用。**
   这最容易误触发别的 agent。

2. **继续同一任务时，把同 topic 新发一条误当成了原生引用回复。**
   这会让消息级引用链断裂。

3. **希望多个 agent 都看见，但没有显式 mention 它们。**
   不可靠。

4. **多个 agent 同时接活，没有 owner。**
   结果是重复劳动和噪音。

5. **上游汇报人未明确指定。**
   最后没有人汇报，或两个人都汇报。

6. **扩散没有边界。**
   一个 agent 不断再去叫更多 agent，最终形成长链路、噪音或循环。

7. **没有按能力边界选人。**
   没先看 profile / SOUL，就随意 @ 一个看起来在线的 bot。

8. **原生引用回复不可用时直接沉默。**
   正确动作是：同一 topic 新发一条 + `@mention` + `reply-fallback` + compact recap。

9. **写文档/举例时裸写真实 bot handle。**
   这会制造意外唤醒。

10. **先分析，后 ACK / 后补消息链路。**
   这是最常见的协议滑落。正确顺序是：先原生引用回复；如果做不到，再 `reply-fallback`，再 `[ACK]`，再给 substantive content。

11. **默认以为对方会自己记得加载这个 skill。**
   不要假设别的 agent 会自动想起这套 protocol。发起协作时应主动写明：先加载 `telegram-group-agent-cluster-communicate-protocol` skill，再回复。

12. **最终可见总结丢失 caller anchor。**
   即使 agent 知道 caller 是谁、甚至内部已经生成过 `[ACK]`，如果最终公开发出的只有 plain-text summary 且没有 `@caller_bot [reply-fallback]`，协议仍然失败。

## Verification Checklist

Before sending a coordination message in a Telegram group/topic, check:

- [ ] 如果这是我对 action request 的第一响应，我是否已经先做了原生引用回复，或明确使用 `@caller [reply-fallback]` 了？
- [ ] 如果没有，我是否先停下来修正协议形态，而不是直接发送分析内容？
- [ ] 我是在继续同一任务吗？如果是，优先使用原生引用回复保持消息级链路。
- [ ] 我真的需要目标 agent 行动吗？如果需要，显式 `@mention` 它。
- [ ] 如果这次协作需要遵守本 protocol，我有没有明确告诉对方先加载 `telegram-group-agent-cluster-communicate-protocol` skill？
- [ ] 我有没有无意中写出别的真实 bot handle？
- [ ] 当前任务链是否已有明确 owner？
- [ ] 如果我要拉其他 agent 进来，我是否先根据 profile / SOUL / routing reference 选对了人？
- [ ] 这次扩展是否真的跨了新的能力边界，而不是为了保险乱扩散？
- [ ] 我有没有把新分支的 stop condition 说清楚？
- [ ] 下游 agent 能否直接看懂：它应当使用原生引用回复，还是应当使用 `reply-fallback`？
- [ ] 如果这是一条分支/gate/handoff，我有没有把它的类型和边界说清楚？
- [ ] 如果在交接，我有没有写清楚 handoff 摘要？
- [ ] 如果准备对用户汇报，我有没有明确谁来汇报？
- [ ] 如果原生引用回复不可用，我有没有用 `reply-fallback` 明确保留上下文？
- [ ] 如果最终可见消息仍然是 fallback topic-post，而不是真正的 native quote-reply，我有没有在最终消息里再次保留 `@caller_bot [reply-fallback]`？
- [ ] 目标 bot username 是否仍然在 live roster 中有效？

## Platform Basis / Useful References

Official Telegram Bot API references worth re-checking when behavior changes:
- `https://core.telegram.org/bots/api`
- `https://core.telegram.org/bots/features#privacy-mode`
- `https://core.telegram.org/bots/api#message`
- `https://core.telegram.org/bots/api#messageentity`
- `https://core.telegram.org/bots/api#sendmessage`
- `https://core.telegram.org/bots/api#replyparameters`
- `https://core.telegram.org/bots/api#forumtopic`

Local runtime-specific references you may want to maintain in your own deployment:
- a note describing how your message-sending tool handles topic continuity vs message-level reply anchors
- a note describing how Telegram privacy mode / mention-gating is configured in your environment

## Remember

The goal is **reliable visible coordination with minimal noise**.

If an agent should act:
- wake it up intentionally
- continue in the right native quote-reply chain, or use explicit `reply-fallback` when native quote-reply is unavailable
- assign one owner
- choose one reporter
- avoid waking everyone else by accident
