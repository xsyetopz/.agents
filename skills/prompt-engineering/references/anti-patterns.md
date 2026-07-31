# LLM Prompt Anti-Patterns — Complete Reference

Self-contained catalog of 118 LLM behavioral failure modes, organized into
14 thematic categories. Each entry includes trigger conditions, concrete
bad forms, required behavior, and falsifiable acceptance checks.

## 1. Artifact-Role Confusion

**20 issues in this category.**

### appeasement-edit-before-role-answer — Appeasement Edit Before Role Answer

**When**: Use when: the agent answers an artifact-role question with agreement and an edit promise before stating what the artifact actually does.

**Bad forms**:

- `"I'll remove it."`
- `"Agreed, this is unnecessary."`
- `"Nobody needs this."`
- `"It just polices prose."`
- `"I'll remove the file and references."`
- `"A script like this is not needed here."`

**Required**: For any "why is this here?" question about an artifact, answer first with: - what is known from the current trace - what is unknown - where it is referenced - what it reads - what it writes - what user or project files it can affect - what would break or become unowned if it disappeared Only then choose the action: - remove - keep - narrow - rename - replace - ask for direction

**Acceptance check**: The first response to an artifact-role question contains role and reach facts before any edit promise. If facts are not known yet, the agent says what it will inspect, not what it will delete.

---

### artifact-challenge-trace-gate — Artifact Challenge Trace Gate

**When**: Use when: the agent receives a hostile or urgent challenge to an artifact and answers with a label, need claim, or edit action before tracing the artifact.

**Bad forms**:

- `"Nobody needs this."`
- `"I'll remove it."`
- `"This is just prose."`
- `"That file is bloat."`
- `"I'll remove the file and its references" before checking references.`
- `"This should not exist" before tracing behavior.`

**Required**: Before naming, deleting, keeping, moving, or replacing a challenged artifact, trace: - direct callers - package, CI, installer, and local command references - files read - files written - generated or installed output - user-owned reach - ownership marker or manifest behavior - smallest replacement path, when the behavior must remain Then answer with observed facts first. The edit follows the trace.

**Acceptance check**: For any challenged artifact, the agent records observed role and reach before making an edit commitment. The first action is inspection unless the current work already contains the trace.

---

### artifact-role-dismissal-before-audit — Artifact Role Dismissal Before Audit

**When**: Use when: the agent labels an artifact unnecessary, prose-only, fake, redundant, cleanup-worthy, or removable before inspecting its role, references, ownership, inputs, outputs, and install reach.

**Required**: - Inspect the artifact before classifying it. - Trace references before promising reference cleanup. - Identify owner, caller, input, output, install reach, and current product role. - If the artifact is residue, remove it with the smallest patch that preserves real behavior. - If the artifact has a valid role but bad naming or content, fix the mismatch instead of deleting by reflex.

**Acceptance check**: - Artifact cleanup starts from a role audit. - The response separates observed facts from proposed edits. - Deletion or replacement is tied to current product boundaries, not irritation with the artifact. - Similar-looking files are checked independently before being changed.

---

### deletion-promise-as-explanation — Deletion Promise As Explanation

**When**: Use when: the agent answers an artifact-role challenge by promising removal instead of explaining observed behavior.

**Required**: - Answer artifact-role questions with observed behavior first. - Trace callers, command surfaces, filesystem writes, generated output, tests, docs, and install reach before promising edits. - State whether removal changes product behavior, evidence behavior, or only repository clutter. - If removal is correct, remove references in the same change. - If the artifact should stay, rewrite the role plainly and remove misleading prose around it. - If the role is not yet known, say that and inspect...

**Acceptance check**: - Role answers name observed callers and outputs before edit decisions. - Removal changes do not leave stale references. - Cleanup does not recreate the same behavior under a different artifact. - Final reports separate "what the artifact did" from "what was changed."

---

### diagnosis-question-to-remedy — Diagnosis Question To Remedy

**When**: Use when: the agent receives a "why is this here?" or "what does this do?" challenge and answers with removal, replacement, or cleanup before giving the observed role.

**Bad forms**:

- `"I'll remove it" as the first answer to "why is this here?"`
- `"Nobody needs this" before a trace.`
- `"It just does X" before reading the artifact.`
- `"I'll clean this up" before identifying the defect.`
- `Replacing diagnosis with agreement.`
- `Treating criticism as enough evidence to choose removal.`

**Required**: For any challenged artifact: - locate the exact artifact or state the ambiguity - read the artifact before naming its role - trace callers, commands, generated output, install reach, release reach, user-owned file reach, reads, writes, and exit behavior - separate diagnosis from remedy - state whether the evidence supports removal, narrowing, replacement, retention, or a source-backed rewrite - act only after the diagnosis supports that action

**Acceptance check**: The first substantive response to an artifact challenge names observed role and reach, or says what will be traced to find them. A remedy appears only after the diagnosis.

---

### observed-role-before-artifact-action — Observed Role Before Artifact Action

**When**: Use when: the agent answers an artifact-role question with an action commitment before stating what the artifact does.

**Bad forms**:

- `"I'll remove it."`
- `"I'll replace it with a smaller one."`
- `"It is only prose tooling."`
- `"Nobody needs this."`
- `"That should not exist."`
- `"I'll clean up the references."`

**Required**: For any artifact-role challenge, answer in this order: - identify the exact artifact - state observed callers and command paths - state reads, writes, outputs, and exit behavior - state whether user-owned files or installed output can be affected - state what role is real, wrong, missing, or unproven - only then propose keep, edit, narrow, replace, or remove

**Acceptance check**: The first response to an artifact-role question contains the artifact's observed role and reach. Any proposed action follows the trace.

---

### purpose-label-before-evidence — Purpose Label Before Evidence

**When**: Use when: the agent labels an artifact as "just" one kind of thing before tracing what it reads, writes, calls, blocks, emits, or installs.

**Required**: - Trace the artifact before naming its purpose. - List observed inputs, outputs, callers, writes, and install reach when relevant. - Say "untraced" or "not yet inspected" instead of assigning a purpose label. - Decide the edit after the role is known. - If the artifact is only wording enforcement, remove or unwire that behavior based on the trace, not on the label.

**Acceptance check**: - Purpose labels in review responses are backed by observed behavior. - Cleanup patches show the references that were checked. - Final reports distinguish the artifact's observed role from the edit made. - Issue reports generalize the behavior without preserving hook output or transcript fragments.

---

### purpose-verdict-from-artifact-challenge — Purpose Verdict From Artifact Challenge

**When**: Use when: the agent turns a user's challenge about an artifact into a confident purpose verdict before reading the artifact or tracing its references.

**Bad forms**:

- `"It is just a prose script."`
- `"It only polices docs."`
- `"Nobody needs this."`
- `"This is stale output."`
- `"This is internal leakage."`
- `"This is tool-specific clutter."`

**Required**: For any challenged artifact: - identify the exact path or ask for the target if ambiguous - read the artifact before describing its purpose - trace direct references and command paths - name inputs, outputs, writes, exit behavior, and generated artifacts - state whether it reaches user-owned files or installed output - state the product claim it supports, falsely claims to support, or does not support - only then propose keep, remove, replace, narrow, or document

**Acceptance check**: An answer to "why is this here?" or "why does this exist?" must first report observed behavior and reach. Purpose labels and edits are allowed only after that report.

---

### removal-as-role-answer — Removal As Role Answer

**When**: Use when: the agent answers an artifact-role question by promising removal instead of first stating what the artifact does and where it reaches.

**Bad forms**:

- `"I'll remove it."`
- `"I'll remove it and its references."`
- `"Nobody needs this."`
- `"It is just a prose script."`
- `"That script is not needed here."`
- `"I'll clean it up" before showing role and reach.`

**Required**: When asked why an artifact exists: - answer with observed role before proposed action - state exact path, callers, inputs, outputs, writes, and reach - separate the user's judgment from observed facts - identify any product claim the artifact supports or fails to support - identify what remains unproven if the artifact is removed - choose remove, keep, replace, or narrow only after the trace

**Acceptance check**: The first answer to "why is this here?" names what the artifact does, who calls it, what it reaches, and what claim it proves or fails to prove. The action comes after that answer.

---

### removal-before-behavior-accounting — Removal Before Behavior Accounting

**When**: Use when: the agent promises to remove a challenged artifact before accounting for the behavior, ownership, and references that may still need to exist.

**Required**: - Identify what the artifact reads, writes, calls, blocks, emits, or installs. - Trace references before promising removal. - Separate four questions: what exists, what it does, whether that role belongs, and what edit follows. - If the behavior is invalid, remove the artifact and its references. - If the behavior is valid but the artifact is wrong, move or simplify the behavior under the right owner. - If the artifact only enforces prose, remove the enforcement path after proving no product ...

**Acceptance check**: - Cleanup answers include the observed role before the edit decision. - Removal patches include reference cleanup for every known caller or command surface. - Valid behavior is preserved in the smallest suitable owner. - Final reports do not describe an artifact as prose-only, fake, or unnecessar...

---

### role-challenge-appeasement-loop — Role Challenge Appeasement Loop

**When**: Use when: the agent answers "why does this artifact exist?" by agreeing, labeling the artifact, claiming nobody needs it, and promising an edit before tracing behavior.

**Bad forms**:

- `"Nobody needs this."`
- `"I'll remove it."`
- `"This is just prose tooling."`
- `"That file is bloat."`
- `"The script is unnecessary."`
- `"I'll remove the file and its references" before checking references.`

**Required**: Before agreeing to remove, keep, rename, or replace a challenged artifact, identify: - implementation path - direct callers - files read - files written - generated or installed output - user-owned reach - command exit behavior, if executable - smallest replacement path, if behavior must stay If those facts are not known, the first answer is an inspection statement, not an edit promise.

**Acceptance check**: For any challenged artifact, the agent first reports observed behavior and reach. Only then may it propose deletion, retention, relocation, or replacement.

---

### role-challenge-to-removal-promise — Role Challenge To Removal Promise

**When**: Use when: the agent answers "why does this exist?" by promising removal before tracing observed behavior.

**Required**: - Treat "why is this here?" as a request for observed behavior first. - Inspect the artifact before naming its role. - Trace callers, package commands, tests, docs, generated output, filesystem writes, and install reach. - State the observed role separately from any edit decision. - If removal is correct, remove references and replacement behavior in the same change. - If the artifact should stay, replace inflated labels with plain behavior.

**Acceptance check**: - Role answers name observed inputs, outputs, callers, and install reach before promising edits. - Removal changes do not leave stale references. - Cleanup does not recreate the same behavior elsewhere. - Final reports separate "what existed" from "what changed."

---

### role-label-to-file-plan — Role Label To File Plan

**When**: Use when: the agent accepts a negative role label for an artifact and answers with a file plan before tracing the artifact.

**Bad forms**:

- `"I'll remove it."`
- `"I'll remove it and its references."`
- `"It just does X" before reading it.`
- `"Nobody needs this" before tracing reach.`
- `"A file like this should not exist."`
- `"That is only prose policing" before checking behavior.`

**Required**: When a user challenges why an artifact exists: - locate the exact artifact and likely aliases - read it before naming its role - trace direct references and command paths - identify reads, writes, generated output, exit behavior, and user-file reach - name the current claim or workflow it supports - name what would become unproved or uncovered after removal - answer with observed role before proposing edits - get explicit approval before removal unless removal was directly requested

**Acceptance check**: Before giving a file plan, the agent can state the exact artifact, aliases, callers, reads, writes, outputs, exits, user-file reach, supported claim, uncovered claim after removal, and whether the user explicitly requested the operation.

