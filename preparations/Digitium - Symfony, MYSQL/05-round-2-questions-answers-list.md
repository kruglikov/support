# Digiteum round 2 — questions

## Questions asked in both interviews

The same interviewer asked these topics in both interviews, so they are the most likely to come up again.

1. Tell me about a challenging task from your experience that, once you finished it, made you feel you could do anything.

2. Why is a Docker image built in layers, and why does the order of the instructions in a Dockerfile matter?
   - Every instruction that changes the filesystem (`RUN`, `COPY`, `ADD`) creates a new read-only layer; the other instructions (`ENV`, `CMD`, `EXPOSE`, …) only change the image metadata.
   - Layers are content-addressed (identified by a hash of their content), so identical layers are stored once and shared between images on the host and in the registry.
   - Build cache: Docker reuses a cached layer when the instruction is unchanged, its inputs are unchanged (for `COPY` / `ADD`, a checksum of the copied files), and every layer before it also came from the cache.
   - The key rule: once one layer changes, every layer after it is rebuilt. That is why the order matters.
   - So order the instructions from least to most frequently changed: base image → OS packages → dependency manifest → dependency install → application source code last.
   - Result in the normal case: a code change rebuilds only the last `COPY` layer, the build takes seconds, and a deploy pulls only that small changed layer, because `docker pull` / `docker push` transfer only the layers the other side is missing.
   - Copy the dependency manifest separately before the source code, so dependencies are re-installed only when the manifest changes (`requirements.txt` / `uv.lock` in Python, `composer.json` + `composer.lock` in PHP).
   - Combine related commands into one `RUN` and clean up in the same `RUN` (`apt-get update && apt-get install -y … && rm -rf /var/lib/apt/lists/*`), because a file deleted in a later layer still takes up space in the earlier layer.
   - Use a `.dockerignore` (`.git`, `vendor/`, `node_modules/`, `.env`, logs), so the build context stays small, unrelated files do not invalidate the cache, and secrets never land in a layer.
   - Never put secrets into a layer, not even if a later instruction deletes them: layers can be extracted from the image. Use BuildKit secret mounts (`RUN --mount=type=secret,…`) instead.
   - Faster installs with BuildKit cache mounts, for example `RUN --mount=type=cache,target=/root/.composer/cache composer install`.
   - Example of the right order for a PHP application:

     ```dockerfile
     FROM php:8.4-fpm
     RUN apt-get update && apt-get install -y --no-install-recommends libzip-dev \
         && docker-php-ext-install pdo_mysql zip \
         && rm -rf /var/lib/apt/lists/*
     COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
     WORKDIR /app
     COPY composer.json composer.lock ./
     RUN composer install --no-dev --no-scripts --no-autoloader
     COPY . .
     RUN composer dump-autoload --optimize --classmap-authoritative
     ```

3. What is a multi-stage Docker build and why is it useful? 
   - **Multi-stage build:** one Dockerfile with several `FROM` stages. The build stages contain compilers, dev dependencies and build tools; the final stage starts from a small runtime image and copies in only the built artifacts with `COPY --from=<stage>`.
   - Benefits of multi-stage: a much smaller final image, a smaller attack surface (no compilers, package managers or dev tools in production), faster pulls and deploys, and no build secrets left in the final image.
   - One Dockerfile can serve several purposes through targets: `docker build --target dev` for local development and `--target prod` for production.
   - BuildKit builds independent stages in parallel, for example the Composer stage and the Node.js asset stage at the same time.
   - Example for PHP: a `composer` stage runs `composer install --no-dev`, a `node` stage builds the frontend assets, and the final `php-fpm` stage copies only `vendor/` and `public/build/`:

     ```dockerfile
     FROM composer:2 AS vendor
     WORKDIR /app
     COPY composer.json composer.lock ./
     RUN composer install --no-dev --no-scripts --prefer-dist

     FROM node:22-alpine AS assets
     WORKDIR /app
     COPY package.json package-lock.json ./
     RUN npm ci
     COPY assets/ assets/
     RUN npm run build

     FROM php:8.4-fpm-alpine AS prod
     WORKDIR /app
     COPY --from=vendor /app/vendor/ vendor/
     COPY --from=assets /app/public/build/ public/build/
     COPY . .
     USER www-data
     ```
