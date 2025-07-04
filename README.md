# DocDocDoc MCP Server

A comprehensive document request SaaS platform MCP server implementing the full DocDocDoc API specification.

## Overview

DocDocDoc is a document request service that allows users to request documents from others. The requested person receives a notification and can upload the required documents through a secure access link.

## Features

- **Request Management**: Create, read, update, delete document requests
- **Document Handling**: Upload, download, and manage documents
- **Access Control**: Secure access links with expiration dates
- **Webhook Support**: Real-time notifications for events
- **Status Tracking**: Complete request lifecycle management
- **Document Types**: Support for specific document types (ID cards, passports, etc.)

## Available Tools

### Request Operations
- `create_request` - Create a new document request
- `get_request` - Get request details with optional related data
- `update_request` - Update request information
- `delete_request` - Delete a request and all associated data
- `cancel_request` - Cancel a request (sets status to cancelled)
- `list_requests` - List all requests with optional status filtering

### Document Operations
- `upload_request_document` - Upload a document to a request
- `get_request_document` - Get document details
- `delete_request_document` - Delete a document
- `download_request_document` - Get document download information

### Access Management
- `get_request_access` - Get access details
- `delete_request_access` - Revoke access
- `extend_request_access` - Extend access expiration

### Webhook Operations
- `list_webhooks` - List all webhooks
- `create_webhook` - Create a new webhook
- `get_webhook` - Get webhook details
- `delete_webhook` - Delete a webhook

### Utility Functions
- `get_request_stats` - Get platform statistics

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

### Access Rights
- `read` - View only access
- `write` - Upload documents
- `manage` - Full management access

## Available Resources

### `request://{request_id}`
Access detailed information about a specific request.

### `document://{document_id}`
Access detailed information about a specific document.

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
      ]
    }
  }
}
```

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

### 2. List Pending Requests

```
list_requests(status="pending")
```

### 3. Upload a Document

```
upload_request_document(
  request_id="123e4567-e89b-12d3-a456-426614174000",
  filename="id_card.pdf",
  mime_type="application/pdf",
  size=1024000
)
```

### 4. Create a Webhook

```
create_webhook(
  url="https://your-app.com/webhook",
  description="Notify when documents are uploaded",
  active=true
)
```

### 5. Get Request Statistics

```
get_request_stats()
```

## API Compliance

This MCP server implements the complete DocDocDoc API specification with:

- ✅ All request operations (CRUD)
- ✅ Document management
- ✅ Access control with expiration
- ✅ Webhook support
- ✅ Proper status management
- ✅ Document type validation
- ✅ File size and type validation
- ✅ Resource access via MCP resources

## Security Features

- API key authentication support (via `X-API-Key` header)
- Access expiration management
- File type and size validation
- Webhook secret generation
- Proper error handling and validation

## Notes

- File uploads are simulated in the MCP server (metadata only)
- Actual file storage would be implemented in the web server
- All data is stored in memory for demonstration purposes
- In production, use a proper database backend
