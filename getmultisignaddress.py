from lib import rpclib
from slickrpc import Proxy
import requests
import subprocess
import json
import os
import sys
from dotenv import load_dotenv
load_dotenv(verbose=True)

rpc_user = os.getenv("IJUICE_KOMODO_NODE_USERNAME")
rpc_password = os.getenv("IJUICE_KOMODO_NODE_PASSWORD")
port = os.getenv("IJUICE_KOMODO_NODE_RPC_PORT")

this_node_address = os.getenv("THIS_NODE_WALLET")
this_node_pubkey = os.getenv("THIS_NODE_PUBKEY")
this_node_wif = os.getenv("THIS_NODE_WIF")

komodo_node_ip = os.getenv("IJUICE_KOMODO_NODE_IPV4_ADDR")

rpc_connect = rpc_connection = Proxy("http://" + rpc_user + ":" + rpc_password + "@" + komodo_node_ip + ":" + port)






signed_data = sys.argv[1]
item_address = subprocess.getoutput("php genaddressonly.php " + signed_data)

item_address = json.loads(item_address)



addresses = [ this_node_pubkey, item_address['pubkey']]

res = rpclib.createmultisig(rpc_connect, 2, addresses)

print(res)
