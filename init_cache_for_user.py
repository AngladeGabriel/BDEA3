from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import WhiteListRoundRobinPolicy, DowngradingConsistencyRetryPolicy
from cassandra.query import tuple_factory
from cassandra import ConsistencyLevel

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

# User to initialize the cache for
username = 'Finn_Hollie-Lee'

stmt_get_follows = "SELECT rel_target_username FROM twitter.follower_relations_by_users WHERE username = '" + username + "' AND rel_type = 'follows'"
for row_follows in session.execute(stmt_get_follows):
    author = row_follows[0]
    stmt_get_tweets_from_author = "SELECT * FROM twitter.tweets_by_authors WHERE author = '" + author + "'"
    for row_tweets in session.execute(stmt_get_tweets_from_author):
        author = row_tweets[0]
        date_time = row_tweets[1]
        tweet_id = row_tweets[2]
        content = row_tweets[3].replace('\'', '')
        language = row_tweets[4]
        number_of_likes = row_tweets[5]
        number_of_shares = row_tweets[6]
        stmt_insert_tweet_in_cache = "INSERT INTO twitter.caches_by_users (username, date_time, tweet_id, author, content, language, number_of_likes, number_of_shares) VALUES ('" + username + "', '" + str(date_time) + "', " + str(tweet_id) + ", '" + author + "', '" + content + "', '" + language + "', " + str(number_of_likes) + ", " + str(number_of_shares) + ")"
        session.execute(stmt_insert_tweet_in_cache)