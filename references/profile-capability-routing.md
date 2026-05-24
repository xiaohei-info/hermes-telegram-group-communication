# Profile Capability Routing Reference

Use this reference when an agent needs to decide **which other agent to @mention** for help in a Telegram group.

You can edit this file directly for local use; rendering from JSON is optional. It gives a fast routing map, but it does not replace reading the underlying role docs when boundaries are important.

## Primary rule

Before asking another agent to act, prefer this order:
1. identify the real problem type
2. map it to the most relevant profile capability
3. pick the **smallest sufficient specialist set**
4. only expand to more agents if the first specialist explicitly needs another boundary crossed

Do **not** start by mentioning many bots “just in case”.

## Quick routing map

### `routing-specialist`
Best for:
- routing
- decomposition
- parallel workstream planning
- upstream summarization

Not best for:
- being the default implementer

Escalate to routing-specialist when:
- you do not know the right split yet
- there are 3+ plausible specialists
- the task is naturally a graph rather than one bounded action

### `architecture-specialist`
Best for:
- system design
- interface boundaries
- migrations
- cross-service coordination

Not best for:
- trivial local bugfixes
- being the default implementer

Escalate to architecture-specialist when:
- the task crosses service/module boundaries
- schema/contract/migration shape matters

### `backend-specialist`
Best for:
- API behavior
- service logic
- business rules
- integrations
- backend tests

Not best for:
- warehouse/ETL ownership
- frontend-visible UX issues as the primary problem

### `frontend-specialist`
Best for:
- UI
- interactions
- browser behavior
- frontend state
- frontend tests

Not best for:
- patching around backend/data semantics instead of escalating upstream

Escalate to frontend-specialist when:
- the real issue is backend contract/data semantics, not browser behavior

### `data-specialist`
Best for:
- ETL/ELT
- data pipelines
- warehouse modeling
- backfill
- data quality

Not best for:
- application API/service logic as the main problem

### `validation-specialist`
Best for:
- reproduction
- user-path verification
- regression checks
- validation evidence collection

Not best for:
- acting as the final product owner
- replacing technical review

### `review-specialist`
Best for:
- independent technical quality review
- checking pass vs blocked
- evaluating implementation sufficiency

Not best for:
- being the implementer
- being the product sign-off owner

### `product-owner`
Best for:
- clarifying scope
- acceptance criteria
- product framing
- final product sign-off after QA evidence

Not best for:
- acting as the technical implementer

## Suggested decision pattern in-group

Before mentioning another bot, mentally ask:
1. What exact capability do I need that I do not already have?
2. Which role doc most clearly owns that capability?
3. Is this a direct request, a review gate, a verification gate, or a decomposition request?
4. Can I keep the request bounded to one branch instead of expanding the whole graph?
5. If the target later expands again, who still owns the parent branch?

## Source basis

Derived from role definitions under: `~/.hermes/profiles`
- `~/.hermes/profiles/routing-specialist/SOUL.md`
- `~/.hermes/profiles/architecture-specialist/SOUL.md`
- `~/.hermes/profiles/backend-specialist/SOUL.md`
- `~/.hermes/profiles/frontend-specialist/SOUL.md`
- `~/.hermes/profiles/data-specialist/SOUL.md`
- `~/.hermes/profiles/validation-specialist/SOUL.md`
- `~/.hermes/profiles/review-specialist/SOUL.md`
- `~/.hermes/profiles/product-owner/SOUL.md`

Use this file as the quick routing sheet; read the underlying role docs directly when the boundary is important or disputed.