What is a multi-architecture image, and how do you build one in a CI/CD pipeline?
   - **Multi-architecture image:** one tag (for example `app:1.4`) that works on several CPU architectures, typically `linux/amd64` (Intel/AMD servers) and `linux/arm64` (Apple Silicon laptops, AWS Graviton instances).
   - How a multi-arch image works: the tag points to an image index (also called a manifest list), which lists one image per platform, and `docker pull` fetches the image that matches the host's architecture.
   - Build command: `docker buildx build --platform linux/amd64,linux/arm64 -t registry/app:1.4 --push .`. The result is pushed straight to a registry, because the classic local image store cannot hold a multi-platform image.
   - Non-native architectures are built through QEMU emulation (simple but slow), on native builder nodes for each architecture (fast), or by cross-compiling.
   - The Dockerfile changes this needs: every base image must itself be multi-arch, and any binary downloaded during the build must be selected by the `TARGETARCH` / `TARGETOS` build arguments instead of a hard-coded `amd64` URL. For cross-compilation, run the build stage on `FROM --platform=$BUILDPLATFORM`.
   - In CI (GitHub Actions): `docker/setup-qemu-action`, `docker/setup-buildx-action`, then `docker/build-push-action` with `platforms: linux/amd64,linux/arm64` and a registry or GitHub Actions cache (`cache-from` / `cache-to`).
   - Verify the result with `docker buildx imagetools inspect registry/app:1.4`, which lists the platforms in the index.
4. Two containers run on the same Docker host, and one cannot reach the other. Why can that happen, and how do you fix it?
   - The main cause: the containers are on different Docker networks. Containers can talk to each other only when they share a network.
   - Fix: attach both containers to one user-defined network (`docker network create shared`, then `docker network connect shared <container>`), or in Docker Compose declare the same network in both projects (`networks: shared: external: true`).
   - Docker Compose creates a separate default network per project, so two Compose projects (two separate `docker-compose.yml` files) cannot reach each other until they share a network.
   - Name resolution: on a user-defined network, Docker's built-in DNS resolves container names and Compose service names (`mysql`, `rabbitmq`). On the default `bridge` network there is no such DNS, so the containers can reach each other only by IP address.
   - Publishing ports is not needed between containers. `EXPOSE` is only documentation, and `-p` / `ports:` publishes a port to the host for outside access. Container-to-container traffic uses the container's own port, not the published host port.
   - Other common causes worth naming:
     - using `localhost` inside a container, which points to that container itself, not to the other container;
     - the application listening on `127.0.0.1` instead of `0.0.0.0`, so the application is unreachable from outside its own container;
     - connecting to the published host port instead of the container port;
     - the dependency not being ready yet: `depends_on` only orders the start, so use `condition: service_healthy` with a `healthcheck`;
     - inter-container communication disabled on the daemon (`--icc=false`), or a firewall rule.
   - Debugging steps: `docker network inspect <network>` to see which containers are attached, then `docker exec -it <container> sh` and try `getent hosts <name>` or `nc -zv <name> <port>` from inside.
