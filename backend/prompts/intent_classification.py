"""
Intent classification prompt for routing user queries.
"""

INTENT_CLASSIFICATION_PROMPT = """Classify the user's query intent into ONE of these categories:

1. "conversation" - For casual interactions:
   - Greetings (hi, hello, hey, good morning, etc.)
   - Identity questions (who are you, what are you, what can you do)
   - Thank you / goodbye messages
   - General chitchat or off-topic questions
   - Questions about the assistant itself

2. "documentation" - For questions about company policies/processes:
   - Policies (code review, escalation, etc.)
   - Processes (deployment, onboarding, etc.)
   - Guides (how-to questions, setup instructions)
   - Team structure and roles
   - General "how do I..." or "what is the process for..." questions

3. "data_query" - For questions requiring specific data:
   - Employees (who, team members, skills, capacity)
   - JIRA tickets (status, assignments, sprints, bugs)
   - Deployments (history, status, versions)
   - Projects (progress, teams, tech stack)
   - Sprints (velocity, story points, burndown)
   - Services/Microservices (status, uptime, performance, tech stack, ownership)
   - Meetings (sprint planning, retrospectives, standups, attendees, action items)

User Query: {user_query}

Respond with ONLY one word: "conversation", "documentation", or "data_query"."""

