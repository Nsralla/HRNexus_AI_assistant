# HRNexus Chat Pipeline Workflow

## Overview
The HRNexus chat pipeline uses a state-based graph architecture powered by LangGraph to intelligently route user queries to specialized handlers.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER QUERY                               │
│                    (with optional history)                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  INTENT CLASSIFICATION                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Model: mistralai/ministral-8b (Fast & Efficient)          │ │
│  │  Task: Analyze query to determine intent type              │ │
│  │  Output: conversation | documentation | data_query |       │ │
│  │          web_search                                         │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
                    ┌──────────┐
                    │ ROUTING  │
                    └─────┬────┘
                          │
        ┌─────────────────┼─────────────────┬──────────────────┐
        │                 │                 │                  │
        ▼                 ▼                 ▼                  ▼
┌───────────────┐ ┌───────────────┐ ┌─────────────┐ ┌────────────────┐
│   GENERAL     │ │ DOCUMENTATION │ │ DATA QUERY  │ │  WEB SEARCH    │
│ CONVERSATION  │ │     QUERY     │ │             │ │     QUERY      │
└───────┬───────┘ └───────┬───────┘ └──────┬──────┘ └────────┬───────┘
        │                 │                 │                  │
        └─────────────────┴─────────────────┴──────────────────┘
                                    │
                                    ▼
                              ┌──────────┐
                              │   END    │
                              └──────────┘
