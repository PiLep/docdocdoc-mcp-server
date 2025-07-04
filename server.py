# server.py
"""Main MCP server file using modular structure."""

from mcp.server.fastmcp import FastMCP
from config.settings import settings
from tools.requests import register_request_tools

# Create an MCP server
mcp = FastMCP("DocDocDoc")

# Register all tools
register_request_tools(mcp)

# === RESOURCES ===
# Note: Resources are kept here for now as they're simple and use the memory storage
# In the future, these could be moved to a separate resources module

# For now, we'll keep a minimal in-memory storage for resources
# In a production system, this would be replaced with actual API calls
memory_requests = {}

@mcp.resource("request://{request_id}")
def get_request_resource(request_id: str) -> str:
    """Get request details as a resource"""
    
    if request_id not in memory_requests:
        return f"Request {request_id} not found in local cache. Use get_request tool instead."
    
    request = memory_requests[request_id]
    
    return f"""DocDocDoc Request: {request['id']}
Status: {request['status']}
Requested Person: {request['requested_name']} ({request['requested_email']})
Requestor: {request['requestor_name']} ({request['requestor_email']})
Document Type: {request['document_type'] or 'Any'}
Message: {request['message'] or 'None'}
Created: {request['created_at']}
Updated: {request['updated_at']}
Companies: {request['requested_company'] or 'N/A'} → {request['requestor_company'] or 'N/A'}
"""

# Note: Document resources would be similar and could be implemented when needed 