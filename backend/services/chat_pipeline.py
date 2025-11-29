import os
from dotenv import load_dotenv
from typing import TypedDict, TYPE_CHECKING

# Lazy imports - only load heavy dependencies when needed
if TYPE_CHECKING:
    from langchain_core.messages import HumanMessage, AIMessage
    from langgraph.graph import StateGraph
    from langchain_openai import ChatOpenAI

load_dotenv()


class StateAgent(TypedDict):
    user_query: str
    intent: str
    chat_history: list  # Use list instead of list[HumanMessage | AIMessage] for lazy loading


class ChatPipeLine:
    def __init__(self):
        try:
            # Import heavy dependencies only when initializing
            from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
            from langgraph.graph import StateGraph, END
            from langchain_openai import ChatOpenAI
            from .employeesService import search_emps_by_key_tool
            from .jiraTicketsService import search_jira_tickets_tool
            from .deploymentsService import search_deployments_tool
            from .projectsService import search_projects_tool
            from .sprintsService import search_sprints_tool
            from .meetingsService import search_meetings_tool
            from .servicesService import search_services_tool

            # Store for use in methods
            self.HumanMessage = HumanMessage
            self.AIMessage = AIMessage
            self.SystemMessage = SystemMessage
            self.END = END

            self.workflow = StateGraph(StateAgent)
            self.llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
                model="x-ai/grok-4.1-fast"
            )
         
            self.intent_llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("Hr_Nexus_Intent_routing"),
                model="mistralai/ministral-8b"  # $0.10/M tokens - cheap, fast, no daily limits
            )

            # Bind ALL 7 tools to the LLM
            self.llm_with_tools = self.llm.bind_tools([
                search_emps_by_key_tool,
                search_jira_tickets_tool,
                search_deployments_tool,
                search_projects_tool,
                search_sprints_tool,
                search_meetings_tool,
                search_services_tool
            ])

            # Store tool map for later use
            self.tool_map = {
                "search_emps_by_key_tool": search_emps_by_key_tool,
                "search_jira_tickets_tool": search_jira_tickets_tool,
                "search_deployments_tool": search_deployments_tool,
                "search_projects_tool": search_projects_tool,
                "search_sprints_tool": search_sprints_tool,
                "search_meetings_tool": search_meetings_tool,
                "search_services_tool": search_services_tool
            }

            # Initialize RAG vector store
            self.vectorstore = None
            self.initialize_rag()

            self.compiled_graph = None
            self.init_graph()

            print("[INFO] ChatPipeLine initialized successfully")
        except Exception as e:
            print(f"[ERROR] Failed to initialize ChatPipeLine: {e}")
            # Re-raise to prevent half-initialized state
            raise

    def initialize_rag(self):
        """Initialize RAG vector store for documentation queries"""
        # Try to import RAG dependencies
        try:
            from rag_data_loader import RAGDataLoader
            has_rag = True
        except ImportError as e:
            print(f"[WARNING] RAG dependencies not available: {e}")
            has_rag = False
            RAGDataLoader = None

        if not has_rag or RAGDataLoader is None:
            print("[WARNING] RAG system not available - missing dependencies")
            self.vectorstore = None
            return

        try:
            rag_loader = RAGDataLoader(
                kb_dir="sources/kb",
                chunk_size=1000,
                chunk_overlap=350,
                embedding_model="embed-english-v3.0",  # Cohere free embedding model
                collection_name="hr_nexus_rag"
            )

            # Try to load existing vector store
            self.vectorstore = rag_loader.load_existing_vectorstore("./chroma_db")

            # If it doesn't exist, create it
            if not self.vectorstore:
                print("[INFO] Vector store not found, creating new one...")
                _, _, self.vectorstore = rag_loader.load_and_create_vectorstore(
                    persist_directory="./chroma_db"
                )
                if self.vectorstore:
                    print("[INFO] RAG vector store created successfully")
                else:
                    print("[WARNING] Failed to create RAG vector store")
            else:
                print("[INFO] RAG vector store loaded successfully")
        except Exception as e:
            print(f"[ERROR] Failed to initialize RAG: {e}")
            self.vectorstore = None

    async def intent_classification(self, state: StateAgent) -> StateAgent:
        """Classify user query intent into conversation, documentation, or data_query"""
        prompt = """Classify the user's query intent into ONE of these categories:

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

        try:
            messages = [self.HumanMessage(content=prompt.format(user_query=state["user_query"]))]
            # Use lighter, faster LLM for intent classification
            print(f"[DEBUG] Calling intent classification LLM with model: {self.intent_llm.model_name}")
            response = await self.intent_llm.ainvoke(messages)
            state["intent"] = response.content.strip().lower()
            print(f"[DEBUG] Intent classification successful: {state['intent']}")
            return state
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Intent classification failed with model '{self.intent_llm.model_name}': {error_msg}")
            if "429" in error_msg or "rate limit" in error_msg.lower():
                print(f"[ERROR] RATE LIMIT HIT on intent classification model: {self.intent_llm.model_name}")
                print(f"[ERROR] API Key used: {os.getenv('Hr_Nexus_Intent_routing', 'NOT_SET')[:15]}...")
            raise Exception(f"Intent classification failed (model: {self.intent_llm.model_name}): {error_msg}")

    def intent_routing(self, state: StateAgent) -> str:
        """Route to appropriate handler based on intent"""
        print("[DEBUG] Intent classified as:", state["intent"])

        if "conversation" in state["intent"]:
            return "general_conversation"
        elif "documentation" in state["intent"]:
            return "documentation_query"
        else:
            return "data_query"

    async def documentation_query(self, state: StateAgent) -> StateAgent:
        """Handle documentation queries using RAG"""
        state["chat_history"].append(self.HumanMessage(content=state["user_query"]))

        if not self.vectorstore:
            response_message = "Documentation system is currently unavailable. Please contact support."
            state["chat_history"].append(self.AIMessage(content=response_message))
            return state

        try:
            # Retrieve relevant documents from vector store
            print(f"[DEBUG] Calling vectorstore similarity_search with Cohere embeddings")
            relevant_docs = self.vectorstore.similarity_search(state["user_query"], k=3)
            print(f"[DEBUG] Retrieved {len(relevant_docs)} relevant documents for query.")
            print(f"[DEBUG] Documents: {[doc.metadata.get('filename', 'unknown') for doc in relevant_docs]}")

            if not relevant_docs:
                response_message = "No relevant documentation found for your query."
                state["chat_history"].append(self.AIMessage(content=response_message))
                return state

            # Build context from retrieved documents
            context_parts = []
            for doc in relevant_docs:
                context_parts.append(f"Source: {doc.metadata.get('filename', 'unknown')}\n{doc.page_content}")

            context = "\n\n---\n\n".join(context_parts)

            # Generate answer using LLM with context
            prompt = f"""Using the following documentation, answer the user's question.
