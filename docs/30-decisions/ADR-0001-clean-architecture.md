# ADR-0001: Adopt Full Stack Clean Architecture with FastAPI, Vue 3, and PostgreSQL

Status: Approved
Date: 2026-10-15
Author: Aitor Nain Mendoza Vallejo (naindev)

## Context

New full-stack services and portfolio applications require a robust, production-grade architectural baseline with zero ongoing cloud hosting costs (0.00 €), rapid local bootstrapping, and strict domain boundary protection.

## Decision

1. **Backend**:
   - Monolithic modular Clean Architecture using Python 3.12, FastAPI, and Pydantic v2.
   - Persistence through asynchronous SQLAlchemy 2.0 with PostgreSQL as the production target and `sqlite+aiosqlite` for zero-setup local unit/integration testing.
   - Strict separation: Domain entities and invariants do not depend on SQLAlchemy ORM or FastAPI routers.

2. **Frontend**:
   - Single Page Application built with Vue 3 Composition API, TypeScript (strict mode), and Vite.
   - Encapsulated UI components with `<nain-ecosystem-bar>` pre-integrated for instant cross-ecosystem navigation.

3. **Infrastructure**:
   - Local multi-container orchestration via Docker Compose.
   - CI/CD governance delegating to central reusable workflows in `Nain9Dev/.github`.

## Consequences

- Invariants and validation are enforced at the domain boundary, preventing illegal state from reaching database tables.
- Zero license or infrastructure expense: all components run locally in Docker or deploy to standard free tiers (Cloudflare Pages, Render, Neon).
