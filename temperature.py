import requests
import sqlite3 as lite
import datetime
from datetime import timedelta

url = 'https://api.forecast.io/forecast/' + api_key
cities = {"Denver": '39.761850, -104.881105', "Chicago": '41.837551, -87.681844', "Miami": '25.775163, -80.208615', "Philadelphia": '40.009376, -75.133346', "Austin": '30.303936, -97.754355'}
end_date = datetime.datetime.now()
con = lite.connect('weather.db')
cur = con.cursor()
with con:
	cur.execute('CREATE TABLE daily_temp ( day_of_reading INT, Denver REAL, Miami REAL, Philadelphia REAL, Austin REAL, Chicago REAL);')
query_date = end_date - datetime.timedelta(days=30)
with con:
	while query_date < end_date:
		cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%s')),))
		query_date += datetime.timedelta(days=1)
for k,v in cities.iteritems():
	query_date = end_date - datetime.timedelta(days=30)
	while query_date < end_date:
		r = requests.get(url + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))
		with con:
			cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))
		query_date += datetime.timedelta(days=1)

con.close()

df = pd.read_sql_query("SELECT * FROM daily_temp", con, index_col = "day_of_reading")

print str(df['Denver'].mean()) + " is the mean in Denver"
print str(df['Miami'].mean()) + " is the mean in Miami"
print str(df['Philadelphia'].mean()) + " is the mean in Philadelphia"
print str(df['Austin'].mean()) + " is the mean in Austin"
print str(df['Chicago'].mean()) + " is the mean in Chicago"

print str(df['Denver'].max()-df['Denver'].min()) + " is the range in Denver"
print str(df['Miami'].max()-df['Miami'].min()) + " is the range in Miami"
print str(df['Austin'].max()-df['Austin'].min()) + " is the range in Austin"
print str(df['Philadelphia'].max()-df['Philadelphia'].min()) + " is the range in Philadelphia"
print str(df['Chicago'].max()-df['Chicago'].min()) + " is the range in Chicago"

print str(df['Denver'].var()) + " is the variance in Denver"
print str(df['Miami'].var()) + " is the variance in Miami"
print str(df['Philadelphia'].var()) + " is the variance in Philadelphia"
print str(df['Austin'].var()) + " is the variance in Austin"
print str(df['Chicago'].var()) + " is the variance in Chicago"

df['Denver'].hist()
df['Miami'].hist()
df['Austin'].hist()
df['Philadelphia'].hist()
df['Chicago'].hist()

plt.show()
