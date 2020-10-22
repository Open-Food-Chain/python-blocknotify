from lib import rpclib
from slickrpc import Proxy
from lib import transaction, bitcoin, util
from lib.util import bfh, bh2u
from lib.transaction import Transaction

import requests
import pytest
import subprocess
import json
import sys
import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

IMPORT_API_HOST = str(os.getenv("IMPORT_API_HOST"))
IMPORT_API_PORT = str(os.getenv("IMPORT_API_PORT"))
IMPORT_API_BASE_URL =  IMPORT_API_HOST

rpc_user = os.getenv("IJUICE_KOMODO_NODE_USERNAME")
rpc_password = os.getenv("IJUICE_KOMODO_NODE_PASSWORD")
port = os.getenv("IJUICE_KOMODO_NODE_RPC_PORT")

address = ""
amount = 0
greedy = True

if len(sys.argv) >= 3:
    address = sys.argv[1]
    amount = float(sys.argv[2])
    greedy = bool(sys.argv[3])

#this_node_pubkey = os.getenv("THIS_NODE_PUBKEY")
#this_node_wif = os.getenv("THIS_NODE_WIF")

def get_utxos_api(address):
    komodo_node_ip = os.getenv("IJUICE_KOMODO_NODE_IPV4_ADDR")

    rpc_connect = rpc_connection = Proxy("http://" + rpc_user + ":" + rpc_password + "@" + komodo_node_ip + ":" + port)

    url = "https://blockchain-explorer.thenewfork.staging.do.unchain.io/insight-api-komodo/addrs/"+ address +"/utxo"

    try:
        res = requests.get(url)
    except Exception as e:
        print(e)

    return res.text

array_of_utxos = []
array_of_utxos_final = []
amount_final = -10000000000


def get_utxos(utxos, amount, greedy):
    global array_of_utxos
    global array_of_utxos_final
    global amount_final

    if len(array_of_utxos) >= len(array_of_utxos_final) and len(array_of_utxos_final) > 0:
        return False

    if amount <= 0 and amount > amount_final:
        return True

    flag = False
    cheap_copy = array_of_utxos
    for utxo in utxos:
        for uxto_in_array in array_of_utxos:
            if uxto_in_array['txid'] == utxo['txid']:
                flag = True

        if flag == False:
            array_of_utxos = array_of_utxos + [utxo]
            if get_utxos(utxos, amount - utxo['amount'], greedy) == True:
                array_of_utxos_final = array_of_utxos
                amount_final = amount
                if greedy == True:
                    return True
        flag = False
    array_of_utxos = cheap_copy
    return False


string = get_utxos_api(address)
to_python = ""

try:
    to_python = json.loads(string)
except Exception as e:
    print(e)
    exit()

final = []

for utxo in to_python:
    if utxo['confirmations'] > 10:
        final = final + [utxo]

get_utxos(final, amount, greedy)

print(array_of_utxos_final)

#TESTING

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True

def test_api():
    test = get_utxos_api("RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW")
    assert is_json(test) == True

