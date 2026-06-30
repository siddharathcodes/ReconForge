from enum import StrEnum
from typing import Final

from pydantic import BaseModel, ConfigDict


class ModuleStatus(StrEnum):
    FOUNDATION = "foundation"
    PLANNED = "planned"
    ACTIVE = "active"


class ModuleDefinition(BaseModel):
    model_config = ConfigDict(frozen=True)

    key: str
    name: str
    description: str
    status: ModuleStatus
    route: str
    worker_queues: tuple[str, ...] = ()


MODULE_CATALOG: Final[tuple[ModuleDefinition, ...]] = (
    ModuleDefinition(
        key="dashboard",
        name="Dashboard",
        description="Operational overview for scan activity, risk priorities, and attack surface changes.",
        status=ModuleStatus.FOUNDATION,
        route="/dashboard",
    ),
    ModuleDefinition(
        key="asset_discovery",
        name="Asset Discovery",
        description="Discovers domains, subdomains, DNS records, ASN, CIDR, certificates, and third-party assets.",
        status=ModuleStatus.PLANNED,
        route="/assets/discovery",
        worker_queues=("scan.discovery",),
    ),
    ModuleDefinition(
        key="live_hosts",
        name="Live Hosts",
        description="Collects HTTP status, redirects, TLS, WAF, CDN, titles, screenshots, and response metadata.",
        status=ModuleStatus.PLANNED,
        route="/live-hosts",
        worker_queues=("scan.http",),
    ),
    ModuleDefinition(
        key="screenshots",
        name="Screenshots",
        description="Captures, classifies, and clusters visual application states.",
        status=ModuleStatus.PLANNED,
        route="/screenshots",
        worker_queues=("scan.http", "ai.enrichment"),
    ),
    ModuleDefinition(
        key="technology_detection",
        name="Technology Detection",
        description="Fingerprints frameworks, servers, CMS platforms, libraries, and exposed versions.",
        status=ModuleStatus.PLANNED,
        route="/technologies",
        worker_queues=("scan.passive",),
    ),
    ModuleDefinition(
        key="port_scanner",
        name="Port Scanner",
        description="Runs authorized network scanning and normalizes exposed ports and services.",
        status=ModuleStatus.PLANNED,
        route="/ports",
        worker_queues=("scan.network",),
    ),
    ModuleDefinition(
        key="javascript_intelligence",
        name="JavaScript Intelligence",
        description="Parses JavaScript, source maps, endpoints, routes, comments, tokens, and secrets.",
        status=ModuleStatus.PLANNED,
        route="/javascript",
        worker_queues=("scan.javascript", "scan.secrets"),
    ),
    ModuleDefinition(
        key="endpoint_discovery",
        name="Endpoint Discovery",
        description="Merges crawler, archive, JavaScript, and API outputs into canonical endpoints.",
        status=ModuleStatus.PLANNED,
        route="/endpoints",
        worker_queues=("scan.archives", "scan.javascript"),
    ),
    ModuleDefinition(
        key="parameter_discovery",
        name="Parameter Discovery",
        description="Indexes parameters and classifies high-value auth, file, redirect, debug, upload, and API inputs.",
        status=ModuleStatus.PLANNED,
        route="/parameters",
        worker_queues=("scan.passive",),
    ),
    ModuleDefinition(
        key="secret_scanner",
        name="Secret Scanner",
        description="Detects credentials and sensitive tokens across HTML, JS, JSON, headers, and stored artifacts.",
        status=ModuleStatus.PLANNED,
        route="/secrets",
        worker_queues=("scan.secrets",),
    ),
    ModuleDefinition(
        key="historical_recon",
        name="Historical Recon",
        description="Collects old JS, APIs, robots, sitemaps, deleted pages, and removed admin panels.",
        status=ModuleStatus.PLANNED,
        route="/history",
        worker_queues=("scan.archives", "scan.diff"),
    ),
    ModuleDefinition(
        key="cloud_discovery",
        name="Cloud Discovery",
        description="Identifies cloud providers and public resources using safe, non-invasive checks.",
        status=ModuleStatus.PLANNED,
        route="/cloud",
        worker_queues=("scan.cloud",),
    ),
    ModuleDefinition(
        key="graphql_analysis",
        name="GraphQL Analysis",
        description="Detects GraphQL endpoints and profiles exposed behavior within authorization policy.",
        status=ModuleStatus.PLANNED,
        route="/graphql",
        worker_queues=("scan.passive",),
    ),
    ModuleDefinition(
        key="swagger_openapi",
        name="Swagger/OpenAPI",
        description="Detects OpenAPI documents and maps routes, methods, schemas, and risky operations.",
        status=ModuleStatus.PLANNED,
        route="/openapi",
        worker_queues=("scan.passive",),
    ),
    ModuleDefinition(
        key="api_discovery",
        name="API Discovery",
        description="Classifies REST, SOAP, gRPC, GraphQL, Swagger, OpenAPI, and Postman assets.",
        status=ModuleStatus.PLANNED,
        route="/apis",
        worker_queues=("scan.passive",),
    ),
    ModuleDefinition(
        key="security_headers",
        name="Security Header Analysis",
        description="Analyzes CSP, HSTS, cookie flags, CORS, robots, and passive exposure indicators.",
        status=ModuleStatus.PLANNED,
        route="/security-headers",
        worker_queues=("scan.passive",),
    ),
    ModuleDefinition(
        key="passive_vulnerability_detection",
        name="Passive Vulnerability Detection",
        description="Generates safe signal-based findings from passive checks and optional safe templates.",
        status=ModuleStatus.PLANNED,
        route="/findings/passive",
        worker_queues=("scan.passive",),
    ),
    ModuleDefinition(
        key="ai_risk_engine",
        name="AI Risk Engine",
        description="Scores interesting records and explains why they deserve investigation.",
        status=ModuleStatus.PLANNED,
        route="/risk",
        worker_queues=("ai.enrichment",),
    ),
    ModuleDefinition(
        key="recon_graph",
        name="Recon Graph",
        description="Projects relationships between company, domains, hosts, ports, services, endpoints, and findings.",
        status=ModuleStatus.PLANNED,
        route="/graph",
        worker_queues=("scan.diff",),
    ),
    ModuleDefinition(
        key="monitoring",
        name="Monitoring",
        description="Runs scheduled scans and notifies teams about attack surface changes.",
        status=ModuleStatus.PLANNED,
        route="/monitoring",
        worker_queues=("notifications.deliver",),
    ),
    ModuleDefinition(
        key="team_collaboration",
        name="Team Collaboration",
        description="Supports notes, tags, assignments, comments, reports, and audit history.",
        status=ModuleStatus.PLANNED,
        route="/collaboration",
    ),
    ModuleDefinition(
        key="reports",
        name="Reports",
        description="Generates professional JSON, CSV, HTML, and PDF reports.",
        status=ModuleStatus.PLANNED,
        route="/reports",
        worker_queues=("reports.render",),
    ),
    ModuleDefinition(
        key="integrations",
        name="Integrations",
        description="Connects ReconForge to external notification and workflow systems.",
        status=ModuleStatus.PLANNED,
        route="/integrations",
        worker_queues=("notifications.deliver",),
    ),
    ModuleDefinition(
        key="settings",
        name="Settings",
        description="Manages organization, workspace, scanner, safety, and notification configuration.",
        status=ModuleStatus.FOUNDATION,
        route="/settings",
    ),
)
