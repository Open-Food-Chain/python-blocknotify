from lib.openfood_env import EXPLORER_URL
from lib.openfood_env import THIS_NODE_WALLET
from lib.openfood_env import THIS_NODE_WIF
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

# TEST FUNCTIONS
def test_postWrapperr():
    url = EXPLORER_URL
    data = {'sender_raddress': THIS_NODE_WALLET,
            'tsintegrity': "1", 'sender_name': 'ORG WALLET', 'txid': "testtest"}

    test = openfood.postWrapper(url, data)
    assert is_json(test) is True


def test_putWrapperr():
    url = EXPLORER_URL
    data = {'sender_raddress': THIS_NODE_WALLET,
            'tsintegrity': "1", 'sender_name': 'ORG WALLET', 'txid': "testtest"}

    test = openfood.putWrapper(url, data)
    assert is_json(test) is True

def test_getWrapperr():
    url = openfood_API_BASE_URL + openfood_API_ORGANIZATION_CERTIFICATE + "18/"

    test = openfood.getWrapper(url)

    assert is_json(test) is True


def test_certificates_no_addy():
    test = openfood.get_certificates_no_timestamp()
    test = json.dumps(test)
    assert is_json(test) is True

def test_batchess_no_addy():
    test = openfood.get_batches_no_timestamp()
    test = json.dumps(test)
    if test == []:
        print("if this is empty the rest of the import api is not testable. Run the scripts in the import api in the docker compose to fill it back up (the austria juice script)")
        assert False == True
    assert is_json(test) is True

def test_get_batches():
    test = openfood.get_batches()
    test = json.dumps(test)

    assert is_json(test) is True

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


def test_offlineWalletGenerator_fromObjectData_certificate():
    obj = {
        "issuer": "chris",
        "date_issue": "mylo",
        "date_expiry": "yesterday",
        "identifier": "1010011000013"
    }

    test = openfood.offlineWalletGenerator_fromObjectData_certificate(obj)

    print(test['address'])

    assert test['address'][0] == 'R'


def test_get_jcapi_organization():
    test = openfood.get_jcapi_organization()

    test = json.dumps(test)

    assert is_json(test) == True


def test_get_certificate_for_batch():
    test = openfood.get_certificate_for_batch()
    test = json.dumps(test)
    assert is_json(test) == True

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
    test = json.dumps(test)

    assert is_json(test) == True


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
    test = json.dumps(test)
    assert is_json(test) == True
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
    test = json.dumps(test)

    assert is_json(test) == True


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


#def test_gen_wallet():
  #  test_wallet = openfood.gen_wallet(TEST_GEN_WALLET_PASSPHRASE)
    #assert TEST_GEN_WALLET_ADDRESS == test_wallet['address']
    #assert TEST_GEN_WALLET_PUBKEY == test_wallet['pubkey']
    #assert TEST_GEN_WALLET_WIF == test_wallet['wif']
   # assert test_wallet['address'][0] == 'R'


def test_get_batches_no_timestamp():
    test = openfood.get_batches_no_timestamp()
    assert type(test) == type(['this', 'is', 'an', 'test', 'array'])


def test_sendtoaddress_wrapper():
    test = openfood.sendtoaddress_wrapper(THIS_NODE_WALLET, 0.1)
    assert not (" " in test)



def test_batch_wallets_generate_timestamping():
    test = openfood.get_batches_no_timestamp()
    test = openfood.batch_wallets_generate_timestamping(test[0], test[0]['id'])
    test = json.dumps(test)
    assert is_json(test) == True


def test_batch_wallets_timestamping_update():
    test = openfood.get_batches()
    test = openfood.batch_wallets_timestamping_update(test[0])
    test = json.dumps(test)
    assert is_json(test) == True


def test_start_stop():
    test = openfood.get_batches_no_timestamp()
    batch_wallets_timestamping_start(test)
    batch_wallets_timestamping_end(test)



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
