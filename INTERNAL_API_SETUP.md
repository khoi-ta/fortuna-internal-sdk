# Internal API Setup Guide

This guide explains how to set up and use the internal Archetype API with HMAC SHA256 authentication.

## Environment Variables

Add these to your `.env` file:

```env
INTERNAL_API_KEY=your-secure-api-key-here
INTERNAL_API_SECRET=your-secure-api-secret-here
```

**Security Note:** Use strong, randomly generated values for both keys. You can generate them using:

```bash
# Generate API Key (32 characters)
openssl rand -hex 16

# Generate API Secret (64 characters)
openssl rand -hex 32
```

## API Endpoints

### GET /internal/archetype/strategy/:sid

Get all archetype IDs for a strategy.

**Authentication:** HMAC SHA256

**Example:**
```bash
curl -X GET "http://localhost:3000/internal/archetype/strategy/A052" \
  -H "X-API-Key: your-api-key" \
  -H "X-Timestamp: 1234567890" \
  -H "X-Signature: generated-hmac-signature"
```

### GET /internal/archetype/:archepid

Get archetype by ID.

**Authentication:** HMAC SHA256

**Example:**
```bash
curl -X GET "http://localhost:3000/internal/archetype/A052071812-7a9581c6-..." \
  -H "X-API-Key: your-api-key" \
  -H "X-Timestamp: 1234567890" \
  -H "X-Signature: generated-hmac-signature"
```

## HMAC Signature Generation

The signature is generated using HMAC SHA256 with the following message format:

```
METHOD|PATH|TIMESTAMP|BODY
```

Where:
- `METHOD`: HTTP method (GET, POST, etc.) in uppercase
- `PATH`: Full request path (e.g., `/internal/archetype/strategy/A052`)
- `TIMESTAMP`: Unix timestamp as string
- `BODY`: JSON stringified request body (only for POST/PUT/PATCH requests, sorted keys)

### Example (GET request):

```
Message: GET|/internal/archetype/strategy/A052|1234567890
Secret: your-api-secret
Signature: HMAC-SHA256(message, secret)
```

### Example (POST request with body):

```
Body: {"key": "value"}
Message: POST|/internal/archetype|1234567890|{"key":"value"}
Secret: your-api-secret
Signature: HMAC-SHA256(message, secret)
```

## Python Client Usage

See `README.md` in the `python-client` directory for detailed usage examples.

## Security Considerations

1. **Timestamp Validation:** Requests are rejected if the timestamp is more than 5 minutes old or in the future (prevents replay attacks)

2. **Timing-Safe Comparison:** Signature comparison uses timing-safe comparison to prevent timing attacks

3. **API Key Validation:** The API key must match exactly

4. **HTTPS:** Always use HTTPS in production to protect the API key and secret in transit

## Testing

You can test the internal API using the Python client:

```python
from fortuna_archetype_client import ArchetypeClient

client = ArchetypeClient(
    base_url="http://localhost:3000",
    api_key="your-api-key",
    api_secret="your-api-secret"
)

# Test getting strategy archetypes
result = client.get_strategy_archetypes("A052")
print(result)

# Test getting specific archetype
archetype = client.get_archetype("A052071812-...")
print(archetype)
```


