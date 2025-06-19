import re


class CleanDataService:

    def clean_text(self, text):
        # Remove unwanted characters and multiple whitespace/newlines
        text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace/newlines with a single space
        text = re.sub(r'\\[a-z]', '', text)  # Remove escaped characters like \n, \t
        text = re.sub(r'\\', '', text)  # Remove any remaining backslashes
        text = text.strip()  # Remove leading and trailing whitespace
        return text

    def clean_data(self, data):
        cleaned_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                cleaned_data[key] = self.clean_text(value)  # Ensure to use self for the class method
            else:
                cleaned_data[key] = value
        return cleaned_data

    '''cleaned_data = clean_data(data)
    cleaned_json = json.dumps(cleaned_data, indent=4)
    print(cleaned_json)'''
