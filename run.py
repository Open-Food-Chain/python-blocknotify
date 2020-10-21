from lib import rpclib
from slickrpc import Proxy
import requests
import subprocess
import json
# import pytest
# import os
from lib import juicychain
# from lib.juicychain_env import MULTI_1X
from lib.juicychain_env import MULTI_2X
from lib.juicychain_env import MULTI_3X
# from lib.juicychain_env import MULTI_4X
from lib.juicychain_env import MULTI_5X
from lib.juicychain_env import KOMODO_NODE
from lib.juicychain_env import RPC_USER
from lib.juicychain_env import RPC_PASSWORD
from lib.juicychain_env import RPC_PORT
from lib.juicychain_env import EXPLORER_URL
from lib.juicychain_env import IMPORT_API_BASE_URL
from lib.juicychain_env import THIS_NODE_ADDRESS
from lib.juicychain_env import THIS_NODE_WIF
from lib.juicychain_env import BLOCKNOTIFY_CHAINSYNC_LIMIT
from lib.juicychain_env import HOUSEKEEPING_ADDRESS
from lib.juicychain_env import DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH
from lib.juicychain_env import DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH
from lib.juicychain_env import DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
from lib.juicychain_env import JUICYCHAIN_API_BASE_URL
from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION_CERTIFICATE_NORADDRESS
from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION_CERTIFICATE
# from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION_CERTIFICATE_RULE
from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION_BATCH

from dotenv import load_dotenv
load_dotenv(verbose=True)
SCRIPT_VERSION = 0.00010021
URL_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH
URL_IMPORT_API_RAW_REFRESCO_TSTX_PATH = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
URL_JUICYCHAIN_API_ORGANIZATION_BATCH = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_BATCH

# TODO f-string https://realpython.com/python-f-strings/
rpc_connect = rpc_connection = Proxy(
    "http://" + RPC_USER + ":" + RPC_PASSWORD + "@" + KOMODO_NODE + ":" + RPC_PORT)

juicychain.connect_node(RPC_USER, RPC_PASSWORD, KOMODO_NODE, RPC_PORT)
juicychain.ismywallet(THIS_NODE_ADDRESS, THIS_NODE_WIF)
juicychain.checksync(BLOCKNOTIFY_CHAINSYNC_LIMIT)
hk_txid = juicychain.sendtoaddressWrapper(HOUSEKEEPING_ADDRESS, SCRIPT_VERSION, MULTI_2X)
print(hk_txid)


def getCertificateForTest(url):
    return juicychain.getWrapper(url)


