from lib import openfood_env
from lib import openfood
import requests
from dotenv import load_dotenv
import json
#import pytest
import os
load_dotenv(verbose=True)


def test_explorer():
	explorer = openfood.EXPLORER_URL + "address/RL5CYAJaAM4pJB3bSVn5kDmMWg62onMqeY"
	res = requests.get(explorer)
	print(res.text)
	assert True == False
