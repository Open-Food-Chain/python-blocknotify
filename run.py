import json
# import pytest
# import os
from lib import juicychain
from lib.juicychain_env import EXPLORER_URL
from lib.juicychain_env import IMPORT_API_BASE_URL
from lib.juicychain_env import THIS_NODE_ADDRESS
from lib.juicychain_env import DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH
from lib.juicychain_env import DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
from lib.juicychain_env import JUICYCHAIN_API_BASE_URL
from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION_CERTIFICATE
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
def import_raw_refresco_batch_integrity_pre_process(wallet, batch, import_id):

    batch_wallets_integrity = juicychain.batch_wallets_generate_timestamping(batch, import_id)
    # integrity_address, batch_lot_raddress
    id = batch_wallets_integrity['id']
    integrity_start_txid = juicychain.batch_wallets_fund_integrity_start(batch_wallets_integrity['integrity_address'])
    print("** txid ** (Timestamp integrity start): " + integrity_start_txid)
    juicychain.batch_wallets_timestamping_start(batch_wallets_integrity, integrity_start_txid)
    sendmany_txid = juicychain.organization_send_batch_links(batch_wallets_integrity)
    # TODO MYLO UP TO HERE ^^^ TO SENDMANY, THEN UPDATE TSTX TABLE.  THEN OFFLINE WALLETS
    # THEN REMOVE THIS FUNCTION AND MOVE LOGIC DOWN INTO batch LOOP.
    juicychain.timestamping_save_batch_links(id, sendmany_txid)

    try:
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
        to_address = batch_wallets_integrity['batch_lot_raddress']
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

        data = {'identifier': batch['bnfp'],
                'jds': batch['jds'],
                'jde': batch['jde'],
                'date_production_start': batch['pds'],
                'date_best_before': batch['bbd'],
                'origin_country': batch['pc'],
                'raddress': batch['address'],
                'pubkey': batch['pubkey'],
                'organization': JC_ORG_ID}
        print(data)

        jcapi_response = juicychain.postWrapper(URL_JUICYCHAIN_API_ORGANIZATION_BATCH, data=data)

        print("POST jcapi_response: " + jcapi_response)
        jcapi_batch_id = json.loads(jcapi_response.text)['id']
        print("BATCH ID @ JUICYCHAIN-API: " + str(jcapi_batch_id))

        # TODO update import api with batch id in jcapi

        # send post integrity tx
        # integrity_end_txid = juicychain.sendtoaddressWrapper(batch_wallets_integrity['integrity_address'], SCRIPT_VERSION, MULTI_3X)
        # print("** txid ** (Timestamp integrity end): " + integrity_end_txid)
        # data = {'name': 'chris', 'integrity_address': batch_wallets_integrity['integrity_address'],
        #        'integrity_post_tx': integrity_end_txid, 'batch_lot_raddress': batch_wallets_integrity['batch_lot_raddress']}

        # integrity_end_response = juicychain.putWrapper(batch_integrity_url, data=data)
        # print(integrity_end_response)

        integrity_end_txid = juicychain.batch_wallets_fund_integrity_end(batch_wallets_integrity['integrity_address'])
        print("** txid ** (Timestamp integrity end): " + integrity_end_txid)
        juicychain.batch_wallets_timestamping_end(batch_wallets_integrity, integrity_end_txid)

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


batches_no_timestamp = juicychain.get_batches_no_timestamp()
for batch in batches_no_timestamp:
    import_raw_refresco_batch_integrity_pre_process(THIS_NODE_ADDRESS, batch, batch['id'])

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
