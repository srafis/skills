---
name: meeting-mom
description: Use when the user wants to create Minutes of Meeting
---

# Meeting Transcript To MoM

Read the supplied transcript, draft and review the MoM, and return only the final Markdown.

## Writing and Accuracy

- Use concise business language focused on requested changes, operational impact, decisions, responsibilities, blockers, and next steps. Explain technical terms only when essential.
- Attribute statements to speakers where possible. Preserve important numbers, percentages, dates, statuses, feature names, and business terminology.
- Use the meeting date supplied by the user or transcript; otherwise default to today's date.
- Include every speaker as an attendee. Estimate duration from available timestamps; use "Not specified" when duration cannot be determined.
- Record only decisions supported by the transcript. Do not turn suggestions into agreed decisions or invent owners, deadlines, blockers, or completed follow-up work.
- Use stated timelines; otherwise use "TBD". Use "TBD" for unassigned action owners as well.
- Mark unclear passages as "(unclear)" or "(inaudible)" and use direct quotes sparingly.
- Before returning the MoM, check it against the transcript for completeness, attribution, and factual accuracy.

## Output Structure

Use the following sections in order. Start directly with `### Meeting Details`, with no preamble or closing remarks. Include the tracker section only when applicable.

### Meeting Details

Use one line:

**Date:** [supplied meeting date or today's date]    **Duration:** [estimated from timestamps or "Not specified"]    **Attendees:** [comma-separated speaker names]

### Agenda Items Covered

List every distinct business topic as a numbered list with concise topic names.

### [N]. [Topic Name]

Create one numbered topic section per agenda item. Use concise bullets covering the discussion, requested changes, concerns, business impact, and outcomes. Use bold labels for subtopics when helpful.

### Key Decisions Made

List supported decisions as bullets, each beginning with a bold declarative sentence stating the agreed outcome or direction.

If none: "No formal decisions were recorded in this meeting."

### Open Questions / Pending Clarifications

Use a numbered list stating what remains unresolved, who needs to clarify when known, and the business impact when relevant.

If none: "No open questions or pending clarifications."

### Action Items Summary

Write each action as a full, self-contained sentence focused on the intended outcome.

| # | Action Item | Owner | ETA |
| --- | --- | --- | --- |

If none, replace the table with: "No action items were identified."

### Blockers / Dependencies

Include only explicitly mentioned blockers or dependencies, their operational impact, and any stated mitigation or next step.

| Blocker | Impact | Mitigation / Next Step |
| --- | --- | --- |

If none, replace the table with: "No blockers were identified."

### Clarification Tracker Reference

Include only if a shared clarification tracker or sheet was mentioned. Describe its stated role or follow-up; claim entries were added only if the transcript confirms that.

### Next Meeting

State the date, time, or recurrence only if explicitly mentioned.

If absent: "Next meeting details were not discussed."

## Formatting

- Use `###` for section headings and `---` between sections, with blank lines around headings, lists, tables, and separators.
- Use `-` for bullets. Use numbered lists for the agenda, open questions, and sequential workflows.
- Use bold for decision sentences and other key facts where it aids scanning.
- Use valid Markdown table separators.
