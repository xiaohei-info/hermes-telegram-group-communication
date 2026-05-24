# Live Telegram Bot Roster For This Deployment

You can edit this file directly for local use; rendering from JSON is optional.
If you do use a structured local config, keep this file aligned with it. Verify every bot username, bot ID, and capability flag against your current Telegram runtime before relying on it.

## Shared-skill visibility note

- Adjust this section to match how your own Hermes profiles load shared skills.
- If you do not maintain a central shared-skills directory, rewrite this note accordingly.

## Verified addressable bots

- `routing-specialist` -> `@your_routing_bot`
  - display_name: `Routing Specialist`
  - has_topics_enabled: `unknown`

- `architecture-specialist` -> `@your_architecture_bot`
  - display_name: `Architecture Specialist`
  - has_topics_enabled: `unknown`

- `backend-specialist` -> `@your_backend_bot`
  - display_name: `Backend Specialist`
  - has_topics_enabled: `unknown`

- `frontend-specialist` -> `@your_frontend_bot`
  - display_name: `Frontend Specialist`
  - has_topics_enabled: `unknown`

- `data-specialist` -> `@your_data_bot`
  - display_name: `Data Specialist`
  - has_topics_enabled: `unknown`

- `validation-specialist` -> `@your_validation_bot`
  - display_name: `Validation Specialist`
  - has_topics_enabled: `unknown`

- `review-specialist` -> `@your_review_bot`
  - display_name: `Review Specialist`
  - has_topics_enabled: `unknown`

- `product-owner` -> `@your_product_owner_bot`
  - display_name: `Product Owner`
  - has_topics_enabled: `unknown`

## Operational reminders

- Re-verify usernames after token rotation, bot replacement, or Telegram-side configuration changes.
- If your deployment does not expose bot IDs publicly, omit them from config and from this rendered file.
