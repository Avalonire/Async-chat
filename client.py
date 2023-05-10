import csv
import json
import yaml

"""
CSV формат
"""

# with open('data.csv') as f:
#     f_reader = csv.reader(f)
#     for l in f_reader:
#         print(l, type(l))
#
# data = [
#     ['hostname', 'vendor', 'model', 'location'],
#     ['kp1', 'Cisco', '2960', 'Moscow'],
#     ['kp2', 'Cisco', '2960', 'Novosibirsk'],
#     ['kp3', 'Cisco', '2960', 'Kazan'],
#     ['kp4', 'Cisco', '2960', 'Tomsk']
# ]
#
# with open('new_data.csv', 'w') as f:
#     f_writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
#     for row in data:
#         f_writer.writerow(row)


"""
JSON формат
"""

# with open('data.json') as f:
#     objects = json.load(f)
#     for s, c in objects.items():
#         print(s, c)


# with open('data.json') as f:
#     objects = json.loads(f.read())
#     print(objects, type(objects))
#     print('data', objects['action'])


# data = {
#     "action": "msg",
#     "time": "<unix timestamp>",
#     "to": "account_name",
#     "from": "account_name",
#     "encoding": "ascii",
#     "message": "message"
# }
#
# with open('new_data.json', 'w') as f:
#     json.dump(data, f, sort_keys=True, indent=4, skipkeys=True)
#
# with open('new_data.json') as f:
#     data = json.load(f)
#     for k, v in data.items():
#         print(k, v, type(v))


"""
YAML формат
"""

action_list = ['msg1', 'msg2', 'msg3']
to_list = ['account', 'account2', 'account3']

data_to_yaml = {'action': action_list, 'to': to_list}

with open('new_data.yaml', 'w') as f:
    yaml.dump(data_to_yaml, f, default_flow_style=True)
