### Feature 1
- Prompt Injection Detector : A prompt injection attack is when a user tries to override the LLM's system instructions by embedding malicious instructions in their input.
  - Takes a user prompt as input
  - Checks it against known injection patterns
  - Returns whether it's safe or suspicious + why