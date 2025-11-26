import json
import os
from dataclasses import dataclass, field
from typing import Any
from langchain_core.tools import tool

@dataclass
class Deployment:
    id: str = ""
    service: str = ""
    version: str = ""
    date: str = ""
    status: str = ""
    environment: str = ""
    deployed_by: str = ""
    duration_minutes: int = 0
    rollback_available: bool = False
    health_check_passed: bool = False
    commit_sha: str = ""
    jira_tickets: list[str] = field(default_factory=list)
    notes: str = ""
    error_message: str = None


class DeploymentsService:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.deployments = []
        self.read_deployments_from_json()

    def read_deployments_from_json(self):
        try:
            with open(f"{self.path}/../sources/Json_files/deployments.json", "r") as f:
                data = json.load(f)
                for d in data:
                    deployment = Deployment()
                    deployment.id = d.get("id", "")
                    deployment.service = d.get("service", "")
                    deployment.version = d.get("version", "")
                    deployment.date = d.get("date", "")
                    deployment.status = d.get("status", "")
                    deployment.environment = d.get("environment", "")
                    deployment.deployed_by = d.get("deployed_by", "")
                    deployment.duration_minutes = d.get("duration_minutes", 0)
                    deployment.rollback_available = d.get("rollback_available", False)
                    deployment.health_check_passed = d.get("health_check_passed", False)
                    deployment.commit_sha = d.get("commit_sha", "")
                    deployment.jira_tickets = d.get("jira_tickets", [])
                    deployment.notes = d.get("notes", "")
                    deployment.error_message = d.get("error_message")
                    self.deployments.append(deployment)
        except Exception as e:
            print(f"Error loading deployments: {e}")

    def search_by_key_with_operator(self, key: str, value: Any, operator: str = "equals") -> list[Deployment]:
        """Search deployments by key with comparison operators."""
        results = []

        for deployment in self.deployments:
            deployment_value = getattr(deployment, key)

            # Convert value to appropriate type for numeric comparisons
            if operator in ["greater_than", "less_than", "greater_equal", "less_equal"]:
                try:
                    value = int(value) if isinstance(deployment_value, int) else float(value)
                except (ValueError, TypeError):
                    continue

            # Apply operator logic
            if operator == "equals":
                # Case-insensitive for strings
                if isinstance(deployment_value, str) and isinstance(value, str):
                    if deployment_value.lower() == value.lower():
                        results.append(deployment)
                # Contains check for lists
                elif isinstance(deployment_value, list) and isinstance(value, str):
                    if any(item.lower() == value.lower() for item in deployment_value if isinstance(item, str)):
                        results.append(deployment)
                # Exact match for other types (bool, int)
                elif deployment_value == value or str(deployment_value).lower() == str(value).lower():
                    results.append(deployment)

            elif operator == "greater_than":
                if isinstance(deployment_value, (int, float)) and deployment_value > value:
                    results.append(deployment)

            elif operator == "less_than":
                if isinstance(deployment_value, (int, float)) and deployment_value < value:
                    results.append(deployment)

            elif operator == "greater_equal":
                if isinstance(deployment_value, (int, float)) and deployment_value >= value:
                    results.append(deployment)

            elif operator == "less_equal":
                if isinstance(deployment_value, (int, float)) and deployment_value <= value:
                    results.append(deployment)

            elif operator == "contains":
                # For string fields, check if value is substring
                if isinstance(deployment_value, str) and isinstance(value, str):
                    if value.lower() in deployment_value.lower():
                        results.append(deployment)
                # For lists, check if value is in list (case-insensitive)
                elif isinstance(deployment_value, list) and isinstance(value, str):
                    if any(value.lower() in str(item).lower() for item in deployment_value):
                        results.append(deployment)

        return results


deployments_service = DeploymentsService()

@tool
def search_deployments_tool(key: str, value: str, operator: str = "equals") -> list[dict]:
    """Search for deployments based on a key-value pair with optional comparison operators.

    Deployment Structure:
    - id: Deployment ID (e.g., "deploy-001")
    - service: Service name (e.g., "payments", "onboarding", "backend", "frontend")
    - version: Version number (e.g., "v1.4.2")
    - date: ISO format date string (e.g., "2025-07-05T10:30:00Z")
    - status: Deployment status ("Success", "Failed")
    - environment: Environment ("production", "staging")
    - deployed_by: Username of person who deployed (e.g., "adam_s", "lina_s")
    - duration_minutes: Deployment duration in minutes (numeric)
    - rollback_available: Boolean indicating if rollback is available
    - health_check_passed: Boolean indicating if health checks passed
    - commit_sha: Git commit SHA hash
    - jira_tickets: List of related JIRA ticket IDs
    - notes: Deployment notes/comments
    - error_message: Error message if deployment failed (string or null)

    Args:
        key: The deployment field to search by. Common fields: 'service', 'status', 'environment', 'deployed_by', 'health_check_passed', 'duration_minutes', 'jira_tickets'
        value: The value to search for (e.g., 'payments', 'Success', 'production', 'adam_s', 'True', '10')
        operator: Comparison operator - 'equals', 'greater_than', 'less_than', 'greater_equal', 'less_equal', 'contains'

    Returns:
        List of matching deployments with their details

    Examples:
        - To find successful deployments: key='status', value='Success', operator='equals'
        - To find production deployments: key='environment', value='production', operator='equals'
        - To find deployments by adam_s: key='deployed_by', value='adam_s', operator='equals'
        - To find failed deployments: key='status', value='Failed', operator='equals'
        - To find payments service deployments: key='service', value='payments', operator='equals'
        - To find deployments longer than 10 minutes: key='duration_minutes', value='10', operator='greater_than'
        - To find deployments with health checks passed: key='health_check_passed', value='True', operator='equals'
    """
    deployments = deployments_service.search_by_key_with_operator(key, value, operator)
    return [vars(deployment) for deployment in deployments]
