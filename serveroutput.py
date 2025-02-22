import requests

url = "http://127.0.0.1:5000/run-script"
response = requests.post(url)

if response.status_code == 200:
    print("Script Output:", response.json()["output"])
else:
    print("Error:", response.json())