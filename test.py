import re
def ParseCommand(message):
    finds = re.findall(r'^\.([^\ ]*)\ ?(.*)', message)
    if len(finds) == 0:
    	return ('', '')
    return finds[0]

msg = ".gt 3 2"
cmd, payload = ParseCommand(msg)
cmd = cmd.lower()
print(cmd, payload)