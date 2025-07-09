
"""Generate secure API keys for MCP server."""

import secrets
import argparse
import sys


def generate_key(length: int = 32) -> str:
    """Generate a secure API key.
    
    Args:
        length: Minimum length of the key in bytes
    
    Returns:
        A secure random API key
    """
    return secrets.token_urlsafe(length)


def main():
    """Generate API keys based on command line arguments."""
    parser = argparse.ArgumentParser(description="Generate secure API keys for MCP server")
    parser.add_argument("-n", "--num-keys", type=int, default=1, 
                       help="Number of keys to generate")
    parser.add_argument("-l", "--length", type=int, default=32,
                       help="Minimum key length in bytes")
    parser.add_argument("-f", "--format", choices=["plain", "env", "json"],
                       default="plain", help="Output format")
    
    args = parser.parse_args()
    
    if args.num_keys < 1:
        print("Number of keys must be at least 1", file=sys.stderr)
        sys.exit(1)
    
    if args.length < 16:
        print("WARNING: Short keys are less secure. Recommended length is 32+.",
             file=sys.stderr)
    
    # Generate keys
    keys = [generate_key(args.length) for _ in range(args.num_keys)]
    
    # Output in specified format
    if args.format == "plain":
        for i, key in enumerate(keys, 1):
            print(f"Key {i}: {key}")
    
    elif args.format == "env":
        print(f"MCP_API_KEYS={','.join(keys)}")
    
    elif args.format == "json":
        import json
        print(json.dumps({"api_keys": keys}, indent=2))


if __name__ == "__main__":
    main()
