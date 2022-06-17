from sqlite3 import Timestamp
import pandas as pd
import sys
import random

tweet_path = ''
try:
    tweet_path = sys.argv[1]
except:
    print('no further params')
if not tweet_path:
    #lazy option
    tweet_path = "C:/Users/Gabriel/Documents/HS-MA/8IB/BDEA/Abgabe3/bdea_data/tweets.csv"

df = pd.read_csv(tweet_path)
df_len = df.shape[0]
new_ids = random.sample(range(df_len%2, df_len*2), df_len)
#replace crooked ids with random generated numbers
df['id'] = new_ids

#replace ugly date_time format with cassandra timestamp format
# given format: MM/DD/YYYY HH:M
# wanted format: yyyy-mm-dd HH:MM:SS

for i, row in df.iterrows():
    elem = row['date_time']
    split_elem = elem.split()
    date = split_elem[0].split('/')
    time = split_elem[1]+':00'
    rearanged_date = '-'.join([date[2],date[0],date[1]])
    cass_timestamp = rearanged_date+' '+time
    df.at[i, 'date_time'] = cass_timestamp

ser = df['latitude']
ser = ser.dropna()
print("SER:")
print(ser)
print(df)
split_path = tweet_path.split('/')[:-1]
path = '/'.join(split_path)+'/tweets_clean.csv'
print(path)
df.to_csv(path_or_buf=path, sep=',')