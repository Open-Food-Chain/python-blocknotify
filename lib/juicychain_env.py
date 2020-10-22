from dotenv import load_dotenv
import os
load_dotenv(verbose=True)

MULTI_1X = 1
MULTI_2X = 2
MULTI_3X = 3
MULTI_4X = 4
MULTI_5X = 5

# explorer
JUICYCHAIN_EXPLORER_MAINNET_UNCHAIN = str(os.getenv("JUICYCHAIN_EXPLORER_MAINNET_UNCHAIN"))
JUICYCHAIN_EXPLORER_MAINNET_UNCHAIN_PORT = str(os.getenv("JUICYCHAIN_EXPLORER_MAINNET_UNCHAIN_PORT"))
EXPLORER_URL = "http://" + JUICYCHAIN_EXPLORER_MAINNET_UNCHAIN + ":" + JUICYCHAIN_EXPLORER_MAINNET_UNCHAIN_PORT + "/"

# this node wallet
THIS_NODE_WALLET = str(os.getenv("THIS_NODE_WALLET"))
THIS_NODE_ADDRESS = str(os.getenv("THIS_NODE_WALLET"))
THIS_NODE_WIF = str(os.getenv("THIS_NODE_WIF"))
THIS_NODE_PUBKEY = str(os.getenv("THIS_NODE_PUBKEY"))

# rpc
RPC_USER = str(os.getenv("KOMODO_SMARTCHAIN_NODE_USERNAME"))
RPC_PASSWORD = str(os.getenv("KOMODO_SMARTCHAIN_NODE_PASSWORD"))
RPC_PORT = str(os.getenv("KOMODO_SMARTCHAIN_NODE_RPC_PORT"))
KOMODO_NODE = str(os.getenv("KOMODO_SMARTCHAIN_NODE_IPV4_ADDR"))

# test wallets
TEST_THIS_NODE_WALLET = str(os.getenv("TEST_THIS_NODE_WALLET"))
TEST_THIS_NODE_WIF = str(os.getenv("TEST_THIS_NODE_WIF"))
TEST_GEN_WALLET_PASSPHRASE = str(os.getenv("TEST_GEN_WALLET_PASSPHRASE"))
TEST_GEN_WALLET_PUBKEY = str(os.getenv("TEST_GEN_WALLET_PUBKEY"))
TEST_GEN_WALLET_WIF = str(os.getenv("TEST_GEN_WALLET_WIF"))
TEST_GEN_WALLET_ADDRESS = str(os.getenv("TEST_GEN_WALLET_ADDRESS"))

# import api
IMPORT_API_HOST = str(os.getenv("IMPORT_API_HOST"))
IMPORT_API_PORT = str(os.getenv("IMPORT_API_PORT"))
IMPORT_API_BASE_URL = "http://" + IMPORT_API_HOST + ":" + IMPORT_API_PORT + "/"

# tweakable changes
BLOCKNOTIFY_CHAINSYNC_LIMIT = int(os.getenv("BLOCKNOTIFY_CHAINSYNC_LIMIT"))
HOUSEKEEPING_ADDRESS = os.getenv("HOUSEKEEPING_ADDRESS")

# integrity/
DEV_IMPORT_API_JCF_BATCH_INTEGRITY_PATH = os.getenv("DEV_IMPORT_API_JCF_BATCH_INTEGRITY_PATH")
# batch/require_integrity/
DEV_IMPORT_API_JCF_BATCH_REQUIRE_INTEGRITY_PATH = os.getenv(
    "DEV_IMPORT_API_JCF_BATCH_REQUIRE_INTEGRITY_PATH")
# raw/refresco/require_integrity/
DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH = str(
    os.getenv("DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH"))
# raw/refresco-integrity/
DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH = str(
    os.getenv("DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH"))
# raw/refresco-tstx/
DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH = str(os.getenv("DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH"))

# LOAD JUICYCHAIN ENV
JUICYCHAIN_API_HOST = str(os.getenv("JUICYCHAIN_API_HOST"))
JUICYCHAIN_API_PORT = str(os.getenv("JUICYCHAIN_API_PORT"))
JUICYCHAIN_API_VERSION_PATH = str(os.getenv("JUICYCHAIN_API_VERSION_PATH"))
JUICYCHAIN_API_BASE_URL = "http://" + JUICYCHAIN_API_HOST + \
    ":" + JUICYCHAIN_API_PORT + "/" + JUICYCHAIN_API_VERSION_PATH

JUICYCHAIN_API_ORGANIZATION_CERTIFICATE_NORADDRESS = str(
    os.getenv("JUICYCHAIN_API_ORGANIZATION_CERTIFICATE_NORADDRESS"))
JUICYCHAIN_API_ORGANIZATION_CERTIFICATE = str(os.getenv("JUICYCHAIN_API_ORGANIZATION_CERTIFICATE"))
JUICYCHAIN_API_ORGANIZATION_CERTIFICATE_RULE = str(os.getenv("JUICYCHAIN_API_ORGANIZATION_CERTIFICATE_RULE"))
JUICYCHAIN_API_ORGANIZATION_BATCH = str(os.getenv("JUICYCHAIN_API_ORGANIZATION_BATCH"))
JUICYCHAIN_API_ORGANIZATION = str(os.getenv("JUICYCHAIN_API_ORGANIZATION"))

# FUNDING
FUNDING_AMOUNT_CERTIFICATE = 15
FUNDING_AMOUNT_TIMESTAMPING_START = 0.00111
FUNDING_AMOUNT_TIMESTAMPING_END = 0.00112
