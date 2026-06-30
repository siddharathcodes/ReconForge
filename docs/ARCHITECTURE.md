# ReconForge X Architecture Blueprint

## 1. Product Vision

ReconForge X is an operating system for bug bounty reconnaissance. It does not try to replace every mature security tool. It orchestrates proven tools, normalizes their outputs, preserves history, enriches data with safe analysis, and presents prioritized investigation paths.

The product goals are:

- Unify external reconnaissance workflows across targets and teams.
- Preserve historical attack surface changes.
- Normalize scanner outputs into a central graph-ready data model.
- Reduce noise through scoring, deduplication, diffing, and AI-assisted triage.
- Expose every UI capability through a documented API.
- Support long-running background jobs through queues and workers.
- Allow scanners and enrichers to be added through plugins.

## 2. Core Principles

- Safe by default: passive and authorized checks only unless explicitly configured.
- Modular by domain: every major module owns its API, service layer, schemas, models, jobs, and UI route.
- Queue-first execution: recon tasks run as durable jobs outside request lifecycles.
- History-first storage: every scan result is attributable to workspace, target, source, job, and scan timestamp.
- Normalize before analyze: tool outputs are converted into canonical records before enrichment.
- API parity: every UI action is backed by an authenticated API endpoint.
- Explainable AI: AI suggests investigation steps and risk reasoning, but does not claim confirmed vulnerabilities.

## 3. System Architecture

### 3.1 Runtime Components

- Frontend: React, TypeScript, Vite, TailwindCSS.
- API: FastAPI application exposing REST endpoints and OpenAPI documentation.
- Database: PostgreSQL for normalized relational data.
- Queue: Redis broker for Celery workers.
- Workers: Celery workers for scan execution, parsing, enrichment, diffing, and report generation.
- Scheduler: Celery beat or a dedicated scheduler service for monitoring jobs.
- Object storage: future storage layer for screenshots, exported reports, and large raw artifacts.
- AI engine: service boundary for risk scoring, summarization, screenshot classification, and investigation guidance.
- Plugin runtime: controlled execution layer for external tools and custom scanners.

### 3.2 Logical Domains

- Identity and Access
- Workspaces and Targets
- Asset Discovery
- Live Host Intelligence
- DNS Intelligence
- Screenshot Intelligence
- Technology Detection
- JavaScript Intelligence
- Endpoint and Parameter Intelligence
- API Discovery
- Secret Detection
- Historical Recon
- Cloud Discovery
- Passive Security Analysis
- Risk Engine
- Recon Timeline
- Recon Graph
- AI Assistant
- Collaboration
- Monitoring
- Reporting
- Integrations
- Plugin Management
- Audit and Observability

## 4. Backend Folder Contract

Each domain should follow the same internal shape as it grows:

```text
backend/app/<domain>/
  api.py
  models.py
  schemas.py
  service.py
  repository.py
  jobs.py
  policies.py
  events.py
```

The existing foundation keeps shared layers in:

```text
backend/app/api/
backend/app/auth/
backend/app/config/
backend/app/core/
backend/app/database/
backend/app/middleware/
backend/app/models/
backend/app/schemas/
backend/app/services/
backend/app/workers/
backend/app/plugins/
backend/app/reports/
backend/app/ai/
backend/app/utils/
```

## 5. Module Catalog

| Module | Purpose | Background Jobs |
| --- | --- | --- |
| Dashboard | Operations summary and priority queue | Aggregation refresh |
| Asset Discovery | Domains, subdomains, DNS, ASN, CIDR, CT, WHOIS, cloud and third-party assets | subfinder, amass, CT import, DNS enrichment |
| Live Hosts | HTTP probing, TLS, redirects, CDN, WAF, title, response metadata | httpx probing, TLS collection |
| Screenshots | Capture and classify visual pages | screenshot capture, AI classification, clustering |
| Technology Detection | Identify frameworks, servers, languages, CMS, and versions | WhatWeb/Wappalyzer-style fingerprinting |
| Port Scanner | Authorized port and service inventory | nmap, masscan, service probes |
| JavaScript Intelligence | Parse JS, source maps, endpoints, secrets, routes, comments, tokens | JS fetch, AST parse, secret scan |
| Endpoint Discovery | Merge crawler, archive, JS, and API endpoints | katana, gau, waybackurls normalization |
| Parameter Discovery | Discover and classify high-value parameters | Arjun, endpoint parameter extraction |
| Secret Scanner | Detect credentials and sensitive material across artifacts | pattern scanning, validator-safe enrichment |
| Historical Recon | Old JS, old APIs, removed pages, old robots and sitemaps | archive ingestion, timeline diff |
| Cloud Discovery | Identify cloud providers and public resources safely | bucket naming checks, metadata normalization |
| GraphQL Analysis | Discover and profile GraphQL endpoints safely | introspection check only when authorized |
| Swagger/OpenAPI | Detect specs and map API routes | spec fetch, route extraction |
| API Discovery | Classify REST, SOAP, gRPC, GraphQL, Swagger, OpenAPI, Postman | API fingerprinting |
| Security Headers | CSP, HSTS, cookies, CORS, robots, exposure checks | passive HTTP analysis |
| Passive Vulnerability Detection | Safe signal-based finding generation | nuclei safe templates, passive rules |
| AI Risk Engine | Score and explain interesting assets and findings | scoring, reason generation |
| Recon Graph | Relationship model from company to finding | graph projection refresh |
| Monitoring | Scheduled scans and notifications | scheduled scans, change alerts |
| Team Collaboration | Notes, tags, assignments, comments, audit log | notification fanout |
| Reports | JSON, CSV, HTML, PDF exports | report render jobs |
| Integrations | Webhooks, Slack, Discord, Jira, GitHub | outbound delivery |
| Settings | Organization, workspace, policies, scanner configuration | configuration validation |