def test_get_utxos():
    testcase = [{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"6d2dbbf64d839bedece788632d6233337494d1d51247823058832a16c1cf1d92","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.01833945,"satoshis":1833945,"confirmations":0,"ts":1602181139},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"ba474f6ddff5883a13bd456570769cd8de54b448cd5baa872fd99d253dc3df79","vout":0,"scriptPubKey":"2102f2cdd772ab57eae35996c0d39ad34fe06304c4d3981ffe71a596634fa26f8744ac","amount":0.04444815,"satoshis":4444815,"height":104219,"confirmations":1},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"95f7f0a9ccd4256be902d773f884c6b13bff465feaa87b56a61a8773a3cd990b","vout":0,"scriptPubKey":"2102f2cdd772ab57eae35996c0d39ad34fe06304c4d3981ffe71a596634fa26f8744ac","amount":0.01014884,"satoshis":1014884,"height":104104,"confirmations":116},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"1e562a43ce53a17c1b0cd2f3a7561d943a849d870e0efd4c9f37c8ce750c015b","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":103904,"confirmations":316},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"cad9777cfd1ea164236800506b24ff633702914a87000be019d82523911fdce2","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":103902,"confirmations":318},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"41451a102cfd2780377c33a67d1ed96b3f70fbb616664a7f431115f83f1beb22","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":103901,"confirmations":319},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"7e7390d8176edb9fef91cbd1843c656da7543169baf361971d6bc7eefa498066","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99497,"confirmations":4723},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"19c73bac8031b52b2c3f9f93c3e40f03dc4747a093703907c0e0a8ef09192fac","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99496,"confirmations":4724},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"db60669396d0bb0aa7b81b9325edfe708c879ff0253c9919af1b892efdefac10","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99492,"confirmations":4728},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"2a39930043b87bc3976c6fc39445708103c6c00f88cb8acd18ad24bbaa83a72e","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99486,"confirmations":4734},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"62b29ebbed4e423a72247c116dafe39643c0f6318c4cc435973f1650407a4c06","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99481,"confirmations":4739},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"32a9965986c5922bf9b0de8fbfbac6a9eea70ba8f9a094b084123e97c918631e","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99477,"confirmations":4743},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"8e8ae844ac5a192602031ef0ae1b69aa60900ad73feb3604a0cd2042978c3f80","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99476,"confirmations":4744},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"9ccc0668d3bd89be852ad45cf51c415c212cf861ca0e7b6622b6d71d139ebfd0","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99476,"confirmations":4744},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"ee2495ab86e04fb7c9a0d051df12621516d86845e72b05bc901e222366b4c8fb","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99476,"confirmations":4744},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"4ce3087fc3e3b3f8d586b2d77b4584d819130d141461a3a23c83d22d35128ecf","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99475,"confirmations":4745},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"6edbe4a746e1f84851eda54fc05e7f967367318866a65d73060847ac60497bc9","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99474,"confirmations":4746},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"c16f7f55dee528b925489e9ec4979a4a6215c9cf11b7a1db02ff822189956f0a","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99473,"confirmations":4747},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"11bb33a95f3f1c713e801754031ff4b0fa7fe17242b2c74d223dee08c2568ae4","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99473,"confirmations":4747},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"2dc4e28f322a641169afbce755db55d8cc4547771a29a4e75f0af850016f67aa","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99342,"confirmations":4878},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"98604c684398bc399a45168d30f7ff4515da1145d53f7584d4388b3d69053b7f","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99341,"confirmations":4879},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"ba506982f94df57e2e80418e8a7393568b2892f1c01184d1ea46419c21413ee4","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99339,"confirmations":4881},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"7956be14d1e0681bec8cc8528d7fede271254cbc6ca7d34ae413748ce972182b","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99339,"confirmations":4881},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"49444806b8f9d32efd9536578dfd106e56fa5594bda37f772b7c4b5e582f971f","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99324,"confirmations":4896},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"0fbb4254adce7fc38a3391cd695061d05e43bdf2c27bdad0a4ba0ee076a966e1","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99320,"confirmations":4900},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"6f0f621ae5b071a1a3ab653ee296c426dfaf099586095606a6dcc11c89893c3a","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99316,"confirmations":4904},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"9b25d4de15729fd11cc8d9b40da4eaa3093186a7c7caf4b991bb7101fb9dd56f","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99312,"confirmations":4908},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"c75171dd9737181cde71adf9196f8fddb3710abcd038242a6f99984aba9d1d77","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99307,"confirmations":4913},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"94e047f42834c829fda5f0dc2cdda88d37c67968c180f8e0bb8a61ef812f2934","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99304,"confirmations":4916},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"c56cbc57e260b418519cf43c209b90079a47c0fd50aca8671e35597cc5f6c9d7","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99301,"confirmations":4919},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"1b368d690f8f3db7239248d5140b710ea75f6a0b788c61bb434759087df9e884","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99299,"confirmations":4921},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"923ffde12287052acbeda7cd825fcb390db099dcd4a6ef42a503ccbed32aca5d","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":99297,"confirmations":4923},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"8a0f23e3f8230458e299f96996fbce97859b07d6b85bfd83d2610aa8ca159c7a","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":94589,"confirmations":9631},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"5c73c06f2999b00453f5eacbcb60845ba2554a0a540860a051d55ee18a490935","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":0.05,"satoshis":5000000,"height":94442,"confirmations":9778},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"fed38c710ceaf82d0ef54316df7447171d4b1ec6d499a4b231846b8c9dd33a31","vout":0,"scriptPubKey":"2102f2cdd772ab57eae35996c0d39ad34fe06304c4d3981ffe71a596634fa26f8744ac","amount":0.28400257,"satoshis":28400257,"height":94145,"confirmations":10075},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"bdde13adb442e0a0b2c5b7220957a2e4d3b9fbbbc47ad3523d35cd996495b608","vout":0,"scriptPubKey":"2102f2cdd772ab57eae35996c0d39ad34fe06304c4d3981ffe71a596634fa26f8744ac","amount":0.0743478,"satoshis":7434780,"height":94144,"confirmations":10076},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"c064d930a22eaa5a73d0b04201abb304d6d2dffab0f11a3f7652a16724c3d484","vout":2,"scriptPubKey":"2102f2cdd772ab57eae35996c0d39ad34fe06304c4d3981ffe71a596634fa26f8744ac","amount":0.3054992,"satoshis":30549920,"height":94137,"confirmations":10083},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"7dcb33a923f7c25fc8738eb5fc7a230455b55b7285281fc6b41dfa42db900e88","vout":0,"scriptPubKey":"2102f2cdd772ab57eae35996c0d39ad34fe06304c4d3981ffe71a596634fa26f8744ac","amount":0.95629085,"satoshis":95629085,"height":94137,"confirmations":10083},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"a25b4fb86c86c22fa127838496ae35e75c92ae30d1d80e85ed7fd6135371ddb5","vout":0,"scriptPubKey":"2102f2cdd772ab57eae35996c0d39ad34fe06304c4d3981ffe71a596634fa26f8744ac","amount":0.8299,"satoshis":82990000,"height":94137,"confirmations":10083},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"f76a8d2ebdab28f39ac76365c36aaaaa4c7cce36ac12f38f32b27548f9ddc6e4","vout":0,"scriptPubKey":"2102f2cdd772ab57eae35996c0d39ad34fe06304c4d3981ffe71a596634fa26f8744ac","amount":0.69274518,"satoshis":69274518,"height":94137,"confirmations":10083},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"fa58a094f7de0c816f1a40ab3322afded4ccdf89cbe3b6b2702ac1011062a0d2","vout":0,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":3.979,"satoshis":397900000,"height":91157,"confirmations":13063},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"b27d126a997f960cdc9e4b82aac74c2c26437005e7025c1bdd188d2ea9b561d1","vout":1,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":1.11,"satoshis":111000000,"height":90011,"confirmations":14209},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"8005ab6aaa009c48a1c43d01b21b09f8a2e6c853a3a197d46f0c0fa1344e14e1","vout":1,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":1.11,"satoshis":111000000,"height":90011,"confirmations":14209},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"15a307cd75a630718b63a28a7465e01309dc1d5c0542791fc384b35e86f30b2c","vout":1,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":1.11,"satoshis":111000000,"height":90010,"confirmations":14210},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"5a090d5dd686bed104ae13472262e7cd9d96608f74631351f1252e0d40be70d4","vout":1,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":1.11,"satoshis":111000000,"height":90010,"confirmations":14210},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"3cdf23999fa1354eded15493bda356d5829cc60a1c0d708a07f2cd8406f47328","vout":1,"scriptPubKey":"76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac","amount":1.11,"satoshis":111000000,"height":90010,"confirmations":14210},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"be25a04b0dc9196cf9b65dff78ec8c57e58114aae398699046680e25d03fa015","vout":0,"scriptPubKey":"2102f2cdd772ab57eae35996c0d39ad34fe06304c4d3981ffe71a596634fa26f8744ac","amount":1.10944966,"satoshis":110944966,"height":89762,"confirmations":14458},{"address":"RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW","txid":"6e975f08b1ee2a3aa02c2b96ebef588b405576acf24f4c81aff1a929085f168b","vout":0,"scriptPubKey":"2102f2cdd772ab57eae35996c0d39ad34fe06304c4d3981ffe71a596634fa26f8744ac","amount":0.97999673,"satoshis":97999673,"height":89762,"confirmations":14458}]

    get_utxos(testcase, 0.01, True)

    assert  array_of_utxos_final == [{'address': 'RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW', 'txid': '6d2dbbf64d839bedece788632d6233337494d1d51247823058832a16c1cf1d92', 'vout': 0, 'scriptPubKey': '76a9147fd21d91b20b713c5a73fe77db4c262117b77d2888ac', 'amount': 0.01833945, 'satoshis': 1833945, 'confirmations': 0, 'ts': 1602181139}]
