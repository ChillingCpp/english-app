# English Learning App — Implementation Specification

## 1. Project Objective

Build a lightweight offline-first Android English vocabulary application.

The application is primarily a personal English-learning tool.

The MVP focuses on:

- offline dictionary
- vocabulary search
- word senses
- Vietnamese meanings
- contextual examples
- flashcards
- fill-in-the-blank active recall
- spaced repetition
- review history
- retrieval-time tracking
- context-specific accepted answers

The application should use as little memory and network access as reasonably possible.

Normal vocabulary lookup and review MUST work without an internet connection.

---

# 2. MVP Boundary

## Included

- Android application
- local SQLite database
- bundled vocabulary database
- word search
- word details
- multiple senses per word
- context labels
- examples
- flashcards
- fill-in-the-blank exercises
- English → Vietnamese recall
- Vietnamese → English recall
- Context → English recall
- answer normalization
- accepted alternative answers
- retrieval-time measurement
- spaced repetition
- review history
- local learning progress

## Excluded from MVP

Do NOT implement:

- user accounts
- backend
- cloud database
- online authentication
- payment
- social features
- cloud synchronization of learning progress
- runtime AI API calls
- AI-generated questions during review
- speaking assessment
- grammar system
- writing assessment
- multiplayer
- unnecessary gamification

The MVP should remain a small offline Android application.

---

# 3. Technology Requirements

## Platform

Native Android.

Use Kotlin.

Reason:

- lightweight
- native Android integration
- good SQLite/Room support
- no JavaScript runtime required
- appropriate for an offline-first utility application

---

# 4. Local Storage

Use SQLite as the persistent local database.

Room may be used as the Android database abstraction layer if it does not introduce unnecessary complexity.

The application MUST NOT load the entire dictionary into memory.

Search and review operations should query only the required records.

Example:

```text
User searches:
"maintain"

        ↓

SQLite query

        ↓

Only matching records loaded

        ↓

Display result
```

Do NOT do:

```text
SQLite
   ↓
Load all 3000+ words
   ↓
Store entire dictionary in RAM
   ↓
Search in Kotlin
```

---

# 5. Data Architecture

Separate static dictionary content from mutable user learning data.

Conceptually:

```text
Dictionary Data
├── Word
├── Sense
├── Context
├── Example
├── Topic
└── Accepted Answer

Learning Data
├── Learning State
└── Review History
```

Dictionary content should be treated as mostly immutable.

Learning data changes frequently.

---

# 6. Word Model

A word is a spelling/lexical item.

Example:

```text
bank
```

A word MUST NOT be assumed to have only one meaning.

---

# 7. Sense Model

A sense represents a distinct meaning of a word.

Example:

```text
bank

├── finance
│   └── ngân hàng
│
└── geography
    └── bờ sông
```

Learning state should be associated with a sense whenever practical.

This prevents:

```text
bank = mastered
```

from incorrectly implying that every sense of `bank` is mastered.

---

# 8. Context Model

Each sense may have multiple contexts.

Example:

```text
iron
└── resource
    ├── mining
    ├── industry
    ├── steel production
    └── economy
```

Contexts are metadata for learning and content organization.

They are NOT necessarily separate vocabulary items.

---

# 9. Example Model

Each example should contain:

```text
Original sentence
Blank sentence
Target answer
Accepted alternative answers
```

Example:

```text
Original:
Regular exercise helps maintain good health.

Blank:
Regular exercise helps ______ good health.

Answer:
maintain

Accepted:
[explicitly validated alternatives only]
```

---

# 10. Review Types

The MVP supports four review modes.

## 10.1 Flashcard

Display:

```text
maintain

verb

duy trì
```

The user reveals the information and reports whether they recalled it.

Flashcards are primarily for learning/review orientation.

---

## 10.2 English → Vietnamese

Prompt:

```text
maintain
```

User enters:

```text
duy trì
```

---

## 10.3 Vietnamese → English

Prompt:

```text
duy trì
```

User enters:

```text
maintain
```

This mode is especially important for active vocabulary.

---

## 10.4 Context → English

Prompt:

```text
Regular exercise helps ______ good health.
```

User enters:

```text
maintain
```

This is the preferred contextual active-recall mode.

---

# 11. Answer Evaluation

The application MUST NOT require an exact raw string match.

Before comparison, normalize the answer.

Normalization should include:

- trim leading/trailing whitespace
- lowercase
- normalize repeated whitespace
- Unicode normalization where appropriate

