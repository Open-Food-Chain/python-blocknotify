from lib import rpclib
from slickrpc import Proxy
import binascii
import requests
import json
import sys


# global vars
rpc_user = "changeme"
rpc_password = "alsochangeme"
port =  24708

komodo_node_ip = "127.0.0.1"

this_node_address = "RLw3bxciVDqY31qSZh8L4EuM2uo3GJEVEW"
this_node_pubkey = "02f2cdd772ab57eae35996c0d39ad34fe06304c4d3981ffe71a596634fa26f8744"
this_node_wif = "UpUiqKNj43SBPe9SvYqpygZE3BS83f87GVQSV8zXt2Gr813YZ3Ah"

rpc_connect = rpc_connection = Proxy("http://%s:%s@127.0.0.1:%d"%(rpc_user, rpc_password, port));

blocknotify_chainsync_limit = 5
housekeeping_address = "RS7y4zjQtcNv7inZowb8M6bH3ytS1moj9A"


#check wallet management
is_mine = rpclib.validateaddress(rpc_connect, this_node_address)['ismine']

if is_mine == False:
    rpclib.importprivkey(rpc_connect, this_node_wif)

is_mine = rpclib.validateaddress(rpc_connect, this_node_address)['ismine']

#start housekeeping

# we send this amount to an address for housekeeping
# update by 0.0001 (manually, if can be done in CI/CD, nice-to-have not need-to-have) (MYLO)
# house keeping address is list.json last entry during dev
script_version = 0.00010005

general_info = rpclib.getinfo(rpc_connect);
sync = general_info['longestchain'] - general_info['blocks']

if sync >= blocknotify_chainsync_limit:
    print('the chain is not synced, try again later')
    exit()

print("the chain is synced")

# send a small amount (SCRIPT_VERSION) for HOUSEKEEPING_ADDRESS from each organization
# ############################
# info: for external documentation then remove from here
# one explorer url to check is
# IJUICE  http://seed.juicydev.coingateways.com:24711/address/RS7y4zjQtcNv7inZowb8M6bH3ytS1moj9A
# POS95   http://seed.juicydev.coingateways.com:54343/address/RS7y4zjQtcNv7inZowb8M6bH3ytS1moj9A
# ############################
# send SCRIPT_VERSION, increment by 0.00000001 for each update

res = rpclib.sendtoaddress(rpc_connect, housekeeping_address, script_version)

# print(res)

# ############################

# END OF HOUSEKEEPING

# ##############################################################################

# ##############################################################################

# START JCF IMPORT API INTEGRITY CHECKS

# JCF is the only part of script that refers to BATCH.
# development of new partners can use RAW_REFRESCO-like variables

###########################
# organization R-address = $1
# raw_json import data in base64 = $2
# batch record import database id(uuid) = $3
###########################

def improt_raw_refresco_batch_integrity_rpe_process():
    ### TODO:
    return


def get_address():
    ### TODO:
    return

def sign_message():
    return
