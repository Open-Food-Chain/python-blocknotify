from dotenv import load_dotenv
from lib import transaction, bitcoin
from lib import rpclib
from lib.transaction import Transaction
from slickrpc import Proxy
import subprocess
import requests
import json
load_dotenv(verbose=True)

RPC = ""


def connect_node(rpc_user, rpc_password, komodo_node_ip, port):
    global RPC
    print("Connecting to: " + komodo_node_ip + ":" + port)
    RPC = Proxy("http://" + rpc_user + ":" + rpc_password + "@" + komodo_node_ip + ":" + port)
    return


def gen_wallet(wallet, data):
    print("10007 - Generate an address using %s with data %s" % (wallet, data))
    signed_data = rpclib.signmessage(RPC, wallet, data)
    print("10007 - Signed data is %s" % (signed_data))
    item_address = subprocess.getoutput("php genbothaddresswif.php " + signed_data)
    print("10007 - Created address %s" % (item_address))
    # item_address = json.loads(item_address)
    return item_address


def organization_certificate_noraddress(url, org_id, this_node_address):
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
        addy = gen_wallet(this_node_address, raw_json)
        # id = str(cert['id'])
        # url = IMPORT_API_BASE_URL + JUICYCHAIN_API_ORGANIZATION_CERTIFICATE + id + "/"

        try:
            data = {"raddress": addy['address'], "pubkey": addy['pubkey']}
            res = requests.patch(url, data=data)
        except Exception as e:
            raise Exception(e)


# TODO f-string
def explorer_get_utxos(explorer_url, querywallet):
    print("Get UTXO for wallet " + querywallet)
    # INSIGHT_API_KOMODO_ADDRESS_UTXO = "insight-api-komodo/addrs/{querywallet}/utxo"
    INSIGHT_API_KOMODO_ADDRESS_UTXO = "insight-api-komodo/addrs/" + querywallet + "/utxo"
    try:
        res = requests.get(explorer_url + INSIGHT_API_KOMODO_ADDRESS_UTXO)
    except Exception as e:
        raise Exception(e)
    vouts = json.loads(res.text)
    for vout in vouts:
        print(vout['txid'] + " " + str(vout['vout']) + " " + str(vout['amount']) + " " + str(vout['satoshis']))
    return res.text


def createrawtx(txids, vouts, to_address, amount):
    return rpclib.createrawtransaction(RPC, txids, vouts, to_address, amount)


def createrawtx2(utxos_json, num_utxo, to_address):
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


def decoderawtx(tx):
        return rpclib.decoderawtransaction(RPC, tx)


def signtx(kmd_unsigned_tx_serialized, amounts, wif):
    txin_type, privkey, compressed = bitcoin.deserialize_privkey(wif)
    pubkey = bitcoin.public_key_from_private_key(privkey, compressed)

    jsontx = transaction.deserialize(kmd_unsigned_tx_serialized)
    inputs = jsontx.get('inputs')
    outputs = jsontx.get('outputs')
    locktime = jsontx.get('lockTime', 0)
    outputs_formatted = []
    print("###### IN SIGNTX FUNCTION #####")
    print(jsontx)
    print(inputs)
    print(outputs)
    print(locktime)

    for txout in outputs:
        outputs_formatted.append([txout['type'], txout['address'], (txout['value'])])
        print("Value of out before miner fee: " + str(txout['value']))
        print("Value of out: " + str(txout['value']))

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
    print("### BEGIN TX ###")
    print(tx)
    print("### END TX ###")
    tx.sign({pubkey: (privkey, compressed)})

    print(tx.serialize())
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
