import json
from lib import openfood


from dotenv import load_dotenv
load_dotenv(verbose=True)

openfood.connect_node()
# openfood.check_node_wallet()

openfood.check_sync()

#hk_txid = openfood.housekeeping_tx()

#print(hk_txid)

