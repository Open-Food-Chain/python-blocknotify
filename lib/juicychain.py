# from lib.juicychain_env import MULTI_1X
from lib.juicychain_env import MULTI_2X
# from lib.juicychain_env import MULTI_3X
# from lib.juicychain_env import MULTI_4X
# from lib.juicychain_env import MULTI_5X
from lib.juicychain_env import KOMODO_NODE
from lib.juicychain_env import RPC_USER
from lib.juicychain_env import RPC_PASSWORD
from lib.juicychain_env import RPC_PORT
from lib.juicychain_env import EXPLORER_URL
from lib.juicychain_env import IMPORT_API_BASE_URL
from lib.juicychain_env import THIS_NODE_ADDRESS
from lib.juicychain_env import THIS_NODE_WIF
from lib.juicychain_env import BLOCKNOTIFY_CHAINSYNC_LIMIT
from lib.juicychain_env import HOUSEKEEPING_ADDRESS
from lib.juicychain_env import DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH
# from lib.juicychain_env import DEV_IMPORT_API_RAW_REFRESCO_INTEGRITY_PATH
from lib.juicychain_env import DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
from lib.juicychain_env import JUICYCHAIN_API_BASE_URL
from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION_CERTIFICATE_NORADDRESS
# from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION_CERTIFICATE
# from lib.juicychain_env import JUICYCHAIN_API_ORGANIZATION_BATCH
from lib.juicychain_env import FUNDING_AMOUNT_CERTIFICATE
from dotenv import load_dotenv
from lib import transaction, bitcoin
from lib import rpclib
from lib.transaction import Transaction
from slickrpc import Proxy
import subprocess
import requests
import json
load_dotenv(verbose=True)
SCRIPT_VERSION = 0.00012111

RPC = ""


def connect_node():
    global RPC
    print("Connecting to: " + KOMODO_NODE + ":" + RPC_PORT)
    RPC = Proxy("http://" + RPC_USER + ":" + RPC_PASSWORD + "@" + KOMODO_NODE + ":" + RPC_PORT)
    return True


def sendtoaddress_wrapper(to_address, amount):
    send_amount = round(amount, 10)
    txid = rpclib.sendtoaddress(RPC, to_address, send_amount)
    return txid


def sendmany_wrapper(from_address, recipients_json):
    txid = rpclib.sendmany(RPC, from_address, recipients_json)
    return txid


def signmessage_wrapper(data):
    signed_data = rpclib.signmessage(RPC, THIS_NODE_ADDRESS, data)
    return signed_data


def housekeeping_tx():
    return sendtoaddress_wrapper(HOUSEKEEPING_ADDRESS, SCRIPT_VERSION)


def sendmanyWrapper(from_address, recipients_json):
    print("Deprecated: use sendmany_wrapper(...)")
    txid = rpclib.sendmany(RPC, from_address, recipients_json)
    return txid


def sendtoaddressWrapper(address, amount, amount_multiplier):
    print("Deprecated: use sendtoaddress_wrapper")
    send_amount = round(amount * amount_multiplier, 10)  # rounding 10??
    txid = rpclib.sendtoaddress(RPC, address, send_amount)
    return txid


def check_sync():
    general_info = rpclib.getinfo(RPC)
    sync = general_info['longestchain'] - general_info['blocks']

    print("Chain info.  Longest chain, blocks, sync diff")
    print(general_info['longestchain'])

    print(general_info['blocks'])

    print(sync)

    if sync >= BLOCKNOTIFY_CHAINSYNC_LIMIT:
        print('the chain is not synced, try again later')
        exit()

    print("Chain is synced")
    return sync


def check_node_wallet():
    # check wallet management
    try:
        is_mine = rpclib.validateaddress(RPC, THIS_NODE_ADDRESS)['ismine']
        if is_mine is False:
            rpclib.importprivkey(RPC, THIS_NODE_WIF)
        is_mine = rpclib.validateaddress(RPC, THIS_NODE_ADDRESS)['ismine']
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


def organization_certificate_noraddress(url, org_id, THIS_NODE_ADDRESS):
    try:
        res = requests.get(url)
    except Exception as e:
        raise Exception(e)

    certs_no_addy = res.text

    certs_no_addy = json.loads(certs_no_addy)


