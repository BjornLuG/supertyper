import json
import re
import requests

# Settings
# Type of text: "gibberish" or "lorem"
text_type = "gibberish"
# Number of texts to retrieve
text_count = 5
# Minumum word count per text
min_text_len = 20
# Maximum word count per text
max_text_len = 30
# File to save result
save_file = "texts.json"

url = f"http://www.randomtext.me/api/{text_type}/p-{text_count}/{min_text_len}-{max_text_len}"

req = requests.get(url)
json_data = req.json()
text_out = json_data["text_out"]

texts = re.findall("<p>(.+?)</p>", text_out)

with open(save_file, "w") as write_file:
    json.dump(texts, write_file, indent=4)