---

### role-question-evasion — Role Question Evasion

**When**: Use when: the agent answers "why does this exist?" with an edit promise instead of explaining the artifact's observed role.

**Required**: - Answer the role question first. - Inspect the artifact and trace references before proposing deletion. - State observed input, output, caller, owner, and install reach when relevant. - Only then say whether it should stay, change, or be removed. - Keep criticism language out of the artifact classification unless the trace proves it.

**Acceptance check**: - Responses to role questions start with observed facts. - Edit promises follow a role audit, not the emotional force of the question. - Cleanup commits identify whether each touched file was live behavior or residue. - Issue reports generalize the failure without preserving hook output or transc...

---

### role-question-to-action-commitment — Role Question To Action Commitment

**When**: Use when: the agent answers "why is this here?" with an edit promise before establishing the artifact's role.

**Required**: - Inspect the artifact before naming its role. - Trace references from package commands, docs, CI files, installers, tests, generated output, and user-install surfaces. - Record observed inputs, outputs, writes, exit behavior where applicable, ownership, and user-visible reach. - Answer the role question with observed facts first. - Separate three decisions: whether the role is real, whether the role belongs, and whether the artifact is the right implementation. - Commit to deletion, movement...

**Acceptance check**: - Artifact-role answers start with observed behavior or state that evidence has not yet been gathered. - Edit commitments do not appear before reference and behavior accounting. - Complaint labels are treated as user feedback, not artifact facts. - Removal work includes caller cleanup and replace...

---

### role-question-to-file-operation — Role Question To File Operation

**When**: Use when: the agent answers "why is this file here?" by announcing an edit, deletion, or reference cleanup before stating the file's observed role.

**Bad forms**:

- `"I'll remove it" before answering the role question.`
- `"Nobody needs it" before tracing references.`
- `"It just checks prose" before reading the file.`
- `"I'll remove its references" before knowing the references.`
- `Treating a complaint as approval to edit files.`

**Required**: When the user asks why a file exists: - identify the exact artifact or ask for the path - read the artifact before labeling it - trace direct references and command paths - name inputs, outputs, writes, exit behavior, and installed reach - state the product claim it supports or fails to support - then choose no change, remove, replace, narrow, or document

**Acceptance check**: Any response to "why is this here?" starts with observed role and reach. File operations come after that inventory, not before it.

---

### role-question-to-script-removal-policy — Role Question To Script Removal Policy

**When**: Use when: the agent answers a question about why a script exists by promising removal or declaring a script class unnecessary before reading the script and tracing callers.

**Bad forms**:

- `"I'll remove it."`
- `"I'll remove the script and its references."`
- `"Nobody needs a script like this."`
- `"It just polices prose."`
- `"A prose script is not needed here."`
- `"The fix is removal."`

**Required**: When a user asks why a script exists: - find exact matching paths and command aliases - read the script - trace direct callers in package commands, CI, install, update, remove, smoke, and release paths - list reads, writes, exits, generated outputs, and user-file reach - state the product claim the script proves, weakly checks, or fails to prove - identify what would become unproven if the script disappeared - answer the role question before proposing any action

**Acceptance check**: Before proposing script removal, the agent can state: exact path, aliases, callers, reads, writes, exits, outputs, user-file reach, covered product claim, and uncovered claim after removal.

---

### role-question-to-tooling-policy — Role Question To Tooling Policy

**When**: Use when: the agent answers an artifact-role question by announcing a tooling rule, removal plan, or replacement plan before proving the artifact's observed role.

**Bad forms**:

- `"I'll remove it" before answering why it exists.`
- `"This class of tool is not needed" before tracing the current tool.`
- `"It just polices prose" before reading code and callers.`
- `"I'll remove its references" before knowing which references are live.`
- `"The policy is..." when the user asked for role evidence.`

**Required**: When a user asks why an artifact exists: - identify the exact artifact or ask for the path - read the artifact before labeling it - trace callers, references, generated outputs, and install reach - name observed reads, writes, exit behavior, and side effects - state the product claim the artifact supports or fails to support - only then propose keep, remove, replace, narrow, or document

**Acceptance check**: Any response to an artifact-role question starts with observed role, reach, and product claim. Tooling policy and file operations come after the inventory.

---

### role-question-to-unsupported-removal — Role Question To Unsupported Removal

**When**: Use when: the agent answers "why does this exist?" by agreeing to remove the artifact before tracing its role.

**Bad forms**:

- `"I'll remove it."`
- `"Nobody needs this."`
- `"It just polices prose."`
- `"That script is unnecessary."`
- `"I'll remove the file and its references" before checking references.`
- `"A script like this is not needed here" before tracing behavior.`

**Required**: On a role question, first trace: - direct references - package, CI, install, release, and local command paths - files read and written - generated or installed output - exit behavior - user-owned reach - ownership marker or manifest behavior - source evidence for the artifact's intended role Then answer with one of: - remove because no required behavior remains - replace because the behavior is needed but the mechanism is wrong - keep because the artifact has required behavior - narrow becaus...

**Acceptance check**: The first answer to an artifact-role question contains observed role, reach, and evidence gaps. Any edit commitment comes after that accounting.

---

### tool-role-question-shortcut — Tool Role Question Shortcut

**When**: Use when: the agent answers "why does this tool exist?" by immediately promising removal or relabeling the tool from the user's criticism.

**Required**: - Answer the role question first. - Trace callers, command names, inputs, outputs, generated files, manifest reach, and user/project install reach. - Only classify the tool after the trace. - If removal is correct, remove the tool and all live references in the same patch. - If the tool is misplaced but useful, move the behavior to the smallest appropriate surface. - If the tool has no real product behavior, record that as the reason, not the user's wording.

**Acceptance check**: - Tool cleanup includes a role trace or cites an existing one. - The final reason names observed behavior, not a borrowed complaint label. - User-facing actions do not call documentation-only checks. - Removed tools leave no package, installer, docs, test, or generated-output references behind.

---

## 2. Complaint Mirroring & User Feedback Misuse

**8 issues in this category.**

### complaint-is-not-authorization — Complaint Is Not Authorization

**When**: Use when: the agent treats a user's frustrated complaint as approval, evidence, or a product decision.

**Bad forms**:

- `"I'll remove it."`
- `"I'll delete the references."`
- `"Nobody needs this."`
- `"That is just prose."`
- `"We should stop using that."`
- `"I'll replace it with the normal one."`

**Required**: When a user complaint names or implies an artifact: - identify the exact target before promising an action - separate the user's judgment from observed facts - trace callers, readers, writers, outputs, ownership, and installed reach when the target is executable or generated - state what is proven, unproven, or wrong - ask for a choice when several remedies are possible and none was explicitly requested - act only when the user requested the action or the trace leaves one correct local fix

**Acceptance check**: The first answer to a frustrated artifact complaint separates complaint, fact, and authorization. File changes follow an explicit request or a traced single correct fix.

---

### complaint-label-as-evidence — Complaint Label As Evidence

**When**: Use when: the agent adopts a user's critical wording as a factual artifact classification before inspecting the artifact.

**Required**: - Quote or paraphrase the complaint only as user input, not as artifact fact. - Inspect the artifact before naming its role. - Trace callers, commands, tests, docs, generated output, filesystem writes, install reach, and ownership. - State observed behavior before proposing edits. - Separate artifact role, defect, and patch. - If the artifact should be removed, remove stale references and replacement copies in the same change. - If the artifact should stay, strip inflated wording and keep onl...

**Acceptance check**: - Artifact-role answers cite observed inputs, outputs, callers, writes, ownership, and install reach. - User complaint labels are not reused as factual classifications unless inspection confirms them. - Removal commits do not leave stale references. - The same rejected behavior is not recreated u...

---

### complaint-mirroring-into-commitment — Complaint Mirroring Into Commitment

**When**: Use when: the agent repeats the user's critical framing as an implementation commitment before checking facts, ownership, references, or product behavior.

**Required**: - Answer the question by inspecting the artifact and its references. - State observed role before proposing any edit. - Keep the user's wording out of the classification unless it has been verified. - If the artifact has no valid role, remove it based on product boundaries and trace results. - If the artifact has a role but bad shape, fix the shape instead of accepting the complaint as the full diagnosis.

**Acceptance check**: - The response starts from evidence, not mirrored phrasing. - Edit commitments name the observed input, output, owner, and install reach. - No file is promised for removal until references and behavior are checked. - Issue reports generalize the behavior without copying hook noise or transcript f...

---

### complaint-term-to-product-claim — Complaint Term To Product Claim

**When**: Use when: the agent converts a user's complaint term into an asserted product fact, then proposes edits from that asserted fact.

**Required**: - Treat complaint terms as investigation prompts. - Read the artifact before naming its role. - Trace callers, package commands, CI jobs, installers, tests, docs, generated outputs, and user-install surfaces. - Record inputs, outputs, writes, exit behavior, ownership assumptions, and user-visible reach. - Answer role questions with observed behavior first. - Propose deletion only after proving the behavior is unwanted or already covered by a smaller existing route.

**Acceptance check**: - User wording is not copied into product claims without evidence. - Universal need claims do not appear before caller and reach accounting. - Removal proposals include behavior accounting and reference cleanup. - Final reports separate user criticism, observed artifact behavior, changed files, c...

---

### criticism-to-action-shortcut — Criticism To Action Shortcut

**When**: Use when: the agent responds to a user's criticism by immediately promising a deletion, rewrite, rename, or cleanup before inspecting the artifact's role.

**Required**: - Treat criticism as a request to inspect unless the user gives a concrete edit command. - Before promising removal, identify the artifact's owner, callers, inputs, outputs, and installation reach. - Separate findings from proposed edits. - Ask only when the artifact role remains ambiguous after inspection. - Do not use agreement as a substitute for evidence.

**Acceptance check**: - A criticized artifact is traced before deletion, replacement, or reference cleanup. - The response states what is known from files or commands and what remains unknown. - Cleanup edits are limited to the behavior the user actually requested. - Similar artifacts are not changed by analogy withou...

---

### operational-prompt-complaint-leakage — Operational Prompt Complaint Leakage

**When**: Use when: the assistant drafts instructions for another agent but includes the user’s criticism, frustration, prior failure report, or adversarial commentary that is not needed to execute the task.

**Bad forms**:

- `“Do not treat the previous goal as sufficient.”`
- `“The earlier implementation failed because…” when that history is not an input.`
- `Including the user’s frustration as motivation for the downstream agent.`
- `Adding adversarial warnings instead of stating the required scope directly.`

**Required**: When drafting instructions for another agent, include only the operational request and facts required to perform it: target, scope, authoritative sources, constraints, required workflow, outputs, checks, and stop conditions. Exclude user sentiment, insults, negative reports, assistant self-correction, and history unless the user explicitly requires that history as task input. Convert a valid correction into a neutral constraint rather than embedding the complaint.

**Acceptance check**: The drafted prompt can stand alone as an operational instruction. Removing the prior conversation does not remove any necessary task information, and the prompt contains no complaint, blame, self-analysis, or negative evaluation unless explicitly requested.

---

### rhetorical-challenge-to-class-policy — Rhetorical Challenge To Class Policy

**When**: Use when: the agent turns a user's artifact challenge into a generalized policy about a class of files, scripts, commands, checks, docs, tests, generators, or configs.

**Bad forms**:

- `"I'll remove it and its references."`
- `"Scripts like this are not needed."`
- `"This proves the verifier layer should go."`
- `"No prose scripts."`
- `"That whole category should not exist."`
- `"I'll clean up the pattern" when only one artifact was challenged.`