Example:

```text
" Maintain "
"maintain"
"MAINTAIN"
```

should normalize to the same value.

---

# 12. Accepted Answers

Every exercise has:

```text
primary_answer
accepted_answers[]
```

Example:

```text
primary_answer:
maintain

accepted_answers:
[
    "..."
]
```

An answer is accepted only when it is explicitly present in the validated accepted-answer set.

Do NOT use fuzzy matching to automatically accept arbitrary words.

Do NOT call an LLM to determine whether an answer is correct.

Do NOT assume that dictionary synonyms are interchangeable.

Synonym validity is context-dependent and should be resolved during content generation.

---

# 13. Retrieval Time

For active-recall exercises, record the time required to produce the first valid answer.

Conceptually:

```text
question shown
      ↓
timer starts
      ↓
user submits answer
      ↓
valid answer
      ↓
timer stops
```

Store:

```text
retrieval_time_ms
```

If the user submits an invalid answer and subsequently gives a valid answer, the implementation should preserve enough information to distinguish:

- first attempt time
- first valid retrieval time
- number of attempts

The first valid retrieval time is the primary retrieval-speed metric.

---

# 14. Retrieval Breadth

The MVP may support multiple accepted answers.

Example:

```text
maintain
retain
preserve
```

If an exercise explicitly allows multiple valid answers, the application may record:

```text
valid_retrieval_count
```

However:

- do not require multiple answers for every exercise
- do not penalize users for not producing every synonym
- do not treat synonym quantity as the same thing as mastery

Retrieval breadth is an additional metric.

Retrieval speed is the primary fluency metric.

---

# 15. Spaced Repetition

The review engine must be independent from the UI.

Conceptually:

```text
Review Result
      ↓
SRS Engine
      ↓
Updated Learning State
      ↓
next_review_at
```

The initial implementation may use a simple established SRS algorithm such as SM-2.

The SRS implementation should be replaceable later.

Do not tightly couple the UI to SM-2-specific fields or behavior.

---

# 16. Review State

Learning state should contain information such as:

```text
sense_id
review_type
due_at
interval
ease_factor
repetitions
lapses
last_review_at
```

Review state should be persistent across application restarts.

---

# 17. Review History

Review history should be append-only.

Each review event may contain:

```text
sense_id
review_type
presented_at
answered_at
retrieval_time_ms
user_answer
normalized_answer
is_correct
matched_answer
attempt_count
```

Historical review records MUST NOT be silently overwritten.

Current learning state may be updated from these events.

---

# 18. Review Selection

The review engine should support:

```text
Due reviews
New words
Topic reviews
Sense reviews
```

The primary review queue should prioritize items whose `due_at` has passed.

Example:

```text
Today

Due:
37 items

New:
15 items
```

The application should not force the user to review the entire dictionary.

---

# 19. Dictionary Search

Search should be performed using SQLite.

Minimum requirements:

- exact word lookup
- prefix lookup
- case-insensitive lookup

Possible later extensions:

- fuzzy search
- typo tolerance
- Vietnamese meaning search

Do not implement fuzzy search in MVP unless it is genuinely necessary.

---

# 20. Offline Database Packaging

The vocabulary database should be generated outside the Android application.

Pipeline:

```text
Vocabulary Dataset
       ↓
Validation
       ↓
SQLite generation
       ↓
dictionary.db
       ↓
Android project assets
       ↓
First application launch
       ↓
Copy/open database locally
```

The application should not need to call a remote API to obtain dictionary content.

---

# 21. Database Versioning

The bundled dictionary database should have a version.

Example:

```text
dictionary_version = 1
```

When vocabulary content changes:

```text
version 1
    ↓
version 2
    ↓
version 3
```

The application should be able to determine which database version it is using.

Do not mix incompatible schemas silently.

---

# 22. Application Architecture

Use a simple layered architecture.

Recommended:

```text
UI
│
├── Dictionary Screen
├── Word Detail Screen
├── Review Screen
└── Progress Screen
        │
        ↓
ViewModel / Presentation Logic
        │
        ↓
Domain
│
├── Dictionary Service
├── Review Engine
├── Answer Evaluator
└── SRS Engine
        │
        ↓
Data Layer
│
├── Dictionary Repository
├── Learning Repository
└── SQLite / Room
```

Do not create excessive abstraction layers.

The architecture should remain understandable for a solo developer.

---

# 23. AI Must NOT Be a Runtime Dependency

The normal application workflow is:

