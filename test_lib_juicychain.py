from lib.openfood_env import EXPLORER_URL
from lib.openfood_env import THIS_NODE_WALLET
from lib.openfood_env import THIS_NODE_WIF
from lib.openfood_env import IMPORT_API_BASE_URL
from lib.openfood_env import DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
from lib.openfood_env import DEV_IMPORT_API_RAW_REFRESCO_PATH

#from lib.openfood_env import TEST_GEN_WALLET_PASSPHRASE
#from lib.openfood_env import TEST_GEN_WALLET_ADDRESS
#from lib.openfood_env import TEST_GEN_WALLET_WIF
#from lib.openfood_env import TEST_GEN_WALLET_PUBKEY
from lib.openfood_env import openfood_API_BASE_URL
from lib.openfood_env import openfood_API_ORGANIZATION_CERTIFICATE
from lib import openfood
from dotenv import load_dotenv
import json
import pytest
load_dotenv(verbose=True)
SCRIPT_VERSION = 0.00012111

RPC = ""

openfood.connect_node()

@pytest.fixture(scope="session", autouse=True)
def execute_before_any_test():
    # your setup code goes here, executed ahead of first test
    openfood.connect_node()
    print("here we go")


import string
import random
import time
import requests
import json
import sys
import os
import binascii
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(verbose=True)

def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    res = time.strftime(format, time.localtime(ptime))
    print(res)
    return res


def generate_random_hex(size):
	return binascii.b2a_hex(os.urandom(size))

def random_date(start, end, prop):
	return str_time_prop(start, end, '%Y-%m-%d', prop)

def random_date_cert(start, end, prop):
        return str_time_prop(start, end, '%d-%m-%Y', prop)

def make_random_string(length):
	str = ""
	for x in range(0,length):
		str = str + random.choice(string.ascii_letters)
	
	return str

def get_random_number(length):
	number = random.randint(10 ** (length-1), 10 ** (length))
	return number

def days(date):
	ret = ""
	for a in date:
		if a == '-':
			ret = ""
		else:
			ret = ret + a 
	return int(ret)
def create_random_batch():
	RANDOM_VAL_ANFP=get_random_number(5)
	RANDOM_VAL_DFP="100EP PA Apfelsaft naturtrüb NF"
	RANDOM_VAL_BNFP=make_random_string(10)
	RANDOM_VAL_PC="DE"
	RANDOM_VAL_PL="Herrath"
	RANDOM_VAL_RMN=11200100520
	RANDOM_VAL_PON=get_random_number(8)
	RANDOM_VAL_POP=get_random_number(2)

	PDS=random_date("2020-1-1", "2020-11-15", random.random())
	PDE=random_date(PDS, "2020-11-15", random.random())
	BBD=PDE

	JDS=days(PDS)
	JDE=days(PDE)

	params = { "anfp": RANDOM_VAL_ANFP, "dfp": RANDOM_VAL_DFP, "bnfp": RANDOM_VAL_BNFP, "pds":PDS , "pde":PDE, "jds":JDS, "jde":JDE , "bbd":BBD , "pc": RANDOM_VAL_PC, "pl": RANDOM_VAL_PL, "rmn":RANDOM_VAL_RMN, "pon":RANDOM_VAL_PON, "pop":RANDOM_VAL_POP }
	print(params)
	return params

def properties_test(tests):
	for test in tests:
		print(test)
		assert test['anfp']
		assert test['dfp']
		assert test['bnfp']
		assert test['pds']
		assert test['pde']
		assert test['jds']
		assert test['jde']
		assert test['bbd']
		assert test['pc']
		assert test['pl']
		assert test['rmn']
		assert test['pon']
		assert test['pop']

def properties_test_cert(tests):
	for test in tests:
		print(test)
		assert test['id']
		assert test['name']
		assert test['date_issue']
		assert test['date_expiry']
		assert test['issuer']
		assert test['identifier']
		assert not test['pubkey']
		assert not test['raddress']
		assert test['organization']


def properties_test_cert_with_addie(tests):
        for test in tests:
                print(test)
                assert test['id']
                assert test['name']
                assert test['date_issue']
                assert test['date_expiry']
                assert test['issuer']
                assert test['identifier']
                assert test['pubkey']
                assert test['raddress']
                assert test['organization']


