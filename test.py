import requests

API_URL_UPLOAD = "http://127.0.0.1:8000/upload"

try:
    # Send a POST request with an empty file to just test connectivity
    response = requests.post(API_URL_UPLOAD, files={"file": ("test.txt", b"test")})
    print("Backend reachable!")
    print("Status code:", response.status_code)
    print("Response:", response.text)
except requests.exceptions.ConnectionError:
    print("Backend NOT reachable. Check if it's running and the URL is correct.")
