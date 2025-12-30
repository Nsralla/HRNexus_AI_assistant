import os
import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING
import importlib

# Import fastmcp while avoiding circular import with this module name 'mcp'
_script_dir = Path(__file__).resolve().parent
_removed_paths: List[str] = []
for _p in list(sys.path):
	try:
		if Path(_p).resolve() == _script_dir:
			_removed_paths.append(_p)
			sys.path.remove(_p)
	except Exception:
		pass

try:
	fastmcp_mod = importlib.import_module("fastmcp")
	FastMCP = getattr(fastmcp_mod, "FastMCP")
finally:
	# Restore any removed paths so local imports keep working
	for _p in _removed_paths:
		if _p not in sys.path:
			sys.path.insert(0, _p)

if TYPE_CHECKING:
	from fastmcp import Context

# ============================================================================
# Logging Configuration
# ============================================================================

log_file = "mcp.log"
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	handlers=[
		logging.FileHandler(log_file),
		logging.StreamHandler()
	]
)
logger = logging.getLogger("hrnexus_mcp_server")


# ============================================================================
# Import setup for project modules
# ============================================================================

# Ensure we can import from backend services when running as MCP server
BASE_DIR = Path(__file__).resolve().parents[1]  # backend/
if str(BASE_DIR) not in sys.path:
	sys.path.append(str(BASE_DIR))

# Lazy-import service modules inside tool functions to avoid startup failures


# ============================================================================
# Server Initialization
# ============================================================================

mcp = FastMCP(name="HRNexus-MCP")


# ============================================================================
# Utility helpers
# ============================================================================

def _read_json_file(path: Path) -> Any:
	try:
		with path.open("r", encoding="utf-8") as f:
			return json.load(f)
	except Exception as e:
		logger.error(f"Failed to read JSON file {path}: {e}")
		return None


def _kb_dir() -> Path:
	# Prefer backend/sources/kb; fallback to top-level kb
	p1 = BASE_DIR / "sources" / "kb"
	p2 = BASE_DIR.parent / "kb"
	return p1 if p1.exists() else p2


def _json_sources_dir() -> Path:
	return BASE_DIR / "sources" / "Json_files"


# ============================================================================
# Tools (Project-related)
# ============================================================================

@mcp.tool
def search_employees(key: str, value: str, operator: str = "equals") -> List[Dict[str, Any]]:
	"""Search employees dataset by a field and operator.

	Common keys: 'role', 'team', 'skills', 'location', 'name', 'availability',
	'years_of_experience', 'current_sprint_capacity', 'current_sprint_allocated'.
	Operators: 'equals' (default), 'greater_than', 'less_than', 'greater_equal', 'less_equal', 'contains'.
	"""
	logger.info(f"TOOL CALL: search_employees(key='{key}', value='{value}', operator='{operator}')")
	try:
		from services.employeesService import emps_service
		results = emps_service.search_emps_by_key_with_operator(key, value, operator)
		payload = [vars(emp) for emp in results]
		logger.info(f"TOOL RESULT: search_employees returned {len(payload)} result(s)")
		return payload
	except Exception as e:
		logger.error(f"search_employees failed: {e}")
		raise


@mcp.tool
def search_projects(key: str, value: str, operator: str = "equals") -> List[Dict[str, Any]]:
	"""Search projects dataset by a field and operator.

	Common keys: 'status', 'lead', 'priority', 'team', 'tech_stack',
	'progress_percentage', 'name'. Operators as above.
	"""
	logger.info(f"TOOL CALL: search_projects(key='{key}', value='{value}', operator='{operator}')")
	try:
		from services.projectsService import projects_service
		results = projects_service.search_by_key_with_operator(key, value, operator)
		payload = [vars(p) for p in results]
		logger.info(f"TOOL RESULT: search_projects returned {len(payload)} result(s)")
		return payload
	except Exception as e:
		logger.error(f"search_projects failed: {e}")
		raise


@mcp.tool
def search_services(key: str, value: str, operator: str = "equals") -> List[Dict[str, Any]]:
	"""Search services/microservices dataset by a field and operator.

	Common keys: 'name', 'type', 'owner_team', 'primary_maintainer', 'status',
	'tech_stack', 'uptime_percentage', 'avg_response_time_ms'. Operators as above.
	"""
	logger.info(f"TOOL CALL: search_services(key='{key}', value='{value}', operator='{operator}')")
	try:
		from services.servicesService import services_service
		results = services_service.search_by_key_with_operator(key, value, operator)
		payload = [vars(s) for s in results]
		logger.info(f"TOOL RESULT: search_services returned {len(payload)} result(s)")
		return payload
	except Exception as e:
		logger.error(f"search_services failed: {e}")
		raise


