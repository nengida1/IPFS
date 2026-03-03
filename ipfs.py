import requests
import json
import base64

CRED_DIR = "/home/codio/workspace"


def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    # Read Infura IPFS credentials
    with open(f"{CRED_DIR}/ipfs_project_id.txt", "r") as f:
        project_id = f.read().strip()

    with open(f"{CRED_DIR}/ipfs_project_secret.txt", "r") as f:
        project_secret = f.read().strip()

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

    gateways = [
        "https://ipfs.io/ipfs/",
        "https://cloudflare-ipfs.com/ipfs/",
        "https://gateway.pinata.cloud/ipfs/",
    ]

    last_err = None
    for base in gateways:
        try:
            url = f"{base}{cid}"
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            data = r.json()
            assert isinstance(data, dict), "get_from_ipfs should return a dict"
            return data
        except Exception as e:
            last_err = e

    raise RuntimeError(f"ERROR: reading {cid} from IPFS gateways. Last error: {last_err}")