Be concise but comprehensive. Use markdown formatting for clarity.

Documentation:
{context}

User Question: {state["user_query"]}

Provide a helpful, well-formatted answer based on the documentation above."""

            response = await self.llm.ainvoke([self.HumanMessage(content=prompt)])
            state["chat_history"].append(self.AIMessage(content=response.content))

        except Exception as e:
            error_message = f"Error retrieving documentation: {str(e)}"
            print(f"[ERROR] {error_message}")
            if "429" in error_message or "rate limit" in error_message.lower():
                print(f"[ERROR] RATE LIMIT HIT during documentation query (likely Cohere embeddings)")
                print(f"[ERROR] Check COHERE_API_KEY limits")
            state["chat_history"].append(self.AIMessage(content="An error occurred while searching documentation."))

        return state

    async def general_conversation(self, state: StateAgent) -> StateAgent:
        """Handle general conversation, greetings, and identity questions"""
        state["chat_history"].append(self.HumanMessage(content=state["user_query"]))

        system_prompt = """You are HRNexus, an AI assistant for your company's HR and engineering operations.

Your capabilities:
- Answer questions about company policies and processes (code review, deployment, onboarding, etc.)
- Search employee information (teams, skills, locations, capacity)
- Query JIRA tickets (status, assignments, sprints, priorities)
- Check deployment history (production, staging, versions, health)
- View project details (progress, teams, tech stack, budgets)
- Track sprint metrics (velocity, story points, burndown)

When greeting users or answering identity questions:
- Be friendly and professional
- Briefly introduce yourself and your main capabilities
- Encourage users to ask specific questions about employees, projects, documentation, etc.

Keep responses concise and helpful."""

        messages = [
            self.HumanMessage(content=system_prompt),
            self.HumanMessage(content=f"User: {state['user_query']}\n\nRespond naturally and helpfully.")
        ]

        try:
            response = await self.llm.ainvoke(messages)
            state["chat_history"].append(self.AIMessage(content=response.content))
        except Exception as e:
            print(f"[ERROR] General conversation failed: {e}")
            state["chat_history"].append(self.AIMessage(content="Hi! I'm HRNexus, your HR assistant. How can I help you today?"))

        return state

    async def data_query(self, state: StateAgent) -> StateAgent:
        """Handle structured data queries with ALL 7 tools"""
        print(f"[DATA_QUERY DEBUG 1/8] Starting data_query for: {state['user_query'][:50]}...")

        state["chat_history"].append(self.HumanMessage(content=state["user_query"]))
        print(f"[DATA_QUERY DEBUG 2/8] Added user query to chat history")

        # System message describing all available tools
        system_message = self.HumanMessage(content="""You are an HR assistant with access to 7 tools for searching company data.