5. A SQL query is slow. How do you find the cause and optimize the query?
   - Measure first, do not guess. Find the slow queries with the MySQL slow query log (`slow_query_log`, `long_query_time`), `performance_schema` / the `sys` schema views, or an APM tool. In PostgreSQL, use `pg_stat_statements`.
   - Read the execution plan with `EXPLAIN` and `EXPLAIN ANALYZE` (MySQL 8.0.18+). Look for `type: ALL` (a full table scan), `key: NULL` (no index used), a large `rows` estimate, and `Extra: Using filesort` / `Using temporary`. In PostgreSQL, use `EXPLAIN (ANALYZE, BUFFERS)`.
   - Index the columns used in `WHERE`, `JOIN` and `ORDER BY`. In a composite index, apply the leftmost-prefix rule: equality columns first, then the range column. A covering index (`Extra: Using index`) answers the query from the index alone, without reading the table rows.
   - Rewrite the patterns that stop MySQL from using an index:
     - a function on an indexed column: `WHERE DATE(created_at) = '2026-09-22'` becomes a range, `created_at >= '2026-09-22' AND created_at < '2026-09-23'`;
     - a leading wildcard: `LIKE '%term'`;
     - implicit type conversion, for example comparing a `VARCHAR` column with a number;
     - an `OR` across different columns.
   - Load less data: select only the needed columns instead of `SELECT *`, and filter and aggregate in SQL instead of in PHP.
   - Paginate with keyset pagination (`WHERE id > :lastId ORDER BY id LIMIT 100`) instead of a large `OFFSET`, which reads and discards every skipped row.
   - Fix ORM problems. N+1 queries in Doctrine: use a fetch join in DQL (`JOIN … SELECT` the related entity) or batch loading. Large result sets: iterate with `toIterable()` and call `EntityManager::clear()` per batch. Where the ORM produces a bad query, write hand-written SQL through the DBAL.
   - Keep the optimizer statistics fresh (`ANALYZE TABLE`), and do not over-index: every index slows down `INSERT` / `UPDATE` / `DELETE` and costs disk and memory, and a low-selectivity index is often ignored anyway.
   - When the query is heavy by nature: summary tables, denormalized columns, caching in Redis, partitioning a very large table, or running reads on a read replica.
   - Verify the fix: run `EXPLAIN` again and measure the query time before and after, on production-sized data, not on a nearly empty dev database.
6. Why do we write unit tests, what is a mock object, and what do we usually mock?
   - Why unit tests: they catch regressions early, make refactoring safe, give feedback on design (a class that is hard to test is usually too coupled), document the expected behaviour, and run fast in CI on every push.
   - A unit test checks one class or function in isolation, is fast, and does no real I/O (no database, network or filesystem). Integration tests check the real database or HTTP; functional / end-to-end tests check a whole flow. The test pyramid: many unit tests, fewer integration tests, few end-to-end tests.
   - Structure each test as Arrange – Act – Assert, test one behaviour per test, and use data providers (PHPUnit `#[DataProvider]`, pytest `@pytest.mark.parametrize`) for several input cases.
   - Test doubles and how they differ:
     - **dummy:** passed in only to fill a parameter, never used;
     - **stub:** returns prepared answers;
     - **spy:** records the calls it receives, for checking afterwards;
     - **mock:** is set up with expectations about the calls it must receive, and fails the test when those expectations are not met;
     - **fake:** a working but simplified implementation, such as an in-memory repository.
   - What to mock: dependencies at the boundaries that are slow, non-deterministic or external. Examples: HTTP clients and third-party APIs (payment gateway, CRM), the mailer, the message bus, the clock (current time), random / UUID generators, the filesystem.
   - What not to mock: the class under test itself, value objects, simple entities, and anything cheap and deterministic. Too many mocks couple the tests to the implementation, so every refactoring breaks them.
   - "Don't mock what you don't own": wrap a third-party SDK in your own interface, mock that interface in unit tests, and cover the real SDK with a few integration tests.
   - Tools: PHPUnit `createMock()` / `createStub()`, Mockery or Prophecy in PHP; `unittest.mock` (`Mock`, `MagicMock`, `patch`) and `pytest-mock` in Python. Note that `patch` must target the name where it is looked up, not where it is defined.
   - A coverage threshold in CI (for example 80%) is a useful gate, but coverage does not prove the assertions are good. Mutation testing (Infection in PHP, mutmut in Python) checks the quality of the tests themselves.
   - Mention TDD from the CV: red – green – refactor, and a failing test written first for every bug fix, so the same bug cannot come back.
