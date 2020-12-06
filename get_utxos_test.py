from lib.openfood_env import KOMODO_NODE
from lib.openfood_env import RPC_USER
from lib.openfood_env import RPC_PASSWORD
from lib.openfood_env import RPC_PORT
# from lib.openfood_env import THIS_NODE_WALLET
# from lib.openfood_env import EXPLORER_URL
# load all needed vars at top of file only

from lib import openfood
from dotenv import load_dotenv
import json
import time
import sys

load_dotenv(verbose=True)
# now ready to hack at code

# THIS_NODE_WALLET = "RS7y4zjQtcNv7inZowb8M6bH3ytS1moj9A"
# THIS_NODE_WIF =  "Uv2jzAFb6UttFYmCWGRyuMxafDHNie15eFe7KYXuvgDzfgWancks"
# num_utxo = 50
# time_in_sec =  1800

THIS_NODE_WALLET = sys.argv[1]
THIS_NODE_WIF = sys.argv[2]
num_utxo = int(sys.argv[3])
time_in_sec = int(sys.argv[4])

while True:
    stop = False
    for EXPLORER_URL in ["https://blockchain-explorer.thenewfork.staging.do.unchain.io/"]:

        print("\n#1# Connect Node\n")
        openfood.connect_node(RPC_USER, RPC_PASSWORD, KOMODO_NODE, RPC_PORT)

        print("\n#2# Get UTXOs\n")
        utxos_json = openfood.explorer_get_utxos(EXPLORER_URL, THIS_NODE_WALLET)
        final = []
        try:
            utxos_json = json.loads(utxos_json)
            for utxo in utxos_json:
                if utxo['confirmations'] > 10:
                    final = final + [utxo]

            utxos_json = final
            utxos_json = json.dumps(utxos_json)
        except Exception as e:
            stop = True
            print(e)

        if stop == False:
            print("\n#3# Create raw tx\n")
            to_address = "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW"
            num_utxo = 50
            rawtx_info = openfood.createrawtx3(utxos_json, num_utxo, to_address)
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
            signedtx = openfood.signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], THIS_NODE_WIF)
            print(signedtx)
            decoded = openfood.decoderawtx(signedtx)
            print("#######")
            print("signed")
            print(decoded)

            txid = openfood.broadcast_via_explorer(EXPLORER_URL, signedtx)
            print(txid)
    time.sleep(time_in_sec)
