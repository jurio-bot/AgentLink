# AgentLink

**Persistent, permissioned, recoverable execution infrastructure for AI workers.**

> **Free starting point:** [AI Automation Readiness Checklist](./FREE_AI_AUTOMATION_READINESS_CHECKLIST.md)
>
> **DIY planning kit:** [AI Automation Quickstart Kit — ¥980](./DIGITAL_PRODUCTS.md)
>
> **Start small:** [AI Automation Opportunity Scan — ¥2,980](https://buy.stripe.com/14AdR8dBAd38g77f0TgEg06)
>
> **Need a technical second opinion?** [AI Agent / RAG Architecture Quick Audit — ¥9,800](https://buy.stripe.com/00w7sK7dc4wCf33f0TgEg05)
>
> **Want a working proof?** [AI Automation Small PoC Starter — ¥29,800](https://buy.stripe.com/eVq9AS8hg8MS6wxbOHgEg07)
>
> **Support AgentLink:** [Flexible project support](https://buy.stripe.com/7sYeVcbtsgfk6wxbOHgEg00) · [Supporter ¥500/mo](https://buy.stripe.com/00w6oG7dc9QW7ABg4XgEg01) · [Builder Patron ¥1,500/mo](https://buy.stripe.com/eVq14m4102oubQR6ungEg02) · [Infrastructure Patron ¥5,000/mo](https://buy.stripe.com/dRm6oG554d385stf0TgEg03)
>
> Support is non-equity project/patron support. It does not provide shares, investment returns, tokens, tax-deductible charitable treatment, exclusivity, or rights to AgentLink core IP.

AgentLink is an early-stage AI execution platform exploring how AI agents can continue useful work across computers, mobile/edge devices, cloud workers, and business services without losing execution state, authority boundaries, or recovery context.

> This repository is a public product / technical showcase. The production core is private and is **not** published here.

## Revenue-ready service ladder

AgentLink currently offers a low-friction path from first assessment to implementation:

0. **Free AI Automation Readiness Checklist**  
   [Use the checklist](./FREE_AI_AUTOMATION_READINESS_CHECKLIST.md)  
   A conservative 20-point preflight for workflow clarity, access, reliability, and business fit.

1. **AI Automation Quickstart Kit — ¥980**  
   [See the kit](./DIGITAL_PRODUCTS.md)  
   DIY scorecard, PoC planning canvas, API preflight, reliability/recovery checklist, and ROI estimator.

2. **AI Automation Opportunity Scan — ¥2,980**  
   [Buy now](https://buy.stripe.com/14AdR8dBAd38g77f0TgEg06)  
   Async review of one workflow or idea with automation candidates, difficulty, risks, and next actions.

3. **AI Agent / RAG Architecture Quick Audit — ¥9,800**  
   [Buy now](https://buy.stripe.com/00w7sK7dc4wCf33f0TgEg05)  
   Architecture review, risk checklist, quality/operability gaps, prioritized next steps, and implementation plan.

4. **AI Automation Small PoC Starter — ¥29,800**  
   [Buy now](https://buy.stripe.com/eVq9AS8hg8MS6wxbOHgEg07)  
   One narrow, non-production workflow: requirements, boundary definition, small executable prototype, basic validation, and handoff notes. Production deployment, ongoing operation, extra integrations, and large-scale data work are outside this fixed scope.

5. **Larger Python / API / RAG / multi-agent PoCs**  
   See [SERVICES.md](./SERVICES.md) and [request a paid service or PoC](../../issues/new?template=paid-service-request.yml).

## Why AgentLink exists

AI models are becoming strong planners and tool users. Real operational work still becomes fragile when it crosses sessions, devices, networks, services, and authorization boundaries.

AgentLink focuses on the layer between **AI reasoning** and **reliable execution**:

- durable work continuity
- heterogeneous worker orchestration
- failure recovery and route failover
- scoped approvals and authority
- action receipts and operational state
- parallel worker coordination

## Concept

```mermaid
flowchart LR
    A[AI / Agent] --> B[AgentLink Execution Layer]
    B --> C[Local PC Worker]
    B --> D[Mobile / Edge Worker]
    B --> E[Cloud Worker]
    B --> F[Business Services]
    B --> G[Approval / Policy Gate]
    C --> H[Receipts + State]
    D --> H
    E --> H
    F --> H
    G --> H
    H --> B
```

The goal is not to replace foundation models. AgentLink is intended to make multiple models and agents more useful by giving them a persistent execution substrate.

## What is already being explored

The private implementation currently spans several directions, including:

- Android / PC / gateway integration
- persistent sessions and job state
- local and cloud worker execution
- execution receipts and replay concepts
- capability leases and worker availability
- failure recovery and stale-owner recovery
- multi-route execution
- permission / approval boundaries
- parallel work lanes and conflict-control research

Only claims that can be backed by implementation evidence are used in external discussions.

## First public technical demo

A deliberately simplified, standalone reliability demo is now public:

**[Receipt Replay Simulator](./demos/receipt-replay-simulator/)**

It demonstrates a conservative recovery rule for interrupted actions:

- completed receipt → skip duplicate execution
- not-started receipt → retry
- uncertain receipt → reconcile instead of blindly replaying

The demo is intentionally separate from production AgentLink and contains no private infrastructure or authorization implementation.

## Validated services and case study

AgentLink is also turning selected verified capabilities into small paid engineering offers without publishing the private production core.

- **[AI automation / RAG / agent service scopes](./SERVICES.md)**
- **[Request a paid service or PoC](../../issues/new?template=paid-service-request.yml)**
- **[RAG Fleet Harness MVP case study](./CASE_STUDY_RAG_FLEET.md)** — 10 isolated agent configurations with routing, validation, health reporting, and **5 automated tests passed**

Public claims are limited to work that has implementation or test evidence. Larger PoCs require scope confirmation before work begins.

## Company thesis

AgentLink is also being developed around an **AI-native company** thesis: use the platform internally as the operating substrate for AI workers before commercializing selected capabilities externally.

Human operators remain responsible for legal accountability, governance, sensitive approvals, and other actions that require human authority.

The intended company structure and legal entity are still being prepared. `AgentLink` is currently used here as the project / product name.

## Enterprise design-partner PoCs

We are exploring three initial paid PoC patterns:

1. **Persistent AI Operations Worker**
   - multi-step business workflow
   - interruption recovery
   - measurable reduction in manual intervention

2. **Secure Agent Execution Gateway**
   - controlled execution environment
   - scoped action permissions
   - approval and audit receipts

3. **Multi-Agent Business Operations Cell**
   - coordinated workers around one narrow objective
   - explicit lane ownership
   - conflict and duplicate-work reduction

See [POC.md](./POC.md).

## R&D themes

Current technical questions include:

- how to fail over without duplicating external side effects
- how authority should survive, narrow, expire, or revoke across worker migration
- how to recover long-running jobs without replaying already-completed actions
- how parallel workers coordinate without globally serializing all useful work
- how execution state stays compact enough for long-horizon operation

See [ARCHITECTURE.md](./ARCHITECTURE.md) and [TECHNICAL_PROOFS.md](./TECHNICAL_PROOFS.md).

## What is intentionally not public

The following remain private:

- production source code
- internal endpoints and host information
- credentials, tokens, secrets, and private URLs
- detailed authorization implementation
- customer / user data
- internal operational runbooks that would materially increase attack surface

See [SECURITY.md](./SECURITY.md).

## Current stage

AgentLink is in an early product / pre-seed stage. Priorities are:

- repeatable third-party onboarding
- enterprise security hardening
- measurable reliability tests
- design partners and paid PoCs
- company / IP structuring
- non-dilutive R&D funding and seed financing

See [ROADMAP.md](./ROADMAP.md).

## Looking for

- enterprise design partners with a safe, measurable AI-agent workload
- AI infrastructure / enterprise software investors
- individual patrons and long-term supporters
- corporate sponsors and strategic patrons
- cloud / compute / model ecosystem partners
- hardware, GPU, cloud-credit, and security-review support
- technical collaborators interested in reliable agent execution

## Support, patronage, and sponsorship

Live support channels are open:

- **Flexible project support:** [choose an amount](https://buy.stripe.com/7sYeVcbtsgfk6wxbOHgEg00)
- **Supporter:** [¥500 / month](https://buy.stripe.com/00w6oG7dc9QW7ABg4XgEg01)
- **Builder Patron:** [¥1,500 / month](https://buy.stripe.com/eVq14m4102oubQR6ungEg02)
- **Infrastructure Patron:** [¥5,000 / month](https://buy.stripe.com/dRm6oG554d385stf0TgEg03)

AgentLink also welcomes corporate sponsorship, cloud / GPU credits, hardware, security or legal support, introductions, and design-partner collaboration.

These channels are for non-equity support. They are not presented as charitable donations and do not imply tax deductibility, equity, investment returns, tokens, exclusivity, or rights to AgentLink core IP.

See [SUPPORT.md](./SUPPORT.md) for details.

## Contact

For investment, partnership, sponsorship, patronage, design-partner discussions, or a non-confidential automation / AI engineering inquiry, open a GitHub Issue or contact the project owner through the GitHub profile associated with this repository.

Do not post credentials, API keys, personal data, proprietary datasets, or other confidential information in a public issue.

## Repository status

This public repository is a **showcase and documentation repository**, not the production AgentLink source tree.

No license is granted to unpublished AgentLink core code. Content in this repository remains subject to the terms in [NOTICE.md](./NOTICE.md).