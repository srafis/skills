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
- Include every speaker as an attendee.
- Record only decisions supported by the transcript. Do not turn suggestions into agreed decisions or invent owners, deadlines, blockers, or completed follow-up work.
- Use stated timelines; otherwise use "TBD". Use "TBD" for unassigned action owners as well.
- Mark unclear passages as "(unclear)" or "(inaudible)" and use direct quotes sparingly.
- Before returning the MoM, check it against the transcript for completeness, attribution, and factual accuracy.

## Output Structure

Use the following layout in order, with no preamble or closing remarks. Include the tracker section only when applicable.

### Opening Details

Start directly with a quote block containing date and attendees on separate lines. Format the date as day with ordinal suffix, full month, and year (e.g., 6th August 2026). Do not add a meeting-details heading or duration.

> **Date:** [supplied meeting date or today's date]
> **Attendees:** [comma-separated speaker names]

### **Agenda Items Covered**

List every distinct business topic as a numbered list with concise topic names.

### **[N]. [Topic Name]**

Create one numbered topic section per agenda item. Group related points under bold subtopic labels ending in a colon, such as **Issue Identified:** or **Decision:**, when helpful. Use bullets covering the discussion, requested changes, concerns, business impact, and outcomes; retain enough detail to explain behavior and restrictions. Use numbered lists for issue summaries or sequential steps when clearer.

### **Key Decisions Made**

List supported decisions as bullets, each beginning with a bold declarative sentence stating the agreed outcome or direction.

If none: "No formal decisions were recorded in this meeting."

### **Open Questions / Pending Clarifications**

Use a numbered list, starting each entry with a bold topic label followed by a colon. State what remains unresolved, who needs to clarify when known, and the business impact when relevant.

If none: "No open questions or pending clarifications."

### **Action Items Summary**

Write each action as a self-contained action description focused on the intended outcome.

| **#** | **Action Item** | **Owner** | **ETA** |
| --- | --- | --- | --- |

If none, replace the table with: "No action items were identified."

### **Blockers / Dependencies**

Include only explicitly mentioned blockers or dependencies, their operational impact, and any stated mitigation or next step.

| **Blocker** | **Impact** | **Mitigation / Next Step** |
| --- | --- | --- |

If none, replace the table with: "No blockers were identified."

### **Clarification Tracker Reference**

If pending clarifications need follow-up, include a short bullet recommending they be tracked in the shared clarification tracker. Claim entries were added only if the transcript confirms that. Otherwise omit this section.

### **Next Meeting**

State the date, time, or recurrence only if explicitly mentioned.

If absent: "Next meeting details were not discussed."

## Formatting

- Use `### **Heading**` for section headings and `---` after the opening quote block and between sections, with blank lines around headings, lists, tables, and separators.
- Use `-` for bullets and numbered lists where specified above.
- Use bold for decision sentences, subtopic labels, table headers, and key facts where it aids scanning. Italicize titles of movies or other works when relevant.
- Use valid Markdown table separators.
