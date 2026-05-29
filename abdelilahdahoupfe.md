# ProvisionHub — IAM Middleware Documentation
**Generated for:** Abdelilah Dahou (PFE)
**Project Version:** 1.0.0

---

## 1. Executive Summary

**ProvisionHub** is a high-performance IAM (Identity and Access Management) Middleware built to orchestrate the provisioning lifecycle for over 40,000 employees. It acts as a central orchestration engine, aggregating identity data from various upstream sources (HRIS, Portals, Webhooks) and synchronizing it with target technical systems (LDAP, GitLab, Jira, SMTP, etc.). 

At its core, it implements a **Hub 360° event-driven architecture**, acting as a unified pivot view to maintain a consolidated "Target State" for every organizational identity in real-time.

---

## 2. Technical Stack

- **Backend Framework:** Spring Boot 3.3.5 (Java 21)
- **Database:** PostgreSQL (Primary), MySQL (Portal Data) with Flyway for schema migrations.
- **Messaging/Eventing:** RabbitMQ (AMQP) for async event-driven orchestration and DLQ.
- **Security:** Spring Security (OAuth2/JWT, LDAP integration, stateless sessions, RBAC).
- **Caching & Rate Limiting:** Caffeine Cache, Bucket4j.
- **API Documentation:** OpenAPI 3.0 (Swagger UI).
- **Observability:** Micrometer + Actuator (Prometheus metrics).

---

## 3. Architecture & Core Concepts (Hub 360°)

The application aggregates employee data from **7 primary dimensions** (sources):
1. **IDENTITY** (Core RH)
2. **TEAM** (MyTeam)
3. **LEAVE** (Congés)
4. **PLANNING** (Shifts & Schedules)
5. **LOGIN** (SSO)
6. **TELEPHONY** 
7. **BADGE** 

### 3.1. Event Flow (The Ingestion Pipeline)
1. **Webhook Reception:** Dedicated webhook controllers (e.g., `MyTeamWebhookController`, `CongesWebhookController`) receive HTTP POST payloads from upstream applications.
2. **Integration Services:** Data is validated and standardized into an `EmployeeEvent`.
3. **Event Processor:** The orchestrator persists the event in `employee_event`, updates the respective dimension tables, and uses business rules to decide if this event warrants downstream provisioning.
4. **Policy Engine Evaluation:** For each active connector (LDAP, GMAIL, etc.), the `PolicyEngine` evaluates SpEL (Spring Expression Language) policies. If a rule triggers, a `PolicyDecision` (CREATE, UPDATE, DELETE, or SKIP) is formulated.
5. **Job Dispatcher:** For actionable decisions, a `ProvisioningJob` is created with a `PENDING` status.
6. **Job Execution:** Asynchronous workers pick up pending jobs and execute them via the respective plugins/connectors.

### 3.2. Declarative Workflows (Hub-and-Spoke V2)
The application includes a powerful V2 orchestrator (`WorkflowOrchestrator`) that manages multi-step execution graphs:
1. **Source Extraction:** Fetches bulk data from REST APIs using encrypted credentials (AES-256-GCM).
2. **Filtering Engine:** Evaluates records using recursive logical combinators (AND, OR, NOT) and 15+ operators (REGEX, CONTAINS, GT, IS_NULL).
3. **Transformation Engine:** JSON-based declarative mapper supporting inline functions (`UPPERCASE`, `SHA256`) and computed string interpolations (e.g., `${firstName}.${lastName}`).
4. **Dispatch:** Re-evaluates policies on transformed data and logs partitioned `Exchange` HTTP trace records for audit and compliance.

### 3.3. RabbitMQ Topology & Messaging
The backend separates real-time events from heavy batch jobs via distinct RabbitMQ exchanges:
- `provisionhub.events`: Topic exchange routing `employee.*.*` events to dedicated dimension queues (`employee.events`, `assignment.events`, `leave.events`).
- `corelistener.exchange`: Dispatches provisioning jobs to the `provisioning_queue` for external workers.
- **Poison Message Handling:** The system supports simulated fault injection and routes exhausted retries directly to native RabbitMQ `.dlq` queues, captured by `RabbitMQDlqListener`.

### 3.4. Error Handling, Retry & DLQ
- **Error Classification:** Errors are classified into `TRANSIENT` (e.g., network timeouts), `RATE_LIMITED`, `AUTH_ERROR`, or `PERMANENT` (e.g., bad request, 404).
- **Exponential Backoff:** `TRANSIENT` and `RATE_LIMITED` errors undergo retries using exponential backoff (e.g., 30s, 60s, 120s up to a `maxRetries` threshold) managed by `RetryManager`.
- **Dead Letter Queue (DLQ):** Exhausted retries or `PERMANENT` errors trigger routing to the DLQ (`dead_letter` table). Operations teams can monitor, resolve, or manually retry these entries via the DLQ API endpoints.

