import json
import os
from dataclasses import dataclass, field
from typing import Any
from langchain_core.tools import tool

@dataclass
class Service:
    id: str = ""
    name: str = ""
    type: str = ""
    description: str = ""
    repository: str = ""
    tech_stack: list[str] = field(default_factory=list)
    owner_team: str = ""
    primary_maintainer: str = ""
    status: str = ""
    uptime_percentage: float = 0.0
    avg_response_time_ms: int = 0
    request_per_day: int = 0
    production_url: str = ""
    staging_url: str = ""
    current_version: str = ""
    deployment_frequency: str = ""
    last_deployment: str = ""
    dependencies: list[str] = field(default_factory=list)
    monitoring_dashboard: str = ""
    documentation: str = ""


class ServicesService:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.services = []
        self.read_services_from_json()

    def read_services_from_json(self):
        try:
            with open(f"{self.path}/../sources/Json_files/services.json", "r") as f:
                data = json.load(f)
                for d in data:
                    service = Service()
                    service.id = d.get("id", "")
                    service.name = d.get("name", "")
                    service.type = d.get("type", "")
                    service.description = d.get("description", "")
                    service.repository = d.get("repository", "")
                    service.tech_stack = d.get("tech_stack", [])
                    service.owner_team = d.get("owner_team", "")
                    service.primary_maintainer = d.get("primary_maintainer", "")
                    service.status = d.get("status", "")
                    service.uptime_percentage = d.get("uptime_percentage", 0.0)
                    service.avg_response_time_ms = d.get("avg_response_time_ms", 0)
                    service.request_per_day = d.get("request_per_day", 0)
                    service.production_url = d.get("production_url", "")
                    service.staging_url = d.get("staging_url", "")
                    service.current_version = d.get("current_version", "")
                    service.deployment_frequency = d.get("deployment_frequency", "")
                    service.last_deployment = d.get("last_deployment", "")
                    service.dependencies = d.get("dependencies", [])
                    service.monitoring_dashboard = d.get("monitoring_dashboard", "")
                    service.documentation = d.get("documentation", "")
                    self.services.append(service)
        except Exception as e:
            print(f"Error loading services: {e}")

    def search_by_key_with_operator(self, key: str, value: Any, operator: str = "equals") -> list[Service]:
        """Search services by key with comparison operators."""
        results = []

        for service in self.services:
            service_value = getattr(service, key)

            # Convert value to appropriate type for numeric comparisons
            if operator in ["greater_than", "less_than", "greater_equal", "less_equal"]:
                try:
                    if isinstance(service_value, float):
                        value = float(value)
                    elif isinstance(service_value, int):
                        value = int(value)
                except (ValueError, TypeError):
                    continue

            # Apply operator logic
            if operator == "equals":
                # Case-insensitive for strings
                if isinstance(service_value, str) and isinstance(value, str):
                    if service_value.lower() == value.lower():
                        results.append(service)
                # Contains check for lists
                elif isinstance(service_value, list) and isinstance(value, str):
                    if any(item.lower() == value.lower() for item in service_value if isinstance(item, str)):
                        results.append(service)
                # Exact match for other types
                elif service_value == value:
                    results.append(service)

            elif operator == "greater_than":
                if isinstance(service_value, (int, float)) and service_value > value:
                    results.append(service)

            elif operator == "less_than":
                if isinstance(service_value, (int, float)) and service_value < value:
                    results.append(service)

            elif operator == "greater_equal":
                if isinstance(service_value, (int, float)) and service_value >= value:
                    results.append(service)

            elif operator == "less_equal":
                if isinstance(service_value, (int, float)) and service_value <= value:
                    results.append(service)

            elif operator == "contains":
                # For string fields, check if value is substring
                if isinstance(service_value, str) and isinstance(value, str):
                    if value.lower() in service_value.lower():
                        results.append(service)
                # For lists, check if value is in list (case-insensitive)
                elif isinstance(service_value, list) and isinstance(value, str):
                    if any(value.lower() in str(item).lower() for item in service_value):
                        results.append(service)

        return results


services_service = ServicesService()

@tool
def search_services_tool(key: str, value: str, operator: str = "equals") -> list[dict]:
    """Search for services/microservices based on a key-value pair with optional comparison operators.

    Service Structure:
    - id: Service ID (e.g., "svc-001")
    - name: Service name (e.g., "payments-service", "auth-service")
    - type: Service type (e.g., "microservice", "web-application", "gateway", "infrastructure", "api")
    - description: Service description
    - repository: Git repository path
    - tech_stack: List of technologies used (e.g., ["Python", "Django", "PostgreSQL"])
    - owner_team: Team that owns the service (e.g., "Backend", "Frontend", "DevOps")
    - primary_maintainer: Main maintainer's username
    - status: Service status (e.g., "production", "staging", "deprecated")
    - uptime_percentage: Service uptime percentage (numeric, e.g., 99.5)
    - avg_response_time_ms: Average response time in milliseconds (numeric)
    - request_per_day: Daily request count (numeric)
    - production_url: Production URL
    - staging_url: Staging URL
    - current_version: Current version (e.g., "v1.4.2")
    - deployment_frequency: How often deployed (e.g., "weekly", "bi-weekly", "monthly", "daily")
    - last_deployment: ISO format date string of last deployment
    - dependencies: List of service dependencies
    - monitoring_dashboard: Grafana dashboard URL
    - documentation: Documentation URL

    Args:
        key: The service field to search by. Common fields: 'name', 'type', 'owner_team', 'primary_maintainer', 'status', 'tech_stack', 'uptime_percentage'
        value: The value to search for (e.g., 'Backend', 'ahmed_ali', 'production', 'Python')
        operator: Comparison operator - 'equals', 'greater_than', 'less_than', 'greater_equal', 'less_equal', 'contains'

    Returns:
        List of matching services with their details

    Examples:
        - To find Backend team services: key='owner_team', value='Backend', operator='equals'
        - To find services maintained by ahmed_ali: key='primary_maintainer', value='ahmed_ali', operator='equals'
        - To find services with uptime > 99%: key='uptime_percentage', value='99', operator='greater_than'
        - To find Python services: key='tech_stack', value='Python', operator='equals'
        - To find microservices: key='type', value='microservice', operator='equals'
        - To find payment-related services: key='name', value='payment', operator='contains'
        - To find services with slow response time: key='avg_response_time_ms', value='150', operator='greater_than'
    """
    services = services_service.search_by_key_with_operator(key, value, operator)
    return [vars(service) for service in services]
