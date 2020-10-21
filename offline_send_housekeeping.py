import json
from lib import juicychain
from lib.juicychain_env import KOMODO_NODE
from lib.juicychain_env import RPC_USER
from lib.juicychain_env import RPC_PASSWORD
from lib.juicychain_env import RPC_PORT
from lib.juicychain_env import EXPLORER_URL
from lib.juicychain_env import THIS_NODE_ADDRESS
from lib.juicychain_env import HOUSEKEEPING_ADDRESS
from lib.juicychain_env import JUICYCHAIN_API_BASE_URL
from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION_CERTIFICATE

# from dotenv import load_dotenv
# load_dotenv(verbose=True)
SCRIPT_VERSION = 0.00011111

juicychain.connect_node(RPC_USER, RPC_PASSWORD, KOMODO_NODE, RPC_PORT)


def getCertificateForTest(url):
    return juicychain.getWrapper(url)


def offline_wallet_send_housekeeping():
    test_url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + "18/"
    certificate = json.loads(getCertificateForTest(test_url))
    offline_wallet = juicychain.offlineWalletGenerator_fromObjectData_certificate(THIS_NODE_ADDRESS, certificate)
    print(offline_wallet)
    # 1. get utxos for address
    print("\n#2# Get UTXOs\n")
    utxos_json = juicychain.explorer_get_utxos(EXPLORER_URL, offline_wallet['address'])
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
    rawtx_info = juicychain.createrawtx4(utxos_json, num_utxo, to_address, fee)
    print(rawtx_info[0]['rawtx'])
# this is an array: rawtx_info['rawtx', [array utxo amounts req for sig]]
    print("\n#4# Decode unsigned raw tx\n")
    decoded = juicychain.decoderawtx(rawtx_info[0]['rawtx'])
    print()
    print("#######")
    print(json.dumps(decoded, indent=2))
    print("#######")
    print()

    print("\n#5# Sign tx\n")
    signedtx = juicychain.signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], offline_wallet['wif'])
    print(signedtx)
    decoded = juicychain.decoderawtx(signedtx)
    print("#######")
    print("signed")
    print(decoded)
    print()

    txid = juicychain.broadcast_via_explorer(EXPLORER_URL, signedtx)
    print(txid)


offline_wallet_send_housekeeping()
