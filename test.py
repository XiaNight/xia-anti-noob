import re
finds = re.findall(r'^\.([^\ ]*)\ ?(.*)', ".att test")[0]
print(finds)