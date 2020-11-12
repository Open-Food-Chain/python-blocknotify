from lib.juicychain_env import EXPLORER_URL
from lib.juicychain_env import THIS_NODE_ADDRESS
from lib.juicychain_env import THIS_NODE_WIF
from lib.juicychain_env import TEST_GEN_WALLET_PASSPHRASE
from lib.juicychain_env import TEST_GEN_WALLET_ADDRESS
from lib.juicychain_env import TEST_GEN_WALLET_WIF
from lib.juicychain_env import TEST_GEN_WALLET_PUBKEY
from lib.juicychain_env import JUICYCHAIN_API_BASE_URL
from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION_CERTIFICATE
from lib import juicychain
from dotenv import load_dotenv
import json
import pytest
load_dotenv(verbose=True)
SCRIPT_VERSION = 0.00012111

RPC = ""

juicychain.connect_node()

@pytest.fixture(scope="session", autouse=True)
def execute_before_any_test():
    # your setup code goes here, executed ahead of first test
    juicychain.connect_node()
    print("here we go")

# TEST FUNCTIONS
def test_postWrapperr():
    url = EXPLORER_URL
    data = {'sender_raddress': THIS_NODE_ADDRESS,
            'tsintegrity': "1", 'sender_name': 'ORG WALLET', 'txid': "testtest"}

    test = juicychain.postWrapper(url, data)
    assert is_json(test) is True


def test_putWrapperr():
    url = EXPLORER_URL
    data = {'sender_raddress': THIS_NODE_ADDRESS,
            'tsintegrity': "1", 'sender_name': 'ORG WALLET', 'txid': "testtest"}

    test = juicychain.putWrapper(url, data)
    assert is_json(test) is True

def test_getWrapperr():
    url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + "18/"

    test = juicychain.getWrapper(url)

    assert is_json(test) is True


def test_certificates_no_addy():
    test = juicychain.get_certificates_no_timestamp()
    test = json.dumps(test)
    assert is_json(test) is True

def test_batchess_no_addy():
    test = juicychain.get_batches_no_timestamp()
    test = json.dumps(test)
    if test == []:
        print("if this is empty the rest of the import api is not testable. Run the scripts in the import api in the docker compose to fill it back up (the austria juice script)")
        assert False == True
    assert is_json(test) is True

def test_get_batches():
    test = juicychain.get_batches()
    test = json.dumps(test)

    assert is_json(test) is True

def test_patchWrapperr():
    url = EXPLORER_URL
    data = {'sender_raddress': THIS_NODE_ADDRESS,
            'tsintegrity': "1", 'sender_name': 'ORG WALLET', 'txid': "testtest"}

    test = juicychain.patchWrapper(url, data)
    assert is_json(test) is True

def test_connect_node():
    test = juicychain.connect_node()
    assert test == True


def test_signmessage_wrapper():
    data = "chris"
    deterministic = "H/RhRKf1Na1ZG142wrAmheGYnZIXBYnaZO65/Z2oJeeoTASUd5oRhHnzejRAQ0yFdUlAb8zX1HNMRbqZJ1u+awY="
    test = juicychain.signmessage_wrapper(data)

    assert test == deterministic


def test_offlineWalletGenerator_fromObjectData_certificate():
    obj = {
        "issuer": "chris",
        "date_issue": "mylo",
        "date_expiry": "yesterday",
        "identifier": "1010011000013"
    }

    test = juicychain.offlineWalletGenerator_fromObjectData_certificate(obj)

    print(test['address'])

    assert test['address'][0] == 'R'


def test_get_jcapi_organization():
    test = juicychain.get_jcapi_organization()

    test = json.dumps(test)

    assert is_json(test) == True


