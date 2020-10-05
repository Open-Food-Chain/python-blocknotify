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