# TODO what does this do?
def import_raw_refresco_batch_integrity_pre_process(wallet, data, import_id):

    data = json.dumps(data)
    PDS = data['pds']
    JDS = data['jds']
    JDE = data['jde']
    BBD = data['bbd']
    PC = data['pc']
    ANFP = data['anfp']
    PON = data['pon']
    BNFP = data['bnfp']
    anfp_wallet = juicychain.gen_wallet(wallet, ANFP, "anfp")
    pon_wallet = juicychain.gen_wallet(wallet, PON, "pon")
    bnfp_wallet = juicychain.gen_wallet(wallet, BNFP, "bnfp")
    integrity_address = juicychain.gen_wallet(wallet, data)

    print("Timestamp-integrity raddress: " + integrity_address['address'])

    data = {'name': 'chris', 'integrity_address': integrity_address[
        'address'], 'batch': import_id, 'batch_lot_raddress': bnfp_wallet['address']}

    batch_wallets_update_response = juicychain.postWrapper(URL_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH, data)

    print("POST response: " + batch_wallets_update_response)

    id = json.loads(batch_wallets_update_response)['id']

    integrity_start_txid = juicychain.sendtoaddressWrapper(integrity_address['address'], SCRIPT_VERSION, MULTI_2X)

    print("** txid ** (Timestamp integrity start): " + integrity_start_txid)

    batch_integrity_url = URL_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH + id + "/"
    data = {'name': 'chris', 'integrity_address': integrity_address[
        'address'], 'integrity_pre_tx': integrity_start_txid, 'batch_lot_raddress': bnfp_wallet['address']}

    batch_integrity_start_response = juicychain.putWrapper(batch_integrity_url, data)
    print(batch_integrity_start_response)

    try:
        print("MAIN WALLET " + THIS_NODE_ADDRESS +
              " SENDMANY TO BATCH_LOT (bnfp), POOL_PO (pon), GTIN (anfp)")
        json_object = {anfp_wallet['address']: SCRIPT_VERSION, pon_wallet[
            'address']: SCRIPT_VERSION, bnfp_wallet['address']: SCRIPT_VERSION}

        sendmany_txid = juicychain.sendmanyWrapper(THIS_NODE_ADDRESS, json_object)

        print("** txid ** (Main org wallet sendmany BATCH_LOT/POOL_PO/GTIN): " + sendmany_txid)
        tstx_data = {'sender_raddress': THIS_NODE_ADDRESS,
                     'tsintegrity': id, 'sender_name': 'ORG WALLET', 'txid': sendmany_txid}

        ts_response = juicychain.postWrapper(URL_IMPORT_API_RAW_REFRESCO_TSTX_PATH, tstx_data)
        print("POST ts_response: " + ts_response)

        # offline wallets
        test_url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + "8/"
        certificate = json.loads(getCertificateForTest(test_url))
        offline_wallet = juicychain.offlineWalletGenerator_fromObjectData_certificate(THIS_NODE_ADDRESS, certificate)
        # get_utxos
        utxos_json = juicychain.explorer_get_utxos(EXPLORER_URL, offline_wallet['address'])
        utxos_obj = json.loads(utxos_json)
        amount = juicychain.utxo_bundle_amount(utxos_obj)
        print("(Not sending this amount atm) Amount of utxo bundle: " + str(amount))
        # create tx
        to_address = bnfp_wallet['address']
        num_utxo = 1
        # fee = 0.00005
        fee = 0
        # rawtx_info = juicychain.createrawtx4(utxos_json, num_utxo, to_address, fee)
        rawtx_info = juicychain.createrawtx5(utxos_json, num_utxo, to_address, fee, offline_wallet['address'])
        # sign tx
        signedtx = juicychain.signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], offline_wallet['wif'])
        # broadcast
        certificates_txid = juicychain.broadcast_via_explorer(EXPLORER_URL, signedtx)

        print("** txid ** (Certificate to batch_lot): " + certificates_txid)
        tstx_data = {'sender_raddress': offline_wallet['address'],
                     'tsintegrity': id, 'sender_name': 'CERTIFICATE WALLET', 'txid': certificates_txid}

        ts_response = juicychain.postWrapper(URL_IMPORT_API_RAW_REFRESCO_TSTX_PATH, tstx_data)
        print("POST ts_response: " + ts_response)

        print("Push data from import-api to juicychain-api for batch_lot")

    except Exception as e:
        print(e)
        print("## ERROR IMPORT API")
        print("#")
        print("# bailing out of tx sending to BATCH_LOT")
        print("# integrity timestamp started, but not finished sending tx")
        print("# Check balances of Organization wallets including certificate, location, etc")
        print("# Warning: Not implemented yet - resume operation")
        print("# Exiting")
        print("#")
        print("##")
        exit()

    try:
        if THIS_NODE_ADDRESS == 'RV5GwBpJjTpXJYB5YGxJuZapECQF8Pn6Wy':
            JC_ORG_ID = 1
        if THIS_NODE_ADDRESS == 'RTWAtzNhLRxLot3QB2fv5oXCr5JfZhp5Fy':
            JC_ORG_ID = 2
        print("Push data from import-api to juicychain-api for batch_lot")

        # print(PDS + JDS + JDE + BBD + PC)
        data = {'identifier': BNFP, 'jds': JDS, 'jde': JDE, 'date_production_start': PDS,
                'date_best_before': BBD, 'origin_country': PC, 'raddress': bnfp_wallet['address'],
                'pubkey': bnfp_wallet['pubkey'], 'organization': JC_ORG_ID}
        print(data)

        jcapi_response = juicychain.postWrapper(URL_JUICYCHAIN_API_ORGANIZATION_BATCH, data=data)

        print("POST jcapi_response: " + jcapi_response)
        jcapi_batch_id = json.loads(jcapi_response.text)['id']
        print("BATCH ID @ JUICYCHAIN-API: " + str(jcapi_batch_id))

        # TODO update import api with batch id in jcapi

        # send post integrity tx
        integrity_end_txid = juicychain.sendtoaddressWrapper(integrity_address['address'], SCRIPT_VERSION, MULTI_3X)
        print("** txid ** (Timestamp integrity end): " + integrity_end_txid)
        data = {'name': 'chris', 'integrity_address': integrity_address['address'],
                'integrity_post_tx': integrity_end_txid, 'batch_lot_raddress': bnfp_wallet['address']}

        integrity_end_response = juicychain.putWrapper(batch_integrity_url, data=data)

        print(integrity_end_response)
        print("** complete **")

    except Exception as e:
        print(e)
        print("### ERROR IMPORT-API PUSH TO JUICYCHAIN-API")
        print("#")
        print("# CHECK JUICYCHAIN-API")
        print("# Exiting")
        print("#")
        print("##")

    return