def test_get_certificate_for_batch():
    test = juicychain.get_certificate_for_batch()
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

    test = juicychain.utxo_bundle_amount(utxos_obj)

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
    amount = juicychain.utxo_bundle_amount(utxos_obj)
    to_address = THIS_NODE_ADDRESS

    for utxo in utxos_obj:
        txids = txids + [ utxo['txid'] ]
        vouts = vouts + [ utxo['vout'] ]

    test = juicychain.createrawtx_wrapper(txids, vouts, to_address, amount)
    test = juicychain.decoderawtx_wrapper(test)
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
    amount = juicychain.utxo_bundle_amount(utxos_obj)
    change_amount = 0.2

    to_address = change_address = THIS_NODE_ADDRESS

    for utxo in utxos_obj:
        txids = txids + [ utxo['txid'] ]
        vouts = vouts + [ utxo['vout'] ]

    test = juicychain.createrawtxwithchange(txids, vouts, to_address, amount, change_address, change_amount)

    test = juicychain.decoderawtx_wrapper(test)
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

    amount = juicychain.utxo_bundle_amount(utxos_obj)
    fee = 0.2

    to_address = change_address = THIS_NODE_ADDRESS

    utxos = json.dumps(utxos_obj)

    test = juicychain.createrawtx5(utxos, len(utxos_obj), to_address, fee, change_address)
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

    amounts = juicychain.utxo_bundle_amount(utxos_obj)

    wif = THIS_NODE_WIF

    test = juicychain.signtx(kmd_unsigned_tx_serialized, amounts, wif)
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

    amount = juicychain.utxo_bundle_amount(utxos_obj)
    fee = 0.2

    to_address = change_address = THIS_NODE_ADDRESS

    utxos = json.dumps(utxos_obj)

    test = juicychain.createrawtx4(utxos, len(utxos_obj), to_address, fee)
    test = json.dumps(test)

    assert is_json(test) == True


