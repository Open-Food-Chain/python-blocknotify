from lib.juicychain_env import IMPORT_API_BASE_URL
import string
import random
import time
import requests
import json
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

for x in range(0,1):
	print(IMPORT_API_BASE_URL)
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

	params={ "anfp": RANDOM_VAL_ANFP, "dfp": RANDOM_VAL_DFP, "bnfp": RANDOM_VAL_BNFP, "pds":PDS , "pde":PDE, "jds":JDS, "jde":JDE , "bbd":BBD , "pc": RANDOM_VAL_PC, "pl": RANDOM_VAL_PL, "rmn":RANDOM_VAL_RMN , "pon":RANDOM_VAL_PON , "pop": RANDOM_VAL_POP }
	print(params)
	url = IMPORT_API_BASE_URL + "raw/refresco/"
	res = requests.post(url, data=params)
	print(res.text)
