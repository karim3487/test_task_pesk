import time
from utils.redis_client import redis_client

# Constants for Redis key prefixes
WHITELIST_PREFIX = "whitelist:"
BLACKLIST_PREFIX = "blacklist:"


class TokenService:
    """
    Service for managing token whitelist and blacklist operations in Redis.
    """

    @staticmethod
    def _current_timestamp() -> int:
        """
        Return the current timestamp as an integer.
        """
        return int(time.time())

    @staticmethod
    def _calculate_ttl(exp: int) -> int:
        """
        Calculate the time-to-live (TTL) for a token based on its expiration time.
        """
        ttl = exp - TokenService._current_timestamp()
        return ttl if ttl > 0 else 0

    @staticmethod
    def add_to_whitelist(jti: str, exp: int) -> None:
        """
        Add a token to the whitelist with a TTL that expires at the token's expiration time.
        """
        ttl = TokenService._calculate_ttl(exp)
        if ttl > 0:
            redis_client.setex(f"{WHITELIST_PREFIX}{jti}", ttl, "1")
        # Optionally, handle the case where ttl <= 0

    @staticmethod
    def add_to_blacklist(jti: str, exp: int) -> None:
        """
        Add a token to the blacklist with a TTL that expires at the token's expiration time.
        """
        ttl = TokenService._calculate_ttl(exp)
        if ttl > 0:
            redis_client.setex(f"{BLACKLIST_PREFIX}{jti}", ttl, "1")
        # Optionally, handle the case where ttl <= 0

    @staticmethod
    def is_blacklisted(jti: str) -> bool:
        """
        Check if the token with the given jti is in the blacklist.
        """
        return redis_client.exists(f"{BLACKLIST_PREFIX}{jti}") == 1

    @staticmethod
    def is_whitelisted(jti: str) -> bool:
        """
        Check if the token with the given jti is in the whitelist.
        """
        return redis_client.exists(f"{WHITELIST_PREFIX}{jti}") == 1

    @staticmethod
    def remove_from_whitelist(jti: str) -> None:
        """
        Remove a token from the whitelist.
        """
        redis_client.delete(f"{WHITELIST_PREFIX}{jti}")
