"""Constants and enums for the DocDocDoc MCP server."""

# Document types enum
DOCUMENT_TYPES = [
    "id_card", "passport", "driver_license", "residence_permit", 
    "statutes", "company_registration", "beneficials_owner_register"
]

# Access rights enum
ACCESS_RIGHTS = ["read", "write", "manage"]

# File validation
MAX_FILE_SIZE = 30 * 1024 * 1024  # 30MB

ALLOWED_MIME_TYPES = [
    "application/pdf", 
    "application/vnd.ms-excel", 
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/csv", 
    "image/jpeg", 
    "image/png"
] 