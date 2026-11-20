# Overview

Helper utilities for the MCP worker. `setup_path.py` mirrors the NukeScripts worker import layout. `conf_dump.py` reads the `[mcp]` block from `server.conf` like the launcher `load_config` dump. `config.py` merges that block with optional `NUKERAT_*` environment overrides.