from datetime import datetime
import pandas as pd
from hrrrb.archive import download_hrrr

sDate = datetime(2019,12,1)
eDate = datetime(2020,4,1)

DATES = pd.date_range(sDate, eDate, freq='1H')

download_hrrr(DATES, fxx = range(0, 1), SAVEDIR='./master_data/hrrr1', dryrun=True)