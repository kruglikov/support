# Architecture of the last project (AI-POWERED PLATFORM) — interview version

Prepared for round 2 of the Digiteum (Symfony + MySQL) process, the technical interview with the client's tech lead. Sources: the CV section "AI-POWERED PLATFORM" in `/home/viktar/Projects/Support/preparations/Digitium - Symfony, MYSQL/00-CV Viktar Kruhlikau [Dev] (15+) - Laravel, Symfony.md:36-61`, the preparation notes in `/home/viktar/Projects/Support/preparations/Digitium - Symfony, MYSQL/06-confluence-hints-Digiteum-Symfony-MySQL.md`, and the question lists in `/home/viktar/Projects/Support/preparations/Digitium - Symfony, MYSQL/04-round-2-questions.md`.

The architecture below is the **as-is** architecture: a modular Symfony monolith with two services extracted out of it. That matches the "Done" note in `/home/viktar/Projects/Support/preparations/Digitium - Symfony, MYSQL/06-confluence-hints-Digiteum-Symfony-MySQL.md` — "Kept modular monlith with some microservices (AI Generation Service)". The full service-per-domain split drafted on that same Confluence page is kept here as the final section, "Where the architecture would go next", so it is told as a plan rather than as a claim about what already runs.

## 1. How to use this document in the interview

- **The 30-second answer** — section 2, "The project in one paragraph".
- **The 2-minute answer** — section 2, plus the diagram in section 4 and the three extraction decisions in section 6.
- **The deep dive** — sections 7 to 13, whichever the interviewer pulls on.
- **The "what would you change" answer** — section 15, and then section 16.

Never open with the technology list. Open with what the platform does for its tenants, then name the two or three forces that shaped the architecture, then draw the picture. A technology list without a driver behind it sounds memorised.

## 2. The project in one paragraph

A multi-tenant SaaS platform that e-commerce companies use to generate, localise and search product content at scale. A tenant connects a product information management system (Plytix PIM) through OAuth, imports a product catalogue, and then runs AI workflows over that catalogue: generating product descriptions and SEO text, translating the generated text into the tenant's locales, building multi-locale newsletters, and searching the whole catalogue lexically and semantically. The platform started as a single Symfony application built by a United States team as an MVP that had already been sold to its first B2B tenants; the team joined as an additional team of five (three backend engineers and two frontend engineers), and my role was lead developer and architect. The goals were to stabilise the platform, to optimise performance and server load, to fix the problems of the legacy code, and to add new features, mainly additional AI providers.

## 3. The forces that shaped the architecture

Name these before drawing anything — every later decision refers back to one of them.

1. **AI calls are slow and unreliable.** A single large-language-model call takes seconds to minutes, fails intermittently, and is rate-limited per provider. Nothing that calls a language model can sit inside an HTTP request.
2. **Work arrives in large batches, not single items.** A tenant does not generate one product description; a tenant generates descriptions for 100,000 products across 5 locales in one action. The unit of work is a run over a catalogue, not a row.
3. **Search is a different workload from CRUD.** Search is read-heavy, latency-sensitive, memory-hungry and needs to scale horizontally on its own; the administrative CRUD of products, users and settings does not.
4. **Every row belongs to a tenant.** Isolation between tenants must hold in the database, in the caches, in the search indexes and in the queues, and a noisy tenant must not starve the others.
5. **The existing code was an MVP under time pressure.** Whatever was designed had to be introduced gradually into a running production system with paying tenants, never as a rewrite.

## 4. The architecture as it runs

```
                React / Next.js admin UI
                          |
                          | HTTPS, REST described by OpenAPI
                          v
            +-------------------------------+
            |   Symfony application (API)   |     modular monolith, PHP 8.2/8.4
            |-------------------------------|
            |  Identity & Tenancy module    |
            |  Catalogue / PIM module       |
            |  Localization module          |
            |  Workflow & Rerun module      |
            |  Newsletter module            |
            |  Media module                 |
            |  Billing & Usage module       |
            +-------------------------------+
               |          |            |
       Doctrine|     AMQP |            | HTTP (internal)
               v          v            v
         +---------+  +--------+   +------------------+
         |  MySQL  |  |RabbitMQ|   |  Search Service  |  standalone, scaled separately
         |  (RDS)  |  +--------+   |  Meilisearch /   |
         +---------+      |        |  Typesense +     |
               ^          |        |  vector index    |
               |          v        +------------------+
         +---------+  +-----------------------+            ^
         |  Redis  |  | AI Generation Service |            | index updates (async)
         +---------+  | (OpenAI, OpenRouter,  |            |
                      |  DeepSeek)            |------------+
                      +-----------------------+
                                 |
                                 v
                          +-------------+
                          | S3 (media,  |
                          | artefacts)  |
                          +-------------+
```

