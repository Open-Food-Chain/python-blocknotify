from lib.juicychain_env import EXPLORER_URL
from lib.juicychain_env import THIS_NODE_ADDRESS
from lib.juicychain_env import TEST_GEN_WALLET_PASSPHRASE
from lib.juicychain_env import TEST_GEN_WALLET_ADDRESS
from lib.juicychain_env import TEST_GEN_WALLET_WIF
from lib.juicychain_env import TEST_GEN_WALLET_PUBKEY
from lib import juicychain
from dotenv import load_dotenv
import json
import pytest
load_dotenv(verbose=True)
SCRIPT_VERSION = 0.00012111

RPC = ""


@pytest.fixture(scope="session", autouse=True)
def execute_before_any_test():
    # your setup code goes here, executed ahead of first test
    juicychain.connect_node()

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

# TEST FUNCTIONS

# @pytest.mark.skip


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
    assert TEST_GEN_WALLET_ADDRESS == test_wallet['address']
    assert TEST_GEN_WALLET_PUBKEY == test_wallet['pubkey']
    assert TEST_GEN_WALLET_WIF == test_wallet['wif']
    assert test_wallet['address'][0] == 'R'


def test_get_batches_no_timestamp():
    test = juicychain.get_batches_no_timestamp()
    assert type(test) == type(['this', 'is', 'an', 'test', 'array'])


def test_sendtoaddress_wrapper():
    test = juicychain.sendtoaddress_wrapper(THIS_NODE_ADDRESS, 0.1)
    assert not (" " in test)


def test_sendmany_wrapper():
    json_object = {THIS_NODE_ADDRESS: SCRIPT_VERSION}
    test = juicychain.sendmany_wrapper(THIS_NODE_ADDRESS, json_object)
    print(test)
    assert not (" " in test)
