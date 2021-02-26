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
files = list(Path("./master_data/temp2").rglob("YGB*"))
i = 0
offset = 12
for loc in files:
	f = str(loc)
	grbs = pygrib.open(str(f))
	f = f.split('/')[-1]

	# Extract Dates
	y = int(f[offset : offset+4])
	m = int(f[offset+4 : offset+6])
	d = int(f[offset+6 : offset+8])
	t = int(f[offset+8 : offset+12])
	datNum = (y * 10000) + (m * 100) + d

	fct = 10000
	for elem in grbs:
		# # Temperature check only
		# if elem['average'] > 25:
		# 	grb = elem
		if elem['forecastTime'] < fct:
			grb = elem
			fct = elem['forecastTime']
	dat = grb.data(lat1=41.11, lat2=41.18, lon1=-73.55, lon2=-73.45)

	grbs.close()

	populate(y,m,d)
	weather[y][m][d][t] = sum(dat[0]) / (len(dat[0])) #could take median to avoid skewing
	
	i += 1
	if i % (len(files) // 20) == 0:
		print(i / len(files))

# Save data in JSON
with open('data2019maxt.json', 'w') as fp:
	json.dump(weather, fp, indent=2, sort_keys=True)