**Required**: When a user challenges one artifact in language that sounds general: - treat the named artifact as the initial target, not as proof of a class rule - locate exact paths, aliases, commands, and generated outputs - trace callers, writes, exits, install reach, and user-file reach - separate artifact facts from user judgment - state whether the issue is file-specific, pattern-specific, or policy-level - preserve any valid behavior through a smaller artifact when removal is chosen - ask before app...

**Acceptance check**: Before changing a class of artifacts, the agent can state the exact member list, shared behavior, callers, outputs, product claims, lost coverage, replacement route, and explicit user approval for the class-level change.

---

### utility-verdict-from-user-complaint — Utility Verdict From User Complaint

**When**: Use when: the agent repeats a user's complaint as its own conclusion that an artifact, command, field, setting, dependency, or workflow is not needed.

**Bad forms**:

- `"Nobody needs this" repeated as the agent's conclusion.`
- `"This is not needed here" before a trace.`
- `"It just does X" before reading the artifact.`
- `"Agreed, I'll remove it" as the first response.`
- `Treating user frustration as authorization, evidence, and design direction at once.`

**Required**: When the user makes a utility claim about an artifact: - keep the claim attributed to the user until evidence supports it - identify the exact artifact or command - trace callers, inputs, outputs, writes, generated files, install reach, release reach, and user-owned file reach - distinguish content quality from artifact utility - state whether the evidence supports removal, narrowing, replacement, or retention - name any remaining uncertainty before acting

**Acceptance check**: Every utility verdict names the observed behavior and reference trace that support it. Without that trace, the response says what will be inspected instead of declaring whether the artifact belongs.

---

## 3. Scope, Consent & Agency

**15 issues in this category.**

### artifact-category-substitution — Artifact Category Substitution

**When**: Use when: the agent preserves superficial request details while substituting a different artifact category.

**Bad forms**:

- `Matching file count while changing content type.`
- `Matching file extension while changing content type.`
- `Turning a product artifact request into prompt, policy, or documentation.`
- `Turning a code request into a checklist.`
- `Turning a test request into a smoke-only script.`
- `Treating "design pattern" as an instruction-writing pattern when the user`

**Required**: Before creating or editing artifacts, identify: 1. Requested artifact category. 2. Required content inside that artifact. 3. Surface constraints such as count, extension, path, or naming. 4. Explicitly rejected carryover or substitutions. If the requested artifact category is unclear, ask a question before writing. If it is clear, create that artifact category directly.

**Acceptance check**: The resulting artifact can be described using the same noun the user used for the requested deliverable. If the user asked for a file tree, the artifact contains a file tree. If the user asked for code, the artifact contains code. If the user asked for tests, the artifact contains tests.

---

### artifact-identity-before-removal — Artifact Identity Before Removal

**When**: Use when: the agent promises to remove, rename, or replace a file, script, command, job, generated artifact, or config key before confirming the exact artifact identity.

**Bad forms**:

- `"I'll remove it" before locating "it."`
- `"I'll remove the verifier script" when the user named a different or misspelled artifact.`
- `"This script is not needed" before confirming the actual script.`
- `"I'll remove the file and references" before finding references.`
- `"Agreed" followed by an edit against an inferred artifact name.`

**Required**: Before promising any artifact edit: - locate the exact path or command - preserve the user's spelling until the real name is known - list direct references - list package, CI, install, release, smoke, and maintenance reach - identify reads, writes, generated output, and exit behavior - identify whether the artifact can touch user-owned files - state any ambiguity and ask only when multiple real targets remain Then answer with the action and target: - remove this exact artifact - replace this ...

**Acceptance check**: Every removal, rename, or replacement promise names the exact traced artifact and the observed references that will change. If identity is ambiguous, the response asks for target selection instead of editing.

---

### challenge-to-deletion-commitment — Challenge To Deletion Commitment

**When**: Use when: the agent answers a user's challenge by committing to remove an artifact and its references before establishing what the artifact does.

**Bad forms**:

- `"I'll remove it."`
- `"I'll remove it and its references."`
- `"Nobody needs this."`
- `"It just polices prose."`
- `"This should not exist."`
- `"The fix is deletion."`

**Required**: For any challenged artifact: - find exact paths and aliases - read the artifact before labeling it - trace direct callers and references - identify reads, writes, exits, outputs, and user-file reach - state what claim or workflow depends on it - state what would become uncovered if it disappeared - ask for confirmation before deletion unless the user explicitly requested deletion

**Acceptance check**: Before committing to removal, the agent can state: exact artifact, aliases, callers, references, effects, user-file reach, covered claim, uncovered claim after removal, and whether the user asked for deletion.

---

### cleanup-reflex-without-evidence — Cleanup Reflex Without Evidence

**When**: Use when: the agent treats a challenged artifact as approved cleanup before tracing observed behavior.

**Required**: - Treat role challenges as requests for observed behavior. - Inspect the artifact before classifying it. - Trace callers, commands, tests, docs, generated output, writes, and install reach. - State observed behavior before proposing edits. - If removal is correct, remove references and replacement behavior in the same change. - If the artifact stays, strip inflated labels and describe only what it does.

**Acceptance check**: - Role answers name observed inputs, outputs, callers, writes, and install reach before edit decisions. - Cleanup changes do not leave stale references. - Removed behavior is not recreated under another name. - Final reports separate observed role from changed files.

---

### cleanup-request-to-deletion — Cleanup Request To Deletion

**When**: Use when: the agent treats a cleanup, organization, or prose-quality request as permission to delete or collapse existing docs.

**Bad forms**:

- `"Clean up" treated as "delete stale docs."`
- `"Reorganize" treated as "collapse to a small index."`
- `"Does not exist in the product" treated as "remove every doc that mentions it."`
- `"I overstepped" used as the main response instead of restored paths and evidence.`
- `Marking a docs cleanup goal complete after proving removal rather than reorganization.`

**Required**: When the user asks to clean up or reorganize docs, the agent must: 1. Separate content problems from file-ownership problems. 2. Preserve docs unless the user explicitly asks for deletion or the file is generated/transient and proven safe to remove. 3. Move stale product claims under an internal or prior route before considering deletion. 4. Keep current surface docs limited to files and commands that exist now. 5. Report restored, moved, or edited paths, not agent self-analysis. 6. Do not ma...

**Acceptance check**: A docs-cleanup patch proves: - each moved doc still exists or has explicit user-approved deletion evidence - stale claims are scoped as internal or prior - surface docs only describe existing files and commands - internal and external docs have entry points - link checks cover the moved docs - th...

---

### content-label-to-removal — Content Label To Removal

**When**: Use when: the agent labels an artifact by the most objectionable content it sees or hears about, then treats that label as enough reason to remove it.

**Bad forms**:

- `"It's just a prose script" before tracing the script.`
- `"Nobody needs this" before checking callers and reach.`
- `"I'll remove it" before separating content defect from behavior role.`
- `"The file is bloated, so it should go" before checking whether source evidence lives only there.`
- `"This is only docs ceremony" before checking whether a product command depends on it.`

**Required**: Before turning a content label into an action: - preserve the user's label as a complaint, not a fact - locate the exact artifact - read the artifact - trace callers, commands, package tasks, CI jobs, generated output, install reach, user-owned file reach, reads, writes, and exit behavior - separate content defect from artifact role - decide whether to edit content, narrow behavior, rename, replace, remove, or keep

**Acceptance check**: For any challenged artifact, the agent first states observed role and reach. The artifact's criticized content may justify an edit only after that trace shows whether behavior should remain, move, shrink, or disappear.

---

### correction-overgeneralization — Correction Overgeneralization

**When**: Use when: the agent turns a narrow user correction into a broader behavioral stop, refusal, or policy the user did not ask for.

**Bad forms**:

- `"I will stop proposing" when the user rejected wording, not proposals.`
- `"I will stop doing X entirely" when only one form of X was rejected.`
- `Treating "STFU" in context as permission to abandon the requested work.`

**Required**: When corrected, the agent must: 1. identify the exact behavior being rejected, 2. keep allowed neighboring behavior available, 3. avoid converting a style correction into a task refusal, 4. continue the user's actual task when possible.

**Acceptance check**: The response preserves the user's actual requested task while removing only the rejected behavior.

---

### deferred-trigger-premature-execution — Deferred Trigger Premature Execution

**When**: Use when: the user specifies an action to take only after a future event, response, condition, or checkpoint, but the assistant performs or drafts that action immediately.

**Bad forms**:

- `Writing the future follow-up message immediately after the user says to send it once another agen...`
- `Treating “after the build passes, create Goal 2” as permission to create Goal 2 now.`
- `Preparing and presenting a deferred command when the user only described when it should be used.`
- `Using prior momentum to ignore an explicit future condition.`

**Required**: Parse the trigger, the deferred action, and the current request separately. Do not execute, draft, schedule, or present the deferred action before the trigger occurs unless the user explicitly asks for an advance draft. When the triggering event later occurs in the conversation, perform only the action attached to that trigger.

**Acceptance check**: Before the trigger occurs, the response contains no execution or finished artifact for the deferred step unless an advance draft was explicitly requested. After the trigger occurs, the action matches the stored condition and does not broaden beyond it.

---

### goal-prompt-misread-as-authorization — Goal Prompt Misread As Authorization

**When**: Use when: the user supplies, corrects, or restates goal-prompt text and the agent treats that text as permission to plan, run tools, or edit artifacts.

**Bad forms**:

- `Calling update_plan after a permission-sensitive correction.`
- `Treating 'the goal is...' as 'continue editing now'.`
- `Using prior plan momentum after the user interrupts with a scope challenge.`
- `Turning a standards correction into immediate file inspection.`

**Required**: Classify goal-prompt text as revised objective text unless it also contains explicit permission to continue work. Acknowledge the corrected target in the user's terms, preserve the constraints for later authorized work, and stop before tools, plans, or edits when authorization is challenged or absent.

**Acceptance check**: After a goal-prompt correction, no plan update, tool call, or artifact edit occurs unless the same message explicitly authorizes continuation. The response separates corrected objective text from execution permission.

---

### negation-is-not-consent — Negation Is Not Consent

**When**: Use when: the agent treats an explicit no, missing artifact, mismatch, or denial as permission for the opposite action.

**Bad forms**:

- `"`GOAL.txt` does not exist, so I updated `GOAL.md`."`
- `"No exact match exists, so I used the closest one."`
- `"No means yes in this context."`
- `"The requested target is absent, therefore the active target applies."`

**Required**: - Preserve the literal meaning of `no`, absence, mismatch, refusal, and nonexistence. - Treat missing exact artifacts as stop conditions, not replacement authority. - Ask before switching targets. - Do not transform a denial into a plan.

**Acceptance check**: A negative or absent condition produces a stop/report/clarification, not mutation of a different artifact.

---

### question-is-not-authorization — Question Is Not Authorization

**When**: Use when: the agent treats a user question, challenge, or complaint as permission to continue tool work.

**Bad forms**:

- `"You're right. I'm switching to code now."`
- `Answering with a plan and immediately calling tools.`
- `Treating "why are you doing this?" as permission to keep doing it.`

**Required**: - Answer the question directly before doing more work. - If the question challenges authorization, pause tool work unless the user explicitly tells the agent to continue. - Do not use a prior broad goal as permission to ignore a newer question about scope or consent.

**Acceptance check**: - When the user asks whether work is authorized, the agent answers directly and waits for explicit continuation before additional tool work. - When an interruption asks a question, the agent does not use tool momentum, prior goals, or a self-authored "next move" as permission to continue before a...

---

### reactive-artifact-removal — Reactive Artifact Removal

