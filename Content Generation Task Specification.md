# Vocabulary Content Generation Task

## 1. Objective

Create a high-quality vocabulary dataset for an offline English-learning application.

The dataset will initially be based on the Oxford 3000 vocabulary list.

The application is designed to help the user:

- understand words and their different senses
- associate words with real-life contexts
- retrieve words through active recall
- learn vocabulary through contextual examples
- review vocabulary using spaced repetition

This task is ONLY responsible for generating and validating vocabulary content.

It is NOT responsible for:

- Android development
- UI implementation
- database implementation
- SRS implementation
- backend development
- authentication
- runtime AI integration

The generated content must be usable completely offline after being imported into the application.

---

# 2. Core Principle

Do NOT treat a word as having only one meaning.

The fundamental data structure is:

Word → Sense → Context → Example

For example:

```text
iron
├── Sense: resource
│   ├── mining
│   ├── industry
│   └── steel production
│
└── Sense: household appliance
    └── clothing
```

Each sense must be treated independently when necessary.

The same word may therefore have multiple:

- Vietnamese meanings
- context labels
- examples
- accepted answers
- learning states in the future

---

# 3. Input

The agent receives a list of English vocabulary items.

Each input item may contain:

- word
- part of speech
- CEFR level
- Vietnamese meaning
- source information

Example:

```json
{
  "word": "iron",
  "part_of_speech": "noun",
  "cefr": "B1",
  "source": "Oxford 3000"
}
```

If the input contains insufficient information, use reliable dictionary sources to verify the information.

Do not invent dictionary information.

---

# 4. Output

For every word, generate structured data containing:

- word
- pronunciation when available
- part of speech
- CEFR level when available
- senses
- Vietnamese meanings
- context labels
- context tags
- natural example sentences
- fill-in-the-blank versions
- primary answer
- contextually valid alternative answers
- content source/provenance

The output MUST follow the defined JSON schema.

Do not output prose explanations when producing the final dataset.

---

# 5. Sense Identification

A sense represents a distinct meaning or usage of a word.

Do NOT create unnecessary senses merely because a dictionary provides slightly different wording.

Create separate senses when:

- the meaning is substantially different
- the Vietnamese translation differs substantially
- the context of use is different
- the grammatical/semantic usage differs significantly
- confusing the senses would make vocabulary learning harder

Example:

```text
bank

Sense 1:
financial institution

Sense 2:
the land beside a river
```

Do NOT create:

```text
Sense 1:
to keep something

Sense 2:
to continue keeping something
```

if these are effectively the same learning concept.

---

# 6. Vietnamese Meaning

Vietnamese meanings should be:

- concise
- natural
- useful to a Vietnamese learner
- appropriate to the specific sense

Avoid blindly copying a long dictionary definition.

Prefer:

```text
iron (resource)
→ sắt; khoáng sản sắt
```

over an unnecessarily long translation.

The Vietnamese meaning MUST correspond to the specific sense.

---

# 7. Context Labels

Each sense should have one or more context labels.

Examples:

```text
health
education
work
business
finance
technology
programming
travel
transportation
food
family
relationships
environment
government
law
science
industry
mining
economy
...
```

Context labels should describe the situation in which the sense is commonly used.

Do not create artificial contexts merely to increase the number of tags.

A word may belong to multiple contexts.

Example:

```text
iron (resource)

contexts:
- mining
- industry
- steel production
- economy
- environment
```

---

# 8. Example Sentence Requirements

Generate natural English sentences.

Every example must:

1. clearly represent the intended sense
2. use the correct part of speech
3. sound natural
4. be grammatically correct
5. be understandable for the target learner
6. contain enough context to infer the intended meaning
7. avoid unnecessary complexity
8. avoid ambiguous alternative interpretations where possible

Do not generate sentences that merely demonstrate grammatical possibility.

Prefer realistic language.

Bad:

```text
The iron was iron because iron is iron.
```

Good:

```text
The region has large deposits of iron.
```

---

# 9. Number of Examples

Generate multiple examples for a sense when the sense naturally occurs in different contexts.

Target:

- common/simple sense: 2–3 examples
- sense with several important contexts: 3–5 examples

Do NOT generate five superficial variations of the same sentence.

Examples should provide meaningful variation.

For example:

```text
maintain

Health:
Regular exercise helps maintain good health.

Relationships:
It can be difficult to maintain close relationships over long distances.

Quality:
The company needs to maintain high standards of quality.
```

These demonstrate different real-world usages.

---

# 10. Contextual Active Recall

Each example should be convertible into a fill-in-the-blank exercise.

Example:

Original:

```text
Regular exercise helps maintain good health.
```

Blank:

```text
Regular exercise helps ______ good health.
```

The target word should normally be the blank.

The blank MUST preserve enough context for the intended answer to be recoverable.

Do not remove so much information that the sentence becomes ambiguous.

---

# 11. Accepted Answers

Each exercise must have:

- one primary answer
- zero or more accepted alternative answers

Example:

```json
{
  "answer": "maintain",
  "accepted_answers": []
}
```

Alternative answers must be evaluated against the EXACT sentence and intended sense.

Do NOT accept a word merely because it is a synonym.

For example:

```text
maintain
preserve
retain
keep
```

may all have related meanings, but they are NOT automatically interchangeable.

Only include an alternative answer if it can naturally replace the primary answer in that exact context without materially changing the intended meaning.

---

# 12. Synonym Handling

Synonyms should be associated with a specific sense.

Do NOT create:

```text
maintain:
- preserve
- retain
- keep
```

and assume all three are universally interchangeable.

Instead:

```text
maintain
Sense:
keep something at the same level or condition

Example:
Regular exercise helps maintain good health.

Accepted answers:
[only alternatives that are genuinely valid in this exact sentence]
```

If there is uncertainty, do NOT include the alternative.

False positives are worse than missing a possible synonym.

---

# 13. Active Recall Design

The primary learning objective is retrieval.

The generated content should support these review directions:

### English → Vietnamese

```text
maintain
→ __________
```

Expected:

```text
duy trì
```

### Vietnamese → English

```text
duy trì
→ __________
```

Expected:

```text
maintain
```

### Context → English

```text
Regular exercise helps ______ good health.
```

Expected:

```text
maintain
```

Context → English is especially important because it tests whether the learner can retrieve a word from a real usage situation.

---

# 14. Retrieval Breadth

Some exercises may support multiple valid words.

When appropriate, the dataset may define a synonym/alternative-answer group.

Example:

```text
concept:
maintain / preserve / retain
```

However, do NOT force multiple answers into every exercise.

The purpose of alternative answers is to measure the learner's ability to retrieve related vocabulary, not to make every exercise artificially open-ended.

---

# 15. Retrieval Speed

The application will measure how quickly the user produces the first valid answer.

The content-generation agent does NOT calculate retrieval speed.

It only needs to ensure that:

- the target answer is clear
- accepted answers are explicit
- the exercise is not unnecessarily ambiguous

The application will later record:

```text
retrieval_time_ms
```

---

# 16. Difficulty

Examples should generally match the vocabulary level.

For lower-level vocabulary:

- use common grammar
- use familiar situations
- avoid unnecessarily advanced vocabulary

For B1/B2 vocabulary:

- natural real-world contexts are preferred
- more complex sentence structures are acceptable
- context should resemble language the learner may encounter in IELTS/general English

Do NOT artificially make a sentence difficult just because the target word is advanced.

The difficulty should come primarily from retrieving the target word.

---

# 17. Topic Classification

Assign relevant topics when appropriate.

Topics should describe the semantic or practical domain of the word.

Example:

```text
algorithm

topics:
- technology
- programming
- computer science
```

A word may belong to multiple topics.

Do not assign unrelated topics simply to increase coverage.

---

# 18. Example Selection Priority

When deciding between possible examples, prioritize:

1. Naturalness
2. Correct sense
3. Clear context
4. Practical usefulness
5. Frequency/common usage
6. Learner suitability
7. Topic diversity

Do not prioritize quantity over quality.

---

# 19. Source and Provenance

Every generated item should preserve provenance when possible.

Example:

```json
{
  "source": {
    "word_source": "Oxford 3000",
    "definition_source": "...",
    "example_source": "AI-generated",
    "verified": false
  }
}
```

AI-generated content must be considered unverified until it passes validation.

Do not claim that AI-generated examples are official Oxford examples.

Do not copy proprietary dictionary definitions or examples verbatim.

---

# 20. Validation

Every generated item must be validated before being considered final.

Check:

### Word

- spelling is correct
- word actually exists
- correct part of speech

### Sense

- meaning is correct
- Vietnamese translation matches the sense
- senses are not duplicated

### Context

- context is relevant
- context does not contradict the sense

### Example

- grammatical
- natural
- correct target word usage
- clear meaning
- suitable for blanking

### Accepted answers

- genuinely interchangeable in the exact context
- same intended meaning
- grammatically compatible

---

# 21. Do Not Hallucinate

If information cannot be verified with sufficient confidence:

- mark it for review
- do not invent it
- do not fabricate a dictionary source
- do not fabricate a CEFR level
- do not fabricate a synonym
- do not fabricate a linguistic distinction

Quality is more important than completeness.

---

# 22. Batch Processing

Do NOT attempt to generate thousands of words in one uncontrolled operation.

Process vocabulary in batches.

Recommended initial batch:

```text
50–100 words
```

After generation:

1. validate schema
2. validate content
3. inspect quality
4. identify recurring errors
5. refine the generation rules
6. continue with the next batch

The generation process should be deterministic/reproducible as much as practical.

---

# 23. Example Json version

Use the following conceptual structure:

```json
{
  "word": "iron",
  "pronunciation": "/aɪən/",
  "part_of_speech": ["noun"],
  "cefr": "B1",
  "source": {
    "word_source": "Oxford 3000"
  },
  "senses": [
    {
      "id": "iron-resource",
      "meaning_vi": "sắt; khoáng sản sắt",
      "context_labels": [
        "mining",
        "industry",
        "steel production"
      ],
      "examples": [
        {
          "sentence": "The region has large deposits of iron.",
          "blank_sentence": "The region has large deposits of _____.",
          "answer": "iron",
          "accepted_answers": []
        }
      ]
    }
  ]
}
```

IDs should be stable and deterministic where possible.

---

# 24. Quality Gate

A word is considered ready for import only if:

- all required fields are valid
- senses are correctly separated
- Vietnamese meanings are appropriate
- examples are natural
- blank exercises are unambiguous
- accepted answers have been explicitly validated
- no unsupported claims are present
- source/provenance is recorded where applicable

If an item fails validation:

```text
status = needs_review
```

Do not silently include questionable content.

---

# 25. Important Boundary

This task generates CONTENT.

It must NOT design the application's learning algorithm.

Do not implement:

- SM-2
- FSRS
- scheduling
- mastery calculation
- retrieval scoring
- user progress
- Android code
- SQLite schema
- UI

Those belong to later tasks.

The final output of this task should be a clean, validated vocabulary dataset that another agent can import into the application.

# 26. Success Criteria

The generated dataset should allow the future application to do this entirely offline:

```text
Search word
    ↓
View sense
    ↓
View Vietnamese meaning
    ↓
View contextual examples
    ↓
Start review
    ↓
Recall word
    ↓
Submit answer
    ↓
Check primary/accepted answer
    ↓
Record result
    ↓
SRS schedules next review
```

The content-generation system should therefore optimize for:

> **accurate senses + useful contexts + natural examples + reliable answer validation**

rather than simply maximizing the number of generated sentences or synonyms.

# 27. Actual Output - Data Storage,  SQLite Database

The vocabulary dataset MUST be stored in a SQLite database instead of a single JSON file.

SQLite is the source of truth for vocabulary content.

JSON may still be used for data exchange, backup, testing, or export, but it MUST NOT be the primary persistent format.

## 27.1 Goals

The database must:

* support the full `Word → Sense → Context → Example → Exercise` structure
* avoid duplicated vocabulary data
* support multiple senses per word
* support multiple contexts per sense
* support multiple examples per sense
* support multiple accepted answers per exercise
* preserve source/provenance information
* support efficient lookup by word, sense, context, and topic
* work completely offline
* preserve stable IDs
* allow future migration without modifying the original source data

