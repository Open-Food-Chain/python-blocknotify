#!/bin/bash
API_HOST="http://172.29.0.4:8777/"

for i in {1..2}
do
	RANDOM_VAL_ANFP=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)
	RANDOM_VAL_DFP=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)
	RANDOM_VAL_BNFP=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)
	RANDOM_VAL_PC=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 3 | head -n 1)
	RANDOM_VAL_PL=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)
	RANDOM_VAL_RMN=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)
	RANDOM_VAL_PON=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 6 | head -n 1)
	RANDOM_VAL_POP=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 3 | head -n 1)
	# RAW_JSON=$(echo '{ \"anfp\": \"'${RANDOM_VAL_1}'\",\"dfp\": \"'${RANDOM_VAL_2}'\"}' | base64 -w 0)
	RAW_JSON=$(echo '{ \"anfp\": \"'${RANDOM_VAL_ANFP}'\",\"dfp\": \"'${RANDOM_VAL_DFP}'\",\"bnfp\": \"'${RANDOM_VAL_BNFP}'\",\"pds\": \"2020-08-05\",\"pde\": \"2020-08-28\",\"jds\": 5,\"jde\": 28,\"bbd\": \"2020-10-28\",\"pc\": \"'${RANDOM_VAL_PC}'\",\"pl\": \"'${RANDOM_VAL_PL}'\",\"rmn\": \"'${RANDOM_VAL_RMN}'\",\"pon\": \"'${RANDOM_VAL_PON}'\",\"pop\": \"'${RANDOM_VAL_POP}'\", \"raw_json\": \"'${RAW_JSON}'\"}' | base64 -w 0)
	curl -X POST -H "Content-Type: application/json" ${API_HOST}batch/ -d "{ \"anfp\": \"${RANDOM_VAL_ANFP}\",\"dfp\": \"${RANDOM_VAL_DFP}\",\"bnfp\": \"${RANDOM_VAL_BNFP}\",\"pds\": \"2020-08-05\",\"pde\": \"2020-08-28\",\"jds\": 5,\"jde\": 28,\"bbd\": \"2020-10-28\",\"pc\": \"${RANDOM_VAL_PC}\",\"pl\": \"${RANDOM_VAL_PL}\",\"rmn\": \"${RANDOM_VAL_RMN}\",\"pon\": \"${RANDOM_VAL_PON}\",\"pop\": \"${RANDOM_VAL_POP}\", \"raw_json\": \"${RAW_JSON}\"}"
	sleep 5
	curl -X POST -H "Content-Type: application/json" ${API_HOST}batch/ -d "{ \"anfp\": \"${RANDOM_VAL_ANFP}\",\"dfp\": \"${RANDOM_VAL_DFP}\",\"bnfp\": \"${RANDOM_VAL_BNFP}\",\"pds\": \"2020-08-05\",\"pde\": \"2020-08-28\",\"jds\": 5,\"jde\": 28,\"bbd\": \"2020-10-28\",\"pc\": \"${RANDOM_VAL_PC}\",\"pl\": \"${RANDOM_VAL_PL}\",\"rmn\": \"${RANDOM_VAL_RMN}\",\"pon\": \"${RANDOM_VAL_PON}\",\"pop\": \"${RANDOM_VAL_POP}\", \"raw_json\": \"${RAW_JSON}\"}"
done
