# AgentLink Services

AgentLink offers selected implementation and architecture work based on capabilities that are already exercised inside the private AgentLink engineering environment.

This page is intentionally conservative: it describes work we can actually scope, prototype, test, and hand off. It does not claim customer outcomes that have not happened.

## 1. AI Agent / RAG Architecture Quick Audit

**Reference price: ¥9,800**

Good fit when you already have an AI-agent or RAG idea and want a concrete technical second opinion before building more.

Typical deliverables:

- architecture review
- retrieval / agent risk checklist
- quality and operability gaps
- prioritized next steps
- implementation plan

Implementation is not included at this tier.

## 2. AI Automation / Small PoC

**Reference price: ¥29,800**

Typical scope:

- one narrow workflow or repetitive process
- requirements and boundary definition
- small executable proof-of-concept
- basic validation
- handoff notes

Examples include Python utilities, API-connected workflow prototypes, prompt/agent routing proofs, and small internal automation helpers.

## 3. Working Python / API / RAG PoC

**Reference price: ¥59,800**

Typical scope:

- executable Python prototype
- API or data-source integration where appropriate
- RAG / retrieval or agent logic
- validation and failure-path checks
- documented run instructions

## 4. Multi-step AI Agent / RAG PoC

**Reference price: ¥98,000**

Typical scope:

- multiple coordinated steps or agents
- explicit routing and state boundaries
- validation / health design
- duplicate-action and recovery considerations
- implementation and handoff documentation

## Verified internal proof: RAG Fleet Harness MVP

A dependency-light Python MVP was built and validated for operating **10 isolated RAG agents behind one harness**.

Verified behaviors:

- 10-agent configuration and fleet health reporting
- isolated retrieval by agent ID
- deterministic local retrieval proof
- source-aware run results
- unknown-agent handling
- validation for invalid fleet configuration
- **5 automated tests passed**

The MVP deliberately keeps vector-store and model-provider dependencies outside the core harness so the operating contract can be tested first. Production adapters can be added later.

This is an engineering proof, not a claim that the simplified local retriever itself is a production RAG stack.

## How to inquire

Open a GitHub Issue in this repository with a **non-confidential** description of:

1. what you want to automate or build
2. current tools / data sources
3. desired output
4. deadline or urgency
5. security / deployment constraints

Please do not post passwords, API keys, personal data, proprietary datasets, or other confidential information in a public issue.

Reference prices are starting points, not automatic contract terms. Scope and final terms must be confirmed before work begins.

---

## 日本語

AgentLinkでは、実際に検証済みの技術資産をベースに、AI業務自動化、Python/API連携、RAG・AI AgentのPoC、設計レビューを提供します。

公開ページでは、未検証の実績や架空の導入効果は記載しません。

相談はこのリポジトリのGitHub Issueから、機密情報を含めずに概要だけお送りください。