# the issuer, issue date, expiry date, identifier (not the db id, the certificate serial number / identfier)

    for cert in certs_no_addy:
        raw_json = {
            "issuer": cert['issuer'],
            "issue_date": cert['date_issue'],
            "expiry_date": cert['date_expiry'],
            "identfier": cert['identifier']
        }
        raw_json = json.dumps(raw_json)
        addy = gen_wallet(THIS_NODE_ADDRESS, raw_json)
        # id = str(cert['id'])
        # url = IMPORT_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + id + "/"

        try:
            data = {"raddress": addy['address'], "pubkey": addy['pubkey']}
            res = requests.patch(url, data=data)
        except Exception as e:
            raise Exception(e)


def explorer_get_utxos(explorer_url, querywallet):
    print("Get UTXO for wallet " + querywallet)
    # INSIGHT_API_KOMODO_ADDRESS_UTXO = "insight-api-komodo/addrs/{querywallet}/utxo"
    INSIGHT_API_KOMODO_ADDRESS_UTXO = "insight-api-komodo/addrs/" + querywallet + "/utxo"
    try:
        res = requests.get(explorer_url + INSIGHT_API_KOMODO_ADDRESS_UTXO)
    except Exception as e:
        raise Exception(e)
    # vouts = json.loads(res.text)
    # for vout in vouts:
        # print(vout['txid'] + " " + str(vout['vout']) + " " + str(vout['amount']) + " " + str(vout['satoshis']))
    return res.text


def createrawtx_wrapper(txids, vouts, to_address, amount):
    return rpclib.createrawtransaction(RPC, txids, vouts, to_address, amount)


def createrawtxwithchange(txids, vouts, to_address, amount, change_address, change_amount):
    return rpclib.createrawtransactionwithchange(RPC, txids, vouts, to_address, amount, change_address, change_amount)


def createrawtx(txids, vouts, to_address, amount):
    print("Deprecated: use createrawtx_wrapper")
    return rpclib.createrawtransaction(RPC, txids, vouts, to_address, amount)


def createrawtx2(utxos_json, num_utxo, to_address):
    print("Deprecated: use createrawtx4 or createrawtx5")
    utxos = json.loads(utxos_json)
    utxos.reverse()
    count = 0

    txids = []
    vouts = []
    amounts = []
    amount = 0

    for objects in utxos:
        print(objects)
        if (count < num_utxo):
            count = count + 1
            easy_typeing2 = [objects['vout']]
            easy_typeing = [objects['txid']]
            txids.extend(easy_typeing)
            vouts.extend(easy_typeing2)
            amount = amount + objects['amount']
            amounts.extend([objects['satoshis']])

    amount = round(amount, 10)

    return createrawtx(txids, vouts, to_address, amount)


def createrawtx3(utxos_json, num_utxo, to_address):
    print("Deprecated: use createrawtx4 or createrawtx5")
    rawtx_info = []  # return this with rawtx & amounts
    utxos = json.loads(utxos_json)
    utxos.reverse()
    count = 0

    txids = []
    vouts = []
    amounts = []
    amount = 0

    for objects in utxos:
        if (count < num_utxo):
            count = count + 1
            easy_typeing2 = [objects['vout']]
            easy_typeing = [objects['txid']]
            txids.extend(easy_typeing)
            vouts.extend(easy_typeing2)
            amount = amount + objects['amount']
            amounts.extend([objects['satoshis']])

    amount = round(amount, 10)

    rawtx = createrawtx(txids, vouts, to_address, amount)
    rawtx_info.append({'rawtx': rawtx})
    rawtx_info.append({'amounts': amounts})
    return rawtx_info


def createrawtx5(utxos_json, num_utxo, to_address, fee, change_address):
    rawtx_info = []  # return this with rawtx & amounts
    utxos = json.loads(utxos_json)
    utxos.reverse()
    count = 0

    txids = []
    vouts = []
    amounts = []
    amount = 0

    for objects in utxos:
        if (objects['amount'] > 0.00005) and count < num_utxo:
            count = count + 1
            easy_typeing2 = [objects['vout']]
            easy_typeing = [objects['txid']]
            txids.extend(easy_typeing)
            vouts.extend(easy_typeing2)
            amount = amount + objects['amount']
            amounts.extend([objects['satoshis']])

    # TODO be smart with change.
    change_amount = 0.555
    amount = round(amount - change_amount, 10)
    print("AMOUNT")
    print(amount)

    rawtx = createrawtxwithchange(txids, vouts, to_address, round(amount - fee, 10), change_address, change_amount)
    rawtx_info.append({'rawtx': rawtx})
    rawtx_info.append({'amounts': amounts})
    return rawtx_info