Everything inside the Symfony application box is one deployable unit with one codebase, one composer dependency set and one deployment pipeline. The two boxes outside it — the Search Service and the AI Generation Service — are separately deployable processes with their own scaling, because each one has a different scaling profile from the rest of the application.

## 5. The modules inside the Symfony application

Each module is a bounded context: a top-level namespace with its own entities, its own repositories, its own application services and its own HTTP controllers. A module never reaches into another module's repositories or entities; a module talks to another module through that module's application service interface, or through a domain event on RabbitMQ when the interaction can be asynchronous.

| Module             | Owns | Notable detail |
|--------------------| --- | --- |
| Identity & Tenancy | Users, organisations, roles, tenant configuration, feature flags, locale settings | Owns the Plytix PIM OAuth onboarding flow; issues the session token that carries the tenant identifier |
| Catalogue / PIM    | Products, attributes, categories, variants, per-locale content rows | The largest tables; the place where hand-written SQL replaces Doctrine ORM |
| Localization       | Locales, translation requests, glossaries, per-locale validation rules | Consumes the output of the AI Generation Service |
| Workflow & Rerun   | Workflow runs, run steps, step states, idempotency keys | The orchestrator of every long-running job; described in section 9 |
| Newsletter         | Newsletter templates, content blocks, schedules | Pulls localised content from Catalogue and Localization |
| Media              | Image and document metadata, S3 object keys, derivatives | Stores bytes in S3, metadata in MySQL |
| Billing & Usage    | Plans, quotas, per-tenant counters for tokens, searches and translations | Fed by usage events emitted by the other modules |

Why the modules stayed in one deployable unit rather than becoming services: every one of those modules writes to the same product rows inside one user action, and splitting them would have converted plain database transactions into distributed transactions. The two parts that genuinely have their own scaling profile were extracted, and the rest stayed together. That is the YAGNI judgement the Digiteum request description asks for in `/home/viktar/Projects/Support/preparations/Digitium - Symfony, MYSQL/00-request-description.md`.

## 6. The two extracted services, and the reason each one was extracted

**The Search Service.** Extracted because its resource profile is incompatible with the rest of the application: the search index wants to sit in RAM, the query load peaks independently of the administrative traffic, and the service scales horizontally behind a load balancer while the write side does not. The Search Service owns the Meilisearch/Typesense indexes and the vector index, exposes a query API, and is fed asynchronously by an indexing pipeline that consumes domain events. It never writes to MySQL.

**The AI Generation Service.** Extracted because its failure modes and its dependencies are different from everything else: it holds the provider credentials, it implements the per-provider rate limits, retries and fallbacks, and it is the only component allowed to talk to an external language-model provider. It consumes jobs from RabbitMQ and publishes results back. Behind one internal interface it supports several providers (OpenAI, OpenRouter, DeepSeek); when one provider is unavailable, the service falls back to the next, and a workflow step never learns which provider served it.

**What was deliberately *not* extracted.** Identity, Catalogue, Localization, Newsletter, Media and Billing stayed inside the Symfony application, because those modules share transactions and a single database, and splitting them would buy nothing but network calls and eventual-consistency bugs.

## 7. Data and multi-tenancy

The model is **one database per tenant**, in two tiers. This is the single design decision most worth being able to defend, because it is unusual enough that an interviewer will push on it.

### The two tiers

- **Large tenants get a dedicated RDS instance**, one instance holding that one tenant's database. A large tenant is one whose catalogue, write volume or contractual isolation requirement justifies its own instance — its own CPU and memory, its own buffer pool, its own maintenance window, its own backup and restore schedule, and its own failure domain.
- **Small tenants share one RDS instance that holds many databases**, one database per tenant. In MySQL a schema *is* a database, so "schema per tenant" and "database per tenant" name the same thing: the tenants share hardware and a connection endpoint, but no tenant's tables are visible from another tenant's database.

### The control-plane database

Alongside the tenant databases there is one **control-plane database**, which is the only database that knows about more than one tenant. It holds the tenant registry — for each tenant, the tier, the RDS endpoint, the database name, a reference to the credentials in AWS Secrets Manager (never the credentials themselves), the tenant's status, and the schema version that tenant's database currently has — plus the users and their tenant membership, the plans and quotas, the feature flags, and the platform-wide usage events used for billing and reporting.

