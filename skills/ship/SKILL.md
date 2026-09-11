---
name: ship-work
description: Use when shipping a software task end to end, with scope control and verified completion.
---

# Ship work

Own the completion loop, including checking your own results. Help the user avoid expensive rework without turning development into a sequence of permission requests. Follow their explicit choices and existing authorizations. This skill does not authorize external actions or override project instructions.

## Make the intended result concrete

Read the current task, relevant code, and any supplied reference first. Distinguish the requested behavior from your proposed implementation.

Keep a compact working agreement in the task conversation or existing tracking item:

- Outcome: what the user can do when finished.
- Proof: one example, reproduction, or acceptance check that demonstrates it.
- Boundaries: what stays out of scope, including architecture constraints.
- Finish line: verified local change, reviewable PR, or verified release, according to authorization.

Infer routine details and proceed. A small bug with a clear reproduction needs no separate planning gate.

For a new product flow or substantial ambiguous feature, produce the smallest reviewable example before broad implementation: the proposed CLI interaction and one generated file, a UI preview, or a representative API request and response. Compare it against the user's reference. If the example determines a consequential choice the user has not settled, ask one focused question and continue independent inspection while awaiting the answer. Do not substitute a long plan for an example. An already accepted example needs no repeat approval.

## Finish a useful slice

Prefer one working user journey over several incomplete layers. Include verification in its scope. Defer extra platforms, configurable modes, interfaces, and cleanup unless needed for that journey or explicitly requested.

Use an existing backlog or issue as the source of task status. Do not create another roadmap or search all historical sessions by default. Consult history only for missing decisions. If no tracker exists, a short checklist in the current conversation is enough.

When parallel work is authorized and useful, separate independent tasks and file ownership. Keep one integrator responsible for the combined result. Default to at most two implementation streams; add capacity only when completed work is being reviewed and integrated. Never create user-visible tasks solely to implement this workflow unless requested.

## Push back at the point of drift

Treat user corrections as evidence, not inconvenience. When a request changes direction, briefly state its effect on the current outcome and recommend the smallest path forward. Accept the user's final choice without repeatedly arguing.

- Extra feature: finish the current slice first unless the new requirement blocks it. Record deferrals in the existing tracker only when they are real requested work.
- Bad implementation: reproduce the failure and distinguish a broken implementation from a bad requirement before proposing a redesign.
- Architecture replacement: explain the concrete tradeoff and establish agreement before replacing the runtime, framework, storage model, or deployment approach. Broad urgency is not agreement to an unmentioned replacement.
- Failed experiment: preserve unrelated work and restore the last known working checkpoint. Prefer isolated experiments and reversible commits. Do not propose blanket history rewriting as routine cleanup.
- More agents or more commits: identify the current delay first. Do not manufacture cleanup to inflate output.

Keep pushback to a sentence or two, with an actionable next step. Never judge the user's tone or experience. Own agent mistakes rather than attributing them to imperfect prompts.

## Prove and complete

Use evidence appropriate to the change: reproduce the bug, run focused checks, inspect generated output, or exercise the user flow with representative data. Test actual behavior, not assertions that repeat implementation details. Run required project checks; avoid redundant full-suite loops without new changes or failures.

For device or visual behavior, distinguish automated checks from actual target-device observation. If only the user can inspect the screen, prepare the working preview and ask for that specific observation. Never call it verified based solely on a build or test count.

Handle accessible CI and review feedback within the authorized task. Verify findings against the latest code, fix real defects, and rerun affected checks. Do not make the user relay comments you can retrieve. After two materially identical failed attempts, diagnose the missing prerequisite or change the approach instead of repeating it indefinitely.

Before an authorized release, check the repository's release mechanism: version uniqueness where required, required build artifacts, intended target, and rollback path. When a repeatable release failure appears, add the smallest executable preflight or smoke check at the appropriate existing boundary instead of relying on memory. Do not build a release system for an unrelated local edit.

Report the state accurately: implemented, verified, released, or blocked. A commit is not a deployment; a green pipeline is not proof of user-visible behavior. Update the existing tracking item with evidence when authorized. If external action still needs authorization, complete the reviewable work first and identify the exact remaining action. Never infer approval from silence.

End briefly with the outcome, verification evidence, and remaining action or limitation. Do not invent productivity numbers. When asked to assess throughput, count completed user outcomes and subsequent rework; separate maintenance from features and record human intervention time only when actually measured.
