import os
import subprocess
import sys
import webbrowser

import globus_sdk

from token_helpers import display_tokens, revoke_tokens


# The native app client ID is stored in an environment variable.
CLIENT_ID = os.getenv("CLIENT_ID", "").strip()
if not CLIENT_ID:
    print("ERROR: CLIENT_ID environment variable set.")
    sys.exit(1)


# Customize the named grant.
# If this is unspecified, it'll be a required input in the web app.
HOSTNAME = subprocess.check_output('hostname').decode("utf-8").strip()
NAMED_GRANT = f"Native app on {HOSTNAME}"


def main():
    get_default_scopes()


def get_default_scopes():
    # Get default scopes.
    client = globus_sdk.NativeAppAuthClient(client_id=CLIENT_ID)
    manager = client.oauth2_start_flow(
        prefill_named_grant=NAMED_GRANT,
        refresh_tokens=False,
    )
    authorize_url = manager.get_authorize_url()
    webbrowser.open(authorize_url)
    authorization_code = input("Type the authorization code here: ")
    tokens = manager.exchange_code_for_tokens(authorization_code)

    display_tokens(tokens, "scope", "resource_server", "token_type", "expires_in")
    revoke_tokens(client, tokens)


def get_refresh_tokens():
    # Get default scopes with refresh tokens.
    client = globus_sdk.NativeAppAuthClient(client_id=CLIENT_ID)
    manager = client.oauth2_start_flow(
        prefill_named_grant=NAMED_GRANT,
        refresh_tokens=True,
    )
    authorize_url = manager.get_authorize_url()
    webbrowser.open(authorize_url)
    authorization_code = input("Type the authorization code here: ")
    tokens = manager.exchange_code_for_tokens(authorization_code)

    display_tokens(tokens, "scope", "resource_server", "token_type", "expires_in")
    revoke_tokens(client, tokens)


if __name__ == "__main__":
    main()
