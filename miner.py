# Created By Addison Hanrattie 2021
# All Right Reserved

import requests

year = "2020" # year of december
headLink = "https://www.ncei.noaa.gov/data/national-digital-guidance-database/access/historical/"

for year in ("2020",):
	for month in ("12", "01", "02", "03"):
		for day in ("01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"):
			if int(day) > 29 or (int(day) > 28 and int(year) % 4 != 0):
				continue
			for hour in ("0500", "0600", "0700"):
				fileName = "LEIA98_KWBR_" + year + month + day + hour
				link = headLink + year + month + "/" + year + month + day + "/" + fileName
				print(link)



# for i in range(32): # LEIA98_KWBR_2020 12 31 1 05 00
# 	link = "LEIA98_KWBR_" + year + 

# 	https://www.ncei.noaa.gov/data/national-digital-guidance-database/access/202012/20201231/LEIA98_KWBR_202012310500