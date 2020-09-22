from lib import rpclib
from slickrpc import Proxy
import requests
import subprocess
import json
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)


# global vars
rpc_user = os.getenv("IJUICE_KOMODO_NODE_USERNAME")
rpc_password = os.getenv("IJUICE_KOMODO_NODE_PASSWORD")
port = os.getenv("IJUICE_KOMODO_NODE_RPC_PORT")

komodo_node_ip = os.getenv("IJUICE_KOMODO_NODE_IPV4_ADDR")

this_node_address = os.getenv("THIS_NODE_WALLET")
this_node_pubkey = os.getenv("THIS_NODE_PUBKEY")
this_node_wif = os.getenv("THIS_NODE_WIF")

# rpc_connect = rpc_connection = Proxy("http://%s:%s@127.0.0.1:%d" % (rpc_user, rpc_password, port))
rpc_connect = rpc_connection = Proxy("http://" + rpc_user + ":" + rpc_password + "@" + komodo_node_ip + ":" + port)

blocknotify_chainsync_limit = int(os.getenv("BLOCKNOTIFY_CHAINSYNC_LIMIT"))
housekeeping_address = os.getenv("HOUSEKEEPING_ADDRESS")


IMPORT_API_HOST = str(os.getenv("IMPORT_API_HOST"))
IMPORT_API_PORT = str(os.getenv("IMPORT_API_PORT"))
IMPORT_API_BASE_URL = "http://" + IMPORT_API_HOST + ":" + IMPORT_API_PORT + "/"
# integrity/
DEV_IMPORT_API_JCF_BATCH_INTEGRITY_PATH = os.getenv("DEV_IMPORT_API_JCF_BATCH_INTEGRITY_PATH")
# batch/require_integrity/
DEV_IMPORT_API_JCF_BATCH_REQUIRE_INTEGRITY_PATH = os.getenv("DEV_IMPORT_API_JCF_BATCH_REQUIRE_INTEGRITY_PATH")
# raw/refresco/require_integrity/
DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH = os.getenv("DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH")
# raw/refresco-integrity/
DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH = os.getenv("DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH")


JUICYCHAIN_API_HOST = str(os.getenv("JUICYCHAIN_API_HOST"))
JUICYCHAIN_API_PORT = str(os.getenv("JUICYCHAIN_API_PORT"))
JUICYCHAIN_API_VERSION_PATH = str(os.getenv("JUICYCHAIN_API_VERSION_PATH"))
JUICYCHAIN_API_BASE_URL = "http://" + JUICYCHAIN_API_HOST + ":" + JUICYCHAIN_API_PORT + "/" + JUICYCHAIN_API_VERSION_PATH

JUICYCHAIN_API_ORGANIZATION_CERTIFICATE = os.getenv("JUICYCHAIN_API_ORGANIZATION_CERTIFICATE")
JUICYCHAIN_API_ORGANIZATION_CERTIFICATE_RULE = os.getenv("JUICYCHAIN_API_ORGANIZATION_CERTIFICATE")

# check wallet management
is_mine = rpclib.validateaddress(rpc_connect, this_node_address)['ismine']

if is_mine is False:
    rpclib.importprivkey(rpc_connect, this_node_wif)

is_mine = rpclib.validateaddress(rpc_connect, this_node_address)['ismine']

# start housekeeping

# we send this amount to an address for housekeeping
# update by 0.0001 (manually, if can be done in CI/CD, nice-to-have not need-to-have) (MYLO)
# house keeping address is list.json last entry during dev
script_version = 0.00010006

general_info = rpclib.getinfo(rpc_connect)
sync = general_info['longestchain'] - general_info['blocks']

print(general_info['longestchain'])

print(general_info['blocks'])

print(sync)

if sync >= blocknotify_chainsync_limit:
    print('the chain is not synced, try again later')
    exit()

print("the chain is synced")

# send a small amount (SCRIPT_VERSION) for HOUSEKEEPING_ADDRESS from each organization
# ############################
# info: for external documentation then remove from here
# one explorer url to check is
# IJUICE  http://seed.juicydev.coingateways.com:24711/address/RS7y4zjQtcNv7inZowb8M6bH3ytS1moj9A
# POS95   http://seed.juicydev.coingateways.com:54343/address/RS7y4zjQtcNv7inZowb8M6bH3ytS1moj9A
# ############################
# send SCRIPT_VERSION, increment by 0.00000001 for each update

res = rpclib.sendtoaddress(rpc_connect, housekeeping_address, script_version)

print(res)

# ############################

# END OF HOUSEKEEPING

# ##############################################################################

# ##############################################################################

# START JCF IMPORT API INTEGRITY CHECKS

# JCF is the only part of script that refers to BATCH.
# development of new partners can use RAW_REFRESCO-like variables

