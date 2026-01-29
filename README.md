## Implementation Overview

This project was implemented incrementally with a focus on correctness, clarity, and maintainability.

1. Initialized the project using Poetry and set up version control with Git.
2. Created a FastAPI application and introduced API versioning under `/api/v2`.
3. Configured SQLAlchemy for database access using environment-based configuration.
4. Modeled datasets using fully qualified names (FQN) as primary identifiers.
5. Added support for column-level metadata associated with each dataset.
6. Implemented dataset-to-dataset lineage using a directed graph model.
7. Added cycle detection logic using depth-first search to prevent invalid lineage relationships.
8. Implemented dataset creation and lineage creation through a clean CRUD layer.
9. Built a search endpoint with priority-based matching:
   - table name
   - column name
   - schema name
   - database name
10. Ensured search results are deduplicated and sorted by match priority.
11. Added Alembic for schema migrations and documented migration commands.
12. Added Docker and Docker Compose configuration and documented how to run the service.
13. Completed documentation with setup instructions, assumptions, and design notes.