```

## Detailed Node Workflows

### 1. Intent Classification Node

**Purpose**: Determine the type of query and route appropriately

```
┌──────────────────────────────────────────────────────────────┐
│ INTENT CLASSIFICATION                                         │
├──────────────────────────────────────────────────────────────┤
│ Input:                                                        │
│   • user_query: string                                        │
│   • chat_history: list of messages                            │
│                                                               │
│ Process:                                                      │
│   1. Format query with classification prompt                 │
│   2. Invoke lightweight LLM (ministral-8b)                   │
│   3. Parse intent from response                              │
│                                                               │
│ Output Intent Types:                                         │
│   • "conversation" → Greetings, identity, casual chat        │
│   • "documentation" → Policy/procedure questions             │
│   • "data_query" → Employee/project/sprint data lookups      │
│   • "web_search" → Current events, latest info               │
│                                                               │
│ Next: Route to appropriate handler                           │
└──────────────────────────────────────────────────────────────┘
```

### 2. General Conversation Node

**Purpose**: Handle casual conversation, greetings, and identity questions

```
┌──────────────────────────────────────────────────────────────┐
│ GENERAL CONVERSATION                                          │
├──────────────────────────────────────────────────────────────┤
│ Triggered By: "conversation" intent                          │
│                                                               │
│ Process Flow:                                                 │
│   1. Add user query to chat history                          │
│   2. Apply system prompt (HRNexus identity)                  │
│   3. Invoke main LLM (grok-4.1-fast)                         │
│   4. Generate natural, conversational response               │
│   5. Add AI response to chat history                         │
│                                                               │
│ Examples:                                                     │
│   • "Hello, who are you?"                                    │
│   • "What can you help me with?"                             │
│   • "Thanks for your help!"                                  │
│                                                               │
│ Model: x-ai/grok-4.1-fast                                    │
│ Context: System prompt + user query                          │
│ Output: Friendly, helpful response                           │
└──────────────────────────────────────────────────────────────┘
```

### 3. Documentation Query Node (RAG)

**Purpose**: Answer questions about company policies and procedures using RAG

```
┌──────────────────────────────────────────────────────────────┐
│ DOCUMENTATION QUERY (RAG)                                     │
├──────────────────────────────────────────────────────────────┤
│ Triggered By: "documentation" intent                          │
│                                                               │
│ RAG Components:                                               │
│   • Vector Store: ChromaDB                                    │
│   • Embeddings: Cohere embed-english-v3.0                    │
│   • Documents: Markdown files from sources/kb/               │
│   • Chunk Size: 1000 chars, Overlap: 350 chars               │
│                                                               │
│ Process Flow:                                                 │
│   1. Add user query to chat history                          │
│   2. Check if vectorstore is available                       │
│   3. ┌─────────────────────────────────────┐                │
│      │ Retrieve top 3 relevant documents   │                │
│      │ using similarity search (Cohere)    │                │
│      └─────────────────────────────────────┘                │
│   4. ┌─────────────────────────────────────┐                │
│      │ Build context from retrieved docs   │                │
│      │ Format: Source: filename + content  │                │
│      └─────────────────────────────────────┘                │
│   5. ┌─────────────────────────────────────┐                │
│      │ Generate answer with LLM using:     │                │
│      │   • Retrieved context                │                │
│      │   • User query                       │                │
│      │   • Documentation prompt template    │                │
│      └─────────────────────────────────────┘                │
│   6. Add AI response to chat history                         │
│                                                               │
│ Examples:                                                     │
│   • "What is our code review policy?"                        │
│   • "How do I onboard a new employee?"                       │
│   • "What's the deployment process?"                         │
│                                                               │
│ Knowledge Base Sources:                                       │
│   • code_review_policy.md                                    │
│   • deployment_process.md                                    │
│   • dev_env_setup.md                                         │
│   • escalation_policy.md                                     │
│   • onboarding_guide.md                                      │
│   • team_structure.md                                        │
└──────────────────────────────────────────────────────────────┘
```

### 4. Data Query Node (Tool Calling)

**Purpose**: Query structured data using specialized search tools

```
┌──────────────────────────────────────────────────────────────┐
│ DATA QUERY (Tool Calling)                                     │
├──────────────────────────────────────────────────────────────┤
│ Triggered By: "data_query" intent or default                 │
│                                                               │
│ Available Tools (7):                                          │
│   1. search_emps_by_key_tool       → Employee data           │
│   2. search_jira_tickets_tool      → JIRA tickets            │
│   3. search_deployments_tool       → Deployment records      │
│   4. search_projects_tool          → Project information     │
│   5. search_sprints_tool           → Sprint data             │
│   6. search_meetings_tool          → Meeting records         │
│   7. search_services_tool          → Service information     │
│                                                               │
│ Process Flow:                                                 │
│   1. Add user query to chat history                          │
│   2. ┌─────────────────────────────────────┐                │
│      │ Create system message with:         │                │
│      │   • All available tools description │                │
│      │   • Tool usage instructions         │                │
│      │   • Data query prompt template      │                │
│      └─────────────────────────────────────┘                │
│   3. ┌─────────────────────────────────────┐                │
│      │ Invoke LLM with tool binding:       │                │
│      │   • LLM analyzes query               │                │
│      │   • Decides which tool(s) to use    │                │
│      │   • Extracts key/value/operator     │                │
│      └─────────────────────────────────────┘                │
│   4. ┌─────────────────────────────────────┐                │
│      │ Execute Tool Calls:                  │                │
│      │   For each tool call:                │                │
│      │     • Extract parameters             │                │
│      │     • Invoke tool function           │                │
│      │     • Collect results                │                │
│      └─────────────────────────────────────┘                │
│   5. ┌─────────────────────────────────────┐                │
│      │ Combine & Format Results:            │                │
│      │   • Aggregate all tool outputs       │                │
│      │   • Raw format (CrewAI handles       │                │
│      │     final formatting)                │                │
│      └─────────────────────────────────────┘                │
│   6. Add results to chat history                             │
│                                                               │
│ Examples:                                                     │
│   • "Find all employees in Engineering"                      │
│   • "Show me open JIRA tickets assigned to John"            │
│   • "What projects are currently active?"                    │
│   • "List recent deployments"                                │
│                                                               │
│ Tool Call Format:                                             │
│   {                                                           │
│     "name": "search_emps_by_key_tool",                       │
│     "args": {                                                 │
│       "key": "department",                                    │
│       "value": "Engineering",                                 │
│       "operator": "equals"  // equals, contains, gt, lt      │
│     }                                                         │
│   }                                                           │
└──────────────────────────────────────────────────────────────┘
```

### 5. Web Search Query Node

**Purpose**: Search the internet for current information using Tavily

```
┌──────────────────────────────────────────────────────────────┐
│ WEB SEARCH QUERY                                              │
├──────────────────────────────────────────────────────────────┤
│ Triggered By: "web_search" intent                            │
│                                                               │
│ Search Provider: Tavily API                                   │
│ Search Depth: Advanced (thorough results)                    │
│ Max Results: 5                                                │
│                                                               │
│ Process Flow:                                                 │
│   1. Add user query to chat history                          │
│   2. ┌─────────────────────────────────────┐                │
│      │ Call Tavily Search Service:          │                │
│      │   • Query: user_query                │                │
│      │   • Depth: advanced                  │                │
│      │   • Results: 5 sources               │                │
│      └─────────────────────────────────────┘                │
│   3. ┌─────────────────────────────────────┐                │
│      │ Receive Search Context:              │                │
│      │   • Titles                           │                │
│      │   • URLs                             │                │
│      │   • Relevant content snippets        │                │
│      └─────────────────────────────────────┘                │
│   4. ┌─────────────────────────────────────┐                │
│      │ Generate Answer with LLM:            │                │
│      │   • Search results as context        │                │
│      │   • User query                       │                │
│      │   • Instructions to cite sources     │                │
│      │   • Markdown formatting              │                │
│      └─────────────────────────────────────┘                │
│   5. Add comprehensive response to history                    │
│                                                               │
│ Examples:                                                     │
│   • "What are the latest HR compliance requirements?"        │
│   • "Current trends in remote work policies"                 │
│   • "Latest news about tech industry layoffs"                │
│   • "Best practices for employee retention in 2025"          │
│                                                               │
│ Response Format:                                              │
│   • Informative answer based on search results               │
│   • Source citations with URLs                               │
│   • Markdown formatting for readability                      │
└──────────────────────────────────────────────────────────────┘
```

## State Structure

```python
StateAgent = {
    "user_query": str,        # Current user question
    "intent": str,            # Classified intent type
    "chat_history": list      # LangChain messages (HumanMessage | AIMessage)
}
```

## LLM Configuration

### Primary LLM (Main Responses)
- **Provider**: OpenRouter
- **Model**: x-ai/grok-4.1-fast
- **Usage**: General conversation, documentation answers, data query synthesis, web search answers

### Intent Classification LLM (Routing)
- **Provider**: OpenRouter
- **Model**: mistralai/ministral-8b
- **Usage**: Fast intent classification for routing
- **Benefit**: Lighter, faster, cost-effective for simple classification

## Tool Architecture

### Tool Binding Pattern
```python
# Tools are bound to the LLM at initialization
llm_with_tools = llm.bind_tools([
    search_emps_by_key_tool,
    search_jira_tickets_tool,
    search_deployments_tool,
    search_projects_tool,
    search_sprints_tool,
    search_meetings_tool,
    search_services_tool,
    search_web_tool  # Available but not used in data_query node
])
```

### Tool Execution Flow
```
User Query
    ↓
