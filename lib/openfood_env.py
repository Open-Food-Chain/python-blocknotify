from dotenv import load_dotenv
import os
load_dotenv(verbose=True)

MULTI_1X = 1
MULTI_2X = 2
MULTI_3X = 3
MULTI_4X = 4
MULTI_5X = 5

# explorer
openfood_EXPLORER_MAINNET_UNCHAIN = os.environ['JUICYCHAIN_EXPLORER_MAINNET_UNCHAIN']
openfood_EXPLORER_MAINNET_UNCHAIN_PORT = str(os.environ['JUICYCHAIN_EXPLORER_MAINNET_UNCHAIN_PORT'])
EXPLORER_URL = "http://" + openfood_EXPLORER_MAINNET_UNCHAIN + ":" + openfood_EXPLORER_MAINNET_UNCHAIN_PORT + "/"

# this node wallet
THIS_NODE_WALLET = str(os.environ['THIS_NODE_WALLET'])
THIS_NODE_RADDRESS = str(os.environ['THIS_NODE_WALLET'])
THIS_NODE_WIF = str(os.environ['THIS_NODE_WIF'])
THIS_NODE_PUBKEY = str(os.environ['THIS_NODE_PUBKEY'])

# rpc
# RPC_USER = str(os.environ['KOMODO_SMARTCHAIN_NODE_USERNAME'])
# RPC_PASSWORD = str(os.environ['KOMODO_SMARTCHAIN_NODE_PASSWORD'])
# RPC_PORT = str(os.environ['KOMODO_SMARTCHAIN_NODE_RPC_PORT'])
# KOMODO_NODE = str(os.environ['KOMODO_SMARTCHAIN_NODE_IPV4_ADDR'])
RPC_USER = str(os.environ['KOMODO_SMARTCHAIN_NODE_USERNAME'])
RPC_PASSWORD = str(os.environ['KOMODO_SMARTCHAIN_NODE_PASSWORD'])
RPC_PORT = str(os.environ['KOMODO_SMARTCHAIN_NODE_RPC_PORT'])
KOMODO_NODE = str(os.environ['KOMODO_SMARTCHAIN_NODE_IPV4_ADDR'])

# test wallet
TEST_GEN_WALLET_PASSPHRASE = "testing123"
TEST_GEN_WALLET_PUBKEY = "035b955ecee91343cae751b6b5c5c1b0efbd3a24ff0a622d8782e11b43eb8ec5af"
TEST_GEN_WALLET_WIF = "UriaaZ1hEftNZFM8pw9TXLF3iMqn2usCJDqeSnfAVkaPEwZXstLK"
TEST_GEN_WALLET_RADDRESS = "RDLtn5usEfoukyL2XqbcuoAg1sohU3m1F1"

# import api
IMPORT_API_HOST = str(os.environ['IMPORT_API_HOST'])
IMPORT_API_PORT = str(os.environ['IMPORT_API_PORT'])
IMPORT_API_BASE_URL = "http://" + IMPORT_API_HOST + ":" + IMPORT_API_PORT + "/"

# tweakable changes
BLOCKNOTIFY_CHAINSYNC_LIMIT = 5
HOUSEKEEPING_RADDRESS = "RS7y4zjQtcNv7inZowb8M6bH3ytS1moj9A"

# integrity/
DEV_IMPORT_API_JCF_BATCH_INTEGRITY_PATH = "integrity/"
# batch/require_integrity/
DEV_IMPORT_API_JCF_BATCH_REQUIRE_INTEGRITY_PATH = "batch/require_integrity/"
# raw/refresco/require_integrity/
DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH = "raw/refresco/require_integrity/"
# raw/refresco-integrity/
DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH = "raw/refresco-integrity/"
# raw/refresco-tstx/
DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH = "raw/refresco-tstx/"
# raw/refresco/
DEV_IMPORT_API_RAW_REFRESCO_PATH = "raw/refresco/"

# LOAD openfood ENV
openfood_API_HOST = str(os.environ['JUICYCHAIN_API_HOST'])
openfood_API_PORT = str(os.environ['openfood_API_PORT'])
openfood_API_VERSION_PATH = str(os.environ['openfood_API_VERSION_PATH'])
openfood_API_BASE_URL = "http://" + openfood_API_HOST + \
    ":" + openfood_API_PORT + "/" + openfood_API_VERSION_PATH

openfood_API_ORGANIZATION_CERTIFICATE_NORADDRESS = "certificate/noraddress/"
openfood_API_ORGANIZATION_CERTIFICATE = "certificate/"
# TODO unused
openfood_API_ORGANIZATION_CERTIFICATE_RULE = "certificate-rule/noraddress/"
openfood_API_ORGANIZATION_BATCH = "batch/"
openfood_API_ORGANIZATION = "organization/"

# FUNDING
FUNDING_AMOUNT_CERTIFICATE = 5
FUNDING_UTXO_COUNT_CERTIFICATE = 10
FUNDING_AMOUNT_LOCATION = 5
FUNDING_UTXO_COUNT_LOCATION = 10
FUNDING_AMOUNT_TIMESTAMPING_START = 0.091
FUNDING_AMOUNT_TIMESTAMPING_END = 0.092