**TOOL 1: search_emps_by_key_tool** - Employee information
Fields: name, role, team, skills, location, timezone, email, jira_username, github_username,
        slack_handle, availability, years_of_experience, current_sprint_capacity, current_sprint_allocated

**TOOL 2: search_jira_tickets_tool** - JIRA tickets
Fields: id, summary, description, assignee, reporter, status, priority, story_points,
        sprint, epic, labels, component, estimated_hours, time_spent_hours, blocked

**TOOL 3: search_deployments_tool** - Deployment history
Fields: id, service, version, date, status, environment, deployed_by, duration_minutes,
        rollback_available, health_check_passed, jira_tickets, notes, error_message

**TOOL 4: search_projects_tool** - Projects
Fields: id, name, key, description, status, lead, team, start_date, target_completion,
        progress_percentage, budget_hours, consumed_hours, epics, repositories, tech_stack, priority

**TOOL 5: search_sprints_tool** - Sprints
Fields: id, name, start_date, end_date, status, goal, total_story_points,
        completed_story_points, team_velocity, tickets

**TOOL 6: search_meetings_tool** - Meetings
Fields: id, title, type, date, duration_minutes, attendees, agenda, notes, action_items
Types: sprint-planning, retrospective, standup, technical, security, team-sync, post-mortem

**TOOL 7: search_services_tool** - Services/Microservices
Fields: id, name, type, owner_team, primary_maintainer, status, uptime_percentage,
        avg_response_time_ms, tech_stack, dependencies, current_version, deployment_frequency

**OPERATORS** (all tools support these):
- equals: Exact match (default)
- greater_than, less_than, greater_equal, less_equal: Numeric comparisons
- contains: Substring/partial match

**EXAMPLES**:
- "backend team members": search_emps_by_key_tool(key='team', value='Backend', operator='equals')
- "open JIRA tickets": search_jira_tickets_tool(key='status', value='Open', operator='equals')
- "failed deployments": search_deployments_tool(key='status', value='Failed', operator='equals')
- "active projects": search_projects_tool(key='status', value='active', operator='equals')
- "Sprint 24 details": search_sprints_tool(key='name', value='Sprint 24', operator='equals')
- "sprint planning meetings": search_meetings_tool(key='type', value='sprint-planning', operator='equals')
- "Backend services": search_services_tool(key='owner_team', value='Backend', operator='equals')

