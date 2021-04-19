from lib import openfood_env
from lib import openfood
from slickrpc import Proxy
from dotenv import load_dotenv

RPC = ""
KV1RPC = ""

# test done
def connect_node():
    global RPC
    print("Connecting to: " + openfood_env.KOMODO_NODE + ":" + openfood_env.RPC_PORT)
    RPC = Proxy("http://" + openfood_env.RPC_USER + ":" + openfood_env.RPC_PASSWORD + "@" + openfood_env.KOMODO_NODE + ":" + openfood_env.RPC_PORT)
    return True


# test done
def connect_kv1_node():
    global KV1RPC
    print("Connecting KV to: " + openfood_env.KV1_NODE + ":" + openfood_env.KV1_RPC_PORT)
    KV1RPC = Proxy("http://" + openfood_env.KV1_RPC_USER + ":" + openfood_env.KV1_RPC_PASSWORD + "@" + openfood_env.KV1_NODE + ":" + openfood_env.KV1_RPC_PORT)
    return True


def getinfo():
    print(openfood.rpclib.getinfo(RPC))


def getinfo_kv():
        print(openfood.rpclib.getinfo(KV1RPC))


connect_node()
connect_kv1_node()
getinfo()
getinfo_kv()