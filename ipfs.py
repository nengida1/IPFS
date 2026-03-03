import requests
import json
import base64

CRED_DIR = "/home/codio/workspace"


def pin_to_ipfs(data):
    assert isinstance(data, dict), "Error pin_to_ipfs expects a dictionary"

    with open(f"{CRED_DIR}/pinata_jwt.txt", "r") as f:
        jwt = f.read().strip()

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }

    resp = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
    resp.raise_for_status()

    cid = resp.json()["IpfsHash"]
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
