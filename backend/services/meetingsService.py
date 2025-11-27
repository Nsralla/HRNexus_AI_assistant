import json
import os
from dataclasses import dataclass, field
from typing import Any
from langchain_core.tools import tool

@dataclass
class Meeting:
    id: str = ""
    title: str = ""
    type: str = ""
    date: str = ""
    duration_minutes: int = 0
    attendees: list[str] = field(default_factory=list)
    agenda: list[str] = field(default_factory=list)
    notes: str = ""
    action_items: list[dict] = field(default_factory=list)


class MeetingsService:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.meetings = []
        self.read_meetings_from_json()

    def read_meetings_from_json(self):
        try:
            with open(f"{self.path}/../sources/Json_files/meetings.json", "r") as f:
                data = json.load(f)
                for d in data:
                    meeting = Meeting()
                    meeting.id = d.get("id", "")
                    meeting.title = d.get("title", "")
                    meeting.type = d.get("type", "")
                    meeting.date = d.get("date", "")
                    meeting.duration_minutes = d.get("duration_minutes", 0)
                    meeting.attendees = d.get("attendees", [])
                    meeting.agenda = d.get("agenda", [])
                    meeting.notes = d.get("notes", "")
                    meeting.action_items = d.get("action_items", [])
                    self.meetings.append(meeting)
        except Exception as e:
            print(f"Error loading meetings: {e}")

    def search_by_key_with_operator(self, key: str, value: Any, operator: str = "equals") -> list[Meeting]:
        """Search meetings by key with comparison operators."""
        results = []

        for meeting in self.meetings:
            meeting_value = getattr(meeting, key)

            # Convert value to appropriate type for numeric comparisons
            if operator in ["greater_than", "less_than", "greater_equal", "less_equal"]:
                try:
                    value = int(value) if isinstance(meeting_value, int) else float(value)
                except (ValueError, TypeError):
                    continue

            # Apply operator logic
            if operator == "equals":
                # Case-insensitive for strings
                if isinstance(meeting_value, str) and isinstance(value, str):
                    if meeting_value.lower() == value.lower():
                        results.append(meeting)
                # Contains check for lists
                elif isinstance(meeting_value, list) and isinstance(value, str):
                    if any(item.lower() == value.lower() for item in meeting_value if isinstance(item, str)):
                        results.append(meeting)
                # Exact match for other types
                elif meeting_value == value:
                    results.append(meeting)

            elif operator == "greater_than":
                if isinstance(meeting_value, (int, float)) and meeting_value > value:
                    results.append(meeting)

            elif operator == "less_than":
                if isinstance(meeting_value, (int, float)) and meeting_value < value:
                    results.append(meeting)

            elif operator == "greater_equal":
                if isinstance(meeting_value, (int, float)) and meeting_value >= value:
                    results.append(meeting)

            elif operator == "less_equal":
                if isinstance(meeting_value, (int, float)) and meeting_value <= value:
                    results.append(meeting)

            elif operator == "contains":
                # For string fields, check if value is substring
                if isinstance(meeting_value, str) and isinstance(value, str):
                    if value.lower() in meeting_value.lower():
                        results.append(meeting)
                # For lists, check if value is in list (case-insensitive)
                elif isinstance(meeting_value, list) and isinstance(value, str):
                    if any(value.lower() in str(item).lower() for item in meeting_value):
                        results.append(meeting)

        return results


meetings_service = MeetingsService()

@tool
def search_meetings_tool(key: str, value: str, operator: str = "equals") -> list[dict]:
    """Search for meetings based on a key-value pair with optional comparison operators.

    Meeting Structure:
    - id: Meeting ID (e.g., "meet-001")
    - title: Meeting title (e.g., "Sprint 24 Planning")
    - type: Meeting type (e.g., "sprint-planning", "retrospective", "standup", "technical", "security", "team-sync", "post-mortem")
    - date: ISO format date string
    - duration_minutes: Meeting duration in minutes (numeric)
    - attendees: List of employee usernames who attended
    - agenda: List of agenda items
    - notes: Meeting notes and summary
    - action_items: List of action items with assigned_to, item, and due_date

    Args:
        key: The meeting field to search by. Common fields: 'title', 'type', 'attendees', 'date', 'duration_minutes'
        value: The value to search for (e.g., 'sprint-planning', 'noor_j', '2025-07-05')
        operator: Comparison operator - 'equals', 'greater_than', 'less_than', 'greater_equal', 'less_equal', 'contains'

    Returns:
        List of matching meetings with their details

    Examples:
        - To find sprint planning meetings: key='type', value='sprint-planning', operator='equals'
        - To find meetings with specific attendee: key='attendees', value='ahmed_ali', operator='equals'
        - To find meetings longer than 60 minutes: key='duration_minutes', value='60', operator='greater_than'
        - To find meetings about security: key='title', value='security', operator='contains'
        - To find retrospective meetings: key='type', value='retrospective', operator='equals'
        - To find meetings on specific date: key='date', value='2025-07-05', operator='contains'
    """
    meetings = meetings_service.search_by_key_with_operator(key, value, operator)
    return [vars(meeting) for meeting in meetings]