@mcp.tool
def search_jira_tickets(key: str, value: str, operator: str = "equals") -> List[Dict[str, Any]]:
	"""Search JIRA tickets dataset by a field and operator.
	Keys include: 'status', 'assignee', 'priority', 'sprint', 'epic', 'labels', etc.
	"""
	logger.info(f"TOOL CALL: search_jira_tickets(key='{key}', value='{value}', operator='{operator}')")
	try:
		from services.jiraTicketsService import tickets_service
		results = tickets_service.search_by_key_with_operator(key, value, operator)
		payload = [vars(t) for t in results]
		logger.info(f"TOOL RESULT: search_jira_tickets returned {len(payload)} result(s)")
		return payload
	except Exception as e:
		logger.error(f"search_jira_tickets failed: {e}")
		raise


@mcp.tool
def search_deployments(key: str, value: str, operator: str = "equals") -> List[Dict[str, Any]]:
	"""Search deployments dataset by a field and operator.
	Keys include: 'service', 'status', 'environment', 'version', 'deployed_by', etc.
	"""
	logger.info(f"TOOL CALL: search_deployments(key='{key}', value='{value}', operator='{operator}')")
	try:
		from services.deploymentsService import deployments_service
		results = deployments_service.search_by_key_with_operator(key, value, operator)
		payload = [vars(d) for d in results]
		logger.info(f"TOOL RESULT: search_deployments returned {len(payload)} result(s)")
		return payload
	except Exception as e:
		logger.error(f"search_deployments failed: {e}")
		raise


@mcp.tool
def search_sprints(key: str, value: str, operator: str = "equals") -> List[Dict[str, Any]]:
	"""Search sprints dataset by a field and operator.
	Keys include: 'name', 'status', 'team_velocity', 'total_story_points', etc.
	"""
	logger.info(f"TOOL CALL: search_sprints(key='{key}', value='{value}', operator='{operator}')")
	try:
		from services.sprintsService import sprints_service
		results = sprints_service.search_by_key_with_operator(key, value, operator)
		payload = [vars(s) for s in results]
		logger.info(f"TOOL RESULT: search_sprints returned {len(payload)} result(s)")
		return payload
	except Exception as e:
		logger.error(f"search_sprints failed: {e}")
		raise


@mcp.tool
def search_meetings(key: str, value: str, operator: str = "equals") -> List[Dict[str, Any]]:
	"""Search meetings dataset by a field and operator.
	Keys include: 'type', 'date', 'attendees', 'title', etc.
	"""
	logger.info(f"TOOL CALL: search_meetings(key='{key}', value='{value}', operator='{operator}')")
	try:
		from services.meetingsService import meetings_service
		results = meetings_service.search_by_key_with_operator(key, value, operator)
		payload = [vars(m) for m in results]
		logger.info(f"TOOL RESULT: search_meetings returned {len(payload)} result(s)")
		return payload
	except Exception as e:
		logger.error(f"search_meetings failed: {e}")
		raise


@mcp.tool
def run_chat_pipeline(query: str, chat_history: Optional[List[Dict[str, str]]] = None) -> str:
	"""Execute the HRNexus chat pipeline with intent routing and tools.

	Args:
		query: The user's question or message.
		chat_history: Optional list of prior messages as [{"role": "user|assistant", "content": "..."}].
	Returns:
		Assistant's response string.
	"""
	logger.info(f"TOOL CALL: run_chat_pipeline(query='{query[:60]}...', history_items={len(chat_history or [])})")
	try:
		import asyncio
		from services.chat_pipeline import get_chat_pipeline
		pipe = get_chat_pipeline()
		# Ensure sync interface for MCP tool
		result = asyncio.run(pipe.run(query, chat_history or []))
		logger.info("TOOL RESULT: run_chat_pipeline returned response")
		return result
	except Exception as e:
		logger.error(f"run_chat_pipeline failed: {e}")
		raise


@mcp.tool
def get_server_info() -> Dict[str, Any]:
	"""Get server information, version, and available tools."""
	logger.info("TOOL CALL: get_server_info()")
	tools = [
		"search_employees",
		"search_projects",
		"search_services",
		"search_jira_tickets",
		"search_deployments",
		"search_sprints",
		"search_meetings",
		"run_chat_pipeline",
	]
	info = {
		"name": "hrnexus-mcp-server",
		"version": "0.1.0",
		"description": "MCP server exposing HRNexus project tools and resources",
		"tools": tools,
	}
	logger.info("TOOL RESULT: get_server_info returned info")
	return info


