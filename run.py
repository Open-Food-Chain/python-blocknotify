import os
import sentry_sdk
# Setup sentry, normall all this would ago after the imports, but the imports are crashing
sentry_dsn = os.getenv('SENTRY_DSN')
if sentry_dsn:
    sentry_sdk.init(
        sentry_dsn,
        environment=os.environ['ENVIRONMENT']
    )
    sentry_sdk.set_tag('org', os.environ['SENTRY_ORG'])

import json
# import pytest
# import os
from lib import openfood
from lib.openfood_env import EXPLORER_URL
from lib.openfood_env import IMPORT_API_BASE_URL
from lib.openfood_env import DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH
from lib.openfood_env import DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
from lib.openfood_env import openfood_API_BASE_URL
from lib.openfood_env import openfood_API_ORGANIZATION_CERTIFICATE
from lib.openfood_env import openfood_API_ORGANIZATION_BATCH

from dotenv import load_dotenv
load_dotenv(verbose=True)

SCRIPT_VERSION = 0.00010021
URL_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH
URL_IMPORT_API_RAW_REFRESCO_TSTX_PATH = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
URL_openfood_API_ORGANIZATION_BATCH = openfood_API_BASE_URL + openfood_API_ORGANIZATION_BATCH

openfood.connect_node()
openfood.connect_kv1_node()
openfood.check_node_wallet()
openfood.check_kv1_wallet()
openfood.verify_kv_pool_wallets()
openfood.check_offline_wallets()
openfood.check_sync()
hk_txid = openfood.housekeeping_tx()
# this works
# openfood.organization_get_pool_wallets_by_raddress(openfood.get_this_node_raddress())
print("House keeping tx:", hk_txid, sep="\n")

