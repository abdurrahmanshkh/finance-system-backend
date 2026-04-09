# AGENTS.md

## Project context

This repository is for a Python developer internship coding assessment at Zorvyn.

The goal is to demonstrate:
- clean Python backend design
- correct business logic
- strong validation
- maintainable structure
- good API design
- reliable data handling
- readable documentation
- thoughtful but not bloated engineering

This is an assessment project, not a production system. Prefer clarity, correctness, and simplicity over unnecessary complexity.

---

## Primary goals

Build a Python-based finance system backend that can:
- create, view, update, delete financial records
- filter records by date, category, and transaction type
- generate useful summaries and analytics
- handle basic user roles
- validate inputs properly
- return clear errors
- persist data in a sensible database
- include strong documentation
- look polished if any UI or API docs are added

---

## Preferred implementation philosophy

1. Keep the scope focused.
2. Build the smallest correct version first.
3. Make the code easy to understand for reviewers.
4. Use clear separation of concerns.
5. Avoid overengineering.
6. Prefer explicit business rules over hidden magic.
7. Use sensible defaults and document assumptions.
8. Every feature should be testable.

---

## Recommended stack

Use the most practical stack for a clean internship submission:
- Python
- FastAPI preferred unless another choice is clearly better for the current codebase
- Pydantic for validation
- SQLAlchemy or a similarly clean ORM layer
- SQLite for simple local development unless the repository already uses something else
- Alembic if migrations are needed
- pytest for testing

If the existing repository already uses a different reasonable stack, continue with the existing stack unless there is a strong reason to change.

---

## Architecture rules

Keep the code organized by responsibility, not by dumping everything into one file.

Suggested layers:
- API/router layer
- schema/validation layer
- service/business-logic layer
- repository/data-access layer
- model/database layer
- utility/helper layer
- tests

Business logic should not live directly inside route handlers unless it is trivial.

Database access should not be scattered across the project.

Validation should be handled as early as possible.

---

## Data model guidance

The project should likely include concepts such as:
- User
- Role
- FinancialRecord / Transaction
- Category
- Summary or analytics response objects
- Optional audit or activity log if a standout feature is added

Use reasonable field names and avoid unnecessary fields.

A financial record should generally include:
- amount
- type: income or expense
- category
- date
- description or notes
- owner/user reference if needed
- timestamps

Do not add complex model relationships unless they clearly improve the solution.

---

## Role handling rules

Use simple, understandable role behavior.

Expected roles:
- Viewer: read-only access to records and summaries
- Analyst: read access plus filters and deeper analytics
- Admin: create, update, delete, and manage records

Keep the role system easy to explain in the README.

If authentication is included, keep it simple and appropriate for an assessment. Do not introduce unnecessary production-grade auth complexity unless it meaningfully improves the project.

---

## Validation rules

All incoming data must be validated carefully.

Validate:
- amount
- date format
- transaction type
- required fields
- role restrictions
- filter parameters
- update payloads
- invalid IDs
- empty or malformed inputs

Validation should produce clear, user-friendly error messages.

---

## Error-handling rules

Return predictable and useful errors.

Prefer:
- clear HTTP status codes
- helpful error messages
- safe failure behavior
- no stack traces in normal API responses
- no silent failures

Handle at least:
- invalid input
- not found
- unauthorized / forbidden access
- duplicate or conflicting data if applicable
- unsupported filter values
- unexpected server errors

Do not swallow errors silently.

---

## Summary and analytics rules

The backend should provide useful finance summaries such as:
- total income
- total expenses
- balance
- category-wise breakdown
- monthly totals
- recent activity

Summaries should be deterministic and easy to explain.

If a standout analytics feature is added, keep it useful and not flashy for its own sake.

---

## Standout feature policy

It is acceptable to add only a few unique features if they genuinely improve the project.

Good examples:
- recurring transaction detection
- financial health indicator
- anomaly or outlier detection
- smart category suggestions
- CSV import/export
- audit trail
- trend summaries

Rules:
- choose only high-value additions
- avoid feature creep
- do not add gimmicks
- every standout feature must be documented and tested
- never make the core CRUD and summary flows harder to understand

---

## Testing rules

Write tests for the most important behavior.

Prioritize:
- record creation
- record update
- record deletion
- filters
- summaries
- role checks
- validation failures
- edge cases

Tests should be easy to run and clearly organized.

When changing behavior, update or add tests.

---

## Documentation rules

Documentation matters heavily for this project.

Required documentation should include:
- what the project does
- tech stack
- setup instructions
- how to run the app
- how to run tests
- API usage examples
- explanation of roles
- explanation of assumptions
- description of standout features
- notes about any simplifications

If the project exposes API docs automatically, make sure they are easy to use.

Document any non-obvious logic inline with concise comments and docstrings.

Avoid cluttered or excessive comments. Comment only where the reasoning matters.

---

## Code style rules

- Use clear and descriptive names
- Keep functions small and focused
- Avoid deeply nested logic
- Prefer early returns where useful
- Avoid duplicated logic
- Keep modules cohesive
- Add type hints where practical
- Use docstrings for public functions/classes where helpful
- Keep formatting consistent
- Do not leave dead code, commented-out code, or temporary debug prints

---

## Workflow rules

Work in small milestones.

For each milestone:
1. describe the goal first
2. identify affected files
3. implement the smallest useful change
4. run relevant checks
5. fix issues before moving on
6. summarize what changed

Do not jump ahead to later milestones unless the current step is complete.

If the task is unclear, state the assumption before proceeding.

If a planned change affects multiple areas, keep it tightly scoped.

---

## File-change rules

- Do not modify unrelated files.
- Do not rename or move files unless necessary and justified.
- Do not introduce new dependencies without a clear reason.
- Do not change project structure wildly unless the current structure is broken.
- Keep the diff easy to review.

---

## API design rules

If building an API:
- use consistent endpoint patterns
- use clear request and response schemas
- keep status codes consistent
- make filtering predictable
- include pagination if the record list can grow large
- keep response payloads clean and review-friendly

If a frontend/admin page exists:
- keep it clean, modern, responsive, and simple
- do not let UI work distract from backend correctness
- prioritize usability over decoration

---

## Data persistence rules

Use a storage approach that is easy to run locally and easy to explain in the submission.

SQLite is acceptable if it keeps the project simple and reliable.

Make sure:
- schema is sensible
- migrations are handled if needed
- seed data is deterministic
- database initialization is documented

---

## Security and privacy rules

Even for an assessment project:
- do not hardcode secrets
- do not log sensitive information
- do not expose internals unnecessarily
- validate inputs before processing
- keep authorization checks explicit

---

## Completion standard

A task is complete only when:
- the implementation works as intended
- tests pass or known failures are documented
- the code is readable and maintainable
- documentation is updated if needed
- the result is consistent with the assignment scope

---

## Final output expectations

At the end of each milestone or major task, provide:
- what changed
- why it changed
- any assumptions made
- any remaining risks
- the next logical step

Keep summaries concise and practical.

---