---
name: work
description: >-
  Runs an Azure ticket delivery loop: fetch tickets, plan against design docs,
  implement via sub-agents, record before/after videos, run quality gates and
  CodeRabbit, then post ticket comments and commit only when asked. Use when
  the user says /work, names an Azure ticket or user story, or asks for a
  before/after video or ticket comment.
disable-model-invocation: true
---

# Work

Azure ticket loop. Not auto-PR / Clockify / develop-sync unless asked.

If the repo has `.agents/skills/ponytail/SKILL.md`, read it and run **ultra**. Else skip. Smallest diff; reuse; YAGNI.

Copy and track:

```
- [ ] 1 Tickets
- [ ] 2 Plan + ALIGNED check (no code until confirmed)
- [ ] 3 Before video (HEAD worktree)
- [ ] 4 Implement via sub-agents
- [ ] 5 After video
- [ ] 6 Quality gates
- [ ] 7 Azure comments (only if asked)
- [ ] 8 Commit (only if asked)
```

## 1. Tickets

If the user did not give ids/titles, **ask**. Do not guess.

- Project: `AGENTS.md` → `Project name over azure board: \`...\``; else Azure DevOps CLI defaults / `--project`.
- `az boards work-item show --id <id> --org <org> --expand relations`. Query children using WIQL hierarchy-forward or the returned relations.
- Every `az` call needs full access to `~/.azure/` (sandbox without it fails).

## 2. Plan — don't code yet

If plan mode is on, or until the user confirms: **plan only**.

1. Map ticket ACs to `docs/hld.md` + `docs/lld.md` if present; else whatever the repo names as design. Open other design docs only if that mapping is incomplete.
2. Spin a **validation subagent** (model: latest Opus **only if the user asked**; else `inherit`) to mark each AC **ALIGNED** vs **scope creep**. Fold findings into the plan.
3. Skip work the docs/tickets exclude. **Don't invent open design confirmations.**
4. If code and design disagree: resolve it (amend the design) — root `CLAUDE.md` if present. Never silently diverge.

## 3. Before video first

Record **before** the main tree is edited (or in parallel from a worktree — never after).

```bash
git worktree add /tmp/$(basename "$(git rev-parse --show-toplevel)")-us-<id>-before HEAD
```

Playwright `recordVideo`, or isolated Vite/API (or equivalent) ports if the main servers use SSO that blocks e2e tokens. Match the e2e config's auth, not production SSO.

Save `tmp/us-<id>-before.webm` (gitignored via `tmp`). Same viewport/framing as the later after video.

## 4. Implement via sub-agents

Read component `CLAUDE.md` **before** touching that tree. Tests live where that file says — do not assume a tests path.

Split by ownership when files **don't collide** (e.g. backend vs frontend). **One** agent if files overlap. Don't launch a duplicate of a running agent.

Implementation agents **skip full e2e**. A later gates agent runs format/lint/typecheck/test.

Ponytail ultra (if loaded): reuse existing modules; no new deps; no hand-written CRUD a generator already owns.

## 5. After video

Matching `tmp/us-<id>-after.webm` of the **NEW** UI. Same framing as before.

## 6. Quality gates

Repo `AGENTS.md` quality bar if present (often: not done with any error/warning).

Commands from component `CLAUDE.md` / package scripts — `format`, `lint`, `typecheck`, `test`. Use whatever the repo uses (`pnpm`, `npm`, `yarn`, `cargo`, `go`, …). Don't assume `pnpm`.

Zero warnings. E2E only if cheap/possible. **Don't fail the story solely on skipped e2e** when SSO blocks e2e tokens.

## 7. Azure comments — only when asked

If the user asks for comments **and** commit: **comments first, then commit**.

Resolve byline at runtime: `AZURE_DEVOPS_USERNAME`, else `git config user.name`. Model = the actual model name for this run. Every comment starts with this blockquote:

```
> Commented on behalf of <AZURE_DEVOPS_USERNAME or git user.name>. By <actual model name>.
```

Then: what exists now, what didn't before, what we fixed, out of scope, process steps (design-doc check, scope-creep check, gates, CodeRabbit, videos), rough **token estimates** (order-of-magnitude, labeled as estimates).

- Parent story = e2e walkthrough + **collective** tokens.
- Children = that slice only.

Attach before/after videos using Azure attachment REST (`az rest` upload + `AttachedFile` relation), full `~/.azure/` access:

```bash
# org from Azure DevOps CLI defaults / git remote; project from §1
URL=$(az rest --method POST \
  --uri "https://dev.azure.com/<org>/<project>/_apis/wit/attachments?fileName=us-<id>-before.webm&api-version=7.1" \
  --headers "Content-Type=application/octet-stream" \
  --resource "@tmp/us-<id>-before.webm" \
  --query url -o tsv)
az rest --method PATCH \
  --uri "https://dev.azure.com/<org>/_apis/wit/workitems/<wid>?api-version=7.1" \
  --headers "Content-Type=application/json-patch+json" \
  --body "[{\"op\":\"add\",\"path\":\"/relations/-\",\"value\":{\"rel\":\"AttachedFile\",\"url\":\"$URL\",\"attributes\":{\"comment\":\"before demo\"}}}]"
```

Same pair on **parent and children**, with a note that the recording is the **whole story**.

Post comments through the Azure DevOps Comments REST API using the authenticated Azure DevOps client. Preserve paragraph and list spacing, and verify the posted comment before assuming it rendered correctly.

## 8. Commit — only when asked

Never commit unless the user asks. Never push unless asked. No `git config`, no `--no-verify`, no `--amend` unless the user's git protocol allows it. Don't commit `.env` or `tmp/*.webm`.

**Before commit:** repo `.agents/skills/code-review/SKILL.md` if present; else `coderabbit review --agent`. Fix real Critical/Warning; skip false positives.

HEREDOC message. State **process steps done**: design-doc check, scope-creep validation, gates, CodeRabbit, Azure comments if already posted. Small atomic commits.

## Lookups

| Where | Rule |
| --- | --- |
| `AGENTS.md` | Azure project; quality bar; commit rules |
| Root `CLAUDE.md` | code vs design → resolve, don't silently diverge |
| Component `CLAUDE.md` | test paths, scripts, module reuse |
| `docs/` | `hld.md` / `lld.md` if present; else the repo's design names |
| Ponytail | `.agents/skills/ponytail/SKILL.md` if present |
| CodeRabbit | `.agents/skills/code-review/SKILL.md` if present; else CLI |

## Don't

- Silently rewrite Azure ACs
- Add schema that contradicts the ERD/design
- Push (unless asked)
- Create extra docs unless asked
- Scope-creep: skip work the docs/tickets exclude; don't invent open design confirmations