def createrawtx4(utxos_json, num_utxo, to_address, fee):
    rawtx_info = []  # return this with rawtx & amounts
    utxos = json.loads(utxos_json)
    utxos.reverse()
    count = 0

    txids = []
    vouts = []
    amounts = []
    amount = 0

    for objects in utxos:
        if (objects['amount'] > 0.00005) and count < num_utxo:
            count = count + 1
            easy_typeing2 = [objects['vout']]
            easy_typeing = [objects['txid']]
            txids.extend(easy_typeing)
            vouts.extend(easy_typeing2)
            amount = amount + objects['amount']
            amounts.extend([objects['satoshis']])

    amount = round(amount, 10)
    print("AMOUNT")
    print(amount)

    rawtx = createrawtx(txids, vouts, to_address, round(amount - fee, 10))
    rawtx_info.append({'rawtx': rawtx})
    rawtx_info.append({'amounts': amounts})
    return rawtx_info


def decoderawtx_wrapper(tx):
    return rpclib.decoderawtransaction(RPC, tx)


def decoderawtx(tx):
    print("Deprecated: use decoderawtx_wrapper(tx)")
    return rpclib.decoderawtransaction(RPC, tx)


def signtx(kmd_unsigned_tx_serialized, amounts, wif):
    txin_type, privkey, compressed = bitcoin.deserialize_privkey(wif)
    pubkey = bitcoin.public_key_from_private_key(privkey, compressed)

    jsontx = transaction.deserialize(kmd_unsigned_tx_serialized)
    inputs = jsontx.get('inputs')
    outputs = jsontx.get('outputs')
    locktime = jsontx.get('lockTime', 0)
    outputs_formatted = []
    print("\n###### IN SIGNTX FUNCTION #####\n")
    print(jsontx)
    print(inputs)
    print(outputs)
    print(locktime)

    for txout in outputs:
        outputs_formatted.append([txout['type'], txout['address'], (txout['value'])])
        print("Value of out before miner fee: " + str(txout['value']))
        print("Value of out: " + str(txout['value']))

    print("\nOutputs formatted:\n")
    print(outputs_formatted)

    for txin in inputs:
        txin['type'] = txin_type
        txin['x_pubkeys'] = [pubkey]
        txin['pubkeys'] = [pubkey]
        txin['signatures'] = [None]
        txin['num_sig'] = 1
        txin['address'] = bitcoin.address_from_private_key(wif)
        txin['value'] = amounts[inputs.index(txin)]  # required for preimage calc

    tx = Transaction.from_io(inputs, outputs_formatted, locktime=locktime)
    print("### TX before signing###")
    print(tx)
    print("### END TX ###")
    tx.sign({pubkey: (privkey, compressed)})

    print("\nSigned tx:\n")
    print(tx.serialize())
    print("Return from signtx")
    return tx.serialize()


def broadcast_via_explorer(explorer_url, signedtx):
    INSIGHT_API_BROADCAST_TX = "insight-api-komodo/tx/send"
    params = {'rawtx': signedtx}
    url = explorer_url + INSIGHT_API_BROADCAST_TX
    print("Broadcast via " + url)

    try:
        broadcast_res = requests.post(url, data=params)
    except Exception as e:
        print(e)

    print(broadcast_res.text)

    return broadcast_res.text


def gen_wallet(wallet, data, label='NoLabelOK'):
    print("Creating a %s address signing with %s and data %s" % (label, wallet, data))
    signed_data = rpclib.signmessage(RPC, wallet, data)
    print("Signed data is %s" % (signed_data))
    new_wallet_json = subprocess.getoutput("php genwallet.php " + signed_data)
    print("Created wallet %s" % (new_wallet_json))

    new_wallet = json.loads(new_wallet_json)

    return new_wallet


