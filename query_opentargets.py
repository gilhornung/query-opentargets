#! /usr/bin/env python

"""
Code to query the Open Targets REST API using a disease or a target.
"""

import argparse
import requests
import statistics
# import json

parser = argparse.ArgumentParser(description='Query the Open Targets REST API with disease or target')
xgroup = parser.add_mutually_exclusive_group(required=True)
xgroup.add_argument('-d','--disease', help='Disease ID, e.g. Orphanet_399', required=False)
xgroup.add_argument('-t','--target',  help='Target gene, e.g. ENSG00000197386', required=False)
args_dict = vars(parser.parse_args())

qtype = "disease" if args_dict["disease"] else "target"
qstring = args_dict["disease"] if args_dict["disease"] else args_dict["target"]

# Query the REST API
rest_url = "https://platform-api.opentargets.io/v3/platform/public/association/filter"
pars = {qtype: qstring}
response = requests.get(rest_url, params=pars)
content = response.json()
if response.status_code != requests.codes.ok:
    err_msg = "Query failed with code "+str(content["code"])+", "+content["message"]
    raise RuntimeError(err_msg)

if len(content["data"])==0:
    err_msg = "Query returned no items. Make sure you got the names right!"
    raise RuntimeError(err_msg)

# Print the scores for each target/disease
out_lines = [d["disease"]["id"]+"\t"+d["target"]["id"]+"\t"+str(d["association_score"]["overall"]) for d in content["data"]]
out_text = "disease"+"\t"+"target"+"\t"+"overall_score\n"+ \
    "\n".join(out_lines) + "\n" + \
    "-------------------------------------------"
print(out_text)

# Statistics on scores
scores = [d["association_score"]["overall"] for d in content["data"]]
mean_score = statistics.mean(scores)
sd_score = statistics.stdev(scores)
max_score = max(scores)
min_score = min(scores)
stats_text = "Score stats: max="+str(max_score)+", min="+str(min_score)+", mean="+str(mean_score)+", stdev="+str(sd_score)+"\n"
print(stats_text)