IMPORTANT: Choose the appropriate tool based on what data the user is asking for.
Always format responses clearly with markdown.""")

        # Create messages for the LLM with tool binding
        messages = [system_message] + state["chat_history"].copy()
        print(f"[DATA_QUERY DEBUG 3/8] Created message list with {len(messages)} messages")

        # Invoke LLM with all 7 tools
        print(f"[DATA_QUERY DEBUG 4/8] Invoking LLM with tools...")
        response = await self.llm_with_tools.ainvoke(messages)
        print(f"[DATA_QUERY DEBUG 5/8] LLM response received, checking for tool calls...")

        # Check if the model wants to use tools
        if response.tool_calls:
            print(f"[DATA_QUERY DEBUG 6/8] Found {len(response.tool_calls)} tool calls")
            tool_results = []

            # Execute all tool calls
            for tool_call in response.tool_calls:
                print(f"[DATA_QUERY DEBUG 6.1/8] Executing tool: {tool_call['name']}")
                tool_name = tool_call["name"]
                key = str(tool_call["args"]["key"])
                value = str(tool_call["args"]["value"])
                operator = str(tool_call["args"].get("operator", "equals"))

                # Use stored tool map from __init__
                if tool_name in self.tool_map:
                    result = self.tool_map[tool_name].invoke({"key": key, "value": value, "operator": operator})
                    print(f"[DATA_QUERY DEBUG 6.2/8] Tool {tool_name} returned: {len(str(result))} chars")

                    if result:
                        formatted_result = f"Found {len(result)} result(s) from {tool_name}:\n\n{result}"
                        tool_results.append(formatted_result)
                    else:
                        tool_results.append(f"No results found from {tool_name}")

            # Combine all tool results
            if tool_results:
                combined_results = "\n\n---\n\n".join(tool_results)
                print(f"[DATA_QUERY DEBUG 7/8] Combined results: {len(combined_results)} chars, sending to LLM for formatting...")

                # Create final response with tool results
                final_messages = messages + [
                    response,
                    self.HumanMessage(content=f"Tool results:\n\n{combined_results}")
                ]
                final_messages.append(
                    self.SystemMessage(
                        content=(
                            "IMPORTANT: Do NOT call any tools now. "
                            "You have already received tool results. "
                            "Your job is ONLY to summarize, organize, or format the provided tool results "
                            "into a clean, helpful answer for the user. "
                            "Do NOT request or generate additional tool calls."
                        )
                    )
                )


                try:
                    final_response = await self.llm.ainvoke(final_messages)
                    response_content = final_response.content if hasattr(final_response, 'content') else str(final_response)
                    print(f"[DATA_QUERY DEBUG 7.2/8] Final response length: {len(response_content)} chars")

                    # Ensure response is not empty
                    if not response_content or not response_content.strip():
                        print(f"[DATA_QUERY WARNING] LLM returned empty response, using tool results directly")
                        response_content = combined_results

                    state["chat_history"].append(self.AIMessage(content=response_content))
                    print(f"[DATA_QUERY DEBUG 8/8] Response added to chat history")
                except Exception as e:
                    print(f"[DATA_QUERY ERROR] Failed to get final response from LLM: {e}")
                    state["chat_history"].append(self.AIMessage(content=combined_results))
                    print(f"[DATA_QUERY DEBUG 8/8] Using tool results directly due to error")
            else:
                # Strict routing - no results found
                print(f"[DATA_QUERY DEBUG 8/8] No tool results, returning 'no data found' message")
                state["chat_history"].append(self.AIMessage(content="No matching data found for your query."))
        else:
            # No tool call made - strict routing error
            print(f"[DATA_QUERY DEBUG 8/8] No tool calls made by LLM")
            state["chat_history"].append(self.AIMessage(content="No matching data found for your query."))

        return state

    def init_graph(self):
        """Initialize and compile the workflow graph"""
        # Add nodes
        self.workflow.add_node("intent_classification", self.intent_classification)
        self.workflow.add_node("general_conversation", self.general_conversation)
        self.workflow.add_node("documentation_query", self.documentation_query)
        self.workflow.add_node("data_query", self.data_query)

        # Set entry point
        self.workflow.set_entry_point("intent_classification")

        # Add conditional edges based on intent
        self.workflow.add_conditional_edges(
            "intent_classification",
            self.intent_routing,
            {
                "general_conversation": "general_conversation",
                "documentation_query": "documentation_query",
                "data_query": "data_query"
            }
        )

        # Add edges to END
        self.workflow.add_edge("general_conversation", self.END)
        self.workflow.add_edge("documentation_query", self.END)
        self.workflow.add_edge("data_query", self.END)

        # Compile the graph
        self.compiled_graph = self.workflow.compile()

    async def run(self, user_query: str, chat_history: list[dict] = None) -> str:
        """Run the chat pipeline with a user query and optional chat history.

        Args:
            user_query: The current user query
            chat_history: List of previous messages in format [{"role": "user/assistant", "content": "..."}]
        """
        print(f"[PIPELINE DEBUG 1/6] Pipeline run started for query: {user_query[:50]}...")

        # Convert chat history to LangChain message format
        langchain_history = []
        if chat_history:
            print(f"[PIPELINE DEBUG 2/6] Converting {len(chat_history)} history messages")
            for msg in chat_history[:-1]:  # Exclude the current message (last one)
                if msg["role"] == "user":
                    langchain_history.append(self.HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    langchain_history.append(self.AIMessage(content=msg["content"]))
            print(f"[PIPELINE DEBUG 3/6] Converted to {len(langchain_history)} LangChain messages")
        else:
            print(f"[PIPELINE DEBUG 2/6] No chat history provided")

        initial_state = {
            "user_query": user_query,
            "intent": "",
            "chat_history": langchain_history
        }
        print(f"[PIPELINE DEBUG 4/6] Initial state created, executing graph...")

        try:
            # Execute the graph
            result = await self.compiled_graph.ainvoke(initial_state)
            print(f"[PIPELINE DEBUG 5/6] Graph execution complete, processing result...")

            # Return the last AI message
            if result["chat_history"]:
                last_message = result["chat_history"][-1]
                if isinstance(last_message, self.AIMessage):
                    response_length = len(last_message.content)
                    print(f"[PIPELINE DEBUG 6/6] Pipeline run successful, returning response ({response_length} chars)")
                    return last_message.content

            print(f"[PIPELINE WARNING] No AI message found in result, returning fallback")
            return "I couldn't process your request."
        except Exception as e:
            print(f"[PIPELINE ERROR] Pipeline execution failed: {type(e).__name__}: {str(e)}")
            raise


# Lazy initialization to prevent startup crashes
_chat_pipe = None

def get_chat_pipeline() -> ChatPipeLine:
    """Get or create the chat pipeline instance (lazy initialization)"""
    global _chat_pipe
    if _chat_pipe is None:
        _chat_pipe = ChatPipeLine()
    return _chat_pipe
