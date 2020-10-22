# blocknotify-python

## Commands

### get_utxos_test.py
@desc: consilidates a number of utxo's every given seconds, and makes it into 1 utxo.
The time between tries should be at least 30 minutes aka 1800 seconds.

@params: address, privatekey, number of uxtos, time between tries.

@return: transaction id, and also the decoded transactions and other debug information.

### select_utxos.py
@desc: this command selects the utxo's to make a transaction of a certain amount. It can either be very efficient, or just efficient enough, depending on the greedy veriable. This will change the algoritm for selection to a greedy one, instead of a normal one.

@params: address, amount, greedy

@return: a list of utxos


## Test

### test.py
#### test_workaround
This will sucseed if the workaround node's wallet is loaded up. otherwise it will fail.

#### test_locate_workaround
This will sucseed if the workaround node's wallet is loaded up. otherwise it will fail.

#### test_isMy
This will sucseed if the normal node's wallet is loaded up. otherwise it will fail.

#### test_checksync
this will sucseed if the normal node's blockchain is synced up. otherwise it will fail.

#### test_explorer_get_utxos
this will sucseed if the resons is an array, thus indicating that a correct answere was recieved from the call. otherwise it will fail.

#### test_gen_Wallet
this will sucseed if a correct address is created with a test input. otherwise it will fail.

#### test_getCertsNoAddy
this will sucseed if the resons is an array, thus indicating that a correct answere was recieved from the call. otherwise it will fail.

#### test_getBatchesNullIntegrity
this will sucseed if the resons is an array, thus indicating that a correct answere was recieved from the call. otherwise it will fail.

#### test_import_jcf_batch_integrity_pre_process
this will sucseed if the resons is an json, thus indicating that a correct answere was recieved from the call. otherwise it will fail.
