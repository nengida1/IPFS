import requests
import json
import base64


def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    # 🔐 Replace with your Infura project credentials
    project_id = "My First Key"
    project_secret = "+IkSUGUp+WR3xybxQpUEGZdsFxGGqKwXUoi5kqL7NtZDNnDw7xLJlA"

    auth = base64.b64encode(
        f"{project_id}:{project_secret}".encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {auth}"
    }

    url = "https://ipfs.infura.io:5001/api/v0/add"

    json_data = json.dumps(data)

    files = {
        "file": ("data.json", json_data)
    }

    response = requests.post(url, files=files, headers=headers)
    response.raise_for_status()

    cid = response.json()["Hash"]

    return cid


def get_from_ipfs(cid, content_type="json"):
    assert isinstance(cid, str), "get_from_ipfs accepts a cid in the form of a string"

    # 🔐 Replace with your Infura project credentials
    project_id = "YOUR_PROJECT_ID"
    project_secret = "YOUR_PROJECT_SECRET"

    auth = base64.b64encode(
        f"{project_id}:{project_secret}".encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {auth}"
    }

    url = f"https://ipfs.infura.io:5001/api/v0/cat?arg={cid}"

    response = requests.post(url, headers=headers)
    response.raise_for_status()

    data = json.loads(response.text)

    assert isinstance(data, dict), "get_from_ipfs should return a dict"

    return data
