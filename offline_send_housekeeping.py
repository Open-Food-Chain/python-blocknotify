import json
from lib import openfood
from lib.openfood_env import KOMODO_NODE
from lib.openfood_env import RPC_USER
from lib.openfood_env import RPC_PASSWORD
from lib.openfood_env import RPC_PORT
from lib.openfood_env import EXPLORER_URL
from lib.openfood_env import THIS_NODE_ADDRESS
from lib.openfood_env import HOUSEKEEPING_ADDRESS
from lib.openfood_env import openfood_API_BASE_URL
from lib.openfood_env import openfood_API_ORGANIZATION_CERTIFICATE

# from dotenv import load_dotenv
# load_dotenv(verbose=True)
SCRIPT_VERSION = 0.00011111

openfood.connect_node(RPC_USER, RPC_PASSWORD, KOMODO_NODE, RPC_PORT)


def getCertificateForTest(url):
    return openfood.getWrapper(url)


def offline_wallet_send_housekeeping():
    test_url = openfood_API_BASE_URL + openfood_API_ORGANIZATION_CERTIFICATE + "18/"
    certificate = json.loads(getCertificateForTest(test_url))
    offline_wallet = openfood.offlineWalletGenerator_fromObjectData_certificate(THIS_NODE_ADDRESS, certificate)
    print(offline_wallet)
    # 1. get utxos for address
    print("\n#2# Get UTXOs\n")
    utxos_json = openfood.explorer_get_utxos(EXPLORER_URL, offline_wallet['address'])
    to_python = json.loads(utxos_json)
    print(to_python)

    count = 0
    list_of_ids = []
    list_of_vouts = []
    amount = 0

    for objects in to_python:
        if (objects['amount']):
            count = count + 1
            easy_typeing2 = [objects['vout']]
            easy_typeing = [objects['txid']]
            list_of_ids.extend(easy_typeing)
            list_of_vouts.extend(easy_typeing2)
            amount = amount + objects['amount']

    amount = round(amount, 10)

    print("\n#3# Create raw tx\n")
    to_address = HOUSEKEEPING_ADDRESS
    num_utxo = 1
    fee = 0.00001
    rawtx_info = openfood.createrawtx4(utxos_json, num_utxo, to_address, fee)
    print(rawtx_info[0]['rawtx'])
# this is an array: rawtx_info['rawtx', [array utxo amounts req for sig]]
    print("\n#4# Decode unsigned raw tx\n")
    decoded = openfood.decoderawtx(rawtx_info[0]['rawtx'])
    print()
    print("#######")
    print(json.dumps(decoded, indent=2))
    print("#######")
    print()

    print("\n#5# Sign tx\n")
    signedtx = openfood.signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], offline_wallet['wif'])
    print(signedtx)
    decoded = openfood.decoderawtx(signedtx)
    print("#######")
    print("signed")
    print(decoded)
    print()

    txid = openfood.broadcast_via_explorer(EXPLORER_URL, signedtx)
    print(txid)


offline_wallet_send_housekeeping()
