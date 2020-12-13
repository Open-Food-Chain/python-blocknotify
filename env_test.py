from lib.openfood_env import EXPLORER_URL
#from lib.openfood_env import THIS_NODE_WALLET
#from lib.openfood_env import THIS_NODE_WIF
#from lib.openfood_env import TEST_GEN_WALLET_PASSPHRASE
#from lib.openfood_env import TEST_GEN_WALLET_ADDRESS
#from lib.openfood_env import TEST_GEN_WALLET_WIF
#from lib.openfood_env import TEST_GEN_WALLET_PUBKEY
#from lib.openfood_env import openfood_API_BASE_URL
#from lib.openfood_env import openfood_API_ORGANIZATION_CERTIFICATE
#from lib import openfood

from dotenv import load_dotenv
import json
#import pytest
import os
load_dotenv(verbose=True)

chris = os.getenv('CHRIS')
print(chris)

chris = os.environ['CHRIS']
print(chris)
