from lib import transaction, bitcoin, util
from lib.util import bfh, bh2u
from lib.transaction import Transaction
import sys

kmd_unsigned_tx_serialized = sys.argv[1] #'0400008085202f890180b25dac8577eca59c862a7f6f24568f868e68b57826fc8f82096cf1b3d095ad0300000000ffffffff0240420f00000000001976a914b0fda403362089103366ae9149c9971fe1d9f01388ac10d4e594000000001976a914a65344e2aebbf9bd515dab38cf7b854ac0a487d188ac000000007cc500000000000000000000000000'

# SEND: ref herrath
# {         "wif": "UqunREfKWf9nogsZmf4zxK1pz4zKynWs39K81bXkfvraadEdDx2P",  "address": "RQSdzzo8zMhWfEcKd6wQoN7wZt7jo3U8HQ"}
wif= sys.argv[2] #'UqunREfKWf9nogsZmf4zxK1pz4zKynWs39K81bXkfvraadEdDx2P'

txin_type, privkey, compressed = bitcoin.deserialize_privkey(wif)
pubkey = bitcoin.public_key_from_private_key(privkey, compressed)

jsontx = transaction.deserialize(kmd_unsigned_tx_serialized)
inputs = jsontx.get('inputs')
outputs = jsontx.get('outputs')
locktime = jsontx.get('lockTime', 0)
outputs_formatted = []

for txout in outputs:
  outputs_formatted.append([txout['type'], txout['address'], txout['value']])

for txin in inputs:
  txin['type'] = txin_type
  txin['x_pubkeys'] = [pubkey]
  txin['pubkeys'] = [pubkey]
  txin['signatures'] = [None]
  txin['num_sig'] = 1
  txin['address'] = bitcoin.address_from_private_key(wif)
  txin['value'] = 2500000000 # required for preimage calc

tx = Transaction.from_io(inputs, outputs_formatted, locktime=locktime)
tx.sign({pubkey:(privkey, compressed)})

print(tx.serialize())
