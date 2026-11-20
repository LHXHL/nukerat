# MCP tools ↔ team server routes

Checklist against `server/core/routes`. `[x]` = at least one MCP tool hits the route; `[ ]` = not covered.

## Auth

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| POST /auth/login | env only | `nukerat_auth_login_info` (documents env auth, no live login) |
| POST /auth/check | x | `nukerat_auth_check` |

## /api/sessions

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/sessions/ | x | `nukerat_list_sessions` |
| PATCH /api/sessions/{tag} | x | `nukerat_patch_session` |
| DELETE /api/sessions/{tag} | x | `nukerat_delete_session` |

## /api/listeners

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/listeners/ | x | `nukerat_list_listeners` |
| POST /api/listeners/ | x | `nukerat_create_listener` |
| DELETE /api/listeners/{tag} | x | `nukerat_delete_listener` |

## /api/aes

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| POST /api/aes/create | x | `nukerat_create_aes_key` |

## /api/agents

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/agents/ | x | `nukerat_list_agents` |
| POST /api/agents/ | x | `nukerat_post_agent` |
| PATCH /api/agents/{tag} | x | `nukerat_patch_agent` |
| DELETE /api/agents/{tag} | x | `nukerat_delete_agent` |

## /api/credentials

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/credentials/ | x | `nukerat_list_credentials` |
| POST /api/credentials/ | x | `nukerat_create_credential` |
| PATCH /api/credentials/{tag} | x | `nukerat_patch_credential` |
| DELETE /api/credentials/{tag} | x | `nukerat_delete_credential` |

## /api/scripts

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/scripts/ | x | `nukerat_list_scripts` |
| POST /api/scripts/ | x | `nukerat_create_script` |
| PATCH /api/scripts/{tag} | x | `nukerat_patch_script` |
| DELETE /api/scripts/{tag} | x | `nukerat_delete_script` |

## /api/nsoutput

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/nsoutput/ | x | `nukerat_fetch_nsoutput` |

## /api/terminal

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| POST /api/terminal/ | x | `nukerat_terminal_command`, `nukerat_terminal_help`, `nukerat_terminal_command_with_file`, `nukerat_terminal_upload_raw`, `nukerat_terminal_download` |

## /api/explorer

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| POST /api/explorer/ | x | `nukerat_explorer_list`, `nukerat_explorer_download_file` |

## /api/process

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| POST /api/process/ | x | `nukerat_list_processes` |

## /api/implants

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| POST /api/implants/ | x | `nukerat_build_implant` |

## /api/file_server

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/file_server/{tag} | x | `nukerat_file_server_list` |
| GET /api/file_server/{tag}/files/{file_name}/download | x | `nukerat_file_server_download` |
| POST /api/file_server/{tag}/files/{file_name} | x | `nukerat_file_server_upload` |
| PATCH /api/file_server/{tag}/files/{file_name} | x | `nukerat_file_server_rename` |
| DELETE /api/file_server/{tag}/files/{file_name} | x | `nukerat_file_server_delete` |

## /api/screenshot

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/screenshot/{tag} | x | `nukerat_screenshot_get` |

## /api/keylogger

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/keylogger/ | x | `nukerat_keylogger_list` |
| DELETE /api/keylogger/{tag} | x | `nukerat_keylogger_delete` |

## /api/queue

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/queue/ | x | `nukerat_queue_list` |
| DELETE /api/queue/{tag} | x | `nukerat_queue_delete` |

## /api/iocs

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/iocs/ | x | `nukerat_list_iocs` |
| DELETE /api/iocs/{tag} | x | `nukerat_delete_ioc` |

## /api/logs

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/logs/ | x | `nukerat_list_logs` |

## /api/notifications

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/notifications/ | x | `nukerat_list_notifications` |
| GET /api/notifications/custom | x | `nukerat_list_custom_notifications` |

## /api/network

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/network/ | x | `nukerat_list_network` |
| POST /api/network/ | x | `nukerat_create_socks_network`, `nukerat_create_port_forward_network`, `nukerat_restart_network` |
| DELETE /api/network/{tag} | x | `nukerat_delete_network` |

## /api/reports

| Route | Covered | MCP tool(s) |
|-------|---------|-------------|
| GET /api/reports/ | x | `nukerat_list_reports` |
| POST /api/reports/ | x | `nukerat_create_report` |
| GET /api/reports/{tag}/download | x | `nukerat_download_report` |
| GET /api/reports/{tag}/view | x | `nukerat_view_report` |
| DELETE /api/reports/{tag} | x | `nukerat_delete_report` |