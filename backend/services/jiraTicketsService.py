import json
import os
from dataclasses import dataclass, field
from typing import Any
from langchain_core.tools import tool

@dataclass
class JiraTicket:
    id: str = ""
    summary: str = ""
    description: str = ""
    assignee: str = ""
    reporter: str = ""
    status: str = ""
    priority: str = ""
    story_points: int = 0
    sprint: str = ""
    epic: str = ""
    labels: list[str] = field(default_factory=list)
    created_date: str = ""
    updated_date: str = ""
    due_date: str = ""
    component: str = ""
    estimated_hours: int = 0
    time_spent_hours: int = 0
    blocked: bool = False
    blocker_reason: str = None
    linked_tickets: list[str] = field(default_factory=list)
    comments_count: int = 0


class JiraTicketsService:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.tickets = []
        self.read_tickets_from_json()

    def read_tickets_from_json(self):
        try:
            with open(f"{self.path}/../sources/Json_files/jira_tickets.json", "r") as f:
                data = json.load(f)
                for d in data:
                    ticket = JiraTicket()
                    ticket.id = d.get("id", "")
                    ticket.summary = d.get("summary", "")
                    ticket.description = d.get("description", "")
                    ticket.assignee = d.get("assignee", "")
                    ticket.reporter = d.get("reporter", "")
                    ticket.status = d.get("status", "")
                    ticket.priority = d.get("priority", "")
                    ticket.story_points = d.get("story_points", 0)
                    ticket.sprint = d.get("sprint", "")
                    ticket.epic = d.get("epic", "")
                    ticket.labels = d.get("labels", [])
                    ticket.created_date = d.get("created_date", "")
                    ticket.updated_date = d.get("updated_date", "")
                    ticket.due_date = d.get("due_date", "")
                    ticket.component = d.get("component", "")
                    ticket.estimated_hours = d.get("estimated_hours", 0)
                    ticket.time_spent_hours = d.get("time_spent_hours", 0)
                    ticket.blocked = d.get("blocked", False)
                    ticket.blocker_reason = d.get("blocker_reason")
                    ticket.linked_tickets = d.get("linked_tickets", [])
                    ticket.comments_count = d.get("comments_count", 0)
                    self.tickets.append(ticket)
        except Exception as e:
            print(f"Error loading JIRA tickets: {e}")

    def search_by_key_with_operator(self, key: str, value: Any, operator: str = "equals") -> list[JiraTicket]:
        """Search JIRA tickets by key with comparison operators."""
        results = []

        for ticket in self.tickets:
            ticket_value = getattr(ticket, key)

            # Convert value to appropriate type for numeric comparisons
            if operator in ["greater_than", "less_than", "greater_equal", "less_equal"]:
                try:
                    value = int(value) if isinstance(ticket_value, int) else float(value)
                except (ValueError, TypeError):
                    continue

            # Apply operator logic
            if operator == "equals":
                # Case-insensitive for strings
                if isinstance(ticket_value, str) and isinstance(value, str):
                    if ticket_value.lower() == value.lower():
                        results.append(ticket)
                # Contains check for lists
                elif isinstance(ticket_value, list) and isinstance(value, str):
                    if any(item.lower() == value.lower() for item in ticket_value if isinstance(item, str)):
                        results.append(ticket)
                # Exact match for other types
                elif ticket_value == value:
                    results.append(ticket)

            elif operator == "greater_than":
                if isinstance(ticket_value, (int, float)) and ticket_value > value:
                    results.append(ticket)

            elif operator == "less_than":
                if isinstance(ticket_value, (int, float)) and ticket_value < value:
                    results.append(ticket)

            elif operator == "greater_equal":
                if isinstance(ticket_value, (int, float)) and ticket_value >= value:
                    results.append(ticket)

            elif operator == "less_equal":
                if isinstance(ticket_value, (int, float)) and ticket_value <= value:
                    results.append(ticket)

            elif operator == "contains":
                # For string fields, check if value is substring
                if isinstance(ticket_value, str) and isinstance(value, str):
                    if value.lower() in ticket_value.lower():
                        results.append(ticket)
                # For lists, check if value is in list (case-insensitive)
                elif isinstance(ticket_value, list) and isinstance(value, str):
                    if any(value.lower() in str(item).lower() for item in ticket_value):
                        results.append(ticket)

        return results


tickets_service = JiraTicketsService()

@tool
def search_jira_tickets_tool(key: str, value: str, operator: str = "equals") -> list[dict]:
    """Search for JIRA tickets based on a key-value pair with optional comparison operators.

    JIRA Ticket Structure:
    - id: Ticket ID (e.g., "HARRI-123")
    - summary: Short description of the ticket
    - description: Detailed description
    - assignee: Username of person assigned (e.g., "ahmed_ali")
    - reporter: Username of person who reported the issue
    - status: Ticket status (e.g., "Open", "In Progress", "Closed")
    - priority: Priority level (e.g., "High", "Medium", "Low", "Critical")
    - story_points: Numeric story points (e.g., 5, 8, 13)
    - sprint: Sprint name (e.g., "Sprint 24", "Sprint 25")
    - epic: Epic name (e.g., "Onboarding Improvements", "DevOps Excellence")
    - labels: List of labels (e.g., ["bug", "backend", "authentication"])
    - created_date: ISO format date string
    - updated_date: ISO format date string
    - due_date: ISO format date string
    - component: Component name (e.g., "onboarding-service", "backend-api")
    - estimated_hours: Estimated hours (numeric)
    - time_spent_hours: Time spent in hours (numeric)
    - blocked: Boolean indicating if ticket is blocked
    - blocker_reason: Reason for blocking (string or null)
    - linked_tickets: List of linked ticket IDs
    - comments_count: Number of comments (numeric)

    Args:
        key: The ticket field to search by. Common fields: 'status', 'priority', 'assignee', 'sprint', 'epic', 'component', 'blocked', 'story_points', 'labels'
        value: The value to search for (e.g., 'Open', 'ahmed_ali', 'Sprint 24', '5')
        operator: Comparison operator - 'equals', 'greater_than', 'less_than', 'greater_equal', 'less_equal', 'contains'

    Returns:
        List of matching JIRA tickets with their details

    Examples:
        - To find open tickets: key='status', value='Open', operator='equals'
        - To find tickets assigned to ahmed_ali: key='assignee', value='ahmed_ali', operator='equals'
        - To find high priority tickets: key='priority', value='High', operator='equals'
        - To find tickets in Sprint 24: key='sprint', value='Sprint 24', operator='equals'
        - To find blocked tickets: key='blocked', value='True', operator='equals'
        - To find tickets with more than 5 story points: key='story_points', value='5', operator='greater_than'
        - To find tickets with bug label: key='labels', value='bug', operator='contains'
    """
    tickets = tickets_service.search_by_key_with_operator(key, value, operator)
    return [vars(ticket) for ticket in tickets]