batches_no_timestamp = openfood.get_batches_no_timestamp()
for batch in batches_no_timestamp:
    try:
        print("""
        
        =====>>>>> STAGE: Batch processing start
        
        """)
        print(batch)
        # batch_wallets_integrity holds integrity address, batch by import_id, batch_lot_raddress
        batch_wallets_integrity = openfood.batch_wallets_generate_timestamping(batch, batch['id'])
        # not sure why this tofix is here dec2020
        tofix_bnfp_wallet = openfood.gen_wallet(batch['bnfp'], "bnfp")
        id = batch_wallets_integrity['id']
        integrity_start_txid = openfood.batch_wallets_fund_integrity_start(batch_wallets_integrity['integrity_address'])
        print("** txid ** (Timestamp integrity start): " + integrity_start_txid)
        openfood.batch_wallets_timestamping_start(batch_wallets_integrity, integrity_start_txid)
        # sendmany_txid = openfood.organization_send_batch_links(batch_wallets_integrity)
        # sendmany_txid = openfood.organization_send_batch_links2(batch_wallets_integrity, batch['pon'])
        sendmany_txid = openfood.organization_send_batch_links3(batch_wallets_integrity, batch['pon'], batch['bnfp'])
        openfood.timestamping_save_batch_links(id, sendmany_txid)
        # Offline wallets
        print("""
        
        =====>>>>> STAGE: Send offline wallets into batch
        
        """)
        txid_delivery_date = openfood.sendToBatchDeliveryDate(tofix_bnfp_wallet['address'], batch['bbd'])
        print("** txid ** (DELIVERY_DATE): " + txid_delivery_date)
        txid_pon = openfood.sendToBatchPON(tofix_bnfp_wallet['address'], batch['pon'])
        print("** txid ** (PON): " + txid_pon)
        txid_julian_start = "" # openfood.sendToBatchFromOfflineWallet(tofix_bnfp_wallet['address'], batch['jds'])
        print("** txid ** (JULIAN START): " + txid_julian_start)
        txid_julian_stop = ""
        print("** txid ** (JULIAN STOP): " + txid_julian_stop)
        txid_origin_country = ""
        print("** txid ** (ORIGIN COUNTRY): " + txid_origin_country)
        txid_bb_date = ""
        print("** txid ** (BB DATE): " + txid_bb_date)
        txid_prod_date = ""
        print("** txid ** (PROD DATE): " + txid_prod_date)
        txid_tin = ""
        print("** txid ** (TIN): " + txid_tin)
        txid_pl = openfood.sendToBatchPL(tofix_bnfp_wallet['address'], batch['pl'])
        print("** txid ** (PL): " + txid_pl)
        print("""
        
        =====>>>>> STAGE: Certificates for batch
        
        """)
        # this can all be put into an openfood lib function like sendToBatchDeliveryDate
        certificate = openfood.get_certificate_for_batch()
        offline_wallet = openfood.offlineWalletGenerator_fromObjectData_certificate(certificate)
        utxos_json = openfood.explorer_get_utxos(offline_wallet['address'])
        utxos_obj = json.loads(utxos_json)
        amount = openfood.utxo_bundle_amount(utxos_obj)
        print("(Not sending this amount atm) Amount of utxo bundle: " + str(amount))
        to_address = batch_wallets_integrity['batch_lot_raddress']
        num_utxo = 1
        # fee = 0.00015
        fee = 0
        # rawtx_info = openfood.createrawtx4(utxos_json, num_utxo, to_address, fee)
        rawtx_info = openfood.createrawtx5(utxos_json, num_utxo, to_address, fee, offline_wallet['address'])
        signedtx = openfood.signtx(rawtx_info[0]['rawtx'], rawtx_info[1]['amounts'], offline_wallet['wif'])
        certificate_txid = openfood.broadcast_via_explorer(EXPLORER_URL, signedtx)
        openfood.timestamping_save_certificate(id, "CERTIFICATE WALLET", offline_wallet, certificate_txid)
        print("** txid ** (Certificate to batch_lot): " + certificate_txid)

    except Exception as e:
        print(e)
        print("## ERROR IMPORT API")
        print("# bailing out of tx sending to BATCH_LOT")
        print("# integrity timestamp started, but not finished sending tx")
        print("# Check balances of Organization wallets including certificate, location, etc")
        print("# Warning: Not implemented yet - resume operation")
        print("# Exiting")
        print("##")
        exit()

    try:
        print("Push data from import-api to openfood-api for batch_lot")
        # http://localhost:8999/api/v1/organization/?raddress=RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW
        organization = openfood.get_jcapi_organization()
        JC_ORG_ID = organization['id']
        jcapi_batch = openfood.push_batch_data_consumer(JC_ORG_ID, batch, tofix_bnfp_wallet)
        integrity_end_txid = openfood.batch_wallets_fund_integrity_end(batch_wallets_integrity['integrity_address'])
        print("** txid ** (Timestamp integrity end): " + integrity_end_txid)
        openfood.batch_wallets_timestamping_end(batch_wallets_integrity, integrity_end_txid)

    except Exception as e:
        print(e)
        print("### ERROR IMPORT-API PUSH TO openfood-API")
        print("# CHECK openfood-API")
        print("# Exiting")
        print("##")

#print("Getting certificates requiring timestamping")
#certificates_no_timestamp = openfood.get_certificates_no_timestamp()
#
#for certificate in certificates_no_timestamp:
#    offline_wallet = openfood.offlineWalletGenerator_fromObjectData_certificate(certificate)
#    url = openfood_API_BASE_URL + openfood_API_ORGANIZATION_CERTIFICATE + str(certificate['id']) + "/"
#    data = {"raddress": offline_wallet['address'], "pubkey": offline_wallet['pubkey']}
#    openfood.patchWrapper(url, data=data)
#    # TODO try/block
#    funding_txid = openfood.fund_certificate(offline_wallet['address'])
#    print("Funding tx " + funding_txid)
#    # TODO add fundingtx, check for unfunded offline wallets

print("End of script")
