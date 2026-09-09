# Authorized computation, 8 September 2026

Scope: execute the prepared curve closure search, then explicit fibre and
Picard/Hodge computations as certificates permit. Targeted claim verification;
the source existence audit is not repeated. Qualified-human verification is
not claimed.

The entire 100-file daytime manifest verified before execution. The prepared
scripts and chart were copied into this run; original runner/controller copies
are retained in `inputs/`. The only initial changes are removal of the
superseded night-only controller gate and stricter execution-window enforcement
in the copied guarded runner. No daytime evidence is edited.

Resource code inspection: one exclusive lock, refusal of pre-existing CAS
processes, exactly one child process group, four thread variables fixed to1,
RSS measured for that process group only, and SIGTERM/SIGKILL only for that
owned group. The copied runner rejects requested RSS limits above2800 MiB or
attempts above3600 seconds. Primary stages remain1800 seconds. No long job
starts at/after16:00 Sao Paulo; owned computations stop by16:35, reserving
the16:45 handoff. Process-list permission is required; monitoring fails closed.
These are monitored limits, not a guarantee that a one-second sampling interval
can prevent every instantaneous RSS overshoot.

All substantial calculations are scheduled by the root agent. Other agents
may inspect sources, derive mathematics and write code concurrently but may
not launch substantial calculations without an explicit slot allocation.
No skeletal-polytope task, global Q-factoriality search or broad linkage search
is in scope. All sibling repositories and archives remain read-only.

Initial dependencies: frozen chart + normalized six-jet -> finite continuation;
exact closure + full central syzygies -> local flat family; certified integral
smooth spread + conormal vanishing -> characteristic-zero Picard rank1.
Finite-order compatibility alone does not supply either downstream conclusion.

12:12 regression note: the copied chart builder's repeat-input assertion
compared Python tuples with their JSON list serialization. The existing data
was preserved; comparison now canonicalizes only the freshly generated data
through JSON. The failed first regression and traceback remain in logs. The
six-jet regression passed before this harmless serialization repair.

## Final execution state

Completed at approximately14:35 Rio time, well before the16:45 handoff.
The prescribed order24/32 rational search ran and failed its bounded
closure tests. A substantially reduced, ramified coefficient-point
construction instead supplies an actual smooth number-field fibre.
The degree-eight product argument proves Picard rank1, Hodge pair(1,31),
and a smooth94-dimensional Hilbert component within the accepted proof
trust boundary. See `COMPUTATION_RESULTS.md` for all dependencies.

The largest completed guarded runtime was205.537s (the genuine pi56
mixed-characteristic point calculation); the largest sampled RSS was
181.61MiB (polynomial peeling, stopped at its expression-growth gate).
No CAS process was needed. All substantial arithmetic ran sequentially
under the inspected resource guard. Exact LLL continuation was allowed
only after measured potential decrease and checkpoint replay; all final
bounded searches and their negative certificates are preserved.

At14:29 the new two-check replay controller itself passed, with guarded
times1.189s and1.190s. All agents released their computation slots; no
owned process remains running. No skeletal-polytope job ran, no sibling
repository was modified, and nothing was pushed. The new continuation
prompt starts with cheap verification, not another unproductive heavy job.
