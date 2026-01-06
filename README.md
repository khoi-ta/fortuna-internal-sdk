# Fortuna Archetype API Client

Python client library for accessing the Fortuna Archetype API with HMAC SHA256 authentication.

## Installation

### From Source

```bash
cd python-client
pip install -e .
```

### Build Wheel

```bash
cd python-client
python -m build
# or
python setup.py bdist_wheel
```

The wheel file will be created in `dist/fortuna_archetype_client-1.0.0-py3-none-any.whl`

### Install from Wheel

```bash
pip install dist/fortuna_archetype_client-1.0.0-py3-none-any.whl
```

## Usage

```python
from fortuna_archetype_client import ArchetypeClient

# Initialize the client
client = ArchetypeClient(
    base_url="https://api.example.com",
    api_key="your-api-key",
    api_secret="your-api-secret"
)

# Get archetype IDs for a strategy
result = client.get_strategy_archetypes("A052")
print(result["archepids"])
# Output: ["A052071812-7a9581c6-...", "A052071813-8b0692d7-..."]

# Get a specific archetype
archetype = client.get_archetype("A052071812-7a9581c6-ad66-474b-a738-5d00ee9ec3c2")
print(archetype["archetypeportfolio"])
# Output: {"HSX:TPB": 0.35, "HSX:SSI": 0.25, ...}
```

## Authentication

The client uses HMAC SHA256 for request authentication. Each request includes:

- `X-API-Key`: Your API key
- `X-Timestamp`: Unix timestamp
- `X-Signature`: HMAC SHA256 signature

The signature is generated from: `METHOD|PATH|TIMESTAMP|BODY` (if body exists)

## Error Handling

```python
from fortuna_archetype_client import ArchetypeClient, ArchetypeAPIError, AuthenticationError

try:
    client = ArchetypeClient(...)
    result = client.get_archetype("invalid-id")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except ArchetypeAPIError as e:
    print(f"API error: {e}")
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black fortuna_archetype_client/

# Type checking
mypy fortuna_archetype_client/
```

## API Endpoints

### GET /internal/archetype/strategy/:sid

Get all archetype IDs for a strategy.

**Parameters:**
- `sid` (str): Strategy ID (4 characters)

**Returns:**
```python
{
    "archepids": ["A052071812-...", "A052071813-..."]
}
```

### GET /internal/archetype/:archepid

Get archetype by ID.

**Parameters:**
- `archepid` (str): Archetype ID

**Returns:**
```python
{
    "archetypeportfolio": {
        "HSX:TPB": 0.35,
        "HSX:SSI": 0.25,
        ...
    }
}
```

## License

MIT