###########################
# organization R-address = $1
# raw_json import data in base64 = $2
# batch record import database id(uuid) = $3
###########################


def import_jcf_batch_integrity_pre_process(wallet, data, import_id):

    data = json.dumps(data)

    signed_data = rpclib.signmessage(rpc_connect, wallet, data)
    item_address = subprocess.getoutput("php genaddressonly.php " + signed_data)

    item_address = json.loads(item_address)

    print(item_address['address'])

    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_JCF_BATCH_INTEGRITY_PATH
    data = {'name': 'chris', 'integrity_address': item_address['address'], 'batch': import_id}

    res = requests.post(url, data=data)

    print(res.text)

    id = json.loads(res.text)['id']

    print(id)

    response = rpclib.sendtoaddress(rpc_connect, item_address['address'], script_version)

    print(response)

    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_JCF_BATCH_INTEGRITY_PATH + id + "/"
    data = {'name': 'chris', 'integrity_address': item_address['address'], 'integrity_pre_tx': response}

    res = requests.put(url, data=data)

    print(res.text)

    return


def get_address(wallet, data):
    print("Creating an address using %s with data %s" % (wallet, data))
    signed_data = rpclib.signmessage(rpc_connect, wallet, data)
    print("Signed data is %s" % (signed_data))
    item_address = subprocess.getoutput("php genaddressonly.php " + signed_data)
    print("Created address %s" % (item_address))

    item_address = json.loads(item_address)['address']

    return item_address


def import_raw_refresco_batch_integrity_pre_process(wallet, data, import_id):

    ANFP = data['anfp']
    PON = data['pon']
    BNFP = data['bnfp']

    anfp_address = get_address(wallet, ANFP)
    pon_address = get_address(wallet, PON)
    bnfp_address = get_address(wallet, BNFP)

    data = json.dumps(data)

    signed_data = rpclib.signmessage(rpc_connect, wallet, data)
    item_address = subprocess.getoutput("php genaddressonly.php " + signed_data)

    item_address = json.loads(item_address)

    print(item_address['address'])

    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH
    data = {'name': 'chris', 'integrity_address': item_address['address'], 'batch': import_id}

    res = requests.post(url, data=data)

    print(res.text)

    id = json.loads(res.text)['id']

    print(id)

    response = rpclib.sendtoaddress(rpc_connect, item_address['address'], script_version)

    print(response)

    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH + id + "/"
    data = {'name': 'chris', 'integrity_address': item_address['address'], 'integrity_pre_tx': response}

    res = requests.put(url, data=data)

    print(res.text)

    json_object = {anfp_address: script_version, pon_address: script_version, bnfp_address: script_version}

    response = rpclib.sendmany(rpc_connect, this_node_address, json_object)

    print(response)

    return


def juicychain_certificate_address_creation(wallet, data, db_id):

    print("## JUICYCHAIN API ##")

    data = json.dumps(data)

    signed_data = rpclib.signmessage(rpc_connect, wallet, data)
    item_address = subprocess.getoutput("php genaddressonly.php " + signed_data)

    item_address = json.loads(item_address)

    print(item_address['address'])

    url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + "66/"
    data = {'raddress': item_address['address']}

    res = requests.patch(url, data=data)  # , headers={"Content-Type": "application/json"})

    print(res.text)

    # id = json.loads(res.text)['id']

    # print(id)

    response = rpclib.sendtoaddress(rpc_connect, item_address['address'], script_version)

    print(response)

    return


def sign_message():
    return


print("start improt api")

url = IMPORT_API_BASE_URL + DEV_IMPORT_API_JCF_BATCH_REQUIRE_INTEGRITY_PATH

res = requests.get(url)

raw_json = res.text

# batches_null_integrity = array(batches_null_integrity)

batches_null_integrity = ""

try:
    batches_null_integrity = json.loads(raw_json)
except Exception as e:
    print("failed to parse to json because of", e)
    exit()


for batch in batches_null_integrity:
    raw_json = batch
    id = batch['id']
    print("starting process for id:", id)
    import_jcf_batch_integrity_pre_process(this_node_address, raw_json, id)


print("start improt api")

url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH

res = requests.get(url)

print(res.text)

raw_json = res.text

# batches_null_integrity = array(batches_null_integrity)

batches_null_integrity = ""

try:
    batches_null_integrity = json.loads(raw_json)
except Exception as e:
    print("failed to parse to json because of", e)
    exit()

for batch in batches_null_integrity:
    raw_json = batch
    id = batch['id']
    print("starting process for id:", id)
    import_raw_refresco_batch_integrity_pre_process(this_node_address, raw_json, id)

juicychain_certificate_address_creation(this_node_address, "FAKEDATA567", "66")

exit()
