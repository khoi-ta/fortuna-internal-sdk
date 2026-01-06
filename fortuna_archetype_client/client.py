"""
Archetype API Client

This client provides methods to interact with the Fortuna Archetype API
using HMAC SHA256 authentication.
"""

import hmac
import hashlib
import time
import requests
from typing import Dict, List, Optional
from .exceptions import ArchetypeAPIError, AuthenticationError


class ArchetypeClient:
    """
    Client for interacting with the Fortuna Archetype API.
    
    Uses HMAC SHA256 for request authentication.
    
    Example:
        >>> client = ArchetypeClient(
        ...     base_url="https://api.example.com",
        ...     api_key="your-api-key",
        ...     api_secret="your-api-secret"
        ... )
        >>> archetypes = client.get_strategy_archetypes("A052")
        >>> archetype = client.get_archetype("A052071812-7a9581c6-...")
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: str,
        api_secret: str,
        timeout: int = 30,
    ):
        """
        Initialize the Archetype API client.
        
        Args:
            base_url: Base URL of the API (e.g., "https://api.example.com")
            api_key: API key for authentication
            api_secret: API secret for HMAC signature generation
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.api_secret = api_secret
        self.timeout = timeout
    
    def _generate_signature(
        self,
        method: str,
        path: str,
        timestamp: str,
        body: Optional[str] = None,
    ) -> str:
        """
        Generate HMAC SHA256 signature for the request.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            timestamp: Unix timestamp as string
            body: Request body as string (optional)
        
        Returns:
            Hexadecimal signature string
        """
        # Create the message to sign
        # Format: METHOD + PATH + TIMESTAMP + (BODY if exists)
        message_parts = [method.upper(), path, timestamp]
        if body:
            message_parts.append(body)
        
        message = "|".join(message_parts)
        
        # Generate HMAC SHA256 signature
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def _get_headers(self, method: str, path: str, body: Optional[str] = None) -> Dict[str, str]:
        """
        Generate authentication headers for the request.
        
        Args:
            method: HTTP method
            path: API endpoint path
            body: Request body as string (optional)
        
        Returns:
            Dictionary of headers
        """
        timestamp = str(int(time.time()))
        signature = self._generate_signature(method, path, timestamp, body)
        
        return {
            "X-API-Key": self.api_key,
            "X-Timestamp": timestamp,
            "X-Signature": signature,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Dict:
        """
        Make an authenticated HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path (e.g., "/internal/archetype/strategy/A052")
            params: URL query parameters (optional)
            json_data: JSON body data (optional)
        
        Returns:
            Response data as dictionary
        
        Raises:
            ArchetypeAPIError: If the API returns an error
            AuthenticationError: If authentication fails
        """
        url = f"{self.base_url}{path}"
        
        # Prepare body for signature if it exists
        body_str = None
        if json_data:
            import json
            body_str = json.dumps(json_data, sort_keys=True)
        
        headers = self._get_headers(method, path, body_str)
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                timeout=self.timeout,
            )
            
            # Handle authentication errors
            if response.status_code == 401:
                raise AuthenticationError("Authentication failed: Invalid API key or signature")
            
            # Handle other errors
            if response.status_code >= 400:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get("errmsg", f"API error: {response.status_code}")
                raise ArchetypeAPIError(
                    message=error_msg,
                    status_code=response.status_code,
                    error_code=error_data.get("errorcode"),
                )
            
            return response.json()
        
        except requests.exceptions.RequestException as e:
            raise ArchetypeAPIError(
                message=f"Request failed: {str(e)}",
                status_code=0,
            )
    
    def get_strategy_archetypes(self, sid: str) -> Dict[str, List[str]]:
        """
        Get all archetype IDs for a strategy.
        
        Args:
            sid: Strategy ID (4 characters, e.g., "A052")
        
        Returns:
            Dictionary with "archepids" key containing list of archetype IDs
        
        Example:
            >>> result = client.get_strategy_archetypes("A052")
            >>> print(result["archepids"])
            ["A052071812-7a9581c6-...", "A052071813-8b0692d7-..."]
        """
        path = f"/internal/archetype/strategy/{sid}"
        return self._make_request("GET", path)
    
    def get_archetype(self, archepid: str) -> Dict[str, Dict]:
        """
        Get archetype by ID.
        
        Args:
            archepid: Archetype ID (e.g., "A052071812-7a9581c6-ad66-474b-a738-5d00ee9ec3c2")
        
        Returns:
            Dictionary with "archetypeportfolio" key containing the portfolio allocation
        
        Example:
            >>> result = client.get_archetype("A052071812-7a9581c6-...")
            >>> print(result["archetypeportfolio"])
            {"HSX:TPB": 0.35, "HSX:SSI": 0.25, ...}
        """
        path = f"/internal/archetype/{archepid}"
        return self._make_request("GET", path)

