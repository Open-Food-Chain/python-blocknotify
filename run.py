from lib import rpclib
from slickrpc import Proxy
import requests
import subprocess
import json
import pytest
import os
from lib import juicychain
from lib.juicychain_env import KOMODO_NODE
from lib.juicychain_env import RPC_USER
from lib.juicychain_env import RPC_PASSWORD
from lib.juicychain_env import RPC_PORT
from lib.juicychain_env import EXPLORER_URL
from dotenv import load_dotenv
load_dotenv(verbose=True)
print("\n#after_demo_1# Connect Node\n")
juicychain.connect_node(RPC_USER, RPC_PASSWORD, KOMODO_NODE, RPC_PORT)

# global vars
# TODO move some env vars from deployment env vars to .env
explorer_host = os.getenv("JUICYCHAIN_EXPLORER_MAINNET_UNCHAIN")
explorer_port = os.getenv("JUICYCHAIN_EXPLORER_MAINNET_UNCHAIN_PORT")
explorer_url = "http://" + explorer_host + ":" + explorer_port + "/"
print(explorer_url)

rpc_user = RPC_USER
rpc_password = RPC_PASSWORD
port = RPC_PORT

komodo_node_ip = KOMODO_NODE

this_node_address = os.getenv("THIS_NODE_WALLET")
this_node_pubkey = os.getenv("THIS_NODE_PUBKEY")
this_node_wif = os.getenv("THIS_NODE_WIF")


# TODO
# import funcs
# move this to housekeeping
# explorer_get_utxos(explorer_url, this_node_address)


# rpc_connect = rpc_connection = Proxy("http://%s:%s@127.0.0.1:%d" % (rpc_user, rpc_password, port))
# TODO f-string https://realpython.com/python-f-strings/
rpc_connect = rpc_connection = Proxy(
    "http://" + rpc_user + ":" + rpc_password + "@" + komodo_node_ip + ":" + port)

blocknotify_chainsync_limit = int(os.getenv("BLOCKNOTIFY_CHAINSYNC_LIMIT"))
housekeeping_address = os.getenv("HOUSEKEEPING_ADDRESS")


IMPORT_API_HOST = str(os.getenv("IMPORT_API_HOST"))
IMPORT_API_PORT = str(os.getenv("IMPORT_API_PORT"))
IMPORT_API_BASE_URL = "http://" + IMPORT_API_HOST + ":" + IMPORT_API_PORT + "/"
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
JUICYCHAIN_API_ORGANIZATION_CERTIFICATE = os.getenv("JUICYCHAIN_API_ORGANIZATION_CERTIFICATE")
JUICYCHAIN_API_ORGANIZATION_CERTIFICATE_RULE = os.getenv("JUICYCHAIN_API_ORGANIZATION_CERTIFICATE")
JUICYCHAIN_API_ORGANIZATION_BATCH = str(os.getenv("JUICYCHAIN_API_ORGANIZATION_BATCH"))


def ismywallet():
    # check wallet management
    try:
        is_mine = rpclib.validateaddress(rpc_connect, this_node_address)['ismine']
        if is_mine is False:
            rpclib.importprivkey(rpc_connect, this_node_wif)
        is_mine = rpclib.validateaddress(rpc_connect, this_node_address)['ismine']
        return is_mine
    except Exception as e:
        print(e)
        print("## JUICYCHAIN_ERROR ##")
        print("# Node is not available. Check debug.log for details")
        print("# If node is rescanning, will take a short while")
        print("# If changing wallet & env, rescan will occur")
        print("# Exiting.")
        print("##")
        exit()


def checksync():
    general_info = rpclib.getinfo(rpc_connect)
    sync = general_info['longestchain'] - general_info['blocks']

    print("Chain info.  Longest chain, blocks, sync diff")
    print(general_info['longestchain'])

    print(general_info['blocks'])

    print(sync)
    return sync

    if sync >= blocknotify_chainsync_limit:
        print('the chain is not synced, try again later')
        exit()

    print("Chain is synced")


ismywallet()

checksync()


# start housekeeping

# we send this amount to an address for housekeeping
# update by 0.0001 (manually, if can be done in CI/CD, nice-to-have not need-to-have) (MYLO)
# house keeping address is list.json last entry during dev
script_version = 0.00010010