7. How do you monitor an application or a data pipeline, and how do you set up alerts that are actually useful?
   - Name the three pillars of observability: **logs** (what happened), **metrics** (how much / how fast, over time), **traces** (the path of one request through several services).
   - Logs:
     - write structured JSON logs (Monolog `JsonFormatter`, Python `structlog`) with a correlation / request id, so one request can be followed across services;
     - use the log levels deliberately;
     - never log secrets or personal data;
     - ship the logs to one central place: CloudWatch Logs, ELK / OpenSearch, or Grafana Loki.
   - Metrics for services, the RED method: request **R**ate, **E**rrors, **D**uration (latency percentiles p95 / p99, not only the average).
   - Metrics for resources, the USE method: **U**tilization, **S**aturation, **E**rrors, for CPU, memory, disk, database connections.
   - Metrics for pipelines and queues: rows or messages processed, rows rejected, run duration, queue depth / consumer lag, and data freshness (when the last successful run finished).
   - Tools: Prometheus + Grafana, CloudWatch metrics and dashboards, Datadog. Sentry for exceptions. OpenTelemetry for traces. Health-check endpoints (liveness / readiness) for the orchestrator and the load balancer.
   - Alert on symptoms users feel, not on every warning: error rate, p95 latency, queue lag, a failed job, and a job that did not run at all (a "dead man's switch" heartbeat alert).
   - Add a duration to every threshold (for example "error rate above 5% for 5 minutes"), so a single spike does not trigger the alert and the alert does not flap on and off.
   - Route by severity: critical alerts page the on-call engineer (PagerDuty, Opsgenie); warnings go to a Slack channel or email.
   - Every alert must be actionable and link to a runbook. Regularly remove or tune noisy alerts, because alert fatigue makes people ignore the real ones.
   - Advanced point: define SLOs (for example 99.9% of requests under 500 ms) and alert on the error-budget burn rate.
   - AWS example: CloudWatch Alarms → SNS topic → Slack and email, plus failure callbacks from AWS Glue / Airflow jobs. From the CV: Grafana and CloudWatch on the AI-powered platform.

## Interview 1 — Aliyev (2026-06-09, data engineering)

1. Tell me about a challenging task from your experience that, once you finished it, made you feel you could do anything.
2. How do you structure the code of a data-processing project so that it is stable and easy to configure?
   - Split the code into layers: configuration, I/O adapters (sources and sinks), transformations, and orchestration that ties them together.
   - Write transformations as pure functions (input in, output out, no I/O), so they are easy to unit-test and safe to re-run.
   - Keep configuration out of the code: environment variables or YAML files, validated at startup (for example with `pydantic-settings`), so a bad config fails immediately instead of halfway through a run.
   - Never hard-code secrets; read them from environment variables or a secret manager (AWS Secrets Manager, SSM Parameter Store).
   - Make every step idempotent (running a step twice gives the same result), so a failed run can simply be restarted.
   - Handle errors deliberately: retries with backoff for transient failures (network, throttling), a quarantine / dead-letter location for bad records, and fail-fast for programming errors.
   - Validate data at the boundaries: schema checks on input, data-quality checks on output (for example Great Expectations or pandera).
   - Use structured logging and metrics (rows read, rows written, rows rejected, duration) for every step.
   - Package the project properly: `src/` layout, `pyproject.toml`, a lockfile, and CI with linting (ruff), type checking (mypy), tests (pytest) and pre-commit hooks.
3. How do you prefer to manage Python dependencies: an old-style `requirements.txt` file or a modern tool such as uv or Poetry?
   - Prefer `pyproject.toml` plus a lockfile (uv or Poetry), because it gives reproducible builds: every environment installs exactly the same versions.
   - Explain the difference: `pyproject.toml` lists the direct dependencies with version ranges, while the lockfile (`uv.lock`, `poetry.lock`) pins every transitive dependency to an exact version and hash.
   - A plain `requirements.txt` mixes direct and transitive dependencies, or leaves transitive ones unpinned; pip-tools (`requirements.in` compiled to `requirements.txt`) is the classic fix.
   - uv: written in Rust, very fast, manages Python versions and virtual environments, and works with pip. Poetry: mature, also builds and publishes packages.
   - Separate dependency groups: runtime versus dev/test (pytest, ruff, mypy), so the production image does not contain test tools.
   - Commit the lockfile for applications; for a library, publish loose version ranges so it does not conflict with its users' pins.
   - Install from the lockfile in CI and Docker (`uv sync --frozen`, `poetry install --no-root`), and update dependencies on purpose (Dependabot / Renovate), not by accident.
   - PHP comparison: `composer.json` is `pyproject.toml`, and `composer.lock` is `uv.lock`.