## 6. Database Schema Blueprint

### 6.1 Identity and Access

- users
- organizations
- organization_memberships
- roles
- permissions
- role_permissions
- api_keys
- auth_sessions
- audit_events

### 6.2 Workspaces and Targets

- workspaces
- workspace_memberships
- targets
- target_scopes
- target_programs
- target_notes
- tags
- taggings
- attachments

### 6.3 Scan Orchestration

- scan_profiles
- scan_jobs
- scan_job_steps
- scan_artifacts
- scan_errors
- scanner_plugins
- plugin_runs
- scheduled_scans
- notification_rules

### 6.4 Assets

- domains
- subdomains
- dns_records
- whois_records
- certificate_records
- asns
- cidr_ranges
- ip_addresses
- cloud_assets
- third_party_services
- mobile_app_assets

### 6.5 Live Hosts and Network

- live_hosts
- http_observations
- redirect_chains
- tls_observations
- ports
- services
- waf_detections
- cdn_detections
- screenshots
- screenshot_clusters

### 6.6 Application Intelligence

- technologies
- asset_technologies
- javascript_files
- javascript_findings
- source_maps
- endpoints
- endpoint_observations
- parameters
- parameter_observations
- api_collections
- api_routes
- graphql_endpoints
- openapi_documents

### 6.7 Findings and Risk

- findings
- finding_evidence
- finding_scores
- finding_status_history
- passive_checks
- security_header_results
- secret_detections
- exposure_indicators
- ai_risk_explanations

### 6.8 History and Graph

- timeline_events
- scan_diffs
- diff_items
- graph_nodes
- graph_edges
- saved_searches
- search_index_records

### 6.9 Collaboration and Reporting

- comments
- assignments
- report_templates
- reports
- report_sections
- report_exports
- integration_connections
- outbound_notifications

This blueprint intentionally starts broader than v1. Tables should be introduced with migrations only when a module is implemented.

## 7. API Design

All endpoints are versioned under `/api/v1`.

Core endpoint groups:

- `/health`
- `/modules`
- `/auth`
- `/organizations`
- `/workspaces`
- `/targets`
- `/scan-profiles`
- `/scan-jobs`
- `/assets`
- `/hosts`
- `/dns`
- `/screenshots`
- `/technologies`
- `/ports`
- `/javascript`
- `/endpoints`
- `/parameters`
- `/secrets`
- `/history`
- `/cloud`
- `/apis`
- `/security-headers`
- `/findings`
- `/risk`
- `/timeline`
- `/graph`
- `/assistant`
- `/comments`
- `/reports`
- `/integrations`
- `/settings`

API rules:

- Use typed request and response schemas.
- Use cursor pagination for large result sets.
- Use idempotency keys for job creation.
- Return accepted jobs with durable job IDs for long-running operations.
- Emit audit events for sensitive actions.
- Enforce workspace scope on every tenant-owned resource.

## 8. Queue and Worker System

Worker queues:

- `scan.discovery`
- `scan.http`
- `scan.network`
- `scan.javascript`
- `scan.archives`
- `scan.secrets`
- `scan.cloud`
- `scan.passive`
- `scan.diff`
- `ai.enrichment`
- `reports.render`
- `notifications.deliver`

Job lifecycle:

