#!/usr/bin/python
# -*- coding: utf-8 -*-

import pathlib
import time
import re
import json
import sys

if len(sys.argv) < 2:
    print("please input path")
    sys.exit(1)
path = sys.argv[1]

if path is None:
    print("please input path")
    sys.exit(1)
# check the path is exist
if not pathlib.Path(path).exists():
    print("path not exist")
    sys.exit(1)
with open(path, "r") as f:
    t = f.readlines()
log = []
id = ""
cmd = ""
spend_time = ""
client_name = ""
flag = False
re_id = re.compile(r"^\s*\d+\)\s+1\)\s+\(integer\)\s+(\d+)")
re_create_time = re.compile(r"^\s*2\)\s+\(integer\)\s+(\d+)")
re_spent_time = re.compile(r"^\s*3\)\s+\(integer\)\s+(\d+)")
re_cmd = re.compile(r"^\s*4\)\s+1\)\s+\"(.+)\"")
re_client = re.compile(r"^\s*5\)\s+\"(.+)\"")
re_client_name = re.compile(r"^\s*6\)\s+\"(.+)\"")
for i in t:
    # match 100) 1) (integer) 145771
    # match  99) 1) (integer) 145772
    # got 145771 and 145772
    if re_id.match(i):
        x = re_id.match(i).group(1)
        log.append({"id": x})
        id = x
        continue
    if re_create_time.match(i):
        x = re_create_time.match(i).group(1)
        log[-1]["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(x)))
        continue
    if re_spent_time.match(i):
        x = re_spent_time.match(i).group(1)
        log[-1]["spent_time"] = x
        continue
    if re_cmd.match(i):
        x = re_cmd.match(i).group(1)
        log[-1]["cmd"] = x
        flag = True
        continue
    if flag:
        if re_client.match(i):
            x = re_client.match(i).group(1)
            log[-1]["client"] = x
            flag = False
            continue
        else:
            # replace 2) or 3) and n) with space
            x = re.sub(r"^\s*\d+\)\s+", " ", i).replace("\n", "").replace("\r", "").replace("\"", "").replace("\\", "")
            log[-1]["cmd"] += x
            continue
    if re_client_name.match(i):
        x = re_client_name.match(i).group(1)
        log[-1]["client_name"] = x
        continue
# sort with spent_time
log.sort(key=lambda x: int(x["spent_time"]), reverse=True)
# print log in json format
print(json.dumps(log, indent=4))
