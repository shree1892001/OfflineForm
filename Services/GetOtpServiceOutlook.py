import re
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
from Services.ms_graph import generate_access_token
from Constants.constant import *


class GetOtpServiceOutlook:
    def __init__(self, username, password, subject_filter=None):
        self.username = username
        self.password = password
        self.subject_filter = subject_filter
        self.headers = None
        self.authenticate()

    def authenticate(self, max_retries=3, retry_delay=5):
        for attempt in range(1, max_retries + 1):
            try:
                # Generate the access token
                access_token = generate_access_token(APP_ID, self.username, self.password, scopes)

                # Validate if 'AccessToken' exists
                if 'AccessToken' not in access_token:
                    raise KeyError("'AccessToken' key is missing in the response.")

                # Extract the token key and secret
                token_key = next(iter(access_token['AccessToken']))
                access_token_secret = access_token['AccessToken'][token_key]['secret']

                # Set headers
                self.headers = {
                    'Authorization': f'Bearer {access_token_secret}'
                }
                return  # Exit the function upon success

            except Exception as e:
                if attempt < max_retries:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Maximum retry attempts reached. Authentication failed.")
                    raise

    def list_emails_by_subject(self, subject, wait_time=2, retry_limit=12):
        retries = 0
        while retries < retry_limit:
            now_utc = datetime.utcnow()
            two_minutes_ago = now_utc - timedelta(seconds=45)
            one_hour_ago_str = two_minutes_ago.strftime('%Y-%m-%dT%H:%M:%SZ')  # Format to 'YYYY-MM-DDTHH:MM:SSZ'

            print(f"Fetching emails received after: {one_hour_ago_str}")

            params = {
                '$top': 15,  # Limit to 15 emails
                '$select': 'subject,hasAttachments,bodyPreview,receivedDateTime',  # Add receivedDateTime
                '$count': 'true'
            }

            self.subject_filter = params[
                '$filter'] = f"contains(subject, '{subject}') and receivedDateTime ge {one_hour_ago_str}"

            response = requests.get(GRAPH_API_ENDPOINT + '/me/mailFolders/inbox/messages', headers=self.headers,
                                    params=params)

            if response.status_code != 200:
                print(f"An error occurred: {response.json()}")
                return None

            emails = response.json().get('value', [])

            if not emails:
                print(
                    f"No emails found with subject containing: {subject} and received in the last hour. Waiting for new emails...")
                time.sleep(wait_time)
                retries += 1
                continue

            for email in emails:
                received_time = self.parse_date(email['receivedDateTime'])
                print(f"Email found: {email['subject']} received at {received_time}")

                if received_time and received_time >= two_minutes_ago:
                    print(f"Email received within the last hour: {email['subject']} at {received_time}")
                    return email

            print("Found emails, but none were received in the last hour.")
            time.sleep(wait_time)
            retries += 1

        print("No new emails found after multiple attempts.")
        return None

    def get_email_body(self, email_id):
        try:
            response = requests.get(f"{GRAPH_API_ENDPOINT}/me/messages/{email_id}", headers=self.headers)
            if response.status_code != 200:
                raise Exception(response.json())

            email_details = response.json()
            body_content = email_details['body']['content']
            verification_code = self.extract_verification_code(body_content)
            return verification_code if verification_code else "No verification code found."

        except Exception as error:
            print(f"An error occurred while fetching email body: {error}")
            return None

    def extract_verification_code(self, body):
        try:
            soup = BeautifulSoup(body, 'html.parser')
            p_tags = soup.find_all('p')
            text = soup.get_text()
            code_match = re.search(r'\b\d{6}\b', text)

            for p in p_tags:
                if "Verification code:" in p.get_text():
                    next_p = p.find_next('p')
                    if next_p:
                        code = next_p.get_text().strip()
                        return code
                elif "Authentication code for user is:" in p.get_text():
                    next_p = p.find_next('p')
                    if next_p:
                        code = next_p.get_text().strip()
                        return code
            if "UtahID One Time Password" in text:
                code = code_match.group(0)  # Get the matched 6-digit code
                return code
            return None
        except Exception as e:
            print(f"Error extracting verification code: {e}")
            return None

    def parse_date(self, date_string):
        try:
            try:
                return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        except Exception as error:
            print(f"Error parsing date: {error}")
        return None


