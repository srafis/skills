---
name: azure-ticket-drafting
description: Draft azure boards work items (ticket/bug/user story)
---

# Azure Ticket Drafting

Produce work items that a developer can implement without guessing the expected output. Default to drafting in chat; do not create or change Azure Boards items unless the user explicitly authorizes it.

## Build the evidence base

1. Read the relevant source material supplied or named by the user. This can be requirements, a specification, design, current work item, meeting transcript, MoM, email, spreadsheet, prototype, or repository code.
2. Establish source priority from the user's instruction or the artifacts themselves. If sources conflict and no priority is clear, call it out as an open decision instead of silently choosing.
3. Separate confirmed requirements from assumptions, proposals, future work, and unresolved decisions. Do not turn an inference into a requirement.
4. Record explicit exclusions, dependencies, integration boundaries, and acceptance constraints where they prevent scope creep.
5. When a source artifact defines a canonical field list, workflow, contract, or terminology, preserve it. Do not substitute an implementation-defined version.

## Title standard

Write a title that stands alone. A developer should understand the concrete output without opening the description.

### User Story titles

The **title is the user story sentence**. Use exactly:

`As a …, I need …, so that …`

- Name a real role in the first clause (`CineMotion operator`, `poster-board owner`, `technician`).
- State the need in plain business language in the second clause.
- State the outcome or benefit in the third clause.
- Do not repeat the title as a separate “User story” field in the description.
- Prefer `As a poster-board owner, I need to update from the mobile app without losing my playlists, so that I can stay current without a technician visit` over `Improve updates`.

### Task and Issue titles

Child tasks and issues use verb-led, implementation-output-focused titles:

- Start with a clear verb: `Implement`, `Build`, `Deliver`, `Track`, `Show`, `Move`, or `Prove`.
- Name the resource or surface, the key behavior, and the critical constraint when it changes the work.
- Prefer `Implement the import API with duplicate detection and a review outcome` over `Improve imports`.
- Do not use vague titles such as `Support`, `Improve`, `Update`, `Handle`, `Investigate`, or a source-document heading unless the output is obvious.

## User-story draft format

Use this structure:

1. **Title** — `As a …, I need …, so that …` (this is the Azure Boards title; do not duplicate it elsewhere).
2. **Detailed description** — desired business outcome, end-to-end flow, data created/changed, roles, API behavior, security/reliability constraints, and the one supported creation/mutation path.
3. **In scope** — concrete capabilities and records.
4. **Acceptance criteria** — numbered, observable outcomes. Cover happy path, permissions, invalid actions, conflicts/retries, and data integrity where relevant.
5. **Definition of Done** — implementation evidence: migration/configuration, API/UI, automated tests, security/audit proof, accessibility for UI, and zero-warning quality gate.
6. **Explicitly out of scope** — only meaningful boundaries from the sources.
7. **Child-ticket decomposition** — independently deliverable tasks with outcome-based titles.
8. **Sources** — exact documents and relevant sections.

## Child-task draft format

Make each task independently implementable and testable. Include:

1. **Standalone title**
2. **Description** — precise component/resource, inputs and outputs, data/persistence behavior, routes, permission model, and relevant architecture constraints.
3. **Acceptance criteria** — concrete API/status/data/role outcomes.
4. **Definition of Done** — migration/configuration, implementation, tests, security/audit evidence, and quality commands.
5. **Out of scope** — adjacent work intentionally left to another task or phase.

Use exact API paths, HTTP status codes, entity names, workflow transitions, security rules, transaction boundaries, and retry/idempotency behavior only when supported by the source evidence. If a detail is not specified, label it as a decision rather than asserting it.

## Quality bar

- Use simple English, but retain exact technical names where they remove ambiguity.
- Separate business outcome from implementation mechanism.
- Treat validation, authorization, encryption, auditability, rollback, and idempotency as acceptance criteria when applicable, not vague quality notes.
- For UI tasks, include keyboard access, visible focus, labels, validation messaging, empty/error states, and server-enforced authorization.
- For API/data tasks, include strict schemas, error behavior, unauthorized/out-of-scope behavior, persistence, and automated test cases.
- Do not duplicate a parent story in every child task. Give each task one clear, non-overlapping responsibility.
- Do not make a task about an external-system integration when the source material only requires tracking, manual hand-off, or another narrower behavior.
- Do not add infrastructure, automation, integrations, or process steps that are not supported by the evidence.

## Estimation and hierarchy

- Default hierarchy is the user's stated iteration/sprint → User Story → child Tasks. Do not add Epic or Feature unless requested.
- Estimate child tasks, not the parent story, unless the user asks otherwise.
- Make estimates additive and show the total. If a budget is given, allocate exactly to it.
- When requested, set Original Estimate and Remaining Work to the same initial value on every new task.
- Keep test/quality work visible as dedicated child tasks; do not hide it inside every implementation estimate.

## Publishing to Azure Boards

Publish only after explicit user authorization.

1. Use the `azure-axi` skill and CLI for Azure Boards operations.
2. Use the project from `AGENTS.md` unless the user specifies another project.
3. Never assume the current iteration is the intended sprint. Use the exact iteration path supplied by the user; if the target is ambiguous or has a similarly named sprint, ask before creating anything.
4. Create the User Story first, then create every child Task with that story as parent.
5. Attach the detailed Markdown description, assign requested estimates, and set Remaining Work equal to Original Estimate when requested. If the wrapper cannot set Remaining Work, use the narrow Azure Boards field update only for the newly created task IDs.
6. Verify only the explicitly targeted work items and report the created IDs, hierarchy, iteration, total estimate, and any board-side automation such as state changes.

## Default response

Lead with the draft and state clearly whether Azure Boards was changed. Offer to publish only after the user approves the wording.
