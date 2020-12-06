from lib.openfood_env import IMPORT_API_BASE_URL
import string
import random
import time
import requests
import json
import sys
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(verbose=True)

print(IMPORT_API_BASE_URL)

def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    res = time.strftime(format, time.localtime(ptime))
    print(res)
    return res


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)


def make_random_string(length):
	str = ""
	for x in range(0,length):
		str = str + random.choice(string.ascii_letters)

	return str

def get_random_number(length):
	number = random.randint((length-1) ** 10, (length) ** 10)
	return number

def days(date):
	ret = ""
	for a in date:
		if a == '-':
			ret = ""
		else:
			ret = ret + a
	return int(ret)


def create_batches(amount):
	responselist = []
	for x in range(0,amount):
		params = create_random_batch()
		res = post_batches(params)
		res = json.loads(res)
		responselist = responselist + [ res ]

	return responselist


def post_batches(params):
	print(IMPORT_API_BASE_URL)
	url = IMPORT_API_BASE_URL + "raw/refresco/"
	res = requests.post(url, data=params)
	return res.text

def create_random_batch():
	RANDOM_VAL_ANFP=get_random_number(5)
	RANDOM_VAL_DFP="100EP PA Apfelsaft naturtrüb NF"
	RANDOM_VAL_BNFP=make_random_string(10)
	RANDOM_VAL_PC="DE"
	RANDOM_VAL_PL="Herrath"
	RANDOM_VAL_RMN=11200100520
	RANDOM_VAL_PON=get_random_number(8)
	RANDOM_VAL_POP=get_random_number(2)

	PDS=random_date("2020-1-1", "2020-11-15", random.random())
	PDE=random_date(PDS, "2020-11-15", random.random())
	BBD=PDE

	JDS=days(PDS)
	JDE=days(PDE)

	params = { "anfp": RANDOM_VAL_ANFP, "dfp": RANDOM_VAL_DFP, "bnfp": RANDOM_VAL_BNFP, "pds":PDS , "pde":PDE, "jds":JDS, "jde":JDE , "bbd":BBD , "pc": RANDOM_VAL_PC, "pl": RANDOM_VAL_PL, "rmn":RANDOM_VAL_RMN, "pon":RANDOM_VAL_PON, "pop":RANDOM_VAL_POP }
	print(params)
	return params

def main():
	amount = int(sys.argv[1])
	create_batches(amount)

if __name__ == '__main__':
    main()

def properties_test(tests):
	for test in tests:
		print(test)
		assert test['anfp']
		assert test['dfp']
		assert test['bnfp']
		assert test['pds']
		assert test['pde']
		assert test['jds']
		assert test['jde']
		assert test['bbd']
		assert test['pc']
		assert test['pl']
		assert test['rmn']
		assert test['pon']
		assert test['pop']

def ids_test(tests):
	for test in tests:
		assert test['id']

def test_create_random_batch():
	test_1 = create_random_batch()
	test_2 = create_random_batch()
	assert not test_1 == test_2

	tests = [test_1, test_2]
	properties_test(tests)

def test_post_random_batch():
	test_1 = create_random_batch()
	res = post_batches(test_1)
	res = json.loads(res)
	ids_test([res])


def test_create_batches():
	res = create_batches(10)
	properties_test(res)
	ids_test(res)
