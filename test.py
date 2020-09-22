from lib import rpclib
from slickrpc import Proxy
import requests
import subprocess
import json


# global vars
rpc_user = "changeme"
rpc_password = "alsochangeme"
port = 24708

komodo_node_ip = "172.29.0.2"

this_node_address = "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW"
this_node_pubkey = "02f2cdd772ab57eae35996c0d39ad34fe06304c4d3981ffe71a596634fa26f8744"
this_node_wif = "UpUiqKNj43SBPe9SvYqpygZE3BS83f87GVQSV8zXt2Gr813YZ3Ah"

rpc_connect = rpc_connection = Proxy("http://%s:%s@127.0.0.1:%d" % (rpc_user, rpc_password, port))


django_base_url = "http://172.29.0.4:8777/"
DEV_IMPORT_API_JCF_BATCH_INTEGRITY_PATH = "integrity/"
DEV_IMPORT_API_JCF_BATCH_REQUIRE_INTEGRITY_PATH = "raw/refresco/require_integrity/"
DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH = "raw/refresco/require_integrity/"
DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH = "raw/refresco-integrity/"

blocknotify_chainsync_limit = 5
housekeeping_address = "RS7y4zjQtcNv7inZowb8M6bH3ytS1moj9A"


# check wallet management
is_mine = rpclib.validateaddress(rpc_connect, this_node_address)['ismine']

if is_mine is False:
    rpclib.importprivkey(rpc_connect, this_node_wif)

is_mine = rpclib.validateaddress(rpc_connect, this_node_address)['ismine']

# start housekeeping

# we send this amount to an address for housekeeping
# update by 0.0001 (manually, if can be done in CI/CD, nice-to-have not need-to-have) (MYLO)
# house keeping address is list.json last entry during dev
script_version = 0.00010005

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

    url = django_base_url + DEV_IMPORT_API_JCF_BATCH_INTEGRITY_PATH
    data = {'name': 'chris', 'integrity_address': item_address['address'], 'batch': import_id}

    res = requests.post(url, data=data)

    print(res.text)

    id = json.loads(res.text)['id']

    print(id)

    response = rpclib.sendtoaddress(rpc_connect, item_address['address'], script_version)

    print(response)

    url = django_base_url + DEV_IMPORT_API_JCF_BATCH_INTEGRITY_PATH + id + "/"
    data = {'name': 'chris', 'integrity_address': item_address['address'], 'integrity_pre_tx': response}

    res = requests.put(url, data=data)

    print(res.text)

    return


def get_address(wallet, data):
    signed_data = rpclib.signmessage(rpc_connect, wallet, data)
    item_address = subprocess.getoutput("php genaddressonly.php " + signed_data)

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

    url = django_base_url + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH
    data = {'name': 'chris', 'integrity_address': item_address['address'], 'batch': import_id}

    res = requests.post(url, data=data)

    print(res.text)

    id = json.loads(res.text)['id']

    print(id)

    response = rpclib.sendtoaddress(rpc_connect, item_address['address'], script_version)

    print(response)

    url = django_base_url + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH + id + "/"
    data = {'name': 'chris', 'integrity_address': item_address['address'], 'integrity_pre_tx': response}

    res = requests.put(url, data=data)

    print(res.text)

    json_object = {anfp_address: script_version, pon_address: script_version, bnfp_address: script_version}

    response = rpclib.sendmany(rpc_connect, this_node_address, json_object)

    print(response)

    return


def sign_message():
    return


print("start improt api")

url = django_base_url + DEV_IMPORT_API_JCF_BATCH_REQUIRE_INTEGRITY_PATH

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

url = django_base_url + DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH

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

exit()
