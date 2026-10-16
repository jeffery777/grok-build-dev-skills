---
name: grok-review-change
description: Review an exact repository change read-only in Grok Build with independent findings and fixed Core gates. Use for code and document review or complete base-to-head Merge Review.
---

# Independent change review in Grok Build

Read [review and security](../../vendor/engineering-workflow-core/contracts/review-and-security.md), [authorization and stops](../../vendor/engineering-workflow-core/contracts/authorization-and-stops.md), and the [Grok capability mapping](../../references/grok-capabilities.md). For a change request or merge readiness, also read the complete [exact-head contract](../../vendor/engineering-workflow-core/contracts/exact-head-and-evidence.md). Read the shared [plain-writing requirements](../../vendor/engineering-workflow-core/contracts/workflow.md#wf-writing) for document and delivery-summary review. Core Chinese text is authoritative.

Confirm the exact repository, request, base/head/merge-base, full diff, DoD and relevant specifications. Remain independent of the author and read-only: inspect source and necessary supporting context; do not modify source/index, create Git objects, publish reviews, or perform external actions. Use existing test results when their identity and assumptions still apply. Any needed test execution requires its own authorized safe boundary.

Check actual loaded tools, effective permissions and required qualification before acting. Do not use a parent plan mode, persona, skill frontmatter or an agent type name as proof of technical read-only enforcement. Shell and MCP capabilities need explicit inspection; official and bundled explore/plan descriptions differ. When required enforcement or reliable authorization forwarding is unavailable, mark the dependent review blocked and preserve the question rather than running it anyway.

Review correctness, regressions, trust boundaries, negative cases, notices and code/docs/configuration/package/version coherence. Within the existing review, sample applicable writing requirements and record the scope, results and unverified limits, including bilingual consistency and the basis for any conformity claim. Assess security scan applicability from the final diff; ordinary review is not a substitute for a required scan. Verify evidence rather than treating summaries, help, exit 0 or packet flags as qualification.

Give each finding a stable ID, concrete path/line, evidence, impact and disposition. Recheck fixes proportionately, preserving valid unchanged evidence. For every changed PR head, perform a new complete base-to-head Merge Review; a fix-only or pre-commit verdict does not replace it.

Return the exact reviewed identities, scope, commands/results, findings/dispositions, residual risks and content verdict. Report platform checks and action authority separately, including not configured or not run states. A clean verdict grants no commit/push/merge permission. Do not start a new session or API service to manufacture independence; use an already authorized qualified reviewer route or return the blocker to the coordinator.
