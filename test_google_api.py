import os
import requests

def test_google_search():
    API_KEY = os.environ.get("GOOGLE_SEARCH_API_KEY")
    SEARCH_ENGINE_ID = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")
    
    search_term = "test"
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={search_term}&searchType=image"
    
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.json().get('error', {}).get('message', 'Unknown error')}")
    else:
        print("API is working correctly!")

if __name__ == "__main__":
    test_google_search()
