import json
from lib import juicychain


from dotenv import load_dotenv
load_dotenv(verbose=True)

juicychain.connect_node()
# juicychain.check_node_wallet()

juicychain.check_sync()

test = {"this":"is", "a":"json"}

#if(type(test) == type({"this":"is", "a":"json"})):
#	test = json.dumps(test)

res = juicychain.kvupdate_wrapper("chirs", test, "10", "if mylo agrees")
print(res)

res = juicychain.kvsearch_wrapper("chirs")
#res = json.loads(res)
print(res['key'])

#hk_txid = juicychain.housekeeping_tx()

#print(hk_txid)

