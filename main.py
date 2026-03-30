# main.py

# DeepSeek API Integration

import requests

class DeepSeek:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.deepseek.io/v1"

    def search(self, query):
        url = f"{self.base_url}/search"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(url, json={"query": query}, headers=headers)
        return response.json()  


if __name__ == '__main__':
    # Example usage
    api_key = 'your_api_key_here'
    deepseek = DeepSeek(api_key)
    results = deepseek.search("example search query")
    print(results)