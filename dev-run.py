# from lib import rpclib
from lib import juicychain
from slickrpc import Proxy
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)
rpc_user = os.getenv("IJUICE_KOMODO_NODE_USERNAME")
rpc_password = os.getenv("IJUICE_KOMODO_NODE_PASSWORD")
port = os.getenv("IJUICE_KOMODO_NODE_RPC_PORT")
komodo_node_ip = os.getenv("IJUICE_KOMODO_NODE_IPV4_ADDR")
rpc_connect = rpc_connection = Proxy("http://" + rpc_user + ":" + rpc_password + "@" + komodo_node_ip + ":" + port)
this_node_address = os.getenv("THIS_NODE_WALLET")
IMPORT_API_HOST = str(os.getenv("IMPORT_API_HOST"))
IMPORT_API_PORT = str(os.getenv("IMPORT_API_PORT"))
IMPORT_API_BASE_URL = IMPORT_API_HOST

wallet_info = juicychain.gen_wallet(rpc_connect, this_node_address, "test")
print(wallet_info)