# TEST FUNCTIONS
def test_postWrapperr():
    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_PATH
    data = create_random_batch()
    test = openfood.postWrapper(url, data)
    test = json.loads(test)
    properties_test( [ test] )


# ORACLE TEST STUFF
def test_oracle_create():
	response = openfood.oracle_create("NYWTHR","Weather in NYC","L")
	print(response)
	assert response['result'] == "success"


def test_oracle_fund():
	hex = openfood.oracle_create("chris", "this is a test", "S")
	if hex['result'] == "success":
        	response = openfood.oracle_fund(hex['hex'])
        	assert response['result']['result'] == "success"
	else:
		assert True == hex['result']

#def oracle register, first create and fund need to work...

def test_oracle_list():
	response = openfood.oracle_list()
	print(response)
	assert type(response) == type([])
	for oracle in response:
		assert oracle
		assert len(oracle) == 64


def oracle_properties(oracle):
	print(oracle)
	assert oracle['result'] == "success"
	assert oracle['txid']
	assert oracle['name']
	assert oracle['description']
	assert oracle['format']
	assert oracle['marker']
	for registered in oracle['registered']:
		assert registered['publisher']
		assert registered['baton']
		assert registered['batontxid']
		assert registered['lifetime']
		assert registered['funds']
		assert registered['datafee']

def test_oracle_info():
	response = openfood.oracle_list()
	assert response[0]
	for oracle in response:
		response = openfood.oracle_info(oracle)
		oracle_properties(response)

def test_oracle_sub():
	response = openfood.oracle_list()
	assert response[0]
	for oracle in response:
		response = openfood.oracle_info(oracle)
		oracle_properties(response)
		response = openfood.oracle_subscribe(oracle, response['registered'][0]['publisher'], "0")
		print(response)
		assert response['result'] == "success"

def test_oracle_sample():
	response = openfood.oracle_list()
	assert response[0]
	for oracle in response:
		response = openfood.oracle_info(oracle)
		response = openfood.oracle_samples(oracle, response['registered'][0]['baton'], "1")
		assert response['result'] == "success"

def test_find_oracleid_with_pubkey():
	response = openfood.oracle_list()
	assert response[0]
	for oracle in response:
		response = openfood.oracle_info(oracle)
		print(response)
		orc_res = openfood.find_oracleid_with_pubkey(response['registered'][0]['publisher'])
		assert orc_res == oracle

#02f2cdd772ab57eae35996c0d39ad34fe06304c4d3981ffe71a596634fa26f8744
#put is no longer used
@pytest.mark.skip
def test_putWrapperr():
    url = EXPLORER_URL
    data = {'sender_raddress': THIS_NODE_WALLET,
            'tsintegrity': "1", 'sender_name': 'ORG WALLET', 'txid': "testtest"}

    test = openfood.putWrapper(url, data)
    assert is_json(test) is True

def test_getWrapperr():
    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_PATH

    test = openfood.getWrapper(url)
    test = json.loads(test)

    properties_test( test )


def test_certificates_no_addy():
    test = openfood.get_certificates_no_timestamp()
    properties_test_cert(test)

def test_batchess_no_addy():
    test = openfood.get_batches_no_timestamp()
    if test == []:
        print("if this is empty the rest of the import api is not testable. Run the scripts in the import api in the docker compose to fill it back up (the austria juice script)")
        assert False == True
    properties_test(test)


def test_get_batches():
    test = openfood.get_batches()

    properties_test(test)

#it seems like this is no longer a possible call
@pytest.mark.skip
def test_patchWrapperr():
    url = EXPLORER_URL
    data = {'sender_raddress': THIS_NODE_WALLET,
            'tsintegrity': "1", 'sender_name': 'ORG WALLET', 'txid': "testtest"}

    test = openfood.patchWrapper(url, data)
    assert is_json(test) is True

def test_connect_node():
    test = openfood.connect_node()
    assert test == True


