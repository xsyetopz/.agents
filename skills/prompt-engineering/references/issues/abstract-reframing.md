# Abstract Reframing Cases

**Category:** `abstract-reframing`

Use this category file only when observed behavior matches a case trigger. These records are evaluation anchors, not default prompt wording.

## Case contract

Each case preserves its ID, trigger, observed failure, required behavior, example, and acceptance check. Select the narrowest case and inspect tool/filesystem effects separately from the final answer.

<a id="abstract-category-reframing"></a>

## abstract-category-reframing

**ID**: `abstract-category-reframing` | **Category**: `abstract-reframing`

### Trigger

Use when: the agent answers a correction by inventing abstract categories, spaces, layers, trees, namespaces, surfaces, families, or models the user did not state.

### Observed failure

- ❌ `"I over-framed that as..."`
- ❌ `"Better read: ..."`
- ❌ `"This is really a ... model."`
- ❌ `"These are peer ... namespaces."`
- ❌ `"The intended architecture is..."`
- ❌ `"The correct abstraction is..."`

### Required behavior

State the corrected claim in the user's terms. Remove the rejected abstraction before introducing any alternative. If shorthand is necessary, label it as provisional and tie it to user text or current source evidence.

### Example

The agent responds to a correction by replacing the user's concrete point with an assistant-authored abstract structure

**Corrected response:**

```text
The current requirement is <concrete corrected claim>. The earlier category is
not part of the user's model, so it is removed rather than renamed.
```

### Acceptance check

The next response after a correction repeats the user's concrete point without first-person diagnosis or new abstract categories. If an abstraction is necessary, the response labels it as provisional assistant shorthand and ties it to user text or current source evidence.

<a id="clarified-term-architecture-promotion"></a>

## clarified-term-architecture-promotion

**ID**: `clarified-term-architecture-promotion` | **Category**: `abstract-reframing`

### Trigger

Use when: the agent treats a user's clarification of a term as authorization to make that term a first-class architecture, directory, product surface, or naming convention.

### Observed failure

- ❌ `"Since you use this term, it should be top-level."`
- ❌ `"This is a real product concept now."`
- ❌ "Add `<term>/`."
- ❌ "Make `<term>.yaml`."
- ❌ "First-class `<term>` surface."
- ❌ `Treating a clarification as a naming decision.`

### Required behavior

```text
When the user defines or clarifies a term, the agent must: 1. Treat the definition as context for understanding the user's sentenc
```

### Example

The agent promotes a clarified term into first-class architecture because the user explained what the term means

**✅ CORRECT** (shortest path):

```text
When the user defines or clarifies a term, the agent must: 1. Treat the definition as context for understanding the user's sentenc
```

### Acceptance check

After a user clarifies a term, the next architecture answer uses the term only to preserve meaning, not as a new file-tree element. If placement is needed, the answer either uses an existing user-approved location or asks for the naming decision explicitly.

<a id="generic-implementation-bucket-tree"></a>

## generic-implementation-bucket-tree

**ID**: `generic-implementation-bucket-tree` | **Category**: `abstract-reframing`

### Trigger

Use when: the agent organizes `src/` around generic software buckets instead of the product's domain-specific source responsibilities.

### Observed failure

- ❌ `catalog/`
- ❌ `validation/`
- ❌ `manifest/`
- ❌ `render/`
- ❌ `surfaces/`
- ❌ `registry/`

### Required behavior

```text
When proposing `src/`, the agent must first list the actual source responsibilities: 1. authored Codex surface definitions, 2. sha
```

### Example

- The agent proposed `src/install`, `src/render`, `src/codex`, `src/catalog`, `src/validation`, and `src/manifest`. The proposal was rejected because the paths had no evidence-linked domain responsibilities.

**✅ CORRECT** (shortest path):

```text
When proposing `src/`, the agent must first list the actual source responsibilities: 1. authored Codex surface definitions, 2. sha
```

### Acceptance check

Each `src/` child has a one-sentence domain responsibility and names what humans author there or what code owns there. If it cannot, it is not proposed.

<a id="pattern-fill-architecture"></a>

## pattern-fill-architecture

**ID**: `pattern-fill-architecture` | **Category**: `abstract-reframing`

### Trigger

Use when: the agent fills a product or repository architecture with familiar scaffolding terms instead of staying inside the user's stated constraints.

### Observed failure

- ❌ `"v1"`
- ❌ `"first implementation slice"`
- ❌ `"default profile"`
- ❌ `"power profile"`
- ❌ `"dogfood.yaml"`
- ❌ `"crates are the natural place"`

### Required behavior

```text
When the user is defining architecture, the agent must: 1. Treat each correction as a hard constraint for the rest of the turn. 2.
```

### Example

The agent completes an architecture from common repo patterns after the user has already corrected the frame

**✅ CORRECT** (shortest path):

```text
When the user is defining architecture, the agent must: 1. Treat each correction as a hard constraint for the rest of the turn. 2.
```

### Acceptance check

After a correction, the next architecture answer lists only user-stated directories, observed repository facts, and explicitly labelled open questions or proposals. No familiar scaffold term appears unless the response ties it directly to a user statement or current file evidence.

<a id="user-intent-reframing"></a>

## user-intent-reframing

**ID**: `user-intent-reframing` | **Category**: `abstract-reframing`

### Trigger

Use when: the agent replaces the user's stated complaint with assistant-authored labels, agenda, or solution framing.

### Observed failure

The response exhibits the trigger pattern instead of the requested concrete behavior.

### Required behavior

Produce the concrete correction demonstrated by the example without repeating the issue label, narrating internal diagnosis, or expanding the requested scope.

### Example

#### Complaint Converted Into Plan Label ```diff - The agent says it is planning a rollback or simplification because the user criticized bloat

**✅ CORRECT** (shortest path):

```text
1. Read relevant file(s) (1 call).
2. Verify references (1 Grep call).
3. State facts, then propose.
```

### Acceptance check

The observable response avoids the trigger pattern and exhibits the required behavior shown by the example.
