# config/settings.py
"""Configuration settings for the DocDocDoc MCP server."""

import os
from typing import Optional

class Settings:
    """Configuration settings loaded from environment variables."""
    
    def __init__(self):
        self.api_key: Optional[str] = os.getenv("API_KEY")
        self.base_url: str = os.getenv("BASE_URL", "https://staging.docdocdoc.com")
    
    def validate(self) -> None:
        """Validate required settings."""
        if not self.api_key:
            raise ValueError("API_KEY environment variable is required")
    
    @property
    def is_configured(self) -> bool:
        """Check if all required settings are configured."""
        return self.api_key is not None

# Global settings instance
settings = Settings() 