```text
Android
  ↓
Local database
  ↓
Review engine
  ↓
SRS
```

NOT:

```text
Android
  ↓
AI API
  ↓
Generate question
  ↓
Evaluate answer
```

The application must remain usable without:

- API keys
- internet access
- AI providers
- backend servers

AI is used during content preparation, not during normal learning.

---

# 24. Content Generation Pipeline

Content is prepared separately from the application.

```text
Oxford 3000
      ↓
Content Generation Agent
      ↓
Sense / Context / Example generation
      ↓
Validation
      ↓
Manual inspection
      ↓
JSON dataset
      ↓
SQLite generator
      ↓
dictionary.db
      ↓
Android app
```

The Android project should consume validated data.

The Android code should not contain the content-generation logic.

---

# 25. Development Workflow

Development should be repository-based.

Recommended project structure:

```text
english-app/
├── app/
├── data/
├── docs/
├── scripts/
├── tests/
├── .github/
├── README.md
└── ...
```

Important development artifacts:

```text
docs/
├── implementation-spec.md
├── learning-model.md
├── content-generation-spec.md
├── data-model.md
├── review-engine.md
└── decisions.md
```

These documents are part of the project context for AI coding agents.

---

# 26. Multi-Device AI Agent Workflow

The project should support development from multiple devices.

Example:

```text
Desktop PC
    │
    │ Git
    ↓
 GitHub Repository
    ↑
    │ Git
    │
Android / Termux
```

The devices do NOT need to share a local filesystem.

GitHub is the synchronization point for:

- source code
- documentation
- tests
- task state
- agent instructions
- implementation changes

---

# 27. Device-Agnostic Agent Context

Every AI coding agent should be able to reconstruct the project context from the repository.

The repository MUST contain:

```text
AGENTS.md
README.md
docs/
```

`AGENTS.md` should describe:

- project purpose
- current architecture
- coding rules
- commands
- testing procedure
- important constraints
- current implementation status
- files that should be read before making changes

An agent must NOT assume that previous chat history is available.

The repository is the source of truth.

---

# 28. Agent Handoff Protocol

When moving from one device/agent to another:

```text
Agent A
   ↓
make changes
   ↓
run tests
   ↓
update project state
   ↓
git commit
   ↓
git push
   ↓
GitHub
   ↓
Agent B
   ↓
git pull
   ↓
read AGENTS.md
   ↓
inspect current git state
   ↓
continue work
```

The next agent MUST inspect the repository before changing code.

It should NOT assume that the previous agent completed a task simply because the task was mentioned in a conversation.

---

# 29. Task State

Maintain a lightweight task file:

```text
docs/TASKS.md
```

Example:

```md
# Current Tasks

## Completed

- [x] Android project initialized
- [x] SQLite database initialized
- [x] Dictionary search
- [x] Word detail screen

## In Progress

- [ ] Review screen

## Next

- [ ] Answer evaluator
- [ ] SRS engine
- [ ] Review history
```

Agents should update this file when completing meaningful implementation work.

Do not mark a task complete unless the implementation and relevant tests are complete.

---

# 30. Agent Handoff Notes

Maintain:

```text
docs/SESSION.md
```

This file contains only temporary development state.

Example:

```md
# Current Development State

## Current Task

Implementing answer normalization.

## Completed

- Answer input UI
- Review model
- Basic repository

## Remaining

- Unicode normalization
- Accepted answer tests

## Known Issues

- Review timer currently starts too early.

## Next Agent

Run:

npm test

Then inspect:

app/src/...
```

The exact commands and paths must match the actual project.

After a task is fully completed, stale session information should be removed or updated.

---

# 31. Git Rules for Agent Collaboration

Agents MUST:

1. inspect current branch/status
2. pull latest changes before starting
3. avoid overwriting unrelated work
4. make focused commits
5. run relevant tests
6. update documentation when architecture changes
7. push completed work when working in a shared repository workflow

Prefer commits such as:

```text
feat: add dictionary search
feat: implement review timer
fix: normalize answer whitespace
test: add accepted answer cases
docs: update review engine
```

Avoid meaningless commits such as:

```text
update
fix
changes
AI stuff
```

---

# 32. Preventing Device Conflicts

Two agents should NOT simultaneously modify the same feature without coordination.

Before starting:

```text
git pull
git status
```

Check:

```text
docs/TASKS.md
docs/SESSION.md
```

If another agent is currently working on the same component, do not overwrite its changes.

