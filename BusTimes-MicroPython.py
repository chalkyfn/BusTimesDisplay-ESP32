import network
import urequests as request
import time

def make_connection():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to the Network")
        wlan.connect("random", "chalky123")
        timeout = time.time() + 10  # 10 seconds timeout
        while not wlan.isconnected():
            if time.time() > timeout:
                print("Connection timed out")
                return False
            pass
    print("Connected:", wlan.isconnected())

make_connection()

url = "http://10.2.35.157:5000"
response = request.post(url)

if response.status_code == 200:
    print(response.json()["output"])
else:
    print("Error:", response.json()["output"])