def test_signmessage_wrapper():
    data = "chris"
    deterministic = "H/RhRKf1Na1ZG142wrAmheGYnZIXBYnaZO65/Z2oJeeoTASUd5oRhHnzejRAQ0yFdUlAb8zX1HNMRbqZJ1u+awY="
    test = openfood.signmessage_wrapper(data)

    assert test == deterministic


@pytest.mark.skip
#php seems broken
def test_offlineWalletGenerator_fromObjectData_certificate():
    obj = {
        "issuer": "chris",
        "date_issue": "mylo",
        "date_expiry": "yesterday",
        "identifier": "1010011000013"
    }

    test = openfood.offlineWalletGenerator_fromObjectData_certificate(obj)

    print(test['address'])

    assert True == False


def properties_jcapi_test(test):
	assert test['id']
	assert test['name']
	assert test['pubkey']
	assert test['raddress']

def test_get_jcapi_organization():
    test = openfood.get_jcapi_organization()
    properties_jcapi_test(test)
    


def test_get_certificate_for_batch():
    test = openfood.get_certificate_for_batch()
    properties_test_cert_with_addie([ test ])

def test_utxo_bundle_amount():
    utxos_obj = [
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 10,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      },
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 11,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      }
    ]

    test = openfood.utxo_bundle_amount(utxos_obj)

    assert test == 2.2


def test_createrawtx_wrapper():
    utxos_obj = [
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 10,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      },
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 11,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      }
    ]

    txids = []
    vouts = []
    amount = openfood.utxo_bundle_amount(utxos_obj)
    to_address = THIS_NODE_WALLET

    for utxo in utxos_obj:
        txids = txids + [ utxo['txid'] ]
        vouts = vouts + [ utxo['vout'] ]

    test = openfood.createrawtx_wrapper(txids, vouts, to_address, amount)
    test = openfood.decoderawtx_wrapper(test)

    print(test)
    transactions_properties(test)


def transactions_properties( tx ):
	assert tx['txid']
	assert tx['overwintered']
	assert tx['version']
	assert tx['versiongroupid']
	assert type(tx['locktime']) == type(0)
	assert tx['expiryheight']
	assert tx['vin']
	for input in tx['vin']:
		assert input['txid']
		assert input['vout']
		assert input['scriptSig']
		assert input['scriptSig']['asm'] or input['scriptSig']['asm'] == ''
		assert input['scriptSig']['hex'] or input['scriptSig']['hex'] == ''
		assert input['sequence']
	assert tx['vout']
	for input in tx['vout']:
		assert input['value']
		assert input['valueZat']
		assert type(input['n']) == type(0)
		assert input['scriptPubKey']
		assert input['scriptPubKey']['asm']
		assert input['scriptPubKey']['hex']
		assert input['scriptPubKey']['reqSigs']
		assert input['scriptPubKey']['type']
		assert input['scriptPubKey']['addresses']
		for addie in input['scriptPubKey']['addresses']:
			assert addie[0] == 'R'
			assert len(addie) == 34 
	assert type(tx['vjoinsplit']) == type([])
	assert type(tx['valueBalance']) == type(0.0)
	assert type(tx['vShieldedSpend']) == type([])
	assert type(tx['vShieldedOutput']) == type([])


#@pytest.mark.skip
def test_createrawtxwithchange():
    utxos_obj = [
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 10,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      },
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 11,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      }
    ]

    txids = []
    vouts = []
    amount = openfood.utxo_bundle_amount(utxos_obj)
    change_amount = 0.2

    to_address = change_address = THIS_NODE_WALLET

    for utxo in utxos_obj:
        txids = txids + [ utxo['txid'] ]
        vouts = vouts + [ utxo['vout'] ]

    test = openfood.createrawtxwithchange(txids, vouts, to_address, amount, change_address, change_amount)

    test = openfood.decoderawtx_wrapper(test)
    test = json.dumps(test)

    assert is_json(test) == True


def sign_properties( tx ):
	assert tx[0]['rawtx']
	assert tx[1]['amounts']

def test_createrawtx5():
    utxos_obj = [
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 10,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      },
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 11,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      }
    ]

    amount = openfood.utxo_bundle_amount(utxos_obj)
    fee = 0.2

    to_address = change_address = THIS_NODE_WALLET

    utxos = json.dumps(utxos_obj)

    test = openfood.createrawtx5(utxos, len(utxos_obj), to_address, fee, change_address)
    print(test)
    sign_properties(test)


