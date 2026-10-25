from __future__ import annotations

import threading
import time
from typing import Dict, Tuple


class TokenBucketRateLimiter:
    """Thread-safe token bucket rate limiter for DoS mitigation on CPU-heavy endpoints."""

    def __init__(self, capacity: int = 10, refill_rate_per_sec: float = 5.0) -> None:
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.buckets: Dict[str, Tuple[float, float]] = {}  # key -> (tokens, last_update)
        self.lock = threading.Lock()

    def check_rate_limit(self, client_key: str, cost: float = 1.0) -> bool:
        """Returns True if allowed, False if rate limited."""
        now = time.time()
        with self.lock:
            if client_key not in self.buckets:
                self.buckets[client_key] = (float(self.capacity) - cost, now)
                return True

            tokens, last_update = self.buckets[client_key]
            elapsed = now - last_update
            tokens = min(float(self.capacity), tokens + (elapsed * self.refill_rate))

            if tokens >= cost:
                self.buckets[client_key] = (tokens - cost, now)
                return True
            else:
                self.buckets[client_key] = (tokens, now)
                return False

    def reset(self) -> None:
        with self.lock:
            self.buckets.clear()

