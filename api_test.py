from typing import Any, Dict
import requests
import time

port = "8001"
service_name = "http://api"
evaluate_url = f"{service_name}:{port}/evaluate"
ping_url = f"{service_name}:{port}/ping"


def send_request(filename: str) -> Dict[str, Any]:
    print("Sending request for file: " + filename)
    file = {"sample": open(filename, "rb")}
    response = requests.post(evaluate_url, files=file)
    print("Response status code: " + str(response.status_code))
    return response.json()


def wait_for_api(timeout: int = 60000) -> bool:
    start = time.time()
    while int((time.time() - start) * 1000) < timeout:
        print("Checking API availability...")
        try:
            response = requests.get(ping_url)
            if response.status_code == 200:
                print("API is now available.")
                return True
        except Exception as e:
            print(e)
        print("API is not available yet. Waiting 1 second before retry.")
        time.sleep(1)

    return False


if __name__ == "__main__":
    if not wait_for_api():
        print("Timeout, API is not up.")
        exit(1)
    print(send_request("dataset/test.JPEG"))
    print(send_request("dataset/test.png"))
