"""
Custom exceptions for the Archetype API client.
"""

from typing import Optional


class ArchetypeAPIError(Exception):
    """Base exception for API errors."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 0,
        error_code: Optional[int] = None,
    ):
        """
        Initialize the API error.
        
        Args:
            message: Error message
            status_code: HTTP status code
            error_code: API error code (if available)
        """
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.status_code}] Error {self.error_code}: {self.message}"
        return f"[{self.status_code}] {self.message}"


class AuthenticationError(ArchetypeAPIError):
    """Exception raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)

