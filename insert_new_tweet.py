import time
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory
from cassandra import ConsistencyLevel
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

time_stamp = datetime.datetime.now()

# Tweet data
author = 'katyperry'
date_time = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
tweet_id = int(time.mktime(time_stamp.timetuple()))
content = 'Hello World!'
language = 'en'

# Insert new tweet into twitter.tweets_by_authors
stmt_insert_new_tweet = "INSERT INTO twitter.tweets_by_authors (author, date_time, tweet_id, content, language, number_of_likes, number_of_shares) VALUES ('" + author + "', '" + str(date_time) + "', " + str(tweet_id) + ", '" + content + "', '" + language + "', 0, 0)"
session.execute(stmt_insert_new_tweet)

# Insert new tweet into follower caches
stmt_get_followers = "SELECT username FROM twitter.follower_relations_by_users WHERE rel_type = 'follows' AND rel_target_username = '" + author + "' ALLOW FILTERING"
for row in session.execute(stmt_get_followers):
    username = row[0]
    stmt_insert_in_follower_cache = "INSERT INTO twitter.caches_by_users (username, date_time, tweet_id, author, content, language, number_of_likes, number_of_shares) VALUES ('" + username + "', '" + str(date_time) + "', " + str(tweet_id) + ", '" + author + "', '" + content + "', '" + language + "', 0, 0)"
    session.execute(stmt_insert_in_follower_cache)