4. Your pipeline has to process a very large CSV file that does not fit in memory. How do you process it, and how do you re-process it when you find that your transformation was wrong and has to be changed?
   - Never load the whole file: stream it row by row (the `csv` module reader is an iterator; wrap the processing in generators) or read it in chunks (`pandas.read_csv(chunksize=...)`), so memory depends on the chunk size, not on the file size.
   - Reduce memory per chunk: read only the needed columns (`usecols`), set explicit `dtype`s, and use categorical types for repeated strings.
   - Mention tools built for this: Polars lazy / streaming mode and DuckDB process larger-than-memory files on one machine; Spark or Dask when one machine is not enough.
   - Write the output incrementally, chunk by chunk, preferably to a columnar format such as Parquet.
   - For re-processing, keep the raw input immutable (a "raw" / "bronze" layer), and never overwrite it.
   - Convert the raw CSV to Parquet once, so every later re-run reads a smaller, faster, typed file.
   - Make the transformation deterministic and idempotent: re-running it overwrites the output (a new versioned path or an atomic partition overwrite) instead of appending duplicates.
   - Validate the output before publishing it: row counts in versus out, schema, null and range checks. Switch consumers to the new version only after validation passes.
5. Your pipeline processes terabytes of CSV files. How do you design it so that processing can be suspended and later resumed from the exact point where it stopped?
   - Checkpointing: after each committed unit of work, persist the progress (file name, byte offset or row number, batch id) in durable storage such as a database table, Redis, or an S3 object.
   - Choose the unit of work (a file or a chunk of a file) and track its state in a manifest table: `pending`, `in_progress`, `done`, `failed`.
   - Writing the output and saving the checkpoint must not drift apart: either commit both in one transaction, or make the output writes idempotent (upserts, deterministic output paths), so re-processing the last chunk after a crash creates no duplicates. At-least-once delivery plus idempotency gives an effectively-once result.
   - Graceful suspend: catch `SIGTERM` / `SIGINT`, finish the current chunk, save the checkpoint, then exit.
   - Resume: read the checkpoint, skip files already marked `done`, and seek to the saved offset in the current file.
   - Parallel workers: each worker claims a file through a queue or a row lock (`SELECT … FOR UPDATE SKIP LOCKED`), so no file is processed twice.
   - Name existing implementations of the same idea: Kafka consumer offsets, Spark Structured Streaming checkpoints, AWS Glue job bookmarks.
6. You build a reusable, multi-purpose pipeline framework used across several projects. How do you make it configurable: how to process the data, and how to plug in different sources and destinations?
   - Describe each pipeline declaratively in a config file (YAML / JSON): source, list of transformations, sink, schedule. Validate the config against a schema (for example pydantic models) when it loads.
   - Define small interfaces: a `Source` that yields batches of records, a `Sink` that writes a batch, and a `Transform` that maps a batch to a batch.
   - Implement each concrete source and sink (S3, PostgreSQL, REST API, Kafka) as an adapter behind those interfaces, and build them from config through a registry / factory keyed by a type name (Strategy and Factory patterns).
   - Write the generic engine once: it runs read → transform → write and owns retries, checkpoints, logging, metrics and data-quality checks.
   - Adding a new source or destination then means adding one adapter class, with no change to the engine (Open/Closed principle).
   - Keep secrets out of the config: the config holds a reference (environment variable name or secret ARN), and the value is read at runtime.
   - Support per-environment overrides (dev / staging / prod) on top of one base config.
   - Ship the framework as a versioned package with contract tests every adapter must pass, and let an orchestrator (Airflow, AWS Step Functions) call it.
7. Your pipeline runs in AWS and reads from an S3 bucket that holds very personal data. How do you connect the pipeline to the bucket, and how do you secure access to the bucket as tightly as possible?
   - Connect through an IAM role attached to the compute (Glue job role, ECS task role, EC2 instance profile, or IAM Roles for Service Accounts on EKS). boto3 picks up temporary credentials automatically, so there are no access keys in code or config.
   - Read efficiently: stream objects with boto3 / s3fs / Spark's `s3a`, and lay out data under partitioned prefixes so jobs read only what they need.
   - Least-privilege IAM policy: only `s3:GetObject` on the exact prefix the job needs, and `s3:ListBucket` limited to that prefix by condition.
   - Turn on S3 Block Public Access at both the account level and the bucket level, and disable ACLs (Object Ownership: bucket owner enforced).
   - Bucket policy: deny any request without TLS (`aws:SecureTransport` = false), and allow access only through the VPC endpoint (`aws:SourceVpce`) and only for the named roles.
   - Encrypt at rest with SSE-KMS using a customer-managed key; the KMS key policy is a second gate, because a role also needs `kms:Decrypt` to read the data.
   - Keep traffic private: an S3 gateway VPC endpoint, so the pipeline never goes through the internet.
   - Audit and detect: CloudTrail data events for S3, S3 server access logs, and Amazon Macie to find PII in the bucket.
   - Protect against loss and tampering: versioning, and Object Lock where regulation requires it.
   - Minimize the data: mask or tokenize PII as early as possible, so downstream systems never see raw personal data.
