import time
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory
from cassandra import ConsistencyLevel
import pandas as pd
import cassandra
import datetime


profile = ExecutionProfile(
    load_balancing_policy=WhiteListRoundRobinPolicy(['127.0.0.1']),
    retry_policy=DowngradingConsistencyRetryPolicy(),
    consistency_level=ConsistencyLevel.LOCAL_QUORUM,
    serial_consistency_level=ConsistencyLevel.LOCAL_SERIAL,
    request_timeout=15,
    row_factory=tuple_factory
)
cluster = Cluster(execution_profiles={EXEC_PROFILE_DEFAULT: profile})
session = cluster.connect('twitter')

#stmt = "SELECT * FROM twitter.follower_relations_by_users"
stmt2 = "SELECT username, COUNT(*) AS followers FROM twitter.follower_relations_by_users WHERE rel_type = 'follower' GROUP BY username ALLOW FILTERING"
#rows = session.execute(stmt)
#rows2 = session.execute(stmt2)

row_list = []
for user_row in session.execute(stmt2):
    row_list.append(user_row)
    # username            | rel_type | rel_target_id | rel_target_username
    #columns = ["username", "rel_type", "rel_target_id", "rel_target_username"]
columns = ["username", "followers"]
#print(len(row_list))
df = pd.DataFrame(row_list, columns=columns)
#print(df)
top100 = df.sort_values(by=['followers'],  ascending=False).head(100)
print(top100)   
json = top100.to_json(orient="records")
#print(json)

d = datetime.datetime.now()

unixtime = time.mktime(d.timetuple())

session.execute("CREATE TABLE IF NOT EXISTS twitter.top100_accounts_by_time (uuid text, follower_json text, ts timeuuid, primary key(uuid, ts)) WITH CLUSTERING ORDER BY (ts DESC)")
query = "INSERT INTO twitter.top100_accounts_by_time(uuid,follower_json,ts) VALUES (?,?,?)"
prepared = session.prepare(query)
session.execute(prepared, ("insert"+str(int(unixtime)) , json, cassandra.util.uuid_from_time(time.time())))

    # CREATE MATERIALIZED VIEW twitter.gummigut 
    # AS SELECT * FROM twitter.follower_relations_by_users 
    # WHERE rel_type = 'follows' 
    # AND rel_target_username IS NOT NULL 
    # AND rel_target_id IS NOT NULL 
    # PRIMARY KEY (username, rel_type, rel_target_username, rel_target_id);

    #CREATE MATERIALIZED VIEW twitter.gummigut AS SELECT * FROM twitter.follower_relations_by_users WHERE rel_type = 'follows' AND rel_target_username IS NOT NULL AND rel_target_id IS NOT NULL PRIMARY KEY (username, rel_type, rel_target_username, rel_target_id);

# take series of usernames from top100 and convert it to list
top100_accounts_list = top100['username'].to_list()
# perpare statement
q_stmt = "SELECT username, rel_target_username FROM twitter.gummigut WHERE rel_type = 'follows' AND username IN %s"
res_list = []
# execute statement in iterative way because of possible pagination
for row in session.execute(q_stmt, parameters=[cassandra.query.ValueSequence(top100_accounts_list)]):
    res_list.append(row)


following_top_100 = pd.DataFrame(res_list, columns=['account', 'follower'])
# group by followers (those following our top100, count amount of followed accounts, sort desc)
ft100 = following_top_100.groupby(["follower"])['account'].count().reset_index().sort_values(by=['account'], ascending=False).head(100)
ft100 = ft100.rename(columns={'account': 'follows'})
print(ft100)
#generate JSON from dataframe
ft100_json = ft100.to_json(orient="records")
print(ft100_json)
#same pattern as above for top100
session.execute("CREATE TABLE IF NOT EXISTS twitter.top100_followers_by_time (uuid text, follower_json text, ts timeuuid, primary key(uuid, ts)) WITH CLUSTERING ORDER BY (ts DESC)")
query = "INSERT INTO twitter.top100_followers_by_time(uuid,follower_json,ts) VALUES (?,?,?)"
prepared = session.prepare(query)
session.execute(prepared, ("insert"+str(int(unixtime)) , ft100_json, cassandra.util.uuid_from_time(time.time())))
