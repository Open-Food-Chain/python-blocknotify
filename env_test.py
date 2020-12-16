from lib import openfood_env
from lib import openfood
import requests
from dotenv import load_dotenv
import json
#import pytest
import os
load_dotenv(verbose=True)


def test_explorer():
	explorer = openfood_env.EXPLORER_URL + "address/RL5CYAJaAM4pJB3bSVn5kDmMWg62onMqeY"
	res = requests.get(explorer)
	print(res.text)
	assert int(openfood_env.openfood_EXPLORER_MAINNET_UNCHAIN_PORT)

def test_this_node():
	assert len(openfood_env.THIS_NODE_WIF) == 52

	assert openfood_env.THIS_NODE_PUBKEY[0:2] == '02'
	assert len(openfood_env.THIS_NODE_PUBKEY) == 66

	assert openfood_env.THIS_NODE_RADDRESS[0] == 'R'
	assert len(openfood_env.THIS_NODE_RADDRESS) == 34

	assert openfood_env.THIS_NODE_RADDRESS == openfood_env.THIS_NODE_WALLET

def test_rpc_values():
	assert openfood.connect_node == True
	assert openfood_env.RPC_PORT == 24708
	assert int(openfood_env.RPC_PORT)
	assert openfood_env.KOMODO_NODE[0:4] == '127.'

def test_rest():
	assert openfood_env.openfood_API_VERSION_PATH == 'api/v1/'
	assert openfood_env.openfood_API_HOST[0:4] == '127.'
	assert openfood_env.IMPORT_API_HOST[0:4] == '127.'
	assert openfood_env.IMPORT_API_PORT == '8777'
	assert True == False