1. API creates a `scan_jobs` record.
2. Scheduler expands the job into `scan_job_steps`.
3. Workers execute steps and persist raw artifacts.
4. Parsers normalize artifacts into canonical tables.
5. Diff engine compares current data to previous scans.
6. Risk engine scores interesting records and findings.
7. Notifications and timeline events are emitted.

## 9. Plugin System

Plugin categories:

- Discovery
- HTTP probing
- Network scanning
- Crawling
- Archive ingestion
- JavaScript analysis
- Secret detection
- Passive checks
- AI enrichers
- Report exporters

Plugin contract:

- Manifest declares name, version, author, category, capabilities, inputs, outputs, and safety level.
- Runtime receives a typed execution context.
- Plugin returns structured output plus raw artifact references.
- Core validates and normalizes plugin output.
- Plugins cannot directly mutate canonical tables.

Recommended external tools:

- subfinder
- amass
- httpx
- katana
- nmap
- masscan
- gau
- waybackurls
- arjun
- WhatWeb
- nuclei with optional safe templates

## 10. AI Engine

AI capabilities:

- Risk scoring
- Finding prioritization
- Screenshot classification
- Report drafting
- Recon data question answering
- Investigation suggestions
- Timeline summaries

Guardrails:

- AI must distinguish evidence from hypotheses.
- AI must recommend tests, not claim vulnerabilities without proof.
- AI prompts must include workspace authorization context.
- Sensitive data should be redacted before external model calls unless explicitly allowed.
- All AI outputs should be traceable to source records.

## 11. Frontend Information Architecture

Primary navigation:

- Dashboard
- Asset Discovery
- Live Hosts
- Screenshots
- Technology Detection
- Port Scanner
- JavaScript Intelligence
- Endpoint Discovery
- Parameter Discovery
- Secret Scanner
- Historical Recon
- Cloud Discovery
- GraphQL Analysis
- Swagger/OpenAPI
- API Discovery
- Security Header Analysis
- Passive Vulnerability Detection
- AI Risk Engine
- Recon Graph
- Monitoring
- Team Collaboration
- Reports
- Integrations
- Settings

UI principles:

- Operational density over marketing layout.
- First screen should show work queues, risk priorities, job state, and changes.
- Every module page should expose filters, saved views, exports, and source evidence.
- Every high-risk item should explain why it is prioritized.

## 12. Security Model

- Organization-level tenancy.
- Workspace-level authorization.
- API keys scoped by workspace and permission.
- Role-based access control.
- Audit logs for authentication, exports, scan creation, target changes, integrations, and AI data access.
- Secret values encrypted at rest where storage is required.
- Sensitive artifacts redacted in logs.
- Scanner execution constrained by target scope and safety policies.

## 13. Deployment

Initial Docker Compose services:

- frontend
- backend
- worker
- postgres
- redis

Future production services:

- API replicas behind a reverse proxy.
- Worker pools by queue.
- Scheduler service.
- Object storage.
- PostgreSQL read replica for analytics.
- Observability stack.
- Kubernetes deployment with network policies, sealed secrets, autoscaling, and job isolation.

## 14. Development Roadmap

### v1.0 Foundation

- Auth, organizations, workspaces, targets.
- Scan job model and queue orchestration.
- Asset discovery with external tool adapters.
- Live host probing.
- Basic dashboard and health/status pages.

### v2.0 Intelligence Core

- Endpoint discovery.
- JavaScript parsing.
- Secret detection.
- Technology detection.
- Security header analysis.

### v3.0 History and Prioritization

- Diff engine.
- Timeline.
- Risk scoring.
- Saved searches.
- Prioritized findings.

### v4.0 Visualization and Reporting

- Recon graph.
- Screenshot intelligence.
- Report builder.
- JSON, CSV, HTML, PDF exports.

### v5.0 Collaboration

- Notes, tags, comments, assignments.
- Audit logs.
- Team workflows.
- Notifications.

### v6.0 Plugin Platform

- Plugin manifests.
- Plugin execution sandbox.
- Plugin marketplace metadata.
- Custom scanner support.

### v7.0 AI Copilot

- Chat over recon data.
- Investigation suggestions.
- Risk explanations.
- AI report generation.

### v8.0 Cloud and API Depth

- Cloud asset intelligence.
- GraphQL analysis.
- Swagger/OpenAPI and Postman ingestion.
- gRPC and SOAP detection.

### v9.0 Enterprise Operations

- SSO.
- Advanced RBAC.
- Multi-region deployments.
- Compliance exports.
- Advanced observability.

### v10.0 Platform Expansion

- CLI.
- Desktop application.
- SaaS operations.
- Mobile companion alerts.
- Public plugin marketplace.