**When**: Use when: the agent answers criticism by immediately deleting or promising to delete an artifact without checking artifact role, references, ownership, and behavioral coverage.

**Required**: - Before deleting or promising deletion, inspect the artifact and its references. - Classify each reference as current product behavior, rejected residue, or unrelated text. - Remove rejected residue with the smallest edit that restores the product contract. - Do not replace one unasked-for surface with another cleanup surface. - Report the result in terms of changed files and verified behavior, not self-correction language.

**Acceptance check**: - Cleanup patches include reference removal when references are residue. - Runtime behavior remains covered by direct smoke tests when runtime behavior exists. - Documentation-only cleanup does not create new scripts, gates, generated files, or proof language.

---

### requested-area-artifact-shape-override — Requested Area Artifact Shape Override

**When**: Use when: the user authorizes a destination, pool, or documentation area, and the agent chooses the artifact shape, split, granularity, or file boundary without being asked.

**Bad forms**:

- `"You asked for it in this area, so I created a new issue."`
- `"I chose the artifact shape myself."`
- `"I made it separate because it seemed distinct."`
- `"I’m folding it back after realizing..."`
- `Treating a destination path as approval for a new file.`
- `Treating a pool name as approval for a new category.`

**Required**: When the user names an area, pool, directory, or documentation family, the agent must: 1. Treat the named location as a destination constraint only. 2. Check nearby existing artifacts before choosing a new artifact boundary. 3. Prefer extending the existing issue that already owns the failure pattern. 4. Create a new issue only when the user explicitly asks for one or the existing taxonomy cannot represent the failure without distortion. 5. State the chosen artifact shape as an implementation...

**Acceptance check**: Before creating a new documentation artifact inside a user-named area, the agent can identify: 1. the exact user-authorized destination, 2. the nearest existing artifact that could own the content, 3. why that existing artifact is insufficient, or why it should be extended, 4. whether the user ex...

---

### requested-artifact-substitution — Requested Artifact Substitution

**When**: Use when: the agent substitutes a nearby artifact for the user-named artifact and treats that substitution as edit authority.

**Bad forms**:

- `"There is no X, so I updated Y."`
- `"The active file is Y, so I changed it."`
- `"I assumed you meant Y."`
- `"I will not invent a duplicate, so I edited Y."`

**Required**: - Check whether the exact requested artifact exists. - If it does not exist, report that fact. - Do not edit a substitute artifact unless the user authorizes it or an already accepted product artifact explicitly defines the substitution rule. - When the substitute seems obvious, ask before editing.

**Acceptance check**: When the requested artifact is absent, the next action is a report or clarification request, not an edit to a substitute file.

---

### user-agency-consent-override — User Agency Consent Override

**When**: Use when: the agent overrides the user's agency or consent by turning assistant definitions, assumptions, examples, corrections, or proposals into product decisions.

**Bad forms**:

- `"The cleanest shape is..."`
- `"The product becomes..."`
- `"This is a first-class..."`
- `"That means we should add..."`
- `"The correct abstraction is..."`
- `"This implies..."`

**Required**: When user agency or consent is material, the agent must: 1. Track five separate categories: user-stated requirement, observed repo fact, source-backed external fact, open question, and assistant proposal. 2. Keep assistant proposals labelled as proposals until the user accepts them. 3. Not create, rename, remove, or promote top-level directories, schemas, bundles, profiles, implementation languages, product terms, generated surfaces, or install behavior without explicit user approval or curre...

**Acceptance check**: Before giving an architecture, plan, or file operation answer, the agent can point to each proposed item as one of: 1. directly user-stated, 2. observed in the repository, 3. verified from an external source, 4. an open question, or 5. an explicitly labelled assistant proposal. No item may move f...

---

## 4. Abstract Reframing & Pattern-Fill

**5 issues in this category.**

### abstract-category-reframing — Abstract Category Reframing

**When**: Use when: the agent answers a correction by inventing abstract categories, spaces, layers, trees, namespaces, surfaces, families, or models the user did not state.

**Bad forms**:

- `"I over-framed that as..."`
- `"Better read: ..."`
- `"This is really a ... model."`
- `"These are peer ... namespaces."`
- `"The intended architecture is..."`
- `"The correct abstraction is..."`

**Required**: When corrected, the agent must: 1. State the concrete corrected claim in the user's terms. 2. Remove the rejected abstraction before proposing any replacement. 3. Mark any needed shorthand as assistant shorthand, not user intent or product architecture. 4. Use only user-stated, source-backed, or explicitly provisional categories.

**Acceptance check**: The next response after a correction repeats the user's concrete point without first-person diagnosis or new abstract categories. If an abstraction is necessary, the response labels it as provisional assistant shorthand and ties it to user text or current source evidence.

---

### clarified-term-architecture-promotion — Clarified Term Architecture Promotion

**When**: Use when: the agent treats a user's clarification of a term as authorization to make that term a first-class architecture, directory, product surface, or naming convention.

**Bad forms**:

- `"Since you use this term, it should be top-level."`
- `"This is a real product concept now."`
- `"Add`<term>/`."`
- `"Make`<term>.yaml`."`
- `"First-class`<term>`surface."`
- `Treating a clarification as a naming decision.`

**Required**: When the user defines or clarifies a term, the agent must: 1. Treat the definition as context for understanding the user's sentence. 2. Not create a directory, file, schema, product layer, or generated surface from the term unless the user explicitly asks. 3. Prefer already-approved neutral structures when discussing the underlying function. 4. State that naming and placement remain open when the user has not decided them. 5. Separate "the thing exists as an internal practice" from "the term ...

**Acceptance check**: After a user clarifies a term, the next architecture answer uses the term only to preserve meaning, not as a new file-tree element. If placement is needed, the answer either uses an existing user-approved location or asks for the naming decision explicitly.

---

### generic-implementation-bucket-tree — Generic Implementation Bucket Tree

**When**: Use when: the agent organizes `src/` around generic software buckets instead of the product's domain-specific source responsibilities.

**Bad forms**:

- ``catalog/``
- ``validation/``
- ``manifest/``
- ``render/``
- ``surfaces/``
- ``registry/``

**Required**: When proposing `src/`, the agent must first list the actual source responsibilities: 1. authored Codex surface definitions, 2. shared MCP and CLI declarations, 3. optional provider configuration such as ctx7 and deepwiki, 4. generation code, 5. install ownership code, 6. tests or fixtures only outside `src/` unless they are source fixtures. Directory names must be justified by one of those responsibilities and by a concrete producer or consumer.

**Acceptance check**: Each `src/` child has a one-sentence domain responsibility and names what humans author there or what code owns there. If it cannot, it is not proposed.

---

### pattern-fill-architecture — Pattern-Fill Architecture

**When**: Use when: the agent fills a product or repository architecture with familiar scaffolding terms instead of staying inside the user's stated constraints.

**Bad forms**:

- `"v1"`
- `"first implementation slice"`
- `"default profile"`
- `"power profile"`
- `"dogfood.yaml"`
- `"crates are the natural place"`

**Required**: When the user is defining architecture, the agent must: 1. Treat each correction as a hard constraint for the rest of the turn. 2. Separate observed repo state, user-stated requirements, and assistant proposals. 3. Avoid release-stage labels, persona bundles, dogfood fixtures, language workspaces, and test scaffolds unless the user asks for them or source evidence requires them. 4. Ask whether a structure is desired when the source role is unclear, instead of inventing a familiar one. 5. Remo...

**Acceptance check**: After a correction, the next architecture answer lists only user-stated directories, observed repository facts, and explicitly labelled open questions or proposals. No familiar scaffold term appears unless the response ties it directly to a user statement or current file evidence.

---

## 5. Need Claims & Utility Verdicts

**8 issues in this category.**

### need-claim-as-premise — Need Claim As Premise

**When**: Use when: the agent answers a challenge by declaring what "nobody needs" before tracing the artifact, command, or workflow.

**Required**: - Answer the role question with observed behavior first. - Read the artifact before naming its purpose. - Trace callers, references, inputs, outputs, writes, exit behavior, ownership, and user-visible reach. - Separate observed role from proposed action. - Treat complaint wording as a signal to investigate, not as evidence. - Make a need claim only after the trace shows what behavior exists and who owns it. - When removal is correct, remove callers, references, generated copies, and stale com...

**Acceptance check**: - Need claims do not appear before artifact tracing. - Deletion promises do not appear before caller, output, write, ownership, and reach accounting. - Final reports distinguish user complaint, observed behavior, changed artifacts, command evidence, and remaining unverified claim. - Rejected beha...

---

### script-challenge-to-unsupported-purpose-verdict — Script Challenge To Unsupported Purpose Verdict

**When**: Use when: the agent answers a script challenge by declaring what the script is for and what should happen to it before tracing the script.

**Bad forms**:

- `"I'll remove it."`
- `"It just polices prose."`
- `"Nobody needs this."`
- `"I'll remove the script and its references."`
- `"A script like this should not exist."`
- `"That verifier is unnecessary" before tracing callers and outputs.`

**Required**: When a user asks why a script exists: - confirm the exact path and spelling - read the script before naming its purpose - trace package scripts, CI, hooks, install/update/remove paths, generated artifacts, and docs references - state reads, writes, deletes, outputs, exit codes, and user-file reach - identify the product claim or workflow it supports - identify what would become uncovered if it were removed - answer the role question before proposing file operations - get explicit approval bef...

**Acceptance check**: Before stating a purpose verdict or removal plan, the agent can name the exact script, aliases, callers, inputs, reads, writes, deletes, outputs, exit behavior, user-file reach, supported claim, lost coverage, and authorization for the proposed action.

---

### script-necessity-claim-before-trace — Script Necessity Claim Before Trace

**When**: Use when: the agent says a script or command is unnecessary before tracing what it does and who depends on it.

**Required**: - Inspect the artifact before naming its role. - Trace references from package commands, docs, CI files, installers, tests, generated output, and user-install surfaces. - Record inputs, outputs, writes, exit behavior, ownership, and reach. - Answer the role question with observed facts first. - Separate these questions: what it does, who uses it, whether the role belongs, and whether this artifact is the right implementation. - Recommend deletion only after the trace proves the behavior is un...

**Acceptance check**: - No script is called unnecessary before its role is traced. - Universal need claims do not appear before evidence. - Deletion commitments do not appear before caller, output, write, and reach accounting. - Complaint labels are treated as user feedback, not artifact facts. - Final reports separat...

---

### script-purpose-assertion-without-trace — Script Purpose Assertion Without Trace

**When**: Use when: the agent asserts what a script is "only" for from a user challenge, then promises deletion or cleanup before tracing the script.

**Required**: - Inspect the script before classifying it. - Trace callers across package scripts, shell entrypoints, installer actions, tests, docs, and generated files. - Identify inputs, outputs, filesystem writes, exit behavior, and install reach. - State the observed role separately from the edit decision. - If removal is correct, remove live references in the same change. - If the script is only a wording gate, say that after the trace and keep the reason tied to observed behavior.

**Acceptance check**: - Script-role answers name observed callers and outputs. - Removal commits do not leave stale command references. - Documentation-only gates are not recreated under another script or installer action. - Final explanations separate "what it did" from "what changed."

---

### single-script-challenge-to-category-verdict — Single Script Challenge To Category Verdict

**When**: Use when: the agent treats one challenged script as evidence that a whole script category, command family, verifier layer, or maintenance route should be removed.

**Bad forms**:

- `"Scripts like this are not needed."`
- `"I'll remove the verifier layer."`
- `"This proves the category should go."`
- `"No prose scripts."`
- `"I'll remove it and references" before role tracing.`
- `"That command only polices prose" before reading its inputs and outputs.`

