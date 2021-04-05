import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

df1 = pd.read_csv('output17.csv')
df2 = pd.read_csv('output18.csv')
df3 = pd.read_csv('output19.csv')

dfs = [df1, df2, df3]
df = pd.concat(dfs, ignore_index=True, verify_integrity=True)
df.drop('Unnamed: 0', axis=1, inplace=True)

# Calculate Z-Scores
minTemps = (df['minTemp']-df['minTemp'].mean())/df['minTemp'].std()
maxTemps = (df['maxTemp']-df['maxTemp'].mean())/df['maxTemp'].std()
percipitations = (df['percipitation']-df['percipitation'].mean())/df['percipitation'].std()
winds = (df['wind']-df['wind'].mean())/df['wind'].std()
windGusts = (df['windGust']-df['windGust'].mean())/df['windGust'].std()

# Replace with normalized data
df['minTemp'] = minTemps
df['maxTemp'] = maxTemps
df['percipitation'] = percipitations
df['wind'] = winds
df['windGust'] = windGusts

# Is this data useable
df['drop'] = False
for index, row in df.iterrows():
    components = row['date'].split('/')
    
    # If the data is a weekday mark it to be dropped
    if date(int(components[2]), int(components[0]), int(components[1])).weekday() >= 5:
        df.loc[index, 'drop'] = True

# Create a row to track snowday labels (set all to false and manually parse)
df.insert(7, "snowday", False)

df.to_csv('normalOutput.csv')

df.plot('minTemp', 'maxTemp', kind='scatter')
plt.show()