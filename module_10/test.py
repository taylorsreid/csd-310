import json

with open("bacchus.json") as bacchus_json:
    bacchus = json.load(bacchus_json)

print(type(bacchus))

i = 0
while i < len(bacchus["employee"]):
    print(bacchus["employee"][i]["employee_first_name"])
    i += 1