from os import listdir
from os.path import isfile, join
import pygrib
import numpy as np
import json

temps = {}

dayComp = ""

def populate(y, m, d):
	if y in temps:
		if m in temps[y]:
			if d not in temps[y][m]:
				temps[y][m][d] = {}
		else:
			temps[y][m] = {}
			temps[y][m][d] = {}
	else:
		temps[y] = {}
		temps[y][m] = {}
		temps[y][m][d] = {}

for f in listdir("temperatures"):
	grbs = pygrib.open("temperatures/" + f)
	for elem in grbs:
		if elem['average'] > 50:
			grb = elem
	dat = grb.data(lat1=41.11, lat2=41.18, lon1=-73.55, lon2=-73.45)

	y = int(f[12:16])
	m = int(f[16:18])
	d = int(f[18:20])
	t = int(f[20:24])
	populate(y,m,d)
	temps[y][m][d][t] = sum(dat[0]) / (len(dat[0])) #take median to avoid skewing
	print(f)

with open('data.json', 'w') as fp:
	json.dump(temps, fp, indent=2, sort_keys=True)