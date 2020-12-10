import json
from lib import openfood


from dotenv import load_dotenv
load_dotenv(verbose=True)

openfood.connect_node()
# openfood.check_node_wallet()

openfood.check_sync()

test = {"this":"is", "a":"json"}

#if(type(test) == type({"this":"is", "a":"json"})):
#	test = json.dumps(test)

res = openfood.kvupdate_wrapper("chirs", test, "10", "if mylo agrees")
print(res)

res = openfood.kvsearch_wrapper("chirs")
#res = json.loads(res)
print(res['key'])

#hk_txid = openfood.housekeeping_tx()

#print(hk_txid)
