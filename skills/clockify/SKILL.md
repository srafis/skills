---
name: clockify
description: >-
  Manage Clockify timers, time entries, and tags, and summarize a user's
  tracked time. Use when Clockify is named or established as the time-tracking
  service. Excludes general timers and unrelated reporting.
---

# Clockify

## Execution and configuration

Use the bundled `scripts/clockify_api.py` with Python 3.10+. Resolve its absolute
path relative to this loaded SKILL.md, regardless of which agent installed it.
In the examples below, `$CLOCKIFY_HELPER` means that resolved script path.

- Required for API access: `CLOCKIFY_API_KEY`. The helper also needs a workspace
  ID, supplied through `CLOCKIFY_WORKSPACE_ID` or `--workspace-id` after resolution.
- Optional: `CLOCKIFY_USER_ID`, `CLOCKIFY_PROJECT_ID`.
- Keep the API key in the environment. Never print it or request it in chat.
  If absent, ask the user to configure it locally.
- The agent may read IDs from applicable `AGENTS.md`; the helper does not parse
  that file. Pass discovered values as `--workspace-id` / `--user-id` /
  `--project-id-default` **before** the subcommand, or set their environment variables.
- Explicit user selection takes precedence over defaults in applicable `AGENTS.md`,
  then environment defaults. Ask only when the required selection remains ambiguous.
- Without a user ID, user-entry reads discover the API-key owner. Start and stop
  validate that a configured user is the owner before changing their timer.
  Starting/stopping another user's timer is unsupported.

## Resolve workspace and project

- Read applicable `AGENTS.md` files for workspace IDs, project IDs or name mappings,
  and local time-entry conventions. Keep those details in the user's configuration;
  never embed personal IDs or conventions in this reusable skill.
- If the workspace is unknown, use a read-only `GET /workspaces` request. Match the
  workspace the user named, or use the only available workspace. Ask if several
  remain possible; do not silently choose one.
- If the user gives a project name, use a matching mapping from applicable
  `AGENTS.md`, or fetch `GET /workspaces/{workspaceId}/projects` from Clockify.
  Follow pagination through all results needed to establish a unique exact name
  match. Resolve the name within the selected workspace, not across workspaces.
- Verify a configured project ID with
  `GET /workspaces/{workspaceId}/projects/{projectId}` before its first use in a task.
  Reject archived projects for new timers. Reuse verified IDs for the rest of the task.
- If no exact match exists or several projects match, show the relevant choices
  and ask. Never invent an ID, choose a fuzzy match silently, or create a project
  merely to resolve a name.
- These discovery endpoints are not helper subcommands. Use scoped read-only API
  requests with the API key from the environment, then pass the resolved IDs to
  the helper. Do not print credentials.
- A project is optional unless the user or workspace requires one. Use a resolved
  default when available; ask only if a required project is unresolved.

## Commands

```bash
python3 "$CLOCKIFY_HELPER" start --description "Work description" --project-id "<id>"
python3 "$CLOCKIFY_HELPER" stop
python3 "$CLOCKIFY_HELPER" list --start "2026-04-01T00:00:00Z" --end "2026-04-02T00:00:00Z"
python3 "$CLOCKIFY_HELPER" list --in-progress true
python3 "$CLOCKIFY_HELPER" get --id "<entry-id>"
python3 "$CLOCKIFY_HELPER" update --id "<entry-id>" --description "Updated description"
python3 "$CLOCKIFY_HELPER" update --id "<entry-id>" --clear-tags
python3 "$CLOCKIFY_HELPER" list-tags --name "<tag-name>"
python3 "$CLOCKIFY_HELPER" create-tag --name "<tag-name>"
python3 "$CLOCKIFY_HELPER" delete --id "<entry-id>"
python3 "$CLOCKIFY_HELPER" in-progress
```

- `start` and `update` accept `--project-id`, `--billable true|false`, repeatable
  `--tag` names and `--tag-id` IDs. Creating missing tags with
  `--create-missing-tags true` requires that tag creation be within the user request.
- `update` reads the existing entry and preserves unspecified supported fields,
  including start/end, project, task, billable state, tags, and entry type.
  Supplied tags replace the tag list; `--clear-tags` explicitly empties it.
  `--description ""` clears the description. `--start` and `--end` change times.
  Reopening a completed entry and clearing its project are not supported.
- `list`, `list-tags`, and `in-progress` fetch every page by default.
  `--page N` requests only that page; `--page-size N` controls batch size.
  Never present a single requested page as a complete total or workspace snapshot.
- Use the user's requested description and tags, or conventions explicitly defined
  in applicable `AGENTS.md`. Do not impose a ticket format or default tag.

## Workflow and verification

1. Resolve the requested workspace, project, date range, and user. Use explicit
   user choices before defaults. Do not guess IDs or silently switch workspaces.
2. Read the running timer before starting one. If one exists, report it and resolve
   whether the user wants to stop/switch it; a start request alone does not authorize
   stopping unrelated work. Fetch a deletion target and verify its identity first.
3. Make only requested changes. After a successful start, stop, or update, re-read
   the returned entry ID with `get` and check the requested fields. After deletion,
   verify the target is absent, distinguishing not-found from permission/network errors.
4. Report affected IDs and verified results concisely. If verification fails, say
   the write may have succeeded. Never retry an uncertain write automatically.

## Reporting and limits

- Reporting covers one user's entries and local duration aggregation. Team-wide
  analytics and the dedicated Reports API are not implemented.
- Resolve the user's IANA timezone from explicit input, applicable `AGENTS.md`,
  or their Clockify profile; ask if unknown. Convert with Python `zoneinfo` using
  the date's offset rather than assuming whole hours.
  Send timezone-aware ISO timestamps. State timezone and date window in results.
- Define whether running entries are excluded or counted through a stated as-of
  time. For time overlapping the window, clip durations to that window and verify
  that retrieval includes boundary-crossing entries before claiming a full total.
- The helper uses Clockify's default global API endpoint. Regional workspaces and
  creation requiring custom fields are unsupported. Updates with existing custom
  fields are refused rather than risking data loss. Do not silently omit required data.
- API/transport failures produce a JSON error and nonzero status; CLI syntax errors
  use argparse's normal error output. Requests time out after 30 seconds, without retries.
- For unsupported discovery or operations, consult [Clockify API docs](https://docs.clockify.me/)
  and use a scoped read-only API call when needed. Do not improvise unsupported writes.

Run offline regression checks with Python 3.10+:
`python3 <skill-directory>/scripts/test_clockify_api.py`.
