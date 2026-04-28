# Vusense: Company-Wide AI Usage Guidelines

This document serves as the top-level governance framework for all Artificial Intelligence (AI) and Large Language Model (LLM) agents operating within the Vusense organization. These rules apply universally across all repositories and development environments.

---

## 1. Security & Data Privacy (Zero-Trust)

As a Verification-as-a-Service platform, our security posture must be flawless. AI agents operate in a strict zero-trust environment.

* **No Secrets in Prompts:** Never paste, expose, or prompt an LLM with production database credentials, API keys, private cryptographic keys, or customer PII.
* **No Mocking of Security Controls:** Never instruct an agent to mock, bypass, or "stub out" cryptographic signature validations (e.g., ProofMode or Vusense Envelope signatures) for the sake of convenience.
* **Secure Memory (Edge):** AI agents writing code for the Mobile Edge must ensure media is handled in secure/volatile memory, never writing to public directories (like the public Camera Roll) prior to hashing.

## 2. Architectural Mandates

* **Strict Polyrepo Boundaries:** Agents must strictly adhere to the Single Responsibility Principle. Do not cross-pollinate logic. A mobile SDK agent must never write or influence server-side validation logic.
* **The Shared Schema is Law:** All data payloads must conform to the structures defined in the `shared-protocol` repository (e.g., `attestation_schema.json`). Agents must not invent custom data fields or modify the schema without explicit cross-team architectural approval.
* **Event-Driven Handoffs:** Agents working on Core and Ledger services must respect the asynchronous, event-driven boundary (via message brokers) and avoid tightly coupled, synchronous REST calls for blockchain transactions.

## 3. Code Quality & Formatting

* **Documentation is Mandatory:** AI-generated code must be heavily commented. Comments should explain the *why* (business logic and security rationale) rather than just the *what* (syntax).
* **SOLID Principles:** All generated code must follow SOLID object-oriented design principles or equivalent functional programming best practices to ensure modularity.
* **Error Handling:** Silent failures are unacceptable. All agents must implement robust logging and error handling, particularly around network retries (Ledger Adapters) and decryption failures (Core Server).

## 4. Agent Initialization

Before an AI agent begins work on a specific repository, it MUST be initialized with the local `.agent_instructions.md` (or equivalent `.cursorrules` file) located in the root of that project. The local instructions will provide the specific **Persona**, **Tech Stack**, **Tasks**, and **Watch-Outs** for that domain.