8. What is AWS Glue used for?
   - A serverless, managed ETL service: you write the job and AWS provides and scales the Spark cluster, so there is no cluster to manage.
   - Job types: Spark jobs (PySpark or Scala) for large data, Python shell jobs for small tasks, Ray jobs, and streaming ETL jobs (for example from Kinesis or Kafka).
   - Glue Data Catalog: a central, Hive-compatible metastore of databases, tables and schemas, shared by Athena, Redshift Spectrum and EMR.
   - Crawlers scan S3 or JDBC sources, infer the schema, and register or update tables in the Data Catalog.
   - Job bookmarks remember what was already processed, so incremental runs read only new data (the same idea as question 5).
   - Orchestration and extras: triggers and workflows, Glue Studio (visual job editor), Glue DataBrew (no-code data preparation), and Glue Data Quality rules.
   - Glue-specific API: `DynamicFrame` (schema-flexible, handles inconsistent types) next to the normal Spark `DataFrame`.
   - Cost: billed per DPU-hour, with a minimum per run. For small data a Lambda function or a Python shell job is cheaper than a Spark job.
9. Your pipeline reads from a PostgreSQL database and runs very slowly because its SQL queries load a lot of data. How do you optimize those queries: where do you start, what do you check, and what do you apply?
   - Measure first, do not guess: find the slow queries with `pg_stat_statements` or the slow-query log (`log_min_duration_statement`).
   - Read the plan with `EXPLAIN (ANALYZE, BUFFERS)`: sequential scans on big tables, estimated rows far from actual rows, sorts or hashes spilling to disk, nested loops over large sets.
   - Load less data: select only the needed columns (no `SELECT *`), filter in SQL instead of in Python, and aggregate in the database.
   - Extract incrementally: `WHERE updated_at > :last_watermark` instead of reloading the full table on every run.
   - Add indexes on the filter, join and sort columns; mind the column order in composite indexes; use covering indexes (`INCLUDE`) for index-only scans.
   - Paginate with keyset pagination (`WHERE id > :last_id ORDER BY id LIMIT n`), not `OFFSET`, which gets slower on every page.
   - Do not pull the whole result into client memory: use a server-side cursor (a psycopg named cursor with `fetchmany`), or `COPY … TO` for bulk export.
   - Partition very large tables (for example by date), so partition pruning skips irrelevant data.
   - Rewrite problem patterns: functions applied to indexed columns (the index is not used), N+1 queries from the application, correlated subqueries.
   - Keep planner statistics fresh (`ANALYZE`, autovacuum), and watch table bloat.
   - Take the load off the primary: run extraction queries against a read replica, and precompute heavy aggregates in materialized views.
   - MySQL comparison: the same method applies, with `EXPLAIN ANALYZE`, the slow query log and `performance_schema`.
10. What are an image and a container in Docker, and how do they differ?
    - An image is a read-only template: a stack of filesystem layers plus metadata (entrypoint / command, environment variables, exposed ports, working directory).
    - An image is built from a Dockerfile, stored in a registry, and identified by a tag (mutable, for example `app:1.4`) and a digest (immutable content hash).
    - A container is a running (or stopped) instance of an image: the image's read-only layers plus a thin writable layer on top, run as an isolated process.
    - Isolation comes from Linux namespaces (processes, network, mounts, users), and resource limits come from cgroups (CPU, memory).
    - Analogy: an image is a class, a container is an object. One image can start many containers.
    - Anything a container writes to its writable layer is lost when the container is removed, so persistent data belongs in volumes or bind mounts.
    - Containers share the host's kernel, so they are lighter and faster to start than virtual machines, which each run their own kernel.
    - Commands that show the difference: `docker build` / `docker pull` / `docker images` work with images; `docker run` / `docker ps` / `docker exec` work with containers.