# send a small amount (SCRIPT_VERSION) for HOUSEKEEPING_ADDRESS from each organization
# ############################
# info: for external documentation then remove from here
# one explorer url to check is
# IJUICE  http://seed.juicydev.coingateways.com:24711/address/RS7y4zjQtcNv7inZowb8M6bH3ytS1moj9A
# JAMJUICE  http://seed.juicydev.coingateways.com:64422/address/RS7y4zjQtcNv7inZowb8M6bH3ytS1moj9A
# POS95   http://seed.juicydev.coingateways.com:54343/address/RS7y4zjQtcNv7inZowb8M6bH3ytS1moj9A
# ############################
# send SCRIPT_VERSION, increment by 0.00000001 for each update

res = rpclib.sendtoaddress(rpc_connect, housekeeping_address, script_version)
# res = rpclib.sendtoaddress(certificates_rpc_connect, housekeeping_address, 0.01)
# res = rpclib.sendtoaddress(location_rpc_connect, housekeeping_address, 0.02)

print(res)

# ############################

# END OF HOUSEKEEPING

# ##############################################################################


#
#
# EXPLORER GET UTXO FOR WALLET


# TODO f-string
def explorer_get_utxos(explorer_url, querywallet):
    print("10007 Get UTXO for wallet " + querywallet)
    # INSIGHT_API_KOMODO_ADDRESS_UTXO = "insight-api-komodo/addrs/{querywallet}/utxo"
    INSIGHT_API_KOMODO_ADDRESS_UTXO = "insight-api-komodo/addrs/" + querywallet + "/utxo"
    # INSIGHT_API_BROADCAST_TX="insight-api-komodo/tx/send"
    res = requests.get(explorer_url + INSIGHT_API_KOMODO_ADDRESS_UTXO)
    print(res.text)
    print("10007 end utxos")
    return res.text


# TODO
# move this to housekeeping
# explorer_get_utxos(explorer_url, this_node_address)

# ##############################################################################

# START JCF IMPORT API INTEGRITY CHECKS

# JCF is the only part of script that refers to BATCH.
# development of new partners can use RAW_REFRESCO-like variables

###########################
# organization R-address = $1
# raw_json import data in base64 = $2
# batch record import database id(uuid) = $3
###########################


def import_jcf_batch_integrity_pre_process(wallet, data, import_id):

    data = json.dumps(data)

    signed_data = rpclib.signmessage(rpc_connect, wallet, data)
    item_address = subprocess.getoutput("php genaddressonly.php " + signed_data)

    item_address = json.loads(item_address)

    print(item_address['address'])

    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_JCF_BATCH_INTEGRITY_PATH
    data = {'name': 'chris', 'integrity_address': item_address['address'], 'batch': import_id}

    res = requests.post(url, data=data)

    print(res.text)

    id = json.loads(res.text)['id']

    print(id)

    response = rpclib.sendtoaddress(rpc_connect, item_address['address'], script_version)

    print(response)

    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_JCF_BATCH_INTEGRITY_PATH + id + "/"
    data = {'name': 'chris', 'integrity_address': item_address[
        'address'], 'integrity_pre_tx': response}

    res = requests.put(url, data=data)

    print(res.text)

    return res.text


def gen_wallet(wallet, data, label='NoLabelOK'):
    print("Creating a %s address signing with %s and data %s" % (label, wallet, data))
    signed_data = rpclib.signmessage(rpc_connect, wallet, data)
    print("Signed data is %s" % (signed_data))
    new_wallet_json = subprocess.getoutput("php genwallet.php " + signed_data)
    print("Created wallet %s" % (new_wallet_json))

    new_wallet = json.loads(new_wallet_json)

    return new_wallet


def sendtoaddressWrapper(address, multiplyer):
    response = rpclib.sendtoaddress(rpc_connect, address, script_version * multiplyer)
    return response


def sendtomanyWrapper(addy, json_object):
    response = rpclib.sendmany(rpc_connect, addy, json_object)
    return response


def workaroundsendWrapper(connectione, wallet, amount):
    certificates_txid = rpclib.sendtoaddress(connectione, wallet, amount)
    return certificates_txid


def postWrapper(url, data):
    res = requests.post(url, data=data)
    if(res.status_code == 200):
        return res.text
    else:
        obj = json.dumps({"error": res.reason})
        return obj


def putWrapper(url, data):
    res = requests.put(url, data=data)

    if(res.status_code == 200):
        return res.text
    else:
        obj = json.dumps({"error": res.reason})
        return obj