LLM with Tools
    ↓
Tool Decision (LLM decides which tool(s) to call)
    ↓
Tool Call(s) Extraction
    ↓
Tool Execution (Invoke actual tool functions)
    ↓
Result Collection
    ↓
Response Generation
```

## Error Handling

### Intent Classification Errors
- Rate limit detection on intent LLM
- Fallback handling
- Detailed error logging

### RAG Errors
- Vector store unavailability check
- No documents found handling
- Cohere API rate limit detection

### Tool Execution Errors
- No tool calls made
- Empty results handling
- Tool execution failures

### Web Search Errors
- Tavily API failures
- Network errors
- Empty search results

## Integration with CrewAI

The pipeline returns **raw tool results** for data queries, which are then processed by CrewAI agents for:
- Intelligent formatting
- Summarization
- Multi-source synthesis
- Natural language presentation

## Performance Optimizations

1. **Lazy Loading**: Heavy dependencies loaded only when needed
2. **Fast Intent Classification**: Lightweight model for routing
3. **Efficient RAG**: Cohere embeddings with optimized chunk size
4. **Tool Binding**: Tools bound once at initialization
5. **Vectorstore Persistence**: ChromaDB for fast retrieval

## Pipeline Lifecycle

```
Application Start
    ↓
Lazy Initialization (first query only)
    ├─ Initialize LLMs
    ├─ Load RAG vectorstore
    ├─ Bind tools to LLM
    ├─ Compile LangGraph workflow
    └─ Ready for queries
    ↓
For Each Query:
    1. Convert chat history to LangChain format
    2. Create initial state
    3. Execute compiled graph
    4. Extract final AI message
    5. Return response
```

## Query Flow Examples

### Example 1: Employee Search
```
User: "Find all software engineers"
    → Intent: data_query
    → Node: data_query
    → Tool: search_emps_by_key_tool(key="role", value="software engineer", operator="contains")
    → Result: Raw employee data
    → CrewAI: Formats into readable list
```

### Example 2: Documentation
```
User: "What's our code review process?"
    → Intent: documentation
    → Node: documentation_query
    → RAG: Retrieve from code_review_policy.md
    → LLM: Generate answer from context
    → Result: Policy explanation
```

### Example 3: Current Events
```
User: "Latest HR compliance laws in 2025"
    → Intent: web_search
    → Node: web_search_query
    → Tavily: Search web for current info
    → LLM: Synthesize answer with sources
    → Result: Current information with URLs
```

### Example 4: Greeting
```
User: "Hello!"
    → Intent: conversation
    → Node: general_conversation
    → LLM: Natural response
    → Result: "Hello! I'm HRNexus..."
```

## Future Enhancements

- [ ] Multi-turn conversation context retention
- [ ] Hybrid queries (RAG + tools + web search)
- [ ] Query refinement and clarification
- [ ] Streaming responses
- [ ] Tool result caching
- [ ] Advanced RAG with re-ranking
- [ ] Custom embeddings fine-tuning

