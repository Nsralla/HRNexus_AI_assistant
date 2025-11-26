import json
import os
from dataclasses import dataclass, field
from typing import Any
from langchain_core.tools import tool

@dataclass
class Project:
    id: str = ""
    name: str = ""
    key: str = ""
    description: str = ""
    status: str = ""
    lead: str = ""
    team: list[str] = field(default_factory=list)
    start_date: str = ""
    target_completion: str = ""
    progress_percentage: int = 0
    budget_hours: int = 0
    consumed_hours: int = 0
    epics: list[str] = field(default_factory=list)
    repositories: list[str] = field(default_factory=list)
    tech_stack: list[str] = field(default_factory=list)
    priority: str = ""


class ProjectsService:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.projects = []
        self.read_projects_from_json()

    def read_projects_from_json(self):
        try:
            with open(f"{self.path}/../sources/Json_files/projects.json", "r") as f:
                data = json.load(f)
                for d in data:
                    project = Project()
                    project.id = d.get("id", "")
                    project.name = d.get("name", "")
                    project.key = d.get("key", "")
                    project.description = d.get("description", "")
                    project.status = d.get("status", "")
                    project.lead = d.get("lead", "")
                    project.team = d.get("team", [])
                    project.start_date = d.get("start_date", "")
                    project.target_completion = d.get("target_completion", "")
                    project.progress_percentage = d.get("progress_percentage", 0)
                    project.budget_hours = d.get("budget_hours", 0)
                    project.consumed_hours = d.get("consumed_hours", 0)
                    project.epics = d.get("epics", [])
                    project.repositories = d.get("repositories", [])
                    project.tech_stack = d.get("tech_stack", [])
                    project.priority = d.get("priority", "")
                    self.projects.append(project)
        except Exception as e:
            print(f"Error loading projects: {e}")

    def search_by_key_with_operator(self, key: str, value: Any, operator: str = "equals") -> list[Project]:
        """Search projects by key with comparison operators."""
        results = []

        for project in self.projects:
            project_value = getattr(project, key)

            # Convert value to appropriate type for numeric comparisons
            if operator in ["greater_than", "less_than", "greater_equal", "less_equal"]:
                try:
                    value = int(value) if isinstance(project_value, int) else float(value)
                except (ValueError, TypeError):
                    continue

            # Apply operator logic
            if operator == "equals":
                # Case-insensitive for strings
                if isinstance(project_value, str) and isinstance(value, str):
                    if project_value.lower() == value.lower():
                        results.append(project)
                # Contains check for lists
                elif isinstance(project_value, list) and isinstance(value, str):
                    if any(item.lower() == value.lower() for item in project_value if isinstance(item, str)):
                        results.append(project)
                # Exact match for other types
                elif project_value == value:
                    results.append(project)

            elif operator == "greater_than":
                if isinstance(project_value, (int, float)) and project_value > value:
                    results.append(project)

            elif operator == "less_than":
                if isinstance(project_value, (int, float)) and project_value < value:
                    results.append(project)

            elif operator == "greater_equal":
                if isinstance(project_value, (int, float)) and project_value >= value:
                    results.append(project)

            elif operator == "less_equal":
                if isinstance(project_value, (int, float)) and project_value <= value:
                    results.append(project)

            elif operator == "contains":
                # For string fields, check if value is substring
                if isinstance(project_value, str) and isinstance(value, str):
                    if value.lower() in project_value.lower():
                        results.append(project)
                # For lists, check if value is in list (case-insensitive)
                elif isinstance(project_value, list) and isinstance(value, str):
                    if any(value.lower() in str(item).lower() for item in project_value):
                        results.append(project)

        return results


projects_service = ProjectsService()

@tool
def search_projects_tool(key: str, value: str, operator: str = "equals") -> list[dict]:
    """Search for projects based on a key-value pair with optional comparison operators.

    Project Structure:
    - id: Project ID (e.g., "proj-001")
    - name: Project name (e.g., "Payment Gateway Integration")
    - key: Project key/abbreviation (e.g., "PAY", "FEM")
    - description: Detailed project description
    - status: Project status (e.g., "active", "completed", "on-hold", "planning")
    - lead: Username of project lead (e.g., "ahmed_ali")
    - team: List of team member usernames
    - start_date: ISO format date string
    - target_completion: ISO format date string
    - progress_percentage: Progress percentage (0-100, numeric)
    - budget_hours: Budgeted hours (numeric)
    - consumed_hours: Hours consumed so far (numeric)
    - epics: List of epic names associated with project
    - repositories: List of repository paths
    - tech_stack: List of technologies used (e.g., ["Python", "Django", "PostgreSQL"])
    - priority: Priority level (e.g., "High", "Medium", "Low")

    Args:
        key: The project field to search by. Common fields: 'status', 'lead', 'priority', 'team', 'tech_stack', 'progress_percentage', 'name'
        value: The value to search for (e.g., 'active', 'ahmed_ali', 'High', 'Python', '50')
        operator: Comparison operator - 'equals', 'greater_than', 'less_than', 'greater_equal', 'less_equal', 'contains'

    Returns:
        List of matching projects with their details

    Examples:
        - To find active projects: key='status', value='active', operator='equals'
        - To find projects led by ahmed_ali: key='lead', value='ahmed_ali', operator='equals'
        - To find high priority projects: key='priority', value='High', operator='equals'
        - To find projects using Python: key='tech_stack', value='Python', operator='contains'
        - To find projects with more than 50% progress: key='progress_percentage', value='50', operator='greater_than'
        - To find projects with specific team member: key='team', value='leen_q', operator='contains'
    """
    projects = projects_service.search_by_key_with_operator(key, value, operator)
    return [vars(project) for project in projects]