Everything tenant-owned — products, attributes, per-locale content, workflow runs and steps, media metadata, newsletters — lives in the tenant's own database and nowhere else.

### How a request reaches the right database

1. A Symfony request listener resolves the tenant once, at the edge, from the authenticated token (or from the host name for a per-tenant subdomain), and puts the resolved tenant into a request-scoped `TenantContext`.
2. A `TenantConnectionResolver` reads that tenant's row from the control-plane database, fetches the credentials from Secrets Manager, and produces the DBAL connection for that tenant's database. Resolved connections are cached per process, and the credentials are cached with a short time to live.
3. Doctrine is configured with two entity managers: the control-plane entity manager, wired to a fixed connection, and the tenant entity manager, wired to the connection the resolver produced. A repository for tenant-owned data can only be constructed with the tenant entity manager.
4. A queue worker resolves the tenant the same way, from the tenant identifier carried in the RabbitMQ message header, before it touches any repository — the worker has no ambient tenant, so a message without that header fails fast rather than reading the wrong database.

### What this model buys

- **Isolation is physical, not conditional.** There is no `tenant_id` predicate to forget, because another tenant's rows are not reachable from the connection at all. A missing `WHERE` clause is a bug inside one tenant, never a data leak across tenants.
- **Per-tenant restore, and per-tenant deletion, are trivial.** Restoring one tenant means restoring that tenant's database, not extracting rows from a shared backup. A GDPR erasure request is `DROP DATABASE` plus the S3 prefix plus the tenant's search index — one operation each, with nothing left behind in a shared table.
- **The noisy-neighbour problem has an answer that does not require code.** A tenant whose batch run saturates an instance is moved to its own instance.
- **Per-tenant tuning and per-tenant scheduling.** A large tenant's instance can be sized, indexed and maintained for that tenant's access pattern, and its migration or reindex can run in its own window.
- **The promotion path is a data move, not a refactor.** A small tenant that outgrows the shared instance is promoted by dumping its database, restoring the dump onto a new dedicated instance, and updating one row in the tenant registry. No application code changes, because the application already reaches every tenant through the resolver.

### What this model costs, and how each cost was handled

- **Every schema change runs N times.** A migration is an orchestrated job, not a single command: it iterates the tenant registry, runs the migration per tenant database, records the new schema version on that tenant's registry row, and is resumable, so a run that fails on tenant 187 continues from tenant 187 rather than starting again. It follows that **every migration must be backward compatible**, because while the run is in progress the same application code is serving tenants whose databases are at two different schema versions — expand first (add the new column, write to both), deploy the code, then contract (drop the old column) in a later migration.
- **Schema drift is the failure mode to guard against.** The schema version on the registry row is the guard: a tenant whose version is behind is not routed to code that requires the newer schema, and a nightly check compares every tenant's actual schema against the expected version and alerts on any difference.
- **Connection count is the operational limit.** With many PHP-FPM workers and many queue workers, connections multiply by active tenants. That is handled by keeping resolved connections short-lived and closed at the end of the request or message, by giving the queue workers tenant affinity so one worker pool handles a bounded set of tenants rather than all of them, and by watching the connection count per instance as a first-class alert.
- **Cross-tenant questions cannot be answered by a join.** "How much did every tenant spend on AI tokens this month" has no single database to query. That is why usage events are published to RabbitMQ and aggregated into the control-plane database: the reporting read model is built from events, not from a query that spans tenant databases.
- **Onboarding is provisioning, not an `INSERT`.** Creating a tenant means creating the database, running every migration against it, seeding the reference data, storing the credentials in Secrets Manager and writing the registry row — an automated, idempotent provisioning job, because doing it by hand is how tenants end up with subtly different schemas.

### The rest of the storage layer, and where tenancy shows up in it

- **Per-locale content is a separate table, not a JSON column** — `product_content(product_id, locale, field, value)` inside the tenant's own database — because the per-locale rows are what the platform reads, writes, versions and indexes, and a JSON blob cannot be indexed or partially updated.
- **Doctrine ORM is used for the write side, where the unit of work and the entity graph earn their cost.** The read side that feeds lists, exports and the indexing pipeline uses hand-written SQL through the DBAL, because hydrating 100,000 entities to read four columns from each one is how a platform runs out of memory.
- **Where hand-written SQL replaced the ORM:** the catalogue export query, the indexing pipeline's batched reader (keyset pagination on `(updated_at, id)`, never `OFFSET`), and the usage-aggregation queries that feed the control-plane database.
- **S3 holds the bytes** — original images, generated assets, exports — under a per-tenant key prefix, and the tenant's database holds only the object keys and the metadata.
- **Redis keys are prefixed with the tenant identifier**, so a cache entry cannot be served to the wrong tenant even though the Redis instance is shared.