def getWrapper(url):
    res = requests.get(url)

    if(res.status_code == 200):
        return res.text
    else:
        obj = json.dumps({"error": res.reason})
        return obj


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

    anfp_wallet = gen_wallet(wallet, ANFP, "anfp")
    pon_wallet = gen_wallet(wallet, PON, "pon")
    bnfp_wallet = gen_wallet(wallet, BNFP, "bnfp")

    data = json.dumps(data)

    item_address = gen_wallet(wallet, data)

    print("Timestamp-integrity raddress: " + item_address['address'])

    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH

    print(url)

    data = {'name': 'chris', 'integrity_address': item_address[
        'address'], 'batch': import_id, 'batch_lot_raddress': bnfp_wallet['address']}

    print(data)

    res = putWrapper(url, data)

    print("PUT response: " + res)

    id = json.loads(res.text)['id']

    response = sendtoaddressWrapper(item_address['address'], 2)

    print("** txid ** (Timestamp integrity start): " + response)

    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH + id + "/"
    data = {'name': 'chris', 'integrity_address': item_address[
        'address'], 'integrity_pre_tx': response, 'batch_lot_raddress': bnfp_wallet['address']}

    res = postWrapper(url, data)

    try:
        print("MAIN WALLET " + this_node_address +
              " SENDMANY TO BATCH_LOT (bnfp), POOL_PO (pon), GTIN (anfp)")
        json_object = {anfp_wallet['address']: script_version, pon_wallet[
            'address']: script_version, bnfp_wallet['address']: script_version}

        # TODO rename to sendmany_txid
        response = sendtomanyWrapper(this_node_address, json_object)

        print("** txid ** (Main org wallet sendmany BATCH_LOT/POOL_PO/GTIN): " + response)
        tstx_url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
        tstx_data = {'sender_raddress': this_node_address,
                     'tsintegrity': id, 'sender_name': 'ORG WALLET', 'txid': response}
        print(tstx_url)
        print(tstx_data)

        res = postWrapper(tstx_url, tstx_data)

        print("POST response: " + res)

        # TODO offline wallets
        # TODO get_utxos
        # TODO create tx
        # TODO sign tx
        # TODO broadcast
        # certificates_txid = workaroundsendWrapper(certificates_rpc_connect, bnfp_wallet['address'], 0.02)
        certificates_txid = "WIP"

        print("** txid ** (Certificate to batch_lot): " + certificates_txid)
        tstx_data = {'sender_raddress': "**WIP**",
                     'tsintegrity': id, 'sender_name': 'CERTIFICATE WALLET', 'txid': certificates_txid}
        print(tstx_url)
        print(tstx_data)

        res = postWrapper(tstx_url, tstx_data)

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
        if this_node_address == 'RV5GwBpJjTpXJYB5YGxJuZapECQF8Pn6Wy':
            JC_ORG_ID = 1
        if this_node_address == 'RTWAtzNhLRxLot3QB2fv5oXCr5JfZhp5Fy':
            JC_ORG_ID = 2
        print("Push data from import-api to juicychain-api for batch_lot")

        # print(PDS + JDS + JDE + BBD + PC)
        jcapi_url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_BATCH
        print(jcapi_url)
        data = {'identifier': BNFP, 'jds': JDS, 'jde': JDE, 'date_production_start': PDS,
                'date_best_before': BBD, 'origin_country': PC, 'raddress': bnfp_wallet['address'],
                'pubkey': bnfp_wallet['pubkey'], 'organization': JC_ORG_ID}
        print(data)

        res = postWrapper(jcapi_url, data=data)  # , headers={"Content-Type": "application/json"})

        print("POST response: " + res)
        jcapi_batch_id = json.loads(res.text)['id']
        print("BATCH ID @ JUICYCHAIN-API: " + str(jcapi_batch_id))

        # TODO update import api with batch id in jcapi

        # send post integrity tx
        response = rpclib.sendtoaddress(rpc_connect, item_address['address'], script_version * 3)
        print("** txid ** (Timestamp integrity end): " + response)
        url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH + id + "/"
        data = {'name': 'chris', 'integrity_address': item_address['address'],
                'integrity_post_tx': response, 'batch_lot_raddress': bnfp_wallet['address']}

        res = putWrapper(url, data=data)

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

    response = rpclib.sendtoaddress(rpc_connect, item_address['address'], script_version)

    print(response)

    return item_address['address']


