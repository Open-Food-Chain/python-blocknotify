from lib.openfood_env import IMPORT_API_BASE_URL
from lib.openfood_env import openfood_API_BASE_URL
from lib.openfood_env import openfood_API_ORGANIZATION_CERTIFICATE_NORADDRESS
from lib.openfood_env import openfood_API_ORGANIZATION_CERTIFICATE
from lib.openfood_env import openfood_API_ORGANIZATION_CERTIFICATE_RULE
from lib.openfood_env import openfood_API_ORGANIZATION_BATCH
from lib.openfood_env import openfood_API_ORGANIZATION
from lib import openfood
import string
import random
import time
import requests
import json
import sys
import os
import binascii
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(verbose=True)

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


def generate_random_hex(size):
	return binascii.b2a_hex(os.urandom(size))

def random_date(start, end, prop):
	return str_time_prop(start, end, '%Y-%m-%d', prop)

def random_date_cert(start, end, prop):
        return str_time_prop(start, end, '%d-%m-%Y', prop)

def make_random_string(length):
	str = ""
	for x in range(0,length):
		str = str + random.choice(string.ascii_letters)
	
	return str

def get_random_number(length):
	number = random.randint(10 ** (length-1), 10 ** (length))
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

def create_random_org():
	
	RANDOM_ORG_NAME= get_random_number(1)
	RANDOM_RADDRESS= "R" + make_random_string(33)
	RANDOM_PUBKEY= str(b'02' + generate_random_hex(32))[2:-1]

	#RANDOM_START_DATE=random_date("2020-1-1", "2020-11-15", random.random())
	#RANDOM_EXPIRY_DATE=random_date(PDS, "2020-11-15", random.random())
	

	params = { "name": RANDOM_ORG_NAME, "pubkey": RANDOM_PUBKEY, "raddress": RANDOM_RADDRESS }

	return params

def create_random_locations(orgid):
	RANDOM_LOCATION_1_RADDRESS= "R" + make_random_string(33)
	RANDOM_PUBKEY = str(b'02'+ generate_random_hex(32))[2:-1]
	LOCATION_1_NAME = "LOCATION A" + str(get_random_number(3))
	ORG_ID = orgid

	params = { "name":LOCATION_1_NAME, "pubkey":RANDOM_PUBKEY, "raddress":RANDOM_LOCATION_1_RADDRESS, "organization":ORG_ID }
	
	return params

def create_random_certificates(ORG_ID):
	RANDOM_START_DAY = random_date("2020-1-1", "2020-11-15", random.random())
	RANDOM_END_DAY = random_date(RANDOM_START_DAY, "2020-11-15", random.random())
	RANDOM_CERT_NAME = "CERT " + make_random_string(3)
	RANDOM_ISSUER_NAME = "USER " + make_random_string(5)
	RANDOM_PUBKEY = str(b'02'+ generate_random_hex(32))[2:-1]
	RANDOM_RADDRESS= "R" + make_random_string(33)
	RANDOM_CERT_ID = str(get_random_number(9))
	
	params =  { "name":RANDOM_CERT_NAME, "pubkey":RANDOM_PUBKEY, "raddress":RANDOM_RADDRESS, "issuer":RANDOM_ISSUER_NAME, "identifier":RANDOM_CERT_ID, "date_issue": RANDOM_START_DAY, "date_expiry":RANDOM_END_DAY, "organization":ORG_ID}

	return params

def create_random_cert_rules(location_raddress, location, CERT_ID):
	CERT_CONDITION = location_raddress
	RULE_NAME = "match location " + location
	RANDOM_PUBKEY = str(b'02'+ generate_random_hex(32))[2:-1]
	RANDOM_RADDRESS= "R" + make_random_string(33)
	
	params =  { "name":RULE_NAME, "pubkey":RANDOM_PUBKEY, "raddress":RANDOM_RADDRESS, "condition":CERT_CONDITION, "certificate":CERT_ID }

	return params

def create_random_batches(ORG_ID):
	RANDOM_PUBKEY = str(b'02'+ generate_random_hex(32))[2:-1]
	RANDOM_RADDRESS = "R" + make_random_string(33)
	RANDOM_IDENTIFIER = "ID-" + str(get_random_number(7))
	RANDOM_JDS = str(get_random_number(2))
	RANDOM_JDE = RANDOM_JDS + str(get_random_number(1))
	RANDOM_START_DAY = random_date("2020-1-1", "2020-11-15", random.random())
	BBD_DATE = random_date(RANDOM_START_DAY, "2020-11-15", random.random())
	ORIGIN_COUNTRY = "DE"
	
	params = { "identifier":RANDOM_IDENTIFIER, "jds":RANDOM_JDS, "jde":RANDOM_JDE, "date_production_start":RANDOM_START_DAY, "date_best_before":BBD_DATE, "origin_country":ORIGIN_COUNTRY, "pubkey":RANDOM_PUBKEY, "raddress":RANDOM_RADDRESS, "organization":ORG_ID }

	return params

def post_to_openfood_api(url_add, params):
	url = openfood_API_BASE_URL + url_add
	print(url)

	res = openfood.postWrapper(url, params)
	return res

def main():
	print(openfood_API_BASE_URL)
	amount = int(sys.argv[1])
	for i in range(0, amount):
		params = create_random_org()
		print(params)
		res = post_to_openfood_api(openfood_API_ORGANIZATION, params)
		print(res)
		org_id = json.loads(res)['id']
		params = create_random_locations(org_id)
		print(params)
		res = post_to_openfood_api("location/", params)
		print(res)
		params = create_random_certificates(org_id)
		print(params)
		res = post_to_openfood_api(openfood_API_ORGANIZATION_CERTIFICATE, params)
		print(res)
		res = json.loads(res)
		cert_id = res['id']
		cert_raddie = res['raddress']
		cert_pub = res['pubkey']
		params = create_random_cert_rules(cert_pub, cert_raddie, cert_id)
		print(params)
		res = post_to_openfood_api(openfood_API_ORGANIZATION_CERTIFICATE_RULE, params)
		print(res)
		params = create_random_batches(org_id)
		print(params)
		res = post_to_openfood_api(openfood_API_ORGANIZATION_BATCH, params)
		print(res)


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
