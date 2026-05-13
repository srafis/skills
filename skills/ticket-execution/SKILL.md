---
name: ticket-execution
description: >-
  Use this skill when working on Azure DevOps tickets that require ticket
  readiness, sprint board hygiene, branch/PR linking, transition comments,
  dev testing, QA evidence, UAT, time tracking, and client-ready updates.
---

# Azure Ticket Execution

Use this skill when work is tied to an Azure DevOps work item, sprint board,
branch, pull request, QA handoff, UAT, or client status update.

## Core Principles

- Make ticket status, ownership, estimates, links, and evidence visible in Azure Boards.
- Do not start implementation until the ticket has enough structure for another reader to understand what will be built and how it will be accepted.
- Add a transition comment on every state change. Include why the state changed, relevant evidence, risks, dependencies, and next owner.
- Keep Original Estimate, Completed/Spent Time, Remaining Time, and Target Completion current.
- Link the branch, PR, related work items, bugs, and parent/child relationships to the ticket.
- Fix issues found during developer self-testing directly on the same ticket.
- Create and link bug work items for issues found by QA, TL/peer review, PO, or client during UAT.
- Keep Clockify/time tracking current during daily work and weekly checks.
- Keep client-facing communication business-focused, concise, and decision/action oriented.

## Ticket Readiness Before Active

Before moving a work item to `Active`, confirm or create the following:

- Title: short verb phrase. It may include a status flag such as `[Blocked]` when applicable.
- Type: Epic, Feature, User Story, Task, Bug, or Impediment.
- Priority and due date.
- Estimate in hours or story points.
- Description in the form: `As a <role> I want <capability> so that <benefit>.`
- Acceptance Criteria: numbered, testable lines, each one or two sentences.
- Pseudocode / Technical Approach: 3-10 bullets.
- TL approval: comment or tag confirming the approach.
- Category: Development, Deployment, QA, Discussion, Requirements, or Impediment.
- Tags: meaningful module, technology, environment, or release tags.
- Parent and relations: correct parent plus child or related links where needed.
- Links: Sifars standards, HLD/LLD, API contracts, designs, or other relevant references.
- Time fields: Original Estimate, Completed/Spent Time, Remaining Time, Target Completion.
- Ticket-level Definition of Done.

If a required field is missing and the information is available, update the
ticket. If the information requires a decision, ask for the decision or leave a
ticket comment requesting it before implementation starts.

## Ready To Active

- Pick the highest-priority or nearest-due item in the sprint unless a specific ticket is assigned.
- Read the Description, Acceptance Criteria, Definition of Done, links, pseudocode, estimates, and relations.
- Confirm the estimate exists.
- Confirm category, tags, parent, related links, and time fields.
- Confirm pseudocode / technical approach has TL approval.
- Create a git branch from `develop` on the local machine.
- Name the branch with ticket number and short title, for example `feature/EXE-128-otp-login`.
- Link the branch to the ticket.
- Move the ticket to `Active`.
- Add a transition comment similar to:
  `Starting work; branch <branch> from develop; AC/DoD reviewed; pseudocode approved by <TL>; ETA <date/TBD>.`

## Active Development

- Develop strictly against the Description, Acceptance Criteria, and Definition of Done.
- Test locally after meaningful changes.
- Fix developer-found issues directly on the same ticket.
- Do not create bug tickets for issues found and fixed during developer self-testing.
- Comment important decisions, deviations, scope changes, risks, and blockers with who/why/what.
- Keep Completed/Spent Time, Remaining Time, and Target Completion current.
- At end of day, push code, update board state, update time fields, and add any necessary comments.

## PR And Review

When local implementation and self-testing satisfy the ticket:

- Create a PR linked to the ticket.
- Keep the PR title and description short and factual, referencing scope and Acceptance Criteria.
- Assign the PR to the TL/peer reviewer.
- Assign the ticket to the reviewer while it is in `Review`.
- Move the ticket to `Review`.
- Add a transition comment similar to:
  `PR #<id> opened; unit tests green; assigned to <reviewer>; moving to Review.`

When review feedback arrives:

- Resolve all review comments.
- If a reviewer-found issue requires tracked work, create/link a bug according to the bug policy.
- Keep the ticket assigned to the appropriate owner at each step.

## Merge, Dev Deploy, And Developer Testing

After the PR is approved and comments are resolved:

- Assign the ticket back to the developer.
- Merge to the target branch.
- Deploy to the dev instance.
- Capture the build/deploy ID.
- Add a comment similar to:
  `PR approved; merged; dev deploy <build-id>; reassigned to self.`
- Move the ticket to `Testing` for developer testing on the dev instance.
- Add a transition comment similar to:
  `Merged to develop; dev build <build-id>; starting developer testing on dev (AC/DoD baseline).`
- Run smoke and functional checks on dev until Acceptance Criteria and Definition of Done are met with zero developer-found issues.
- Keep time fields current.

## QA Loop

When developer testing passes:

- Move the ticket to QA or assign it to QA while in `Testing`, depending on the board setup.
- Assign the ticket to the QA person.
- Leave a directed handoff comment with scope, environment/build, test notes, and risks.
- QA tests independently and attaches evidence such as screenshots, videos, logs, or test reports.

If QA finds issues:

- Log bug work items.
- Set the same parent as the original Story/Feature.
- Link bug <-> ticket.
- Attach evidence.
- Assign the ticket back to the developer.
- Cycle through Active -> Review -> Testing until no QA-found bugs remain and AC/DoD hold on dev.
- QA re-tests, updates evidence, and confirms clean.

## UAT Loop

After QA is clean with evidence:

- Move the ticket to `UAT`.
- PO/client validates the increment.
- If PO/client finds issues, log bug work items with the same parent and link them to the ticket.
- Cycle UAT-found fixes through Active -> Review -> Testing -> QA as needed.
- Move to `Done/Completed` only after UAT passes or PO accepts documented deviations.

## Done Checklist

Before moving to `Done/Completed`, confirm:

- PR(s) merged.
- CI green.
- Dev deployment complete.
- QA evidence attached.
- All non-accepted bugs closed.
- UAT passed or accepted deviations are documented.
- Time logged.
- Release notes updated if needed.

Final comment:

```text
Completed; DoD met; release notes updated.
```

## Switching Work, Pauses, And Blockers

- If asked to pause and switch to another ticket, comment the reason.
- Link the new ticket as Related.
- Update Remaining Time and Target Completion.
- Note due-date impact as old -> new.
- For Blocked, On Hold, Paused, or Discuss states, prefix the title with a square-bracket flag such as `[Blocked]`.
- Do not continue development while a flag remains.
- Remove the flag and comment when the issue is resolved.

## Daily And Weekly Discipline

During daily standups, keep these items current:

- Yesterday's committed work and whether it was delivered.
- Today's planned delivery.
- Needed support, blockers, and dependencies.
- Current sprint/project goal awareness.
- Board status.
- Estimates and time fields.
- Items that were added after initial planning.
- Clockify/time tracking.
- Daily client update status.

Weekly checks:

- Monday: confirm the board is updated, sprint is ready/planned, and spillovers are explained.
- Thursday: confirm internal demo, management/sales invites if needed, client demo invite, and client acceptance/reminder.
- Friday: confirm retrospective, weekly report, next sprint planning, UAT email, dev/staging deployment, QA testing, Clockify, weekly status email, and demo recording.

If new work is added after sprint planning, discuss it with the team. If it adds effort,
shift equivalent effort to a later sprint and inform the team/client.

## Two-Week Sprint Cadence

- Day 0, Friday before sprint: select backlog items, agree sprint goal, confirm/refine DoD, estimate stories, finalize committed backlog in Azure Boards.
- Every working day, Monday through Thursday: 15-minute standup, progress, today's plan, blockers, board update, impediment log.
- Day 4, Week 1 Friday AM: internal demo/dry-run, validate completed stories against DoD, note gaps/defects, assign quick fixes, tick Demo Ready checklist.
- Day 5, Week 1 Friday PM: optional backlog refinement, split or re-estimate upcoming stories, ensure candidate stories have Acceptance Criteria.
- Day 7, Week 2 Tuesday EOD: code complete / merge freeze, development tasks finished, only approved PRs merged to `develop`, CI build and automated tests green.
- Day 8, Week 2 Wednesday: QA and regression testing, log and retest defects.
- Day 9, Week 2 Thursday AM: final internal demo/dry-run, confirm stories remain Done.
- Day 9, Week 2 Thursday midday: prepare sprint report and record a 3-5 minute demo video.
- Day 9, Week 2 Thursday PM: client sprint review/demo, share report and video link, capture feedback/change requests.
- Day 9, Week 2 Thursday late PM: send UAT kickoff email with demo video, UAT checklist, environment link, UAT window, and feedback channel.
- Day 9, Week 2 Thursday EOD: tag release, deploy to staging/production, and publish release notes if shippable.
- Day 10, Week 2 Friday AM: retrospective, agree 1-2 concrete improvement actions with owners and due dates.
- Day 10, Week 2 Friday PM: next sprint planning, reconfirm capacity, sprint goal, and initial estimates.

Asynchronous UAT: the Product Owner monitors client feedback during the 1-2 week UAT
window and schedules fixes in future sprints.

## Client Updates, MOMs, And Clarification Tracking

Client-facing updates:

- Write for a non-technical client reader.
- Explain what changed, what value is now available, what is planned next, and what is blocking progress.
- Avoid unnecessary internal terminology such as backend, frontend, API, component, framework, ticket, or task.
- Use technical detail only when the client explicitly needs it.
- Convert implementation details into business outcomes.
- Group daily and weekly updates by product area or workflow.
- Include completed progress, current work, next tasks, and client inputs needed.

MOMs:

- Keep MOMs short and decision-focused.
- Capture key discussion points, business/domain decisions, action items, and important clarifications.
- Avoid long call transcripts.
- Keep key decisions separate from the action-item table.
- Record action items with action, owner, and ETA/status.
- Do not commit exact dates such as "tomorrow", "by Friday", or calendar dates unless approved.
- Use TBD or broad timelines while timing is being evaluated.

Clarification tracker:

- Create one Excel workbook per project when open questions, blockers, or pending client inputs need tracking.
- Store it in SharePoint or the agreed shared location when client access is required.
- Treat it as the single source of truth for clarifications.
- Use columns: Date Raised, Clarification / Question, Client Answer, Assigned To, Priority, Status, Notes / Comments.
