from lib import rpclib
from slickrpc import Proxy
import requests
import subprocess
import json
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)

IMPORT_API_HOST = str(os.getenv("IMPORT_API_HOST"))
IMPORT_API_PORT = str(os.getenv("IMPORT_API_PORT"))
IMPORT_API_BASE_URL =  IMPORT_API_HOST

rpc_user = os.getenv("IJUICE_KOMODO_NODE_USERNAME")
rpc_password = os.getenv("IJUICE_KOMODO_NODE_PASSWORD")
port = os.getenv("IJUICE_KOMODO_NODE_RPC_PORT")

komodo_node_ip = os.getenv("IJUICE_KOMODO_NODE_IPV4_ADDR")

rpc_connect = rpc_connection = Proxy("http://" + rpc_user + ":" + rpc_password + "@" + komodo_node_ip + ":" + port)

this_node_address = os.getenv("THIS_NODE_WALLET")

openfood_API_ORGANIZATION_CERTIFICATE_NORADDRESS = str(os.getenv("openfood_API_ORGANIZATION_CERTIFICATE_NORADDRESS"))
openfood_API_ORGANIZATION_CERTIFICATE = str(os.getenv("openfood_API_ORGANIZATION_CERTIFICATE"))

print("start getting the address less certificates")

url = IMPORT_API_BASE_URL + openfood_API_ORGANIZATION_CERTIFICATE_NORADDRESS

def get_address(wallet, data):
    print("Creating an address using %s with data %s" % (wallet, data))
    signed_data = rpclib.signmessage(rpc_connect, wallet, data)
    print("Signed data is %s" % (signed_data))
    item_address = subprocess.getoutput("php genaddressonly.php " + signed_data)
    print("Created address %s" % (item_address))

    item_address = json.loads(item_address)

    return item_address


try:
    res = requests.get(url)
except Exception as e:
    raise Exception(e)

certs_no_addy = res.text

certs_no_addy = json.loads(certs_no_addy)


#the issuer, issue date, expiry date, identifier (not the db id, the certificate serial number / identfier)

for cert in certs_no_addy:
    raw_json = {
        "issuer" : cert['issuer'],
        "issue_date": cert['date_issue'],
        "expiry_date": cert['date_expiry'],
        "identfier": cert['identifier']
    }
    raw_json = json.dumps(raw_json)
    addy = get_address(this_node_address, raw_json)
    id = str(cert['id'])
    url = IMPORT_API_BASE_URL + openfood_API_ORGANIZATION_CERTIFICATE + id + "/"

    try:
        data={"raddress": addy['address'], "pubkey": addy['pubkey']}
        res = requests.patch(url, data=data)
    except Exception as e:
        raise Exception(e)


# integrity/
