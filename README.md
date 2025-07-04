# DocDocDoc MCP Server

A Model Context Protocol server for the DocDocDoc API that enables document request management.

## Overview

DocDocDoc is a document request service that allows users to request documents from others. The requested person receives a notification and can upload the required documents through a secure access link.

## Features

- **Request Management**: Create, read, update, delete, and cancel document requests
- **Status Tracking**: Monitor request lifecycle 
- **Document Types**: Support for specific document types (ID cards, passports, etc.)
- **API Integration**: Full integration with DocDocDoc staging API

## Available Tools

### Request Operations
- `create_request` - Create a new document request
- `get_request` - Get request details by ID
- `update_request` - Update request information
- `delete_request` - Delete a request permanently
- `cancel_request` - Cancel a request (sets status to cancelled)

## Data Models

### Request Statuses
- `pending` - Request created, waiting for response
- `viewed` - Request has been viewed by the requested person
- `cancelled` - Request was cancelled
- `completed` - Request fulfilled with documents
- `rejected` - Request was rejected
- `approved` - Request was approved
- `expired` - Request has expired

### Document Types
- `id_card` - National ID card
- `passport` - Passport
- `driver_license` - Driver's license
- `residence_permit` - Residence permit
- `statutes` - Company statutes
- `company_registration` - Company registration documents
- `beneficials_owner_register` - Beneficial owners register

## Installation

```bash
uv sync
```

## Usage

Run the server:

```bash
uv run main.py
```

## Configuration

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "docdocdoc-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/docdocdoc-mcp-server",
        "run",
        "main.py"
      ],
      "env": {
        "API_KEY": "your-api-key-here",
        "BASE_URL": "https://staging.docdocdoc.fr"
      }
    }
  }
}
```

## Environment Variables

- `API_KEY` - Your DocDocDoc API key (required)
- `BASE_URL` - API base URL (defaults to https://staging.docdocdoc.fr)

## Example Usage

### 1. Create a Document Request

```
create_request(
  requested_email="john.doe@company.com",
  requested_name="John Doe",
  requestor_email="hr@company.com",
  requestor_name="HR Department",
  document_type="id_card",
  message="Please provide your ID card for verification"
)
```

### 2. Get Request Details

```
get_request(request_id="123e4567-e89b-12d3-a456-426614174000")
```

### 3. Update a Request

```
update_request(
  request_id="123e4567-e89b-12d3-a456-426614174000",
  message="Updated: Please provide your passport instead",
  document_type="passport"
)
```

### 4. Cancel a Request

```
cancel_request(request_id="123e4567-e89b-12d3-a456-426614174000")
```

### 5. Delete a Request

```
delete_request(request_id="123e4567-e89b-12d3-a456-426614174000")
```

## Security Features

- API key authentication via `X-API-Key` header
- Input validation for emails, phone numbers, and required fields
- Proper error handling and validation

## Architecture

- **Modular Design**: Clean separation of concerns with dedicated modules
- **API Client**: Centralized HTTP client for DocDocDoc API
- **Configuration**: Environment-based configuration management
- **Error Handling**: Comprehensive validation and error reporting

## Notes

- All operations work with live API endpoints
- Supports full CRUD operations for document requests
- Request cancellation preserves data while marking as cancelled
- Request deletion permanently removes data from the system
