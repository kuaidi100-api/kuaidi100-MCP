# __init__.py
from .api_mcp import mcp

def main():
    """MCP KUAIDI100 API Server - HTTP call KUAIDI100 API for MCP"""
    mcp.run()

if __name__ == "__main__":
    main()