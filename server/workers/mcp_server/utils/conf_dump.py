import configparser
from pathlib import Path

def parse_bool(value, default):
    # Interprets boolean strings the same way as the launcher config loader

    if value is None:
        return default

    text = str(value).strip().lower()

    if text in ("1", "true", "yes", "on"):
        return True

    if text in ("0", "false", "no", "off"):
        return False

    return default

def server_conf_path():
    # Points at server.conf next to the team server root
    return Path(__file__).resolve().parents[3] / "server.conf"

def read_server_conf():
    # Opens server.conf into a ConfigParser or returns an empty parser
    parser = configparser.ConfigParser(interpolation=None)
    path = server_conf_path()

    if path.is_file():
        parser.read(path, encoding="utf-8")

    return parser

def server_public_url(parser):
    # Builds a team server base URL from [server] and [server.tls] when mcp.base_url is empty

    if not parser.has_section("server"):
        return ""

    host = parser.get("server", "host", fallback="127.0.0.1").strip() or "127.0.0.1"
    port = parser.get("server", "port", fallback="9000").strip() or "9000"
    tls = False

    if parser.has_section("server.tls"):
        raw = parser.get("server.tls", "tls", fallback="false").strip().lower()
        tls = raw in ("1", "true", "yes", "on")

    scheme = "https" if tls else "http"

    if host in ("0.0.0.0", "::", "[::]"):
        host = "127.0.0.1"

    return f"{scheme}://{host}:{port}"

def mcp_text(parser, key, default=""):
    # Reads one string from the mcp section

    if not parser.has_section("mcp"):
        return default

    raw = parser.get("mcp", key, fallback=default).strip()
    return raw if raw else default

def dump_mcp_config():
    # Extracts the mcp block from server.conf like launcher load_config does for other workers
    try:
        from launcher.utils.config import config

        block = config.get("mcp")

        if isinstance(block, dict) and block:
            return block

    except Exception:
        pass

    parser = read_server_conf()
    enabled = parse_bool(mcp_text(parser, "enabled", "false"), False)
    base_url = mcp_text(parser, "base_url", "")

    if not base_url:
        base_url = server_public_url(parser)

    tls_verify = parse_bool(mcp_text(parser, "tls_verify", "true"), True)
    operator_key = mcp_text(parser, "operator_key", "")

    return {
        "enabled": enabled,
        "base_url": base_url.rstrip("/") if base_url else "",
        "operator_key": operator_key,
        "tls_verify": tls_verify,
    }