# @pytest.mark.skip
@pytest.mark.skip
def test_signtx():
    kmd_unsigned_tx_serialized = "0400008085202f8902b8be1dbe757519f6ce972e1f62a4eca1d6bed2cc5817fbb151fbc32ed95579270a00000000ffffffffb8be1dbe757519f6ce972e1f62a4eca1d6bed2cc5817fbb151fbc32ed95579270b00000000ffffffff01002d3101000000001976a914cbeb5be30aaede02316436da368ee57cfcd8187988ac000000008fea01000000000000000000000000"
    utxos_obj = [
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 10,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      },
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 11,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      }
    ]

    amounts = openfood.utxo_bundle_amount(utxos_obj)

    wif = THIS_NODE_WIF

    test = openfood.signtx(kmd_unsigned_tx_serialized, amounts, wif)
    print(test)

    assert test == True


#test function not done
@pytest.mark.skip
def test_broadcast_via_explorer():

    test = broadcast_via_explorer(explorer_url, signedtx)


def test_createrawtx4():
    utxos_obj = [
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 10,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      },
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 11,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      }
    ]

    amount = openfood.utxo_bundle_amount(utxos_obj)
    fee = 0.2

    to_address = change_address = THIS_NODE_WALLET

    utxos = json.dumps(utxos_obj)

    test = openfood.createrawtx4(utxos, len(utxos_obj), to_address, fee)

    sign_properties(test)


