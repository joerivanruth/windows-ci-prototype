#!/usr/bin/env python3

import re
import sys
from urllib.request import urlopen

BASE = 'https://www.monetdb.org/downloads/Windows/Latest/'

if len(sys.argv) != 2:
	exit(f"Usage: {sys.argv[0]} ..\\path\\to\\msifile.exe")
dest = sys.argv[1]


# The name of the file we need contains the date it was created
# so we first have to figure out the exact name of the file by parsing
# the accompanying chechsum file

pattern = re.compile(r'MonetDB5-SQL-Installer-x86_64-\d+[.]msi$')
for line in urlopen(BASE + 'SHA256SUM'):
	line = str(line, 'utf-8').rstrip()
	m = pattern.search(line)
	if m:
		filename = m.group(0)
		break
else:
	exit('could not figure out the exact filename to download')

# It's only a few megabytes..
msi_url = BASE + filename
r = urlopen(msi_url)
content = r.read()
r.close()
w = open(dest, 'wb')
w.write(content)
w.close()

print(f"Succesfully downloaded {msi_url} to {dest}")