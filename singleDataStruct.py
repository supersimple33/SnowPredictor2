import json
import pandas as pd

# structure = {'date', 'minTemp', 'maxTemp', 'percipitation', 'wind'}
structure = ['date', 'minTemp', 'maxTemp', 'percipitation', 'wind', 'windGust']
rows = []

with open("rt2017temp.json", 'r') as f:
	temp = json.load(f)

with open("rt2017p.json", 'r') as f:
	percip = json.load(f)

with open("rt2017wind.json", 'r') as f:
	wind = json.load(f)

with open("rt2017gust.json", 'r') as f:
	gust = json.load(f)

for y in temp.keys():
	for m in temp[y].keys():
		for d in temp[y][m].keys():
			# Safety check, ensure data exists
			if len(temp[y][m][d]) < 24 or len(percip[y][m][d]) < 24 or len(wind[y][m][d]) < 24 or len(gust[y][m][d]) < 24:
				print('A data group was missing data on ' + m + '/' + d + '/' + y)
			
			# Get temperature data
			# avgTemp = sum(temp[y][m][d].values()) / len(temp[y][m][d])
			maxTemp = max(temp[y][m][d].values())
			minTemp = min(temp[y][m][d].values())

			# Get percip data
			totalPercipitation = sum(percip[y][m][d].values())

			# Get wind data
			avgWind = sum(wind[y][m][d].values()) / len(wind[y][m][d])

			# Get gust data
			maxGust = max(gust[y][m][d].values())

			elem = [m + '/' + d + '/' + y, minTemp, maxTemp, totalPercipitation, avgWind, maxGust]
			rows.append(elem)

df = pd.DataFrame(data=rows, columns=structure)

df.to_csv("output17.csv")