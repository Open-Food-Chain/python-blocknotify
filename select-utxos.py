from lib import rpclib
from slickrpc import Proxy
from lib import transaction, bitcoin, util
from lib.util import bfh, bh2u
from lib.transaction import Transaction

import requests
import subprocess
import json
import sys
import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

IMPORT_API_HOST = str(os.getenv("IMPORT_API_HOST"))
IMPORT_API_PORT = str(os.getenv("IMPORT_API_PORT"))
IMPORT_API_BASE_URL =  IMPORT_API_HOST

rpc_user = os.getenv("IJUICE_KOMODO_NODE_USERNAME")
rpc_password = os.getenv("IJUICE_KOMODO_NODE_PASSWORD")
port = os.getenv("IJUICE_KOMODO_NODE_RPC_PORT")

address = sys.argv[1]
amount = float(sys.argv[2])
greedy = bool(sys.argv[3])

#this_node_pubkey = os.getenv("THIS_NODE_PUBKEY")
#this_node_wif = os.getenv("THIS_NODE_WIF")

def get_utxos_api(address):
    komodo_node_ip = os.getenv("IJUICE_KOMODO_NODE_IPV4_ADDR")

    rpc_connect = rpc_connection = Proxy("http://" + rpc_user + ":" + rpc_password + "@" + komodo_node_ip + ":" + port)

    url = "https://blockchain-explorer.thenewfork.staging.do.unchain.io/insight-api-komodo/addrs/"+ address +"/utxo"

    try:
        res = requests.get(url)
    except Exception as e:
        print(e)

    try:
        to_python = json.loads(res.text)
    except Exception as e:
        print(e)
        exit()

    return to_python

array_of_utxos = []
array_of_utxos_final = []
amount_final = -10000000000


def get_utxos(utxos, amount, greedy):
    global array_of_utxos
    global array_of_utxos_final
    global amount_final

    print(amount)


    if len(array_of_utxos) >= len(array_of_utxos_final) and len(array_of_utxos_final) > 0:
        return False

    if amount <= 0 and amount > amount_final:
        return True

    flag = False
    cheap_copy = array_of_utxos
    for utxo in utxos:
        for uxto_in_array in array_of_utxos:
            if uxto_in_array['txid'] == utxo['txid']:
                flag = True

        if flag == False:
            array_of_utxos = array_of_utxos + [utxo]
            if get_utxos(utxos, amount-utxo['amount'], greedy) == True:
                array_of_utxos_final = array_of_utxos
                amount_final = amount
                if greedy == True:
                    return True
        flag = False
    array_of_utxos = cheap_copy
    return False



get_utxos(get_utxos_api(address), amount, greedy)

print(array_of_utxos_final)