def test_decoderawtx_wrapper():
    tx = "0400008085202f8902b8be1dbe757519f6ce972e1f62a4eca1d6bed2cc5817fbb151fbc32ed95579270a00000000ffffffffb8be1dbe757519f6ce972e1f62a4eca1d6bed2cc5817fbb151fbc32ed95579270b00000000ffffffff01002d3101000000001976a914cbeb5be30aaede02316436da368ee57cfcd8187988ac000000008fea01000000000000000000000000"
    decode = {'txid': '554f123c994f1c38b1a8e2d1f542669c84ab3eb260c372aa0b2df21e3590448d', 'overwintered': True, 'version': 4, 'versiongroupid': '892f2085', 'locktime': 0, 'expiryheight': 125583, 'vin': [{'txid': '277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8', 'vout': 10, 'scriptSig': {'asm': '', 'hex': ''}, 'sequence': 4294967295}, {'txid': '277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8', 'vout': 11, 'scriptSig': {'asm': '', 'hex': ''}, 'sequence': 4294967295}], 'vout': [{'value': 0.2, 'valueZat': 20000000, 'n': 0, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 cbeb5be30aaede02316436da368ee57cfcd81879 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a914cbeb5be30aaede02316436da368ee57cfcd8187988ac', 'reqSigs': 1, 'type': 'pubkeyhash', 'addresses': ['RTsRCUy4cJoyTKJfSWcidEwcj7g1Y3gTG5']}}], 'vjoinsplit': [], 'valueBalance': 0.0, 'vShieldedSpend': [], 'vShieldedOutput': []}

    test = openfood.decoderawtx_wrapper(tx)

    assert test == decode

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


def test_check_node_wallet():
    test = openfood.check_node_wallet()
    assert test is True


def test_check_sync():
    test = openfood.check_sync()
    assert type(10) == type(test)


# @pytest.mark.skip
def test_explorer_get_utxos():
    try:
        test = openfood.explorer_get_utxos("RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW")
        assert is_json(test) is True
    except Exception as e:
        assert e is True


def test_gen_wallet():
    test_wallet = openfood.gen_wallet("TEST_GEN_WALLET_PASSPHRASE")
    assert TEST_GEN_WALLET_ADDRESS == test_wallet['address']
    assert TEST_GEN_WALLET_PUBKEY == test_wallet['pubkey']
    assert TEST_GEN_WALLET_WIF == test_wallet['wif']
    assert test_wallet['address'][0] == 'R'


def test_get_batches_no_timestamp():
    test = openfood.get_batches_no_timestamp()
    properties_test(test)


def test_sendtoaddress_wrapper():
    test = openfood.sendtoaddress_wrapper(THIS_NODE_WALLET, 0.1)
    print(test)
    assert not(" " in test)


#function no longer in lib
@pytest.mark.skip
def test_batch_wallets_generate_timestamping():
    test = openfood.get_wbatches_no_timestamp()
    test = openfood.batch_wallets_generate_timestamping(test[0], test[0]['id'])
    test = json.dumps(test)
    print(test)
    assert True == False


def test_batch_wallets_timestamping_update():
    test = openfood.get_batches()
    test = openfood.batch_wallets_timestamping_update(test[0])
    test = json.loads(test)
    properties_test( [ test ] )


def test_start_stop():
    test = openfood.get_batches_no_timestamp()
    batch_wallets_timestamping_start(test)
    batch_wallets_timestamping_end(test)


#we are here
def batch_wallets_timestamping_start(testObj):

    utxos_obj = [
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 10,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      },
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 11,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      }
    ]

    amount = openfood.utxo_bundle_amount(utxos_obj)
    fee = 0.2

    to_address = change_address = THIS_NODE_WALLET

    utxos = json.dumps(utxos_obj)

    rawtx_info = openfood.createrawtx5(utxos, len(utxos_obj), to_address, fee, change_address)
    print("info" + str(rawtx_info))
    rawtx_info = openfood.decoderawtx_wrapper(rawtx_info[0]['rawtx'])
    print("info" + str(rawtx_info))
    test = openfood.batch_wallets_timestamping_start(testObj[0], rawtx_info['txid'])

    #test = openfood.batch_wallets_generate_timestamping(test[0], test[0]['id'])
    test = json.dumps(test)

    print(test)
    assert is_json(test) == True

def batch_wallets_timestamping_end(testObj):
    utxos_obj = [
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 10,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      },
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 11,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      }
    ]

    amount = openfood.utxo_bundle_amount(utxos_obj)
    fee = 0.2

    to_address = change_address = THIS_NODE_WALLET

    utxos = json.dumps(utxos_obj)

    rawtx_info = openfood.createrawtx5(utxos, len(utxos_obj), to_address, fee, change_address)
    print("info" + str(rawtx_info))
    rawtx_info = openfood.decoderawtx_wrapper(rawtx_info[0]['rawtx'])
    print("info" + str(rawtx_info))
    test = openfood.batch_wallets_timestamping_end(testObj[0], rawtx_info['txid'])

    #test = openfood.batch_wallets_generate_timestamping(test[0], test[0]['id'])
    test = json.dumps(test)

    assert is_json(test) == True

def test_batch_wallets_fund_integrity_start():
    test = openfood.batch_wallets_fund_integrity_start(THIS_NODE_WALLET)
    assert type(int(test, 16)) == type(10)

def test_batch_wallets_fund_integrity_end():
    test = openfood.batch_wallets_fund_integrity_end(THIS_NODE_WALLET)
    assert type(int(test, 16)) == type(10)

def test_timestamping_save_batch_links():
    test = openfood.get_batches()
    utxos_obj = [
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 10,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      },
      {
        "address": "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW",
        "txid": "277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8",
        "vout": 11,
        "scriptPubKey": "76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac",
        "amount": 1.1,
        "satoshis": 110000000,
        "height": 11461,
        "confirmations": 1550
      }
    ]

    amount = openfood.utxo_bundle_amount(utxos_obj)
    fee = 0.2

    to_address = change_address = THIS_NODE_WALLET

    utxos = json.dumps(utxos_obj)

    rawtx_info = openfood.createrawtx5(utxos, len(utxos_obj), to_address, fee, change_address)
    rawtx_info = openfood.decoderawtx_wrapper(rawtx_info[0]['rawtx'])
    test = openfood.timestamping_save_batch_links(test[0]['id'], rawtx_info['txid'])
    assert test == True

def test_sendmany_wrapper():
    json_object = {THIS_NODE_WALLET: SCRIPT_VERSION}
    test = openfood.sendmany_wrapper(THIS_NODE_WALLET, json_object)
    print(test)
    assert not (" " in test)
