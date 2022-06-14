from html.entities import name2codepoint
from os import name
import os
import pandas as pd
import numpy as np
from itertools import count, product

#get tweets csv to grab the names of our VIPs
csv_path = "C:/Users/Gabriel/Documents/HS-MA/8IB/BDEA/Abgabe3/bdea_data/tweets.csv"
data = pd.read_csv(csv_path)
df = data.groupby(by=['author']).count()

#grab follower relations to get all occuring IDs
follower_path = "C:/Users/Gabriel/Documents/HS-MA/8IB/BDEA/Abgabe3/bdea_data/twitter_combined/twitter_combined.csv"
data2 = pd.read_csv(follower_path, delimiter=' ', names=['user', 'follower'])
f_rel_dataframe_indexed = pd.read_csv(follower_path, delimiter=' ', names=['user', 'follower'], index_col=False)

df2 = data2.groupby(by=['user']).count()

# most followed ids from follower-relations will be assigned VIP accounts
t20 = df2.sort_values(by='follower', ascending=False).head(df.shape[0])
lo = t20.index.to_list()
df = df.index.to_frame()
df['user_id'] = lo


#get namelists to generate random usernames (fillin)
boy_names = pd.read_csv('C:/Users/Gabriel/Documents/HS-MA/8IB/BDEA/Abgabe3/bdea_data/name_gen_res/babies-first-names-21-full-list_Boys.csv', sep=',')
girl_names =  pd.read_csv('C:/Users/Gabriel/Documents/HS-MA/8IB/BDEA/Abgabe3/bdea_data/name_gen_res/babies-first-names-21-full-list_Girls.csv', sep=',')
# ----------------------------------------------------------
#generate random usernames by getting ever combination of both np.Series with product
#result will be a tuple of a "first name" and "last name" - CDU style ;)
endless_names = list(product(boy_names['Boys\' names'].dropna(), girl_names['Girls\' names'].dropna()))
print('generated username-list length:'+str(len(endless_names)))
print('unique follower ids to serve:'+str(df2.shape[0]))
# add an empty col for usernames
df2['username'] = np.nan
# OLD NAME-ASSIGNER, did not cover unique ids in "follower"-col
# counter = 0
# for i, row in df2.iterrows():
#     #ugly and simple solution, urgh
#     df2.at[i, 'username'] = '_'.join(endless_names[counter])
#     counter = counter+1
# #remove unnessesary cols
# name_dataframe = df2.drop(columns='follower')

# NEW NAME-ASSIGNER
print('----------------------------------------\n----------------------------------------\n')
print(f_rel_dataframe_indexed)
print('----------------------------------------\n----------------------------------------\n')
#unique_ids = pd.concat(f_rel_dataframe_indexed['user'], f_rel_dataframe_indexed['follower']).unique()
unique_ids = list(set(f_rel_dataframe_indexed.user).union(set(f_rel_dataframe_indexed.follower)))
userlist = {'user':[], 'username':[]}
for index in range(len(unique_ids)):
    userlist['user'].append(unique_ids[index])
    userlist['username'].append('_'.join(endless_names[index]))

name_dataframe = pd.DataFrame(data=userlist)
print(name_dataframe)
print('----------------------------------------\n----------------------------------------\n')
print("End name-gen")
print('----------------------------------------\n----------------------------------------\n')
# ----------------------------------------------------------
 
vip_dataframe = df.copy()
# replace "fillin" names with vip accounts
for i, row in vip_dataframe.iterrows():
    id = row['user_id']
    name_dataframe.loc[name_dataframe['user']==id, ['username']] = row['author']
print('----------------------------------------\n----------------------------------------\n')
print("End vip replace")
print('----------------------------------------\n----------------------------------------\n')

print(name_dataframe)
# -> verify if our favorite ramen-noodle haired singer has arrived
print(name_dataframe.loc[name_dataframe['username']=='jtimberlake'])

#modified those dataframes so much, better get a clean version
follower_path = "C:/Users/Gabriel/Documents/HS-MA/8IB/BDEA/Abgabe3/bdea_data/twitter_combined/twitter_combined.csv"
data2 = pd.read_csv(follower_path, delimiter=' ', names=['user', 'follower'], index_col=False)
print(data2)

def build_follower_relation(user_id, username, follower_id, follower_name):
    '''
    with:
        params: 1234, katyperry, 4564, josephgoebbels
    returns:
        follower_rel:   katyperry, follower, josephgoebbels, 4564
        followes_rel:   josephgoebbels, follows, katyperry, 1234
    '''

    follower_rel = [username, 'follower', follower_name, follower_id]
    follows_rel = [follower_name, 'follows', username, user_id]
    res = {'follower_rel': follower_rel, 'follows_rel': follows_rel}
    return res

follower_relation_container = []

result_path = 'C:/Users/Gabriel/Documents/HS-MA/8IB/BDEA/Abgabe3/bdea_data/result/res_follower.csv'

for i, row in data2.iterrows():
    if len(follower_relation_container)%5000==0:
        # write chunk, this may take a while to finish 
        # create df with gathered 5000 entries
        print('Writing chunk with 5000 entries')
        follower_relation_df = pd.DataFrame(data=follower_relation_container, columns=['username', 'relation_type', 'rel_target_username', 'rel_target_id'])
        follower_relation_df.to_csv(path_or_buf=result_path, sep=',',index=False, mode='a', header=not os.path.exists(result_path))
        # clean, frech list
        follower_relation_container = []

    user_id = row['user']
    follower_id = row['follower']
    username = name_dataframe.loc[name_dataframe['user']==user_id]['username'].values[0]
    followername = name_dataframe.loc[name_dataframe['user']==follower_id]['username'].values[0]

    res = build_follower_relation(user_id, username, follower_id, followername)

    follower_relation_container.append(res['follower_rel'])
    follower_relation_container.append(res['follows_rel'])
    
print(len(follower_relation_container))
# write last chunk
follower_relation_df = pd.DataFrame(data=follower_relation_container, columns=['username', 'relation_type', 'rel_target_username', 'rel_target_id'])
follower_relation_df.to_csv(path_or_buf=result_path, sep=',',index=False, mode='a', header=not os.path.exists(result_path))
print('TERMINATED')