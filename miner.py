# Created By Addison Hanrattie 2021
# All Right Reserved

import requests
import shutil

headLink = "https://www.ncei.noaa.gov/data/national-digital-guidance-database/access/"
header = "LEIA98_KWBR_"
missed = []

# Parse Through Date Components
for winterYear in ("2019",):
	for month in ("12", "01", "02", "03"):
		#Move year forward if after december
		year = winterYear
		if month != "12":
			year = str(int(winterYear) + 1)
		print("Started: " + year + "/" + month)

		# Is data in historical folder
		if year + month in ("202102", "202101", "202012", "202011", "202010", "202009", "202008", "202007", "202006"): #"202005", "201912", "201911", "201910", "201909", "201908", "201907", "201906", "201905", "201904", "201903", "201902", "201812", "201811", "201711"]:
			historical = ""
		else:
			historical = "historical/"
		for day in ("01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"):
			# Skip if extra days of febuary
			if month == "02" and (int(day) > 29 or (int(day) > 28 and int(year) % 4 != 0)):
				continue

			# May's Data is split in the middle
			if year + month == "202005" and int(day) <= 15:
				historical = "historical/"
			elif year + month == "202005":
				historical = ""

			for hour in ("0000", "0100", "0200", "0300", "0400", "0500", "0600", "0700", "0800", "0900", "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800", "1900", "2000", "2100", "2200", "2300"):
				# Create File Link
				fileName = header + year + month + day + hour
				link = headLink + historical + year + month + "/" + year + month + day + "/" + fileName

				# Request Data
				r = requests.get(link, stream=True)
				if r.status_code == 200:
					r.raw.decode_content = True
					with open("data/" + fileName, 'wb') as f:
						shutil.copyfileobj(r.raw, f)
				else:
					# If fail search alternate directory and then check
					hisTemp = "historical/" if historical == "" else ""
					link = headLink + hisTemp + year + month + "/" + year + month + day + "/" + fileName

					# Request Data Again
					r = requests.get(link, stream=True)
					if r.status_code == 200:
						r.raw.decode_content = True
						with open("data/" + fileName, 'wb') as f:
							shutil.copyfileobj(r.raw, f)
						print("Retreived " + hisTemp + fileName + " on alternate")
					else:
						print("Failed to get " + fileName + ", reason: " + r.reason + ", code: " + str(r.status_code))
						missed.append(fileName)

# Note missed files so they may be recovered through other methods
with open("data/missed.txt", 'w') as fp:
	fp.write('\n'.join(missed) + '\n')
print("Finished with " + str(len(missed)) + " files skipped")
