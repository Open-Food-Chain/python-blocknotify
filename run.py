from lib import rpclib
from slickrpc import Proxy
import requests
import subprocess
import json
# import pytest
# import os
from lib import juicychain
from lib.juicychain_env import MULTI_1X
from lib.juicychain_env import MULTI_2X
from lib.juicychain_env import MULTI_3X
from lib.juicychain_env import MULTI_4X
from lib.juicychain_env import MULTI_5X
from lib.juicychain_env import KOMODO_NODE
from lib.juicychain_env import RPC_USER
from lib.juicychain_env import RPC_PASSWORD
from lib.juicychain_env import RPC_PORT
from lib.juicychain_env import EXPLORER_URL
from lib.juicychain_env import IMPORT_API_BASE_URL
from lib.juicychain_env import THIS_NODE_ADDRESS
from lib.juicychain_env import THIS_NODE_WALLET
from lib.juicychain_env import THIS_NODE_PUBKEY
from lib.juicychain_env import THIS_NODE_WIF
from lib.juicychain_env import BLOCKNOTIFY_CHAINSYNC_LIMIT
from lib.juicychain_env import HOUSEKEEPING_ADDRESS
from lib.juicychain_env import DEV_IMPORT_API_JCF_BATCH_INTEGRITY_PATH
# from lib.juicychain_env import DEV_IMPORT_API_JCF_BATCH_REQUIRE_INTEGRITY_PATH
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

juicychain.connect_node(RPC_USER, RPC_PASSWORD, KOMODO_NODE, RPC_PORT)

# TODO f-string https://realpython.com/python-f-strings/
rpc_connect = rpc_connection = Proxy(
    "http://" + RPC_USER + ":" + RPC_PASSWORD + "@" + KOMODO_NODE + ":" + RPC_PORT)


juicychain.ismywallet(THIS_NODE_ADDRESS, THIS_NODE_WIF)
juicychain.checksync(BLOCKNOTIFY_CHAINSYNC_LIMIT)
hk_txid = juicychain.sendtoaddressWrapper(HOUSEKEEPING_ADDRESS, SCRIPT_VERSION, MULTI_2X)
print(hk_txid)


# TODO what does this do?
def import_raw_refresco_batch_integrity_pre_process(wallet, data, import_id):

    print("10009 Import API - Raw Refresco Pre Process")

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

    data = json.dumps(data)

    item_address = juicychain.gen_wallet(wallet, data)

    print("Timestamp-integrity raddress: " + item_address['address'])

    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH

    print(url)

    data = {'name': 'chris', 'integrity_address': item_address[
        'address'], 'batch': import_id, 'batch_lot_raddress': bnfp_wallet['address']}

    print(data)

    res = juicychain.postWrapper(url, data)

    print("POST response: " + res)

    id = json.loads(res)['id']

    response = juicychain.sendtoaddressWrapper(item_address['address'], SCRIPT_VERSION, MULTI_2X)

    print("** txid ** (Timestamp integrity start): " + response)

    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH + id + "/"
    data = {'name': 'chris', 'integrity_address': item_address[
        'address'], 'integrity_pre_tx': response, 'batch_lot_raddress': bnfp_wallet['address']}

    res = juicychain.putWrapper(url, data)

    try:
        print("MAIN WALLET " + THIS_NODE_ADDRESS +
              " SENDMANY TO BATCH_LOT (bnfp), POOL_PO (pon), GTIN (anfp)")
        json_object = {anfp_wallet['address']: SCRIPT_VERSION, pon_wallet[
            'address']: SCRIPT_VERSION, bnfp_wallet['address']: SCRIPT_VERSION}

        # TODO rename to sendmany_txid
        response = juicychain.sendmanyWrapper(THIS_NODE_ADDRESS, json_object)

        print("** txid ** (Main org wallet sendmany BATCH_LOT/POOL_PO/GTIN): " + response)
        tstx_url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
        tstx_data = {'sender_raddress': THIS_NODE_ADDRESS,
                     'tsintegrity': id, 'sender_name': 'ORG WALLET', 'txid': response}
        print(tstx_url)
        print(tstx_data)

        res = juicychain.postWrapper(tstx_url, tstx_data)

        print("POST response: " + res)

        # TODO offline wallets
        test_url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + "8/"
        certificate = json.loads(getCertificateForTest(test_url))
        offline_wallet = juicychain.offlineWalletGenerator_fromObjectData_certificate(THIS_NODE_ADDRESS, certificate)
        # TODO get_utxos
        utxos_json = juicychain.explorer_get_utxos(EXPLORER_URL, offline_wallet['address'])
        utxos_obj = json.loads(utxos_json)
        amount = juicychain.utxo_bundle_amount(utxos_obj)
        print("(Not sending this amount atm) Amount of utxo bundle: " + str(amount))
        # TODO create tx
        to_address = bnfp_wallet['address']
        num_utxo = 1
        # fee = 0.00005
        fee = 0
        # rawtx_info = juicychain.createrawtx4(utxos_json, num_utxo, to_address, fee)
        rawtx_info = juicychain.createrawtx5(utxos_json, num_utxo, to_address, fee, offline_wallet['address'])
        # TODO sign tx
        signedtx = juicychain.signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], offline_wallet['wif'])
        # TODO broadcast
        certificates_txid = juicychain.broadcast_via_explorer(EXPLORER_URL, signedtx)
        # certificates_txid = workaroundsendWrapper(certificates_rpc_connect, bnfp_wallet['address'], 0.02)

        print("** txid ** (Certificate to batch_lot): " + certificates_txid)
        tstx_data = {'sender_raddress': offline_wallet['address'],
                     'tsintegrity': id, 'sender_name': 'CERTIFICATE WALLET', 'txid': certificates_txid}
        print(tstx_url)
        print(tstx_data)

        res = juicychain.postWrapper(tstx_url, tstx_data)

        print("POST response: " + res)

        print("Push data from import-api to juicychain-api for batch_lot")
        # print(PDS + JDS + JDE + BBD + PC)

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
        jcapi_url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_BATCH
        print(jcapi_url)
        data = {'identifier': BNFP, 'jds': JDS, 'jde': JDE, 'date_production_start': PDS,
                'date_best_before': BBD, 'origin_country': PC, 'raddress': bnfp_wallet['address'],
                'pubkey': bnfp_wallet['pubkey'], 'organization': JC_ORG_ID}
        print(data)

        res = juicychain.postWrapper(jcapi_url, data=data)  # , headers={"Content-Type": "application/json"})

        print("POST response: " + res)
        jcapi_batch_id = json.loads(res.text)['id']
        print("BATCH ID @ JUICYCHAIN-API: " + str(jcapi_batch_id))

        # TODO update import api with batch id in jcapi

        # send post integrity tx
        response = rpclib.sendtoaddress(rpc_connect, item_address['address'], SCRIPT_VERSION * 3)
        print("** txid ** (Timestamp integrity end): " + response)
        url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH + id + "/"
        data = {'name': 'chris', 'integrity_address': item_address['address'],
                'integrity_post_tx': response, 'batch_lot_raddress': bnfp_wallet['address']}

        res = juicychain.putWrapper(url, data=data)

        print(res)
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