def juicychain_certificate_address_creation(wallet, data, db_id):

    print("## JUICYCHAIN API ##")

    data = json.dumps(data)

    signed_data = rpclib.signmessage(rpc_connect, wallet, data)
    item_address = subprocess.getoutput("php genaddressonly.php " + signed_data)

    item_address = json.loads(item_address)

    print(item_address['address'])

    url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + id + '/'
    data = {'raddress': item_address['address']}

    res = requests.patch(url, data=data)  # , headers={"Content-Type": "application/json"})

    print(res.text)

    # id = json.loads(res.text)['id']

    # print(id)

    response = rpclib.sendtoaddress(rpc_connect, item_address['address'], SCRIPT_VERSION)

    print(response)

    return item_address['address']


def getBatchesNullIntegrity():
    print("10009 start import api - raw/refresco")
    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH
    print("Trying: " + url)

    try:
        res = requests.get(url)
    except Exception as e:
        print("###### REQUIRE INTEGRITY URL ERROR: ", e)
        print("20201020 - url not sending nice response " + url)

    print(res.text)

    raw_json = res.text

    batches_null_integrity = ""

    try:
        batches_null_integrity = json.loads(raw_json)
    except Exception as e:
        print("10009 failed to parse to json because of", e)

    print("New batch requires timestamping: " + str(len(batches_null_integrity)))
    return batches_null_integrity


def modifyBatchesNullIntegrity(batches_null_integrity):
    for batch in batches_null_integrity:
        raw_json = batch
        id = batch['id']
        print("starting process for id:", id)
        import_raw_refresco_batch_integrity_pre_process(THIS_NODE_ADDRESS, raw_json, id)
        juicychain_certificate_address_creation(THIS_NODE_ADDRESS, raw_json, id)


def getCertsNoAddy():
    print("10008 start getting the address less certificates")

    url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE_NORADDRESS
    print("10008 trying " + url)

    try:
        res = requests.get(url)
    except Exception as e:
        raise Exception(e)

    certs_no_addy = res.text

    certs_no_addy = json.loads(certs_no_addy)

    return certs_no_addy


batches_null_integrity = getBatchesNullIntegrity()
modifyBatchesNullIntegrity(batches_null_integrity)
certs_no_addy = getCertsNoAddy()

for cert in certs_no_addy:
    offline_wallet = juicychain.offlineWalletGenerator_fromObjectData_certificate(THIS_NODE_ADDRESS, cert)
    url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + str(cert['id']) + "/"
    data = {"raddress": offline_wallet['address'], "pubkey": offline_wallet['pubkey']}
    juicychain.patchWrapper(url, data=data)
    # TODO try/block
    txid = juicychain.sendtoaddressWrapper(offline_wallet['address'], SCRIPT_VERSION, MULTI_5X)
    print("Funding tx " + txid)
    # TODO add fundingtx, check for unfunded offline wallets
