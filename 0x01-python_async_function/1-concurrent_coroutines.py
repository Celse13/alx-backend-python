#!/usr/bin/env python3
""" Async function """
import asyncio
import random
from typing import List

wait_random = __import__("0-basic_async_syntax").wait_random


async def wait_n(n: int, max_delay: int) -> list:
    """ wait n """"
    delays = []
    for _ in range(n):
        delay = asyncio.create_task(wait_random(max_delay))
        delays.append(delay)
    completed, pending = await asyncio.wait(delays, return_when=asyncio.ALL_COMPLETED)
    return [task.result() for task in completed]
