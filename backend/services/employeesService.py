import json
import os
from dataclasses import dataclass
from typing import Any
from langchain_core.tools import tool

@dataclass
class Employee:
    id: int = 0
    name: str = ""
    email: str = ""
    role: str = ""
    team: str = ""
    jira_username: str = ""
    skills: list[str] = None
    years_of_experience: int = 0
    location: str = ""
    timezone: str = ""
    github_username: str = ""
    availability: str = ""
    current_sprint_capacity: int = 0
    current_sprint_allocated: int = 0
    slack_handle: str = ""

    def __post_init__(self):
        if self.skills is None:
            self.skills = []



class EmployeeService:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.emps = []
        self.read_employees_from_json()

    def read_employees_from_json(self):
        try:
            with open(f"{self.path}/../sources/employees.json", "r") as f:
                data = json.load(f)
                for d in data:
                    e = Employee()
                    e.id = d["id"]
                    e.name = d["name"]
                    e.email = d["email"]
                    e.role = d["role"]
                    e.team = d["team"]
                    e.jira_username = d["jira_username"]
                    e.skills = d["skills"]
                    e.years_of_experience = d["years_of_experience"]
                    e.location = d["location"]
                    e.timezone = d["timezone"]
                    e.github_username = d["github_username"]
                    e.availability = d["availability"]
                    e.current_sprint_capacity = d["current_sprint_capacity"]
                    e.current_sprint_allocated = d["current_sprint_allocated"]
                    e.slack_handle = d["slack_handle"]
                    self.emps.append(e)
        except Exception as e:
            print(e)

    def search_emps_by_key(self, key: str, value: Any) -> list[Employee]:
        """Search employees by key with case-insensitive string matching."""
        results = []
        for emp in self.emps:
            emp_value = getattr(emp, key)
            # Case-insensitive comparison for strings
            if isinstance(emp_value, str) and isinstance(value, str):
                if emp_value.lower() == value.lower():
                    results.append(emp)
            # For lists (like skills), check if value is in the list (case-insensitive)
            elif isinstance(emp_value, list) and isinstance(value, str):
                if any(item.lower() == value.lower() for item in emp_value if isinstance(item, str)):
                    results.append(emp)
            # Exact match for other types (int, bool, etc.)
            elif emp_value == value:
                results.append(emp)
        return results

    def search_emps_by_key_with_operator(self, key: str, value: Any, operator: str = "equals") -> list[Employee]:
        """Search employees by key with comparison operators."""
        results = []

        for emp in self.emps:
            emp_value = getattr(emp, key)

            # Convert value to appropriate type for numeric comparisons
            if operator in ["greater_than", "less_than", "greater_equal", "less_equal"]:
                try:
                    value = int(value) if isinstance(emp_value, int) else float(value)
                except (ValueError, TypeError):
                    continue

            # Apply operator logic
            if operator == "equals":
                # Case-insensitive for strings
                if isinstance(emp_value, str) and isinstance(value, str):
                    if emp_value.lower() == value.lower():
                        results.append(emp)
                # Contains check for lists
                elif isinstance(emp_value, list) and isinstance(value, str):
                    if any(item.lower() == value.lower() for item in emp_value if isinstance(item, str)):
                        results.append(emp)
                # Exact match for other types
                elif emp_value == value:
                    results.append(emp)

            elif operator == "greater_than":
                if isinstance(emp_value, (int, float)) and emp_value > value:
                    results.append(emp)

            elif operator == "less_than":
                if isinstance(emp_value, (int, float)) and emp_value < value:
                    results.append(emp)

            elif operator == "greater_equal":
                if isinstance(emp_value, (int, float)) and emp_value >= value:
                    results.append(emp)

            elif operator == "less_equal":
                if isinstance(emp_value, (int, float)) and emp_value <= value:
                    results.append(emp)

            elif operator == "contains":
                # For string fields, check if value is substring
                if isinstance(emp_value, str) and isinstance(value, str):
                    if value.lower() in emp_value.lower():
                        results.append(emp)
                # For lists, check if value is in list (case-insensitive)
                elif isinstance(emp_value, list) and isinstance(value, str):
                    if any(value.lower() in str(item).lower() for item in emp_value):
                        results.append(emp)

        return results
    

emps_service = EmployeeService()

@tool
def search_emps_by_key_tool(key: str, value: str, operator: str = "equals") -> list[dict]:
    """Search for employees based on a key-value pair with optional comparison operators.

    Employee Structure:
    - id: Employee ID number
    - name: Full name of the employee
    - email: Email address
    - role: Job title (e.g., "Backend Lead", "Frontend Engineer", "DevOps Engineer")
    - team: Department/team name (e.g., "Backend", "Frontend", "DevOps", "QA", "Management")
    - jira_username: JIRA username
    - skills: List of technical skills (e.g., ["Python", "Django", "PostgreSQL"])
    - years_of_experience: Years of professional experience (numeric)
    - location: Physical location (e.g., "Amman, Jordan", "Dubai, UAE")
    - timezone: Timezone (e.g., "Asia/Amman")
    - github_username: GitHub username
    - availability: Work availability status (e.g., "Full-time")
    - current_sprint_capacity: Sprint capacity hours (numeric)
    - current_sprint_allocated: Allocated sprint hours (numeric)
    - slack_handle: Slack handle

    Args:
        key: The employee field to search by. Common fields: 'role', 'team', 'skills', 'location', 'name', 'availability', 'years_of_experience', 'current_sprint_capacity'
        value: The value to search for (e.g., 'Backend', 'Python', 'Amman', '5')
        operator: Comparison operator - 'equals', 'greater_than', 'less_than', 'greater_equal', 'less_equal', 'contains'

    Returns:
        List of matching employees with their details

    Examples:
        - To find backend team members: key='team', value='Backend', operator='equals'
        - To find employees with Python skills: key='skills', value='Python', operator='contains'
        - To find employees with more than 5 years experience: key='years_of_experience', value='5', operator='greater_than'
        - To find employees with capacity >= 40: key='current_sprint_capacity', value='40', operator='greater_equal'
    """
    employees = emps_service.search_emps_by_key_with_operator(key, value, operator)
    return [vars(emp) for emp in employees]


        
