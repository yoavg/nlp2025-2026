import random
import json
import webbrowser

lines = open("page_urls.jsonl").readlines()
selected = json.loads(random.choice(lines))
print(selected["url"])
print(selected["file_name"])
print(selected["file_name"].split("/")[-1].split(".")[0])
webbrowser.open(selected["file_name"])