# ============================================================================
# Resources
# ============================================================================

@mcp.resource("config://server-info")
def get_server_config() -> Dict[str, Any]:
	"""Provides server config including version and available transforms/prompts."""
	logger.info("RESOURCE CALL: get_server_config()")
	config = {
		"version": "0.1.0",
		"name": "hrnexus-mcp-server",
		"transforms": ["uppercase", "lowercase", "reverse"],
		"prompts": ["summarize", "explain", "simplify", "employee_summary"],
	}
	logger.info("RESOURCE RESULT: get_server_config returned config")
	return config


@mcp.resource("kb://list")
def list_kb_docs() -> List[str]:
	"""List available knowledge base documents."""
	logger.info("RESOURCE CALL: list_kb_docs()")
	kb = _kb_dir()
	docs = []
	if kb.exists():
		for p in sorted(kb.glob("*.md")):
			docs.append(p.name)
	logger.info(f"RESOURCE RESULT: list_kb_docs returned {len(docs)} doc(s)")
	return docs


@mcp.resource("kb://document/{name}")
def get_kb_document(name: str) -> Dict[str, Any]:
	"""Return KB document content by name (e.g., 'deployment_process.md')."""
	logger.info(f"RESOURCE CALL: get_kb_document(name='{name}')")
	kb = _kb_dir()
	target = kb / name
	if not target.exists():
		raise FileNotFoundError(f"KB document not found: {name}")
	content = target.read_text(encoding="utf-8")
	logger.info("RESOURCE RESULT: get_kb_document returned content")
	return {"name": name, "content": content}


@mcp.resource("dataset://summary")
def dataset_summary() -> Dict[str, Any]:
	"""Provide quick summary counts for available JSON datasets."""
	logger.info("RESOURCE CALL: dataset_summary()")
	src = _json_sources_dir()
	summary = {}
	if src.exists():
		for p in sorted(src.glob("*.json")):
			data = _read_json_file(p) or []
			summary[p.stem] = len(data) if isinstance(data, list) else 1
	logger.info("RESOURCE RESULT: dataset_summary returned counts")
	return summary


# ============================================================================
# Prompts
# ============================================================================

@mcp.prompt()
def format_prompt(prompt_name: str, text: str) -> str:
	"""Format and apply a named prompt template to text."""
	logger.info(f"PROMPT CALL: format_prompt(prompt_name='{prompt_name}')")
	prompts = {
		"summarize": "Provide a concise summary of the following text in one sentence:\n{text}",
		"explain": "Explain the following text in detail with examples:\n{text}",
		"simplify": "Rewrite the following text in simpler, more accessible language:\n{text}",
		"employee_summary": "Summarize the employee dataset insightfully for leadership:\n{text}",
		"transform_uppercase": "Transform this text to uppercase: {text}",
		"transform_lowercase": "Transform this text to lowercase: {text}",
		"transform_reverse": "Reverse this text: {text}",
	}
	if prompt_name not in prompts:
		raise ValueError(f"Unknown prompt: {prompt_name}")
	template = prompts[prompt_name]
	result = template.format(text=text)
	logger.info("PROMPT RESULT: format_prompt returned formatted prompt")
	return result


@mcp.prompt()
def format_search_results(query: str, results: List[Dict[str, Any]]) -> str:
	"""Format search results into a readable summary."""
	logger.info(f"PROMPT CALL: format_search_results(query='{query}', num_results={len(results)})")
	formatted = f"Search Results for: {query}\n\n"
	for i, result in enumerate(results[:10], 1):
		title = result.get("name") or result.get("title") or result.get("id") or "Result"
		desc = result.get("description") or result.get("summary") or json.dumps(result)[:200]
		formatted += f"{i}. {title}\n   {desc}\n\n"
	logger.info("PROMPT RESULT: format_search_results returned formatted results")
	return formatted


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
	logger.info("=" * 80)
	logger.info("Starting HRNexus MCP Server")
	logger.info("=" * 80)
	try:
		mcp.run(transport="stdio")
	except KeyboardInterrupt:
		logger.info("Server shutdown requested")
	except Exception as e:
		logger.error(f"Server error: {e}", exc_info=True)
		raise