## 8. Synchronous and asynchronous communication

- **Synchronous, REST over HTTPS, described by OpenAPI:** everything the user waits for — reading a product, saving a setting, listing runs, querying search. The OpenAPI specification is generated from the code and from attributes on the controllers, so a specification that disagrees with the code fails the build rather than misleading the frontend team.
- **Asynchronous, RabbitMQ through Symfony Messenger:** everything the user does not wait for — AI generation, translation, indexing, newsletter assembly, exports, usage aggregation.
- **The rule for the boundary:** if an operation can exceed a couple of seconds, the HTTP endpoint accepts the work and returns `202 Accepted` with the identifier of a run, and the client polls the run's status endpoint (or receives a WebSocket notification) for the result. That is exactly the pattern the interviewer probed in question 8 of interview 2 in `/home/viktar/Projects/Support/preparations/Digitium - Symfony, MYSQL/04-round-2-questions.md`.

**The RabbitMQ topology.** A topic exchange per domain (`catalogue`, `ai`, `search`, `newsletter`), routing keys shaped as `<entity>.<event>` (`product.created`, `ai.generation.finished`, `content.updated`, `translation.completed`, `media.uploaded`). Each consumer group binds its own durable queue to the exchange, so adding the indexing consumer did not require any change to the publisher. Every queue has a dead-letter exchange and a parking queue; a message that fails its retry budget lands in the parking queue with the failure reason, and never blocks the queue behind it.

**Why events rather than direct calls between the Symfony application and the services:** the publisher does not need to know who consumes. When the vector indexing was added, the Search Service bound a second queue to the existing `content.updated` routing key and no publisher changed.

## 9. The workflow and rerun engine — the part worth describing in detail

This is the piece to volunteer when the interviewer asks what was architecturally interesting, because it answers idempotency, retries, partial failure and resumability in one story.

A **run** is one user action over a set of products — "generate and localise descriptions for these 40,000 products in these 5 locales". A run is stored in MySQL as a row in `workflow_run`, and every unit of work inside a run is a row in `workflow_run_step` with its own state (`pending`, `running`, `succeeded`, `failed`, `skipped`), its attempt count, its error and its idempotency key.

1. The HTTP request creates the run and its steps in one transaction, then returns the run identifier. Nothing else happens inside the request.
2. A dispatcher publishes one message per step to RabbitMQ, in batches, so a run of 200,000 steps does not build one enormous message.
3. Each consumer takes a step, checks the step's state (a step already `succeeded` is acknowledged and dropped — that is the idempotency guard), calls the AI Generation Service or the Localization module, and writes the result plus the new state in one transaction.
4. A failure increments the attempt count and is retried with exponential backoff; when the attempt budget is exhausted, the step becomes `failed` and the message goes to the dead-letter queue. The rest of the run keeps going.
5. **The rerun engine** is then the answer to "what do I do with a run where 300 of 40,000 steps failed": a rerun re-dispatches only the steps in the `failed` state, and because the successful steps carry their idempotency keys, no work is repeated and no output is duplicated. A rerun can also start from a chosen step when the tenant changed a prompt and wants the later stages redone.
6. Because state lives in MySQL and not in the worker's memory, a worker that is killed mid-run loses at most the one step it held, and the run resumes when workers come back. The same property answers the "suspend and resume processing" question from interview 1.

Redis holds only the hot, disposable part of this: per-tenant concurrency locks (so one tenant cannot occupy every worker), rate-limit counters per provider, and short-lived idempotency markers. Redis is never the record of what happened.

## 10. Search: a read model, not a second source of truth

The search side is a CQRS read model. MySQL is the write model; Meilisearch/Typesense plus the vector index form the read model; the two are reconciled asynchronously.

