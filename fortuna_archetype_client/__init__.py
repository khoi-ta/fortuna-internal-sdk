"""
Fortuna Archetype API Client

A Python client for accessing the Fortuna Archetype API with HMAC SHA256 authentication.
"""

from .client import ArchetypeClient
from .exceptions import ArchetypeAPIError, AuthenticationError

__version__ = "1.0.0"
__all__ = ["ArchetypeClient", "ArchetypeAPIError", "AuthenticationError"]


