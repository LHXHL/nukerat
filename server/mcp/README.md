# MCP Server

This folder holds utility files for setting up the NukeRat MCP server.

- `template.json`: base configuration JSON for agents that use JSON, for example Cursor
- `vars.sh`: helper script that prints the paths you need to configure the MCP server in some tools

# Where is the MCP server?

The `server/mcp` folder is only for helpers. All MCP server logic lives under `server/workers/mcp_server`.

# Tutorials

If you want to integrate the NukeRat MCP server with a tool or agent, see:

- https://nukerat.com/docs/mcp/