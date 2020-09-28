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

address = "RS7y4zjQtcNv7inZowb8M6bH3ytS1moj9A"
privkey = "Uv2jzAFb6UttFYmCWGRyuMxafDHNie15eFe7KYXuvgDzfgWancks"

#this_node_pubkey = os.getenv("THIS_NODE_PUBKEY")
#this_node_wif = os.getenv("THIS_NODE_WIF")

minimum_utxo_size = 3.5 #sys.argv[1]
amount = 50


komodo_node_ip = os.getenv("IJUICE_KOMODO_NODE_IPV4_ADDR")

rpc_connect = rpc_connection = Proxy("http://" + rpc_user + ":" + rpc_password + "@" + komodo_node_ip + ":" + port)

url = "http://seed.juicydev.coingateways.com:24711/insight-api-komodo/addrs/"+ address +"/utxo"


def sign_raw_tx(wif, kmd_unsigned_tx_serialized):
    txin_type, privkey, compressed = bitcoin.deserialize_privkey(wif)
    pubkey = bitcoin.public_key_from_private_key(privkey, compressed)

    jsontx = transaction.deserialize(kmd_unsigned_tx_serialized)
    inputs = jsontx.get('inputs')
    outputs = jsontx.get('outputs')
    locktime = jsontx.get('lockTime', 0)
    outputs_formatted = []

    for txout in outputs:
      outputs_formatted.append([txout['type'], txout['address'], txout['value']])

    for txin in inputs:
      txin['type'] = txin_type
      txin['x_pubkeys'] = [pubkey]
      txin['pubkeys'] = [pubkey]
      txin['signatures'] = [None]
      txin['num_sig'] = 1
      txin['address'] = bitcoin.address_from_private_key(wif)
      txin['value'] = 2500000000 # required for preimage calc

    tx = Transaction.from_io(inputs, outputs_formatted, locktime=locktime)
    tx.sign({pubkey:(privkey, compressed)})

    return tx.serialize()

try:
    res = requests.get(url)
except Exception as e:
    print(e)

to_python = json.loads(res.text)

count = 0

list_of_ids = []
list_of_vouts = []
amount = 0.1
tx = ""

for objects in to_python:
    if (objects['amount'] > minimum_utxo_size ) and count < 1:
        count = count + 1
        print(objects)
        tx = objects

amount = round(amount, 10)

count = 0
max = int(minimum_utxo_size*10)
print(tx)

addies = []

for count in range(max):
    addies = addies + [address]

res = rpclib.createrawtransaction(rpc_connect, list_of_ids, list_of_vouts, addies, amount)

final_res = sign_raw_tx(privkey,res)

decoded = rpclib.decoderawtransaction(rpc_connect, final_res)

print(decoded)

params = { 'rawtx':final_res }

url = "http://seed.juicydev.coingateways.com:24711/insight-api-komodo/tx/send"

try:
    res = requests.post(url, data=params)
except Exception as e:
    print(e)

print(res.text)
