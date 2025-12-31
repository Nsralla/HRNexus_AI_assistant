import os
import sys
import yaml
import logging
from typing import Optional
from pathlib import Path
from crewai import Agent, Task, Crew
from crewai.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Add backend directory to path for imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from tools.summary_tool import SummaryTool
from tools.format_tool import FormatTool

load_dotenv()

# Setup logger
logger = logging.getLogger(__name__)

# Initialize tool instances
summary_tool_instance = SummaryTool()
format_tool_instance = FormatTool()


@tool("create_summary")
def create_summary_tool(text: str) -> str:
    """
    Create a concise summary of the given text. This tool summarizes langgraph outputs while preserving key information.
    Returns a concise summary preserving key information (50-200 words).
    
    Args:
        text: The text to summarize (typically output from langgraph pipeline)
        
    Returns:
        A concise summary preserving key information
    """
    return summary_tool_instance.create_summary(text)


@tool("format_response")
def format_response_tool(text: str) -> str:
    """
    Format the given text into a clear, professional, and well-structured response. 
    This tool formats langgraph outputs for better readability in HR contexts.
    Returns a well-formatted response with proper structure, bullet points, and sections.
    
    Args:
        text: The text to format (typically output from langgraph pipeline)
        
    Returns:
        A well-formatted response with proper structure, bullet points, and sections
    """
    return format_tool_instance.format_response(text)


def load_agent_config(config_path: Optional[str] = None) -> dict:
    """
    Load agent configuration from YAML file.
    
    Args:
        config_path: Path to agent config YAML file. Defaults to agents/agent_config.yaml
        
    Returns:
        Dictionary containing agent configuration
    """
    if config_path is None:
        # Get the directory of this file and construct path to config
        current_dir = Path(__file__).parent
        config_path = current_dir / "agent_config.yaml"
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Loaded agent config from {config_path}")
        return config
    except Exception as e:
        logger.error(f"Failed to load agent config from {config_path}: {e}")
        raise


def create_response_formatter_agent(config: Optional[dict] = None, llm: Optional[ChatOpenAI] = None) -> Agent:
    """
    Create the response formatter agent with summary and format tools.
    
    Args:
        config: Agent configuration dictionary. If None, loads from agent_config.yaml
        llm: LLM instance for the agent. If None, creates a default one.
        
    Returns:
        CrewAI Agent instance configured for response formatting
    """
    if config is None:
        config = load_agent_config()
    
    agent_config = config.get("agents", {}).get("response_formatter_agent", {})
    
    if not agent_config:
        raise ValueError("response_formatter_agent configuration not found in config file")
    
    # Get agent properties from config
    role = agent_config.get("role", "Response Formatter and Summarizer")
    goal = agent_config.get("goal", "Format and summarize langgraph outputs")
    backstory = agent_config.get("backstory", "You are an HR response formatter agent.")
    verbose = agent_config.get("verbose", True)
    allow_delegation = agent_config.get("allow_delegation", False)
    max_iter = agent_config.get("max_iter", 3)
    
    # Prepare tools list
    tools = []
    tool_names = agent_config.get("tools", [])
    
    if "create_summary" in tool_names:
        tools.append(create_summary_tool)
    if "format_response" in tool_names:
        tools.append(format_response_tool)
    
    if not tools:
        logger.warning("No tools found in agent config. Agent will be created without tools.")
    
    # Create LLM if not provided
    if llm is None:
        # CrewAI uses litellm which requires provider prefix for OpenRouter models
        model_name = os.getenv("CREW_MODEL", "openrouter/xiaomi/mimo-v2-flash:free")
        # Ensure model has openrouter prefix if not already present
        if not model_name.startswith("openrouter/"):
            model_name = f"openrouter/{model_name}"
        
        llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("CREW_KEY"),
            model=model_name,
            temperature=0.3,
        )
    
    # Create the agent
    agent = Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools,
        verbose=verbose,
        allow_delegation=allow_delegation,
        max_iter=max_iter,
        llm=llm,
    )
    
    logger.info(f"Created response_formatter_agent with {len(tools)} tool(s)")
    return agent


def process_langgraph_output(langgraph_output: str, summarize: bool = True, format_output: bool = True) -> str:
    """
    Process langgraph output using the response formatter agent.
    
    Args:
        langgraph_output: The raw output from langgraph pipeline
        summarize: Whether to summarize the output (default: True)
        format_output: Whether to format the output (default: True)
        
    Returns:
        Processed output (summarized and/or formatted)
    """
    try:
        result = langgraph_output
        
        # Summarize if requested
        if summarize:
            logger.info("Summarizing langgraph output...")
            # CrewAI tools need to be invoked using .run() method
            result = create_summary_tool.run(text=result)
            logger.info(f"Summary created: {len(result)} characters")
        
        # Format if requested
        if format_output:
            logger.info("Formatting langgraph output...")
            # CrewAI tools need to be invoked using .run() method
            result = format_response_tool.run(text=result)
            logger.info(f"Response formatted: {len(result)} characters")
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing langgraph output: {e}")
        # Return original output on error
        return langgraph_output


# Lazy initialization
_response_formatter_agent = None


def get_response_formatter_agent() -> Agent:
    """
    Get or create the response formatter agent instance (singleton pattern).
    
    Returns:
        CrewAI Agent instance
    """
    global _response_formatter_agent
    if _response_formatter_agent is None:
        _response_formatter_agent = create_response_formatter_agent()
    return _response_formatter_agent


def process_with_agent(langgraph_output: str) -> str:
    """
    Process langgraph output using CrewAI agent with Task and Crew.
    This creates a proper CrewAI workflow to format the response.
    
    Args:
        langgraph_output: The raw output from langgraph pipeline
        
    Returns:
        Processed output (formatted and summarized by the agent)
    """
    try:
        agent = get_response_formatter_agent()
        
        # Create a task for the agent
        task = Task(
            description=f"""Take the following langgraph output and process it:
1. Summarize it concisely while preserving key information
2. Format it in a clear, professional, and well-structured format suitable for HR communications
3. Use appropriate formatting: bullet points, sections, clear paragraphs
4. Ensure the tone is professional and appropriate for HR context

Langgraph output to process:
{langgraph_output}""",
            agent=agent,
            expected_output="A well-formatted, concise, and professional response suitable for HR communications."
        )
        
        # Create a crew with the agent and task
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        # Extract the result (CrewAI returns a CrewOutput object)
        if hasattr(result, 'raw'):
            return str(result.raw)
        elif hasattr(result, 'output'):
            return str(result.output)
        else:
            return str(result)
            
    except Exception as e:
        logger.error(f"Error processing with CrewAI agent: {e}")
        # Fallback to direct tool processing
        return process_langgraph_output(langgraph_output, summarize=True, format_output=True)