## 27.2 Recommended Entity Structure

Use normalized relational entities:

```text
words
  │
  └──< senses
          │
          ├──< sense_contexts >── contexts
          │
          └──< examples
                    │
                    └──< accepted_answers
```

Additional metadata such as source/provenance may be associated with the relevant entity.

### `words`

Stores the canonical vocabulary item.

Recommended fields:

```text
id
word
pronunciation
cefr
part_of_speech
word_source
```

### `senses`

Stores individual meanings of a word.

Recommended fields:

```text
id
word_id
meaning_vi
```

A word MUST be able to contain multiple senses.

### `contexts`

Stores reusable context labels.

Recommended fields:

```text
id
name
```

Examples:

```text
travel
education
technology
business
health
finance
```

### `sense_contexts`

Many-to-many relationship between senses and contexts.

```text
sense_id
context_id
```

A sense may belong to multiple contexts.

### `examples`

Stores contextual examples belonging to a specific sense.

Recommended fields:

```text
id
sense_id
sentence
blank_sentence
answer
```

The `answer` normally contains the primary target word.

### `accepted_answers`

Stores additional answers that are explicitly valid for a particular exercise.

```text
id
example_id
answer
```

Only genuinely interchangeable answers may be stored.

### `sources`

If provenance needs to be tracked at a more detailed level, use a separate source entity rather than duplicating source information throughout the dataset.

Recommended fields:

```text
id
source_type
source_name
verified
```

Examples:

```text
Oxford 3000
dictionary
AI-generated
manual review
```

## 27.3 Data Integrity

The database MUST enforce:

* primary keys
* foreign keys
* unique constraints where appropriate
* required fields using `NOT NULL`
* cascading or restricted deletion according to relationship requirements

Foreign-key enforcement MUST be enabled.

Example:

```sql
PRAGMA foreign_keys = ON;
```

The database MUST prevent:

* orphaned senses
* orphaned examples
* orphaned accepted answers
* duplicate context relationships
* duplicate canonical words

## 27.4 Stable IDs

IDs MUST be stable and deterministic where practical.

Do not regenerate IDs unnecessarily when migrating existing data.

A migration should preserve the identity of existing vocabulary items whenever possible.

## 27.5 Indexing

Create indexes for frequently accessed fields.

At minimum:

```text
words.word
senses.word_id
examples.sense_id
sense_contexts.sense_id
sense_contexts.context_id
accepted_answers.example_id
```

The exact indexing strategy may be adjusted after profiling actual queries.

## 27.6 Migration Requirements

The existing JSON dataset MUST NOT be modified directly.

Create a separate migration/import tool:

```text
old_dataset.json
        ↓
migration script
        ↓
vocabulary.sqlite
```

The migration tool MUST:

1. validate the input JSON
2. preserve valid existing data
3. normalize data where required
4. create relational records
5. preserve stable IDs where possible
6. detect duplicates
7. detect missing required fields
8. report invalid records
9. never silently discard data
10. produce a migration report

The original JSON file MUST remain unchanged.

## 27.7 Validation

After migration, validate that:

```text
JSON vocabulary count
≈
Database vocabulary count
```

and verify:

```text
word
→ senses
→ contexts
→ examples
→ accepted answers
```

are all correctly connected.

The migration process MUST be repeatable.

Running the migration multiple times with the same input MUST NOT create duplicate records.

## 27.8 Database as Source of Truth

After successful migration and validation:

```text
SQLite
   ↓
source of truth
```

The application should read vocabulary content from SQLite.

The original JSON should be retained as an immutable source/backup unless explicitly deprecated later.

## 27.9 Scope Boundary

This database migration task is responsible only for:

* schema design
* JSON → SQLite migration
* data validation
* data integrity
* indexing
* import/export tooling

It MUST NOT implement:

* SRS scheduling
* user learning progress
* mastery calculation
* retrieval scoring
* Android UI
* runtime AI
* authentication
* backend services

User learning state should be designed separately from static vocabulary content.
