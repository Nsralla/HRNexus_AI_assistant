import json
import os
from dataclasses import dataclass, field
from typing import Any
from langchain_core.tools import tool

@dataclass
class Sprint:
    id: str = ""
    name: str = ""
    start_date: str = ""
    end_date: str = ""
    status: str = ""
    goal: str = ""
    total_story_points: int = 0
    completed_story_points: int = 0
    team_velocity: int = 0
    tickets: list[str] = field(default_factory=list)
    burndown: list[dict] = field(default_factory=list)
    retrospective_notes: str = None


class SprintsService:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.sprints = []
        self.read_sprints_from_json()

    def read_sprints_from_json(self):
        try:
            with open(f"{self.path}/../sources/Json_files/sprints.json", "r") as f:
                data = json.load(f)
                for d in data:
                    sprint = Sprint()
                    sprint.id = d.get("id", "")
                    sprint.name = d.get("name", "")
                    sprint.start_date = d.get("start_date", "")
                    sprint.end_date = d.get("end_date", "")
                    sprint.status = d.get("status", "")
                    sprint.goal = d.get("goal", "")
                    sprint.total_story_points = d.get("total_story_points", 0)
                    sprint.completed_story_points = d.get("completed_story_points", 0)
                    sprint.team_velocity = d.get("team_velocity", 0)
                    sprint.tickets = d.get("tickets", [])
                    sprint.burndown = d.get("burndown", [])
                    sprint.retrospective_notes = d.get("retrospective_notes")
                    self.sprints.append(sprint)
        except Exception as e:
            print(f"Error loading sprints: {e}")

    def search_by_key_with_operator(self, key: str, value: Any, operator: str = "equals") -> list[Sprint]:
        """Search sprints by key with comparison operators."""
        results = []

        for sprint in self.sprints:
            sprint_value = getattr(sprint, key)

            # Convert value to appropriate type for numeric comparisons
            if operator in ["greater_than", "less_than", "greater_equal", "less_equal"]:
                try:
                    value = int(value) if isinstance(sprint_value, int) else float(value)
                except (ValueError, TypeError):
                    continue

            # Apply operator logic
            if operator == "equals":
                # Case-insensitive for strings
                if isinstance(sprint_value, str) and isinstance(value, str):
                    if sprint_value.lower() == value.lower():
                        results.append(sprint)
                # Contains check for lists
                elif isinstance(sprint_value, list) and isinstance(value, str):
                    if any(item.lower() == value.lower() for item in sprint_value if isinstance(item, str)):
                        results.append(sprint)
                # Exact match for other types
                elif sprint_value == value:
                    results.append(sprint)

            elif operator == "greater_than":
                if isinstance(sprint_value, (int, float)) and sprint_value > value:
                    results.append(sprint)

            elif operator == "less_than":
                if isinstance(sprint_value, (int, float)) and sprint_value < value:
                    results.append(sprint)

            elif operator == "greater_equal":
                if isinstance(sprint_value, (int, float)) and sprint_value >= value:
                    results.append(sprint)

            elif operator == "less_equal":
                if isinstance(sprint_value, (int, float)) and sprint_value <= value:
                    results.append(sprint)

            elif operator == "contains":
                # For string fields, check if value is substring
                if isinstance(sprint_value, str) and isinstance(value, str):
                    if value.lower() in sprint_value.lower():
                        results.append(sprint)
                # For lists, check if value is in list (case-insensitive)
                elif isinstance(sprint_value, list) and isinstance(value, str):
                    if any(value.lower() in str(item).lower() for item in sprint_value):
                        results.append(sprint)

        return results


sprints_service = SprintsService()

@tool
def search_sprints_tool(key: str, value: str, operator: str = "equals") -> list[dict]:
    """Search for sprints based on a key-value pair with optional comparison operators.

    Sprint Structure:
    - id: Sprint ID (e.g., "sprint-24")
    - name: Sprint name (e.g., "Sprint 24")
    - start_date: ISO format date string
    - end_date: ISO format date string
    - status: Sprint status (e.g., "active", "completed", "planned")
    - goal: Sprint goal/objective description
    - total_story_points: Total story points planned (numeric)
    - completed_story_points: Story points completed so far (numeric)
    - team_velocity: Team velocity metric (numeric)
    - tickets: List of JIRA ticket IDs in this sprint
    - burndown: List of burndown data points with date and remaining_points
    - retrospective_notes: Retrospective notes (string or null)

    Args:
        key: The sprint field to search by. Common fields: 'name', 'status', 'total_story_points', 'completed_story_points', 'team_velocity', 'tickets'
        value: The value to search for (e.g., 'Sprint 24', 'active', '50', 'HARRI-123')
        operator: Comparison operator - 'equals', 'greater_than', 'less_than', 'greater_equal', 'less_equal', 'contains'

    Returns:
        List of matching sprints with their details

    Examples:
        - To find active sprint: key='status', value='active', operator='equals'
        - To find Sprint 24: key='name', value='Sprint 24', operator='equals'
        - To find sprints with more than 80 story points: key='total_story_points', value='80', operator='greater_than'
        - To find sprints containing specific ticket: key='tickets', value='HARRI-123', operator='contains'
        - To find completed sprints: key='status', value='completed', operator='equals'
        - To find sprints with high velocity: key='team_velocity', value='80', operator='greater_equal'
    """
    sprints = sprints_service.search_by_key_with_operator(key, value, operator)
    return [vars(sprint) for sprint in sprints]
