from utils.redis_client import redis_client


class TokenService:

    @staticmethod
    def add_to_whitelist(jti: str, exp: int):
        """
        Add token to whitelist with TTL before the expiration of the deadline
        """
        ttl = exp - TokenService._current_timestamp()
        redis_client.setex(f"whitelist:{jti}", ttl, "1")

    @staticmethod
    def add_to_blacklist(jti: str, exp: int):
        """
        Add token to blacklist with TTL before the expiration of the deadline
        """
        ttl = exp - TokenService._current_timestamp()
        redis_client.setex(f"blacklist:{jti}", ttl, "1")

    @staticmethod
    def is_blacklisted(jti: str) -> bool:
        return redis_client.exists(f"blacklist:{jti}") == 1

    @staticmethod
    def is_whitelisted(jti: str) -> bool:
        return redis_client.exists(f"whitelist:{jti}") == 1

    @staticmethod
    def _current_timestamp():
        import time

        return int(time.time())
