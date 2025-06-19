import requests


class VerifyDomain:
    def get_mx_via_doh(domain):
        """Fetch MX records using DNS-over-HTTPS for security."""
        url = f"https://cloudflare-dns.com/dns-query?name={domain}&type=MX"
        headers = {"Accept": "application/dns-json"}

        try:
            response = requests.get(url, headers=headers, timeout=3)
            response.raise_for_status()  # Raise error for bad HTTP responses
            data = response.json()

            # Extract MX records
            if "Answer" in data:
                mx_records = [ans["data"].split()[-1].rstrip('.') for ans in data["Answer"]]
                return mx_records
            return []

        except requests.Timeout:
            return "Error: Request timed out"
        except requests.RequestException as e:
            return f"Error: {e}"

    def get_email_provider(email):
        """Determines if an email is Gmail, Outlook, or other based on MX records."""
        domain = email.split("@")[-1]
        mx_records = VerifyDomain.get_mx_via_doh(domain)

        if isinstance(mx_records, str):  # Handle errors
            return mx_records

        # Check for Gmail or Outlook MX records
        if any("google.com" in mx for mx in mx_records):
            print("gmail account")
            return "Gmail"
        elif any("outlook.com" in mx or "protection.outlook.com" in mx for mx in mx_records):
            print("outlook account")
            return "Outlook"
        elif mx_records:
            return "Other / Custom Email Provider"
        else:
            return "Error: No MX records found"


email = "apurva.narate@redberyltech.com"
print(VerifyDomain.get_email_provider(email))
