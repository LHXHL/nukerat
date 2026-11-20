import os
import re
from urllib.parse import urlparse
from utils import conf_dump

base_url = ""
tls_verify = True
operator_key_line = ""
operator_user = ""
operator_pass = ""
operator_secret = ""
enabled = False
host_tag_pattern = re.compile(r"^[A-Za-z0-9]{3,32}$")
command_max_chars = 8192
binary_max_bytes = 52428800

def parse_bool(value, default):
    # Interprets common truthy and falsy env strings

    if value is None:
        return default

    text = str(value).strip().lower()

    if text in ("1", "true", "yes", "on"):
        return True

    if text in ("0", "false", "no", "off"):
        return False

    return default

def apply_conf_block(block):
    # Copies one mcp dict from server.conf into module-level settings
    global enabled, base_url, tls_verify
    global operator_key_line, operator_user, operator_pass, operator_secret

    if not isinstance(block, dict):
        return

    enabled = bool(block.get("enabled"))

    if block.get("base_url"):
        base_url = str(block.get("base_url", "")).strip().rstrip("/")

    raw_key = str(block.get("operator_key", "")).strip()

    operator_key_line = ""
    operator_user = ""
    operator_pass = ""
    operator_secret = ""

    if raw_key.count(":") >= 2:
        parts = raw_key.split(":", 2)
        operator_user = parts[0].strip()
        operator_pass = parts[1].strip()
        operator_secret = parts[2].strip()

        if operator_user and operator_pass and operator_secret:
            operator_key_line = raw_key

    if "tls_verify" in block:
        tls_verify = bool(block.get("tls_verify"))

def apply_env_overrides():
    # Environment variables win over server.conf for operator-specific secrets
    global base_url, tls_verify
    global operator_key_line, operator_user, operator_pass, operator_secret
    env_base = os.environ.get("NUKERAT_BASE_URL", "").strip()

    if env_base:
        base_url = env_base.rstrip("/")

    env_key = os.environ.get("NUKERAT_OPERATOR_KEY", "").strip()

    if env_key.count(":") >= 2:
        parts = env_key.split(":", 2)
        operator_user = parts[0].strip()
        operator_pass = parts[1].strip()
        operator_secret = parts[2].strip()

        if operator_user and operator_pass and operator_secret:
            operator_key_line = env_key

    if "NUKERAT_TLS_VERIFY" in os.environ:
        tls_verify = parse_bool(os.environ.get("NUKERAT_TLS_VERIFY"), tls_verify)

def validate_base_url():
    # Ensures we have a usable team server URL before any HTTP tool runs
    global base_url

    if not base_url:
        raise RuntimeError("mcp.base_url or NUKERAT_BASE_URL is required")

    parsed = urlparse(base_url)

    if parsed.scheme not in ("http", "https"):
        raise RuntimeError("mcp.base_url must start with http:// or https://")

    if not parsed.netloc:
        raise RuntimeError("mcp.base_url host is missing")

    base_url = base_url.rstrip("/")

def load_settings():
    # Loads MCP connection settings from server.conf, then environment overrides
    apply_conf_block(conf_dump.dump_mcp_config())
    apply_env_overrides()
    validate_base_url()