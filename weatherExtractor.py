from pathlib import Path
from os.path import isfile, join
import pygrib
import numpy as np
import json

weather = {}

dayComp = ""

def populate(y, m, d):
	if y in weather:
		if m in weather[y]:
			if d not in weather[y][m]:
				weather[y][m][d] = {}
		else:
			weather[y][m] = {}
			weather[y][m][d] = {}
	else:
		weather[y] = {}
		weather[y][m] = {}
		weather[y][m][d] = {}


# Get a list and iterate through all gribs
files = list(Path("./data").rglob("LEIA*"))
i = 0
for loc in files:
	f = str(loc)
	grbs = pygrib.open(str(f))
	f = f[5:]
	for elem in grbs:
		# # Temperature check only
		# if elem['average'] > 25:
		# 	grb = elem
		grb = elem
	dat = grb.data(lat1=41.11, lat2=41.18, lon1=-73.55, lon2=-73.45)

	grbs.close()

	y = int(f[12:16])
	m = int(f[16:18])
	d = int(f[18:20])
	t = int(f[20:24])

	populate(y,m,d)
	weather[y][m][d][t] = sum(dat[0]) / (len(dat[0])) #could take median to avoid skewing
	
	i += 1
	if i % (len(files) // 20) == 0:
		print(i / len(files))

# Save data in JSON
with open('data2019p.json', 'w') as fp:
	json.dump(weather, fp, indent=2, sort_keys=True)