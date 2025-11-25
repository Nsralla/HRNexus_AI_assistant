import os
from dotenv import load_dotenv
from typing import TypedDict
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from .employeesService import search_emps_by_key_tool
load_dotenv()


class StateAgent(TypedDict):
    user_query: str
    intent: str
    chat_history: list[HumanMessage | AIMessage]


class ChatPipeLine:
    def __init__(self):
        self.workflow = StateGraph(StateAgent)
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model="x-ai/grok-4.1-fast"
        )
        self.llm_with_tools = self.llm.bind_tools([search_emps_by_key_tool])
        self.compiled_graph = None
        self.init_graph()


    async def intent_classification(self, state: StateAgent) -> StateAgent:
        prompt = """You are a helpful AI assistant. Classify the user's query intent.

The user may ask about:
1. Static info about the company - respond with "company"
2. Employee data (searching, finding employees by role, team, skills, etc.) - respond with "employees"

User Query: {user_query}

Respond with ONLY one word: either "company" or "employees"."""

        messages = [HumanMessage(content=prompt.format(user_query=state["user_query"]))]
        response = await self.llm.ainvoke(messages)
        state["intent"] = response.content.strip().lower()
        return state


    def intent_routing(self, state: StateAgent) -> str:
        if "company" in state["intent"]:
            return "company_info"
        else:
            return "employees_info"


    def company_info(self, state: StateAgent) -> StateAgent:
        # Skip for now, will be implemented when vector DB is ready.
        state["chat_history"].append(HumanMessage(content=state["user_query"]))
        response_message = "Company information feature is not yet implemented. Please ask about employee data instead."
        state["chat_history"].append(AIMessage(content=response_message))
        return state


    async def employees_info(self, state: StateAgent) -> StateAgent:
        """Handle employee-related queries using tool calling."""
        # Add user query to chat history
        state["chat_history"].append(HumanMessage(content=state["user_query"]))

        # Add system context about available tools
        system_message = HumanMessage(content="""You are an HR assistant that helps find employee information.

When searching for employees, use the search_emps_by_key_tool with appropriate key-value pairs and operators.

Available employee fields:
- team: Department (Backend, Frontend, DevOps, QA, Management)
- role: Job title (Backend Lead, Frontend Engineer, etc.)
- skills: Technical skills (Python, React, Docker, etc.)
- location: Physical location (Amman, Dubai, Cairo, etc.)
- name: Employee name
- availability: Work status (Full-time, Part-time, etc.)
- years_of_experience: Numeric - years of experience
- current_sprint_capacity: Numeric - sprint capacity in hours
- current_sprint_allocated: Numeric - allocated sprint hours

Comparison operators (use the 'operator' parameter):
- equals: Exact match (default) - use for team, role, name, location, availability
- greater_than: > comparison - use for numeric fields (years_of_experience > 5)
- less_than: < comparison - use for numeric fields
- greater_equal: >= comparison - use for numeric fields
- less_equal: <= comparison - use for numeric fields
- contains: Substring/partial match - use for skills or partial name matches

Examples:
- "employees with more than 5 years experience": key='years_of_experience', value='5', operator='greater_than'
- "backend team": key='team', value='Backend', operator='equals'
- "employees who know Python": key='skills', value='Python', operator='contains'

IMPORTANT: When you receive tool results with employee data, use the EXACT information provided.
All employee fields (jira_username, github_username, slack_handle, etc.) are included in the tool results.
Do NOT say information is unavailable if it's present in the tool results.

Always format your response in a clear, professional manner using markdown.
Extract and present the specific information requested by the user.
""")

        # Create messages for the LLM with tool binding
        messages = [system_message] + state["chat_history"].copy()

        # Invoke LLM with tools
        response = await self.llm_with_tools.ainvoke(messages)

        # Check if the model wants to use tools
        if response.tool_calls:
            # Execute tool calls
            for tool_call in response.tool_calls:
                if tool_call["name"] == "search_emps_by_key_tool":
                    key = str(tool_call["args"]["key"])
                    value = str(tool_call["args"]["value"])
                    operator = str(tool_call["args"].get("operator", "equals"))

                    result = search_emps_by_key_tool.invoke({"key": key, "value": value, "operator": operator})
                    # Format the result with all employee details
                    if result:
                        formatted_result = f"Found {len(result)} employee(s):\n\n"
                        for emp in result:
                            formatted_result += f"Name: {emp['name']}\n"
                            formatted_result += f"Role: {emp['role']}\n"
                            formatted_result += f"Team: {emp['team']}\n"
                            formatted_result += f"Email: {emp['email']}\n"
                            formatted_result += f"Jira Username: {emp['jira_username']}\n"
                            formatted_result += f"GitHub: {emp['github_username']}\n"
                            formatted_result += f"Slack: {emp['slack_handle']}\n"
                            formatted_result += f"Location: {emp['location']}\n"
                            formatted_result += f"Timezone: {emp['timezone']}\n"
                            formatted_result += f"Skills: {', '.join(emp['skills'])}\n"
                            formatted_result += f"Years of Experience: {emp['years_of_experience']}\n"
                            formatted_result += f"Availability: {emp['availability']}\n"
                            formatted_result += f"Sprint Capacity: {emp['current_sprint_capacity']}h\n"
                            formatted_result += f"Sprint Allocated: {emp['current_sprint_allocated']}h\n"
                            formatted_result += "\n"
                    else:
                        formatted_result = "No employees found matching your criteria."

                    # Create final response
                    final_messages = messages + [
                        response,
                        HumanMessage(content=f"Tool result: {formatted_result}")
                    ]
                    final_response = await self.llm.ainvoke(final_messages)
                    state["chat_history"].append(AIMessage(content=final_response.content))
        else:
            # No tool call needed, use the direct response
            state["chat_history"].append(AIMessage(content=response.content))

        return state


    def init_graph(self):
        """Initialize and compile the workflow graph."""
        # Add nodes
        self.workflow.add_node("intent_classification", self.intent_classification)
        self.workflow.add_node("company_info", self.company_info)
        self.workflow.add_node("employees_info", self.employees_info)

        # Set entry point
        self.workflow.set_entry_point("intent_classification")

        # Add conditional edges based on intent
        self.workflow.add_conditional_edges(
            "intent_classification",
            self.intent_routing,
            {
                "company_info": "company_info",
                "employees_info": "employees_info"
            }
        )

        # Add edges to END
        self.workflow.add_edge("company_info", END)
        self.workflow.add_edge("employees_info", END)

        # Compile the graph
        self.compiled_graph = self.workflow.compile()

    async def run(self, user_query: str, chat_history: list[dict] = None) -> str:
        """Run the chat pipeline with a user query and optional chat history.

        Args:
            user_query: The current user query
            chat_history: List of previous messages in format [{"role": "user/assistant", "content": "..."}]
        """
        # Convert chat history to LangChain message format
        langchain_history = []
        if chat_history:
            for msg in chat_history[:-1]:  # Exclude the current message (last one)
                if msg["role"] == "user":
                    langchain_history.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    langchain_history.append(AIMessage(content=msg["content"]))

        initial_state = {
            "user_query": user_query,
            "intent": "",
            "chat_history": langchain_history
        }

        # Execute the graph
        result = await self.compiled_graph.ainvoke(initial_state)

        # Return the last AI message
        if result["chat_history"]:
            last_message = result["chat_history"][-1]
            if isinstance(last_message, AIMessage):
                return last_message.content

        return "I couldn't process your request."


chat_pipe = ChatPipeLine()