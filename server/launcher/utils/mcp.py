import secrets
import string
from pathlib import Path
import bcrypt
from infra.database.database import User, sqlite_db_sync as sqlite_db
from launcher.utils.config import config_operations, config_set


def parse_operator_key_line(line):
    raw = str(line or "").strip()

    if raw.count(":") < 2:
        return "", "", ""

    name, passwd, key_secret = raw.split(":", 2)
    return name.strip(), passwd.strip(), key_secret.strip()


def provision_mcp_operator(username, force_new):
    sqlite_db.start()
    base = str(username or "").strip()

    if not base:
        print("MCP username is required")
        return 1

    if "/" in base or "\\" in base or base in (".", ".."):
        print("Invalid MCP username")
        return 1

    if len(base) > 150:
        print("MCP username must be less than 150 characters")
        return 1

    parser = config_operations("read")
    current_key = ""

    if parser.has_section("mcp"):
        current_key = parser.get("mcp", "operator_key", fallback="").strip()
        key_user, _, _ = parse_operator_key_line(current_key)

        if key_user and current_key and not force_new:
            return 0

    pool = string.ascii_letters + string.digits
    password = "".join(secrets.choice(pool) for _ in range(23))
    operator_key = "".join(secrets.choice(pool) for _ in range(256))
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    rows = sqlite_db.read(User, user=base)

    if rows:
        sqlite_db.modify(
            User,
            {"user": base},
            {"password_hash": password_hash, "secret": operator_key},
        )
        action = "updated"
    else:
        sqlite_db.write(User(user=base, password_hash=password_hash, secret=operator_key))
        action = "created"

    key_path = Path.cwd() / f"{base}.key"
    key_path.write_text(f"{base}:{password}:{operator_key}\n", encoding="utf-8")

    credential_line = f"{base}:{password}:{operator_key}"

    if config_set("mcp.operator_key", credential_line):
        return 1

    print(credential_line)
    print(f"MCP operator {action}: {base}")
    print(f"Saved: {key_path}")
    return 0


def mcp_enable():
    parser = config_operations("read")
    username = "mcp"

    raw = ""
    if parser.has_section("mcp"):
        raw = parser.get("mcp", "operator_key", fallback="").strip()
        key_user, key_pass, key_secret = parse_operator_key_line(raw)
        if key_user:
            username = key_user

    key_user, key_pass, key_secret = parse_operator_key_line(raw)
    missing_key = not (key_user and key_pass and key_secret)

    if missing_key:
        if provision_mcp_operator(username, True):
            return 1

    code = config_set("mcp.enabled", "true")

    if code:
        return code

    print("MCP server enabled")
    return 0

def mcp_disable():
    code = config_set("mcp.enabled", "false")

    if code:
        return code

    print("MCP server disabled")
    return 0

def mcp_reauth():
    parser = config_operations("read")
    username = "mcp"

    if parser.has_section("mcp"):
        raw = parser.get("mcp", "operator_key", fallback="").strip()
        key_user, _, _ = parse_operator_key_line(raw)
        if key_user:
            username = key_user

    if provision_mcp_operator(username, True):
        return 1

    print("MCP operator key recreated")
    return 0