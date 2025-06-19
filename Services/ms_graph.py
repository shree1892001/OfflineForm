import json
import os
import msal
from Constants.constant import *
from datetime import datetime

GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'


def generate_access_token(app_id, username, password, scopes):
    # Initialize the token cache
    access_token_cache = msal.SerializableTokenCache()

    # Read the token file if it exists and is not empty
    if os.path.exists(MsGraphJsonPath):
        try:
            with open(MsGraphJsonPath, "r") as token_file:
                file_content = token_file.read().strip()

                # Check if the file is empty or contains invalid content
                if not file_content:
                    print("Token file is empty, acquiring a new token.")
                else:
                    access_token_cache.deserialize(file_content)
                    token_detail = json.loads(file_content)

                    # Check if there is a valid access token
                    if 'AccessToken' in token_detail:
                        token_detail_key = list(token_detail['AccessToken'].keys())[0]
                        token_expiration = datetime.fromtimestamp(
                            int(token_detail['AccessToken'][token_detail_key]['expires_on']))

                        # If the token is still valid, return the token details
                        if datetime.now() < token_expiration:
                            print("Token is still valid. No need to re-authenticate.")
                            return token_detail
        except json.JSONDecodeError:
            print("Invalid JSON format in token file. Acquiring a new token.")

    # Use the tenant-specific or organizations authority
    client = msal.PublicClientApplication(
        client_id=app_id,
        authority=f"https://login.microsoftonline.com/organizations",  # or use your tenant ID
        token_cache=access_token_cache
    )

    # Acquire token by passing username and password
    token_response = client.acquire_token_by_username_password(username=username, password=password, scopes=scopes)

    if "error" in token_response:
        raise Exception(f"Failed to acquire token: {token_response.get('error_description')}")

    # Save the token cache to a file for future use
    with open(MsGraphJsonPath, 'w') as token_file:
        token_file.write(access_token_cache.serialize())

    return token_response



