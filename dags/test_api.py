import json
import requests

def test_api():
    print("Starting API test...")
    try:
        print("Making API request to randomuser.me...")
        res = requests.get('https://randomuser.me/api/')
        res.raise_for_status()
        
        data = res.json()
        print(f"API DATA: {json.dumps(data, indent=2)}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"ERROR: API request failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    result = test_api()
    print("Test complete.")