- The indexing pipeline consumes `content.updated`, `product.created`, `translation.completed` and `media.uploaded` from RabbitMQ, reads the affected rows in batches with hand-written SQL, and writes documents into the index.
- Lexical search runs against Meilisearch/Typesense; semantic and multimodal search runs against embeddings produced by the AI Generation Service and stored in the vector index.
- Indexes are tenant-aware: either one index per large tenant, or a shared index with a mandatory tenant filter for the long tail of small tenants.
- Redis caches the hot queries, keyed by tenant plus the normalised query, with a short time to live; an index update invalidates the affected keys by tag.
- The honest trade-off to state out loud: search results are eventually consistent, usually within seconds. For a catalogue search that is acceptable; anything that must be immediately consistent (a permission check, a billing quota) is read from MySQL, never from the index.

## 11. Caching

Three layers, each with an explicit invalidation story, because a cache without an invalidation story is a bug with good performance.

1. **Doctrine's second-level cache and query result cache in Redis** for the reference data that is read constantly and written rarely — tenant configuration, locales, attribute definitions, feature flags.
2. **An application cache in Redis** for computed read models: the product list projections, the dashboard counters, the search result sets. Keyed by tenant, tagged by entity, invalidated by the same domain events that drive indexing.
3. **HTTP caching** with `ETag` and `Cache-Control` on the read endpoints the frontend polls, so a poll that changes nothing costs a `304 Not Modified`.

## 12. Infrastructure and deployment

- Containers built with Docker, run on AWS EC2 instances; Podman and LXC on the development machines. Images are layered so that the base image, the system packages and `composer.json` plus `composer.lock` come before the application source, and a code change rebuilds only the last layer — the reasoning written out in the closing section of `/home/viktar/Projects/Support/preparations/Digitium - Symfony, MYSQL/06-confluence-hints-Digiteum-Symfony-MySQL.md`.
- Separate deployable units, each scaled on its own: the web/API processes, the queue worker processes (several pools, one per queue class, so a slow AI queue cannot starve the indexing queue), the Search Service, and the AI Generation Service.
- MySQL on RDS with a read replica for the reporting and export queries; S3 for media and artefacts; CloudWatch for logs and metrics; Grafana for the dashboards.
- Structured logging in JSON with a correlation identifier that is created at the API edge and carried through the RabbitMQ message headers into every worker, so one user action can be followed across the Symfony application, the AI Generation Service and the Search Service.
- Alerts on the things that actually signal damage: queue depth and consumer lag per queue, dead-letter queue arrival rate, AI provider error and fallback rate, p95 search latency, MySQL slow-query count, worker restart rate.

## 13. The quality gates that hold the modernisation together

This is the part the Digiteum request description in `/home/viktar/Projects/Support/preparations/Digitium - Symfony, MYSQL/00-request-description.md` cares about most, so it deserves its own beat in the conversation.

- **Test first for every bug fix.** The failing test that reproduces the bug is written before the fix, which is the only way to know the fix works and that the bug stays fixed.
- **PHPStan at level max with no suppressions**, including custom rules written when a class of bug came back more than once — for example a rule that forbids a repository method that builds a query without the tenant predicate.
- **Rector and PHP CS Fixer** to modernise the MVP code mechanically and reviewably, in small pull requests, never as a rewrite.
- **The strangler approach to the legacy parts:** put the old behaviour under characterisation tests first, extract the behaviour behind an interface, re-implement it, switch the call sites behind a feature flag, then delete the old code.

## 14. Numbers to have ready

From the estimates already worked out in `/home/viktar/Projects/Support/preparations/Digitium - Symfony, MYSQL/06-confluence-hints-Digiteum-Symfony-MySQL.md`, and worth quoting because they show the scale was reasoned about rather than guessed:

| Layer                                    | Size          |
|------------------------------------------|---------------|
| MySQL (content, tenants, workflow state) | 100 GB – 2 TB |
| Search index                             | 200 GB – 2 TB |
| Vector index                             | 50 GB – 2 TB  |
| S3 media                                 | 1 TB – 50 TB  |
| Logs and metrics                         | 100 GB – 1 TB |
| Redis and RabbitMQ                       | 1–50 GB       |

The framing to use: this is not "big data" by global standards, but it is data-heavy for a multi-tenant SaaS, and the hard part was never the total number of bytes — the hard part was concurrency, index freshness, vector processing and tenant isolation.

## 15. Decisions and trade-offs, stated as trade-offs

An interviewer trusts an architecture more when its author names what the architecture costs.