def offlineWalletGenerator_fromObjectData_certificate(signing_wallet, objectData):
    obj = {
        "issuer": objectData['issuer'],
        "issue_date": objectData['date_issue'],
        "expiry_date": objectData['date_expiry'],
        "identfier": objectData['identifier']
    }
    raw_json = json.dumps(obj)
    print("libjuicychain->offlineWalletGenerator object data as json: " + raw_json)

    log_label = objectData['identifier']
    offline_wallet = gen_wallet(signing_wallet, raw_json, log_label)

    return offline_wallet


def utxo_bundle_amount(utxos_obj):
    count = 0
    list_of_ids = []
    list_of_vouts = []
    amount = 0

    for objects in utxos_obj:
        if (objects['amount']):
            count = count + 1
            easy_typeing2 = [objects['vout']]
            easy_typeing = [objects['txid']]
            list_of_ids.extend(easy_typeing)
            list_of_vouts.extend(easy_typeing2)
            amount = amount + objects['amount']

    amount = round(amount, 10)
    return amount


def get_batches_no_timestamp():
    print("10009 start import api - raw/refresco")
    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_REQUIRE_INTEGRITY_PATH
    print("Trying: " + url)

    try:
        res = requests.get(url)
    except Exception as e:
        print("###### REQUIRE INTEGRITY URL ERROR: ", e)
        print("20201020 - url not sending nice response " + url)

    print(res.text)
    raw_json = res.text
    batches_no_timestamp = ""

    try:
        batches_no_timestamp = json.loads(raw_json)
    except Exception as e:
        print("10009 failed to parse to json because of", e)

    print("New batch requires timestamping: " + str(len(batches_no_timestamp)))
    return batches_no_timestamp


def get_certificates_no_timestamp():
    url = JUICYCHAIN_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE_NORADDRESS
    try:
        res = requests.get(url)
    except Exception as e:
        raise Exception(e)

    certs_no_addy = json.loads(res.text)
    return certs_no_addy


def fund_certificate(certificate_address):
    txid = sendtoaddress_wrapper(certificate_address, FUNDING_AMOUNT_CERTIFICATE)
    return txid


def postWrapper(url, data):
    res = requests.post(url, data=data)
    if(res.status_code == 200 | res.status_code == 201):
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


def patchWrapper(url, data):
    res = requests.patch(url, data=data)

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


# TEST FUNCTIONS

def test_postWrapperr():
    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
    data = {'sender_raddress': THIS_NODE_ADDRESS,
            'tsintegrity': "1", 'sender_name': 'ORG WALLET', 'txid': "testtest"}

    test = postWrapper(url, data)
    assert is_json(test) == True


def test_putWrapperr():
    url = IMPORT_API_BASE_URL + DEV_IMPORT_API_RAW_REFRESCO_TSTX_PATH
    data = {'sender_raddress': THIS_NODE_ADDRESS,
            'tsintegrity': "1", 'sender_name': 'ORG WALLET', 'txid': "testtest"}

    test = putWrapper(url, data)
    assert is_json(test) == True

# TEST FUNCTIONS

# @pytest.mark.skip


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


def test_check_node_wallet():
    test = check_node_wallet()
    assert test == True


def test_check_sync():
    test = check_sync()
    assert type(10) == type(test)


# @pytest.mark.skip
def test_explorer_get_utxos():
    try:
        test = explorer_get_utxos(EXPLORER_URL, "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW")
        assert is_json(test) == True
    except Exception as e:
        assert e == True


def test_gen_wallet():
    test = gen_wallet(THIS_NODE_ADDRESS, "testtest")
    assert type("test") == type(test['address'])
    assert test['address'][0] == 'R'


def test_getCertsNoAddy():
    test = getCertsNoAddy()
    assert type(test) == type(['this', 'is', 'an', 'test', 'array'])


def test_get_batches_no_timestamp():
    test = get_batches_no_timestamp()
    assert type(test) == type(['this', 'is', 'an', 'test', 'array'])


def test_sendtoaddressWrapper():
    test = sendtoaddressWrapper(THIS_NODE_ADDRESS, 1, MULTI_2X)
    assert not (" " in test)


def test_sendtomanyWrapper():
    json_object = {THIS_NODE_ADDRESS: SCRIPT_VERSION}
    test = sendmanyWrapper(THIS_NODE_ADDRESS, json_object)
    print(test)
    assert not (" " in test)
