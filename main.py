import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from server import mcp


def main():
    """Main entry point for the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