def getBatchesNullIntegrity():
    print("10009 skip batch import api")
    #
    # url = IMPORT_API_BASE_URL + DEV_IMPORT_API_JCF_BATCH_REQUIRE_INTEGRITY_PATH
    # print ("10009 - " + url)
    #
    # TODO skipped, come back
    # res = requests.get(url)
    #
    # raw_json = res.text
    #
    # batches_null_integrity = ""
    #
    # try:
    #     batches_null_integrity = json.loads(raw_json)
    # except Exception as e:
    #     print("failed to parse to json because of", e)
    #     print("10007 - probably nothing returned from " + url)
    #
    #
    # TODO when data model being queried
    # for batch in batches_null_integrity:
    #    raw_json = batch
    #    id = batch['id']
    #    print("starting process for id:", id)
    #    import_jcf_batch_integrity_pre_process(this_node_address, raw_json, id)
    #
    #
    print("10009 start import api - raw/refresco")
    print(IMPORT_API_BASE_URL)
    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH
    print("Trying: " + url)

    try:
        res = requests.get(url)
    except Exception as e:
        print("something wrong", e)
        print("10009 - url not sending nice response " + url)

    print(res.text)

    raw_json = res.text

    batches_null_integrity = ""

    try:
        batches_null_integrity = json.loads(raw_json)
    except Exception as e:
        print("10009 failed to parse to json because of", e)

    return batches_null_integrity


def modifyBatchesNullIntegrity(batches_null_integrity):
    for batch in batches_null_integrity:
        raw_json = batch
        id = batch['id']
        print("starting process for id:", id)
        import_raw_refresco_batch_integrity_pre_process(this_node_address, raw_json, id)
        juicychain_certificate_address_creation(this_node_address, raw_json, id)


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


def giveCertsAddy(certs_no_addy):
    for cert in certs_no_addy:
        raw_json = {
            "issuer": cert['issuer'],
            "issue_date": cert['date_issue'],
            "expiry_date": cert['date_expiry'],
            "identfier": cert['identifier']
        }

        raw_json = json.dumps(raw_json)
        # addy = get_address(this_node_address, raw_json)
        cert_wallet = gen_wallet(this_node_address, raw_json, cert['identifier'])
        id = str(cert['id'])
        url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + id + "/"

        try:
            data = {"raddress": cert_wallet['address'], "pubkey": cert_wallet['pubkey']}
            res = requests.patch(url, data=data)
            print(res)
            txid = rpclib.sendtoaddress(rpc_connect, cert_wallet['address'], script_version * 2)
            print("Funding tx " + txid)

        except Exception as e:
            raise Exception(e)


def getCertificateForTest():
    pass


def getWalletFromCertificateData(certificate_data):
    pass


def offline_wallet_send_housekeeping():
    certificate = getCertificateForTest()
    print(certificate)
    offline_wallet = getWalletFromCertificateData(certificate)
    # sign a tx to housekeeping address
    # 1. get utxos for address
    print("\n#2# Get UTXOs\n")
    utxos_json = juicychain.explorer_get_utxos(EXPLORER_URL, offline_wallet['address'])
    to_python = json.loads(utxos_json)

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


batches_null_integrity = getBatchesNullIntegrity()
modifyBatchesNullIntegrity(batches_null_integrity)
certs_no_addy = getCertsNoAddy()
giveCertsAddy(certs_no_addy)


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
        test = explorer_get_utxos(explorer_url, "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW")
        assert is_json(test) == True
    except Exception as e:
        assert e == True


def test_gen_Wallet():
    test = gen_wallet(this_node_address, "testtest")
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
    test = import_jcf_batch_integrity_pre_process(this_node_address, data, "001")
    assert is_json(test) == True


def test_sendtoaddressWrapper():
    test = sendtoaddressWrapper(this_node_address, 1)
    assert not (" " in test)


def test_sendtomanyWrapper():
    json_object = {this_node_address: script_version}
    test = sendtomanyWrapper(this_node_address, json_object)
    print(test)
    assert not (" " in test)


def test_postWrapperr():
    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
    data = {'sender_raddress': this_node_address,
            'tsintegrity': "1", 'sender_name': 'ORG WALLET', 'txid': "testtest"}

    test = postWrapper(url, data)
    assert is_json(test) == True


def test_putWrapperr():
    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
    data = {'sender_raddress': this_node_address,
            'tsintegrity': "1", 'sender_name': 'ORG WALLET', 'txid': "testtest"}

    test = putWrapper(url, data)
    assert is_json(test) == True
