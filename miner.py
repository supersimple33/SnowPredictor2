# Created By Addison Hanrattie 2021
# All Right Reserved

import requests
import shutil

headLink = "https://www.ncei.noaa.gov/data/national-digital-guidance-database/access/"

# Parse Through Date Components
for winterYear in ("2018",):
	for month in ("12", "01", "02", "03"):
		#Move year forward if after december
		year = winterYear
		if month != "12":
			year = str(int(winterYear) + 1)

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

			for hour in ("0500",):
				# Create File Link
				fileName = "LTIA98_KWBR_" + year + month + day + hour
				link = headLink + historical + year + month + "/" + year + month + day + "/" + fileName

				# Save File
				r = requests.get(link, stream=True)
				r.raw.decode_content = True
				with open("data/" + fileName, 'wb') as f:
					shutil.copyfileobj(r.raw, f)
					print("Data Saved: " + link)
