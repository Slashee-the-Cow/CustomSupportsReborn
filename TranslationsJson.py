import json
import sys

data = json.load(sys.stdin)
for entry in data:
    print(f'_("{entry["msgid"]}")')