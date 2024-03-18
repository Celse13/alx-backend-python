#!/usr/bin/env python3
""" Async """
import asyncio
import time

wait_n = __import__("1-concurrent_coroutines").wait_n


def measure_time(n: int, max_delay: int) -> float:
    """Async func """
    begin = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    ending = time.perf_counter()
    return (ending - begin) / n