def test_decoderawtx_wrapper():
    tx = "0400008085202f8902b8be1dbe757519f6ce972e1f62a4eca1d6bed2cc5817fbb151fbc32ed95579270a00000000ffffffffb8be1dbe757519f6ce972e1f62a4eca1d6bed2cc5817fbb151fbc32ed95579270b00000000ffffffff01002d3101000000001976a914cbeb5be30aaede02316436da368ee57cfcd8187988ac000000008fea01000000000000000000000000"
    decode = {'txid': '554f123c994f1c38b1a8e2d1f542669c84ab3eb260c372aa0b2df21e3590448d', 'overwintered': True, 'version': 4, 'versiongroupid': '892f2085', 'locktime': 0, 'expiryheight': 125583, 'vin': [{'txid': '277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8', 'vout': 10, 'scriptSig': {'asm': '', 'hex': ''}, 'sequence': 4294967295}, {'txid': '277955d92ec3fb51b1fb1758ccd2bed6a1eca4621f2e97cef6197575be1dbeb8', 'vout': 11, 'scriptSig': {'asm': '', 'hex': ''}, 'sequence': 4294967295}], 'vout': [{'value': 0.2, 'valueZat': 20000000, 'n': 0, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 cbeb5be30aaede02316436da368ee57cfcd81879 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a914cbeb5be30aaede02316436da368ee57cfcd8187988ac', 'reqSigs': 1, 'type': 'pubkeyhash', 'addresses': ['RTsRCUy4cJoyTKJfSWcidEwcj7g1Y3gTG5']}}], 'vjoinsplit': [], 'valueBalance': 0.0, 'vShieldedSpend': [], 'vShieldedOutput': []}

    test = juicychain.decoderawtx_wrapper(tx)

    assert test == decode

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


def test_check_node_wallet():
    test = juicychain.check_node_wallet()
    assert test is True


def test_check_sync():
    test = juicychain.check_sync()
    assert type(10) == type(test)


# @pytest.mark.skip
def test_explorer_get_utxos():
    try:
        test = juicychain.explorer_get_utxos("RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW")
        assert is_json(test) is True
    except Exception as e:
        assert e is True


def test_gen_wallet():
    test_wallet = juicychain.gen_wallet(TEST_GEN_WALLET_PASSPHRASE)
    #assert TEST_GEN_WALLET_ADDRESS == test_wallet['address']
    #assert TEST_GEN_WALLET_PUBKEY == test_wallet['pubkey']
    #assert TEST_GEN_WALLET_WIF == test_wallet['wif']
    assert test_wallet['address'][0] == 'R'


def test_get_batches_no_timestamp():
    test = juicychain.get_batches_no_timestamp()
    assert type(test) == type(['this', 'is', 'an', 'test', 'array'])


def test_sendtoaddress_wrapper():
    test = juicychain.sendtoaddress_wrapper(THIS_NODE_ADDRESS, 0.1)
    assert not (" " in test)



def test_batch_wallets_generate_timestamping():
    test = juicychain.get_batches_no_timestamp()
    test = juicychain.batch_wallets_generate_timestamping(test[0], test[0]['id'])
    test = json.dumps(test)
    assert is_json(test) == True


def test_batch_wallets_timestamping_update():
    test = juicychain.get_batches()
    test = juicychain.batch_wallets_timestamping_update(test[0])
    test = json.dumps(test)
    assert is_json(test) == True


def test_start_stop():
    test = juicychain.get_batches_no_timestamp()
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

    amount = juicychain.utxo_bundle_amount(utxos_obj)
    fee = 0.2

    to_address = change_address = THIS_NODE_ADDRESS

    utxos = json.dumps(utxos_obj)

    rawtx_info = juicychain.createrawtx5(utxos, len(utxos_obj), to_address, fee, change_address)
    print("info" + str(rawtx_info))
    rawtx_info = juicychain.decoderawtx_wrapper(rawtx_info[0]['rawtx'])
    print("info" + str(rawtx_info))
    test = juicychain.batch_wallets_timestamping_start(testObj[0], rawtx_info['txid'])

    #test = juicychain.batch_wallets_generate_timestamping(test[0], test[0]['id'])
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

    amount = juicychain.utxo_bundle_amount(utxos_obj)
    fee = 0.2

    to_address = change_address = THIS_NODE_ADDRESS

    utxos = json.dumps(utxos_obj)

    rawtx_info = juicychain.createrawtx5(utxos, len(utxos_obj), to_address, fee, change_address)
    print("info" + str(rawtx_info))
    rawtx_info = juicychain.decoderawtx_wrapper(rawtx_info[0]['rawtx'])
    print("info" + str(rawtx_info))
    test = juicychain.batch_wallets_timestamping_end(testObj[0], rawtx_info['txid'])

    #test = juicychain.batch_wallets_generate_timestamping(test[0], test[0]['id'])
    test = json.dumps(test)

    assert is_json(test) == True

def test_batch_wallets_fund_integrity_start():
    test = juicychain.batch_wallets_fund_integrity_start(THIS_NODE_ADDRESS)
    assert type(int(test, 16)) == type(10)

def test_batch_wallets_fund_integrity_end():
    test = juicychain.batch_wallets_fund_integrity_end(THIS_NODE_ADDRESS)
    assert type(int(test, 16)) == type(10)

def test_timestamping_save_batch_links():
    test = juicychain.get_batches()
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

    amount = juicychain.utxo_bundle_amount(utxos_obj)
    fee = 0.2

    to_address = change_address = THIS_NODE_ADDRESS

    utxos = json.dumps(utxos_obj)

    rawtx_info = juicychain.createrawtx5(utxos, len(utxos_obj), to_address, fee, change_address)
    rawtx_info = juicychain.decoderawtx_wrapper(rawtx_info[0]['rawtx'])
    test = juicychain.timestamping_save_batch_links(test[0]['id'], rawtx_info['txid'])
    assert test == True

def test_sendmany_wrapper():
    json_object = {THIS_NODE_ADDRESS: SCRIPT_VERSION}
    test = juicychain.sendmany_wrapper(THIS_NODE_ADDRESS, json_object)
    print(test)
    assert not (" " in test)
