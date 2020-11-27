import json
from lib import juicychain


from dotenv import load_dotenv
load_dotenv(verbose=True)

juicychain.connect_node()
# juicychain.check_node_wallet()

juicychain.check_sync()

#hk_txid = juicychain.housekeeping_tx()

#print(hk_txid)