11. Why do we say a Docker image is layered, and why is that important when you write a Dockerfile?
12. What rules do you follow to write the most efficient Dockerfile?
13. A typical Python Dockerfile goes: `FROM` a base image, install OS packages, copy `requirements.txt`, install the dependencies, and copy the source code last. Why is it written in exactly that order?
14. Two applications run as containers on the same Docker host, for example your pipeline and a Kafka container, and one cannot reach the other. Why can that happen?
15. Do you have experience building multi-architecture Docker images, and can you set up a CI/CD pipeline that builds them?
16. What is your experience with Terraform?
17. How do you monitor your pipeline: whether it works, its problems, its performance, CPU usage and memory usage? What tools do you use?
18. What is your attitude to unit tests? Do you write them, and why?
19. What is a mock object in unit testing?
20. Log files on a regular file system grow by gigabytes a day, new files keep arriving every hour, and the file currently being read keeps being appended to. How do you process them memory-efficiently, and resume from the same position in the same file after the process dies?

## Interview 2 — Heniuk (2026-07-01, Python backend)

1. Tell me about a challenging task from your experience that, once you finished it, made you feel you could do anything.
2. Why is Python so popular for backend development?
3. How do you structure a large backend project that has several APIs and also scheduled (cron) tasks?
4. How do you configure your application, instead of hard-coding connection strings and other settings?
5. Apart from slow SQL, what are the main performance problems of an API, why do they happen, and how do you avoid them?
6. You build a RESTful API with FastAPI. Give a strict definition: what is REST, and what makes an API RESTful?
7. What do the URLs in a RESTful API look like: which parts do they have (resources, IDs, version)?
8. A user picks a date range and filters, and the API must generate a report, or process an uploaded file into a PDF, which takes several minutes and cannot be sped up. A synchronous request would hit the 30-second default timeout or Cloudflare's one-minute limit. How do you implement this RESTfully?
9. How do you secure API endpoints and restrict operations by user role (authentication and authorization)?
10. You use JWTs. What is their main problem?
11. You implement a webhook for a payment provider such as Stripe. It is a public endpoint with no login and no JWT. How do you secure it as much as possible?
12. How do you verify that the webhook payload (transaction ID, amount, currency) was not modified by a third party?
13. You built an API and I am the frontend developer who will use it. How do you give me as much information as possible about the API?
14. A public API is already in production and used by partners. The naming convention requires renaming the public field `user_id` to `id`, and the database does not change. How do you make this change without breaking partners?
15. In a distributed system, how can the different parts communicate with each other?
16. What is database normalization?
17. When and why do you denormalize tables? Give examples.
18. A query is slow. How do you optimize it: where do you start checking, and what do you implement?
19. Is it good to have many indexes on a table? What does each extra index cost?
20. Have you worked with RabbitMQ?
21. What is an exchange in RabbitMQ, and what types of exchange exist?
22. When do you use a fanout exchange?
23. Have you worked with WebSockets? A dashboard needs real-time, bidirectional updates, and the backend runs on four horizontally scaled servers. How do you tell each user's browser that something on the UI must be updated?
24. In that setup, what kind of queue does each backend server declare, and with which queue parameters (for example durable or not)?
25. Everyone likes Docker. Do you, and why?
26. When you write a Dockerfile, why is it important to remember that images are layered?
27. Why are multi-stage Docker builds useful: a build stage installs build dependencies and builds, and only its output is copied into the final base image?
28. Do you have experience building multi-architecture Docker images?
29. What types of network exist in Docker?
30. Two containers on one Docker host need to talk to each other but cannot. Why?
31. Can you set up a CI/CD pipeline from scratch, or have you only modified existing pipelines?
32. Why do we write unit tests, what do we usually use for testing, what is a mock object, and what do we usually mock?
33. How do you test FastAPI endpoints?
34. How do you do logging and monitoring for an application, and how do you configure useful alerts?
35. Not how to set up a Kubernetes cluster from scratch, but: do you know how to use `kubectl`, check logs in the cluster, and get a shell into a pod to troubleshoot?
36. Have you written CLI tools, meaning console applications that accept parameters?
