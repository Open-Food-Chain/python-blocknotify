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
this_node_pubkey = os.getenv("THIS_NODE_PUBKEY")

openfood_API_ORGANIZATION_CERTIFICATE_RULE_NORADDRESS = str(os.getenv("openfood_API_ORGANIZATION_CERTIFICATE_RULE_NORADDRESS"))
openfood_API_ORGANIZATION_CERTIFICATE_RULE = str(os.getenv("openfood_API_ORGANIZATION_CERTIFICATE_RULE"))
openfood_API_ORGANIZATION_CERTIFICATE = str(os.getenv("openfood_API_ORGANIZATION_CERTIFICATE"))

print("start getting the address less certificates")

url = IMPORT_API_BASE_URL + openfood_API_ORGANIZATION_CERTIFICATE_RULE_NORADDRESS
print("http://openfood-api.thenewfork.staging.do.unchain.io/api/v1/certificate-rule/noraddress/")

script_version = 0.00010006

def get_address(wallet, data):
    print("Creating an address using %s with data %s" % (wallet, data))
    signed_data = rpclib.signmessage(rpc_connect, wallet, data)
    #add the passphrase to the database
    print("Signed data is %s" % (signed_data))
    item_address = subprocess.getoutput("php genaddressonly.php " + signed_data)
    print("Created address %s" % (item_address))

    item_address = json.loads(item_address)

    return item_address


def create_multisig(addy, cert_id):
    cert_pubkey = ""
    try:
        url = IMPORT_API_BASE_URL + openfood_API_ORGANIZATION_CERTIFICATE + str(cert_id) + '/'
        res = requests.get(url)
        cert_pubkey = json.loads(res.text)['pubkey']
        print(cert_pubkey)

        if(len(cert_pubkey) < 66):
            message = "THIS IS A TEST !!!! IF THIS IS NOT A TEST ABORT"
            print(message)
            cert_pubkey = get_address(this_node_address, message)['pubkey']

        array = [addy, this_node_pubkey, cert_pubkey]

        res = rpclib.createmultisig(rpc_connect, 2, array)['address']

        return res

    except Exception as e:
        raise Exception(e)
    return

try:
    res = requests.get(url)
except Exception as e:
    raise Exception(e)

certs_no_addy = res.text

certs_no_addy = json.loads(certs_no_addy)

print(certs_no_addy)
#the issuer, issue date, expiry date, identifier (not the db id, the certificate serial number / identfier)
#RHzfsgzafuWb8PDouZqioa7c8NyQbuiQCS
for cert in certs_no_addy:
    raw_json = cert['condition']
    raw_json = json.dumps(raw_json)
    addy = get_address(this_node_address, raw_json)

    raw_json = json.loads(raw_json)
    mutlisig = create_multisig(addy['pubkey'], cert['certificate'])

    try:
        data={"raddress":mutlisig, "pubkey":addy['pubkey']}
        #res = requests.patch(url, data=data)
        print(res.text)

        url = IMPORT_API_BASE_URL + openfood_API_ORGANIZATION_CERTIFICATE + str(cert['certificate']) + '/'
        res = requests.get(url)
        cert_address = json.loads(res.text)['raddress']
        json= { addy['address']:script_version, cert_address:script_version }
        res = rpclib.sendmany(rpc_connect, "", json)
        print(res)
    except Exception as e:
        raise Exception(e)


# integrity/