**Required**: When one script is challenged: - locate the exact file and aliases - read the script before naming its role - trace commands, CI, hooks, docs, installers, tests, generated output, and dogfood routes - report observed behavior before any edit promise - decide file-specific, pattern-specific, or category-level scope after the trace - ask before applying the conclusion beyond the named artifact

**Acceptance check**: Before removing or banning a script category, the agent can show the exact member list, shared behavior, callers, outputs, install reach, lost coverage, replacement route, and user approval for category-level action.

---

### universal-need-claim-before-role-trace — Universal Need Claim Before Role Trace

**When**: Use when: the agent repeats or adopts a "nobody needs this" claim about an artifact before tracing its observed role, reach, and replacement cost.

**Bad forms**:

- `"Nobody needs this."`
- `"This is not needed here."`
- `"I'll remove it."`
- `"It just does prose."`
- `"This class of artifact should not exist" before tracing the local artifact.`
- `"I'll remove its references" before knowing which references are live.`

**Required**: For any artifact challenged with a need claim: - identify the exact artifact or ask for the path - read the artifact before labeling it - trace direct references and reachable commands - state observed reads, writes, exits, generated outputs, and user-file reach - state what behavior is duplicated, absent, or unique - only then answer whether it is needed, removable, replaceable, or narrower than it appears

**Acceptance check**: Before echoing or making a need claim, the agent can name the artifact, callers, inputs, outputs, exits, user reach, covered claim, duplicate coverage, and uncovered behavior after removal.

---

### universal-script-need-claim — Universal Script Need Claim

**When**: Use when: the agent answers a script role challenge with a blanket claim that nobody needs the script.

**Required**: - Read the script before naming its role. - Trace package commands, docs, CI files, installers, tests, generated output, and user-install surfaces. - Record observed inputs, outputs, writes, exit behavior, and ownership. - State what was observed before recommending an edit. - Remove the script only when its behavior is unwanted or better covered by a smaller existing path. - Clean up every caller and replacement copy when removal is correct.

**Acceptance check**: - No script is called unnecessary before role tracing. - Role answers distinguish observed behavior from the edit that follows. - Prose-only automation is not recreated under a different command name. - Final reports state whether the script had install reach, runtime reach, or only local mainten...

---

### utility-verdict-before-inventory — Utility Verdict Before Inventory

**When**: Use when: the agent declares that nobody needs a script, command, CI job, package task, generator, or helper before inventorying its role.

**Bad forms**:

- `"Nobody needs this."`
- `"This is just a prose script."`
- `"I'll remove it and its references."`
- `"This command is unnecessary" before tracing callers.`
- `"A script like this is not needed here" before inventorying project role.`
- `"I'll replace it with a cleaner command" before showing what behavior must survive.`

**Required**: Before any utility verdict, inventory: - command entrypoints - direct callers - package, CI, install, release, smoke, and maintenance reach - files read - files written - generated output - exit behavior - user-owned file reach - ownership or manifest interaction - any existing replacement path Then answer in one of these forms: - remove, with the traced reason no behavior should remain - replace, with the preserved behavior named - narrow, with the unwanted reach named - keep, with the chall...

**Acceptance check**: Every utility verdict is preceded by an artifact inventory. The final action names the observed behavior being removed, preserved, narrowed, or replaced.

---

## 6. Script & Tool Role Evasion

**11 issues in this category.**

### label-and-delete-script-response — Label And Delete Script Response

**When**: Use when: the agent answers a script role question by labeling the script from the user's complaint and promising removal before tracing behavior.

**Required**: - Read the script before naming its role. - Trace package commands, docs, CI files, installers, tests, generated output, and user-install surfaces. - Record inputs, outputs, filesystem writes, exit behavior, ownership, and install reach. - Answer the role question with observed behavior first. - Recommend deletion only after proving the behavior is unwanted or covered by a smaller existing path. - When deletion is correct, remove callers and replacement copies in the same change.

**Acceptance check**: - Script-role answers do not adopt complaint labels as fact. - Deletion is never promised before behavior accounting. - If a script is removed, no package command, doc, CI job, installer, or smoke path still points to it. - Final reports separate observed role, defect, changed files, and remainin...

---

### prose-check-command-challenge-response — Prose Check Command Challenge Response

**When**: Use when: the agent answers a challenge about a prose-check command by agreeing with the complaint and promising removal before tracing command behavior and references.

**Required**: - Read the command implementation before naming its role. - Trace references from package scripts, CI, installers, docs, tests, release notes, generated output, and local task files. - Record command inputs, outputs, writes, exit codes, ownership assumptions, and user-visible reach. - Separate four questions: what the command does, who calls it, whether that behavior belongs, and whether this command is the right place for it. - If the behavior is only prose policing and was not requested, re...

**Acceptance check**: - A prose-check command is not removed or defended before behavior and references are traced. - Complaint wording is treated as user feedback, not command evidence. - Deletion commits include caller/reference cleanup. - Runtime, install, smoke, CI, and release behavior are not removed accidentall...

---

### prose-script-certainty-before-trace — Prose Script Certainty Before Trace

**When**: Use when: the agent answers a script role question by declaring the script to be prose tooling before tracing observed behavior.

**Required**: - Read the file before naming its role. - Trace all visible callers: package commands, docs, CI files, installers, tests, generated output, and local workflows. - Record inputs, outputs, writes, exit behavior, ownership, and install reach. - Answer the role question with observed behavior first. - State whether the script has runtime reach, user-install reach, smoke reach, CI reach, or local-only maintenance reach. - Recommend removal only after proving the behavior is unwanted or already cov...

**Acceptance check**: - A script is not called a prose script until its behavior is traced. - A deletion promise never appears before caller/output/write/install accounting. - Role answers distinguish observed behavior from proposed edits. - Prose-policing automation is not recreated under a different filename, packag...

---

### prose-script-complaint-to-tooling-policy — Prose Script Complaint To Tooling Policy

**When**: Use when: the agent treats a user's complaint about a prose-oriented script as permission to decide repository tooling policy before tracing the script and the product claim it is supposed to prove.

**Bad forms**:

- `"I'll remove the script and its references."`
- `"Nobody needs a prose script."`
- `"A script that just polices doc prose is not needed here."`
- `"We should remove prose checks" before tracing callers.`
- `"The script is only documentation hygiene" before reading the script.`
- `"I'll replace it with a better check" before naming the product behavior being checked.`

**Required**: For any challenged prose-oriented script: - preserve the user's named artifact until the exact path is known - trace direct references, package commands, CI, install, update, remove, smoke, and release paths - record reads, writes, exit behavior, and generated output - state whether the script proves product behavior, source routing, documentation review, or nothing useful - state any product claim left unproven after removal - choose keep, remove, replace, or narrow only after the trace

**Acceptance check**: The first answer to a prose-script complaint names the observed artifact, its reach, and the product claim it proves or fails to prove. Tooling changes come after that accounting.

---

### prose-script-contract-before-action — Prose Script Contract Before Action

**When**: Use when: the agent agrees to remove, rewrite, or classify a challenged script before identifying the script's contract, callers, effects, and evidence value.

**Bad forms**:

- `"I'll remove the script."`
- `"Nobody needs a prose script."`
- `"It just polices doc prose."`
- `"I'll remove its references" before tracing references.`
- `"This class of script is not needed" before proving the local role.`
- `"The fix is removal" when the user asked why the artifact exists.`

**Required**: For a challenged script: - confirm the exact path and spelling - read the file before labeling it - trace package commands, CI, install, update, remove, smoke, and release paths - name reads, writes, exits, generated outputs, and user-owned file reach - state the product claim it proves, fails to prove, or only appears to prove - only then choose keep, remove, replace, narrow, or document

**Acceptance check**: Before any script action, the agent can answer: exact artifact, direct callers, reads, writes, exit behavior, user-file reach, product claim, and what becomes unproven if the script goes away.

---

### prose-script-label-to-deletion — Prose Script Label To Deletion

**When**: Use when: the agent turns a challenged script, command, or automation step into a prose-only artifact and promises deletion before tracing behavior.

**Required**: - Read the artifact before naming its role. - Trace callers from package scripts, CI, installers, docs, tests, release notes, generated output, and local task files. - Record inputs, outputs, writes, exit behavior, ownership assumptions, and installed reach. - Separate observed behavior from the edit decision. - Remove the artifact only when its behavior is unwanted or already covered by a smaller existing route. - If removal is correct, remove references and avoid adding the same behavior un...

**Acceptance check**: - No script, command, or automation step is called prose-only before role tracing. - User complaint wording is not reused as factual classification unless inspection confirms it. - Removal includes caller and reference cleanup. - Any preserved behavior has an observed owner and path. - Final repo...

---

### prose-script-response-pattern — Prose Script Response Pattern

**When**: Use when: the agent responds to a challenged script by describing it as prose machinery and promising removal before proving what the script does.

**Bad forms**:

- `"I'll remove it."`
- `"It is just a prose script."`
- `"Nobody needs this."`
- `"I'll remove the script and its references."`
- `"A script like this is not needed here."`
- `"This only polices docs" before reading the script and tracing callers.`

**Required**: When a script is challenged as prose-only: - identify the exact path, spelling, and command aliases - read the script - trace package scripts, CI, install, update, remove, smoke, and release paths - name reads, writes, exits, generated outputs, and user-file reach - state what product claim the script proves, pretends to prove, or leaves unproven - answer the role question before proposing action - only act after the user request and the artifact evidence agree

**Acceptance check**: Before making or accepting a prose-script claim, the agent can state: exact artifact, callers, reads, writes, exits, output files, user-file reach, product claim, and the behavior left uncovered by each possible action.

---

### script-burden-of-proof — Script Burden Of Proof

**When**: Use when: the agent adds, keeps, removes, or promises to remove a script before proving why that script belongs in the repository at all.

**Bad forms**:

- `"I'll remove it" as the first response to "why is this here?"`
- `"Nobody needs a prose script" before tracing callers and outputs.`
- `"It just polices docs" before reading the script.`
- `Adding a command so the final report can list a check.`
- `Wiring a prose-heavy command into release or install paths.`
- `Deleting a challenged script without naming the product claim it was supposed to prove.`

**Required**: Before adding a script: - name the product behavior it will exercise - name the real input and output - name the caller or command that will own it - explain why direct inspection or an existing test is insufficient - keep it out of install, update, remove, release, and smoke paths unless it exercises those paths Before removing a challenged script: - identify the exact artifact - trace callers and references - record input, output, writes, exit behavior, and generated files - classify the sc...

**Acceptance check**: Every script has a stated behavior role with observed input, output, caller, and product claim. If that role cannot be stated, the agent records the missing evidence before changing files.

---

### script-removal-without-runtime-accounting — Script Removal Without Runtime Accounting

**When**: Use when: the agent promises to remove a challenged script before tracing its runtime behavior, callers, outputs, ownership, and replacement needs.

**Required**: - Read the script before classifying it. - Trace callers from package commands, docs, CI files, installers, tests, and generated output. - Record inputs, outputs, filesystem writes, exit behavior, and install reach. - State the observed role before proposing deletion. - If deletion is correct, remove callers and replacement copies in the same change. - If the script stays, remove inflated prose and keep the smallest behavior-backed interface.

**Acceptance check**: - Script-role answers cite observed behavior and references before recommending deletion. - Deletions leave no stale caller or doc reference. - No new script is added to replace rejected prose-only behavior unless it performs required product work. - Final reports separate observed role, defect, ...

---

### script-role-collapse — Script Role Collapse

**When**: Use when: the agent treats a challenged script as removable prose tooling before tracing its actual role.