---

## 4. API & Controller Layer

The API is highly modular, grouped into REST controllers under `/api/v1/` and `/api/v2/`.

### 4.1. Core IAM & Organization
- **EmployeeController (`/api/v1/employees`)**: Manages employee lifecycles, retrieves 360° timelines, target states, assignments, and audit trails.
- **Hub360Controller (`/api/v1/hub360`)**: Provides the consolidated pivot view (contracts, assignments).
- **PolicyController (`/api/v1/policies`)**: CRUD for IAM policies. Allows exporting/importing rules and validating SpEL expressions.
- **JobController (`/api/v1/jobs`)**: Job monitoring, backfilling, cancelation, and manual execution triggers.

### 4.2. Workflow & Ingestion
- **SourceV2Controller (`/api/v2/sources`) & WorkflowController**: Full declarative ETL pipelines. Configure Extract (REST/CSV) -> Stage -> Transform (JSON Mapping Engine) -> Load (Destinations).
- **EventController & EventStatsController (`/api/v1/events`)**: Querying of ingested events, batch ingestion, and analytical stats.
- **OnboardingController (`/api/v1/onboarding`)**: Workflows specific to new hires.

### 4.3. System Resilience & Operations
- **ConnectorController (`/api/v1/connectors`)**: Plugin management, secrets rotation, connection testing, and LDAP sync execution.
- **DlqController (`/api/v1/dlq`)**: Dead Letter Queue management (dismiss, resolve, retry).
- **DriftController (`/api/v1/drift`)**: Discrepancy detection between the Hub state and external target states (e.g., LDAP).
- **AlertController (`/api/v1/alerts`)**: Notification configuration for system thresholds.
- **DashboardController (`/api/v1/dashboard`)**: Aggregated metrics for the front-end Admin Portal.

### 4.4. Security & Authentication
- **AuthController (`/api/v1/auth`)**: OAuth2 callback, token refresh, and user profile management via JWT stored in secure HTTP-only cookies.
- **Filters**: Protected by `JwtAuthFilter` for role-based access control (RBAC) and `RateLimitingFilter` (10 requests/minute on auth endpoints).

---

## 5. Database Schema & Flyway Migrations

The database leverages PostgreSQL schemas extensively with partitioning and `JSONB` for flexibility.

### 5.1. Central Entities
- `employee`: Master table containing core identity details, references, and a JSONB `attrs` payload.
- `employee_history`: Partitioned table tracking all state changes over time.
- `policy` & `policy_version_history`: Stores the SpEL expressions and tracks modifications for rollback capabilities.
- `job`, `job_step`, `step_log`: Tracks the status, payload, and retry counts of provisioning tasks.
- `decision_audit`: Partitioned table explaining *why* a policy triggered or skipped a job.
- `dead_letter`: Records tasks that completely failed execution for manual administrative resolution.

### 5.2. Organization & 360° Dimensions
Structured in migrations (e.g., `V202604280003__hub360_schema.sql`):
- `organization`, `region`, `country`, `site`, `direction`, `uo`, `project`, `team`.
- Dimension facts: `employee_event`, `employee_team`, `employee_leave`, `employee_login`, `employee_planning`, `employee_telephony`.

### 5.3. Declarative Workflows (V2)
Structured in migrations (e.g., `V202604280010__workflow_exchange_schema.sql`):
- `source`, `source_endpoint`, `destination`, `destination_operation`.
- `workflow`, `workflow_run`, `exchange` (partitioned HTTP call records).

---

## 6. Testing Strategy

The project employs a robust suite of unit and integration tests (using MockMvc, Mockito, and H2/Testcontainers).

- **API Integration:** Controller tests (`PolicyControllerTest`) verifying complete CRUD lifecycles, HTTP response codes, and database transactions.
- **Business Logic:** Service layer tests (`FieldMappingServiceTest`, `PolicyServiceTest`) covering JSON payload mappings, partial updates, and version incrementing.
- **Engine Rules:** Granular tests (`FilterEngineTest`, `TransformEngineTest`) covering the dynamic SpEL parsers, AND/OR logic, nested conditions, string manipulation, hashing, and default fallbacks.
- **Resilience:** `JobResilienceTest` validates that `TRANSIENT` errors correctly reschedule jobs via exponential backoff, while `PERMANENT` errors are immediately routed to the Dead Letter Queue.

---

## 7. Next Steps & Focus
The immediate roadmap for ProvisionHub involves moving towards **Resilience Testing**, specifically simulating high loads and verifying the recovery behavior of the Dead Letter Queue (DLQ) across various mocked connector failure scenarios.
