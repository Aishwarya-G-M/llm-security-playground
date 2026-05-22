### How to use
From inside llm-security-playground/, run:
- docker compose up --build
### Endpoints available
/chat = normal app behavior.

/analyze = inspect one prompt for safety.

/attacks = curated library of known bad scenarios.

/attacks/run = execute one of those scenarios and record the outcome.

### Feature 1 - Hardcoded prompt patterns
- Prompt Injection Detector : A prompt injection attack is when a user tries to override the LLM's system instructions by embedding malicious instructions in their input.
  - Takes a user prompt as input
  - Checks it against known injection patterns
  - Returns whether it's safe or suspicious + why 
  - 
  - 
### Feature 2 — Fintech Attack Pattern Library
  - Replaces hardcoded injection strings with a structured, domain-specific pattern library sourced from OWASP LLM Top 10 and open-source security tools. Patterns are organized by fintech context (banking, payments, KYC) and carry severity scores, enabling risk-based decisions instead of binary safe/unsafe responses.

