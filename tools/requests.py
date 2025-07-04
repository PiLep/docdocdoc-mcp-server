# tools/requests.py
"""Request-related MCP tools."""

import re
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from api.client import api_client
from models.constants import DOCUMENT_TYPES

def _validate_email(email: str) -> bool:
    """Validate email format."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def _validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    phone_pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
    return re.match(phone_pattern, phone) is not None

def _validate_string_length(text: str, max_length: int = 255) -> bool:
    """Validate string length."""
    return len(text) <= max_length

def register_request_tools(mcp: FastMCP) -> None:
    """Register all request-related tools with the MCP server."""
    
    @mcp.tool()
    def get_request(
        request_id: str,
        with_documents: Optional[bool] = False,
        with_accesses: Optional[bool] = False,
        with_events: Optional[bool] = False,
        with_messages: Optional[bool] = False
    ) -> Dict[str, Any]:
        """Get request details by ID
        
        Args:
            request_id: Unique identifier of the document request to retrieve
            with_documents: Include documents associated with the request in the response
            with_accesses: Include granted accesses in the response
            with_events: Include event history in the response
            with_messages: Include exchanged messages in the response
        """
        
        params = {}
        if with_documents:
            params["with_documents"] = "true"
        if with_accesses:
            params["with_accesses"] = "true"
        if with_events:
            params["with_events"] = "true"
        if with_messages:
            params["with_messages"] = "true"
        
        result = api_client.get_request(request_id, params)
        if "error" not in result:
            result["message"] = "Request retrieved successfully from API"
        
        return result
    
    @mcp.tool()
    def create_request(
        requested_email: str,
        requested_name: str, 
        requestor_email: str,
        requestor_name: str,
        requested_phone: Optional[str] = None,
        requested_company: Optional[str] = None,
        requestor_phone: Optional[str] = None,
        requestor_company: Optional[str] = None,
        document_type: Optional[str] = None,
        message: Optional[str] = None,
        dont_send_message: Optional[bool] = False
    ) -> Dict[str, Any]:
        """Create a new document request via DocDocDoc API.
        
        Args:
            requested_email: Email address of the person to request the document from (required)
            requested_name: Full name of the person to request the document from (required)
            requestor_email: Email address of the person making the request (required)
            requestor_name: Full name of the person making the request (required)
            requested_phone: Phone number of the requested person (format: +33123456789, 01.23.45.67.89 or 0123456789)
            requested_company: Company name of the requested person
            requestor_phone: Phone number of the requester (format: +33123456789, 01.23.45.67.89 or 0123456789)
            requestor_company: Company name of the requester
            document_type: Type of document requested (id_card, passport, driver_license, residence_permit, statutes, company_registration, beneficials_owner_register)
            message: Custom message to send with the request (max 255 characters)
            dont_send_message: If true, do not automatically send the notification email
        
        Phone format examples: "+33123456789", "01.23.45.67.89", "0123456789"
        Document types: id_card, passport, driver_license, residence_permit, statutes, company_registration, beneficials_owner_register
        """
        
        # Validation of required fields
        if not requested_email or not requested_email.strip():
            return {"error": "requested_email is required and cannot be empty"}
        
        if not _validate_email(requested_email):
            return {"error": f"requested_email '{requested_email}' is not a valid email address"}
        
        if not requested_name or not requested_name.strip():
            return {"error": "requested_name is required and cannot be empty"}
        
        if not _validate_string_length(requested_name):
            return {"error": "requested_name must be 255 characters or less"}
        
        if not requestor_email or not requestor_email.strip():
            return {"error": "requestor_email is required and cannot be empty"}
        
        if not _validate_email(requestor_email):
            return {"error": f"requestor_email '{requestor_email}' is not a valid email address"}
        
        if not requestor_name or not requestor_name.strip():
            return {"error": "requestor_name is required and cannot be empty"}
        
        if not _validate_string_length(requestor_name):
            return {"error": "requestor_name must be 255 characters or less"}
        
        # Validation of optional fields
        if requested_phone and not _validate_phone(requested_phone):
            return {"error": f"requested_phone '{requested_phone}' is not a valid phone number. Use format like '+33123456789' or '01.23.45.67.89'"}
        
        if requestor_phone and not _validate_phone(requestor_phone):
            return {"error": f"requestor_phone '{requestor_phone}' is not a valid phone number. Use format like '+33123456789' or '01.23.45.67.89'"}
        
        if requested_company and not _validate_string_length(requested_company):
            return {"error": "requested_company must be 255 characters or less"}
        
        if requestor_company and not _validate_string_length(requestor_company):
            return {"error": "requestor_company must be 255 characters or less"}
        
        if document_type and document_type not in DOCUMENT_TYPES:
            return {"error": f"Invalid document_type '{document_type}'. Must be one of: {', '.join(DOCUMENT_TYPES)}"}
        
        if message and not _validate_string_length(message):
            return {"error": "message must be 255 characters or less"}
        
        # Data preparation
        data = {
            "requested_email": requested_email.strip(),
            "requested_name": requested_name.strip(),
            "requestor_email": requestor_email.strip(),
            "requestor_name": requestor_name.strip(),
        }
        
        # Adding non-empty optional fields
        if requested_phone and requested_phone.strip():
            data["requested_phone"] = requested_phone.strip()
        if requested_company and requested_company.strip():
            data["requested_company"] = requested_company.strip()
        if requestor_phone and requestor_phone.strip():
            data["requestor_phone"] = requestor_phone.strip()
        if requestor_company and requestor_company.strip():
            data["requestor_company"] = requestor_company.strip()
        if document_type and document_type.strip():
            data["document_type"] = document_type.strip()
        if message and message.strip():
            data["message"] = message.strip()
        if dont_send_message is not None:
            data["dont_send_message"] = dont_send_message
        
        result = api_client.create_request(data)
        if "error" not in result:
            result["message"] = "Request created successfully via API"
            if "data" in result and "id" in result["data"]:
                result["request_id"] = result["data"]["id"]
        
        return result
    
    @mcp.tool()
    def update_request(
        request_id: str,
        requested_email: Optional[str] = None,
        requested_phone: Optional[str] = None,
        requested_name: Optional[str] = None,
        requested_company: Optional[str] = None,
        requestor_email: Optional[str] = None,
        requestor_phone: Optional[str] = None,
        requestor_name: Optional[str] = None,
        requestor_company: Optional[str] = None,
        document_type: Optional[str] = None,
        message: Optional[str] = None,
        send_again: Optional[bool] = False
    ) -> Dict[str, Any]:
        """Update an existing request
        
        Args:
            request_id: Unique identifier of the request to modify
            requested_email: New email address of the requested person
            requested_phone: New phone number of the requested person
            requested_name: New name of the requested person
            requested_company: New company name of the requested person
            requestor_email: New email address of the requester
            requestor_phone: New phone number of the requester
            requestor_name: New name of the requester
            requestor_company: New company name of the requester
            document_type: New document type (id_card, passport, driver_license, etc.)
            message: New custom message
            send_again: If true, resend the notification email
        """
        
        if document_type and document_type not in DOCUMENT_TYPES:
            return {"error": f"Invalid document type. Must be one of: {', '.join(DOCUMENT_TYPES)}"}
        
        data = {
            "requested_email": requested_email,
            "requested_phone": requested_phone,
            "requested_name": requested_name,
            "requested_company": requested_company,
            "requestor_email": requestor_email,
            "requestor_phone": requestor_phone,
            "requestor_name": requestor_name,
            "requestor_company": requestor_company,
            "document_type": document_type,
            "message": message,
            "send_again": send_again
        }
        
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        
        result = api_client.update_request(request_id, data)
        if "error" not in result:
            result["message"] = "Request updated successfully via API"
        
        return result
    
    @mcp.tool()
    def cancel_request(
        request_id: str
    ) -> Dict[str, Any]:
        """Cancel a request by setting its status to cancelled
        
        Args:
            request_id: Unique identifier of the request to cancel
        """
        
        result = api_client.cancel_request(request_id)
        if "error" not in result:
            result["message"] = "Request cancelled successfully via API"
        
        return result
    
    @mcp.tool()
    def delete_request(
        request_id: str
    ) -> Dict[str, Any]:
        """Delete a request
        
        Args:
            request_id: Unique identifier of the request to delete
        """
        
        result = api_client.delete_request(request_id)
        if "error" not in result:
            result["message"] = "Request deleted successfully via API"
        
        return result 