# Explicit GitNexus operations in Grok

Read this reference when GitNexus is relevant to execution or review. The
[workflow](../vendor/engineering-workflow-core/contracts/workflow.md) and
[authorization/stops](../vendor/engineering-workflow-core/contracts/authorization-and-stops.md)
still apply. This reference and CLI flags grant no authority.

## Scope and selection

Grok 0.2.0 candidate uses the same bounded index-write controller as Codex
0.35.0 candidate, with Core 0.1.0 and **GitNexus exactly 1.6.12**. The
[source lock](../gitnexus.lock.json) pins local, unreleased S/T commits and four
unchanged source files, including the complete [MIT notice](../vendor/gitnexus-index-controller/LICENSE).
The pure `memory_contract.py` dependency provides data validation/digests;
no Memory backend, hooks, scheduler, model or service is installed or activated.

The orchestrator decides when to use GitNexus, the target and which side is
the one index writer. Either Codex or Grok may be assigned. Preserve the
original request, exact root/worktree/remote/branch/HEAD, permitted action,
request ID and stop conditions. A reviewer does not refresh. Missing or
conflicting assignment returns to the orchestrator before dependent action.
Do not substitute another checkout's index, assume cwd selects the target,
or expand scope to obtain a passing result.

## Existing accepted evidence

Use only a profile and its expected raw SHA-256 independently accepted in the
current brief. Do not invent a profile, derive its trust from its filename,
copy private profiles into this package or broaden coverage from metadata.
The profile is a bounded JSON object containing exactly the arguments of
`qualify_local_1612`: `configured_path`, `runtime_path`, `package_root`,
`accepted_executable_sha256`, `accepted_runtime_sha256`,
`accepted_package_sha256`, `accepted_runner_identity`,
`accepted_dependency_sha256`, `expected_coverage_paths`, `version_output`,
`analyze_help_output`, `accepted_probe_sha256`.

The controller reads accepted version/help receipts without running new
probes, then rechecks the selected installation bytes. Missing or incompatible
evidence stops the operation. Do not use its general operator CLI or the
general qualification API: those can run new probes. Tool evidence can be
reused only within its original content, scope and environment limits.

## Explicit entry

Use the [thin entry](../scripts/gitnexus_index.py) from the verified candidate
package, in a normal fresh Python process. The required selectors for each
action are:

```text
python3 scripts/gitnexus_index.py inspect|plan|refresh
  --root EXACT_ABSOLUTE_CANONICAL_CHECKOUT
  --repository-id ACCEPTED_REPOSITORY_ID
  --expected-remote EXPECTED_ORIGIN
  --expected-head FULL_COMMIT_SHA --expected-branch EXPECTED_BRANCH
  --profile ACCEPTED_ABSOLUTE_PROFILE_JSON
  --expected-profile-sha256 INDEPENDENTLY_ACCEPTED_RAW_SHA256
  --request-id ORIGINAL_REQUEST_ID
```

This is an argument shape, not a ready-to-run command or an accepted profile.
`inspect` is read-only evidence collection, not GitNexus `status` or a query.
`plan` has no write effect and makes no eligibility or authorization promise.
Both default to `--role review`; they start no GitNexus process. Exit 0 for
these observations does not mean the index is fresh or the task is complete.

Only an authorized Grok execution assignment may add all of:

```text
--role execution --assigned-writer grok --confirm-refresh
--isolated-home EXACT_PRIVATE_EMPTY_HOME
```

If Codex is assigned, Grok does not take over. `--timeout` is 1–180 seconds,
default 120. The fixed controller owns process bounds, isolated registry/home,
canonical `/tmp`/UID lock namespace, eligible clean-checkout checks and sidecar
postconditions. The thin entry exposes no runner, environment or lock override.
Keep the existing sidecar name/schema and complete controller receipt.
Request IDs are traceability, not durable deduplication or authority.

Fresh evidence returns `not_run/already-fresh`. Missing/stale evidence can
reach the controller, which rechecks all eligibility conditions. Other states
block refresh. Dirty, detached, linked-worktree, same-HEAD refresh and
configuration restrictions remain those of the fixed controller; never work
around a rejection by changing branch, root, config or flags.

## Result and failure

The outer result binds actor `grok`, request/target evidence, profile digest
and fixed sources. It does not modify the nested controller receipt or its
canonical digest. `observed`, `plan_only` and `not_run` are distinct from
`refreshed`. A refreshed receipt is still derived advisory evidence, not a
review, gate, external-write authority or overall task completion.

Read both process exit and semantic status. Failed/blocked/unknown outcomes
return nonzero. If the controller does not return or is interrupted, preserve
the attempt and report `unknown` with manual reconciliation required. Do not
automatically retry, resume or steal a lock. Read back known effects and return
the full question/original request, applicable session/revision/action/target
identity and limits to the orchestrator; wait for any new authorization.

Native MCP remains optional tool access. Query/MCP coexistence with index
updates, watch/auto-sync, linked-worktree automatic refresh and multi-process
DB concurrency are not qualified or enabled here. Source/Git evidence remains
the safe fallback when index evidence is missing or unsuitable.

Offline stub checks establish our selection, argument/API use, receipt and
failure behavior. They do not prove native Grok agent adoption. Reuse existing
valid tool/loading evidence; propose a bounded case before any new native call.
Never extend old live-call budgets or test GitNexus internals to close our
integration gaps. The source-only acceptance record is `docs/verification/gitnexus-operation-acceptance.md`.

English follows ASD-STE100 clarity principles; full conformance is unverified.
