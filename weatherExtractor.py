from pathlib import Path
import pygrib
import json
from concurrent import futures

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

def extract(file):
	grbs = pygrib.open(file)

	for grb in grbs:
		if grb.name == '2 metre temperature' and grb.bitsPerValue >= 10:
			dat = grb.data(lat1=41.11, lat2=41.18, lon1=-73.55, lon2=-73.45)
			grbs.close()
			return sum(dat[0]) / len(dat[0]) #could take median to avoid skewing
	raise KeyError # should only be executed if d
# Get a list and iterate through all gribs
files = list(Path("./master_data/rtma3").rglob("LTIA*"))
offset = 12

with futures.ThreadPoolExecutor() as executor:
	future_extract = dict((executor.submit(extract, str(loc)), str(loc)) for loc in files)

	i = 0
	for future in futures.as_completed(future_extract):
		file = future_extract[future]
		if future.exception() is not None:
			print('%r generated an exception: %s' % (file, future.exception()))
		else:
			f = file.split('/')[-1]
			# Extract Dates
			y = int(f[offset : offset+4])
			m = int(f[offset+4 : offset+6])
			d = int(f[offset+6 : offset+8])
			t = int(f[offset+8 : offset+12])
			populate(y,m,d)
			weather[y][m][d][t] = future.result()
		if i % (len(files) // 20) == 0:
			print(i / len(files))
		i += 1

# Save data in JSON
with open('rt2019wind3.json', 'w') as fp:
	json.dump(weather, fp, indent=2, sort_keys=True)