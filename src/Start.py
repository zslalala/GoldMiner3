import redis
from DashLayOut import app

r = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

if __name__  == "__main__":
    app.run_server()