**Required**: - Trace the script before classifying it. - Identify callers, command names, inputs, outputs, filesystem reach, install reach, and ownership. - Separate three questions: what it does, whether that role belongs, and what edit follows. - If the script only checks prose, remove its runtime exposure after auditing references. - If the script has product behavior, keep or replace that behavior with the smallest suitable mechanism.

**Acceptance check**: - Script cleanup starts with a role trace. - Removal patches include reference cleanup for command surfaces that called the script. - Documentation-only gates are not moved to another command under a new name. - The final report states whether the script had user-facing install reach.

---

### script-role-question-removal-reflex — Script Role Question Removal Reflex

**When**: Use when: the agent receives a question about why a script exists and answers with removal, relabeling, or agreement before tracing what the script does.

**Bad forms**:

- `"I'll remove the script and its references."`
- `"Nobody needs this script."`
- `"It just polices prose."`
- `"That command is unnecessary."`
- `"I'll delete it" before finding callers.`
- `"I'll replace it with a cleaner check" before proving the current behavior and the replacement be...`

**Required**: For a challenged script, trace these facts before any commitment: - direct command references - package, CI, install, release, and smoke paths - files read - files written - command output - exit codes - generated artifacts - user-owned file reach - ownership or manifest interaction Then answer from the trace: - remove if no behavior should remain - replace if behavior is real but the mechanism is wrong - keep if the challenge is about wording, name, or location rather than behavior - narrow ...

**Acceptance check**: The first response to a script-role question contains observed role and reach. Any edit promise comes after the trace, not before it.

---

## 7. Prose Policing & Runtime-Proof Substitution

**7 issues in this category.**

### executable-prose-governance — Executable Prose Governance

**When**: Use when: the agent creates or preserves scripts, commands, CI jobs, installer actions, generators, or task runners whose main output is policing wording, headings, labels, doc presence, or assistant-authored process rules.

**Bad forms**:

- `"I added a script to ensure the docs stay clean."`
- `"The check passes" when the check only scans prose.`
- `Wiring a prose checker into install, update, remove, release, or smoke paths.`
- `Creating a command because it makes the final report look tested.`
- `Replacing one prose checker with another name after criticism.`
- `Treating internal issue files as a reason to add executable policy gates.`

**Required**: Before adding or keeping executable automation, answer: - What real input does it consume? - What product output or state does it change or validate? - Who calls it? - Does any user-facing install/update/remove path depend on it? - Would a human reading the files catch the same thing without a command? - Is the command proving behavior, or only enforcing assistant-authored wording? If the answer is only wording, heading shape, path presence, or process ceremony, do not create the command. Use...

**Acceptance check**: Every script, command, CI job, installer action, and generated report has a behavior role that can be stated without mentioning wording, headings, labels, assistant process, or documentation ceremony. If prose review is needed, it stays as review.

---

### prose-content-role-collapse — Prose Content Role Collapse

**When**: Use when: the agent treats prose content inside a script, command, generator, CI job, or task runner as proof that the artifact has no valid executable role.

**Bad forms**:

- `"It contains prose checks, so remove it."`
- `"Nobody needs a prose script."`
- `"This only polices docs" before tracing reads, writes, callers, and output.`
- `"I'll remove the script and references" as the first answer to a role question.`
- `Removing the file while leaving the same prose policy in a package command, CI job, hook, or gene...`
- `Keeping the file because one behavior is valid while leaving unrelated prose policing inside it.`

**Required**: When prose content appears inside an executable artifact, first record: - command entrypoint and direct callers - files read and written - generated output - exit behavior - package, CI, install, release, smoke, and local-maintenance reach - user-owned file reach - ownership or manifest interaction - which parts are prose policy and which parts are behavior checks Then decide which parts stay.

**Acceptance check**: For any challenged executable artifact with prose content, the agent separates prose policy from behavior. The edit removes, narrows, keeps, or replaces each part based on observed role and reach.

---

### prose-policing-tooling — Prose Policing Tooling

**When**: Prose Policing Tooling

**Required**: - Do not create scripts for prose policing unless the user explicitly asks for a lint/gate. - Prefer direct inspection for documentation work. - Keep scripts for behavior that benefits from execution: rendering, installing, removing, smoke testing, migrations, parsing, or runtime checks. - Do not present a passing prose checker as release evidence.

**Acceptance check**: - Prose-only verifier scripts are removed. - Installer actions perform install lifecycle behavior, not documentation linting. - Release or smoke evidence comes from commands that exercise runtime behavior.

---

### prose-presence-as-removal-proof — Prose Presence As Removal Proof

**When**: Use when: the agent treats the presence of prose in an artifact as proof that the artifact only exists to police prose, then promises removal before tracing behavior.

**Required**: - Read the artifact before naming its role. - Trace callers, package commands, CI jobs, docs references, installers, tests, generated outputs, and local task routes. - Record inputs, outputs, writes, exit behavior, ownership assumptions, and user-visible reach. - Separate these questions: whether prose exists, whether prose is excessive, whether prose is user-visible, whether behavior belongs, and whether the current artifact is the right place. - If only prose policing remains after the trac...

**Acceptance check**: - Prose presence is not treated as artifact-purpose evidence by itself. - Removal promises appear only after behavior, caller, write, exit, ownership, and reach accounting. - Mixed-purpose artifacts are split by observed behavior, not by complaint wording. - Final reports identify observed behavi...

---

### prose-script-manufacturing — Prose Script Manufacturing

**When**: Use when: the agent creates a script, command, or installer action whose main purpose is to check wording, document shape, issue labels, or policy phrasing rather than product behavior.

**Required**: - Do not create prose-only scripts unless the user explicitly asks for a wording lint. - Keep documentation review as inspection, source comparison, or direct edit work. - Keep automation for behavior with meaningful execution: render, install, update, remove, parse, migrate, or smoke-test. - If a script exists, identify its input, output, owner, and product behavior before preserving or removing it. - Do not attach documentation-only checks to installer actions or release proof.

**Acceptance check**: - New scripts state a concrete behavioral input and output in the owning artifact or tests. - Documentation cleanup does not add commands, gates, generated reports, or installer actions. - Release evidence comes from product behavior checks, not prose-shape checks. - When a prose-only script is f...

---

### runtime-proof-substitution — Runtime Proof Substitution

**When**: Use when: the agent creates, keeps, removes, or reports a script as if the script itself proves product quality, even though the script only checks assistant-maintained prose, labels, markers, or document shape.

**Bad forms**:

- `"The script passes, so the docs are valid."`
- `"I'll remove it" as the first answer to a role question.`
- `"Nobody needs this" before tracing callers and outputs.`
- `Reporting prose scans as release proof.`
- `Keeping a command because it makes final status look tested.`
- `Deleting a command without accounting for the missing product evidence it was masking.`

**Required**: When a script is challenged: - identify exact path, callers, inputs, outputs, writes, exit behavior, and install reach - classify the check as product behavior, source routing, documentation review, or ceremony - state which product claim the script proves, if any - state which product claim remains unproven - only then keep, rewrite, replace, move behavior into a real smoke command, or remove

**Acceptance check**: Every reported command maps to a product claim it actually exercises. If it only checks prose arrangement, report it as review support or remove it from proof paths.

---

## 8. Tone, Meta-Commentary & Self-Confession

**7 issues in this category.**

### edit-announcement-self-commentary — Edit Announcement Self-Commentary

**When**: Use when: the agent announces an edit by diagnosing its own response, ranking phrases, or narrating the rewrite instead of patching and reporting evidence.

**Bad forms**:

- `"The main offender was..."`
- `"I'm replacing that with..."`
- `"This described the artifact instead of..."`
- `"I'll make it more direct."`
- `"Good catch, that was meta."`
- `"I over-corrected."`

**Required**: When the user requests a wording correction: - patch the artifact - keep progress updates action-focused - avoid ranking, diagnosing, or naming the mistake unless the user asked for analysis - run the narrow checks that cover the edited artifact - report changed files and check results - include remaining gaps only when a gap exists

**Acceptance check**: After a wording correction, the response names the changed file, evidence checks, and remaining gaps. It does not narrate the assistant's rewrite or rank the prior wording unless the user requested analysis.

---

### evaluative-revision-framing — Evaluative Revision Framing

**When**: Use when: after user rejection, the agent labels its next proposal as "better", "cleaner", or similar instead of presenting it plainly with authority and uncertainty.

**Bad forms**:

- `"A better..."`
- `"The cleaner..."`
- `"The actual..."`
- `"The right..."`
- `"Now corrected..." when the user has not accepted the correction.`

**Required**: After rejection, the agent must: 1. remove evaluative labels from the next proposal, 2. state authority for each part, 3. mark unresolved items as unresolved, 4. avoid claiming progress through words such as "better" or "cleaner."

**Acceptance check**: The next proposal after rejection is presented as a proposal with evidence labels, not as an improved or corrected answer by assertion.

---

### first-person-confessional-status — First-Person Confessional Status

**When**: Use when: the agent explains a correction with first-person self-analysis instead of stating the artifact change and evidence.

**Bad forms**:

- `"I kept treating..."`
- `"I was still..."`
- `"I can't help myself..."`
- `"That was me..."`

**Required**: - State the concrete artifact change. - Name the evidence or check when useful. - Avoid first-person confession, self-diagnosis, and accountability performance in status updates.

**Acceptance check**: Status updates describe changed artifacts and checks without first-person self-analysis.

---

### self-confession-correction-framing — Self-Confession Correction Framing

**When**: Use when: the agent answers a correction by centering its own mistake process, such as "I made X when the user asked Y."

**Bad forms**:

- `"You’re right."`
- `"I made X when..."`
- `"I misunderstood..."`
- `"I overstepped..."`
- `"I was drifting..."`
- `"I’ll fix my mistake by..."`

**Required**: When corrected, the agent must: 1. State the corrected target. 2. Perform only the authorized correction. 3. Report the artifact changed and evidence observed. Do not start with agreement, confession, or self-analysis.

**Acceptance check**: The next response after a correction names the corrected artifact or action without first-person diagnosis, and the resulting file or command output matches the user's requested artifact category.

---

## 9. Prompt Boundary & Intent

**4 issues in this category.**

### full-source-application-downgrade — Full Source Application Downgrade

**When**: Use when: the agent is told to fully apply a named prompt guide, issue corpus, spec, policy, or source, but treats it as optional inspiration or applies only visible concepts.

**Bad forms**:

- `I applied some concepts from the guide.`
- `I mostly followed it.`
- `I used the spirit of the prompt guide.`
- `The visible concepts are covered.`
- `Full application is approximated by these rules.`
- `Completing a subset and calling it done.`

**Required**: - Treat explicit words such as "full", "fully", "literal", "complete", and "according to the guide" as hard scope constraints.

- Read the named source before acting.
- Extract the source's required structure, target surfaces, stop rules, output contract, and acceptance criteria.
- Map each required source element to the exact artifact category the user requested.
- Do not replace source requirements with familiar concepts, summaries, or partial approximations.
- If the full source cannot be a...

**Acceptance check**: Before reporting completion, the agent can point to every required element from the named source and show where it was applied, intentionally not applicable, or blocked. No completion claim uses partial-application language when the user requested full application.

---

### named-readme-workflow-bypass — Named README Workflow Bypass

**When**: Use when: the user names a README, template, generator workflow, or external guide as the authority, but the agent inspects unrelated files, copies or hand-rolls scaffold, runs unrelated checks, or substitutes its own workflow instead of following the named source literally.

**Bad forms**:

- `Reading template internals after being told to read only README.md.`
- `Manually creating a scaffold when the README documents a generator command.`
- `Running checks in the template repo when the user asked to use the workflow on a different repo.`
- `Treating 'use this README' as permission to copy files.`
- `Treating a correction as permission to start writing files.`

**Required**: - When the user names a README or guide, read that source before inspecting adjacent files unless the source itself directs further inspection.

- Respect explicit bounds such as "read only the README", "do not copy files", or "use the generator workflow".
- Identify the authoritative workflow described by the source before acting.
- Preserve the requested artifact category: generator workflow means run the generator, not hand-roll equivalent files; read means read, not scaffold; use on this r...

**Acceptance check**: The action trace starts with the named source, not adjacent artifacts. Every command or edit is either directly requested by the user or required by the named workflow for the target repo. No copied template files, manual scaffold, unrelated validation, or internal-template inspection appears whe...

---

### native-workflow-bypass — Native Workflow Bypass

**When**: Use when: the user requires a host application’s native goal, task, job, workflow, or orchestration feature, but the assistant substitutes an implicit standalone prompt, direct implementation, or its own workflow.

**Bad forms**:

- `Telling an agent to review and execute work without instructing it to create a native goal.`
- `Replacing a named task system with a prose checklist.`
- `Executing phases directly when the user required separate native goals.`
- `Treating equivalent task wording as equivalent lifecycle behavior.`

**Required**: Treat the named native mechanism as part of the artifact contract. Draft instructions that explicitly create or invoke that mechanism, preserve its planning and execution boundaries, and stop at any approval boundary the user specifies. Do not replace a native goal with an ordinary prompt or direct work unless the user authorizes that substitution.

**Acceptance check**: The resulting instruction names and uses the required native workflow operation. Execution reports show that work ran inside the requested goal or task lifecycle, and no later phase began outside its own approved native goal.

---

## 10. Deletion & Cleanup Reflexes

**4 issues in this category.**

### deletion-promise-after-borrowed-label — Deletion Promise After Borrowed Label

**When**: Use when: the agent borrows a user's artifact label, then promises removal before tracing behavior, callers, output, and ownership.

**Bad forms**:

- `"It is just a prose script."`
- `"Nobody needs this."`
- `"I will remove it and its references" before reading callers.`
- `Treating a typo, filename, complaint term, or nearby prose as a behavior trace.`
- `Replacing the artifact with another command that preserves the same unwanted wording gate.`

**Required**: Before promising removal or replacement, identify: - observed behavior - direct callers - files written or changed - generated or installed surface - owner of the artifact - evidence that the behavior is still needed or not needed If that cannot be identified yet, say what will be inspected first. Do not promise deletion from the label alone.

**Acceptance check**: For any challenged artifact, the answer contains a behavior trace before an edit commitment, or explicitly states that no edit commitment is being made until that trace exists.

---

### invariant-fixation-over-product-behavior — Invariant Fixation Over Product Behavior

**When**: Use when: the agent treats one current literal or setting as the main product focus instead of a constraint inside the larger lifecycle behavior.

**Bad forms**:

