import random
import json
import webbrowser
from pathlib import Path

lines = open("page_urls.jsonl").readlines()
selected = json.loads(random.choice(lines))
print(selected["url"])
print(selected["file_name"])
print(selected["file_name"].split("/")[-1].split(".")[0])

current_dir = Path(__file__).parent.absolute()
url = current_dir / selected["file_name"]

webbrowser.open(url)
