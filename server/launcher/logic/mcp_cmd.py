from launcher.utils.mcp import mcp_disable, mcp_enable, mcp_reauth

def main_mcp(option):
    # Receives the mcp command and calls enable, disable, or reauth
    parts = option.split()

    if len(parts) < 2 or parts[0] != "mcp":
        print("Invalid option")
        return

    action = parts[1]

    if action == "enable":
        if len(parts) != 2:
            print('Invalid syntax. Use "mcp enable".')
            return
        exit_code = mcp_enable()
        if exit_code:
            raise SystemExit(exit_code)
        return

    if action == "disable":
        if len(parts) != 2:
            print('Invalid syntax. Use "mcp disable".')
            return
        exit_code = mcp_disable()
        if exit_code:
            raise SystemExit(exit_code)
        return

    if action == "reauth":
        if len(parts) != 2:
            print('Invalid syntax. Use "mcp reauth".')
            return
        exit_code = mcp_reauth()
        if exit_code:
            raise SystemExit(exit_code)
        return

    print("Invalid option")