def getCertificateForTest(url):
    return juicychain.getWrapper(url)


def offline_wallet_send_housekeeping():
    test_url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + "7/"
    certificate = json.loads(getCertificateForTest(test_url))
    offline_wallet = juicychain.offlineWalletGenerator_fromObjectData_certificate(THIS_NODE_ADDRESS, certificate)
    print(offline_wallet)
    # sign a tx to housekeeping address
    # 1. get utxos for address
    print("\n#2# Get UTXOs\n")
    utxos_json = juicychain.explorer_get_utxos(EXPLORER_URL, offline_wallet['address'])
    to_python = json.loads(utxos_json)
    print(to_python)

    count = 0
    list_of_ids = []
    list_of_vouts = []
    amount = 0

    for objects in to_python:
        if (objects['amount']):
            count = count + 1
            easy_typeing2 = [objects['vout']]
            easy_typeing = [objects['txid']]
            list_of_ids.extend(easy_typeing)
            list_of_vouts.extend(easy_typeing2)
            amount = amount + objects['amount']

    amount = round(amount, 10)

    print("\n#3# Create raw tx\n")
    to_address = HOUSEKEEPING_ADDRESS
    num_utxo = 1
    fee = 0.00005
    # rawtx_info = juicychain.createrawtx3(utxos_json, num_utxo, to_address)
    rawtx_info = juicychain.createrawtx4(utxos_json, num_utxo, to_address, fee)
    print(rawtx_info[0]['rawtx'])
# this is an array: rawtx_info['rawtx', [array utxo amounts req for sig]]
    print("\n#4# Decode unsigned raw tx\n")
    decoded = juicychain.decoderawtx(rawtx_info[0]['rawtx'])
    print()
    print("#######")
    print(json.dumps(decoded, indent=2))
    print("#######")
    print()

    print("\n#5# Sign tx\n")
    signedtx = juicychain.signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], offline_wallet['wif'])
    print(signedtx)
    decoded = juicychain.decoderawtx(signedtx)
    print("#######")
    print("signed")
    print(decoded)
    print()

    txid = juicychain.broadcast_via_explorer(EXPLORER_URL, signedtx)
    print(txid)


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


offline_wallet_send_housekeeping()


# the issuer, issue date, expiry date, identifier (not the db id, the
# certificate serial number / identfier)


# integrity/

def is_json(myjson):
    try:
        # json_object = json.loads(myjson)
        json.loads(myjson)
    except ValueError as e:
        print(e)
        return False
    return True


# TEST FUNCTIONS

# @pytest.mark.skip

def test_isMy():
    test = ismywallet()
    assert test == True


def test_checksync():
    test = checksync()
    assert type(10) == type(test)


# @pytest.mark.skip
def test_explorer_get_utxos():
    try:
        test = explorer_get_utxos(EXPLORER_URL, "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW")
        assert is_json(test) == True
    except Exception as e:
        assert e == True


def test_gen_Wallet():
    test = gen_wallet(THIS_NODE_ADDRESS, "testtest")
    assert type("test") == type(test['address'])
    assert test['address'][0] == 'R'


def test_getCertsNoAddy():
    test = getCertsNoAddy()
    assert type(test) == type(['this', 'is', 'an', 'test', 'array'])


def test_getBatchesNullIntegrity():
    test = getBatchesNullIntegrity()
    assert type(test) == type(['this', 'is', 'an', 'test', 'array'])


def test_import_jcf_batch_integrity_pre_process():
    data = {'this': 'is', 'test': 'data'}
    test = import_jcf_batch_integrity_pre_process(THIS_NODE_ADDRESS, data, "001")
    assert is_json(test) == True


def test_sendtoaddressWrapper():
    test = sendtoaddressWrapper(THIS_NODE_ADDRESS, 1)
    assert not (" " in test)


def test_sendtomanyWrapper():
    json_object = {THIS_NODE_ADDRESS: SCRIPT_VERSION}
    test = sendtomanyWrapper(THIS_NODE_ADDRESS, json_object)
    print(test)
    assert not (" " in test)
