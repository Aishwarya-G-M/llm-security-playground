# ADR 0001: Move from playground API to secure LLM gateway

## Status
Accepted

## Context
The initial version of this project started as an LLM security playground to explore prompt inspection, attack catalogs, logging, and guarded chat flows. That version was useful for experimentation, but it did not clearly express a production-style security boundary around model usage.

For the next version, the project needs to better represent how real teams secure LLM applications in backend and platform environments. The goal is to evolve the project into a recruiter-facing portfolio piece that demonstrates backend architecture, LLM security controls, and systems thinking.

## Decision
The project will evolve from a playground-style FastAPI application into a secure LLM gateway.

The secure LLM gateway will:
- receive user and system prompts through a gateway layer,
- inspect inputs before any model call is made,
- call the LLM only if policy checks allow it,
- inspect model outputs before returning them to the caller,
- enforce actions such as allow, block, redact, or review,
- log security decisions and request metadata for observability.

The architecture will separate responsibilities into:
- gateway/orchestration layer,
- inspector/guardrail layer,
- LLM client/provider layer.

The first implementation of the inspector will use deterministic rules and pattern libraries. Model-based inspection may be added later as an optional second layer.

## Consequences
### Positive
- The project better reflects real-world LLM security architecture.
- The repository tells a clearer story for backend, AI infra, and cybersecurity roles.
- Security controls become easier to test, explain, and extend.
- The design supports future observability and analytics integrations.

### Negative
- The codebase will require refactoring from endpoint-centric logic to service-oriented flow.
- Some v1 endpoints may need to be deprecated or reshaped.
- The project scope becomes broader and requires stronger documentation discipline.

## Alternatives considered
- Keep the project as a lightweight playground and only add more attack examples.
- Build a separate new repository for the gateway architecture.
- Use a model-only guardrail approach from the start.

These options were rejected because they either weakened the architecture story, split effort across repos, or added unnecessary complexity too early.