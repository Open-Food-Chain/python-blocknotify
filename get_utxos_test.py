from lib.juicychain_env import KOMODO_NODE
from lib.juicychain_env import RPC_USER
from lib.juicychain_env import RPC_PASSWORD
from lib.juicychain_env import RPC_PORT
# from lib.juicychain_env import THIS_NODE_WALLET
# from lib.juicychain_env import EXPLORER_URL
# load all needed vars at top of file only

from lib import juicychain
from dotenv import load_dotenv
import json
load_dotenv(verbose=True)
# now ready to hack at code

for EXPLORER_URL in ["https://rick.explorer.dexstats.info/", "https://morty.explorer.dexstats.info/"]:
    THIS_NODE_WALLET = "RRT896bgjzjFqxH1i3bUKyXwr22mjdvzhh"
    THIS_NODE_WIF = "Uqd27fBgxWbZwwdJVqiSz8eXVBxikfPQsEb7QriC2Trzy5Lkx48y"

    print("\n#1# Connect Node\n")
    juicychain.connect_node(RPC_USER, RPC_PASSWORD, KOMODO_NODE, RPC_PORT)

    print("\n#2# Get UTXOs\n")
    utxos_json = juicychain.explorer_get_utxos(EXPLORER_URL, THIS_NODE_WALLET)

    print("\n#3# Create raw tx\n")
    to_address = "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW"
    num_utxo = 1
    rawtx_info = juicychain.createrawtx3(utxos_json, num_utxo, to_address)
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
    signedtx = juicychain.signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], THIS_NODE_WIF)
    print(signedtx)
    decoded = juicychain.decoderawtx(signedtx)
    print("#######")
    print("signed")
    print(decoded)
    print()

    txid = juicychain.broadcast_via_explorer(EXPLORER_URL, signedtx)
    print(txid)
