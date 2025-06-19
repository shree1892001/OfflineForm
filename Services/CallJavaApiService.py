import requests


class CallJavaApiService:
    def __init__(self, base_url):
        self.base_url = base_url

    def java_api_call(self,method,data=None):
        try:
            response = requests.request(method=method, url=self.base_url, json=data, headers=self.form_headers())
            response.raise_for_status()
            if response:
                return response.json()
            else:
                return(f"API Call to {self.base_url}  | Failed. No response received.")
        except Exception as e:
            return "Not Found"

    def form_headers(self):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': "*/*"
        }
        return self.headers




