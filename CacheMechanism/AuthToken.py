import redis
from threading import Lock

class AuthTokenCache:
    def __init__(self, max_size, redis_host='localhost', redis_port=6379, redis_db=0):
        """
        Initialize the AuthTokenCache with a maximum size and connect to Redis.
        
        :param max_size: Maximum number of tokens the cache can hold.
        :param redis_host: Host where Redis is running.
        :param redis_port: Port where Redis is running.
        :param redis_db: Redis database index to use.
        """
        self.max_size = max_size
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
        self._lock = Lock()  # Lock to ensure thread safety

    def getToken(self, user_id):
        """
        Retrieve a token from the cache for a given user_id.
        
        :param user_id: The user_id for which the token is to be retrieved.
        :return: The token if it exists in the cache, otherwise None.
        """
        with self._lock:
            token = self.redis_client.get(user_id)
            if token:
                # Move the token to the end to simulate access order
                # Redis does not require manual reordering as in OrderedDict,
                # but we include this to simulate similar behavior if needed.
                self.redis_client.expire(user_id, 3600)  # Optionally reset TTL for the key
            return token

    def setToken(self, user_id, token):
        """
        Add a new token to the cache and handle FIFO eviction if necessary.
        
        :param user_id: The user_id associated with the token.
        :param token: The authentication token to be stored.
        """
        with self._lock:
            if self.redis_client.exists(user_id):
                # If user_id already in cache, remove it to update its position
                self.redis_client.delete(user_id)
            elif self.redis_client.dbsize() >= self.max_size:
                # If cache is at max capacity, evict the oldest entry (FIFO)
                oldest_key = next(iter(self.redis_client.scan_iter()))
                self.redis_client.delete(oldest_key)

            # Add the new token
            self.redis_client.set(user_id, token)

    def __repr__(self):
        """
        Return a string representation of the current cache contents for debugging.
        
        :return: String representation of the cache.
        """
        with self._lock:
            keys = self.redis_client.keys()
            return str({key: self.redis_client.get(key) for key in keys})

