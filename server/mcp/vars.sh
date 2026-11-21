#!/usr/bin/env bash

root="$(cd "$(dirname "$0")/.." && pwd)"
conf="${root}/server.conf"

if [ ! -f "${conf}" ]; then
  echo "server.conf not found at ${conf}" >&2
  exit 1
fi

trim() {
  local v="$1"
  v="${v#"${v%%[![:space:]]*}"}"
  v="${v%"${v##*[![:space:]]}"}"
  printf '%s' "$v"
}

echo "Command: ${root}/venv/bin/python"
echo "Args:    ${root}/workers/mcp_server/main.py"
echo

mcp="$(grep -A 10 '^\[mcp\]' "${conf}")"

base_url="$(trim "$(echo "${mcp}" | grep -E '^[[:space:]]*base_url[[:space:]]*=' | head -1 | cut -d= -f2-)")"
tls_verify="$(trim "$(echo "${mcp}" | grep -E '^[[:space:]]*tls_verify[[:space:]]*=' | head -1 | cut -d= -f2-)")"
operator_key="$(trim "$(echo "${mcp}" | grep -E '^[[:space:]]*operator_key[[:space:]]*=' | head -1 | cut -d= -f2-)")"

if [ -z "${base_url}" ]; then
  srv="$(grep -A 15 '^\[server\]' "${conf}")"
  host="$(trim "$(echo "${srv}" | grep -E '^[[:space:]]*host[[:space:]]*=' | head -1 | cut -d= -f2-)")"
  port="$(trim "$(echo "${srv}" | grep -E '^[[:space:]]*port[[:space:]]*=' | head -1 | cut -d= -f2-)")"
  tls="$(trim "$(grep -A 5 '^\[server.tls\]' "${conf}" | grep -E '^[[:space:]]*tls[[:space:]]*=' | head -1 | cut -d= -f2-)")"
  [ -z "${host}" ] && host="127.0.0.1"
  [ -z "${port}" ] && port="9000"
  case "${host}" in 0.0.0.0 | :: | "[::]") host="127.0.0.1" ;; esac
  case "$(printf '%s' "${tls}" | tr '[:upper:]' '[:lower:]')" in
    true | 1 | yes | on) scheme="https" ;;
    *) scheme="http" ;;
  esac
  base_url="${scheme}://${host}:${port}"
fi

[ -z "${tls_verify}" ] && tls_verify="true"

echo "NUKERAT_BASE_URL=${base_url}"
echo "NUKERAT_TLS_VERIFY=${tls_verify}"
[ -n "${operator_key}" ] && echo "NUKERAT_OPERATOR_KEY=${operator_key}"