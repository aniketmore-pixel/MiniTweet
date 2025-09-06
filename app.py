from flask import Flask, request, jsonify, render_template
import psycopg2
import redis
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# Connect to Postgres
conn = psycopg2.connect(
    dbname="twitterdb",
    user="postgres",
    password="005007",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route('/')
def home():
    return render_template('index.html')

# Users
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    cursor.execute("INSERT INTO users (username) VALUES (%s) RETURNING id;", (data['username'],))
    user_id = cursor.fetchone()[0]
    conn.commit()
    return jsonify({"user_id": user_id})

# Follow
@app.route('/follow', methods=['POST'])
def follow():
    data = request.json
    cursor.execute("INSERT INTO follows (follower_id, following_id) VALUES (%s,%s);",
                   (data['follower_id'], data['following_id']))
    conn.commit()
    return jsonify({"status": "followed"})

# Tweets
@app.route('/tweet', methods=['POST'])
def tweet():
    data = request.json
    cursor.execute("INSERT INTO tweets (user_id, content) VALUES (%s,%s) RETURNING id, created_at;",
                   (data['user_id'], data['content']))
    tweet_id, created_at = cursor.fetchone()
    conn.commit()

    # push tweet into Redis cache for fast retrieval
    followers_query = "SELECT follower_id FROM follows WHERE following_id=%s;"
    cursor.execute(followers_query, (data['user_id'],))
    followers = cursor.fetchall()
    for f in followers:
        feed_key = f"feed:{f[0]}"
        r.lpush(feed_key, f"{tweet_id}:{data['content']}:{created_at}")
        r.ltrim(feed_key, 0, 99)  # keep only 100 latest tweets

    return jsonify({"tweet_id": tweet_id})

# Feed
@app.route('/feed/<int:user_id>', methods=['GET'])
def feed(user_id):
    feed_key = f"feed:{user_id}"
    cached_feed = r.lrange(feed_key, 0, 20)
    if cached_feed:
        return jsonify({"feed": cached_feed})

    # fallback to DB if cache miss
    query = """
        SELECT t.id, t.content, t.created_at
        FROM tweets t
        JOIN follows f ON t.user_id=f.following_id
        WHERE f.follower_id=%s
        ORDER BY t.created_at DESC
        LIMIT 20;
    """
    cursor.execute(query, (user_id,))
    tweets = cursor.fetchall()
    return jsonify({"feed": tweets})

if __name__ == '__main__':
    app.run(debug=True)