| Decision | What it bought | What it cost |
| --- | --- | --- |
| Modular monolith instead of a service per domain | Plain database transactions, one deployment, a small team could move fast | Module boundaries hold only by discipline and architecture tests, not by the network |
| Extracting only the Search Service and the AI Generation Service | Independent scaling exactly where the profile differed | Two more deployables to operate and monitor |
| CQRS between MySQL and the search index | Search scales and stays fast under load | Eventual consistency; a bug in the indexing pipeline shows as "the data is wrong" to the user |
| Bypassing Doctrine ORM on the read paths | Batch reads stopped exhausting memory | Two ways of reading data in one codebase, so the rule for which to use has to be written down |
| Provider abstraction with fallback in the AI Generation Service | Survives one provider being down or rate-limited | The abstraction is the lowest common denominator of the providers; provider-specific features need an escape hatch |
| Storing workflow state in MySQL rather than in the worker | Suspend, resume, rerun and partial failure all work | Every step costs writes to the database, so steps are batched and state transitions are kept small |

## 16. Likely follow-up questions, and the short answer for each

Drawn from the topics the same interviewer asked in both round 2 recordings, listed in `/home/viktar/Projects/Support/preparations/Digitium - Symfony, MYSQL/04-round-2-questions.md`.

1. **"How do the parts of the distributed system communicate?"** — Synchronous REST described by OpenAPI where the user waits; RabbitMQ domain events where the user does not. Topic exchanges per domain, a durable queue per consumer group, dead-letter queues for the failures.
2. **"An operation takes minutes — how do you keep the API RESTful?"** — The endpoint creates a run and returns `202 Accepted` with the run's identifier and a status URL; the work goes onto a queue; the client polls the status resource or is notified over a WebSocket; the finished artefact is fetched from its own resource URL.
3. **"How do you scale WebSocket notifications across several servers?"** — Each server holds its own connections and binds its own non-durable queue to a fanout exchange, so a notification published once reaches every server and therefore every connected user. The queues are non-durable on purpose: when a server dies its connections die with it, so a message kept for the restart would be useless.
4. **"A query is slow — what do you do?"** — Measure first: find the query in the slow-query log, run `EXPLAIN` (and `EXPLAIN ANALYZE`) to read the access type, the chosen index and the rows examined against the rows returned. Then fix the cause: a composite index in the right column order, rewriting the query so the predicate stays sargable, replacing `OFFSET` pagination with keyset pagination, removing the N+1 by fetch-joining or by batching, and denormalising a counter only when the read pattern genuinely needs it.
5. **"Is it good to have many indexes?"** — No. Every index costs storage, slows every write on that table because the index must be maintained, consumes buffer-pool memory and gives the optimiser more plans to get wrong. Indexes are added against measured queries and removed when nothing uses them.
6. **"Why denormalise?"** — For a read pattern that would otherwise join across large tables on every request: per-tenant counters for quotas, a denormalised product list projection for the grid. The cost is that the duplicate has to be kept correct, which is why each denormalised value is written by the same event that changes the source.
7. **"What is an exchange in RabbitMQ, and which types exist?"** — An exchange is the routing component a publisher publishes to; queues bind to the exchange with a binding key, and the exchange type decides how a message's routing key is matched: direct (exact match), topic (pattern with `*` and `#`), fanout (every bound queue), headers (matching on header values).
8. **"How do you secure the endpoints?"** — Authentication with a signed token carrying the tenant and the roles, authorisation with Symfony voters on the resource, plus the tenant predicate enforced in the data layer so an authorisation mistake still cannot cross tenants. The webhook endpoints from the PIM provider are public, so they are verified by an HMAC-SHA256 signature over the raw body with a shared secret, with a timestamp check against replay.
9. **"What did you monitor?"** — Queue depth and consumer lag per queue, dead-letter arrivals, AI provider error and fallback rates, p95 search latency, MySQL slow-query counts, memory and restart rates per worker pool, all in CloudWatch with Grafana dashboards, and alerts only on the signals that need a human.

## 17. Where the architecture would go next

This is the section drafted on the Confluence page. Present it as the direction, not as what runs today: if the tenant count and the catalogue sizes kept growing, the modular monolith splits along the module boundaries that already exist — Identity & Tenant, Content/PIM, Localization, Workflow & Rerun, Newsletter, Media, Billing/Usage — behind an API gateway or backend-for-frontend, each service owning its own schema, with the same RabbitMQ event bus already in place carrying the integration events. The value of having kept strict module boundaries inside the monolith is exactly that this split becomes a deployment change rather than a rewrite. The step that would come first is the Content/PIM service, because that module is the one whose write load grows with every new tenant.