Prefer separate branches for larger parallel tasks.

For simple sequential work:

```text
main
 ↓
Agent A
 ↓
push
 ↓
Agent B
 ↓
pull
```

is sufficient.

---

# 33. Using Termux on Android

The Android device may be used as a lightweight development environment.

Example workflow:

```text
Termux
   ↓
Linux environment
   ↓
Git
   ↓
GitHub repository
```

The Android device does not need to contain the full development state independently.

The repository remains the synchronization mechanism.

The agent running on Android should:

```text
git pull
```

before continuing work.

After completing work:

```text
git add
git commit
git push
```

The desktop agent can then pull the changes.

---

# 34. Important Distinction: Source Sync vs App Data Sync

GitHub synchronization is ONLY for development artifacts.

It must NOT be used as the runtime synchronization mechanism for:

- review history
- learning state
- user progress
- personal vocabulary
- private user data

MVP learning data is local to the Android device.

Future cloud synchronization, if ever needed, should be designed separately.

---

# 35. Agent Recovery

If an agent loses its conversational context, it should be able to recover from the repository.

Recovery sequence:

```text
1. git pull
2. read AGENTS.md
3. read README.md
4. read docs/implementation-spec.md
5. read docs/TASKS.md
6. read docs/SESSION.md
7. inspect git status
8. inspect recent commits
9. run tests
10. continue the current task
```

The agent should not ask the user to repeat project requirements that are already documented in the repository.

---

# 36. AI Coding Agent Rules

Before implementing a task, the agent MUST:

1. understand the relevant specification
2. inspect existing code
3. inspect existing tests
4. determine whether the requested functionality already partially exists
5. avoid unnecessary rewrites

The agent MUST NOT:

- rewrite the project architecture without justification
- add backend infrastructure unnecessarily
- add AI API integration to the MVP
- introduce cloud synchronization
- add dependencies without reason
- implement features outside the current task
- delete working functionality without justification

---

# 37. Testing Requirements

Every core learning component must be unit-testable.

At minimum, test:

## Answer normalization

```text
" maintain "
"MAINTAIN"
"maintain"
```

→ equivalent.

## Answer matching

```text
primary answer
accepted answer
invalid answer
```

## Sense separation

Different senses of the same word must remain independent.

## Retrieval timer

Verify:

- timer starts correctly
- first valid retrieval is recorded
- invalid attempts are handled
- review completion stops the timer

## SRS

Verify deterministic scheduling for known inputs.

## Persistence

Verify that:

- learning state survives application restart
- review history is persisted
- dictionary content remains available offline

---

# 38. Performance Requirements

The application should prioritize low memory usage.

Requirements:

- query SQLite instead of loading the entire dictionary
- avoid unnecessary caching
- avoid large in-memory collections
- avoid unnecessary background services
- avoid network requests during normal use
- release screen-specific resources when no longer needed

The dictionary size is expected to be manageable, but implementation should remain scalable beyond the initial 3000 words.

---

# 39. Future Compatibility

The architecture should allow future additions without requiring a complete rewrite.

Possible future features:

- additional vocabulary datasets
- larger vocabulary collections
- FSRS
- more review modes
- grammar
- AI-generated content
- speaking practice
- cloud synchronization
- user-created vocabulary

These features are NOT part of MVP.

Do not implement them prematurely.

---

# 40. Definition of Done

A feature is considered complete only when:

- implementation works
- relevant tests pass
- offline operation is preserved
- no unnecessary dependency was introduced
- documentation is updated when necessary
- task state is updated
- code is committed
- repository state is clean enough for another agent to continue

For cross-device development, the completed state should be pushed to the shared Git repository.

---

# 41. Core Product Principle

The application should remain:

```text
Lightweight
Offline-first
Context-aware
Active-recall focused
SRS-driven
Simple
Testable
Agent-friendly
```

The primary learning loop is:

```text
Word
  ↓
Sense
  ↓
Context
  ↓
Understand
  ↓
Active Recall
  ↓
Answer Evaluation
  ↓
Retrieval Metrics
  ↓
Spaced Repetition
  ↓
Future Recall
```

The primary development loop is:

```text
Specification
  ↓
AI Agent
  ↓
Implementation
  ↓
Tests
  ↓
Git Commit
  ↓
GitHub
  ↓
Another Device / Agent
  ↓
Repository Context
  ↓
Continue
```

Both loops should remain independent.

The learning system belongs to the application.

The Git/GitHub workflow belongs to the development process.