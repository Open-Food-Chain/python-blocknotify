import requests
import subprocess
import json
# import pytest
# import os
from lib import juicychain
from lib.juicychain_env import MULTI_1X
from lib.juicychain_env import MULTI_2X
from lib.juicychain_env import MULTI_3X
# from lib.juicychain_env import MULTI_4X
from lib.juicychain_env import EXPLORER_URL
from lib.juicychain_env import IMPORT_API_BASE_URL
from lib.juicychain_env import THIS_NODE_ADDRESS
# from lib.juicychain_env import DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH
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

juicychain.connect_node()
juicychain.check_node_wallet()
juicychain.check_sync()
hk_txid = juicychain.housekeeping_tx()
print(hk_txid)


def getCertificateForTest(url):
    return juicychain.getWrapper(url)


# TODO what does this do?
def import_raw_refresco_batch_integrity_pre_process(wallet, new_import_record, import_id):

    data = json.dumps(new_import_record)
    anfp_wallet = juicychain.gen_wallet(wallet, data['anfp'], "anfp")
    pon_wallet = juicychain.gen_wallet(wallet, data['pon'], "pon")
    bnfp_wallet = juicychain.gen_wallet(wallet, data['bnfp'], "bnfp")
    # pds_wallet = juicychain.gen_wallet(wallet, data['pds'], "pds")
    # jds_wallet = juicychain.gen_wallet(wallet, data['jds'], "jds")
    # jde_wallet = juicychain.gen_wallet(wallet, data['jde'], "jde")
    # bbd_wallet = juicychain.gen_wallet(wallet, data['bbd'], "bbd")
    # pc_wallet = juicychain.gen_wallet(wallet, data['pc'], "pc")
    integrity_address = juicychain.gen_wallet(wallet, data, "integrity address")

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

        data = {'identifier': new_import_record['bnfp'],
                'jds': new_import_record['jds'],
                'jde': new_import_record['jde'],
                'date_production_start': new_import_record['pds'],
                'date_best_before': new_import_record['bbd'],
                'origin_country': new_import_record['pc'],
                'raddress': bnfp_wallet['address'],
                'pubkey': bnfp_wallet['pubkey'],
                'organization': JC_ORG_ID}
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

    signed_data = juicychain.signmessage_wrapper(data)
    item_address = subprocess.getoutput("php genaddressonly.php " + signed_data)

    item_address = json.loads(item_address)

    print(item_address['address'])

    url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + id + '/'
    data = {'raddress': item_address['address']}

    res = requests.patch(url, data=data)  # , headers={"Content-Type": "application/json"})

    print(res.text)

    # id = json.loads(res.text)['id']

    # print(id)

    txid = juicychain.sendtoaddressWrapper(item_address['address'], SCRIPT_VERSION, MULTI_1X)
    print(txid)

    return item_address['address']


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


batches_no_timestamp = juicychain.get_batches_no_timestamp()
for json_batch in batches_no_timestamp:
    import_raw_refresco_batch_integrity_pre_process(THIS_NODE_ADDRESS, json_batch, json_batch['id'])
    juicychain_certificate_address_creation(THIS_NODE_ADDRESS, json_batch, json_batch['id'])

certificates_no_timestamp = juicychain.get_certificates_no_timestamp()

for certificate in certificates_no_timestamp:
    offline_wallet = juicychain.offlineWalletGenerator_fromObjectData_certificate(THIS_NODE_ADDRESS, certificate)
    url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + str(certificate['id']) + "/"
    data = {"raddress": offline_wallet['address'], "pubkey": offline_wallet['pubkey']}
    juicychain.patchWrapper(url, data=data)
    # TODO try/block
    funding_txid = juicychain.fund_certificate(offline_wallet['address'])
    print("Funding tx " + funding_txid)
    # TODO add fundingtx, check for unfunded offline wallets
