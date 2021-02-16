from os import listdir
from os.path import isfile, join
import pygrib
import numpy as np

temp = []

for f in listdir("temperatures"):
	grbs = pygrib.open("temperatures/" + f)
	grb = grbs.select(name="2 metre temperature")[1] #0 or 1
	dat = grb.data(lat1=41.1, lat2=41.15, lon1=-73.5, lon2=-73.45)
	print(dat)
