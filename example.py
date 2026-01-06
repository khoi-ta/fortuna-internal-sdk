"""
Example usage of the Fortuna Archetype API Client.
"""

from fortuna_archetype_client import ArchetypeClient, ArchetypeAPIError, AuthenticationError

def main():
    # Initialize the client
    client = ArchetypeClient(
        base_url="http://localhost:3000",  # Replace with your API base URL
        api_key="your-api-key-here",        # Replace with your API key
        api_secret="your-api-secret-here",  # Replace with your API secret
        timeout=30,
    )

    try:
        # Example 1: Get archetype IDs for a strategy
        print("Fetching archetype IDs for strategy A052...")
        result = client.get_strategy_archetypes("A052")
        print(f"Found {len(result['archepids'])} archetypes:")
        for archepid in result['archepids']:
            print(f"  - {archepid}")

        # Example 2: Get a specific archetype
        if result['archepids']:
            archepid = result['archepids'][0]
            print(f"\nFetching archetype: {archepid}...")
            archetype = client.get_archetype(archepid)
            print("Archetype portfolio:")
            for symbol, allocation in archetype['archetypeportfolio'].items():
                print(f"  {symbol}: {allocation}")

    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
    except ArchetypeAPIError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()


