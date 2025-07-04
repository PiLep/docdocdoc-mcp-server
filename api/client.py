"""API client for interacting with the DocDocDoc API."""

import requests
from typing import Dict, Any, Optional
from config.settings import settings

class DocDocDocAPI:
    """Client for interacting with the DocDocDoc API."""
    
    def __init__(self):
        self.base_url = settings.base_url
        self.headers = {
            "X-API-Key": settings.api_key,
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a request to the API."""
        if not settings.is_configured:
            return {"error": "API_KEY not configured"}
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data
            )
            response.raise_for_status()
            
            api_response = response.json()
            
            return {
                "message": f"Request successful",
                "data": api_response.get("data", api_response),
                "meta": api_response.get("meta", {})
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "error": f"API request failed: {str(e)}",
                "fallback_message": "Could not connect to DocDocDoc API"
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}"
            }
    
    def get_request(self, request_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get a specific request by ID."""
        return self._make_request("GET", f"/api/request/{request_id}", params=params)
    
    def create_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new request."""
        return self._make_request("POST", "/api/request", data=data)
    
    def update_request(self, request_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing request."""
        return self._make_request("PUT", f"/api/request/{request_id}", data=data)
    
    def cancel_request(self, request_id: str) -> Dict[str, Any]:
        """Cancel a request by calling the cancel endpoint."""
        return self._make_request("GET", f"/api/request/{request_id}/cancel")
    
    def delete_request(self, request_id: str) -> Dict[str, Any]:
        """Delete a request."""
        return self._make_request("DELETE", f"/api/request/{request_id}")

# Global API client instance
api_client = DocDocDocAPI() 