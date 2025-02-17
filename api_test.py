from typing import Any, Dict
import requests

port = "8001"
service_name = "http://api"
evaluate_url = f"{service_name}:{port}/evaluate"


def send_request(filename: str) -> Dict[str, Any]:
    print("Sending request for file: " + filename)
    file = {"sample": open(filename, "rb")}
    response = requests.post(evaluate_url, files=file)
    print("Response status code: " + str(response.status_code))
    return response.json()


if __name__ == "__main__":
    print(send_request("dataset/logo.jpg"))