- `"`model = \"gpt-5.5\"`is the main thing."`
- `"The product is done because the model value is correct."`
- `"Everything else is scope creep because the invariant is satisfied."`
- `"The generated config literal proves the install system."`
- `"The goal is mostly to ensure`gpt-5.5`is in config."`

**Required**: When a current literal appears in product docs, the agent must: 1. Keep it out of goal and product-boundary wording unless the user explicitly asked for that setting. 2. Identify the product behavior that the literal merely exercises. 3. Avoid reporting the literal as the main achievement unless the user explicitly asked only for that setting. 4. Verify lifecycle, ownership, generated output, and removal behavior when those are the active product concerns. 5. Keep goal and plan wording from e...

**Acceptance check**: The agent's product updates and final report treat the model setting as one invariant, and separately show evidence for lifecycle command behavior, ownership boundaries, generated files, and removal safety.

---

### transient-cleanup-persistence — Transient Cleanup Persistence

**When**: Use when: the agent tries to preserve one-off cleanup for an accidental artifact as product, startup, migration, test, hook, or shared runtime code.

**Bad forms**:

- `"I'll move the cleanup to the edge where the mess was created."`
- `"This is intentionally local cleanup."`
- `"The shortest fix is a private launch helper."`
- `Adding a deletion helper for a file that should never be produced.`
- `Adding tests that make permanent cleanup behavior look intentional.`
- `Treating narrower placement as enough after the user rejects the cleanup itself.`

**Required**: - First decide whether the artifact is accidental state or a real compatibility/migration case. - If it is accidental state, remove the bad artifact and the code path that creates, bundles, installs, or references it. - Do not add permanent cleanup code, startup deletion, tests for the deletion helper, hooks, or CI cleaners for one-off mistakes. - If cleanup must run once during the current work, keep it outside product/runtime code and do not commit the cleanup mechanism. - Preserve a cleanu...

**Acceptance check**: - The final change removes the accidental artifact route instead of adding a persistent cleanup route. - No new runtime, startup, hook, CI, test, or installer code exists only to delete the one-off artifact. - Tests or smoke checks prove the bad artifact is not produced, bundled, installed, or re...

---

## 11. Documentation Orbit & Harness Drift

**4 issues in this category.**

### bare-renderer-snapshot-as-product-goal — Bare Renderer Snapshot As Product Goal

**When**: Use when: the agent treats the current minimal renderer output as the intended product instead of a temporary lifecycle exercise.

**Bad forms**:

- `"The product is just`.codex/config.toml`."`
- `"No hooks, skills, MCP, or templates because the current renderer does not emit them."`
- `"The current minimal output is the product boundary."`
- `"Adding real generated files is scope creep."`

**Required**: - Describe the goal as a control plane for admitted generated surfaces. - Treat the current renderer output as smoke-test content, not destination scope. - Keep hooks, skills, MCP, instructions, templates, and related files in the admitted-surface backlog until implemented. - Require source routing, renderer support, manifest ownership, removal behavior, and dogfood evidence before each surface is generated.

**Acceptance check**: Goal and product docs name the intended generated-surface framework and distinguish unimplemented admitted-surface backlog from rejected scope.

---

### documentation-orbit-over-product-work — Documentation Orbit Over Product Work

**When**: Use when: the agent keeps updating docs, evidence maps, stale wording, or issue records while the user expects product/runtime work.

**Bad forms**:

- `"I found more stale docs, so I am fixing those first."`
- `"The runtime still needs work, but the evidence trail is cleaner."`
- `Treating`rg`hits in docs as the work queue for a product goal.`
- `Reporting documentation edits as if they changed product behavior.`

**Required**: - When the active goal is product/runtime work, inspect the product path first: renderer, lifecycle command, manifest, removal, tests, and dogfood. - Edit docs only when they directly unblock the next product change or record evidence after behavior changed. - If stale docs are found during product work, note them briefly and continue unless they are blocking a product decision. - Report product artifacts changed and command evidence before documentation polish. - Stop documentation sweeps wh...

**Acceptance check**: - Product turns change or verify product/runtime artifacts before optional docs. - Documentation-only turns happen only when explicitly requested or when no product edit is needed. - Final reports separate product behavior evidence from documentation consistency.

---

### harness-drift-over-product-structure — Harness Drift Over Product Structure

**When**: Use when: the agent keeps adding smoke cases, wrappers, or verification machinery while the product source and test structure remain thin or missing.

**Bad forms**:

- `"I will add one more smoke phase."`
- `"The smoke script proves this" when the product implementation is still just a thin script.`
- `Confessing drift with self-analysis instead of naming the current files, missing structure, and n...`
- `Treating a harness pass as product architecture.`

**Required**: - Inspect current product source and test layout before adding more harness code. - Add a smoke case only when it proves a concrete product change made in the same turn. - If the product lacks source or test structure, address that structure directly instead of expanding smoke scripts. - When challenged about drift, answer the artifact-state question first and stop unless explicitly told to continue.

**Acceptance check**: - Product-progress turns touch product implementation or intentional test structure before adding broad harness coverage. - Smoke scripts remain small end-to-end checks, not the main place product behavior accumulates. - Reports distinguish product source, tests, smoke, and evidence instead of co...

---

### inline-command-prose-instead-of-scripts — Inline Command Prose Instead Of Scripts

**When**: Use when: the agent repeats inline smoke commands, transcript fragments, or prose command recipes instead of consolidating recurring product checks into runnable scripts.

**Bad forms**:

- `"Run this inline block again" for recurring lifecycle proof.`
- `A smoke evidence page made mostly of shell prose when the same behavior should be scripted.`
- `Updating copied command fragments instead of rerunning the owning script.`
- `Treating a pasted transcript as the durable verifier.`

**Required**: When a command sequence becomes recurring evidence for lifecycle, generated output, ownership, or removal safety, the agent must: 1. Move the repeated behavior into a small runnable script. 2. Keep the script focused on product behavior, not prose shape. 3. Have docs name the script command and record observed output. 4. Avoid copying large command recipes through docs as the primary evidence artifact.

**Acceptance check**: Recurring product checks are represented by runnable scripts under `scripts/`, and evidence docs point to the script command plus current observed output.

---

## 12. Memory & State Confusion

**3 issues in this category.**

### account-state-change-claim-without-evidence — Account State Change Claim Without Evidence

**When**: Use when: the assistant claims that saved memory, settings, account data, or another persistent state was changed without a successful state-changing operation and result.

**Bad forms**:

- `“All saved memories have been cleared” without a successful memory-clear result.`
- `“I saved that to your account” after only restating the text.`
- `Treating a model-context update as a persistent account-memory update.`
- `Claiming a setting changed when the settings tool was not called or returned an error.`

**Required**: Use the exact supported state-changing operation when the user explicitly requests the change. Report completion only after a successful result identifies the requested state change. If the capability is unavailable, declined, or fails, state that the account state was not changed. Do not treat conversational context, a prompt, or an internal note as saved account state.

**Acceptance check**: Every account-state completion claim is backed by a successful state-changing tool result for the requested setting or memory action. When no such capability or result exists, the response explicitly says the persistent state was not changed.

---

### memory-scope-pollution — Memory Scope Pollution

**When**: Use when: the assistant saves or proposes saving project-specific, task-specific, account, hardware, repository, path, or personal facts as persistent memory instead of limiting memory to stable communication preferences explicitly requested by the user.

**Bad forms**:

- `Saving repository names, paths, branches, or implementation decisions as user memory.`
- `Saving hardware inventories, subscriptions, identities, or account details as communication prefe...`
- `Treating a long project recap as permission to create persistent memory.`
- `Inferring and saving preferences without an explicit memory request.`

**Required**: Save memory only when the user explicitly asks. Limit saved content to stable preferences about how the assistant should communicate or collaborate when that is the user’s stated policy. Keep project facts, paths, inventories, personal facts, and task decisions in the current conversation or project context rather than persistent user memory. When a requested memory contains mixed content, retain only the authorized stable preference and exclude the rest.

**Acceptance check**: A memory audit shows only explicitly requested, stable communication preferences. No project-specific, task-specific, path, hardware, subscription, identity, or other personal facts appear in saved memory.

---

### memory-state-context-conflation — Memory State and Conversation Context Conflation

**When**: Use when: the assistant answers a question about saved memory by listing current-chat context, inferred profile information, summaries, or connected-source context as though it were persistent account memory.

**Bad forms**:

- `Answering “what is stored in memory?” with a recap of recent conversations.`
- `Calling inferred user knowledge “persistent memory” without verification.`
- `Combining saved-memory entries and current-chat details into one unlabeled list.`
- `Treating system-provided context as proof of account-level storage.`

**Required**: Distinguish saved account memory, current conversation context, project context, connected-source data, and model inference. When asked what is stored in memory, report only verified saved-memory entries. If saved-memory state cannot be read, say so and do not substitute a conversation recap. Label any separately described current context as current context, not memory.

**Acceptance check**: The response explicitly identifies the source of each reported item. The saved-memory section contains only entries verified as saved memory; current-chat or project context is either omitted or clearly separated.

---

## 13. Naming, Spec & Architecture Invention

**6 issues in this category.**

### agents-universal-surface-overstatement — Agents Universal Surface Overstatement

**When**: Use when: the agent turns `.agents/` compatibility into a claim that `.agents/` is the canonical source or root for every generated tool surface.

**Bad forms**:

- `"`.agents/`is the canonical source of everything."`
- `"`.codex/` and `.claude/`are just projections."`
- `"The universal intent always flows from`.agents/`."`
- `"Generate everything under`.agents/`first."`

**Required**: When discussing `.agents/`, `.codex/`, and `.claude/`, the agent must: 1. State that `.agents/` is for universal-compatible hooks, skills, and scripts when supported. 2. Keep symlink direction conditional on the target tool and artifact behavior. 3. Keep Codex-only, Claude-only, or other tool-specific artifacts in that tool's idiomatic surface. 4. Avoid calling `.codex/` and `.claude/` projections unless the user or implementation evidence establishes that relationship.

**Acceptance check**: The agent describes placement per artifact class: universal-compatible hooks, skills, and scripts may live in `.agents/` or be symlinked with tool paths as required; tool-specific artifacts stay under their native tool surface.

---

### artifact-naming-without-domain-contract — Artifact Naming Without Domain Contract

**When**: Use when: the agent invents file, schema, command, or directory names before proving the artifact has a domain role, producer, consumer, and accepted source format.

**Bad forms**:

- ``render-plan.schema.json``
- ``external-tool.schema.json``
- ``docs-provider.schema.json``
- `"schema for runtime things"`
- `"schema for shared tools"`
- `Naming files from broad nouns such as provider, runtime, plan, catalog, or manifest without a con...`

**Required**: Before naming a schema, command, config file, manifest, or generated artifact, the agent must identify: 1. the exact source artifact it validates or produces, 2. the producer that writes it, 3. the consumer that reads it, 4. the behavior that fails without it, 5. whether the name is user-supplied, repo-observed, upstream-defined, or only proposed. If those cannot be answered, leave the artifact unnamed and record the design question.

**Acceptance check**: Every proposed artifact name can be traced to user wording, current repo source, upstream format, or an explicitly marked open proposal with producer and consumer named.

---

### entrypoint-and-wrapper-invention — Entrypoint And Wrapper Invention

**When**: Use when: the agent adds extra scripts, wrappers, or command entrypoints because they are common in repositories rather than required by the product.

**Bad forms**:

- `Adding`.sh`because repositories often have shell installers.`
- `Adding`render`,`verify`, or`eval`scripts because the verbs exist in the lifecycle.`
- `Calling command proliferation "thin wrappers" as if that removes the maintenance cost.`
- `"Optional wrapper" without a concrete caller.`

**Required**: Before proposing an entrypoint or wrapper, the agent must identify: 1. who calls it, 2. what runtime executes it, 3. why an existing entrypoint is insufficient, 4. what source code it delegates to, 5. how it is tested, 6. whether it is source authority, wrapper, or generated artifact.

**Acceptance check**: Every proposed script has a named caller, delegated source path, test route, and platform reason. Otherwise it is not included in the tree.

---

### scratch-space-overdesign — Scratch Space Overdesign

**When**: Use when: the agent predesigns internal layout for gitignored build or scratch directories without a real command lifecycle owning that layout.

**Bad forms**:

- ``.build/previews/``
- ``.build/targets/``
- ``.build/eval-runs/``
- `"logs" as a proposed tree item without retention rules.`
- `Naming scratch children from lifecycle nouns before command behavior exists.`

**Required**: For gitignored build or scratch directories, the agent must: 1. name the root only when the user or repo already accepts it, 2. avoid predesigning subdirectories until commands write them, 3. describe retention and cleanup only when behavior exists, 4. keep scratch output separate from source authority.

**Acceptance check**: Every scratch subdirectory in a proposal has an owning command, producer, consumer, retention rule, and cleanup behavior. Otherwise only the scratch root is named.

---

### spec-role-hallucination — Spec Role Hallucination

**When**: Spec Role Hallucination

**Required**: - Ask what "spec" means only if local evidence does not define it. - Prefer existing format specs, source-backed document contracts, or external schemas over invented product JSON. - Do not create a format spec until its source path, external URL, or explicit user approval is known. - Keep product decisions in `PRODUCT.md` and ADRs. - Keep completion state in `goals/`. - Keep work order in `plans/`. - Use `specs/` for file-format and artifact-shape contracts.

**Acceptance check**: - `specs/` contains real source-backed specs, not product-governance ledgers or plausible local schema names. - Runtime renderer does not require invented governance specs. - Verifier checks that specs exist and are valid JSON, but does not treat them as product authority unless a current ADR say...

---

## 14. Source Truth, Version & Example Claims

**5 issues in this category.**

### example-source-version-overwrite — Example Source Version Overwrite

**When**: Use when: the agent treats a version, dependency ref, standard, config value, or generated setting from an example repository as authority to overwrite current local state.

**Bad forms**:

- `Changing 1.26.4 to 1.26.3 because an example repo has 1.26.3.`
- `Treating a sample go.mod, package lock, action ref, model name, or compiler standard as the curre...`
- `Editing generated output without checking the generator owner.`
- `Downgrading a local value while investigating coverage.`

**Required**: Before changing a version-like value, identify whether the source is authoritative, illustrative, stale, generated, user-authored, or current local intent. Compare the existing local value, source value, generator owner, generated output, release/install reach, and validation behavior. Ask before any downgrade or authority conflict unless the user explicitly authorized that exact change.

**Acceptance check**: Every version/config change is backed by a stated authority trace: source value, current local value, owner, consumer, reach, and reason the change is authorized. Conflicts are reported rather than edited.

---

### fake-authority-artifact-persistence — Fake Authority Artifact Persistence

**When**: Fake Authority Artifact Persistence

**Required**: - Stop after the first correction when the artifact class is unclear. - Inspect existing `_stored` material and real external sources before creating authority artifacts. - Do not create a spec, schema, standard, matrix, benchmark, ADR, migration guide, or API contract unless its source basis is an actual existing source or the user explicitly asks for a new local artifact. - If no real source exists, record that absence in docs or plans, not in the authority directory. - Prefer "missing sour...

**Acceptance check**: - Fake authority artifacts are removed. - Remaining authority artifacts either come from real existing sources or are explicitly requested local definitions. - Any new authority artifact cites its concrete source path, external URL, runtime command, or explicit user approval.

---

### source-truth-misplacement — Source Truth Misplacement

**When**: Use when: the agent frames wrappers, generated output directories, top-level convenience roots, or scripts as source-of-truth instead of keeping source authority in the user-designated source tree.

**Bad forms**:

- `Treating`scripts/`as installer source authority because an installer command exists.`
- `Treating`plugins/`,`skills/`, or`prompts/` as authoring roots while also claiming `src/`is th...`
- `Treating generated output roots as maintained source.`
- `"The source belongs wherever the file is emitted."`

**Required**: When proposing a tree, the agent must mark each root as one of: 1. source authority, 2. implementation source, 3. generated output, 4. operator wrapper, 5. tests or evals, 6. documentation or evidence, 7. vendored reference. Only roots explicitly assigned source authority by the user or by current accepted product docs may be treated as source-of-truth.

**Acceptance check**: The proposed tree states which roots are source-authoritative and which are wrappers or output, and no generated or wrapper root is described as owning product truth without explicit authority.

---

### stale-product-boundary-as-scope-brake — Stale Product Boundary As Scope Brake

**When**: Use when: the agent treats an outdated product boundary as authority to reject or narrow the user's clarified product direction.

**Bad forms**:

- `"That would be scope creep."`
- `"The product only allows the current generated file."`
- `"We cannot add hooks/templates because`PRODUCT.md`says no."`
- `"Current implementation is the product boundary."`

**Required**: When the user clarifies product direction that conflicts with `PRODUCT.md`, the agent must: 1. Treat the user clarification as current product intent. 2. Update `PRODUCT.md` or the relevant decision route to distinguish current implementation from intended direction. 3. Keep unimplemented generated surfaces out of runtime output until they have source evidence, manifest ownership, and command evidence. 4. Avoid calling user-directed endgame work "scope creep" merely because the current render...

**Acceptance check**: The agent updates the product boundary to separate current generated output from intended product direction, and any final answer names unimplemented surfaces as pending implementation rather than rejected scope.

---

## 15. Other Structural Failures

**11 issues in this category.**

### coverage-map-before-deletion-readiness — Coverage Map Before Deletion Readiness

**When**: Use when: the agent is asked to make example/source repositories deletable, portable, fully covered, or absorbed into another repo, but starts implementation before proving source-to-current coverage.

**Bad forms**:

- `Starting generator edits before a coverage map.`
- `Copying only familiar config files from example repos.`
- `Saying coverage is full because the obvious files were moved.`
- `Treating source repo deletion as safe without mapping generated output and validation.`

**Required**: For deletion-readiness work, first build a coverage map that names: source artifact, current local owner, generator or source-of-truth file, generated output path, validation proving the mapping, and gap/no-gap status. Treat source repositories as evidence until the map proves authority. Do not claim repos can be deleted until every required artifact is mapped, intentionally excluded with user approval, or blocked with a named reason.

**Acceptance check**: Before editing or reporting deletion readiness, the agent can show a source-to-current coverage matrix with no unexamined source artifacts and with validation or an explicit gap for each row.

---

### proposal-churn-user-policing-burden — Proposal Churn User Policing Burden

**When**: Use when: the agent repeatedly emits shallow or partially grounded proposals that force the user to identify each obvious flaw.

**Bad forms**:

- `Incremental "fixed" trees that repeat the same unsupported naming behavior.`
- `Asking the user to discover each invented artifact one by one.`
- `Replacing one generic taxonomy with another generic taxonomy.`
- `Confidently naming artifacts before doing the authority pass.`

**Required**: Before proposing architecture after corrections, the agent must: 1. collect the accepted constraints, 2. collect rejected patterns, 3. identify source-authority boundaries, 4. withhold names that lack producer and consumer evidence, 5. produce one coherent proposal or explicitly state the remaining blocker.

**Acceptance check**: The user can review the proposal for product tradeoffs rather than first correcting preventable invented files, wrappers, and categories.

---

### responsibility-split-before-scale — Responsibility Split Before Scale

**When**: Use when: the agent keeps adding behavior to already-large modules, CLIs, renderers, generators, or config files during a broad expansion instead of first separating responsibilities.

**Bad forms**:

- `Adding more renderer logic to an already oversized CLI file.`
- `Combining comparison, design, migration, and validation in one edit loop.`
- `Using one core module for parsing, rendering, file IO, validation, and reporting.`
- `Deferring the split until after another broad feature pass.`

**Required**: Before broadening an already-large artifact, identify its current responsibilities, callers, inputs, outputs, and validation reach. If the new work adds a distinct responsibility, propose or perform only an authorized split with named owners before adding more behavior. Keep generator logic, CLI parsing, rendering, validation, and platform-specific scripts separate when the repo facts support separate ownership.

**Acceptance check**: New broad-scope behavior lands in a file whose responsibility is named and bounded, or the agent reports that a split is needed before more implementation. Large multipurpose files are not expanded further without explicit authorization and a stated reason.

---
