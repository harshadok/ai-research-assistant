# AI Research Assistant

**Status: Planning / documentation only.** This repository currently contains a project specification and implementation roadmap. No working application, provider integration, deployment, or measured results are included yet.

A personal learning project by [Harshad Odakkal](https://github.com/harshadok), building on professional Flutter and mobile engineering experience while transitioning toward AI/mobile engineering.

## Problem and goal

Help users investigate a question and review a concise research brief with traceable sources and clearly identified uncertainty.

## Skills to practise

- Search integration
- AI agents
- Source verification
- Citation tracking
- Evidence-based synthesis

## Planned end-to-end workflow

1. Accept a research question and a bounded research budget.
2. Generate focused search queries and retrieve candidate results.
3. Fetch accessible source pages and record titles, URLs, and retrieval timestamps.
4. Use a bounded agent workflow to collect and compare supporting evidence.
5. Check that each factual statement has relevant source support and flag contradictions.
6. Present a research brief with citations and unresolved questions.

## Proposed architecture

Flutter research and source viewer; Python API service; search provider adapter; page extraction adapter; LLM agent workflow; evidence store.

The stack is a design proposal. Specific providers, libraries, model versions, and database products will be selected and documented during implementation.

## Planned API surface

- `POST /research` — start a bounded research job
- `GET /research/{id}/status` — inspect progress and budget usage
- `GET /research/{id}/brief` — retrieve the brief and citations
- `GET /research/{id}/sources` — inspect collected evidence

These endpoints are proposed contracts; they are not implemented.

## Core data model

ResearchJob(question, limits, status); Source(url, title, retrieved_at, excerpt); Claim(text, source_ids, verification_state); Brief(summary, claims, uncertainties).

## Flutter/mobile experience

Research question form, progress indicator, brief reader, source cards, and claim-to-evidence navigation.

## Evaluation and acceptance plan

- [ ] Verify cited URLs resolve and cited passages support the associated claims.
- [ ] Test conflicting sources, inaccessible pages, and questions with insufficient evidence.
- [ ] Enforce search, model-call, time, and token budgets.
- [ ] Check that instructions embedded in retrieved pages cannot trigger unintended tools.
- [ ] Assess claim support and source coverage on a small manually reviewed dataset.

No accuracy, latency, cost, or reliability results have been measured. Results will be added only after reproducible runs.

## Implementation roadmap

- [ ] **Milestone 1:** Build search retrieval and store source metadata.
- [ ] **Milestone 2:** Add page extraction and a claim-to-source evidence model.
- [ ] **Milestone 3:** Implement a bounded search, read, and synthesize agent workflow.
- [ ] **Milestone 4:** Add citation checks, contradiction handling, and a Flutter brief viewer.
- [ ] **Milestone 5:** Publish sample briefs and a manually reviewed verification report.

## Planned demonstration

Research a narrow question using public sources, inspect evidence for individual claims, and demonstrate how conflicting information is displayed.

## Data and operational boundaries

Treat retrieved pages as untrusted data. Restrict fetched destinations, avoid private-network access, and label unsupported claims and uncertainty.

## Getting started today

1. Read the proposed workflow and choose the first milestone.
2. Decide on providers and local development tools; record those decisions before implementation.
3. Add application code and a reproducible setup guide as the first milestone is built.
4. Use synthetic or public test data and keep credentials outside version control.

**There is no runnable quick start yet.** Installation and run commands will be added when code exists.

## Suggested future layout

```text
apps/mobile/        # Planned Flutter client
services/api/       # Planned application API
evals/              # Planned fixtures and evaluation runs
docs/               # Architecture decisions and demonstration notes
```

These directories describe the intended structure and have not been implemented.

## Portfolio context

This is an independent planned portfolio project, not client work or a production deployment. Its current scope is documentation; update the status and roadmap as working milestones are completed.
